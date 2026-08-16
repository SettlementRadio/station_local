"""Every audio file carries its own licence period, generation date, model version and AI marker.

COMMISSION.md §9 asks for those four values *inside the file*, and the reason is not tidiness.
**The audio and the wiki will be separated** — by a backup, a move, a hand-off, a rebuilt volume —
and `music/audio/` is gitignored while the lyrics files are not. When a stranger, or the operator
in two years, holds one mp3, the only thing travelling with it is the file. A take that cannot say
what licence it was made under is a take nobody may broadcast.

Where the values come from: the per-album `generation:` block M-17 shaped and M-18 filled in, with
each song's `take:` block read first and the album's block used for anything null there (D-062).
A band generated in one sitting therefore records the four values once and the song blocks stay
almost empty, which is the shape those files are actually written in.

**No new dependency.** ffmpeg is already a required system tool and already decodes for
`analyse.py`; it writes ID3 too, mapping any key it does not recognise onto a `TXXX` frame that it
and every tag editor read back unchanged. §22 asks a dependency to save more than ~200 lines, and a
tagging library here would save about thirty.

**The audio is never re-encoded and the file is never edited in place.** ffmpeg cannot write tags
in place, so each take is copied with `-c copy` — the mp3 bitstream passed through untouched — the
copy is checked against the original packet for packet, and only then does it replace the original
in one atomic move. An interrupted run leaves whole files behind, never a half-written one. A take
costs a Suno sitting to make again, so nothing here trusts a rewrite it has not verified.

**Re-running is a no-op.** A file already carrying the four right values is not rewritten at all,
which is what lets M-39 run this after every genre rather than once at the end of 500 songs.
"""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Iterable
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from station import log
from station.music import analyse

LYRICS_DIR = "production/lyrics"  # under `music/` — one file per album, keyed by album id
AUDIO_DIR = "audio"

FFPROBE_TIMEOUT_S = 10  # §25 gives ffprobe ten seconds and this is the same read
FFMPEG_TIMEOUT_S = 120  # a remux is a copy, not an encode; a minute of audio takes well under 1s

# The four values COMMISSION.md §9 requires, and the tag key each is written under. Plain uppercase
# keys, which ffmpeg writes as ID3v2 `TXXX` frames and reads back exactly as given. Everything
# already in the file is left alone — Suno's own `comment` carries the generation id and timestamp
# that M-18 verified the whole dispatch against, and losing it would cost that evidence.
TAG_AI = "AI_GENERATED"
TAG_MODEL = "AI_MODEL_VERSION"
TAG_LICENCE = "LICENCE_PERIOD"
TAG_DATE = "GENERATION_DATE"
TAG_KEYS = (TAG_AI, TAG_MODEL, TAG_LICENCE, TAG_DATE)

# What happened to one file. `pending` is not a failure: the lyrics for a genre are written before
# its Suno sitting, so a song with no audio yet is a card that has not run, not a fault here.
WRITTEN, UNCHANGED, PENDING, FAILED = "written", "unchanged", "pending", "failed"

logger = log.get_logger(job="music-tag")


class TagError(RuntimeError):
    """A file could not be tagged, or a song cannot say what it was made under. Never silent."""


class Provenance(BaseModel):
    """The four values one file has to carry, resolved song-first and album-second (D-062)."""

    model_config = ConfigDict(protected_namespaces=())

    licence_period: str
    generated_on: str
    model_version: str
    ai_generated: bool

    def tags(self) -> dict[str, str]:
        """The four values as the file's own tags."""
        return {
            TAG_AI: "true" if self.ai_generated else "false",
            TAG_MODEL: self.model_version,
            TAG_LICENCE: self.licence_period,
            TAG_DATE: self.generated_on,
        }


class Song(BaseModel):
    """One song's audio file and the provenance that belongs inside it."""

    album_id: str
    song_id: str
    title: str
    track_number: int
    path: Path
    provenance: Provenance


class Result(BaseModel):
    """What one pass did to one file, and why when it did nothing."""

    album_id: str
    song_id: str
    track_number: int
    path: str
    action: str  # written | unchanged | pending | failed
    note: str = ""


class Summary(BaseModel):
    """A whole pass, counted in the terms the card's check is written in."""

    written: int
    unchanged: int
    pending: int
    failed: int
    unclaimed: list[str]

    @property
    def carrying_tags(self) -> int:
        """Files that now hold all four values, whether this run wrote them or found them."""
        return self.written + self.unchanged

    @property
    def complete(self) -> bool:
        """True when nothing under `music/audio/` is left without its four values."""
        return not self.failed and not self.unclaimed


# --- the lyrics files -----------------------------------------------------------------------


class _Block(BaseModel):
    """The fields of a `generation:` or a `take:` block that decide the four tags."""

    model_config = ConfigDict(extra="ignore", protected_namespaces=())

    licence_period: str | None = None
    generated_on: str | None = None
    model_version: str | None = None
    ai_generated: bool | None = None

    @field_validator("generated_on", mode="before")
    @classmethod
    def _as_iso(cls, value: object) -> str | None:
        """YAML reads an unquoted `2026-08-15` as a date and a quoted one as text. One day, one tag."""
        if value is None:
            return None
        return value.isoformat() if isinstance(value, date) else str(value)


class _Take(_Block):
    file: str | None = None  # written from the repository root, as M-18's dispatch recorded it


class _SongEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    track_number: int
    take: _Take | None = None


class _AlbumEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str


class _AlbumFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    album: _AlbumEntry
    generation: _Block | None = None
    songs: list[_SongEntry]


def load_songs(music_dir: Path, album: str | None = None) -> list[Song]:
    """Every song a lyrics file records a take for, with its four values already resolved.

    Driven from the lyrics files rather than from the disk because the disk holds audio and nothing
    else: the licence a file was made under is only written down here.
    """
    directory = music_dir / LYRICS_DIR
    files = sorted(directory.glob("*.yaml"))
    if not files:
        raise TagError(
            f"no lyrics files under {directory} — nothing records what the audio was made under"
        )
    songs: list[Song] = []
    for path in files:
        parsed = _read_album(path)
        if album is not None and parsed.album.id != album:
            continue
        songs += _album_songs(music_dir, path, parsed)
    return songs


def _read_album(path: Path) -> _AlbumFile:
    """One lyrics file, validated on the way in so a missing field names the file (§31)."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise TagError(f"{path.name}: could not be read as YAML — {exc}") from None
    try:
        return _AlbumFile.model_validate(raw)
    except ValidationError as exc:
        raise TagError(f"{path.name}: not the shape al_001.yaml fixes — {exc}") from None


def _album_songs(music_dir: Path, path: Path, parsed: _AlbumFile) -> list[Song]:
    """The songs of one album that have a take recorded. A song with no take has no audio to tag."""
    songs = []
    for entry in parsed.songs:
        if entry.take is None or not entry.take.file:
            continue
        songs.append(
            Song(
                album_id=parsed.album.id,
                song_id=entry.id,
                title=entry.title,
                track_number=entry.track_number,
                path=music_dir.parent / entry.take.file,
                provenance=_resolve(path.name, entry, parsed.generation),
            )
        )
    return songs


def _resolve(where: str, entry: _SongEntry, album: _Block | None) -> Provenance:
    """The song's `take:` first, the album's `generation:` for anything null there (D-062)."""
    blocks = [block for block in (entry.take, album) if block is not None]
    values = {field: _first(blocks, field) for field in _Block.model_fields}
    missing = [field for field, value in values.items() if value is None]
    if missing:
        raise TagError(
            f"{where}: {entry.id} has no {', '.join(missing)} in its take: block or in the album's "
            "generation: block — the file would not be able to say what it was made under"
        )
    if values["ai_generated"] is not True:
        raise TagError(
            f"{where}: {entry.id} declares ai_generated false. Every take under music/audio/ is "
            "machine-generated and the file has to say so (COMMISSION.md §9)"
        )
    return Provenance.model_validate(values)


def _first(blocks: list[_Block], field: str) -> object | None:
    """The first block that fills `field` in. This is the whole of D-062's resolution rule."""
    for block in blocks:
        value: object = getattr(block, field)
        if value is not None:
            return value
    return None


# --- the files themselves -------------------------------------------------------------------


def _run(command: list[str], timeout: int, path: Path) -> bytes:
    """One external call: explicit timeout, and a failure that names the file rather than a stack."""
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise TagError(f"{path}: {command[0]} did not finish inside {timeout}s") from None
    except FileNotFoundError:
        raise TagError(
            f"{command[0]} is not installed — `make setup`, then `make doctor`"
        ) from None
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
        raise TagError(f"{path}: {command[0]} failed — {detail[-1] if detail else 'no output'}")
    return result.stdout


def read_tags(path: Path) -> dict[str, str]:
    """Every tag the file carries, as ffprobe reads it back. What the operator's check reads."""
    output = _run(
        ["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "json", str(path)],
        FFPROBE_TIMEOUT_S,
        path,
    )
    try:
        payload = json.loads(output or b"{}")
    except json.JSONDecodeError:
        raise TagError(f"{path}: ffprobe returned nothing readable") from None
    tags = payload.get("format", {}).get("tags", {})
    return {str(key): str(value) for key, value in tags.items()}


def audio_md5(path: Path) -> str:
    """The checksum of the audio packets alone — tags excluded, so tagging must not change it."""
    command = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(path)]
    command += ["-map", "0:a", "-c", "copy", "-f", "md5", "-"]
    return _run(command, FFMPEG_TIMEOUT_S, path).decode("utf-8", "replace").strip()


def write_tags(path: Path, tags: dict[str, str]) -> None:
    """Add `tags`, leaving every audio packet and every tag already there exactly where it was.

    The tagged copy is written beside the original, checked against it, and moved over it in one
    `os.replace` — atomic on the same filesystem. At no instant does the path hold half a file.
    """
    fingerprint = audio_md5(path)
    temp = path.with_name(f".{path.stem}.tagging{path.suffix}")
    metadata = [part for key, value in tags.items() for part in ("-metadata", f"{key}={value}")]
    command = ["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(path)]
    command += ["-map", "0", "-c", "copy", *metadata, str(temp)]
    try:
        _run(command, FFMPEG_TIMEOUT_S, path)
        _verify(temp, tags, fingerprint, path)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _verify(temp: Path, tags: dict[str, str], fingerprint: str, original: Path) -> None:
    """Refuse to replace a good file with a bad one: the same audio, and the four values readable."""
    if audio_md5(temp) != fingerprint:
        raise TagError(f"{original}: the tagged copy does not hold the same audio — original kept")
    written = read_tags(temp)
    wrong = [key for key, value in tags.items() if written.get(key) != value]
    if wrong:
        raise TagError(f"{original}: {', '.join(wrong)} did not survive the write — original kept")


def carries(present: dict[str, str], wanted: dict[str, str]) -> bool:
    """Whether a file already says all four things it has to say."""
    return all(present.get(key) == value for key, value in wanted.items())


def tag(song: Song) -> Result:
    """Write the four values into one song's file, or say exactly why it was left alone."""

    def outcome(action: str, note: str = "") -> Result:
        return Result(
            album_id=song.album_id,
            song_id=song.song_id,
            track_number=song.track_number,
            path=str(song.path),
            action=action,
            note=note,
        )

    if not song.path.is_file():
        return outcome(PENDING, "no audio file yet")
    wanted = song.provenance.tags()
    try:
        if carries(read_tags(song.path), wanted):
            return outcome(UNCHANGED)
        write_tags(song.path, wanted)
    except TagError as exc:
        logger.error("untagged", path=str(song.path), error=str(exc))
        return outcome(FAILED, str(exc))
    logger.debug("tagged", path=str(song.path), licence=song.provenance.licence_period)
    return outcome(WRITTEN)


def unclaimed(audio_root: Path, songs: Iterable[Song]) -> list[Path]:
    """Audio on disk that no lyrics file claims — the files a pass like this leaves untagged.

    Without this the command could report forty-five successes over a directory holding fifty, and
    the five nobody wrote down would be exactly the five with no licence attached (§25).
    """
    if not audio_root.is_dir():
        return []
    claimed = {song.path.resolve() for song in songs}
    return [path for path in analyse.audio_files(audio_root) if path.resolve() not in claimed]


def summarise(results: list[Result], left_out: list[Path]) -> Summary:
    """What the pass did, counted."""
    counted = {
        action: sum(1 for r in results if r.action == action)
        for action in (WRITTEN, UNCHANGED, PENDING, FAILED)
    }
    return Summary(
        written=counted[WRITTEN],
        unchanged=counted[UNCHANGED],
        pending=counted[PENDING],
        failed=counted[FAILED],
        unclaimed=[str(path) for path in left_out],
    )
