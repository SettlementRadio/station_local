"""The four values COMMISSION.md §9 puts inside an audio file, and the safe way to write them.

Two commands write these tags — `make music-tag` over the catalogue's takes and `make imaging-tag`
over the station furniture — and the mechanics are identical because the requirement is identical:
**the audio and its manifest will be separated**, by a backup, a move, a hand-off or a rebuilt
volume, and when a stranger holds one mp3 the only thing travelling with it is the file. A file
that cannot say what licence it was made under is a file nobody may broadcast.

What differs between the two is only *where the four values come from* — a per-album `generation:`
block for music (D-062), a licence note plus each file's own Suno timestamp for imaging (D-095) —
and that half stays in `music/tag.py` and `imaging/tag.py`. Everything below is the half that was
about to be copied, which is what I-03 said to make one module of.

**No tagging library.** ffmpeg is already a required system tool and already decodes for
`analyse.py`; it writes ID3 too, mapping any key it does not recognise onto a `TXXX` frame that it
and every tag editor read back unchanged. §22 asks a dependency to save more than ~200 lines, and a
tagging library here would save about thirty (D-084).

**The audio is never re-encoded and the file is never edited in place.** ffmpeg cannot write tags
in place, so each file is copied with `-c copy` — the mp3 bitstream passed through untouched — the
copy's audio checksum and its four tags are checked against the original, and only then does it
replace the original in one atomic move. An interrupted run leaves whole files behind, never a
half-written one. A take costs a Suno sitting to make again and a jingle cannot be re-made at all,
so nothing here trusts a rewrite it has not verified.

**Re-running is a no-op.** A file already carrying the four right values is not rewritten at all.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from station import log

FFPROBE_TIMEOUT_S = 10  # §25 gives ffprobe ten seconds and this is the same read
FFMPEG_TIMEOUT_S = 120  # a remux is a copy, not an encode; a minute of audio takes well under 1s

# The four values COMMISSION.md §9 requires, and the tag key each is written under. Plain uppercase
# keys, which ffmpeg writes as ID3v2 `TXXX` frames and reads back exactly as given. Everything
# already in the file is left alone — Suno's own `comment` carries the generation id and timestamp,
# which is the evidence M-18 verified the music dispatch against and the only way any of the 56
# imaging files can be re-exported from the account. Losing it would cost both.
TAG_AI = "AI_GENERATED"
TAG_MODEL = "AI_MODEL_VERSION"
TAG_LICENCE = "LICENCE_PERIOD"
TAG_DATE = "GENERATION_DATE"
TAG_KEYS = (TAG_AI, TAG_MODEL, TAG_LICENCE, TAG_DATE)

# What happened to one file. `pending` is not a failure: music writes lyrics before its Suno
# sitting, so a song with no audio yet is a card that has not run, not a fault here.
WRITTEN, UNCHANGED, PENDING, FAILED = "written", "unchanged", "pending", "failed"

logger = log.get_logger(job="tagging")


class TagError(RuntimeError):
    """A file could not be tagged, or cannot say what it was made under. Never silent (§25)."""


class Provenance(BaseModel):
    """The four values one file has to carry, whatever resolved them."""

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


def run(command: list[str], timeout: int, path: Path) -> bytes:
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
    output = run(
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
    return run(command, FFMPEG_TIMEOUT_S, path).decode("utf-8", "replace").strip()


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
        run(command, FFMPEG_TIMEOUT_S, path)
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


def apply(path: Path, provenance: Provenance) -> tuple[str, str]:
    """Write the four values into one file, and say what that took: the action and a note.

    The one decision both callers share — already right, write it, or failed — and the one place
    that decides it. A caller turns the pair into whatever row it prints.
    """
    wanted = provenance.tags()
    try:
        if carries(read_tags(path), wanted):
            return UNCHANGED, ""
        write_tags(path, wanted)
    except TagError as exc:
        logger.error("untagged", path=str(path), error=str(exc))
        return FAILED, str(exc)
    logger.debug("tagged", path=str(path), licence=provenance.licence_period)
    return WRITTEN, ""
