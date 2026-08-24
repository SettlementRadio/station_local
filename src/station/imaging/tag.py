"""Where a jingle's four licence values come from. The writing itself is `station/tagging.py`.

§9 says provenance is mandatory in the imaging file itself — licence period, generation date, model
version and an AI marker — on the same reasoning `COMMISSION.md` §9 gives for music. The 56 files
are the sharpest case for it in the project: they were carried over from a previous attempt, they
are not in git, and their whole manifest is a `README.md` written for a person. Separate one from
that folder and today it says only "made with suno".

**Imaging has no per-album metadata block, so the four values come from two places** (D-095):

- **The licence note** — `music/licence-evidence/2026-07-suno-licence-note.md` — for the period and
  the model version. Both are facts about the whole pile rather than about one file: the account was
  on Pro throughout July 2026 and every one of the 56 was generated on v5.5. The note is where I-01
  recorded the model version, and reading it here rather than copying the value means a correction
  to the note reaches the files.
- **Each file's own Suno `comment` tag** for the generation date. Suno writes
  `created=2026-07-08T10:03:15Z` into every export, so the date is a fact the file already carries
  and nothing here has to remember or guess. **A file that does not carry one is a failure, never a
  guessed date** (§25): a wrong generation date in an audio file is evidence that reads as fact.

**The two are cross-checked.** A file whose Suno date falls outside the month the note says it
covers is refused by name. That is the case where a later pile gets tagged with an earlier pile's
terms, which is the one mistake this command could make that nobody would ever notice.

`ai_generated` is not read from anywhere and is not configurable. Everything under this folder is
Suno output and §18 requires the marker; music refuses a take that declares otherwise, and here
there is no field to declare it with.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel

from station.tagging import (
    FAILED,
    TAG_KEYS,
    UNCHANGED,
    WRITTEN,
    Provenance,
    TagError,
    apply,
    read_tags,
)

# Re-exported deliberately: a caller of this module tags imaging, and should not have to reach
# across to `station/tagging.py` to name the four keys or read a file back.
__all__ = [
    "LICENCE_NOTE",
    "TAG_KEYS",
    "Note",
    "Provenance",
    "Result",
    "Summary",
    "TagError",
    "read_note",
    "read_tags",
    "summarise",
    "tag",
]

# Under `music/`. The pile is one generation month and the note that covers it is named after that
# month, the way `COMMISSION.md` §9 files evidence. A pile generated in another month needs its own
# note, and until then the month check below refuses its files by name rather than mis-tagging them.
LICENCE_NOTE = Path("licence-evidence") / "2026-07-suno-licence-note.md"

# The rows of the note's table this reads, by their exact left-hand label. Narrow on purpose: a
# loose match over a prose document is how a plausible wrong value gets into 56 files at once.
ROW_MONTH = "Covers generation month"
ROW_MODEL = "Model version used"
ROW_PERIOD = "`licence_period` to record per asset"

MONTH = re.compile(r"^\d{4}-\d{2}$")
PERIOD = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
# Suno's own export, in three precisions across the 56 — `…T10:03:15Z`, `…T08:43:28.694Z`,
# `…T18:55:23.185912Z`. Only the day is wanted and only the day is matched.
CREATED = re.compile(r"created=(\d{4}-\d{2}-\d{2})T")

COLUMNS = 2  # the note's tables are label | value, and a row of any other shape is not one of them


class Note(BaseModel):
    """What the licence note states about a whole generation month."""

    month: str  # `2026-07` — the month every file in the pile has to have been generated in
    licence_period: str  # `suno-pro-2026-07` — what each asset records as its licence
    model_version: str  # `v5.5` — I-01's answer, and the only place it is written down


class Result(BaseModel):
    """What one pass did to one file, and what that file now says."""

    name: str
    path: str
    action: str  # written | unchanged | failed
    note: str = ""
    provenance: Provenance | None = None  # None only where the file could not say when it was made


class Summary(BaseModel):
    """A whole pass, counted in the terms the card's check is written in."""

    written: int
    unchanged: int
    failed: int

    @property
    def carrying_tags(self) -> int:
        """Files that now hold all four values, whether this run wrote them or found them."""
        return self.written + self.unchanged

    @property
    def complete(self) -> bool:
        """True when every file in the pile carries its four values. Anything else exits red."""
        return not self.failed


# --- the licence note ---------------------------------------------------------------------------


def read_note(path: Path) -> Note:
    """The three values the note states about the whole pile, or a failure naming the missing row.

    The note is markdown written for a person, so the parse is deliberately literal: find the table
    row whose first cell is exactly one of the three labels, strip the emphasis and backticks the
    document decorates values with, and take the first word. Anything else — a renamed row, a value
    that is prose rather than a value — is a loud failure here rather than 56 wrong tags.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TagError(f"{path}: the licence note could not be read — {exc}") from None

    rows = _rows(text)
    month = _value(path, rows, ROW_MONTH, MONTH, "a generation month like 2026-07")
    period = _value(path, rows, ROW_PERIOD, PERIOD, "a licence period like suno-pro-2026-07")
    version = _value(path, rows, ROW_MODEL, VERSION, "a model version like v5.5")
    if not period.endswith(month):
        raise TagError(
            f"{path}: the note covers {month} but records the licence period as {period}. "
            "One of the two rows is wrong and every asset would carry the wrong one"
        )
    return Note(month=month, licence_period=period, model_version=version)


def _rows(text: str) -> dict[str, str]:
    """The note's two-column table rows, keyed by their first cell exactly as written."""
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == COLUMNS and cells[0] and cells[0] not in rows:
            rows[cells[0]] = cells[1]
    return rows


def _value(path: Path, rows: dict[str, str], label: str, shape: re.Pattern[str], want: str) -> str:
    """One row's value: the first word, undecorated, and only if it looks like what it should be."""
    if label not in rows:
        raise TagError(
            f"{path}: no row named `{label}` — that row is where {want} is recorded, and without "
            "it no imaging file can say what it was made under"
        )
    first = rows[label].replace("**", "").replace("`", "").strip().split(" ", 1)[0]
    if not shape.match(first):
        raise TagError(
            f"{path}: the `{label}` row reads {rows[label]!r}, which does not start with {want}"
        )
    return first


# --- one file -----------------------------------------------------------------------------------


def generated_on(path: Path) -> str:
    """The day Suno made this file, read from the `comment` tag Suno itself wrote.

    Never inferred from the filesystem. A copied folder carries new mtimes and the same audio, and
    a generation date is the one value here that a plausible guess would corrupt invisibly.
    """
    for value in read_tags(path).values():
        found = CREATED.search(value)
        if found:
            return found.group(1)
    raise TagError(
        f"{path.name}: no `created=` in any tag — Suno writes one into every export, so this file "
        "has been re-encoded or stripped and its generation date is no longer knowable from it"
    )


def provenance(path: Path, note: Note) -> Provenance:
    """The four values for one file: two from the note, the date from the file, the marker fixed."""
    day = generated_on(path)
    if not day.startswith(note.month):
        raise TagError(
            f"{path.name}: generated {day}, but {LICENCE_NOTE.name} covers {note.month}. "
            "Tagging it would record terms that were never checked against this file"
        )
    return Provenance(
        licence_period=note.licence_period,
        generated_on=day,
        model_version=note.model_version,
        ai_generated=True,
    )


def tag(path: Path, note: Note) -> Result:
    """Write the four values into one piece of imaging, or say exactly why it was left alone."""
    try:
        values = provenance(path, note)
    except TagError as exc:
        return Result(name=path.stem, path=str(path), action=FAILED, note=str(exc))
    action, why = apply(path, values)
    return Result(name=path.stem, path=str(path), action=action, note=why, provenance=values)


def summarise(results: list[Result]) -> Summary:
    """What the pass did, counted."""
    counted = {
        action: sum(1 for r in results if r.action == action)
        for action in (WRITTEN, UNCHANGED, FAILED)
    }
    return Summary(written=counted[WRITTEN], unchanged=counted[UNCHANGED], failed=counted[FAILED])
