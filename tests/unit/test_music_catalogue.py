"""`music/catalogue.yaml` is committed, so the failure worth catching is it going stale.

The file is derived from the wiki and regenerated whole, which means a fresh build can never
disagree with the wiki that produced it. What can — and what nothing else would notice — is a genre
file edited without `make music-catalogue` being re-run, leaving the station's one source of truth
describing last week's wiki. That is what the first test is, and it is the reason `validate()`
exists at all.

Everything else here is the arithmetic that decides what goes in a row: what makes a record
catalogue rather than current, what a label reference means when it is not a label, and the YAML
quoting bug that truncated twenty-five titles without ever failing anything.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest
import yaml

from station.music import catalogue, catalogue_check, wiki

ROOT = Path(__file__).resolve().parents[2]

PRESENT = 2626  # music/CONSTANTS.md §1, and stated in every genre file's `section:` block


def test_the_catalogue_agrees_with_the_wiki() -> None:
    """The gate. Red means the wiki moved and `make music-catalogue` was not re-run."""
    problems = catalogue_check.validate(ROOT)
    assert not problems, "music/catalogue.yaml is out of date:\n  " + "\n  ".join(problems)


def test_a_wiki_edit_without_a_rebuild_is_caught(tmp_path: Path) -> None:
    """The one failure a fresh build cannot produce, so it is the one worth a test."""
    music = tmp_path / "music"
    music.mkdir()
    (music / wiki.WIKI_DIR).symlink_to(ROOT / "music" / wiki.WIKI_DIR)
    stale = catalogue.load(ROOT / "music" / catalogue.CATALOGUE_FILE)
    dropped = stale.tracks.pop()
    stale.albums[0].title = "A Title The Wiki Does Not Have"
    catalogue.write(music / catalogue.CATALOGUE_FILE, stale)

    problems = catalogue_check.validate(tmp_path)
    assert any(dropped.id in problem for problem in problems), problems
    assert any("named differently" in problem for problem in problems), problems


def test_a_missing_catalogue_says_which_command_writes_it(tmp_path: Path) -> None:
    """§25: never silently produce nothing. An absent file is a message, not an empty problem list."""
    music = tmp_path / "music"
    music.mkdir()
    (music / wiki.WIKI_DIR).symlink_to(ROOT / "music" / wiki.WIKI_DIR)
    assert catalogue_check.validate(tmp_path) == [
        f"{music / catalogue.CATALOGUE_FILE} does not exist — run `make music-catalogue`"
    ]


@pytest.mark.parametrize(
    ("release_year", "expected"),
    [(PRESENT, catalogue.HEAVY), (PRESENT - 4, catalogue.HEAVY), (PRESENT - 5, catalogue.GOLD)],
)
def test_gold_starts_five_in_world_years_back(release_year: int, expected: str) -> None:
    """§8's own definition, and the reason the present year is written into the file."""
    assert catalogue._category(release_year, PRESENT) == expected


def test_the_present_year_has_to_be_one_year() -> None:
    """Two presents would make one record catalogue in one genre and current in another."""
    one, other = wiki.GenreWiki(), wiki.GenreWiki()
    one.section.present_year, other.section.present_year = PRESENT, PRESENT + 1
    with pytest.raises(catalogue.CatalogueError, match="one year"):
        catalogue.present_year({"a": one, "b": other})


def test_no_house_is_not_the_same_as_a_broken_reference() -> None:
    """`unsigned` is a fact about a band (D-059); `label_9` is a typo, and both become a null id."""
    counted: Counter[str] = Counter()
    assert catalogue._label_id("label_2", counted) == "label_2"
    assert catalogue._label_id("2", counted) == "label_2"
    assert catalogue._label_id("unsigned", counted) is None
    assert counted == Counter({"unsigned": 1})
    assert catalogue._label_id("label_9", counted) == "label_9"  # resolves to nothing, and is named


def test_an_unquoted_comma_truncates_a_title_and_is_reported() -> None:
    """`{title: Two Callers, One Sheet}` is valid YAML, a truncated title, and was in the wiki."""
    truncated = wiki.Song.model_validate(
        yaml.safe_load("{id: s_0528, title: Two Callers, One Sheet, track_number: 6}")
    )
    assert truncated.title == "Two Callers" and truncated.stray_keys == ["One Sheet"]
    whole = wiki.Song.model_validate({"id": "s_0528", "title": "Two Callers, One Sheet",
                                      "track_number": 6, "genre": "deck-talk", "credits": {}})  # fmt: skip
    assert whole.stray_keys == []


# --- a collection in the catalogue (M-52) ------------------------------------------------------


def _collection(wiki_dir: Path) -> dict[str, wiki.GenreWiki]:
    """One `independents.yaml`: a record the station holds, and a title it only knows about."""
    wiki_dir.mkdir(parents=True)
    (wiki_dir / "independents.yaml").write_text(
        yaml.safe_dump(
            {
                "section": {"present_year": PRESENT},
                "layer_a": {
                    "bands": [
                        {
                            "id": "b_101",
                            "name": "The Lane Runners",
                            "kind": "group",
                            "genre": "independents",
                            "label": "unsigned",
                            "active_from": 2610,
                            "albums": [
                                {
                                    "id": "al_101",
                                    "title": "Green Lights",
                                    "label": "unsigned",
                                    "genre": "independents",
                                    "release_year": 2615,
                                    "songs": [
                                        {
                                            "id": "s_0101",
                                            "title": "Green Lights All the Way",
                                            "track_number": 1,
                                            "playable": True,
                                            "fact": "Haulers play it leaving port for luck.",
                                        },
                                        {
                                            "id": "s_0102",
                                            "title": "Harbour Light",
                                            "track_number": 2,
                                            "playable": True,
                                            "fact": "Cut the same afternoon as the first.",
                                        },
                                    ],
                                }
                            ],
                        }
                    ]
                },
                "layer_b": {
                    "bands": [
                        {
                            "id": "b_102",
                            "name": "Ysolde Mar",
                            "kind": "solo",
                            "genre": "independents",
                            "label": "unsigned",
                            "active_from": 2614,
                            "albums": [
                                {
                                    "id": "al_102",
                                    "title": "Cargo Hold",
                                    "label": "unsigned",
                                    "genre": "independents",
                                    "release_year": 2621,
                                    "songs": [
                                        {
                                            "id": "s_0121",
                                            "title": "Cargo Hold Lullaby",
                                            "track_number": 1,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                },
            }
        )
    )
    return catalogue.genres(wiki_dir)


def test_a_collection_becomes_rows_like_any_other_wiki_file(tmp_path: Path) -> None:
    """M-52 check 6. Rotation asks whether there is a file, never who commissioned it — so a
    collection is read here exactly as a genre is, and only the plan and the anchors ignore it."""
    found = _collection(tmp_path / "wiki")
    assert list(found) == ["independents"]

    take = catalogue.Take(
        file="music/audio/unsigned/al_101/01.mp3",
        licence_note="suno-pro-2026-07",
        duration_sec=159.4,
        intro_ramp_sec=2.0,
        outro_type="fade",
    )
    tracks, problems = catalogue._tracks(found, PRESENT, {"s_0101": take})
    assert problems == []
    rows = {track.id: track for track in tracks}
    assert set(rows) == {"s_0101", "s_0102", "s_0121"}

    played = rows["s_0101"]
    assert played.playable and played.file == take.file
    assert played.duration_sec == 159.4 and played.intro_ramp_sec == 2.0
    assert played.outro_type == "fade" and played.licence_note == "suno-pro-2026-07"
    assert played.category == catalogue.GOLD  # 2615, eleven in-world years back

    for silent in ("s_0102", "s_0121"):  # a take not made yet, and a title never pressed
        assert not rows[silent].playable
        assert rows[silent].file is None and rows[silent].category is None


def test_a_collection_title_with_audio_against_it_is_still_a_problem(tmp_path: Path) -> None:
    """Layer B is what the world knows and the station does not hold, collection or not."""
    found = _collection(tmp_path / "wiki")
    take = catalogue.Take(
        file="music/audio/unsigned/al_102/01.mp3",
        licence_note="suno-pro-2026-07",
        duration_sec=479.4,
        intro_ramp_sec=0.0,
        outro_type="cold",
    )
    _, problems = catalogue._tracks(found, PRESENT, {"s_0121": take})
    assert any("s_0121" in problem and "layer-B" in problem for problem in problems)
