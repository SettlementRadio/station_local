"""`COMMISSION.md` §12's ten writing rules have to go red on the thing they name.

The point of M-45 is that a prose rule nobody counts is a preference. So the tests that matter are
the ones that break a correct album one way at a time and assert the command names it — the same
shape as `test_music.py`'s wiki tests, and for the same reason: six sessions of evidence that the
rules which survive are the ones with a number behind them.

One fixture album of six songs, deliberately varied, and one test per way of flattening it. M-50
added two rules about length, so the fixture is now a full-length lyric: three verses and past
rule 10's word floor, with knobs that take away one of those without touching the other.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from station.music import check, commission, writing

ROOT = Path(__file__).resolve().parents[2]

# A song built from parts, so a test can flatten exactly one of them. The default carries two
# world nouns, a named third party, no parenthetical echo, three verses, enough words to clear
# rule 10, and does not sing its own title.
LYRIC = """[Intro - 8 seconds, {intro}]

[Verse 1]
The {noun_one} came in short and Talla counted it again,
She wrote the difference down and left it on the desk.
Nobody asked her twice and nobody asked her once,
And the paper sat all evening underneath the reading lamp.
She has a way of writing numbers nobody can argue with,
A small clear hand that never once has needed to be loud.

[{middle}]
{hook}

[Verse 2]
By the {noun_two} she had stopped explaining what it cost,
And nobody who owed her ever said the word out loud.
The men who signed for it were somewhere warm and unavailable,
The woman who did not sign for it was standing in the wet.
She learned the trick of waiting where the argument would come to her,
Which is cheaper than going out to meet it in the road.
Everyone she works beside has told her she should let it go,
And every one of them has asked her privately what the number was.

[{middle}]
{hook}

[Verse 3]
There is a version where she says it plainly to their faces,
And a version where she writes it and says nothing else at all.
She has written it so often that the writing does the arguing,
And the faces are a thing she can decline to look at now.
Whatever else is missing, the account of it is honest,
And an honest empty column is worth more than a full one.
The lamp is on the desk and the desk is where it happened,
And the whole of it will still be there tomorrow if they want it.
{extra}
[Outro - 4 seconds, {intro}]
"""

# The lines rule 10 costs: the default lyric clears the floor, and without these it does not.
EXTRA = """
[{middle}]
{hook}

[Coda]
Talla put the light out on the desk and left the total where it was,
Because a number nobody disputes is a number nobody remembers,
And she would rather be remembered for the one they all disputed,
And she would rather leave it written than explain it in the morning.
"""

NOUNS = ("manifest", "berth", "hauler", "airlock", "relay", "ration", "cargo", "hold")
MIDDLES = ("Chorus", "Refrain", "Bridge", "Pre-Chorus", "Turnaround", "Coda")


def _song(number: int, **flat: Any) -> dict[str, Any]:
    """One song of the fixture. Keyword arguments flatten it the way one rule cares about."""
    parts = {
        "intro": "fiddle alone",
        "noun_one": flat.get("noun_one", NOUNS[number % len(NOUNS)]),
        "noun_two": flat.get("noun_two", NOUNS[(number + 3) % len(NOUNS)]),
        "middle": flat.get("middle", MIDDLES[number % len(MIDDLES)]),
        "hook": flat.get("hook", "And she kept the difference, and she kept the desk."),
    }
    lyric = LYRIC.format(extra=flat.get("extra", EXTRA), **parts).format(**parts)
    return {
        "id": f"s_{number:04d}",
        "title": f"Counted Twice {number}",
        "track_number": number,
        "lyrics": lyric.replace("[Verse 3]", flat.get("third", "[Verse 3]")),
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
    for name in (commission.COMMISSION_FILE, check.TASKS_FILE):
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
    rules = commission.load_rules(ROOT / "music" / commission.COMMISSION_FILE)
    assert sorted(rules.threshold) == list(commission.RULES)
    assert rules.threshold[1] == pytest.approx(0.40)
    assert rules.threshold[2] == 3
    assert rules.threshold[9] == 3, "M-50: three verses"
    assert rules.threshold[10] >= 280, "M-50: the word floor, and it is not the pilot's mean"
    assert "burn day" in rules.world_nouns and "the lag" in rules.world_nouns
    assert "overdub" in rules.studio_words
    assert rules.exempt_albums == ("al_001", "al_002", "al_003", "al_004")


def test_a_commission_without_section_twelve_stops_the_check(tmp_path: Path) -> None:
    root = _root_with(tmp_path, _fixture_album())
    (root / "music" / commission.COMMISSION_FILE).write_text("# no rules here\n")
    with pytest.raises(check.CheckError):
        writing.check_writing(root)


def test_rules_one_to_five_are_owed_to_the_card_that_rewrites_the_pilot(tmp_path: Path) -> None:
    """M-47 has not run, so a flat album is reported to nobody — and lands the moment it has."""
    flat = _fixture_album(middle="Chorus", hook="Counted twice (counted twice), counted twice.")
    assert _details(tmp_path, flat, live=False) == ""
    assert _details(tmp_path, flat) != ""


# --- the seven lyric rules ---------------------------------------------------------------------


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
        song["lyrics"] = re.sub(r"\b(Talla|She|she|her|hers|he|him|his)\b", "I", song["lyrics"])
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


def test_a_song_with_two_verses_is_named(tmp_path: Path) -> None:
    """M-50 rule 9. The words are untouched, so only the verse count can be what went red."""
    detail = _details(tmp_path, _fixture_album(third="[Bridge]"))
    assert "al_900" in detail and "s_0001" in detail
    assert "rule 9" in detail and "2 verse section(s)" in detail
    assert "rule 10" not in detail, "taking a tag away must not also take the words away"


def test_a_song_too_short_to_fill_the_hour_is_named(tmp_path: Path) -> None:
    """M-50 rule 10. Three verses are still there; there are simply not enough words in them."""
    detail = _details(tmp_path, _fixture_album(extra=""))
    assert "al_900" in detail and "s_0001" in detail
    assert "rule 10" in detail and "sung words" in detail
    assert "rule 9" not in detail, "a short lyric is not a lyric missing a verse"


# --- the three wiki rules, against the real wiki ----------------------------------------------


def test_the_written_wiki_passes_every_live_rule() -> None:
    """The one that runs on the real thing: `make check` is red whenever this is not empty."""
    problems = writing.check_writing(ROOT)
    assert not problems, "the writing rules are broken:\n" + "\n".join(p.line() for p in problems)


def test_the_pilot_is_exempt_from_the_length_rules_and_still_counted() -> None:
    """M-50's exemption is four ids in §12, and it is the opposite of a rule nobody counts.

    The pilot's 45 are the only lyrics that exist and the only ones rules 9 and 10 will never
    apply to, so this is where the floor can be watched working: every finding against those four
    albums is counted, none of them is fatal, and `make check` stays green on all of it (D-087).
    """
    exempt = [f for f in writing.count_writing(ROOT) if f.exempt]
    albums = {f.problem.genre for f in exempt}
    assert albums == {"al_001", "al_002", "al_003", "al_004"}
    assert {f.rule for f in exempt} == {9, 10}
    assert not any(f.fatal for f in exempt)
    short_on_words = [f for f in exempt if f.rule == 10]
    assert len(short_on_words) == 45, "the floor is above every one of the pilot's lyrics"


def test_rules_seven_and_eight_are_owed_to_the_catalogue_wide_card() -> None:
    """Neither can be satisfied by the genre being written today, which is why M-15 owns them."""
    rules = commission.load_rules(ROOT / "music" / commission.COMMISSION_FILE)
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


# --- a collection's stub lyrics (M-52) ---------------------------------------------------------


def _collection_wiki(root: Path, album_id: str) -> None:
    """An `independents.yaml` owning one album, which is how `writing.py` knows it is a stub."""
    (root / "music" / "wiki" / "independents.yaml").write_text(
        yaml.safe_dump(
            {
                "layer_a": {
                    "albums": [
                        {
                            "id": album_id,
                            "title": "Green Lights",
                            "band": "b_101",
                            "label": "unsigned",
                            "genre": "independents",
                            "release_year": 2615,
                            "songs": [],
                        }
                    ]
                }
            }
        )
    )


def _all_ten_live(root: Path) -> Path:
    """Mark M-47 done, the way `_details` does, so no rule is merely owed and the skip is the
    only thing that can be keeping the stub green."""
    tasks = root / "music" / check.TASKS_FILE
    heading = "### M-47 · **DONE** · the fixture's stand-in"
    tasks.write_text(re.sub(r"^### M-47 ·.*$", heading, tasks.read_text(), count=1, flags=re.M))
    return root


def _stub(album_id: str) -> dict[str, Any]:
    """What M-54 files: the ids and the titles, and no lyrics — the takes predate the commission."""
    return {
        "album": {"id": album_id, "title": "Green Lights"},
        "songs": [
            {"id": f"s_{n:04d}", "title": f"Song {n}", "track_number": n} for n in range(101, 107)
        ],
    }


def test_a_collection_album_with_no_lyrics_is_exempt(tmp_path: Path) -> None:
    """M-52 check 7. There is no written lyric to count and inventing one would be a lie about
    what the take sings, so §12 has no claim on it — the file exists for `tag.py`'s sake (M-54)."""
    root = _all_ten_live(_root_with(tmp_path, None))
    (root / "music" / writing.LYRICS_DIR / "al_101.yaml").write_text(
        yaml.safe_dump(_stub("al_101"))
    )
    _collection_wiki(root, "al_101")
    assert writing.check_writing(root) == []


def test_a_genre_album_with_no_lyrics_still_goes_red(tmp_path: Path) -> None:
    """The other half, and the reason the exemption is keyed to the wiki rather than to emptiness:
    an album of the 500 with nothing written in it is a card nobody did."""
    root = _all_ten_live(_root_with(tmp_path, None))
    (root / "music" / writing.LYRICS_DIR / "al_101.yaml").write_text(
        yaml.safe_dump(_stub("al_101"))
    )
    detail = "\n".join(p.line() for p in writing.check_writing(root))
    assert "al_101" in detail and "rule 9" in detail and "rule 10" in detail


def test_a_collection_album_that_does_carry_lyrics_is_counted(tmp_path: Path) -> None:
    """Exempt is a fact about a stub, not about a shelf: words written here are held to §12 like
    any others, or the collection becomes the place to put a lyric nobody wanted counted."""
    root = _all_ten_live(_root_with(tmp_path, _fixture_album(middle="Chorus")))
    _collection_wiki(root, "al_900")
    detail = "\n".join(p.line() for p in writing.check_writing(root))
    assert "al_900" in detail and "rule 1" in detail
