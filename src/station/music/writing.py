"""`COMMISSION.md` §12 — the eight writing rules, counted.

`check.py` counts identity and arithmetic: ids, song totals, release years. This module counts the
things that make 500 songs 500 *different* songs, and it exists for one measured reason. Across six
writing sessions the counting rules in `check.py` held perfectly and the prose rules in
`COMMISSION.md` §1 to §11 failed completely — same agents, same instructions. The difference is that
one set went red (M-45, and D-069's closing line). So the quality rules move to the mechanism that
works.

**Nothing here is a new rule.** Rule 5 is §3's swap-the-nouns test, rule 6 is §6's one-fact rule,
rules 1 to 4 are §7's shape rules. Each was already written down and each was already ignored.

**The numbers and the two word lists are read out of §12, never kept here.** A threshold in code and
a threshold in the writer's brief drift apart within a week, and the writer's copy is the one that
gets read. Same reasoning as the anchor years in `check.py`.

A rule may be **owed to a card** (§12): counted, reported, but not fatal until that card is marked
DONE in `MUSIC_TASKS.md` — at which point it goes red, so the card cannot close over undone work.
This is `plan.yaml`'s `owed_to:` mechanism (D-069) applied to prose instead of counts.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from station.music import wiki
from station.music.check import TASKS_FILE, CheckError, Problem, music_cards

COMMISSION_FILE = "COMMISSION.md"
LYRICS_DIR = "production/lyrics"
RULES = (1, 2, 3, 4, 5, 6, 7, 8)

# §12's rule table: `| 1 | more than `40%` of an album's ... | album | `M-47` |`. The threshold is
# the first backticked value in the description; the last column is the card that owes the rule.
_RULE_ROW = re.compile(
    r"^\|\s*([1-8])\s*\|([^|]*)\|[^|]*\|\s*(?:`(M-\d+)`|—)\s*\|\s*$", re.MULTILINE
)
_THRESHOLD = re.compile(r"`(\d+)(%?)`")
_MIN_ALBUM = re.compile(r"counted only on albums of `(\d+)` songs or more")


@dataclass(frozen=True)
class Rules:
    """§12, parsed. `threshold` is a share for the percentage rules and a count for the rest."""

    threshold: dict[int, float]
    owed_to: dict[int, str]
    min_album_songs: int
    world_nouns: tuple[str, ...]
    studio_words: tuple[str, ...]

    def pattern(self, terms: tuple[str, ...]) -> re.Pattern[str]:
        """§12's word lists are matched as written, whole words, any case."""
        longest_first = sorted(terms, key=len, reverse=True)
        return re.compile(r"\b(" + "|".join(re.escape(t) for t in longest_first) + r")\b", re.I)


def _blockquote(text: str, heading: str) -> tuple[str, ...]:
    """The `·`-separated word list under one `### ` heading in §12."""
    body = text.split(f"\n### {heading}", 1)
    if len(body) == 1:
        raise CheckError(f"{COMMISSION_FILE} §12 has no `### {heading}` section")
    quoted = re.search(r"^((?:> [^\n]*\n)+)", body[1], re.MULTILINE)
    if not quoted:
        raise CheckError(f"{COMMISSION_FILE} §12's `{heading}` has no `> ` word list under it")
    joined = " ".join(line.lstrip("> ").strip() for line in quoted.group(1).splitlines())
    return tuple(term.strip() for term in joined.split("·") if term.strip())


def load_rules(commission: Path) -> Rules:
    """Read §12, or fail naming what stopped matching."""
    try:
        text = commission.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CheckError(f"missing {commission} — section 12 holds the writing rules") from None
    thresholds: dict[int, float] = {}
    owed: dict[int, str] = {}
    for number, description, card in _RULE_ROW.findall(text):
        found = _THRESHOLD.search(description)
        if not found:
            raise CheckError(f"{COMMISSION_FILE} §12 rule {number} states no `number` to count to")
        value, percent = found.groups()
        thresholds[int(number)] = int(value) / 100 if percent else int(value)
        if card:
            owed[int(number)] = card
    if sorted(thresholds) != list(RULES):
        raise CheckError(
            f"{COMMISSION_FILE} §12 gives rules {sorted(thresholds)}, not {list(RULES)}. Each row "
            f"reads `| N | … `number` … | over | `M-NN` or — |` and that shape is what makes the "
            f"table readable from here."
        )
    floor = _MIN_ALBUM.search(text)
    if not floor:
        raise CheckError(
            f"{COMMISSION_FILE} §12 no longer says which albums are too short to count"
        )
    return Rules(
        threshold=thresholds,
        owed_to=owed,
        min_album_songs=int(floor.group(1)),
        world_nouns=_blockquote(text, "Rule 5 · the world's own nouns"),
        studio_words=_blockquote(text, "Rule 6 · what counts as a studio anecdote"),
    )


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


def _sections(lyric: str) -> str:
    """A song's shape: its section tags in order, with the numbering and the staging stripped."""
    names = []
    for line in lyric.splitlines():
        tag = _TAG.match(line)
        if tag:
            head = tag.group(1).split(" - ")[0].split(",")[0].strip().lower()
            names.append(_TRAILING_NUMBER.sub("", head))
    return " / ".join(names)


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


def _lyric_rules(music: Path, rules: Rules) -> list[tuple[int, Problem]]:
    """Rules 1 to 5, over `music/production/lyrics/`."""
    nouns = rules.pattern(rules.world_nouns)
    out: list[tuple[int, Problem]] = []
    for album in load_lyrics(music / LYRICS_DIR):
        where = f'{album.album.id} "{album.album.title}"'
        for song in album.songs:
            body = _body(song.lyrics)
            carried = {m.group(0).lower() for m in nouns.finditer(body)}
            if len(carried) < rules.threshold[5]:
                out.append(
                    (
                        5,
                        Problem(
                            album.album.id,
                            f'{song.id} "{song.title}" carries {len(carried)} of the world\'s own '
                            f"nouns, and §12 asks for {rules.threshold[5]:g}. The world supplies "
                            f"the furniture (§3); this lyric would read the same on Earth",
                        ),
                    )
                )
        if len(album.songs) >= rules.min_album_songs:
            out += _album_shares(album, where, rules)
    return out


def _album_shares(album: LyricsAlbum, where: str, rules: Rules) -> list[tuple[int, Problem]]:
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
        (rule, Problem(where, f"{detail} — §12 rule {rule}"))
        for rule, red, detail in counted
        if red
    ]


# --- the wiki ---------------------------------------------------------------------------------


def _studio_facts(wiki_dir: Path, rules: Rules) -> list[tuple[int, Problem]]:
    """Rule 6: a band whose facts are mostly the room has nothing human for a presenter to say."""
    studio = rules.pattern(rules.studio_words)
    out: list[tuple[int, Problem]] = []
    for slug in wiki.written_genres(wiki_dir):
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
                    (
                        6,
                        Problem(
                            slug,
                            f"{names.get(band_id, band_id)} ({band_id}) has {anecdotes} studio "
                            f"anecdotes among {songs} facts — §12 rule 6 allows half",
                        ),
                    )
                )
    return out


def _layer_b_calendar(wiki_dir: Path, rules: Rules) -> list[tuple[int, Problem]]:
    """Rule 7: layer B has no floor to hit, so it is what carries the other two hundred years."""
    years = {
        album.release_year
        for slug in wiki.written_genres(wiki_dir)
        for album, _, layer in wiki.load_genre(wiki_dir / f"{slug}.yaml").every_album()
        if layer == "B"
    }
    if not years or len(years) >= rules.threshold[7]:
        return []
    return [
        (
            7,
            Problem(
                "the wiki",
                f"every layer-B album in it sits on {len(years)} distinct release years, and §12 "
                f"rule 7 asks for {rules.threshold[7]:g}. Two hundred years of music history "
                f"cannot have happened on {len(years)} days",
            ),
        )
    ]


def _cross_genre_bands(wiki_dir: Path, rules: Rules) -> list[tuple[int, Problem]]:
    """Rule 8: nine sealed worlds read as a database. An industry is bands who know each other."""
    slugs = wiki.written_genres(wiki_dir)
    loaded = {slug: wiki.load_genre(wiki_dir / f"{slug}.yaml") for slug in slugs}
    named = {
        slug: {b.name for b in genre.layer_a.bands + genre.layer_b.bands if b.name}
        for slug, genre in loaded.items()
    }
    out: list[tuple[int, Problem]] = []
    for slug in slugs:
        if not named[slug]:
            continue
        text = (wiki_dir / f"{slug}.yaml").read_text(encoding="utf-8")
        foreign = {
            name for other in slugs if other != slug for name in named[other] if name in text
        }
        if len(foreign) < rules.threshold[8]:
            out.append(
                (
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


def check_writing(root: Path) -> list[Problem]:
    """Every writing rule that is both broken and live. An empty list is a green `make check`."""
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
    return [problem for rule, problem in found if _live(rules, cards, rule)]
