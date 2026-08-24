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
    from station.music.tag import Result

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
CONFIG_FREE = frozenset(
    {
        "version",
        "music-albums",
        "music-screen",
        "music-analyse",
        "music-tag",
        "music-catalogue",
        "imaging-analyse",
    }
)


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
    from station.music import console, screen, wiki

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
        total += console.screen_report(report)

    if total:
        typer.echo(
            "\nRecord the verdict on each of these in music/CONSTANTS.md §3 — cleared and "
            "rejected both, or the same collision gets proposed again next genre."
        )


@app.command("music-analyse")
def music_analyse(album: str = typer.Option(None, "--album", help="only this album id")) -> None:
    """Measure every take: duration, the run-up before the first sung word, and how it ends."""
    from station.music import analyse, console

    root = Path.cwd() / "music" / "audio"
    if not root.is_dir():
        typer.secho(
            f"no audio yet — {root} does not exist (M-18 in music/MUSIC_TASKS.md)", fg="yellow"
        )
        return
    paths = [p for p in analyse.audio_files(root) if album is None or p.parent.name == album]
    if not paths:
        typer.secho(
            f"no audio files under {root}" + (f" for {album}" if album else ""), fg="yellow"
        )
        return

    typer.echo(f"{len(paths)} file(s) under music/audio — about a second each\n")
    typer.echo(f"{'TRACK':<10}{'DURATION':>9}{'RAMP':>7}  {'OUTRO':<9}")
    measured, failed = [], []
    current = ""
    for path in paths:
        one, problems = analyse.measure_all([path])
        measured += one
        failed += problems
        if not one:
            continue
        if str(path.parent) != current:
            current = str(path.parent)
            typer.secho(f"\n{path.parent.relative_to(root)}", bold=True)
        console.measurement(one[0], path.stem)
    console.analyse_summary(measured, failed)


@app.command("music-tag")
def music_tag(album: str = typer.Option(None, "--album", help="only this album id")) -> None:
    """Write the licence period, generation date, model version and AI marker into every take."""
    from station.music import console
    from station.music import tag as tagger

    music = Path.cwd() / "music"
    try:
        songs = tagger.load_songs(music, album=album)
    except tagger.TagError as exc:
        typer.secho(f"\n{exc}\n", err=True, fg="red")
        raise typer.Exit(code=1) from None
    if not songs:
        typer.secho("no takes recorded yet" + (f" for {album}" if album else ""), fg="yellow")
        return

    typer.echo(f"{len(songs)} take(s) recorded in music/production/lyrics\n")
    typer.echo(f"{'TRACK':<7}{'LICENCE':<20}{'MODEL':<8}{'DATE':<12}{'':<10}")
    results: list[Result] = []
    current = ""
    for song in songs:
        if song.album_id != current:
            current = song.album_id
            typer.secho(f"\n{song.album_id}", bold=True)
        results.append(tagger.tag(song))
        console.tag_row(song, results[-1])
    # "nothing under music/audio is left untagged" is a claim about the whole tree, so the sweep
    # for files no lyrics file claims only runs on a full pass. Narrowed to one album, every other
    # album's audio would read as unclaimed and the command would go red for no reason.
    left_out: list[Path] = (
        tagger.unclaimed(music / tagger.AUDIO_DIR, songs) if album is None else []
    )
    console.tag_summary(tagger.summarise(results, left_out), results, whole=album is None)


@app.command("music-catalogue")
def music_catalogue() -> None:
    """Build `music/catalogue.yaml` — the wiki, the lyrics and the audio as one file (§17a)."""
    from station.music import catalogue, catalogue_check, console

    root = Path.cwd()
    path = root / "music" / catalogue.CATALOGUE_FILE
    typer.echo("measuring every take that exists — about a second each\n")
    try:
        built = catalogue.build(root, on_measured=console.measuring)
        catalogue.write(path, built.catalogue)
        problems = built.problems + catalogue_check.validate(root)
    except catalogue.CatalogueError as exc:
        typer.secho(f"\n{exc}\n", err=True, fg="red")
        raise typer.Exit(code=2) from None
    if not console.catalogue_summary(built, problems, path):
        raise typer.Exit(code=1)


# The pile has not moved yet. §9 puts imaging audio on the external volume under `imaging/`, but
# what exists today is the 56 files carried over from the previous attempt, and moving them is
# I-06's job, not this command's. So it reads whichever of the two holds audio, and says which.
IMAGING_DIRS = (Path("imaging"), Path("music") / "jingles" / "approved")


@app.command("imaging-analyse")
def imaging_analyse(
    piece: str = typer.Option(None, "--piece", help="only pieces whose name contains this"),
) -> None:
    """Measure every piece of imaging: length, run-up, energy, and a bed's loop seam."""
    from station.imaging import analyse, console

    roots = [Path.cwd() / d for d in IMAGING_DIRS]
    found = [(root, analyse.audio_files(root)) for root in roots if root.is_dir()]
    root, paths = next(((r, p) for r, p in found if p), (roots[0], []))
    if not paths:
        typer.secho(
            "no imaging audio — looked in " + " and ".join(str(d) for d in IMAGING_DIRS),
            fg="yellow",
        )
        return
    paths = [p for p in paths if piece is None or piece in p.stem]
    if not paths:
        typer.secho(f"no piece under {root} matches {piece!r}", fg="yellow")
        return

    typer.echo(
        f"{len(paths)} piece(s) under {root.relative_to(Path.cwd())} — about a second each, "
        "and ten for a long bed\n"
    )
    typer.echo(console.HEADER)
    measured, failed = [], []
    for path in paths:
        one, problems = analyse.measure_all([path])
        measured += one
        failed += problems
        if one:
            console.measurement(one[0])
    console.analyse_summary(measured, failed)


def main() -> None:
    """Console-script entry point."""
    app()
