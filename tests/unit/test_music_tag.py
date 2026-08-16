"""`make music-tag` — the resolution rule, which is where a wrong licence would come from.

No test writes a tag. ffmpeg and ffprobe are two calls §29 does not want a test of, and the write
already refuses to replace a file whose audio checksum or tags did not survive the copy — a check
that runs on every one of the 500 files rather than once in CI.

What is worth testing is D-062's resolution: a song's `take:` block first, the album's
`generation:` block for anything null there. That rule is the only reason 45 files can be tagged
from four metadata blocks, and getting it wrong writes a plausible-looking wrong licence period
into a file that will one day be all the evidence there is (COMMISSION.md §9).

The last two tests read the real lyrics files, because the shape M-17 fixed is what this reads and
a change to it should turn something red here rather than at 02:00.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from station.music import tag

ROOT = Path(__file__).resolve().parents[2]
MUSIC = ROOT / "music"

ALBUM = {
    "model_version": "v5.5",
    "licence_period": "suno-pro-2026-08",
    "generated_on": "2026-08-15",
    "ai_generated": True,
}


def _album_file(
    generation: dict[str, object] | None, take: dict[str, object] | None
) -> dict[str, object]:
    """One lyrics file cut down to the fields tagging reads."""
    song: dict[str, object] = {"id": "s_0001", "title": "Meet Me at Noon", "track_number": 1}
    if take is not None:
        song["take"] = take
    return {"album": {"id": "al_001"}, "generation": generation, "songs": [song]}


def _one(generation: dict[str, object] | None, take: dict[str, object] | None) -> tag.Song:
    parsed = tag._AlbumFile.model_validate(_album_file(generation, take))
    return tag._album_songs(MUSIC, Path("al_001.yaml"), parsed)[0]


def test_the_album_block_fills_in_what_the_take_leaves_null() -> None:
    """The shape the pilot is actually written in: one sitting, one band, four values recorded once."""
    song = _one(ALBUM, {"attempts": 1, "model_version": None, "file": "music/audio/x/01.mp3"})
    assert song.provenance.tags() == {
        "AI_GENERATED": "true",
        "AI_MODEL_VERSION": "v5.5",
        "LICENCE_PERIOD": "suno-pro-2026-08",
        "GENERATION_DATE": "2026-08-15",
    }


def test_the_song_wins_where_it_says_something() -> None:
    """A song re-generated later carries its own model and date — that is why D-062 reads it first."""
    song = _one(
        ALBUM,
        {"model_version": "v6.0", "generated_on": "2026-09-02", "file": "music/audio/x/01.mp3"},
    )
    assert song.provenance.model_version == "v6.0"
    assert song.provenance.generated_on == "2026-09-02"
    assert song.provenance.licence_period == "suno-pro-2026-08"  # still the album's


def test_an_unquoted_yaml_date_and_a_quoted_one_are_the_same_tag() -> None:
    """YAML reads `2026-08-15` as a date object and `'2026-08-15'` as text. One day, one tag."""
    loaded = yaml.safe_load("generated_on: 2026-08-15")
    assert tag._Block.model_validate(loaded).generated_on == "2026-08-15"


def test_a_song_that_cannot_say_what_it_was_made_under_fails_loudly() -> None:
    """§25: never silently produce nothing. An untagged file is a file nobody may broadcast."""
    with pytest.raises(tag.TagError, match="licence_period"):
        _one({"model_version": "v5.5"}, {"generated_on": "2026-08-15", "file": "a/01.mp3"})


def test_a_take_declared_not_machine_generated_is_refused() -> None:
    """Writing `AI_GENERATED=false` into a Suno take would be a compliance lie, not a tag."""
    with pytest.raises(tag.TagError, match="ai_generated"):
        _one({**ALBUM, "ai_generated": False}, {"file": "a/01.mp3"})


def test_a_song_with_no_take_yet_is_not_a_song_to_tag() -> None:
    """Lyrics are written before the Suno sitting; a song with no take has no file to write into."""
    parsed = tag._AlbumFile.model_validate(_album_file(ALBUM, None))
    assert tag._album_songs(MUSIC, Path("al_001.yaml"), parsed) == []


def test_the_pilot_resolves_to_four_values_a_song() -> None:
    """The real files, in the shape al_001.yaml fixes — 45 takes, every one able to name its licence."""
    songs = tag.load_songs(MUSIC)
    assert len(songs) == 45
    assert all(len(song.provenance.tags()) == len(tag.TAG_KEYS) for song in songs)
    assert {song.provenance.licence_period for song in songs} == {"suno-pro-2026-08"}


def test_every_take_points_at_a_file_under_the_audio_root() -> None:
    """A path resolved from the wrong root would report forty-five files waiting for audio."""
    audio = (MUSIC / tag.AUDIO_DIR).resolve()
    assert all(audio in song.path.resolve().parents for song in tag.load_songs(MUSIC))
