"""What `make imaging-analyse` prints. Presentation only — every number was computed in `analyse.py`.

Split from `cli.py` for the reason `music/console.py` records: `cli.py` is where every make target
is declared (§17) and has to stay readable as a list of commands, while the table and the summary
are the part that grows each time a card adds an imaging target.
"""

from __future__ import annotations

from pathlib import Path

import typer

from station.imaging.analyse import BRIGHT_HZ, DARK_HZ, MIN_LOOP_S, SEAM_S, Measurement

HEADER = f"{'PIECE':<38}{'LENGTH':>8}{'RAMP':>7}{'ENERGY':>8}{'LOOP':>8}"


def measurement(m: Measurement) -> None:
    """One row of the table, flagged in yellow when it needs an ear."""
    loop = f"{m.bed_loop_sec:.1f}" if m.bed_loop_sec is not None else "—"
    line = (
        f"{Path(m.path).stem:<38}{m.duration_sec:>8.1f}{m.intro_ramp_sec:>7.1f}"
        f"{m.energy:>8.2f}{loop:>8}"
    )
    if m.flagged:
        typer.secho(f"{line}  check  {m.note}", fg="yellow")
    elif m.note:
        typer.secho(line, nl=False)
        typer.secho(f"  {m.note}", fg="bright_black")
    else:
        typer.echo(line)


def _length(measured: list[Measurement]) -> None:
    lengths = sorted(m.duration_sec for m in measured)
    typer.echo(
        f"  length      {sum(lengths) / 60:.1f} minutes in total, "
        f"{lengths[0]:.1f}s shortest, {lengths[-1]:.1f}s longest"
    )


def _run_up(measured: list[Measurement]) -> None:
    ramps = sorted(m.intro_ramp_sec for m in measured if m.intro_ramp_sec > 0)
    typer.echo(
        f"  run-up      {len(ramps)} with one to talk over, "
        f"{len(measured) - len(ramps)} at full level from the top"
    )
    if len(ramps) == 1:
        typer.echo(f"              the one runs {ramps[0]:.1f}s — worth an ear")
    elif ramps:
        typer.echo(
            f"              those run {ramps[0]:.1f}s to {ramps[-1]:.1f}s, "
            f"middle {ramps[len(ramps) // 2]:.1f}s — spot-check these by ear"
        )


def _energy(measured: list[Measurement]) -> None:
    values = sorted(m.energy for m in measured)
    typer.echo(
        f"  energy      {values[0]:.2f} to {values[-1]:.2f}, "
        f"middle {values[len(values) // 2]:.2f} — 0 is {DARK_HZ:.0f} Hz, 1 is {BRIGHT_HZ / 1000:.0f} kHz"
    )


def _loop(measured: list[Measurement]) -> None:
    long_enough = [m for m in measured if m.duration_sec >= 2 * SEAM_S + MIN_LOOP_S]
    found = [m for m in long_enough if m.bed_loop_sec is not None]
    typer.echo(
        f"  loop        {len(long_enough)} long enough to loop, "
        f"{len(found)} repeating its own ending closely enough to claim a seam"
    )
    if len(found) < len(long_enough):
        typer.secho(
            "              the rest do not repeat their ending — a fact about the audio, not a "
            "failed measurement.\n              A piece meant to be a bed and printing no seam is "
            "a piece that needs one edited in.",
            fg="bright_black",
        )


def analyse_summary(measured: list[Measurement], failed: list[str]) -> None:
    """What the whole pass found, and what has to be listened to."""
    if not measured:
        typer.secho("\nnothing could be measured", fg="red", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"\n{len(measured)} piece(s) measured, {len(failed)} unreadable.")
    _length(measured)
    _run_up(measured)
    _energy(measured)
    _loop(measured)
    for problem in failed:
        typer.secho(f"  UNREADABLE  {problem}", fg="red", err=True)

    flagged = [m for m in measured if m.flagged]
    if flagged:
        typer.secho(
            f"\n{len(flagged)} to listen to — §9 puts the last half-second of a ramp and the "
            "treatment of a loop seam\nbeyond what any measurement settles, and these are the rows "
            "the pass is least sure of.",
            fg="yellow",
        )
