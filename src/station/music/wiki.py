"""Read `music/wiki/*.yaml` — the writer's output — back into typed objects.

Why models rather than dicts: the wiki is hand-produced by a writer working from a prose brief, so
its shape is *nearly* uniform and never exactly so. Validating on the way in means a missing field
fails here, naming the file and the entry, rather than three steps later inside a rendered prompt
that quietly says "None" (§31: dataclasses across boundaries, never bare dicts).

Extra keys are ignored on purpose. A writer who adds a field is not an error; a writer who omits a
required one is.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class WikiError(RuntimeError):
    """The wiki could not be read. The message names the file or id to fix."""


class _Entry(BaseModel):
    model_config = ConfigDict(extra="ignore")


class _Labelled(_Entry):
    """Anything carrying a label reference.

    Writers give the label as either a number (`3`) or a slug (`label_3`); both are natural readings
    of `COMMISSION.md` §4, and rejecting one would fail a wiki that is perfectly correct. They are
    normalised to text on the way in so downstream comparisons never depend on which was used.
    """

    label: str

    @field_validator("label", mode="before")
    @classmethod
    def _as_text(cls, value: object) -> str:
        return str(value)


class Song(_Entry):
    id: str
    title: str
    track_number: int
    playable: bool = False
    mood_tags: list[str] = Field(default_factory=list)
    fact: str | None = None


class Album(_Labelled):
    id: str
    title: str
    # Layer A lists albums beside the bands and points back with `band`; layer B nests them inside
    # the band that made them, so the reference is implied. Both are natural YAML and both occur.
    band: str = ""
    release_year: int
    kind: str = "album"
    genre: str
    cornerstone: bool = False
    notes: str = ""
    songs: list[Song] = Field(default_factory=list)

    @property
    def playable_songs(self) -> list[Song]:
        return [s for s in self.songs if s.playable]


class Member(_Entry):
    name: str
    instruments: list[str] = Field(default_factory=list)


class Band(_Labelled):
    id: str
    name: str
    kind: str
    genre: str
    active_from: int
    active_to: int | None = None
    home_settlement: str = ""
    # A band's standing in the Purist/Synthesist/Localist argument. Writers give this either as one
    # word or as a mapping recording a switch of sides — both are legitimate and §2 invites the
    # second, so it is accepted as written and flattened for display.
    movement: str | dict[str, object] = ""
    bio: str = ""
    members: list[Member] = Field(default_factory=list)
    albums: list[Album] = Field(default_factory=list)  # layer B nests them here

    @property
    def movement_line(self) -> str:
        if isinstance(self.movement, str):
            return self.movement or "unstated"
        return "; ".join(f"{k}: {v}" for k, v in self.movement.items())

    def line_up(self) -> str:
        """One line per member, for a style-card brief. Solo acts often have no member list."""
        if not self.members:
            return "  (solo — no member list given)"
        return "\n".join(
            f"  {m.name}: {', '.join(m.instruments) or 'unspecified'}" for m in self.members
        )


class _Layer(_Entry):
    bands: list[Band] = Field(default_factory=list)
    albums: list[Album] = Field(default_factory=list)


class GenreWiki(_Entry):
    """One `music/wiki/<genre>.yaml`.

    Layer C is not modelled: its figures have no albums by definition, so nothing here can read it.
    `section` is the writer's own header block and is likewise ignored — declaring fields nothing
    uses only creates ways for a valid wiki to be rejected.
    """

    layer_a: _Layer = Field(default_factory=_Layer)
    layer_b: _Layer = Field(default_factory=_Layer)

    @property
    def bands(self) -> list[Band]:
        return self.layer_a.bands

    @property
    def albums(self) -> list[Album]:
        return self.layer_a.albums

    def every_album(self) -> list[tuple[Album, Band | None, str]]:
        """(album, its band, its layer) across A and B, so a listing can show both."""
        bands = {b.id: b for b in self.layer_a.bands}
        out: list[tuple[Album, Band | None, str]] = [
            (a, bands.get(a.band), "A") for a in self.layer_a.albums
        ]
        out += [(a, b, "B") for b in self.layer_b.bands for a in b.albums]
        return out


def load_genre(path: Path) -> GenreWiki:
    """Read one genre file, or fail naming it."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise WikiError(f"missing {path} — write that genre first (music/RUNBOOK.md)") from None
    except yaml.YAMLError as exc:
        raise WikiError(f"{path} is not valid YAML: {exc}") from None
    try:
        return GenreWiki.model_validate(raw)
    except Exception as exc:  # pydantic ValidationError, reported with the file that caused it
        raise WikiError(f"{path} does not match the expected shape:\n{exc}") from None


def written_genres(wiki_dir: Path) -> list[str]:
    """Genre slugs that have a wiki file, in a stable order."""
    if not wiki_dir.is_dir():
        return []
    return sorted(p.stem for p in wiki_dir.glob("*.yaml"))


def find_album(wiki_dir: Path, album_id: str) -> tuple[Album, Band, str]:
    """Locate an album across every written genre. Returns the album, its band, and the genre."""
    seen: list[str] = []
    for slug in written_genres(wiki_dir):
        genre = load_genre(wiki_dir / f"{slug}.yaml")
        for album, band, layer in genre.every_album():
            if album.id != album_id:
                if layer == "A":
                    seen.append(album.id)
                continue
            if layer == "B":
                raise WikiError(
                    f"{album_id} is a layer-B album — the station references it but does not hold "
                    f"it, so it has no lyrics and never becomes audio. Pick a layer-A album: "
                    f"run `make music-albums`."
                )
            if band is None:
                raise WikiError(f"album {album_id} names band {album.band}, which is not in {slug}")
            return album, band, slug
    known = ", ".join(seen[:12]) or "none — no genre has been written yet"
    raise WikiError(f"no album {album_id!r}. Playable albums: {known}")


class AlbumRow(_Entry):
    """One line of `make music-albums` — enough to choose an album without opening a file."""

    album_id: str
    title: str
    band: str
    band_id: str
    genre: str
    layer: str
    year: int
    songs: int
    playable: int
    cornerstone: bool
    has_style: bool


def album_rows(wiki_dir: Path, styles: dict[str, str]) -> list[AlbumRow]:
    """Every album in the wiki — layer A and layer B both, so the listing shows what is playable."""
    rows: list[AlbumRow] = []
    for slug in written_genres(wiki_dir):
        genre = load_genre(wiki_dir / f"{slug}.yaml")
        found = genre.every_album()
        for album, band, layer in sorted(found, key=lambda t: (t[2], t[0].id)):
            band_id = album.band or (band.id if band else "")
            rows.append(
                AlbumRow(
                    album_id=album.id,
                    title=album.title,
                    band=band.name if band else "?",
                    band_id=band_id,
                    genre=slug,
                    layer=layer,
                    year=album.release_year,
                    songs=len(album.songs),
                    playable=len(album.playable_songs),
                    cornerstone=album.cornerstone,
                    has_style=bool(band_id) and band_id in styles,
                )
            )
    return rows


def load_styles(path: Path) -> dict[str, str]:
    """Band id → style card, from `music/production/styles.yaml`. Absent is not an error yet."""
    if not path.is_file():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise WikiError(f"{path} should be a mapping of band id to style card")
    return {str(k): _render_card(v) for k, v in raw.items()}


def _render_card(card: object) -> str:
    """Style cards are written as a small mapping; render them back as the six labelled lines."""
    if isinstance(card, str):
        return card.strip()
    if isinstance(card, dict):
        return "\n".join(f"  {k}: {v}" for k, v in card.items())
    return str(card)
