"""`music/plan.yaml` has to add up, and the brief has to carry the rules that matter.

The arithmetic tests are the point of this file. The plan is hand-edited and its totals are the
only thing standing between a genre-by-genre commission and a catalogue that cannot make a label
retrospective — a failure that is free to fix now and very expensive after 500 songs exist
(`music/COMMISSION.md` §5).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from station.music import brief

ROOT = Path(__file__).resolve().parents[2]

TOTAL_SONGS = 500
TOTAL_BANDS = 25
MIN_BANDS_PER_LABEL = 3
MIN_SONGS_PER_LABEL = 40
# COMMISSION.md §4: the three big forms may not be the property of one label.
SPREAD = {"relay-pop": 4, "lane-rock": 3, "frontier-reels": 3}


@pytest.fixture(scope="module")
def plan() -> brief.Plan:
    return brief.load_plan(ROOT / "music" / "plan.yaml")


def test_playable_total_is_five_hundred(plan: brief.Plan) -> None:
    assert plan.total_songs == TOTAL_SONGS


def test_band_total(plan: brief.Plan) -> None:
    assert plan.total_bands == TOTAL_BANDS


def test_every_label_can_carry_a_retrospective(plan: brief.Plan) -> None:
    """§5: >=3 bands and >=40 playable songs, or the label retrospective cannot be made."""
    bands, songs = plan.bands_per_label(), plan.songs_per_label()
    thin = {
        plan.labels[n]: (bands[n], songs[n])
        for n in plan.labels
        if bands[n] < MIN_BANDS_PER_LABEL or songs[n] < MIN_SONGS_PER_LABEL
    }
    assert not thin, f"labels too thin for a retrospective: {thin}"


@pytest.mark.parametrize(("genre", "least"), SPREAD.items())
def test_big_forms_are_spread_across_labels(plan: brief.Plan, genre: str, least: int) -> None:
    assert len(plan.genres[genre].labels) >= least


def test_genre_slugs_match_the_eight_canon_forms(plan: brief.Plan) -> None:
    assert len(plan.genres) == 8


def test_write_brief_carries_commission_constants_and_the_numbers(plan: brief.Plan) -> None:
    text = brief.build("write", "relay-pop", ROOT)
    genre = plan.genres["relay-pop"]
    # the whole brief is embedded, not referenced: a phrase from deep inside each source file
    assert "swap-the-nouns test" in text  # COMMISSION.md §3 came through
    assert "the eight canon forms" in text  # §8 came through
    assert "anchor years" in text.lower()  # CONSTANTS came through
    assert f"LAYER A — {genre.songs} songs" in text
    assert "Label 1 (Concordance, prestige): 45 songs" in text
    assert "playable: false" in text


def test_unknown_genre_names_the_valid_ones() -> None:
    with pytest.raises(brief.BriefError, match="relay-pop"):
        brief.build("write", "jazz", ROOT)


def test_check_brief_refuses_when_the_genre_has_not_been_written(tmp_path: Path) -> None:
    """Against an empty root, so the result does not depend on which genres happen to be written."""
    music = tmp_path / "music"
    (music / "wiki").mkdir(parents=True)
    for name in ("COMMISSION.md", "CONSTANTS.md", "plan.yaml"):
        (music / name).write_text((ROOT / "music" / name).read_text(encoding="utf-8"))
    with pytest.raises(brief.BriefError, match=re.escape("wiki/relay-pop.yaml")):
        brief.build("check", "relay-pop", tmp_path)


def test_songs_brief_carries_the_album_story_titles_and_facts() -> None:
    """The lyric writer needs the record's story and each song's existing fact, or it invents both."""
    if not (ROOT / "music" / "wiki" / "relay-pop.yaml").is_file():
        pytest.skip("relay-pop has not been written yet")
    text = brief.build_songs("al_001", ROOT)
    assert "Terms of Arrival" in text  # the album
    assert "Measure Kindly" in text  # the band
    assert "2619" in text  # the year
    assert "fact:" in text  # every song's fact came through
    assert "swap-the-nouns test" in text  # the subject rules came through


def test_songs_brief_names_the_valid_albums_when_the_id_is_wrong() -> None:
    with pytest.raises(brief.BriefError, match="no album"):
        brief.build_songs("al_999", ROOT)
