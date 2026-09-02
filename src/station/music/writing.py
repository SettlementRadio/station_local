"""`COMMISSION.md` §12 — the ten writing rules, counted.

`check.py` counts identity and arithmetic: ids, song totals, release years. This module counts the
things that make 500 songs 500 *different* songs, and it exists for one measured reason. Across six
writing sessions the counting rules in `check.py` held perfectly and the prose rules in
`COMMISSION.md` §1 to §11 failed completely — same agents, same instructions. The difference is that
one set went red (M-45, and D-069's closing line). So the quality rules move to the mechanism that
works.

**Nothing here is a new rule.** Rule 5 is §3's swap-the-nouns test, rule 6 is §6's one-fact rule,
rules 1 to 4 are §7's shape rules, and rules 9 and 10 are §7's duration table read backwards through
the one measurement the pilot produced — 0.76 seconds of take per sung word (M-50, D-088). Each was
already written down and each was already ignored.

**The numbers, the two word lists and the exempt album ids are read out of §12, never kept here** —
`commission.py` does that reading. A threshold in code and a threshold in the writer's brief drift
apart within a week, and the writer's copy is the one that gets read.

A finding may fail to be fatal in two ways, and both are visible on it. A rule may be **owed to a
card** (§12): counted but not fatal until that card is marked DONE in `MUSIC_TASKS.md`, at which
point it goes red so the card cannot close over undone work — `plan.yaml`'s `owed_to:` mechanism
(D-069) applied to prose. And an album may be **exempt**: the pilot's four are exempt from rules 9
and 10 permanently, because the operator has accepted those 45 takes and no card will re-cut them
(D-087). Neither kind is dropped — `count_writing()` returns both, marked, because a rule nobody can
watch working is a rule nobody trusts.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from itertools import pairwise
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from station.music import wiki
from station.music.check import TASKS_FILE, CheckError, Problem, music_cards
from station.music.commission import COMMISSION_FILE, Rules, load_rules

LYRICS_DIR = "production/lyrics"

__all__ = ["Finding", "check_writing", "count_writing", "load_lyrics"]


@dataclass(frozen=True)
class Finding:
    """One rule, broken — and the two reasons `make check` might still stay green on it."""

    rule: int
    problem: Problem
    exempt: bool = False
    fatal: bool = False


# --- the lyrics -------------------------------------------------------------------------------


class LyricSong(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    lyrics: str = ""


class _AlbumRef(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    title: str


class LyricsAlbum(BaseModel):
    """One `music/production/lyrics/<album>.yaml`. Only the words are modelled; prompts are not."""

    model_config = ConfigDict(extra="ignore")

    album: _AlbumRef
    songs: list[LyricSong] = Field(default_factory=list)


def load_lyrics(lyrics_dir: Path) -> list[LyricsAlbum]:
    """Every written album of lyrics, in a stable order. None written yet is not an error."""
    if not lyrics_dir.is_dir():
        return []
    out: list[LyricsAlbum] = []
    for path in sorted(lyrics_dir.glob("*.yaml")):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise CheckError(f"{path} is not valid YAML: {exc}") from None
        try:
            out.append(LyricsAlbum.model_validate(raw))
        except Exception as exc:
            raise CheckError(f"{path} does not match the expected shape:\n{exc}") from None
    return out


_TAG = re.compile(r"^\s*\[([^\]]*)\]")
_TRAILING_NUMBER = re.compile(r"\s*\d+$")
_ECHO = re.compile(r"\([^()\n]*\w[^()\n]*\)")
_THIRD_PERSON = re.compile(r"\b(he|him|his|she|her|hers)\b", re.IGNORECASE)
_PROPER_NAME = re.compile(r"[A-Z][a-z]{2,}")
# A sung word: starts with a letter, and an apostrophe or hyphen inside it does not split it.
_WORD = re.compile(r"[^\W\d_][\w'\u2019-]*")
_VERSE = "verse"

# §7: a lyric at rule 10's floor comes back near 3:36, which is what the remaining 455 have to
# average. The floor itself is read from §12, so a shorter lyric is reported in proportion to it
# rather than against a copy of §7's seconds-per-word.
_FLOOR_TAKE_SEC = 216


def _section_names(lyric: str) -> list[str]:
    """The section tags in order, with the numbering and the staging stripped."""
    names = []
    for line in lyric.splitlines():
        tag = _TAG.match(line)
        if tag:
            head = tag.group(1).split(" - ")[0].split(",")[0].strip().lower()
            names.append(_TRAILING_NUMBER.sub("", head))
    return names


def _sections(lyric: str) -> str:
    """A song's shape, as one string — what rule 1 counts repeats of."""
    return " / ".join(_section_names(lyric))


def _body(lyric: str) -> str:
    """The sung words, with the bracketed staging tags removed — a tag is not a lyric."""
    return "\n".join(line for line in lyric.splitlines() if not _TAG.match(line))


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", text.lower())).strip()


def _has_named_character(body: str) -> bool:
    """A capital where a sentence did not just end is a name, not the start of a line."""
    for line in body.splitlines():
        words = line.split()
        for before, word in pairwise(words):
            if before.endswith((".", "!", "?", ":")):
                continue
            if _PROPER_NAME.fullmatch(word.strip(",.!?;:'\"-")):
                return True
    return False


def _take(words: float, rules: Rules) -> str:
    """What §7 says a lyric of this length comes back as, scaled off rule 10's own floor."""
    seconds = round(_FLOOR_TAKE_SEC * words / rules.threshold[10])
    return f"{int(seconds) // 60}:{int(seconds) % 60:02d}"


def _song_rules(
    album_id: str, song: LyricSong, rules: Rules, nouns: re.Pattern[str]
) -> list[Finding]:
    """Rules 5, 9 and 10 — the three counted over one song rather than over an album."""
    body = _body(song.lyrics)
    named = f'{song.id} "{song.title}"'
    carried = {m.group(0).lower() for m in nouns.finditer(body)}
    verses = sum(1 for name in _section_names(song.lyrics) if name.startswith(_VERSE))
    words = len(_WORD.findall(body))
    counted: list[tuple[int, bool, str]] = [
        (
            5,
            len(carried) < rules.threshold[5],
            f"carries {len(carried)} of the world's own nouns, and §12 asks for "
            f"{rules.threshold[5]:g}. The world supplies the furniture (§3); this lyric would "
            f"read the same on Earth",
        ),
        (
            9,
            verses < rules.threshold[9],
            f"has {verses} verse section(s), and §12 rule 9 asks for {rules.threshold[9]:g}",
        ),
        (
            10,
            words < rules.threshold[10],
            f"is {words} sung words, and §12 rule 10 asks for {rules.threshold[10]:g} — this take "
            f"comes back near {_take(words, rules)}, and the hour needs "
            f"{_take(rules.threshold[10], rules)} (§7)",
        ),
    ]
    return [
        Finding(rule, Problem(album_id, f"{named} {detail}"))
        for rule, red, detail in counted
        if red
    ]


def _is_a_stub(album: LyricsAlbum, collections: set[str]) -> bool:
    """A collection album whose lyrics file carries no lyrics — §12 has no claim on it.

    The takes in a collection were generated before the commission existed, so there is no written
    lyric and inventing one would be a lie about what the take sings; the file exists only so
    `tag.py` can find the provenance (M-54). A *genre* album with the same emptiness is a genre
    somebody did not write, and every rule below still goes red on it.
    """
    return album.album.id in collections and not any(song.lyrics.strip() for song in album.songs)


def _lyric_rules(music: Path, rules: Rules) -> list[Finding]:
    """Rules 1 to 5 and 9 to 10, over `music/production/lyrics/`."""
    nouns = rules.pattern(rules.world_nouns)
    collections = wiki.collection_albums(music / wiki.WIKI_DIR)
    out: list[Finding] = []
    for album in load_lyrics(music / LYRICS_DIR):
        if _is_a_stub(album, collections):
            continue
        where = f'{album.album.id} "{album.album.title}"'
        exempt = album.album.id in rules.exempt_albums
        for song in album.songs:
            out += [
                replace(found, exempt=exempt and found.rule in (9, 10))
                for found in _song_rules(album.album.id, song, rules, nouns)
            ]
        if len(album.songs) >= rules.min_album_songs:
            out += _album_shares(album, where, rules)
    return out


def _album_shares(album: LyricsAlbum, where: str, rules: Rules) -> list[Finding]:
    """Rules 1 to 4: the four ways an album turns into one song sung eleven times."""
    total = len(album.songs)
    shape, repeated = Counter(_sections(s.lyrics) for s in album.songs).most_common(1)[0]
    echoed = sum(1 for s in album.songs if _ECHO.search(_body(s.lyrics)))
    hooked = sum(1 for s in album.songs if _flat(s.title) in _flat(_body(s.lyrics)))
    peopled = sum(
        1
        for s in album.songs
        if _THIRD_PERSON.search(_body(s.lyrics)) or _has_named_character(_body(s.lyrics))
    )
    counted: list[tuple[int, bool, str]] = [
        (
            1,
            repeated / total > rules.threshold[1],
            f"{repeated} of {total} songs are {shape or 'untagged'}",
        ),
        (
            2,
            peopled < rules.threshold[2],
            f"only {peopled} of {total} songs have a third person in them",
        ),
        (
            3,
            echoed / total > rules.threshold[3],
            f"{echoed} of {total} songs use the echoed answer",
        ),
        (
            4,
            hooked / total > rules.threshold[4],
            f"{hooked} of {total} songs are titled after their own hook",
        ),
    ]
    return [
        Finding(rule, Problem(where, f"{detail} — §12 rule {rule}"))
        for rule, red, detail in counted
        if red
    ]


# --- the wiki ---------------------------------------------------------------------------------


def _studio_facts(wiki_dir: Path, rules: Rules) -> list[Finding]:
    """Rule 6: a band whose facts are mostly the room has nothing human for a presenter to say."""
    studio = rules.pattern(rules.studio_words)
    out: list[Finding] = []
    for slug in wiki.written_slugs(wiki_dir):
        genre = wiki.load_genre(wiki_dir / f"{slug}.yaml")
        tally: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        names: dict[str, str] = {b.id: b.name for b in genre.layer_a.bands}
        for album, band, layer in genre.every_album():
            if layer != "A":
                continue
            band_id = album.band or (band.id if band else "?")
            for song in album.playable_songs:
                tally[band_id][1] += 1
                tally[band_id][0] += bool(studio.search(song.fact or ""))
        for band_id, (anecdotes, songs) in sorted(tally.items()):
            if songs and anecdotes / songs > rules.threshold[6]:
                out.append(
                    Finding(
                        6,
                        Problem(
                            slug,
                            f"{names.get(band_id, band_id)} ({band_id}) has {anecdotes} studio "
                            f"anecdotes among {songs} facts — §12 rule 6 allows half",
                        ),
                    )
                )
    return out


def _layer_b_calendar(wiki_dir: Path, rules: Rules) -> list[Finding]:
    """Rule 7: layer B has no floor to hit, so it is what carries the other two hundred years."""
    years = {
        album.release_year
        for slug in wiki.written_slugs(wiki_dir)
        for album, _, layer in wiki.load_genre(wiki_dir / f"{slug}.yaml").every_album()
        if layer == "B"
    }
    if not years or len(years) >= rules.threshold[7]:
        return []
    return [
        Finding(
            7,
            Problem(
                "the wiki",
                f"every layer-B album in it sits on {len(years)} distinct release years, and §12 "
                f"rule 7 asks for {rules.threshold[7]:g}. Two hundred years of music history "
                f"cannot have happened on {len(years)} days",
            ),
        )
    ]


def _cross_genre_bands(wiki_dir: Path, rules: Rules) -> list[Finding]:
    """Rule 8: nine sealed worlds read as a database. An industry is bands who know each other.

    The one rule collections stay out of, on both sides. §12 counts it over a *genre file*, and the
    thing it is asking for is that the nine commissioned forms know each other — a shelf of unsigned
    records is not a tenth world to be sealed, and letting it supply the names would answer the rule
    without any of the nine having done anything.
    """
    slugs = wiki.written_genres(wiki_dir)
    loaded = {slug: wiki.load_genre(wiki_dir / f"{slug}.yaml") for slug in slugs}
    named = {
        slug: {b.name for b in genre.layer_a.bands + genre.layer_b.bands if b.name}
        for slug, genre in loaded.items()
    }
    out: list[Finding] = []
    for slug in slugs:
        if not named[slug]:
            continue
        text = (wiki_dir / f"{slug}.yaml").read_text(encoding="utf-8")
        foreign = {
            name for other in slugs if other != slug for name in named[other] if name in text
        }
        if len(foreign) < rules.threshold[8]:
            out.append(
                Finding(
                    8,
                    Problem(
                        slug,
                        f"names {len(foreign)} bands that live in other genre files, and §12 rule "
                        f"8 asks for {rules.threshold[8]:g} — a genre nobody else mentions is a "
                        f"sealed world, not a scene",
                    ),
                )
            )
    return out


def _live(rules: Rules, cards: dict[str, bool], rule: int) -> bool:
    """A rule owed to a card is counted but not fatal until that card claims to be finished."""
    card = rules.owed_to.get(rule)
    if card is None:
        return True
    if card not in cards:
        raise CheckError(
            f"{COMMISSION_FILE} §12 owes rule {rule} to {card}, which is not a card in "
            f"{TASKS_FILE} — either the card was renumbered, or the rule is now nobody's"
        )
    return cards[card]


def count_writing(root: Path) -> list[Finding]:
    """Every broken rule, including the ones nothing goes red on — each marked with why.

    The exempt and the owed findings are the point of returning them: M-50's word floor can be
    watched working on the pilot's four albums today, which are the only lyrics that exist and the
    only ones it will never apply to.
    """
    music = root / "music"
    rules = load_rules(music / COMMISSION_FILE)
    cards = music_cards(music / TASKS_FILE)
    wiki_dir = music / wiki.WIKI_DIR
    found = (
        _lyric_rules(music, rules)
        + _studio_facts(wiki_dir, rules)
        + _layer_b_calendar(wiki_dir, rules)
        + _cross_genre_bands(wiki_dir, rules)
    )
    return [replace(f, fatal=not f.exempt and _live(rules, cards, f.rule)) for f in found]


def check_writing(root: Path) -> list[Problem]:
    """Every writing rule that is broken and red. An empty list is a green `make check`."""
    return [f.problem for f in count_writing(root) if f.fatal]
