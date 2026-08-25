"""File a pile of Suno takes into `music/audio/`, proved against the lyric each one carries.

**The mapping is never inferred from filename order** (D-091). M-18 filed relay-pop's pilot by
sorting the export by timestamp and walking the track list, and M-30 checked that method against the
lyric Suno writes into every file's own tags — and found a song that had never been generated: at one
sitting the style box moved on and the lyric box did not, so what came back in track 9's slot was a
second take of track 8. Under the filename method that file was the right size, in the right place,
with a plausible timestamp, and *Coffee After Turnover* would have entered the catalogue as a record
whose one stated fact describes a performance that does not exist on it.

So this module matches on words and refuses to move anything until the assignment is a **bijection**:
every take claims exactly one song, no song is claimed twice, and every song that was waiting for
audio got some. That is the shape of the failure D-091 found — a duplicate claim and an orphan — and
it is what the thresholds below are for rather than any belief about how good a match "should" be.

**Nothing is deleted and nothing is overwritten.** A take moves to a path that does not yet exist, and
both ends of the move are appended to `music/audio/RAW/dispatch-manifest.json`, so a wrong call can
be walked back from the file that recorded it.

The `take:` blocks in `music/production/lyrics/` are written by hand from that manifest. Those files
carry the words, and a YAML round-trip would flatten every lyric block and drop every comment in
them; the manifest is the machine-readable half and the lyrics file stays the written one.
"""

from __future__ import annotations

import difflib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

from station import log
from station.tagging import FFPROBE_TIMEOUT_S, TagError, read_tags, run

__all__ = [
    "MANIFEST",
    "MIN_SECONDS",
    "Assignment",
    "DispatchError",
    "Plan",
    "Take",
    "Written",
    "append_manifest",
    "commit",
    "duration",
    "file_takes",
    "load_written",
    "plan",
    "prepare",
    "read_pile",
    "sung_words",
]

LYRICS_DIR = "production/lyrics"
AUDIO_DIR = "audio"
RAW_DIR = "audio/RAW"
MANIFEST = "audio/RAW/dispatch-manifest.json"

# A take whose best match is weaker than this, or which does not beat its runner-up by this much,
# stops the whole pile rather than being filed on a guess. Both are floors on *confidence in the
# assignment*, not judgements of the take: Suno rewrites words, drops sections and doubles others,
# and a take can be a poor copy of its lyric and still be unmistakably that lyric and no other.
MIN_SCORE = 0.30
MIN_GAP = 0.20

# COMMISSION.md §7: nothing under 2:00. A download that stopped early carries the whole lyric and
# the whole Suno id in its tags and matches its song perfectly, so the words prove nothing about it
# — M-31 filed an eight-second file into a cornerstone album and only a hand check on durations
# found it. The generation is fine in the account; it is the copy on this disk that is not.
MIN_SECONDS = 120.0

# Two lyrics is the least a bijection can mean anything over: with one, every take "matches" it.
LEAST_COMPARABLE = 2

# Suno returns curly quotes where the lyrics files hold straight ones; one apostrophe, one word.
_CURLY = str.maketrans({"\u2019": "'", "\u2018": "'"})

_TAG_LINE = re.compile(r"^\s*\[")
_NOT_WORD = re.compile(r"[^a-z0-9' ]")
_SUNO_ID = re.compile(r"id=([0-9a-fA-F-]{36})")
_SUNO_CREATED = re.compile(r"created=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z)")

logger = log.get_logger(job="music-dispatch")


class DispatchError(RuntimeError):
    """The pile cannot be filed as it stands. Never silent, never a partial move (§25)."""


def sung_words(lyric: str) -> list[str]:
    """The sung words alone, lowercased. A `[staging]` line is not a lyric and counts for nothing.

    The same reading `writing.py` uses for §12 rules 9 and 10, so "what the take sings" and "what
    the rule counted" are the same words.
    """
    lines = [line for line in lyric.splitlines() if not _TAG_LINE.match(line)]
    body = " ".join(lines).translate(_CURLY)
    return _NOT_WORD.sub(" ", body.lower()).split()


class Written(BaseModel):
    """One song that has words. `filed` says whether it already has a take recorded."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    song_id: str
    album_id: str
    label: str
    title: str
    track_number: int
    words: list[str]
    filed: bool = False

    def destination(self, music: Path) -> Path:
        """`music/audio/<label>/<album>/NN.mp3` — the layout every earlier card filed into."""
        return music / AUDIO_DIR / self.label / self.album_id / f"{self.track_number:02d}.mp3"


@dataclass(frozen=True)
class Take:
    """One file in the pile, and what it says about itself."""

    path: Path
    words: list[str]
    suno_id: str
    created: str
    seconds: float


# One row of `dispatch-manifest.json`: both ends of a move, plus the evidence it was the right one.
ManifestRow = dict[str, str | int | float]


@dataclass(frozen=True)
class Assignment:
    """One take, the song its own words claim, and how safely it claims it."""

    take: Take
    song: Written
    score: float
    gap: float
    runner_up: str


@dataclass(frozen=True)
class Plan:
    """What a whole pile would do. Built before anything moves, and refused as a whole."""

    assignments: list[Assignment]
    unclaimed_songs: list[str]
    problems: list[str]

    @property
    def ok(self) -> bool:
        return not self.problems


def load_written(music: Path, genre: str | None = None) -> list[Written]:
    """Every song that has a lyric, whether or not it already has a take.

    **A pile is matched against all of them and filed against the ones still waiting**, which is not
    the same thing. Matching only against what is waiting means a top-up of one song has exactly one
    candidate, and a candidate set of one turns "which song is this" into a question with no wrong
    answer — the take would be filed as that song whatever it actually contained. Keeping the filed
    songs in the pool costs nothing and is what lets a take that belongs to something already on disk
    say so instead of being forced onto the gap.

    `genre` narrows both halves together, so a lane-rock pile is never compared to relay-pop's words.
    """
    written: list[Written] = []
    for path in sorted((music / LYRICS_DIR).glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        album = raw["album"]
        if genre and album.get("genre") != genre:
            continue
        for song in raw.get("songs", []):
            written.append(
                Written(
                    song_id=song["id"],
                    album_id=album["id"],
                    label=album["label"],
                    title=song["title"],
                    track_number=song["track_number"],
                    words=sung_words(song.get("lyrics", "")),
                    filed=song.get("take") is not None,
                )
            )
    return written


def read_pile(raw_dir: Path) -> list[Take]:
    """Every mp3 under the pile, with the lyric, the vendor id and the timestamp it carries.

    Searched recursively: an export arrives as whatever folder the browser made for it, and asking
    the operator to flatten it first is a step that will one day be done wrong.
    """
    takes: list[Take] = []
    for path in sorted(raw_dir.rglob("*.mp3")):
        tags = {key.lower(): value for key, value in read_tags(path).items()}
        lyric = next((v for k, v in tags.items() if k.startswith("lyrics")), "")
        comment = tags.get("comment", "")
        if not lyric.strip():
            raise DispatchError(
                f"{path} carries no lyric in its own tags, so nothing can prove what it is "
                f"(D-091). Re-export it from the account rather than filing it by name."
            )
        suno = _SUNO_ID.search(comment)
        created = _SUNO_CREATED.search(comment)
        if not suno or not created:
            raise DispatchError(
                f"{path} has no Suno id or creation time in its comment tag — that is the only "
                f"way this take can ever be found in the account again (§9)."
            )
        takes.append(
            Take(
                path=path,
                words=sung_words(lyric),
                suno_id=suno.group(1),
                created=created.group(1),
                seconds=duration(path),
            )
        )
    return takes


def duration(path: Path) -> float:
    """How long the file actually is. What a truncated download gets caught by."""
    output = run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        FFPROBE_TIMEOUT_S,
        path,
    )
    try:
        return float(json.loads(output or b"{}")["format"]["duration"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        raise DispatchError(f"{path}: ffprobe cannot say how long this file is") from None


def _score(take: Take, song: Written) -> float:
    """How much of one take's words are the other's, in order.

    `autojunk` is off deliberately: difflib calls any element appearing in more than 1% of a long
    sequence "junk", which is every common word in a lyric, and a ratio computed with it on is not
    a measure of anything.
    """
    return difflib.SequenceMatcher(None, take.words, song.words, autojunk=False).ratio()


def _best(take: Take, songs: list[Written]) -> tuple[Written, float, float, str]:
    """The song a take's own words claim, and the margin over the next-best claim."""
    ranked = sorted(((_score(take, song), song) for song in songs), key=lambda pair: -pair[0])
    (top, first), (second, runner) = ranked[0], ranked[1]
    return first, top, top - second, runner.song_id


def plan(takes: list[Take], songs: list[Written]) -> Plan:
    """Match the whole pile, then say why it may not be filed — never file half of it.

    Every check here is one of D-091's two failure shapes: a take that claims a song some other take
    claims better, and a song nobody claims at all.
    """
    if len(songs) < LEAST_COMPARABLE:
        raise DispatchError("a pile cannot be proved against fewer than two written lyrics")
    waiting = {song.song_id for song in songs if not song.filed}
    assignments = [Assignment(take, *_best(take, songs)) for take in takes]
    problems: list[str] = []
    for found in assignments:
        where = found.take.path.name
        if found.take.seconds < MIN_SECONDS:
            problems.append(
                f"{where}: {found.take.seconds:.0f}s of audio, and §7 puts nothing under "
                f"{MIN_SECONDS / 60:.0f}:00 on air — the download stopped early. The generation is "
                f"still in the account as {found.take.suno_id}; fetch it again."
            )
        elif found.song.filed:
            problems.append(
                f"{where}: claims {found.song.song_id}, which already has a take recorded. Either "
                f"this is a second copy of a filed song, or the take it belongs to is missing from "
                f"the pile (D-091)"
            )
        elif found.score < MIN_SCORE:
            problems.append(
                f"{where}: closest lyric is {found.song.song_id} at {found.score:.0%}, under the "
                f"{MIN_SCORE:.0%} floor — this take may be of something not written here"
            )
        elif found.gap < MIN_GAP:
            problems.append(
                f"{where}: claims {found.song.song_id} at {found.score:.0%} but "
                f"{found.runner_up} is {found.gap:.0%} behind it — too close to file on"
            )
    claimed = [found.song.song_id for found in assignments]
    for song_id in sorted({s for s in claimed if claimed.count(s) > 1}):
        holders = ", ".join(f.take.path.name for f in assignments if f.song.song_id == song_id)
        problems.append(
            f"{song_id} is claimed by more than one take ({holders}) — at some sitting the lyric "
            f"box did not change when the style box did (D-091)"
        )
    unclaimed = sorted(waiting - set(claimed))
    return Plan(assignments=assignments, unclaimed_songs=unclaimed, problems=problems)


def prepare(music: Path, pile: Path, genre: str | None) -> tuple[Plan, int]:
    """Everything that happens before a file moves: read both sides, match, and say what is wrong.

    One entry point so that the command stays a list of targets (§17) and every caller gets the same
    refusals — including `TagError`, which is what an unreadable file raises and is a reason not to
    file the pile like any other.
    """
    try:
        songs = load_written(music, genre=genre)
        takes = read_pile(pile)
    except TagError as exc:
        raise DispatchError(str(exc)) from None
    if not takes:
        raise DispatchError(f"no mp3 under {pile}")
    waiting = sum(1 for song in songs if not song.filed)
    if not waiting:
        raise DispatchError("every written song already has a take — nothing is waiting for audio")
    return plan(takes, songs), waiting


def commit(music: Path, ready: Plan) -> tuple[int, Path]:
    """File a plan that passed, and record both ends of every move. Refuses a plan that did not."""
    if not ready.ok:
        raise DispatchError("this pile was refused; nothing was moved")
    rows = file_takes(music, ready.assignments)
    return len(rows), append_manifest(music, rows)


def file_takes(music: Path, found: list[Assignment]) -> list[ManifestRow]:
    """Move every take to its song's path and return the manifest rows for what moved.

    Nothing is overwritten: a destination that already holds a file stops the run, because the only
    ways to get here are a song filed twice and a card being run over finished work.
    """
    rows: list[ManifestRow] = []
    for one in found:
        target = one.song.destination(music)
        if target.exists():
            raise DispatchError(f"{target} already exists — refusing to overwrite a filed take")
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(one.take.path, target)
        logger.info(
            "filed", song=one.song.song_id, take=one.take.path.name, score=round(one.score, 3)
        )
        rows.append(
            {
                "song": one.song.song_id,
                "album": one.song.album_id,
                "track": one.song.track_number,
                "file": str(target.relative_to(music.parent)),
                "raw": one.take.path.name,
                "suno_id": one.take.suno_id,
                "created": one.take.created,
                "lyric_match": round(one.score, 4),
            }
        )
    return rows


def append_manifest(music: Path, rows: list[ManifestRow]) -> Path:
    """Add this pile to the dispatch manifest, keeping every row an earlier card wrote."""
    path = music / MANIFEST
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(existing + rows, indent=2) + "\n", encoding="utf-8")
    return path
