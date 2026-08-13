"""`COMMISSION.md` §12's eight writing rules have to go red on the thing they name.

The point of M-45 is that a prose rule nobody counts is a preference. So the tests that matter are
the ones that break a correct album one way at a time and assert the command names it — the same
shape as `test_music.py`'s wiki tests, and for the same reason: six sessions of evidence that the
rules which survive are the ones with a number behind them.

One fixture album of six songs, deliberately varied, and one test per way of flattening it.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from station.music import check, writing

ROOT = Path(__file__).resolve().parents[2]

# A song built from parts, so a test can flatten exactly one of them. The default carries two
# world nouns, a named third party, no parenthetical echo, and does not sing its own title.
LYRIC = """[Intro - 8 seconds, {intro}]

[Verse 1]
The {noun_one} came in short and Talla counted it again,
She wrote the difference down and left it on the desk.

[{middle}]
{hook}

[Verse 2]
By the {noun_two} she had stopped explaining what it cost,
And nobody who owed her ever said the word out loud.

[Outro - 4 seconds, {intro}]
"""

NOUNS = ("manifest", "berth", "hauler", "airlock", "relay", "ration", "cargo", "hold")
MIDDLES = ("Chorus", "Refrain", "Bridge", "Pre-Chorus", "Turnaround", "Coda")


def _song(number: int, **flat: Any) -> dict[str, Any]:
    """One song of the fixture. Keyword arguments flatten it the way one rule cares about."""
    return {
        "id": f"s_{number:04d}",
        "title": f"Counted Twice {number}",
        "track_number": number,
        "lyrics": LYRIC.format(
            intro="fiddle alone",
            noun_one=flat.get("noun_one", NOUNS[number % len(NOUNS)]),
            noun_two=flat.get("noun_two", NOUNS[(number + 3) % len(NOUNS)]),
            middle=flat.get("middle", MIDDLES[number % len(MIDDLES)]),
            hook=flat.get("hook", "And she kept the difference, and she kept the desk."),
        ),
    }


def _fixture_album(**flat: Any) -> dict[str, Any]:
    """Six songs that pass all five lyric rules. `flat` applies to every song at once."""
    return {
        "album": {"id": "al_900", "title": "Counted Twice"},
        "songs": [_song(n, **flat) for n in range(1, 7)],
    }


def _root_with(tmp_path: Path, album: dict[str, Any] | None) -> Path:
    """A repository root holding the real §12 and task file, and one fixture album of lyrics."""
    music = tmp_path / "music"
    (music / writing.LYRICS_DIR).mkdir(parents=True, exist_ok=True)
    (music / "wiki").mkdir(exist_ok=True)
    for name in (writing.COMMISSION_FILE, check.TASKS_FILE):
        (music / name).write_text((ROOT / "music" / name).read_text(encoding="utf-8"))
    if album is not None:
        (music / writing.LYRICS_DIR / "al_900.yaml").write_text(yaml.safe_dump(album))
    return tmp_path


def _details(tmp_path: Path, album: dict[str, Any] | None, *, live: bool = True) -> str:
    """Every problem the rules find. `live` marks M-47 done, so rules 1 to 5 stop being owed.

    The card's heading is rewritten either way rather than read, so that these tests keep testing
    the same thing on the day M-47 actually lands.
    """
    root = _root_with(tmp_path, album)
    tasks = root / "music" / check.TASKS_FILE
    heading = f"### M-47 ·{' **DONE** ·' if live else ''} the fixture's stand-in"
    tasks.write_text(re.sub(r"^### M-47 ·.*$", heading, tasks.read_text(), count=1, flags=re.M))
    return "\n".join(p.line() for p in writing.check_writing(root))


# --- §12 itself -------------------------------------------------------------------------------


def test_the_rules_come_out_of_the_commission() -> None:
    """Nothing is hard-coded here: change a number in §12 and the command changes with it."""
    rules = writing.load_rules(ROOT / "music" / writing.COMMISSION_FILE)
    assert sorted(rules.threshold) == list(writing.RULES)
    assert rules.threshold[1] == pytest.approx(0.40)
    assert rules.threshold[2] == 3
    assert "burn day" in rules.world_nouns and "the lag" in rules.world_nouns
    assert "overdub" in rules.studio_words


def test_a_commission_without_section_twelve_stops_the_check(tmp_path: Path) -> None:
    root = _root_with(tmp_path, _fixture_album())
    (root / "music" / writing.COMMISSION_FILE).write_text("# no rules here\n")
    with pytest.raises(check.CheckError):
        writing.check_writing(root)


def test_rules_one_to_five_are_owed_to_the_card_that_rewrites_the_pilot(tmp_path: Path) -> None:
    """M-47 has not run, so a flat album is reported to nobody — and lands the moment it has."""
    flat = _fixture_album(middle="Chorus", hook="Counted twice (counted twice), counted twice.")
    assert _details(tmp_path, flat, live=False) == ""
    assert _details(tmp_path, flat) != ""


# --- the five lyric rules ---------------------------------------------------------------------


def test_a_varied_album_reports_nothing(tmp_path: Path) -> None:
    assert _details(tmp_path, _fixture_album()) == ""


def test_no_lyrics_at_all_is_not_a_failure(tmp_path: Path) -> None:
    """M-21 … M-29 have not been written. An empty directory is not a flat one."""
    assert _details(tmp_path, None) == ""


def test_one_structure_over_an_album_is_named(tmp_path: Path) -> None:
    detail = _details(tmp_path, _fixture_album(middle="Chorus"))
    assert "al_900" in detail and "rule 1" in detail and "6 of 6" in detail


def test_an_album_with_nobody_in_it_is_named(tmp_path: Path) -> None:
    """§3: songs are about someone. Six first-person songs is one narrator, not an album."""
    album = _fixture_album()
    for song in album["songs"]:
        song["lyrics"] = song["lyrics"].replace("Talla counted it again,", "I counted it again,")
        song["lyrics"] = song["lyrics"].replace("She wrote", "I wrote").replace("she had", "I had")
        song["lyrics"] = song["lyrics"].replace("who owed her", "who owed me")
        song["lyrics"] = song["lyrics"].replace("she kept", "I kept")
    detail = _details(tmp_path, album)
    assert "rule 2" in detail and "third person" in detail


def test_the_echoed_answer_on_every_song_is_named(tmp_path: Path) -> None:
    detail = _details(tmp_path, _fixture_album(hook="Keep the desk (keep the desk), keep it."))
    assert "rule 3" in detail and "echoed answer" in detail


def test_an_album_that_sings_its_own_titles_is_named(tmp_path: Path) -> None:
    album = _fixture_album()
    for number, song in enumerate(album["songs"], start=1):
        song["lyrics"] = song["lyrics"].replace(
            "And she kept the difference", f"And Counted Twice {number} is what she called it"
        )
    detail = _details(tmp_path, album)
    assert "rule 4" in detail and "titled after their own hook" in detail


def test_a_lyric_with_no_world_in_it_is_named(tmp_path: Path) -> None:
    """The swap-the-nouns test inverted: nothing to swap means nothing was ever there."""
    detail = _details(tmp_path, _fixture_album(noun_one="letter", noun_two="morning"))
    assert "s_0001" in detail and "world's own nouns" in detail


def test_an_album_too_short_to_have_a_distribution_is_left_alone(tmp_path: Path) -> None:
    """A two-track single would fail rule 1 for existing; §12 sets a floor and this is it."""
    album = _fixture_album(middle="Chorus")
    album["songs"] = album["songs"][:2]
    detail = _details(tmp_path, album)
    assert detail == ""


# --- the three wiki rules, against the real wiki ----------------------------------------------


def test_the_written_wiki_passes_every_live_rule() -> None:
    """The one that runs on the real thing: `make check` is red whenever this is not empty."""
    problems = writing.check_writing(ROOT)
    assert not problems, "the writing rules are broken:\n" + "\n".join(p.line() for p in problems)


def test_rules_seven_and_eight_are_owed_to_the_catalogue_wide_card() -> None:
    """Neither can be satisfied by the genre being written today, which is why M-15 owns them."""
    rules = writing.load_rules(ROOT / "music" / writing.COMMISSION_FILE)
    assert rules.owed_to[7] == rules.owed_to[8] == check.LAYER_B_CALENDAR_CARD


def test_layer_b_gets_its_own_calendar_only_when_that_card_lands() -> None:
    """The swap in `year_layers` is the other half of rule 7 — never neither, never both."""
    card = check.LAYER_B_CALENDAR_CARD
    assert check.year_layers({card: False}) == "AB", "until then, both layers cluster"
    assert check.year_layers({card: True}) == "A", "after it, layer B carries the calendar"
    with pytest.raises(check.CheckError, match=card):
        check.year_layers({"M-01": True})


def test_a_band_whose_facts_are_all_studio_anecdotes_is_named(tmp_path: Path) -> None:
    """Rule 6 is live today, so it gets the real check's treatment: break it, and be named."""
    root = _root_with(tmp_path, None)
    (root / "music" / "wiki" / "core-harmonies.yaml").write_text(
        yaml.safe_dump(
            {
                "layer_a": {
                    "bands": [
                        {
                            "id": "b_001",
                            "name": "Held Note",
                            "kind": "group",
                            "genre": "core-harmonies",
                            "label": "label_1",
                            "active_from": 2600,
                        }
                    ],
                    "albums": [
                        {
                            "id": "al_001",
                            "title": "One Room",
                            "band": "b_001",
                            "label": "label_1",
                            "genre": "core-harmonies",
                            "release_year": 2600,
                            "songs": [
                                {
                                    "id": f"s_{n:04d}",
                                    "title": f"Song {n}",
                                    "track_number": n,
                                    "playable": True,
                                    "fact": "Kept from the second take, after the engineer moved "
                                    "the microphone."
                                    if n > 1
                                    else "Vara Ennel wrote it walking.",
                                }
                                for n in range(1, 5)
                            ],
                        }
                    ],
                }
            }
        )
    )
    detail = "\n".join(p.line() for p in writing.check_writing(root))
    assert "Held Note" in detail and "b_001" in detail and "studio anecdotes" in detail
