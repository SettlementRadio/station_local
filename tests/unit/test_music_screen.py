"""`make music-screen` — every invented name reaches Wikidata, and a screen that failed says so.

Split out of `test_music.py` when that file passed §31's 400 lines. The two suites test the same
`music/wiki/` shape and nothing else: this one needs a genre file with one of every kind of name in
it, and never the plan, so it builds its own small fixture rather than sharing one.

No test here touches the network. `screen()` takes its fetcher, and these pass a stub.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from station.music import screen, wiki

# One of every kind of name §19 asks for: a label, a session player, a layer-A band with a member,
# a layer-C figure, and album and song titles on both sides of the playable line.
GENRE: dict[str, Any] = {
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
        "albums": [
            {
                "id": "al_001",
                "title": "Album al_001",
                "band": "b_001",
                "label": "label_1",
                "genre": "core-harmonies",
                "release_year": 2624,
                "songs": [
                    {
                        "id": "s_0001",
                        "title": "Song 1",
                        "track_number": 1,
                        "playable": True,
                        "fact": "Recorded in one take with the hall doors open.",
                    }
                ],
            }
        ],
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
                "albums": [
                    {
                        "id": "al_002",
                        "title": "Album al_002",
                        "band": "b_002",
                        "label": "label_1",
                        "genre": "core-harmonies",
                        "release_year": 2583,
                        "songs": [
                            {
                                "id": "s_0021",
                                "title": "Song 21",
                                "track_number": 1,
                                "playable": False,
                            }
                        ],
                    }
                ],
            }
        ]
    },
    "layer_c": {"figures": [{"id": "f_001", "name": "Edda Corven"}]},
}


def _one_hit(name: str, qid: str = "Q313258", sitelinks: int = 42) -> dict[str, Any]:
    return {
        "results": {
            "bindings": [
                {
                    "name": {"value": name},
                    "item": {"value": f"http://www.wikidata.org/entity/{qid}"},
                    "sitelinks": {"value": str(sitelinks)},
                    "kinds": {"value": "human"},
                    "desc": {"value": "United States Secretary of State (1909-1994)"},
                }
            ]
        }
    }


def _screened(tmp_path: Path) -> list[screen.Name]:
    path = tmp_path / "core-harmonies.yaml"
    path.write_text(yaml.safe_dump(GENRE), encoding="utf-8")
    return screen.names_in(wiki.load_genre(path))


def test_every_kind_of_invented_name_is_screened(tmp_path: Path) -> None:
    """§19's list: bands, labels, people, album titles and song titles — layer B included."""
    names = _screened(tmp_path)
    by_name = {n.name: n.kind for n in names}
    assert by_name["Civic Lantern"] == "label"
    assert by_name["Held Note"] == "band" and by_name["The Slow Room"] == "band"
    assert by_name["Ivena Sorn"] == "person" and by_name["Tenn Ruso"] == "person"
    assert by_name["Edda Corven"] == "person", "layer C figures are invented names too"
    assert by_name["Album al_001"] == "album" and by_name["Album al_002"] == "album"
    assert by_name["Song 1"] == "song" and by_name["Song 21"] == "song"


def test_a_name_is_put_to_wikidata_once_however_often_it_is_used(tmp_path: Path) -> None:
    """A session player on four albums is one name to screen and one line to read."""
    names = [*_screened(tmp_path), screen.Name(name="Ivena Sorn", kind="person", where="again")]
    asked: list[str] = []

    def fetch(query: str) -> dict[str, Any]:
        asked.append(query)
        return _one_hit("Ivena Sorn")

    findings = screen.screen(names, fetch=fetch)
    assert sum(q.count('"Ivena Sorn"@en') for q in asked) == 1
    assert len(findings) == 1
    assert [u.where for u in findings[0].uses] == ["session player", "again"]


def test_the_query_asks_for_exact_matches_above_the_notability_floor() -> None:
    """D-009: below the floor every plausible name matches something and the screen means nothing."""
    query = screen.build_query(['Held "Note"', "Civic Lantern"])
    assert f"FILTER(?sitelinks >= {screen.SITELINK_FLOOR})" in query
    assert '"Held \\"Note\\""@en' in query, "a quote in a title must not break out of the query"
    assert "wd:Q5" in query and "wd:Q43229" in query, "people and organisations, not every string"


def test_names_are_screened_in_bounded_batches() -> None:
    many = [
        screen.Name(name=f"Name {n}", kind="song", where="x") for n in range(screen.BATCH * 2 + 1)
    ]
    sizes: list[int] = []

    def fetch(query: str) -> dict[str, Any]:
        sizes.append(query.count("@en"))
        return {"results": {"bindings": []}}

    assert screen.screen(many, fetch=fetch) == []
    assert len(sizes) == 3 == screen.requests_for(len(many))
    assert max(sizes) <= screen.BATCH


def test_a_screen_that_could_not_run_is_never_reported_as_clear(tmp_path: Path) -> None:
    """§25's unbreakable rule. An empty report reads as 'every name is clear', which is the one
    answer this tool must never give by accident."""

    def fetch(query: str) -> dict[str, Any]:
        raise screen.ScreenError("Wikidata did not answer after 3 attempts")

    with pytest.raises(screen.ScreenError):
        screen.screen(_screened(tmp_path), fetch=fetch)


def test_matches_are_reported_worst_first() -> None:
    payload = _one_hit("Held Note", qid="Q1", sitelinks=7)
    payload["results"]["bindings"] += _one_hit("Held Note", qid="Q2", sitelinks=90)["results"][
        "bindings"
    ]
    finding = screen.screen(
        [screen.Name(name="Held Note", kind="band", where="b_001")], fetch=lambda _: payload
    )[0]
    assert [m.qid for m in finding.matches] == ["Q2", "Q1"]
    assert finding.matches[0].url == "https://www.wikidata.org/wiki/Q2"
