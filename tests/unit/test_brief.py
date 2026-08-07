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


def test_check_brief_refuses_when_the_genre_has_not_been_written() -> None:
    with pytest.raises(brief.BriefError, match=re.escape("wiki/relay-pop.yaml")):
        brief.build("check", "relay-pop", ROOT)
