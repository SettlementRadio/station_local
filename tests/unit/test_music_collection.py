"""A collection is a wiki file that is not a genre, and these are the eight ways that shows.

`music/wiki/` holds the nine commissioned forms. It also holds — from M-53 — a **collection**: a set
of records that reached the station from outside the seven houses, generated before the commission
existed and belonging to none of it. `wiki.COLLECTIONS` names those files, and the whole of what the
name buys is that **two** checks stop applying: the plan count and the anchor years.

Everything else keeps applying, and that is the half worth testing hardest, because each miss is
silent. A collection that stopped minting counted ids would hand the next genre a number already in
use. One that stopped being screened would be forty-two invented band names nobody was ever asked
about. So every test below is a pair: the thing a collection is excused, and the thing it is not.

`test_music.py` owns the genre side of `check.py`; this file owns the third state.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from station.music import check, wiki

ROOT = Path(__file__).resolve().parents[2]

COLLECTION = "independents"  # `wiki.COLLECTIONS`, and the file M-53 writes
OFF_THE_ANCHORS = 2615  # M-53 re-dates the pile into 2612-2621, mostly missing the eight


def _songs(count: int, first: int, *, playable: bool, fact: bool) -> list[dict[str, Any]]:
    return [
        {
            "id": f"s_{first + n:04d}",
            "title": f"Song {first + n}",
            "track_number": n + 1,
            "playable": playable,
            **({"fact": "Haulers play it leaving port for luck."} if fact else {}),
        }
        for n in range(count)
    ]


def _album(album_id: str, year: int, songs: list[dict[str, Any]]) -> dict[str, Any]:
    """An unsigned record: no house, and a year no house shipped into."""
    return {
        "id": album_id,
        "title": f"Album {album_id}",
        "label": "unsigned",
        "genre": COLLECTION,
        "release_year": year,
        "songs": songs,
    }


def _band(band_id: str, name: str, albums: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "id": band_id,
        "name": name,
        "kind": "group",
        "genre": COLLECTION,
        "label": "unsigned",
        "active_from": 2610,
        "albums": albums,
    }


def _fixture_collection() -> dict[str, Any]:
    """Three records the station holds and two titles it only knows about, on no label at all.

    Deliberately the shape that would fail both dropped rules: songs nothing allocated, in a year
    that is not an anchor. If either check ever reaches it, this fixture is what goes red.
    """
    return {
        "layer_a": {
            "bands": [
                _band(
                    "b_101",
                    "The Lane Runners",
                    [_album("al_101", OFF_THE_ANCHORS, _songs(3, 101, playable=True, fact=True))],
                )
            ]
        },
        "layer_b": {
            "bands": [
                _band(
                    "b_102",
                    "Ysolde Mar",
                    [_album("al_102", 2621, _songs(2, 121, playable=False, fact=False))],
                )
            ]
        },
    }


def _root_with(tmp_path: Path, **files: dict[str, Any]) -> Path:
    """A repository root holding only `music/` — the real plan, constants and cards; a fixture wiki."""
    music = tmp_path / "music"
    (music / wiki.WIKI_DIR).mkdir(parents=True)
    for name in ("CONSTANTS.md", "plan.yaml", check.TASKS_FILE):
        (music / name).write_text((ROOT / "music" / name).read_text(encoding="utf-8"))
    for slug, data in files.items():
        (music / wiki.WIKI_DIR / f"{slug.replace('_', '-')}.yaml").write_text(yaml.safe_dump(data))
    return tmp_path


def _details(tmp_path: Path, **files: dict[str, Any]) -> str:
    return "\n".join(p.line() for p in check.check_wiki(_root_with(tmp_path, **files)))


def test_a_collection_is_read_where_the_anchor_file_is_skipped(tmp_path: Path) -> None:
    """The third state itself, and why there are two sets rather than one.

    `written_slugs` is also the list `make music-screen` sweeps with no argument, so a collection
    missing from it is a file of invented names nobody is ever asked about.
    """
    root = _root_with(tmp_path, void_ballads={}, independents={})
    wiki_dir = root / "music" / wiki.WIKI_DIR
    (wiki_dir / "anchors.yaml").write_text("anchor_years: []\n")

    assert wiki.written_slugs(wiki_dir) == [COLLECTION, "void-ballads"]
    assert wiki.written_genres(wiki_dir) == ["void-ballads"]
    assert wiki.is_collection(COLLECTION) and not wiki.is_collection("void-ballads")


def test_a_collection_needs_no_allocation_and_sits_off_the_anchor_years(tmp_path: Path) -> None:
    """The two checks it is excused, and the contrast is what makes them a state rather than a hole.

    The same file under a genre's name has to be two failures: a form of the nine that pressed
    songs nobody planned for, on no label, in a year no house shipped into.
    """
    collection = _fixture_collection()
    assert _details(tmp_path / "as-a-collection", independents=collection) == ""

    detail = _details(tmp_path / "as-a-genre", void_ballads=collection)
    assert str(OFF_THE_ANCHORS) in detail and "anchor years" in detail
    assert "playable songs" in detail


def test_an_id_a_collection_takes_from_a_genre_is_still_a_failure(tmp_path: Path) -> None:
    """Ids are the one thing a collection is counted for, because they are the one thing shared."""
    collection = _fixture_collection()
    collection["layer_a"]["bands"][0]["albums"][0]["id"] = "al_001"
    genre = {"layer_b": {"bands": [_band("b_001", "Held Note", [_album("al_001", 2624, [])])]}}
    detail = _details(tmp_path, core_harmonies=genre, independents=collection)
    assert "id al_001 is used 2 times" in detail
    assert "core-harmonies" in detail and COLLECTION in detail


def test_the_next_free_id_counts_a_collection_too(tmp_path: Path) -> None:
    """The same rule from the other end: the next genre written cannot be handed a used number."""
    root = _root_with(tmp_path, independents=_fixture_collection())
    assert wiki.next_free_ids(root / "music" / wiki.WIKI_DIR) == {
        "song": "s_0123",  # the collection's layer-B titles are the high-water mark
        "album": "al_103",
        "band": "b_103",
    }


def test_a_collection_song_obeys_the_fact_rule(tmp_path: Path) -> None:
    """Layer A is what a presenter can say something about, wherever the record came from."""
    collection = _fixture_collection()
    del collection["layer_a"]["bands"][0]["albums"][0]["songs"][1]["fact"]
    collection["layer_b"]["bands"][0]["albums"][0]["songs"][0]["fact"] = "Cut in a stairwell."
    detail = _details(tmp_path, independents=collection)
    assert "s_0102" in detail and "no fact" in detail
    assert "s_0121" in detail and "layer B" in detail
