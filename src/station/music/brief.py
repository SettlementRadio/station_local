"""Assemble a complete, ready-to-paste brief for the music writer (`music/RUNBOOK.md`).

Why this is a target rather than a paragraph in the runbook: a brief is `COMMISSION.md`, plus the
fixed points in `CONSTANTS.md`, plus one genre's slice of `plan.yaml` — three files the operator was
stitching together by hand, which is exactly where the thread was being lost. Nothing here calls a
model or invents anything; it concatenates files the operator owns and fills in numbers that are
already fixed.

Two kinds of brief come out, matching the runbook's two-chat pattern: `write` goes to the writer,
`check` goes to a *different* conversation, because a writer marking its own homework always passes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

from station.music import wiki

Kind = Literal["write", "check"]

# `music/wiki/<genre>.yaml` is where a checked genre lands; `check` reads it back.
WIKI_DIR = "wiki"


class BriefError(RuntimeError):
    """A brief could not be assembled. The message names the file or genre to fix."""


class LabelSlice(BaseModel):
    """One label's share of a genre: how many songs, spread over how many bands."""

    label: int
    songs: int = Field(gt=0)
    bands: int = Field(gt=0)


class GenreSlice(BaseModel):
    """One genre's whole allocation across the three layers."""

    title: str
    layer_b_bands: int = Field(ge=0)
    layer_c_figures: int = Field(ge=0)
    labels: list[LabelSlice] = Field(min_length=1)

    @property
    def songs(self) -> int:
        return sum(s.songs for s in self.labels)

    @property
    def bands(self) -> int:
        return sum(s.bands for s in self.labels)


class Plan(BaseModel):
    """`music/plan.yaml` — the allocation of playable songs across genres and labels."""

    labels: dict[int, str]
    genres: dict[str, GenreSlice]

    @property
    def total_songs(self) -> int:
        return sum(g.songs for g in self.genres.values())

    @property
    def total_bands(self) -> int:
        return sum(g.bands for g in self.genres.values())

    def bands_per_label(self) -> dict[int, int]:
        """Bands each label ends up with. §5 requires at least three, or no retrospective."""
        counts = dict.fromkeys(self.labels, 0)
        for genre in self.genres.values():
            for slice_ in genre.labels:
                counts[slice_.label] += slice_.bands
        return counts

    def songs_per_label(self) -> dict[int, int]:
        counts = dict.fromkeys(self.labels, 0)
        for genre in self.genres.values():
            for slice_ in genre.labels:
                counts[slice_.label] += slice_.songs
        return counts


def load_plan(path: Path) -> Plan:
    """Read and validate `plan.yaml`, or fail naming the file."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise BriefError(f"missing {path} — see music/RUNBOOK.md step 3") from None
    except yaml.YAMLError as exc:
        raise BriefError(f"{path} is not valid YAML: {exc}") from None
    return Plan.model_validate(raw)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise BriefError(f"missing {path}") from None


def _label_lines(genre: GenreSlice, plan: Plan) -> str:
    return "\n".join(
        f"  Label {s.label} ({plan.labels[s.label]}): {s.songs} songs across {s.bands} band(s)"
        for s in genre.labels
    )


def _write_instruction(name: str, genre: GenreSlice, plan: Plan) -> str:
    """The one instruction that follows COMMISSION.md in the writer's chat."""
    return f"""\
Write the {genre.title} section of the wiki.

LAYER A — {genre.songs} songs, {genre.bands} bands, distributed exactly like this:
{_label_lines(genre, plan)}
  Full bios, full album stories, every song with its one fact, playable: true.

LAYER B — about {genre.layer_b_bands} more {genre.title} bands the station does not hold.
  Two-sentence bios, one-line album notes, song titles only, playable: false.

LAYER C — about {genre.layer_c_figures} {genre.title} figures from 2426-2546.
  Three sentences each. No albums, no track lists — their recordings are lost.

Return YAML only. No lyrics, no prompts, no style cards, no durations.
Genre slug for every entry: {name}"""


_CHECKS = """\
1.  Band, album and song counts per layer against what was asked above.
2.  Every layer-A song has playable: true and exactly one concrete, sayable fact.
    Not a mood, not a summary.
3.  No layer-B song has a fact. No layer-C figure has an album or track list.
4.  Release years fall on the anchor years, or have a stated reason.
5.  No age, no relative date, no "recently", no "last year". Years only.
6.  Every band has active years. No career exceeds about 35 years.
7.  No session player is credited outside their active years.
8.  No real artist, band, label, album or song name anywhere.
9.  No name repeats one from the used-names list.
10. Bios are plain speech, not lyrical.
11. No song is about leaving Earth, the crossing, the cradle or the long dark.
12. Every song has a vocal. No instrumentals."""


def _check_instruction(name: str, genre: GenreSlice, plan: Plan, returned: str) -> str:
    """The checker prompt, for a different conversation than the one that wrote the genre."""
    return f"""\
You are checking one genre of a music wiki against the brief above. Report only
failures, as a numbered list. Do not rewrite anything. Do not be encouraging.

What was asked for:

LAYER A — {genre.songs} songs, {genre.bands} bands:
{_label_lines(genre, plan)}
LAYER B — about {genre.layer_b_bands} bands.
LAYER C — about {genre.layer_c_figures} figures, 2426-2546.

Check:

{_CHECKS}

End with PASS or FAIL.

--- the {name} wiki as returned ---

{returned}"""


def _style_instruction(genre_wiki: wiki.GenreWiki, name: str) -> str:
    """Ask for one style card per layer-A band, from the line-up the writer already invented."""
    rosters = "\n\n".join(
        f"{b.name}  (id: {b.id}, {b.kind}, {b.label}, {b.active_from}-{b.active_to or 'now'})\n"
        f"  movement: {b.movement_line}\n{b.line_up()}"
        for b in genre_wiki.bands
    )
    return f"""\
Write a style card for each of these {name} bands. Six lines each, exactly the
format in COMMISSION.md section 7:

  voice / backing / instruments / production / tempo range / exclude

Use the production palette for {name}. Build the instruments line from the
line-up below — these players are already fixed.

THE VOICE LINE IS FIXED FOR THE LIFE OF THE BAND. It never changes between
albums. State the lead singer's gender, register, texture and delivery.

Return YAML: band id at the top level, the six lines beneath it. Nothing else.

--- the bands ---

{rosters}"""


def _songs_instruction(album: wiki.Album, band: wiki.Band, card: str) -> str:
    """Everything needed to write one album: the story, the line-up, the titles and their facts."""
    songs = "\n".join(
        f"{s.track_number:>3}. {s.title}\n"
        f"     mood: {', '.join(s.mood_tags) or 'unstated'}\n"
        f"     fact: {s.fact or 'MISSING — flag this'}"
        for s in album.playable_songs
    )
    style = card or "  MISSING — run `make music-style` for this genre first."
    return f"""\
Album: "{album.title}" — {band.name}, {album.release_year}, {album.genre}.
Label: {album.label}. {"Cornerstone album." if album.cornerstone else ""}

What this record is:
  {album.notes}

The band's style card — every prompt below must obey it, especially the voice line:
{style}

For each of the {len(album.playable_songs)} songs, return:
  1. lyrics — COMMISSION.md section 3 subject rules and the swap-the-nouns test.
     Open with an instrumental-intro tag before the first verse. The song's
     existing fact is already true of it; write lyrics that fit that fact.
  2. a generation prompt — the style card, plus this song's mood, tempo and one
     arrangement note — and an exclude line.

Every song has a vocal. Nothing about leaving Earth. Keep the album coherent:
this is one band, in one room, in one year.

Return YAML keyed by song id.

--- the songs ---

{songs}"""


def build_style(name: str, root: Path) -> str:
    """The style-card brief for one genre's layer-A bands."""
    music = root / "music"
    genre_wiki = wiki.load_genre(music / WIKI_DIR / f"{name}.yaml")
    if not genre_wiki.bands:
        raise BriefError(f"{name} has no layer-A bands to write style cards for")
    return (
        "\n\n".join(
            [_read(music / "COMMISSION.md"), "\n---\n", _style_instruction(genre_wiki, name)]
        )
        + "\n"
    )


def build_songs(album_id: str, root: Path) -> str:
    """The lyrics-and-prompts brief for one album."""
    music = root / "music"
    try:
        album, band, _ = wiki.find_album(music / WIKI_DIR, album_id)
    except wiki.WikiError as exc:
        raise BriefError(str(exc)) from None
    card = wiki.load_styles(music / "production" / "styles.yaml").get(band.id, "")
    return (
        "\n\n".join(
            [_read(music / "COMMISSION.md"), "\n---\n", _songs_instruction(album, band, card)]
        )
        + "\n"
    )


def build(kind: Kind, name: str, root: Path) -> str:
    """Assemble one brief. `root` is the repository root."""
    music = root / "music"
    plan = load_plan(music / "plan.yaml")
    if name not in plan.genres:
        known = ", ".join(sorted(plan.genres))
        raise BriefError(f"unknown genre {name!r} — plan.yaml has: {known}")
    genre = plan.genres[name]

    parts = [
        _read(music / "COMMISSION.md"),
        "\n---\n\n# The fixed points\n",
        _read(music / "CONSTANTS.md"),
        "\n---\n",
    ]
    if kind == "write":
        parts.append(_write_instruction(name, genre, plan))
    else:
        returned = _read(music / WIKI_DIR / f"{name}.yaml")
        parts.append(_check_instruction(name, genre, plan, returned))
    return "\n\n".join(parts) + "\n"
