"""Every invented name in a genre, put to Wikidata — so nobody googles four hundred of them.

What this decides and what it does not. `DECISIONS.md` D-009 fixed the rule: an **exact** match on
the full name, against an entity with **≥5 sitelinks** ("has a real article in several languages"),
is the thing worth acting on. Below that floor nearly every plausible human name matches something,
and a screen that fires constantly is switched off within a week. Surname-only echoes, and a name
that reads as a famous one with a letter changed, are judgements this file will never make —
`music/RUNBOOK.md` step 3 is where they get made, by the operator, on the short list this produces.

Why the live query service rather than the ~1.5M-name extract D-014 specifies for the world tick:
that screen runs inside the nightly batch on every proposed figure and cannot depend on somebody
else's uptime. This one is an operator command run nine times in the life of the catalogue, on a
few hundred names, and a 1.5M-row download plus a bloom filter is a lot of machinery to maintain
for nine runs (D-056).

Nothing here is a gate. It exits 0 whatever it finds; the verdicts go in `music/CONSTANTS.md` §3.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from station.music import wiki

ENDPOINT = "https://query.wikidata.org/sparql"
# WMF blocks anonymous clients; the policy asks for a UA that says who is calling and where to
# complain. Do not send this without one.
USER_AGENT = (
    "SettlementRadio/0.1 (https://github.com/SettlementRadio/station_local; music name screen)"
)

SITELINK_FLOOR = 5  # D-009. Not a knob: below it the screen reports everything and means nothing.
BATCH = 50  # names per request — 350 names is seven requests, each about a second.
TIMEOUT_S = 30  # §25: every external call has an explicit timeout.
BACKOFF_S = (2, 8, 30)  # §25's ladder; the last entry is never slept, it only sizes the attempts.
# Below this the endpoint is telling us the query is wrong, and it will be just as wrong in 30
# seconds. At or above it — 429 too many requests, 500s — the call is worth making again.
RETRYABLE_FROM = 429


class ScreenError(RuntimeError):
    """The screen could not run. §25: never silently produce nothing — an empty report would read
    as "every name is clear", which is the one wrong answer this tool can give."""


class Name(BaseModel):
    """One invented name, and where in the genre it is used."""

    name: str
    kind: str  # band · label · person · album · song
    where: str


class Match(BaseModel):
    """A real notable entity sharing that name exactly."""

    qid: str
    sitelinks: int
    kinds: str = ""
    description: str = ""

    @property
    def url(self) -> str:
        return f"https://www.wikidata.org/wiki/{self.qid}"


class Finding(BaseModel):
    """One name that matched, with every use of it in the genre and every entity it hit."""

    name: str
    uses: list[Name]
    matches: list[Match]


class Report(BaseModel):
    """What `make music-screen` prints for one genre."""

    genre: str
    screened: int  # distinct names put to Wikidata
    uses: int  # places those names are used — always the larger number
    findings: list[Finding] = Field(default_factory=list)


def names_in(genre: wiki.GenreWiki) -> list[Name]:
    """Every name the genre invented: bands, labels, people, album titles, song titles.

    Layer B is screened as hard as layer A. A presenter says a layer-B title on air exactly as
    readily as a layer-A one — it is never recorded, which has nothing to do with whether it
    collides with a real band.
    """
    out = [Name(name=x.name, kind="label", where="labels") for x in genre.labels]
    out += [Name(name=x.name, kind="person", where="session player") for x in genre.session_players]
    out += [
        Name(name=x.name, kind="person", where="lost figure, layer C")
        for x in genre.layer_c.figures
    ]
    for layer, group in (("A", genre.layer_a), ("B", genre.layer_b)):
        for band in group.bands:
            out.append(Name(name=band.name, kind="band", where=f"{band.id}, layer {layer}"))
            out += [
                Name(name=m.name, kind="person", where=f"{band.name} line-up") for m in band.members
            ]
    for album, maker, layer in genre.every_album():
        who = maker.name if maker else "?"
        out.append(Name(name=album.title, kind="album", where=f"{album.id}, {who}, layer {layer}"))
        out += [
            Name(name=s.title, kind="song", where=f"{album.id} track {s.track_number}")
            for s in album.songs
        ]
    return [n for n in out if n.name.strip()]


# --- the query ---------------------------------------------------------------------------------
#
# `wdt:P279*` up to human or organisation is what makes this a screen for *people and companies*
# rather than for every string in Wikidata. The geographic exclusion is not optional: administrative
# entities reach `organization` through the subclass tree, so without it every one-word title
# matches a village somewhere and the report is unreadable.

_QUERY = """\
SELECT ?name ?item ?sitelinks ?desc (GROUP_CONCAT(DISTINCT ?kindLabel; separator=", ") AS ?kinds)
WHERE {{
  VALUES ?name {{ {values} }}
  ?item rdfs:label|skos:altLabel ?name .
  ?item wikibase:sitelinks ?sitelinks .
  FILTER(?sitelinks >= {floor})
  ?item wdt:P31 ?kind .
  ?kind wdt:P279* ?super .
  VALUES ?super {{ wd:Q5 wd:Q43229 }}
  FILTER NOT EXISTS {{
    ?item wdt:P31/wdt:P279* ?place .
    VALUES ?place {{ wd:Q56061 wd:Q27096213 }}
  }}
  ?kind rdfs:label ?kindLabel . FILTER(lang(?kindLabel) = "en")
  OPTIONAL {{ ?item schema:description ?desc . FILTER(lang(?desc) = "en") }}
}}
GROUP BY ?name ?item ?sitelinks ?desc
"""


def _escape(name: str) -> str:
    return name.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def build_query(names: Sequence[str], floor: int = SITELINK_FLOOR) -> str:
    """The SPARQL for one batch. Exact match, English label or alias, above the floor."""
    return _QUERY.format(
        values=" ".join(f'"{_escape(n)}"@en' for n in names),
        floor=floor,
    )


Fetch = Callable[[str], dict[str, Any]]
"""A SPARQL query in, the endpoint's JSON out. Injected so the tests never touch the network."""


def _post(query: str) -> dict[str, Any]:
    """One request, with the timeout and the bounded retry of §25."""
    body = urllib.parse.urlencode({"query": query, "format": "json"}).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
    )
    last = ""
    for attempt, pause in enumerate(BACKOFF_S, start=1):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
                payload: dict[str, Any] = json.loads(response.read().decode("utf-8"))
                return payload
        except urllib.error.HTTPError as exc:
            if exc.code < RETRYABLE_FROM:
                raise ScreenError(
                    f"Wikidata rejected the query ({exc.code} {exc.reason})"
                ) from None
            last = f"{exc.code} {exc.reason}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = str(exc)
        if attempt < len(BACKOFF_S):
            time.sleep(pause)
    raise ScreenError(
        f"Wikidata did not answer after {len(BACKOFF_S)} attempts ({last}). Nothing was screened — "
        f"an empty report would read as 'every name is clear'. Check the connection and run again."
    )


def _matches(payload: dict[str, Any]) -> dict[str, list[Match]]:
    """The endpoint's bindings, by the name that produced them."""
    found: dict[str, list[Match]] = {}
    for row in payload.get("results", {}).get("bindings", []):
        name = row["name"]["value"]
        found.setdefault(name, []).append(
            Match(
                qid=row["item"]["value"].rsplit("/", 1)[-1],
                sitelinks=int(row["sitelinks"]["value"]),
                kinds=row.get("kinds", {}).get("value", ""),
                description=row.get("desc", {}).get("value", ""),
            )
        )
    return found


def screen(
    names: Sequence[Name],
    fetch: Fetch = _post,
    floor: int = SITELINK_FLOOR,
    on_batch: Callable[[], None] | None = None,
) -> list[Finding]:
    """Put every distinct name to Wikidata in batches, and return only the ones that hit.

    Distinct, because a session player who plays on four albums is one name to screen, and the
    report the operator reads should say so once. `on_batch` fires after each round trip: a genre
    is seven of them and the better part of a minute, and silence for a minute reads as a hang.
    """
    uses: dict[str, list[Name]] = {}
    for entry in names:
        uses.setdefault(entry.name, []).append(entry)

    distinct = list(uses)
    hits: dict[str, list[Match]] = {}
    for start in range(0, len(distinct), BATCH):
        hits |= _matches(fetch(build_query(distinct[start : start + BATCH], floor)))
        if on_batch:
            on_batch()

    return [
        Finding(
            name=name,
            uses=uses[name],
            matches=sorted(hits[name], key=lambda m: -m.sitelinks),
        )
        for name in distinct
        if name in hits
    ]


def screen_genre(
    wiki_dir: Path, slug: str, fetch: Fetch = _post, on_batch: Callable[[], None] | None = None
) -> Report:
    """One genre file, read and screened."""
    names = names_in(wiki.load_genre(wiki_dir / f"{slug}.yaml"))
    return Report(
        genre=slug,
        screened=len({n.name for n in names}),
        uses=len(names),
        findings=screen(names, fetch, on_batch=on_batch),
    )


def requests_for(name_count: int) -> int:
    """How many round trips a genre of this size costs — printed before the wait starts."""
    return -(-name_count // BATCH)
