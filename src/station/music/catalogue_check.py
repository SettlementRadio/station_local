"""`music/catalogue.yaml` read back and checked against the wiki it was built from.

`catalogue.py` writes the file; this reads it. They are separate passes for the same reason
`writing.py` is separate from `check.py` (M-45): the builder can only be wrong in ways it already
believes, and the file is *committed*, so the failure worth catching is not a bad build — it is a
good build going stale. Somebody edits a genre file, `make music-catalogue` is not re-run, and the
station's one source of truth quietly describes last week's wiki while looking authoritative.

**Nothing here touches the audio, and that is deliberate.** `music/audio/` is gitignored, so CI has
none of it (§30). Every check below is identity and arithmetic against files that are in git: the
ids and titles agree with the wiki, every reference resolves, the present year still holds, and a
row either carries a whole take or carries none of one. Whether a measured ramp is *right* is a
question for the ear (`make music-analyse`, ARCHITECTURE §9), never for `make check`.

The one check that is not about the catalogue at all is `stray_keys`: a song written as a flow
mapping with an unquoted comma loses its title at the comma and stays valid YAML. Twenty-five layer-B
titles were truncated that way before this existed, and a truncated title is a record a presenter
names wrongly on air, so it is caught here rather than trusted to review.
"""

from __future__ import annotations

from pathlib import Path

from station.music import catalogue, wiki

# How many ids a failure names before it stops. Enough to recognise the pattern, few enough to read.
SHOWN = 5

REBUILD = "run `make music-catalogue`"


def validate(root: Path) -> list[str]:
    """Every disagreement between `music/catalogue.yaml` and the wiki. Empty means they match."""
    music = root / "music"
    found = catalogue.genres(music / wiki.WIKI_DIR)
    problems = _stray_keys(found)
    catalogue_path = music / catalogue.CATALOGUE_FILE
    if not catalogue_path.is_file():
        return [*problems, f"{catalogue_path} does not exist — {REBUILD}"]
    built = catalogue.load(catalogue_path)
    return problems + _same_world(built, found) + _resolves(built) + _rows_are_whole(built)


def _first(ids: list[str]) -> str:
    shown = ", ".join(ids[:SHOWN])
    return f"{shown}, …" if len(ids) > SHOWN else shown


def _stray_keys(found: dict[str, wiki.GenreWiki]) -> list[str]:
    """A key nothing defines on a song entry — see the module docstring, and `wiki.Song`."""
    out: list[str] = []
    for slug, genre in sorted(found.items()):
        for album, _, _ in genre.every_album():
            for song in album.songs:
                if song.stray_keys:
                    out.append(
                        f'{slug}: {album.id} {song.id} "{song.title}" also carries '
                        f"{', '.join(song.stray_keys)} — that is an unquoted comma inside a flow "
                        f"mapping, and the title is cut off at it. Quote the title"
                    )
    return out


def _wiki_names(found: dict[str, wiki.GenreWiki]) -> dict[str, dict[str, str]]:
    """id → name, for each of the four things the catalogue lists, exactly as the wiki has them."""
    names: dict[str, dict[str, str]] = {k: {} for k in ("label", "artist", "album", "track")}
    for genre in found.values():
        names["label"].update({x.id: x.name for x in genre.labels})
        for band in genre.layer_a.bands + genre.layer_b.bands:
            names["artist"][band.id] = band.name
        for album, _, _ in genre.every_album():
            names["album"][album.id] = album.title
            names["track"].update({song.id: song.title for song in album.songs})
    return names


def _same_world(built: catalogue.Catalogue, found: dict[str, wiki.GenreWiki]) -> list[str]:
    """The catalogue lists what the wiki lists, under the same names. This is the staleness check."""
    present = catalogue.present_year(found)
    problems = []
    if built.present_year != present:
        problems.append(
            f"catalogue.yaml was built when the present was {built.present_year} and the wiki now "
            f"says {present} — `category` is an age against that year, so {REBUILD}"
        )
    listed = {
        "label": {x.id: x.name for x in built.labels},
        "artist": {x.id: x.name for x in built.artists},
        "album": {x.id: x.title for x in built.albums},
        "track": {x.id: x.title for x in built.tracks},
    }
    for what, expected in _wiki_names(found).items():
        problems += _compare(what, expected, listed[what])
    return problems


def _compare(what: str, expected: dict[str, str], listed: dict[str, str]) -> list[str]:
    missing = sorted(set(expected) - set(listed))
    extra = sorted(set(listed) - set(expected))
    renamed = sorted(i for i in set(expected) & set(listed) if expected[i] != listed[i])
    out = []
    if missing:
        out.append(
            f"{len(missing)} {what}(s) in the wiki are missing from catalogue.yaml "
            f"({_first(missing)}) — {REBUILD}"
        )
    if extra:
        out.append(
            f"{len(extra)} {what}(s) in catalogue.yaml are not in the wiki ({_first(extra)}) — "
            f"an id is never renumbered (COMMISSION.md §10), so this is a stale file: {REBUILD}"
        )
    if renamed:
        out.append(
            f"{len(renamed)} {what}(s) are named differently in catalogue.yaml "
            f"({_first(renamed)}) — {REBUILD}"
        )
    return out


def _resolves(built: catalogue.Catalogue) -> list[str]:
    """Every reference points at a row in the same file, and every enumerated value is one of §8's."""
    labels = {x.id for x in built.labels}
    artists = {x.id for x in built.artists}
    albums = {x.id for x in built.albums}
    out: list[str] = []
    bad_kind = sorted(
        x.id for x in built.artists if x.kind not in set(catalogue.ARTIST_KINDS.values())
    )
    if bad_kind:
        out.append(
            f"{len(bad_kind)} artist(s) are not solo, group or collective: {_first(bad_kind)}"
        )
    out += _dangling("artist", "label", [(x.id, x.label) for x in built.artists], labels)
    out += _dangling("album", "artist", [(x.id, x.artist) for x in built.albums], artists)
    out += _dangling("album", "label", [(x.id, x.label) for x in built.albums], labels)
    out += _dangling("track", "album", [(x.id, x.album) for x in built.tracks], albums)
    out += _dangling("track", "artist", [(x.id, x.artist) for x in built.tracks], artists)
    kinds = sorted(x.id for x in built.albums if x.kind not in catalogue.ALBUM_KINDS)
    if kinds:
        listed = ", ".join(sorted(catalogue.ALBUM_KINDS))
        out.append(f"{len(kinds)} album(s) have a kind outside {listed}: {_first(kinds)}")
    return out


def _dangling(
    what: str, field: str, pairs: list[tuple[str, str | None]], known: set[str]
) -> list[str]:
    """A null reference is legitimate — an unsigned band has no house. A wrong one never is."""
    broken = sorted(id_ for id_, target in pairs if target is not None and target not in known)
    if not broken:
        return []
    return [
        f"{len(broken)} {what}(s) point at a {field} that is not in the file: {_first(broken)} — "
        f"{REBUILD}"
    ]


def _rows_are_whole(built: catalogue.Catalogue) -> list[str]:
    """§8: a playable track has a file and everything measured off it; an unplayable one has none.

    This is the invariant a scheduler would otherwise have to remember. A row that says `playable`
    and carries no ramp is dead air or a clipped vocal, and a row that says nothing is playable
    while carrying a file is a track rotation will never reach for no reason anybody can see.
    """
    measured = ("file", "duration_sec", "intro_ramp_sec", "outro_type", "licence_note", "category")
    half, wrong_language, wrong_category = [], [], []
    for track in built.tracks:
        filled = sum(1 for field in measured if getattr(track, field) is not None)
        if filled != (len(measured) if track.playable else 0):
            half.append(track.id)
        if track.language != catalogue.LANGUAGE:
            wrong_language.append(track.id)
        if track.category is not None and track.category not in (catalogue.HEAVY, catalogue.GOLD):
            wrong_category.append(track.id)
    out = []
    if half:
        out.append(
            f"{len(half)} track(s) carry part of a take rather than all of it or none of it "
            f"({_first(half)}) — §8 wants file, duration, ramp, outro, licence and category "
            f"together on a playable row and null on every other one. {REBUILD}"
        )
    if wrong_language:
        out.append(
            f"{len(wrong_language)} track(s) are not `{catalogue.LANGUAGE}`: {_first(wrong_language)}"
        )
    if wrong_category:
        out.append(
            f"{len(wrong_category)} track(s) carry a category this pass never writes "
            f"({_first(wrong_category)}) — only `{catalogue.HEAVY}` and `{catalogue.GOLD}` are "
            f"derived, and the rest are the operator's to set (D-085)"
        )
    return out
