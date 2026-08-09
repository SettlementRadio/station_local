"""`music/plan.yaml` has to add up, the wiki has to match it, and the brief has to carry the rules.

The arithmetic tests are the point of this file. The plan is hand-edited and its totals are the
only thing standing between a genre-by-genre commission and a catalogue that cannot make a label
retrospective — a failure that is free to fix now and very expensive after 500 songs exist
(`music/COMMISSION.md` §5). The second half does the same for what has actually been written: the
wiki is nine files produced weeks apart, and nobody is going to count 105 songs by hand twice.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from station.music import brief, check, wiki

ROOT = Path(__file__).resolve().parents[2]

TOTAL_SONGS = 500
TOTAL_BANDS = 25
MIN_BANDS_PER_LABEL = 3
MIN_SONGS_PER_LABEL = 40
# COMMISSION.md §4: the big forms may not be the property of one label.
SPREAD = {"relay-pop": 4, "lane-rock": 3, "deck-talk": 3, "frontier-reels": 3}


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


def test_genre_slugs_match_the_nine_canon_forms(plan: brief.Plan) -> None:
    """§2 is a closed list. A tenth genre is a canon edit, never a plan edit."""
    assert len(plan.genres) == 9


def test_write_brief_carries_commission_constants_and_the_numbers(plan: brief.Plan) -> None:
    text = brief.build("write", "relay-pop", ROOT)
    genre = plan.genres["relay-pop"]
    # the whole brief is embedded, not referenced: a phrase from deep inside each source file
    assert "swap-the-nouns test" in text  # COMMISSION.md §3 came through
    assert "the nine canon forms" in text  # §8 came through
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


def test_album_listing_reports_which_bands_still_need_a_style_card() -> None:
    """`music-albums` is how the operator finds an id for `music-songs`; the style column is why."""
    if not (ROOT / "music" / "wiki" / "relay-pop.yaml").is_file():
        pytest.skip("relay-pop has not been written yet")
    rows = wiki.album_rows(ROOT / "music" / "wiki", styles={})
    assert rows, "relay-pop has albums, so the listing must not be empty"
    assert all(not r.has_style for r in rows), "no style card was passed, so none may report one"
    one = next(r for r in rows if r.album_id == "al_001")
    assert one.band == "Measure Kindly" and one.cornerstone and one.playable == 12

    with_style = wiki.album_rows(ROOT / "music" / "wiki", styles={one.band_id: "voice: ..."})
    assert next(r for r in with_style if r.album_id == "al_001").has_style


def test_listing_shows_layer_b_albums_and_marks_them_unplayable() -> None:
    """Layer B is most of the discography; a listing that hides it hides what the presenters use."""
    if not (ROOT / "music" / "wiki" / "relay-pop.yaml").is_file():
        pytest.skip("relay-pop has not been written yet")
    rows = wiki.album_rows(ROOT / "music" / "wiki", styles={})
    layer_b = [r for r in rows if r.layer == "B"]
    assert layer_b, "relay-pop has layer-B albums, so they must appear"
    assert all(r.playable == 0 for r in layer_b), "a layer-B album has no playable songs"
    assert all(r.songs > 0 for r in layer_b), "but it does have songs, which is the point of it"
    assert all(r.band != "?" for r in layer_b), "layer-B albums nest inside their band"


def test_songs_brief_refuses_a_layer_b_album_and_says_why() -> None:
    """The failure a listing invites: picking an id that can never become audio."""
    if not (ROOT / "music" / "wiki" / "relay-pop.yaml").is_file():
        pytest.skip("relay-pop has not been written yet")
    with pytest.raises(brief.BriefError, match="layer-B"):
        brief.build_songs("al_012", ROOT)


# --- the wiki against the plan (M-01) ---------------------------------------------------------
#
# One fixture genre, correct, and one test per way of breaking it. core-harmonies is the smallest
# allocation in the plan — 15 songs on one label — so the fixture is the real shape at a size that
# fits in a test file.


def _songs(count: int, first: int, *, playable: bool, fact: bool) -> list[dict[str, Any]]:
    return [
        {
            "id": f"s_{first + n:04d}",
            "title": f"Song {first + n}",
            "track_number": n + 1,
            "playable": playable,
            **({"fact": "Recorded in one take with the hall doors open."} if fact else {}),
        }
        for n in range(count)
    ]


def _album(album_id: str, year: int, songs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "id": album_id,
        "title": f"Album {album_id}",
        "band": "b_001",
        "label": "label_1",
        "genre": "core-harmonies",
        "release_year": year,
        "songs": songs,
    }


def _fixture_genre() -> dict[str, Any]:
    """A core-harmonies that passes every check: 15 playable songs on label 1, and one layer-B record."""
    return {
        "labels": [{"id": "label_1", "name": "Civic Lantern"}],
        "session_players": [{"id": "sp_ivena_sorn", "name": "Ivena Sorn"}],
        "layer_a": {
            "bands": [
                {
                    "id": "b_001",
                    "name": "Held Note",
                    "kind": "group",
                    "genre": "core-harmonies",
                    "label": "label_1",
                    "active_from": 2600,
                    "members": [{"id": "p_tenn_ruso", "name": "Tenn Ruso"}],
                }
            ],
            "albums": [_album("al_001", 2559, _songs(15, 1, playable=True, fact=True))],
        },
        "layer_b": {
            "bands": [
                {
                    "id": "b_002",
                    "name": "The Slow Room",
                    "kind": "group",
                    "genre": "core-harmonies",
                    "label": "label_1",
                    "active_from": 2570,
                    "albums": [_album("al_002", 2583, _songs(4, 16, playable=False, fact=False))],
                }
            ]
        },
        "layer_c": {"figures": [{"id": "f_001", "name": "Edda Corven"}]},
    }


def _root_with(tmp_path: Path, **genres: dict[str, Any]) -> Path:
    """A repository root holding only `music/` — the real plan and constants, a fixture wiki."""
    music = tmp_path / "music"
    (music / "wiki").mkdir(parents=True)
    for name in ("CONSTANTS.md", "plan.yaml"):
        (music / name).write_text((ROOT / "music" / name).read_text(encoding="utf-8"))
    for slug, data in genres.items():
        (music / "wiki" / f"{slug.replace('_', '-')}.yaml").write_text(yaml.safe_dump(data))
    return tmp_path


def _details(tmp_path: Path, **genres: dict[str, Any]) -> str:
    return "\n".join(p.line() for p in check.check_wiki(_root_with(tmp_path, **genres)))


def test_the_written_wiki_matches_the_plan() -> None:
    """The one that runs on the real thing: `make check` is red whenever this is not empty."""
    if not wiki.written_genres(ROOT / "music" / "wiki"):
        pytest.skip("no genre has been written yet")
    problems = check.check_wiki(ROOT)
    assert not problems, "the wiki does not match the plan:\n" + "\n".join(
        p.line() for p in problems
    )


def test_a_correct_genre_reports_nothing(tmp_path: Path) -> None:
    assert _details(tmp_path, core_harmonies=_fixture_genre()) == ""


def test_a_wrong_song_count_names_the_genre_the_label_and_both_numbers(tmp_path: Path) -> None:
    """The count the operator would otherwise do by hand, once per genre, twice to be sure."""
    genre = _fixture_genre()
    genre["layer_a"]["albums"][0]["songs"].pop()
    detail = _details(tmp_path, core_harmonies=genre)
    assert "core-harmonies" in detail
    assert "label 1" in detail and "14" in detail and "15" in detail


def test_a_layer_a_song_without_a_fact_is_named(tmp_path: Path) -> None:
    genre = _fixture_genre()
    del genre["layer_a"]["albums"][0]["songs"][2]["fact"]
    detail = _details(tmp_path, core_harmonies=genre)
    assert "s_0003" in detail and "no fact" in detail


def test_a_layer_b_song_with_a_fact_is_named(tmp_path: Path) -> None:
    """Layer B is titles only: a fact there is effort spent on a record nobody can play."""
    genre = _fixture_genre()
    genre["layer_b"]["bands"][0]["albums"][0]["songs"][0]["fact"] = "Cut in a stairwell."
    detail = _details(tmp_path, core_harmonies=genre)
    assert "s_0016" in detail and "layer B" in detail


def test_a_release_year_off_the_anchors_is_named(tmp_path: Path) -> None:
    genre = _fixture_genre()
    genre["layer_a"]["albums"][0]["release_year"] = 2560
    detail = _details(tmp_path, core_harmonies=genre)
    assert "al_001" in detail and "2560" in detail and "anchor years" in detail


def test_an_id_used_by_two_genres_is_a_failure(tmp_path: Path) -> None:
    """The whole point of the card: genre two silently overwriting genre one."""
    second = {"layer_b": {"bands": [dict(_fixture_genre()["layer_b"]["bands"][0])]}}
    detail = _details(tmp_path, core_harmonies=_fixture_genre(), void_ballads=second)
    assert "id b_002 is used 2 times" in detail
    assert "id s_0016 is used 2 times" in detail
    assert "core-harmonies" in detail and "void-ballads" in detail


def test_a_session_player_may_appear_in_every_genre_that_hired_them(tmp_path: Path) -> None:
    """§6 requires them across three labels, so a shared id is the design, not a collision."""
    shared = _fixture_genre()["session_players"]
    second = {"session_players": shared, "labels": _fixture_genre()["labels"]}
    assert _details(tmp_path, core_harmonies=_fixture_genre(), void_ballads=second) == ""


def test_the_same_id_under_two_different_names_is_still_a_failure(tmp_path: Path) -> None:
    second = {"session_players": [{"id": "sp_ivena_sorn", "name": "Someone Else"}]}
    detail = _details(tmp_path, core_harmonies=_fixture_genre(), void_ballads=second)
    assert "sp_ivena_sorn" in detail and "Someone Else" in detail


def test_the_next_free_id_is_derived_from_what_is_written(tmp_path: Path) -> None:
    """CONSTANTS.md no longer carries these by hand; the wiki is the counter."""
    empty = tmp_path / "empty"
    assert wiki.next_free_ids(empty) == {"song": "s_0001", "album": "al_001", "band": "b_001"}
    root = _root_with(tmp_path, core_harmonies=_fixture_genre())
    assert wiki.next_free_ids(root / "music" / "wiki") == {
        "song": "s_0020",  # 15 layer-A songs, then four layer-B titles
        "album": "al_003",
        "band": "b_003",
    }


def test_the_anchor_years_come_out_of_constants() -> None:
    """If the table's shape changes, this fails rather than the years quietly becoming none."""
    years = check.anchor_years(ROOT / "music" / "CONSTANTS.md")
    assert len(years) == check.ANCHOR_COUNT
    assert 2559 in years and 2624 in years


def test_a_missing_anchor_table_stops_the_check_rather_than_passing_it(tmp_path: Path) -> None:
    root = _root_with(tmp_path, core_harmonies=_fixture_genre())
    (root / "music" / "CONSTANTS.md").write_text("# no table here\n")
    with pytest.raises(check.CheckError, match="anchor years"):
        check.check_wiki(root)
