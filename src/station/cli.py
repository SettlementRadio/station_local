"""The one entry point: every `make` target calls into here (§17).

Why the config import is deferred into `_boot`: importing `station.config` is what validates the
environment (§23), and it must fail as a message that names the missing line rather than as a
traceback. Nothing above that call may import config, or the failure escapes the handler.
"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import typer

from station import __version__

if TYPE_CHECKING:
    from station.config import Settings
    from station.music.screen import Report

app = typer.Typer(add_completion=False, help="Settlement Radio — operator commands (§17).")


@dataclass(frozen=True)
class Tool:
    """A system tool `make setup` expects, and whether the Studio can work without it."""

    command: str
    required: bool
    install: str
    note: str


# §22's Homebrew list, split by where the tool actually runs (§4): liquidsoap and icecast live on
# the Transmitter, so a Studio without them is fine and says so rather than failing.
TOOLS = (
    Tool("uv", True, "brew install uv", "package manager; the lockfile is authoritative"),
    Tool("gitleaks", True, "brew install gitleaks", "secret scan, pre-commit and CI"),
    Tool("ffmpeg", True, "brew install ffmpeg", "mix, loudness, ffprobe"),
    Tool("psql", True, "brew install postgresql@16", "world database"),
    Tool("liquidsoap", False, "brew install liquidsoap", "Transmitter-side; optional locally"),
    Tool("icecast", False, "brew install icecast", "Transmitter-side; optional locally"),
)


def _boot() -> Settings:
    """Load settings, or stop with the lines to fix. This is the fail-fast gate of §23."""
    try:
        from station.config import settings
    except RuntimeError as exc:  # ConfigError — config.py raises it while being imported
        typer.secho(f"\n{exc}\n", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=2) from None
    return settings


# Commands that read only files already in the repository and touch no environment. §23's gate
# exists to stop the *station* running mis-configured; it must not stop the operator writing
# content. The music wiki is deliberately buildable before any hardware or volume exists (D-044).
CONFIG_FREE = frozenset({"version", "music-albums", "music-screen"})


@app.callback()
def _main(ctx: typer.Context) -> None:
    """Validate configuration before any command runs, then configure logging once."""
    from station import log

    if ctx.invoked_subcommand in CONFIG_FREE:
        log.configure()
        return
    settings = _boot()
    log.configure(settings.log_level)
    ctx.obj = settings


@app.command()
def version() -> None:
    """Print the station version and the Python running it."""
    typer.echo(f"settlement-radio {__version__} (python {sys.version.split()[0]})")


@app.command()
def doctor(ctx: typer.Context) -> None:
    """Report whether this machine can run the station: config, volume, system tools."""
    settings: Settings = ctx.obj
    problems = 0

    typer.echo("configuration")
    typer.echo("  .env                 loaded, all required lines present")
    typer.echo(f"  media_root           {settings.media_root}")
    if not settings.media_root.is_dir():
        typer.secho(
            "                       missing — the external volume is not mounted", fg="yellow"
        )
    typer.echo(
        f"  cast engine          {settings.tts.cast_engine} (fallback {settings.tts.fallback_engine})"
    )
    typer.echo(
        f"  batch window         {settings.batch.start_hour}:00 → {settings.batch.must_finish_by}"
    )

    typer.echo("\nsystem tools")
    for tool in TOOLS:
        path = shutil.which(tool.command)
        if path:
            typer.echo(f"  {tool.command:<20} {path}")
        elif tool.required:
            problems += 1
            typer.secho(f"  {tool.command:<20} MISSING — {tool.install}", fg="red")
        else:
            typer.secho(f"  {tool.command:<20} absent — {tool.note}", fg="yellow")

    if problems:
        typer.secho(f"\n{problems} required tool(s) missing. Run `make setup`.", fg="red", err=True)
        raise typer.Exit(code=1)
    typer.secho("\nready", fg="green")


_GENRE_FILTER = typer.Option(None, "--genre", help="only this genre")


@app.command("music-albums")
def music_albums(genre: str = _GENRE_FILTER) -> None:
    """List every album in the wiki — the id, the layer, and whether the band has a style card."""
    from station.music import wiki

    music = Path.cwd() / "music"
    try:
        styles = wiki.load_styles(music / "production" / "styles.yaml")
        rows = wiki.album_rows(music / wiki.WIKI_DIR, styles)
    except wiki.WikiError as exc:
        typer.secho(f"\n{exc}\n", fg="red", err=True)
        raise typer.Exit(code=2) from None

    rows = [r for r in rows if genre is None or r.genre == genre]
    if not rows:
        typer.secho("no albums yet — no genre has been written (music/RUNBOOK.md)", fg="yellow")
        return

    typer.echo(
        f"{'ALBUM':<8} {'L':<2} {'BAND':<20} {'YEAR':<6} {'SONGS':<6} {'PLAY':<5} {'STYLE':<6} TITLE"
    )
    current = ""
    for row in rows:
        if row.genre != current:
            current = row.genre
            typer.secho(f"\n{current}", bold=True)
        style = "yes" if row.has_style else ("-" if row.layer == "B" else "--")
        mark = " *" if row.cornerstone else ""
        line = (
            f"{row.album_id:<8} {row.layer:<2} {row.band:<20} {row.year:<6} "
            f"{row.songs:<6} {row.playable:<5} {style:<6} {row.title}{mark}"
        )
        typer.secho(line, fg=None if row.layer == "A" else "bright_black")

    playable = [r for r in rows if r.layer == "A"]
    typer.echo(
        f"\n{len(playable)} playable albums (L=A), {len(rows) - len(playable)} referenced only (L=B)."
        "\n  L=B is written about but never recorded, and never becomes audio."
        "\n  * cornerstone, long enough to carry a whole 56-minute programme."
    )
    missing = sorted({r.band for r in playable if not r.has_style})
    if missing:
        typer.secho(
            f"\nno style card yet: {', '.join(missing)}"
            "\n  style cards come from M-16 and M-20 in music/MUSIC_TASKS.md, before any lyrics.",
            fg="yellow",
        )


@app.command("music-screen")
def music_screen(genre: str = _GENRE_FILTER) -> None:
    """Screen every invented name in the wiki against real notable people and organisations."""
    from station.music import screen, wiki

    wiki_dir = Path.cwd() / "music" / wiki.WIKI_DIR
    slugs = [genre] if genre else wiki.written_genres(wiki_dir)
    if not slugs:
        typer.secho("no genre has been written yet (music/RUNBOOK.md)", fg="yellow")
        return

    typer.echo(
        f"Wikidata: exact name match, at least {screen.SITELINK_FLOOR} sitelinks, people and "
        f"organisations only.\nSurname-only echoes and near-misses are not reported — those stay "
        f"yours (music/RUNBOOK.md step 3).\n"
    )
    total = 0
    for slug in slugs:
        typer.secho(f"{slug}  ", bold=True, nl=False)
        try:
            report = screen.screen_genre(
                wiki_dir, slug, on_batch=lambda: typer.secho("·", fg="bright_black", nl=False)
            )
        except (wiki.WikiError, screen.ScreenError) as exc:
            typer.secho(f"\n\n{exc}\n", fg="red", err=True)
            raise typer.Exit(code=2) from None
        total += _print_screen(report)

    if total:
        typer.echo(
            "\nRecord the verdict on each of these in music/CONSTANTS.md §3 — cleared and "
            "rejected both, or the same collision gets proposed again next genre."
        )


def _print_screen(report: Report) -> int:
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


def main() -> None:
    """Console-script entry point."""
    app()
