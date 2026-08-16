"""`COMMISSION.md` §12, read rather than copied.

The ten thresholds, the two word lists and the four exempt album ids live in the writer's brief, and
this module parses them out of it. **Nothing here is a rule; it is only the reading of them.** A
threshold in code and a threshold in the brief drift apart within a week and the brief is the copy
that gets read, so editing a number in §12 is what changes the command — the same reasoning as the
anchor years in `check.py`.

Split out of `writing.py` when M-50 took that module past §31's 400 lines. One file reads the brief,
one counts against it.

Every failure here names what stopped matching, because a table that has quietly changed shape would
otherwise leave the command finding no rules and reporting nothing wrong.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from station.music.check import CheckError

COMMISSION_FILE = "COMMISSION.md"
RULES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# §12's rule table: `| 1 | more than `40%` of an album's ... | album | `M-47` |`. The threshold is
# the first backticked value in the description; the last column is the card that owes the rule.
_RULE_ROW = re.compile(r"^\|\s*(\d+)\s*\|([^|]*)\|[^|]*\|\s*(?:`(M-\d+)`|—)\s*\|\s*$", re.MULTILINE)
_THRESHOLD = re.compile(r"`(\d+)(%?)`")
_MIN_ALBUM = re.compile(r"counted only on albums of `(\d+)` songs or more")

EXEMPT_HEADING = "Rules 9 and 10 · the four albums that are exempt"


@dataclass(frozen=True)
class Rules:
    """§12, parsed. `threshold` is a share for the percentage rules and a count for the rest."""

    threshold: dict[int, float]
    owed_to: dict[int, str]
    min_album_songs: int
    world_nouns: tuple[str, ...]
    studio_words: tuple[str, ...]
    exempt_albums: tuple[str, ...]

    def pattern(self, terms: tuple[str, ...]) -> re.Pattern[str]:
        """§12's word lists are matched as written, whole words, any case."""
        longest_first = sorted(terms, key=len, reverse=True)
        return re.compile(r"\b(" + "|".join(re.escape(t) for t in longest_first) + r")\b", re.I)


def _blockquote(text: str, heading: str) -> tuple[str, ...]:
    """The `·`-separated list under one `### ` heading in §12 — a word list, or four album ids."""
    body = text.split(f"\n### {heading}", 1)
    if len(body) == 1:
        raise CheckError(f"{COMMISSION_FILE} §12 has no `### {heading}` section")
    quoted = re.search(r"^((?:> [^\n]*\n)+)", body[1], re.MULTILINE)
    if not quoted:
        raise CheckError(f"{COMMISSION_FILE} §12's `{heading}` has no `> ` word list under it")
    joined = " ".join(line.lstrip("> ").strip() for line in quoted.group(1).splitlines())
    return tuple(term.strip() for term in joined.split("·") if term.strip())


def load_rules(commission: Path) -> Rules:
    """Read §12, or fail naming what stopped matching."""
    try:
        text = commission.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise CheckError(f"missing {commission} — section 12 holds the writing rules") from None
    thresholds: dict[int, float] = {}
    owed: dict[int, str] = {}
    for number, description, card in _RULE_ROW.findall(text):
        found = _THRESHOLD.search(description)
        if not found:
            raise CheckError(f"{COMMISSION_FILE} §12 rule {number} states no `number` to count to")
        value, percent = found.groups()
        thresholds[int(number)] = int(value) / 100 if percent else int(value)
        if card:
            owed[int(number)] = card
    if sorted(thresholds) != list(RULES):
        raise CheckError(
            f"{COMMISSION_FILE} §12 gives rules {sorted(thresholds)}, not {list(RULES)}. Each row "
            f"reads `| N | … `number` … | over | `M-NN` or — |` and that shape is what makes the "
            f"table readable from here."
        )
    floor = _MIN_ALBUM.search(text)
    if not floor:
        raise CheckError(
            f"{COMMISSION_FILE} §12 no longer says which albums are too short to count"
        )
    return Rules(
        threshold=thresholds,
        owed_to=owed,
        min_album_songs=int(floor.group(1)),
        world_nouns=_blockquote(text, "Rule 5 · the world's own nouns"),
        studio_words=_blockquote(text, "Rule 6 · what counts as a studio anecdote"),
        exempt_albums=_blockquote(text, EXEMPT_HEADING),
    )
