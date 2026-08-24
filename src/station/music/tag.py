"""Where a take's four licence values come from. The writing itself is `station/tagging.py`.

`COMMISSION.md` §9 asks for the licence period, the generation date, the model version and an AI
marker *inside the file*, and the reason is not tidiness — `station/tagging.py`'s own docstring
carries it, along with every mechanical decision D-084 took. This module is the half that is about
music and nothing else: **which value belongs in which take.**

The values come from the per-album `generation:` block M-17 shaped and M-18 filled in, with each
song's `take:` block read first and the album's block used for anything null there (D-062). A band
generated in one sitting therefore records the four values once and the song blocks stay almost
empty, which is the shape those files are actually written in.

I-03 built the imaging equivalent and found this module's second half copied wholesale, so it moved
to `station/tagging.py` and both callers import it (D-095). The names re-exported below are that
module's — a caller of this one should not have to know where the ffmpeg call lives.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from station.music import analyse
from station.tagging import (
    FAILED,
    PENDING,
    TAG_KEYS,
    UNCHANGED,
    WRITTEN,
    Provenance,
    TagError,
    apply,
    read_tags,
)

# Re-exported deliberately: a caller of this module tags music, and should not have to reach across
# to `station/tagging.py` to name the four keys or read a file back.
__all__ = [
    "AUDIO_DIR",
    "LYRICS_DIR",
    "TAG_KEYS",
    "Provenance",
    "Result",
    "Song",
    "Summary",
    "TagError",
    "load_songs",
    "read_tags",
    "summarise",
    "tag",
    "unclaimed",
]

LYRICS_DIR = "production/lyrics"  # under `music/` — one file per album, keyed by album id
AUDIO_DIR = "audio"


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


# --- one file ---------------------------------------------------------------------------------


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
    return outcome(*apply(song.path, song.provenance))


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
