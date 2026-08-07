"""The one entry point: every `make` target calls into here (§17).

Why the config import is deferred into `_boot`: importing `station.config` is what validates the
environment (§23), and it must fail as a message that names the missing line rather than as a
traceback. Nothing above that call may import config, or the failure escapes the handler.
"""

from __future__ import annotations

import shutil
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import typer

from station import __version__

if TYPE_CHECKING:
    from station.config import Settings

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
CONFIG_FREE = frozenset({"version", "music-brief", "music-style", "music-songs"})


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


def _emit(build: Callable[[], str], out: Path | None) -> None:
    """Render a brief to stdout or a file, turning BriefError into a message rather than a trace."""
    from station.music.brief import BriefError

    try:
        text = build()
    except BriefError as exc:
        typer.secho(f"\n{exc}\n", fg="red", err=True)
        raise typer.Exit(code=2) from None
    if out is None:
        typer.echo(text)
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    typer.secho(f"{out}  ({len(text.split())} words)", fg="green")


# typer needs its defaults as call results; B008 forbids that inline, so they are singletons.
_GENRE_ARG = typer.Argument(..., help="genre slug, e.g. relay-pop")
_KIND_OPT = typer.Option("write", "--kind", help="write | check")
_OUT_OPT = typer.Option(None, "--out", help="write here instead of stdout")


@app.command("music-brief")
def music_brief(genre: str = _GENRE_ARG, kind: str = _KIND_OPT, out: Path = _OUT_OPT) -> None:
    """Assemble the writer or checker brief for one genre (`music/RUNBOOK.md`)."""
    from station.music import brief

    if kind not in ("write", "check"):
        typer.secho(f"--kind must be write or check, not {kind!r}", fg="red", err=True)
        raise typer.Exit(code=2)
    _emit(lambda: brief.build(kind, genre, Path.cwd()), out)  # type: ignore[arg-type]


_ALBUM_ARG = typer.Argument(..., help="album id, e.g. al_001")


@app.command("music-style")
def music_style(genre: str = _GENRE_ARG, out: Path = _OUT_OPT) -> None:
    """Assemble the style-card brief for one genre's bands (`music/RUNBOOK.md` step 7)."""
    from station.music import brief

    _emit(lambda: brief.build_style(genre, Path.cwd()), out)


@app.command("music-songs")
def music_songs(album: str = _ALBUM_ARG, out: Path = _OUT_OPT) -> None:
    """Assemble the lyrics-and-prompts brief for one album (`music/RUNBOOK.md` step 8)."""
    from station.music import brief

    _emit(lambda: brief.build_songs(album, Path.cwd()), out)


def main() -> None:
    """Console-script entry point."""
    app()
