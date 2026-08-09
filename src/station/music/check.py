"""Count the wiki against the plan, so nobody counts 105 songs by hand.

Five things are decided here, and every one of them is arithmetic or identity rather than
judgement: a label whose song count does not match `plan.yaml`, a layer-A song with no fact, a
layer-B song that has one, a release year that is not one of the eight anchors, and an id used
twice. Everything else about a genre — whether the bios read well, whether a name is too close to a
real one — is a human judgement and stays one (`COMMISSION.md` §19, and M-03 for the screen).

Why not leave this to `make music-check`: that brief asks a model to count 105 songs across eleven
albums, and a model that miscounts is indistinguishable from a wiki that is wrong. The counting
half moves here; the reading half stays with the operator.

Nothing here fixes anything. It returns problems, each naming the genre and the number, and
`tests/unit/test_brief.py` turns them into a red `make check`.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from station.music import brief, wiki

# `CONSTANTS.md` §1 is the one place the anchor years are written down. They are read out of that
# table rather than copied into code, because two copies of eight numbers is two copies too many.
ANCHOR_COUNT = 8
_ANCHOR_ROW = re.compile(r"^\|\s*\*\*(\d{4})\*\*\s*\|", re.MULTILINE)


class CheckError(RuntimeError):
    """The check could not run at all — a file it reads is missing or has changed shape."""


@dataclass(frozen=True)
class Problem:
    """One thing that is wrong, in the terms the operator would use to fix it."""

    genre: str
    detail: str

    def line(self) -> str:
        return f"{self.genre}: {self.detail}"


def anchor_years(constants: Path) -> list[int]:
    """The eight anchor years, read from `CONSTANTS.md` §1."""
    try:
        text = constants.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CheckError(f"missing {constants} — section 1 holds the anchor years") from None
    years = sorted({int(y) for y in _ANCHOR_ROW.findall(text)})
    if len(years) != ANCHOR_COUNT:
        raise CheckError(
            f"{constants} section 1 gives {len(years)} anchor years, not {ANCHOR_COUNT}. Each row "
            f"starts `| **YYYY** |` and that shape is what makes the table readable from here."
        )
    return years


def _is_written(genre: wiki.GenreWiki) -> bool:
    """A placeholder file has an empty layer A. It is not wrong yet; it is not written yet."""
    return bool(genre.layer_a.bands or genre.layer_a.albums)


def _layer_a_albums(genre: wiki.GenreWiki) -> list[wiki.Album]:
    return [album for album, _, layer in genre.every_album() if layer == "A"]


def _counts(slug: str, genre: wiki.GenreWiki, plan: brief.Plan) -> list[Problem]:
    """§5: a label that does not get its share of songs cannot carry its retrospective."""
    allocation = plan.genres[slug]
    expected = {slice_.label: slice_.songs for slice_ in allocation.labels}
    actual: dict[int, int] = defaultdict(int)
    out: list[Problem] = []
    for album in _layer_a_albums(genre):
        number = album.label_number
        if number is None:
            out.append(
                Problem(
                    slug,
                    f"{album.id} sits on label {album.label!r}, which is not a "
                    f"label number — labels are `label_3` or `3`",
                )
            )
            continue
        actual[number] += len(album.playable_songs)
    for number in sorted(set(expected) | set(actual)):
        want, got = expected.get(number, 0), actual.get(number, 0)
        if want != got:
            name = plan.labels.get(number, "no such label in plan.yaml")
            out.append(
                Problem(
                    slug, f"label {number} ({name}) has {got} playable songs, plan.yaml says {want}"
                )
            )
    total = sum(actual.values())
    if total != allocation.songs:
        out.append(
            Problem(slug, f"{total} playable songs in all, plan.yaml says {allocation.songs}")
        )
    return out


def _facts(slug: str, genre: wiki.GenreWiki) -> list[Problem]:
    """§1: layer A is what the presenters say something about; layer B is what they can only name."""
    out: list[Problem] = []
    for album, _, layer in genre.every_album():
        for song in album.songs:
            has_fact = bool((song.fact or "").strip())
            if layer == "A" and not has_fact:
                out.append(
                    Problem(
                        slug,
                        f'{album.id} track {song.track_number} ({song.id} "{song.title}")'
                        f" has no fact — every layer-A song carries exactly one",
                    )
                )
            elif layer == "B" and has_fact:
                out.append(
                    Problem(
                        slug,
                        f'{album.id} ({song.id} "{song.title}") has a fact — layer B is '
                        f"titles only, and a fact there is effort spent on a record the "
                        f"station will never hold",
                    )
                )
    return out


def _years(slug: str, genre: wiki.GenreWiki, anchors: list[int]) -> list[Problem]:
    """§1 of CONSTANTS: a year is only a programme if enough records landed on it."""
    listed = ", ".join(str(year) for year in anchors)
    return [
        Problem(
            slug,
            f'{album.id} "{album.title}" is dated {album.release_year}, which is not one of the '
            f"eight anchor years ({listed})",
        )
        for album, _, _ in genre.every_album()
        if album.release_year not in anchors
    ]


def _same_entity(uses: list[tuple[str, wiki.Entity]]) -> bool:
    """A label or a session player appears in every genre it touches — that is one entity, not two."""
    return all(entity.shared for _, entity in uses) and (
        len({(entity.kind, entity.name) for _, entity in uses}) == 1
    )


def _duplicate_ids(found: list[tuple[str, wiki.Entity]]) -> list[Problem]:
    """The failure this whole module was written for: genre two overwriting genre one's numbers."""
    by_id: dict[str, list[tuple[str, wiki.Entity]]] = defaultdict(list)
    for slug, entity in found:
        by_id[entity.id].append((slug, entity))
    out: list[Problem] = []
    for id_, uses in sorted(by_id.items()):
        if len(uses) == 1 or _same_entity(uses):
            continue
        where = "; ".join(f'{slug} {e.kind} "{e.name}" ({e.where})' for slug, e in uses)
        out.append(
            Problem(
                uses[0][0],
                f"id {id_} is used {len(uses)} times: {where}. An id is an identity and is never "
                f"reused or renumbered (COMMISSION.md §10) — the new entry takes the next free one",
            )
        )
    return out


def check_wiki(root: Path) -> list[Problem]:
    """Every problem in every written genre. An empty list is a wiki that matches the plan."""
    music = root / "music"
    plan = brief.load_plan(music / "plan.yaml")
    anchors = anchor_years(music / "CONSTANTS.md")
    wiki_dir = music / brief.WIKI_DIR

    problems: list[Problem] = []
    found: list[tuple[str, wiki.Entity]] = []
    for slug in wiki.written_genres(wiki_dir):
        genre = wiki.load_genre(wiki_dir / f"{slug}.yaml")
        found += [(slug, entity) for entity in wiki.defined_ids(genre)]
        if not _is_written(genre):
            continue
        if slug not in plan.genres:
            known = ", ".join(sorted(plan.genres))
            problems.append(Problem(slug, f"has no allocation in plan.yaml, which has: {known}"))
            continue
        problems += _counts(slug, genre, plan)
        problems += _facts(slug, genre)
        problems += _years(slug, genre, anchors)
    return problems + _duplicate_ids(found)
