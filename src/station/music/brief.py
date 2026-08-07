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
