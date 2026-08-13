"""`music/plan.yaml`, and the wiki counted against it — so nobody counts 105 songs by hand.

Six things are decided here, and every one of them is arithmetic or identity rather than
judgement: a label whose song count does not match `plan.yaml`, a layer-A song with no fact, a
layer-B song that has one, a release year that is not one of the eight anchors, an id used twice,
and an `owed_to:` marker that has outlived the card it names. Whether a name is too close to a real
one stays a human judgement (M-03 narrows the pile; it does not clear it).

**Whether the writing is any good used to be a judgement too, and that is what failed.** The eight
rules of `COMMISSION.md` §12 — the ways an album becomes one song sung eleven times — are counted
in `writing.py`, which is a separate pass over the same files (M-45).

Why this is code: a checker prompt asks a model to count 105 songs across eleven albums, and a
model that miscounts is indistinguishable from a wiki that is wrong (D-054). The counting half
lives here; the reading half stays with the operator.

Nothing here fixes anything. It returns problems, each naming the genre and the number, and
`tests/unit/test_music.py` turns them into a red `make check`.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from station.music import wiki

# `CONSTANTS.md` §1 is the one place the anchor years are written down. They are read out of that
# table rather than copied into code, because two copies of eight numbers is two copies too many.
ANCHOR_COUNT = 8
_ANCHOR_ROW = re.compile(r"^\|\s*\*\*(\d{4})\*\*\s*\|", re.MULTILINE)

# `MUSIC_TASKS.md` card headings — `### M-46 · [agent] lane-rock grows to 110`, and DONE when the
# heading says so. Range headings (`### M-21 … M-29 ·`) are not cards and do not match.
TASKS_FILE = "MUSIC_TASKS.md"
_CARD_HEADING = re.compile(r"^###\s+(M-\d+)\s+·(.*)$", re.MULTILINE)

# The card that gives layer B its own calendar — see `year_layers()` and `COMMISSION.md` §12.
LAYER_B_CALENDAR_CARD = "M-15"


class CheckError(RuntimeError):
    """The check could not run at all — a file it reads is missing or has changed shape."""


class LabelSlice(BaseModel):
    """One label's share of a genre: how many songs, spread over how many bands."""

    label: int
    songs: int = Field(gt=0)
    bands: int = Field(gt=0)


class GenreSlice(BaseModel):
    """One genre's whole allocation across the three layers.

    `labels` may be empty: a form the station does not press has no layer A at all, and every
    band, album and story it owns lives in layer B (`COMMISSION.md` §1, D-068). `owed_to` names
    the card that will bring a written genre up to the numbers here — see `_owed_cards()`.
    """

    title: str
    owed_to: str | None = None
    layer_b_bands: int = Field(ge=0)
    layer_c_figures: int = Field(ge=0)
    labels: list[LabelSlice] = Field(default_factory=list)

    @property
    def songs(self) -> int:
        return sum(s.songs for s in self.labels)

    @property
    def bands(self) -> int:
        return sum(s.bands for s in self.labels)


class Plan(BaseModel):
    """`music/plan.yaml` — the allocation of playable songs across genres and labels."""

    labels: dict[int, str]
    genres: dict[str, GenreSlice]

    @property
    def total_songs(self) -> int:
        return sum(g.songs for g in self.genres.values())

    @property
    def total_bands(self) -> int:
        return sum(g.bands for g in self.genres.values())

    def bands_per_label(self) -> dict[int, int]:
        """Bands each label ends up with. §5 requires at least three, or no retrospective."""
        counts = dict.fromkeys(self.labels, 0)
        for genre in self.genres.values():
            for slice_ in genre.labels:
                counts[slice_.label] += slice_.bands
        return counts

    def songs_per_label(self) -> dict[int, int]:
        counts = dict.fromkeys(self.labels, 0)
        for genre in self.genres.values():
            for slice_ in genre.labels:
                counts[slice_.label] += slice_.songs
        return counts


def load_plan(path: Path) -> Plan:
    """Read and validate `plan.yaml`, or fail naming the file."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise CheckError(f"missing {path} — it is the authority for every count") from None
    except yaml.YAMLError as exc:
        raise CheckError(f"{path} is not valid YAML: {exc}") from None
    return Plan.model_validate(raw)


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


def music_cards(tasks: Path) -> dict[str, bool]:
    """Every music card and whether it is marked DONE, read from `MUSIC_TASKS.md`."""
    try:
        text = tasks.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CheckError(f"missing {tasks} — it is where the music cards are marked DONE") from None
    cards = {number: "**DONE" in rest for number, rest in _CARD_HEADING.findall(text)}
    if not cards:
        raise CheckError(
            f"{tasks} has no card headings. Each one starts `### M-NN ·` and that shape is what "
            f"makes `owed_to:` in plan.yaml readable from here."
        )
    return cards


def _owed_cards(plan: Plan, cards: dict[str, bool]) -> list[Problem]:
    """A genre may be behind the plan while a card owes it songs — but not once that card is DONE.

    This is what stops a re-weight from quietly disabling the count check for good: the marker in
    `plan.yaml` and the card in `MUSIC_TASKS.md` have to be retired in the same edit (D-069).
    """
    out: list[Problem] = []
    for slug, allocation in sorted(plan.genres.items()):
        card = allocation.owed_to
        if card is None:
            continue
        if card not in cards:
            out.append(Problem(slug, f"plan.yaml says it is owed to {card}, which is not a card"))
        elif cards[card]:
            out.append(
                Problem(
                    slug,
                    f"plan.yaml still says it is owed to {card}, and {card} is marked DONE — "
                    f"either the genre now matches the plan and the `owed_to:` line goes, or the "
                    f"card is not finished",
                )
            )
    return out


def _is_written(genre: wiki.GenreWiki) -> bool:
    """A placeholder file has an empty layer A. It is not wrong yet; it is not written yet."""
    return bool(genre.layer_a.bands or genre.layer_a.albums)


def _layer_a_albums(genre: wiki.GenreWiki) -> list[wiki.Album]:
    return [album for album, _, layer in genre.every_album() if layer == "A"]


def _counts(slug: str, genre: wiki.GenreWiki, plan: Plan) -> list[Problem]:
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


def _years(slug: str, genre: wiki.GenreWiki, anchors: list[int], layers: str) -> list[Problem]:
    """§1 of CONSTANTS: a year is only a programme if enough records landed on it."""
    listed = ", ".join(str(year) for year in anchors)
    return [
        Problem(
            slug,
            f'{album.id} "{album.title}" is dated {album.release_year}, which is not one of the '
            f"eight anchor years ({listed})",
        )
        for album, _, layer in genre.every_album()
        if layer in layers and album.release_year not in anchors
    ]


def year_layers(cards: dict[str, bool]) -> str:
    """Which layers the anchors bind — and it changes exactly once, when M-15 lands.

    A programme needs its records clustered, so today every album in both layers sits on an anchor.
    That is also why two hundred years of history happened on eight days. `COMMISSION.md` §12's
    rule 7 is the replacement: after M-15 the anchors bind layer A and layer B carries the rest of
    the calendar. The swap is keyed to the card so there is no window in which neither rule applies.
    """
    if LAYER_B_CALENDAR_CARD not in cards:
        raise CheckError(
            f"{TASKS_FILE} has no {LAYER_B_CALENDAR_CARD}, which is the card that hands layer B "
            f"its own calendar (COMMISSION.md §12 rule 7). It cannot be renumbered away."
        )
    return "A" if cards[LAYER_B_CALENDAR_CARD] else "AB"


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
    plan = load_plan(music / "plan.yaml")
    anchors = anchor_years(music / "CONSTANTS.md")
    wiki_dir = music / wiki.WIKI_DIR
    cards = music_cards(music / TASKS_FILE)
    layers = year_layers(cards)

    problems: list[Problem] = _owed_cards(plan, cards)
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
        if not plan.genres[slug].owed_to:
            problems += _counts(slug, genre, plan)
        problems += _facts(slug, genre)
        problems += _years(slug, genre, anchors, layers)
    return problems + _duplicate_ids(found)
