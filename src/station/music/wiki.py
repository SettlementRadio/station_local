"""Read `music/wiki/*.yaml` — the nine genre files — back into typed objects.

Why models rather than dicts: each genre is written in one long pass against `COMMISSION.md`, so
its shape is *nearly* uniform and never exactly so. Validating on the way in means a missing field
fails here, naming the file and the entry, rather than three steps later inside something that
quietly says "None" (§31: dataclasses across boundaries, never bare dicts).

Extra keys are ignored on purpose. A writer who adds a field is not an error; a writer who omits a
required one is. Most of the world in these files — bios, album stories, movements, the lost
figures' histories — is prose no code reads, and is deliberately not modelled here.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

# `music/wiki/<genre>.yaml` — one file per genre, written by an agent working one card of
# `music/MUSIC_TASKS.md`.
WIKI_DIR = "wiki"


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

    @property
    def label_number(self) -> int | None:
        """`label_3` and `3` are the same label; `plan.yaml` counts by number. None if unreadable."""
        digits = self.label.rsplit("_", 1)[-1]
        return int(digits) if digits.isdigit() else None


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
    # Members carry an id because the credits point at them by id, and because a player who turns
    # up in two genres has to be the same person and not two people sharing a number.
    id: str = ""
    name: str
    instruments: list[str] = Field(default_factory=list)


class Named(_Entry):
    """A label, a session player or a lost figure: an id and a name, and nothing this file reads."""

    id: str
    name: str


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


class _Layer(_Entry):
    bands: list[Band] = Field(default_factory=list)
    albums: list[Album] = Field(default_factory=list)


class _LayerC(_Entry):
    """Only the figures' identities. Their history is prose no code reads."""

    figures: list[Named] = Field(default_factory=list)


class GenreWiki(_Entry):
    """One `music/wiki/<genre>.yaml`.

    `section` is the writer's own header block and is ignored — declaring fields nothing uses only
    creates ways for a valid wiki to be rejected. Labels, session players and layer C are modelled
    for one reason only: they mint ids, and an id used twice is the failure this file exists to
    catch (`check.py`).
    """

    labels: list[Named] = Field(default_factory=list)
    session_players: list[Named] = Field(default_factory=list)
    layer_a: _Layer = Field(default_factory=_Layer)
    layer_b: _Layer = Field(default_factory=_Layer)
    layer_c: _LayerC = Field(default_factory=_LayerC)

    @property
    def bands(self) -> list[Band]:
        return self.layer_a.bands

    @property
    def albums(self) -> list[Album]:
        return self.layer_a.albums

    def every_album(self) -> list[tuple[Album, Band | None, str]]:
        """(album, its band, its layer) across A and B, so a listing can show both.

        Both placements are accepted in both layers — beside the bands with a `band:` pointing
        back, or nested inside the band — because a checker that misses an album placed the other
        way passes a genre it never read.
        """
        bands = {b.id: b for b in self.layer_a.bands + self.layer_b.bands}
        out: list[tuple[Album, Band | None, str]] = []
        for layer, group in (("A", self.layer_a), ("B", self.layer_b)):
            out += [(a, bands.get(a.band), layer) for a in group.albums]
            out += [(a, b, layer) for b in group.bands for a in b.albums]
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


class Entity(_Entry):
    """One id a genre file mints, with enough context to name it in a failure message.

    `shared` marks the entities that are the *same* thing in every genre they touch: a label, a
    session player, a musician who plays in two bands. Those ids repeat by design (§6 wants players
    across three labels), so only a repeat that disagrees about who it is counts as a collision.
    """

    id: str
    name: str
    kind: str
    where: str
    shared: bool = False


def _album_entities(albums: list[Album], layer: str) -> list[Entity]:
    out: list[Entity] = []
    for album in albums:
        out.append(Entity(id=album.id, name=album.title, kind="album", where=f"layer {layer}"))
        out += [
            Entity(id=s.id, name=s.title, kind="song", where=f"layer {layer}, {album.id}")
            for s in album.songs
        ]
    return out


def defined_ids(genre: GenreWiki) -> list[Entity]:
    """Every id one genre file defines — the input to the duplicate check."""
    out = [
        Entity(id=x.id, name=x.name, kind="label", where="labels", shared=True)
        for x in genre.labels
    ]
    out += [
        Entity(id=x.id, name=x.name, kind="session player", where="session_players", shared=True)
        for x in genre.session_players
    ]
    for layer, group in (("A", genre.layer_a), ("B", genre.layer_b)):
        out += _album_entities(group.albums, layer)
        for band in group.bands:
            out.append(Entity(id=band.id, name=band.name, kind="band", where=f"layer {layer}"))
            out += [
                Entity(id=m.id, name=m.name, kind="person", where=f"in {band.name}", shared=True)
                for m in band.members
                if m.id
            ]
            out += _album_entities(band.albums, layer)
    out += [
        Entity(id=x.id, name=x.name, kind="figure", where="layer C") for x in genre.layer_c.figures
    ]
    return out


# The three counted id series, and the width each is written to (`s_0001`, `al_001`, `b_001`).
COUNTERS = (("song", "s_", 4), ("album", "al_", 3), ("band", "b_", 3))


def next_free_ids(wiki_dir: Path) -> dict[str, str]:
    """The next id in each counted series — derived from what is written, never hand-kept.

    `CONSTANTS.md` used to carry these three numbers by hand, which is exactly how the second genre
    written comes to reuse the first one's ids (D-053 note on M-01). No id is ever renumbered
    (`COMMISSION.md` §10), so the counter can only ever be the high-water mark plus one.
    """
    highest = dict.fromkeys((kind for kind, _, _ in COUNTERS), 0)
    for slug in written_genres(wiki_dir):
        for entity in defined_ids(load_genre(wiki_dir / f"{slug}.yaml")):
            if entity.kind not in highest:
                continue
            digits = entity.id.rsplit("_", 1)[-1]
            if digits.isdigit():
                highest[entity.kind] = max(highest[entity.kind], int(digits))
    return {kind: f"{prefix}{highest[kind] + 1:0{width}d}" for kind, prefix, width in COUNTERS}


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
