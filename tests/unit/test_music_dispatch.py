"""The proof that a take is the song it claims to be (D-091), and the two ways it goes wrong.

M-18 filed the pilot's 45 takes by sorting the export by timestamp and walking the track list. M-30
checked that against the lyric Suno writes into every file's own tags and found a song that had
never been generated — the file in track 9's slot was a second take of track 8, right size, right
place, plausible timestamp. **Both halves of that failure are asserted here**: the duplicate claim
and the song nobody claims. A test that only checked the happy path would not have caught it either.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from station.music import dispatch

LYRIC_ONE = """\
[Intro - 12 seconds, two guitars, no vocal]

[Verse 1]
Four bays down the transfer hall and four different rates,
same crew, same backs, same cargo off the same hauler.

[Chorus]
Bay rate, bay rate,
the number moves and the weight never does.
"""

LYRIC_TWO = """\
[Intro - 4 seconds, bass alone, no vocal]

[Verse 1]
Two crews in a transfer hall and one road between them
and both of them have been running it eleven years.

[Chorus]
Whose route is this, whose route is this,
ask the office and the office will send you to the other office.
"""


def _song(song_id: str, lyric: str, track: int = 1, filed: bool = False) -> dispatch.Written:
    return dispatch.Written(
        song_id=song_id,
        album_id="al_900",
        label="label_9",
        title=song_id,
        track_number=track,
        words=dispatch.sung_words(lyric),
        filed=filed,
    )


def _take(name: str, lyric: str, seconds: float = 240.0) -> dispatch.Take:
    return dispatch.Take(
        path=Path(name),
        words=dispatch.sung_words(lyric),
        suno_id="0" * 8 + "-0000-0000-0000-" + "0" * 12,
        created="2026-08-23T20:07:05Z",
        seconds=seconds,
    )


# --- what the words are -----------------------------------------------------------------------


def test_a_staging_tag_is_not_a_lyric() -> None:
    """The same reading §12 rules 9 and 10 use, so both count the same words."""
    assert "intro" not in dispatch.sung_words(LYRIC_ONE)
    assert dispatch.sung_words(LYRIC_ONE)[:4] == ["four", "bays", "down", "the"]


def test_a_curly_apostrophe_is_the_same_word_as_a_straight_one() -> None:
    """Suno returns curly quotes and the lyrics files hold straight ones. One word, either way."""
    curly = "don" + "\u2019" + "t wait up"
    assert dispatch.sung_words(curly) == dispatch.sung_words("don't wait up")


# --- the happy path, which is not the point ---------------------------------------------------


def test_a_take_claims_the_lyric_it_was_generated_from() -> None:
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("a.mp3", LYRIC_ONE)], songs)
    assert plan.assignments[0].song.song_id == "s_0001"
    assert plan.assignments[0].score == pytest.approx(1.0)


def test_a_reworded_take_still_claims_its_own_lyric_and_not_the_other() -> None:
    """Suno paraphrases. A take can be a poor copy of its lyric and still unmistakably be it."""
    reworded = LYRIC_ONE.replace("cargo", "pallet").replace("favour", "prank")
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    found = dispatch.plan([_take("a.mp3", reworded)], songs).assignments[0]
    assert found.song.song_id == "s_0001"
    assert found.gap > dispatch.MIN_GAP


# --- D-091's two failure shapes ---------------------------------------------------------------


def test_two_takes_of_one_song_leave_the_other_unclaimed_and_stop_the_pile() -> None:
    """The exact defect M-30 found: the style box moved on and the lyric box did not."""
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("01.mp3", LYRIC_ONE), _take("02.mp3", LYRIC_ONE)], songs)
    assert not plan.ok, "a pile that generated one song twice must not be filed"
    assert plan.unclaimed_songs == ["s_0002"]
    assert any("claimed by more than one take" in p for p in plan.problems)


def test_a_download_that_stopped_early_stops_the_pile() -> None:
    """The words prove nothing here: a truncated file carries the whole lyric and the whole id.

    M-31 filed an eight-second file into a cornerstone album at 88% match, because the tags were
    complete and only the audio was not. §7 puts nothing under 2:00 on air.
    """
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("a.mp3", LYRIC_ONE, seconds=8.2)], songs)
    assert not plan.ok, "an eight-second take must never reach an album folder"
    assert any("stopped early" in p for p in plan.problems)
    assert any("fetch it again" in p for p in plan.problems)


def test_one_song_is_topped_up_against_the_whole_written_pool() -> None:
    """A pile of one is the case that broke this: filing s_0340 alone had one candidate.

    Matching only against what is waiting makes "which song is this" a question with no wrong
    answer. The filed songs stay in the pool so the take has something to be wrong about.
    """
    songs = [_song("s_0001", LYRIC_ONE, 1, filed=True), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("b.mp3", LYRIC_TWO)], songs)
    assert plan.ok, plan.problems
    assert plan.assignments[0].song.song_id == "s_0002"
    assert plan.unclaimed_songs == [], "a filed song is not waiting and is not missing"


def test_a_second_copy_of_an_already_filed_song_stops_the_pile() -> None:
    """The take that is wrong about which gap it fills, which only a full pool can notice."""
    songs = [_song("s_0001", LYRIC_ONE, 1, filed=True), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("a.mp3", LYRIC_ONE)], songs)
    assert not plan.ok
    assert any("already has a take recorded" in p for p in plan.problems)
    assert plan.unclaimed_songs == ["s_0002"]


def test_a_take_of_something_never_written_here_stops_the_pile() -> None:
    """A file that belongs to another card, or to no card, is not filed on its closest guess."""
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    stranger = "[Verse 1]\nnothing in this lyric was ever written for this station at all\n"
    plan = dispatch.plan([_take("x.mp3", stranger)], songs)
    assert not plan.ok
    assert any("under the" in p and "floor" in p for p in plan.problems)


def test_two_songs_too_alike_to_tell_apart_stop_the_pile() -> None:
    """Without a margin over the runner-up, a bijection is arithmetic rather than evidence."""
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_ONE, 2)]
    plan = dispatch.plan([_take("a.mp3", LYRIC_ONE)], songs)
    assert not plan.ok
    assert any("behind it" in p for p in plan.problems)


def test_one_written_lyric_is_not_enough_to_prove_anything_against() -> None:
    with pytest.raises(dispatch.DispatchError, match="fewer than two"):
        dispatch.plan([_take("a.mp3", LYRIC_ONE)], [_song("s_0001", LYRIC_ONE)])


# --- nothing moves until the whole pile is proved ---------------------------------------------


def test_a_refused_plan_cannot_be_committed() -> None:
    songs = [_song("s_0001", LYRIC_ONE, 1), _song("s_0002", LYRIC_TWO, 2)]
    plan = dispatch.plan([_take("01.mp3", LYRIC_ONE), _take("02.mp3", LYRIC_ONE)], songs)
    with pytest.raises(dispatch.DispatchError, match="nothing was moved"):
        dispatch.commit(Path("."), plan)


def test_a_filed_take_is_never_overwritten(tmp_path: Path) -> None:
    """The only ways to reach an occupied destination are a double-file and a re-run over a card."""
    music = tmp_path / "music"
    song = _song("s_0001", LYRIC_ONE, 1)
    target = song.destination(music)
    target.parent.mkdir(parents=True)
    target.write_bytes(b"already filed")
    found = dispatch.Assignment(_take("a.mp3", LYRIC_ONE), song, 1.0, 0.9, "s_0002")
    with pytest.raises(dispatch.DispatchError, match="refusing to overwrite"):
        dispatch.file_takes(music, [found])
    assert target.read_bytes() == b"already filed"
