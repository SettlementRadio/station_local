"""`make imaging-tag` — the two reads a wrong licence would come from.

No test writes a tag. ffmpeg and ffprobe are two calls §29 does not want a test of, and the write
already refuses to replace a file whose audio checksum or four tags did not survive the copy — a
check that runs on every one of the 56 files rather than once in CI.

What is worth testing is where imaging's four values come from, because unlike music there is no
per-song metadata block to get them wrong in: the licence period and the model version are parsed
out of a **markdown note written for a person**, and the generation date is parsed out of a tag
**Suno wrote**. Neither is a schema. A loose parse over either is how one plausible wrong value
reaches 56 files at once, and both are read again below against the real files (D-095).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from station.imaging import tag
from station.tagging import TAG_KEYS

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "music" / tag.LICENCE_NOTE
APPROVED = ROOT / "music" / "jingles" / "approved"


def _pile() -> list[Path]:
    """The 56 files, where they are today. Empty in CI: §4 keeps audio out of git."""
    return sorted(APPROVED.glob("*.mp3"))


NOTE_TEXT = f"""# a note
| | |
|---|---|
| {tag.ROW_MONTH} | 2026-07 |
| {tag.ROW_MODEL} | **v5.5** — operator, 2026-08-23. The same model the 45 songs record |
| {tag.ROW_PERIOD} | `suno-pro-2026-07` |
| Complete? | **Yes** |
"""


def _note(text: str, tmp_path: Path) -> tag.Note:
    path = tmp_path / "note.md"
    path.write_text(text, encoding="utf-8")
    return tag.read_note(path)


def test_the_note_reads_through_its_markdown_decoration(tmp_path: Path) -> None:
    """The values are bold and backticked in the document. What goes in a file is the value."""
    note = _note(NOTE_TEXT, tmp_path)
    assert note.month == "2026-07"
    assert note.model_version == "v5.5"  # not "**v5.5**", and not the sentence after it
    assert note.licence_period == "suno-pro-2026-07"


def test_a_renamed_row_fails_by_name_rather_than_writing_nothing(tmp_path: Path) -> None:
    """§25: never silently produce nothing. A rewritten note must stop the pass, not empty it."""
    with pytest.raises(tag.TagError, match=re.escape(tag.ROW_MODEL)):
        _note(NOTE_TEXT.replace(tag.ROW_MODEL, "Model"), tmp_path)


def test_a_row_holding_prose_instead_of_a_value_is_refused(tmp_path: Path) -> None:
    """`not recorded` is what this row said before I-01. It is not a model version."""
    with pytest.raises(tag.TagError, match="model version"):
        _note(NOTE_TEXT.replace("**v5.5** — operator, 2026-08-23.", "*not recorded* —"), tmp_path)


def test_a_period_that_does_not_cover_the_stated_month_is_refused(tmp_path: Path) -> None:
    """Two rows of one note disagreeing is the case where every asset carries the wrong one."""
    with pytest.raises(tag.TagError, match="licence period"):
        _note(NOTE_TEXT.replace("suno-pro-2026-07", "suno-pro-2026-08"), tmp_path)


def test_the_real_note_still_states_all_three(tmp_path: Path) -> None:
    """The note is prose and gets edited. A rewrite should turn this red rather than `make imaging-tag`."""
    note = tag.read_note(NOTE)
    assert note.licence_period == "suno-pro-2026-07"
    assert note.model_version == "v5.5", "I-01's answer, and the only place it is written down"
    assert note.licence_period.endswith(note.month)


@pytest.mark.parametrize(
    "comment",
    [
        "made with suno; created=2026-07-08T10:03:15Z; id=afb174c4",
        "made with suno; created=2026-07-04T08:43:28.694Z; id=b145fd2a",
        "made with suno; created=2026-07-04T18:55:23.185912Z; id=d656f8dd",
    ],
)
def test_suno_writes_its_timestamp_at_three_precisions_and_only_the_day_is_wanted(
    comment: str,
) -> None:
    """All three appear across the 56. A parse that handled one of them would tag a third of them."""
    found = tag.CREATED.search(comment)
    assert found is not None and len(found.group(1)) == len("2026-07-08")


@pytest.mark.skipif(not _pile(), reason="the imaging audio is not in git (§4) — a Studio test")
def test_a_file_generated_outside_the_notes_month_is_refused() -> None:
    """The one mistake this command could make that nobody would notice: last month's terms.

    Run against a real July file with an August note, because the check is worth nothing unless it
    sits between the file's own timestamp and the note — which is where the real one sits.
    """
    august = tag.Note(month="2026-08", licence_period="suno-pro-2026-08", model_version="v5.5")
    with pytest.raises(tag.TagError, match="covers 2026-08"):
        tag.provenance(_pile()[0], august)


@pytest.mark.skipif(not _pile(), reason="the imaging audio is not in git (§4) — a Studio test")
def test_every_approved_file_can_say_when_it_was_made() -> None:
    """The pile's own claim: every file carrying the Suno timestamp its generation date comes from.

    This reads the real audio, which `make check` can afford because it is a tag read rather than a
    decode. A file that has been re-encoded or stripped loses the only record of when it was made,
    and this is where that gets noticed rather than at the point of writing a guess.
    """
    note = tag.read_note(NOTE)
    values = [tag.provenance(path, note) for path in _pile()]
    assert all(len(value.tags()) == len(TAG_KEYS) for value in values)
    assert all(value.ai_generated for value in values), "§18: the marker is not optional"
    assert {value.generated_on for value in values} == {"2026-07-04", "2026-07-08", "2026-07-20"}
