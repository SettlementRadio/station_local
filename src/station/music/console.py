"""What the five music commands print. Moved out of `cli.py`, which had reached §31's 400 lines.

`cli.py` is where every make target is declared (§17) and it has to stay readable as a list of
commands. The tables, the summaries and the colours are presentation for one subject — the music
job — and they are the part that grows every time a card adds a target, so they live beside the
modules they report on. Nothing here decides anything; every number it prints was computed in
`analyse.py`, `tag.py`, `screen.py` or `catalogue.py`.
"""

from __future__ import annotations

from pathlib import Path

import typer

from station.music import catalogue as catalogue_module
from station.music import dispatch as dispatch_module
from station.music import tag as tagger
from station.music.analyse import Measurement
from station.music.screen import Report
from station.music.tag import Result, Song, Summary

# --- make music-screen ------------------------------------------------------------------------


def screen_report(report: Report) -> int:
    """One genre's findings. Returns how many names need looking at."""
    typer.echo(f"\n  {report.screened} distinct names, used in {report.uses} places")
    if not report.findings:
        typer.secho("  nothing matched. Every name is clear on the mechanical test.\n", fg="green")
        return 0

    for finding in report.findings:
        typer.secho(f"\n  {finding.name}", fg="yellow", bold=True)
        for use in finding.uses:
            typer.echo(f"      used as {use.kind} — {use.where}")
        for match in finding.matches:
            what = " — ".join(x for x in (match.kinds, match.description) if x)
            typer.echo(f"      {match.qid:<10} {match.sitelinks:>3} sitelinks  {what}")
            typer.secho(f"      {' ' * 10} {match.url}", fg="bright_black")
    typer.echo(f"\n  {len(report.findings)} name(s) to look at.\n")
    return len(report.findings)


# --- make music-analyse -----------------------------------------------------------------------


def measurement(m: Measurement, track: str) -> None:
    """One row of the table, flagged in yellow when it needs an ear."""
    minutes, seconds = divmod(round(m.duration_sec), 60)
    line = (
        f"{track:<10}{minutes:>6}:{seconds:02d}{m.intro_ramp_sec:>7.1f}  {m.outro_type:<9}"
        f"{'check  ' + m.note if m.flagged else ''}"
    )
    typer.secho(line, fg="yellow" if m.flagged else None)


def analyse_summary(measured: list[Measurement], failed: list[str]) -> None:
    """What the whole pass found, and what has to be listened to."""
    if not measured:
        typer.secho("\nnothing could be measured", fg="red", err=True)
        raise typer.Exit(code=1)
    ramps = [m.intro_ramp_sec for m in measured]
    with_ramp = [r for r in ramps if r > 0]
    total = sum(m.duration_sec for m in measured)
    kinds = {k: sum(1 for m in measured if m.outro_type == k) for k in ("cold", "fade", "sustain")}
    flagged = [m for m in measured if m.flagged]

    typer.echo(f"\n{len(measured)} song(s) measured, {len(failed)} unreadable.")
    typer.echo(
        f"  duration    {total / len(measured) / 60:.2f} minutes average, "
        f"{min(m.duration_sec for m in measured) / 60:.2f} shortest, "
        f"{max(m.duration_sec for m in measured) / 60:.2f} longest"
    )
    typer.echo(
        f"  intro ramp  {len(with_ramp)} with a measurable run-up, "
        f"{len(measured) - len(with_ramp)} singing from the top"
    )
    ordered = sorted(with_ramp)
    if len(ordered) == 1:
        typer.echo(f"              the one runs {ordered[0]:.1f}s — worth an ear")
    elif ordered:
        typer.echo(
            f"              those run {ordered[0]:.1f}s to {ordered[-1]:.1f}s, "
            f"middle {ordered[len(ordered) // 2]:.1f}s — spot-check these by ear"
        )
    typer.echo(
        f"  outro       {kinds['cold']} cold · {kinds['fade']} fade · {kinds['sustain']} sustain"
    )
    for problem in failed:
        typer.secho(f"  UNREADABLE  {problem}", fg="red", err=True)
    if flagged:
        typer.secho(
            f"\n{len(flagged)} to listen to — the ramp is a judgement in the last half-second "
            "(ARCHITECTURE §9) and these are the ones the measurement is least sure of.",
            fg="yellow",
        )


# --- make music-tag ---------------------------------------------------------------------------


def tag_row(song: Song, result: Result) -> None:
    """One file: what it now says, and whether this pass had to write it."""
    colour = {"failed": "red", "pending": "yellow", "written": "green"}.get(result.action)
    values = song.provenance
    line = (
        f"{song.track_number:<7}{values.licence_period:<20}{values.model_version:<8}"
        f"{values.generated_on:<12}{result.action:<10}{result.note}"
    )
    typer.secho(line, fg=colour)


def tag_summary(summary: Summary, results: list[Result], whole: bool) -> None:
    """The counts, one file's tags in full, and a non-zero exit if anything is still uncovered."""
    typer.echo(
        f"\n{summary.written} written · {summary.unchanged} already correct · "
        f"{summary.pending} waiting for audio · {summary.failed} failed"
    )
    for result in (r for r in results if r.action == "failed"):
        typer.secho(f"  FAILED      {result.note}", fg="red", err=True)
    for path in summary.unclaimed:
        typer.secho(f"  UNCLAIMED   {path} — no lyrics file records a take for it", fg="red")

    done = next((r for r in results if r.action in ("written", "unchanged")), None)
    if done:  # the card's check in one place: read one file, and it tells you what it is
        typer.echo(f"\nwhat one file now says — {done.path}")
        present = tagger.read_tags(Path(done.path))
        for key in tagger.TAG_KEYS:
            typer.echo(f"  {key:<18}{present.get(key, '—')}")

    if not summary.complete:
        raise typer.Exit(code=1)
    covered = f"all {summary.carrying_tags} file(s) under music/audio carry the four tags"
    typer.secho(
        f"\n{covered}" if whole else f"\n{summary.carrying_tags} file(s) tagged", fg="green"
    )


# --- make music-catalogue ---------------------------------------------------------------------


def measuring() -> None:
    """One dot per take measured. A 500-song pass is eight minutes and must not look stuck."""
    typer.secho("·", fg="bright_black", nl=False)


def catalogue_summary(built: catalogue_module.Build, problems: list[str], path: Path) -> bool:
    """What went into the file, what is still waiting for a Suno card, and whether it is usable."""
    written = built.catalogue
    playable = [t for t in written.tracks if t.playable]
    typer.secho(f"\n\n{path}", bold=True)
    typer.echo(
        f"  {len(written.labels)} labels · {len(written.artists)} artists · "
        f"{len(written.albums)} albums · {len(written.tracks)} tracks"
    )
    typer.echo(
        f"  {len(playable)} playable — audio on disk, measured and licensed. "
        f"{len(written.tracks) - len(playable)} carry a title and no file."
    )
    _rotation(playable)
    if built.unlabelled:
        stated = ", ".join(f"{word} ({count})" for word, count in built.unlabelled.items())
        typer.echo(f"  no house: {stated}")
    if not any(label.house_style for label in written.labels):
        typer.secho(
            f"  none of the {len(written.labels)} labels states a house style — §8 gives labels one "
            "and no genre file writes it. Harmless today; it is what a specialist show is built on.",
            fg="yellow",
        )
    for problem in built.unmeasurable:
        typer.secho(f"  UNMEASURABLE  {problem} — left unplayable rather than guessed", fg="red")
    for problem in problems:
        typer.secho(f"  PROBLEM       {problem}", fg="red", err=True)

    if problems or built.unmeasurable:
        typer.secho("\ncatalogue.yaml was written, and it is not usable as it stands.", fg="red")
        return False
    typer.secho(f"\n{path} agrees with the wiki. `make check` re-runs this every time.", fg="green")
    return True


def _rotation(playable: list[catalogue_module.Track]) -> None:
    """The rotation weights the file hands the scheduler, which is the half nobody can see (§8)."""
    if not playable:
        typer.echo("  no audio yet — every row is a title (M-18, then M-30 … M-38)")
        return
    counts = {
        name: sum(1 for track in playable if track.category == name)
        for name in (catalogue_module.HEAVY, catalogue_module.GOLD)
    }
    heavy, gold = counts[catalogue_module.HEAVY], counts[catalogue_module.GOLD]
    typer.echo(
        f"  rotation: {heavy} in heavy rotation, {gold} gold — a record "
        f"{catalogue_module.GOLD_AFTER_YEARS} in-world years old or more is catalogue (§8, D-085)"
    )


# --- make music-dispatch ----------------------------------------------------------------------


DISPATCH_HEADER = f"{'TAKE':<12}{'SONG':<9}{'TRACK':<18}{'MATCH':<8}{'GAP':<7}"


def dispatch_plan(plan: dispatch_module.Plan, waiting: int) -> None:
    """Every take, the song its own words claim, and how clearly it claims it (D-091)."""
    typer.echo(f"{len(plan.assignments)} take(s) against {waiting} song(s) waiting for audio\n")
    typer.echo(DISPATCH_HEADER)
    album = ""
    for found in sorted(plan.assignments, key=lambda a: (a.song.album_id, a.song.track_number)):
        if found.song.album_id != album:
            album = found.song.album_id
            typer.secho(f"\n{album}", bold=True)
        weak = found.score < _CLOSE_ENOUGH
        typer.secho(
            f"{found.take.path.name:<12}{found.song.song_id:<9}"
            f"{found.song.track_number:>2}  {found.song.title[:14]:<14}"
            f"{found.score:>5.0%}   {found.gap:>+5.0%}",
            fg="yellow" if weak else None,
        )


# A take under this still files — the gap and the bijection are what prove it — but it is worth the
# operator's eye, because it means Suno sang something a fair way from the words it was given.
_CLOSE_ENOUGH = 0.85

# How many drifted song ids to name before the line stops being readable.
_NAMED_IN_LINE = 6


def dispatch_summary(plan: dispatch_module.Plan) -> None:
    """Why the pile may not be filed, or what filing it would do. Refused whole, never in part."""
    drifted = [f for f in plan.assignments if f.score < _CLOSE_ENOUGH]
    if drifted:
        typer.secho(
            f"\n{len(drifted)} take(s) sing a fair way from the words they were given — "
            f"{', '.join(f.song.song_id for f in drifted[:_NAMED_IN_LINE])}"
            f"{' …' if len(drifted) > _NAMED_IN_LINE else ''}",
            fg="yellow",
        )
        typer.echo("  that is a finding for your ear, not a reason not to file them.")
    if plan.unclaimed_songs:
        typer.secho(
            f"\n{len(plan.unclaimed_songs)} song(s) no take claims: "
            f"{', '.join(plan.unclaimed_songs)}",
            fg="red",
        )
        typer.echo("  a lyric with no audio is a song that was never generated (D-091).")
    for problem in plan.problems:
        typer.secho(f"  {problem}", fg="red")
    if not plan.ok:
        typer.secho("\nnothing was moved.", fg="red")
