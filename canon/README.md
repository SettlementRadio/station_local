# canon/ — the world bible

> **Markdown in git is the source of truth; the database is derived and disposable. That direction
> never reverses** (ARCHITECTURE §7). You write prose and facts here; `canon-check` validates them
> and `canon-sync` projects them into Postgres. Nothing is ever hand-edited in the database.

This README is the **authoring contract** — the file shape, how a fact is identified, and what does
and does not belong here. Two companions:

- [`SPIRIT.md`](SPIRIT.md) — the creative brief: the idea, the SF tradition, the register, and the
  IP firewall. **Read it first.** It is what makes the writing good; this file only makes it load.
- [`COMMISSION.md`](COMMISSION.md) — the self-contained brief handed to a commissioned writer: what
  is missing, the header block, the format, the forbidden-fact list and the IP rule, assuming no
  access to this repo (`DECISIONS.md` D-027).

None of the three carries frontmatter, so none is world content (§1 below). **These three are the
only authoring guides**, and there is no fourth: *checking* canon is `canon-check`'s job (§6), never
a runbook's (D-026).

---

## 1. The file shape

Every canon file is Markdown with a **YAML frontmatter block**:

```yaml
---
id: economy          # unique across canon/; the file's stable name
domain: finance      # one of the seventeen — see §2
scope: universe      # universe | station
status: active       # active | retired
supersedes: []       # ids this file replaces
---
```

**Frontmatter is what marks a file as world content.** A file without it — `README.md` and
`SPIRIT.md` — is an authoring guide, is skipped by `canon-check` and `canon-sync`, and never
reaches the DJs. That is what lets `SPIRIT.md` name real authors freely.

The numeric filename prefix (`35-economy.md`) is **reading order for humans only**. Nothing keys off
it: `id` and `domain` carry the meaning. Leave gaps so a new file slots in without renumbering.
**Several files may share a domain** — `50-daily-life.md`, `55-language.md` and `58-knowledge.md`
are all `culture`. One domain per *file*, not one file per *domain*.

## 2. The seventeen domains — a closed list

`domain:` must be one of:

> `politics` · `finance` · `sport` · `conflict` · `crime` · `technology` · `health` · `art` ·
> `culture` · `history` · `religion` · `celebrity` · `fashion` · `music` · `logistics` ·
> `geography` · `peoples`

**Nothing may invent an eighteenth** (`PROGRAMMING.md` §3). Four separate mechanisms key off this
list: `facts.domain`, the `domain_floor`, the 12-facts-per-domain diversity cap in retrieval, and
the Tier 1 always-shipped domain summaries. A new domain is not an authoring decision.

What each domain covers in-world, and the trap in each, is `PROGRAMMING.md` §3. If a new file
doesn't obviously fit one, that is the signal to fold it into the nearest domain — not to add one.

## 3. What a fact is, and how it keeps its name

A **fact** is one atomic assertion, typically 1–3 sentences — not a paragraph, not a file. Too
coarse and retrieval returns junk bundled with the good; too fine and the assertion loses the
context that makes it mean anything.

Identity and version are **two separate things**:

| | What it is | When it changes |
|---|---|---|
| `fact_key` | the fact's **name** | **never** — assigned once, on first sight |
| `text_hash` | the fact's **version** | on every edit; drives re-embedding |

`fact_key` comes from an explicit anchor you write, or is slugified from the fact's subject if you
don't. **Write the anchor on anything the world will refer back to** — a faction, a ship, a named
observance, a figure:

```markdown
### The Ashfall Minute {#the-ashfall-minute}
```

**Why this matters more than it looks.** If identity were the hash of the text, fixing a typo would
create a "new" fact, retire the old one, and orphan every `coverage` and `quotes` row pointing at
it — silently breaking continuity for material that has **already aired**. With the split, an edit
is a version change and history survives. Where a fact is genuinely *replaced* rather than edited,
`supersedes` records it.

**So: editing a fact is always safe. Renaming a file or an anchor is not.**

## 4. Prose and facts do different jobs

The two halves of a file go to two different places, and it matters that you know which is which:

| What you write | Where it goes | Reaches a script? |
|---|---|---|
| `## `/`### ` **prose** | **Tier 1** — a generated 150–200 word domain summary, regenerated when the domain changes, **shipped on every call** | only through the summary |
| the `## Canon facts` list | **Tier 2** — retrieved by hybrid search (BM25 for names + embeddings for meaning), reranked, capped at 12 per domain | **yes, individually** |

**The fact list is the only way a specific detail ever gets said on air.** Pass 1 parses that
numbered list; it does not atomise your prose — it is one of the deterministic passes that runs
without a model (§7 §"Where it runs"), which a model-free pass could not do to free-flowing text.
So a lovely detail buried in a paragraph will shape the *summary* and never be quoted. **If it
should reach the microphone, make it a fact.**

This is why restating a prose point in the fact list is correct rather than redundant: the prose
explains, the list declares what is searchable.

Two consequences for how you write. **Proper nouns earn their keep** — BM25 is what makes "Cold
Harbor" or a figure's name findable, so name things and name them consistently. And **the domain
summary is generated from your prose**, so a domain written vaguely produces a vague summary that
ships on *every prompt in the station*.

There are no tags. Narrowing by topic is `domain` plus retrieval; a tag list in the source would
land in the embedding as noise.

## 5. What does **not** go in canon

Canon is the **static substrate** — it changes only when you change it. The moving present is
database state you never hand-edit (ARCHITECTURE §6):

| Not canon | What it actually is |
|---|---|
| Dated events, "the vote is on Thursday" | **beats**, written by the nightly tick |
| Ongoing storylines | **threads** |
| One-liner texture, a late ferry, a rota swap | **items**, 36-hour read window |
| **The station's own identity, the premise, the clock** | **`core/`** — Tier 0, loaded whole and verbatim on every call |
| DJ cards, speech profiles | **`cast/`** — item C2, Tier 0, never retrieved |
| Chart positions, airplay | derived from `music/` and playout |

**The `core/` line is the one that catches people out.** "Humanity lives across many settlements"
and "settlement time is the shared clock" are not facts to be *found* — the station needs them in
front of it every time it speaks, so they live in `core/` and ship on every call. Canon is what gets
**searched**; `core/` is what is always **there**. If a statement would be embarrassing for the
station not to know, it belongs in `core/`, and `core/` is deliberately tiny (D-030).

The line: a **recurring observance** is canon (the Lumen Festival, what it means, what people do); a
**dated instance** of it is a beat. Write the institution, never the date — and never a fixed year,
since the in-world year is always `real year + 600`, computed at generation time.

**Named entities split two ways** (this is what §7 pass 4 validates): **settlements are database
rows** because five tables join to them. **Factions and named ships are canon facts** with
`fact_key`s of the form `faction:*` and `ship:*`, because they carry no per-day state. Anything that
needs a foreign key is a row; anything that is only ever named is a fact.

## 6. Validation — what will be checked

`canon-check` runs seven passes and costs nothing (local model). Four are deterministic and run on
pre-commit; three need a loaded writer and run on pre-push.

| Pass | Checks | Authoring consequence |
|---|---|---|
| 1 | parse & atomise | one assertion per fact |
| 2 | **contradiction** — the 8 most similar existing facts, then asked whether they clash | keep new facts consistent; the check names both `fact_key`s |
| 3 | **domain summaries pinned** | a changed summary **blocks the push** until reviewed — highest blast radius in the system |
| 4 | **link integrity** — every settlement, figure, faction, ship, year resolves | declare a new entity in the same commit or the reference fails |
| 5 | **IP screen** — `config/banned-entities.yaml` plus a model pass | see [`SPIRIT.md`](SPIRIT.md) §0. Flags for adjudication, never auto-rejects |
| 6 | **register** — epigram density, banned abstractions, hedge rate | canon is what the world tick imitates; see `SPIRIT.md` §5a |
| 7 | **timeline sanity** | no fact after in-world now; no birth after death |

Output is `canon-report.md`, a derived artifact. `error` blocks, `warn` prints. Resolution per
conflict: **keep both**, **supersede**, or **edit**.

> **Neither command is built yet** — `canon-check` and `canon-sync` are build steps 3 and 4
> (ARCHITECTURE §35). Canon is authored *before* them on purpose: it gates phase C, and it is the
> largest thing only the operator can do. Write to this contract now and it will load when they
> land.

## 7. Where the current files sit

| File | Domain | | File | Domain |
|---|---|---|---|---|
| `05-worlds.md` | `geography` | | `50-daily-life.md` | `culture` |
| `06-gazetteer.md` | `geography` | | `51-observances.md` | `culture` |
| `10-history.md` | `history` | | `52-sports.md` | `sport` |
| `11-earth.md` | `history` | | `54-health.md` | `health` |
| `12-crossings.md` | `history` | | `55-language.md` | `culture` |
| `15-figures.md` | `history` | | `56-style.md` | `fashion` |
| `20-peoples.md` | `peoples` | | `58-knowledge.md` | `culture` |
| `25-other-minds.md` | `technology` | | `60-faith.md` | `religion` |
| `30-polities.md` | `politics` | | `65-arts.md` | `art` |
| `35-economy.md` | `finance` | | `70-music.md` | `music` |
| `36-logistics.md` | `logistics` | | `72-celebrity.md` | `celebrity` |
| `40-law.md` | `crime` | | `75-technology.md` | `technology` |
| `41-crime.md` | `crime` | | `78-communication.md` | `logistics` |
| `45-conflict.md` | `conflict` | | `80-cosmos.md` | `geography` |

**All seventeen domains now carry canon** (28 files, 370 facts) — `celebrity` was the last empty one
and closed with `72-celebrity.md`. Two domains are deliberately split across a principle file and a
practice file: `40-law.md` / `41-crime.md` (rights, then cases), and `78-communication.md` /
`36-logistics.md` (how word travels, then how mass does).

What remains is depth, not coverage. **Every domain is now at or above the 12-fact retrieval cap**, the number the station can draw
on for a single programme — so no domain is forced to recycle the same handful of facts on air.
`COMMISSION.md` holds the brief for commissioning further canon. What remains is depth, not coverage: `COMMISSION.md` §1 holds the
open list, and `DECISIONS.md` D-028 explains which domains are thinner than their airtime deserves.

## 8. Checklist

- Frontmatter on every content file; `domain` from the seventeen.
- One atomic assertion per fact. Name things; name them the same way twice.
- `{#anchor}` on anything the world will refer back to.
- Never a fixed year, never a date — the observance, not the instance.
- Editing a fact is safe; renaming a file or an anchor is not.
- Read [`SPIRIT.md`](SPIRIT.md) before writing, not after.
- Don't fabricate a world in one sitting. Grow the cornerstones, keep them consistent.
