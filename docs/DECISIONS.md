# Settlement Radio — Decisions

Append-only. One paragraph each, newest at the bottom. Includes things tried and reverted.
A decision recorded here outranks memory; if the code and a line here disagree, one of them is
wrong and fixing it is a task.

---

### D-001 · One clock, seven days — 2026-07-31

The station runs a single 24-hour skeleton every day of the week: the same junction at `:00`, the
same slot lengths, the same daypart character. Only the *occupant* of a slot and its *freshness*
vary by day. Slot lengths are day-invariant — a 56-minute weekend programme may not sit in an hour
that runs `4 + 28 + 28` on weekdays.

**Why.** `grid.yaml` was blocked on a weekend grid that did not exist at the same resolution as the
weekday one, and validations 5, 8 and 9 could not pass without it. Authoring a second (really a
third — Saturday and Sunday were to differ) 24-hour table meant three day-shapes to keep summing to
1,440 forever, and a permanent tax on every future schedule change. Considered and rejected.

**The weekend is still lighter**, because lightness is a freshness property rather than a clock
property (ARCHITECTURE §36: "the capacity lever is the freshness tier, not the format mix"). The
17:04 slot holds a fresh flagship on Monday and the same slot holds a repeat on Sunday. Weekday
fresh speech is ~526 min; weekend ~295. Twelve slots carry weekend overrides; everything else is
identical all week.

**Reversible.** A weekend variant later is a `days:` filter on a handful of programmes, not a schema
change. `grid.yaml`'s per-programme `schedule: [{days, at}]` already expresses everything above.

### D-002 · Weekly strands repeat inside the week; repeat count is editorial — 2026-07-31

The three 56-minute `W` strands (`The Common Table`, `Assembly`, `The Documentary`) previously
repeated "at the weekend", which the one-clock decision removed as a distinct place. They now repeat
in named in-week and weekend slots declared per strand in `repeat_slots`.

**Repeat count is not a capacity decision.** A `W` edition costs its production night once, whether
it airs twice or six times; the only cost of a further airing is audible repetition. ARCHITECTURE
§14's "two or three times" is therefore replaced by "as declared in `repeat_slots`, typically 2–6",
and same-day double-runs (`Relay` at 09:32 and 15:32, `Dispatch` at 11:32 and 14:04) are accepted as
standard practice for explainer and dispatch strands rather than treated as a shortfall.

### D-003 · The archive pool is ~135 hours, not 90 — 2026-07-31

Sizing the archive pool at "5 h/night × 14-day separation = 70 h floor, 90 h target" was wrong: the
grid as written airs **~9.5 hours of archive-class material per day** averaged across the week
(7.9 h on a weekday, 13.1 h Saturday, 13.5 h Sunday, where lightness means archive). At a 14-day
separation the floor is daily consumption × 14 ≈ **135 h**, with **165 h** as the target.

**The build cost roughly doubles.** ~135 hours at ~50% speech density is **~4,000 speech-minutes**,
not 2,250 — about 19 nights of pure archive render at the 0.7× tier, and realistically a couple of
months alongside everything else. This makes the pre-launch archive the longest pole in §35 by a
wide margin.

**The cost dial is the overnight music-led share.** A talk archive hour is ~42 speech-minutes; a
`music_show` or `music_sequence` hour is ~6. The Night Watch (01:00–05:00) is therefore specified
music-led in three of its four hours. Two further levers exist and are **not** taken — a shorter
separation window at launch (10 days → ~96 h floor), and a shorter Night Watch — both of which trade
audible recurrence for build time.

### D-004 · No music sequences in the daytime — 2026-07-31

The 05:32 slot held "Music to the hour", a `music_sequence`, which contradicted the station's own
rule that the only daytime music is the chart (PROGRAMMING §7) and ARCHITECTURE §11's statement that
`music_sequence` exists solely for the 01:00–05:00 archive block. The slot now holds `The Long
Record`, the history documentary strand, drawn from the archive pool. History is the cheapest and
most reusable content on the station, so this costs nothing and removes the contradiction.

### D-005 · The grid names `programme_type` directly — 2026-07-31

PROGRAMMING §8's "Format" column used free text (`explainer`, `analysis`, `short items`,
`specialist`, `review + profile`) that did not map onto the closed `programme_type` set in
ARCHITECTURE §11, so `grid.yaml` could not be written from it without inventing a mapping. The
column now carries a legal `programme_type` value and nothing else; the descriptive shape lives in
the strand's brief. A mapping table was considered and rejected as a second thing to keep in sync.

### D-006 · The full 165-hour pool is built; there is no launch date — 2026-07-31

This is a pet project with no deadline and nothing downstream of launch, so **render time before
going live is free** and the full pool is built rather than shortened. The levers in D-003 stay
unused. Do not re-propose them: a session that finds the ~4,000 speech-minute figure alarming is
reading it as a schedule risk, and it is not one.

**What binds instead is ordering, not time.** 165 hours is ~165 programmes, well past the 50-show
line at which step 13b forces the voice-identity decision, and the archive is the deepest lock-in in
the system (§3) — once it exists in a voice, changing that voice orphans it. So the pool is built
**after** the voice and register have survived real listening, not during the wait for it. Step 16
stays step 16. Unlimited time makes that ordering easier to respect, not optional.

### D-007 · Retention is keyed on slot length, not on format class — 2026-07-31

`format_class: junction` and "four minutes long" were the same thing until §13 made 28-minute news
programmes junction-class so they could state the time. The retention rule "junctions deleted after
air" then silently deleted `The Six`, `The Midnight Report` and `Crossfire` — around an hour a day
of the station's main news output, which `/archive` promises listeners they can browse.

Retention therefore keys on **`slot_minutes == 4`**. A bulletin from last Tuesday is four minutes of
a clock reading that no longer applies; a `The Six` from last Tuesday is a programme, and is kept 30
days and then offered to the archive pool like any other. The general rule: *class* decides what a
format may say, *length* decides whether it is worth keeping.

### D-008 · Imaging and pool items are separated by ownership, not by length — 2026-07-31

Idents and sonic logos appeared in both the `imaging` table (§9) and `pool_items` (§6), and in both
§13's pool minimums and §9's hour clock. One object in two tables drifts, and the drift shows up as
an ident that the mixer and the back-timer both think they own.

The boundary is **identity**: anything carrying a station or programme identity is `imaging` and is
placed by the hour clock; `pool_items` holds only back-timing filler, chosen by length. Idents come
out of `pool_items.kind` and out of `make pool-check`'s counts, which means the 37-piece minimum is
now 37 pieces of *filler* and slightly harder to reach than it looked.

### D-009 · The real-person screen matches on full names above a notability floor — 2026-07-31

"Any proposed figure name matching Wikidata's 1.5M humans is regenerated" is unusable: nearly every
plausible human name appears somewhere in that list, so the world tick would spend most of its
budget rewriting perfectly good invented people, and the screen would be switched off within a week
— which is worse than a loose screen.

The rule is now **exact match on the full name, against entities with ≥5 Wikidata sitelinks**
(roughly "has a real article in several languages") → ERROR and regenerate. Full-name matches below
the floor pass with an INFO line. Surname-only and fuzzy matches **flag in the rundown** rather than
blocking, because two people sharing a surname is how surnames work. Organisations use the same
mechanism and the same floor.

The risk this actually guards against is an invented council member sharing a full name with a
notable real person, and that is a far smaller set than 1.5M. A screen that fires constantly
protects nothing.

### D-010 · The Count is a weekly strand, and Saturday is a repeat — 2026-07-31

The Saturday chart slot was described as a "full rundown", implying a second and longer edition. It
cannot be: the chart computes 40 positions but 40 will not fit 28 minutes, and `R` means the same
audio. **Saturday reruns Friday's top 20, billed on air as a repeat.**

That makes `The Count` **`W`, not `F`** — produced once a week, repeated once, which is exactly
§14's definition of a weekly strand regardless of the fact that it carries this week's news. It
declares `production_day: wed` and one `repeat_slot`, and validation 9 now applies to it.

**A counting error surfaced with it.** `Relay` and `Body & Air` share the 09:32 slot but are two
separate weekly productions; the capacity tables had been counting them as one since v9. Corrected,
`W` production is **nine strands and 364 min/week** — 52 slot-minutes a day amortised, ~39 of
speech, not the ~27 previously carried. Weekday fresh speech is therefore **~526** rather than ~514,
weekend ~295, weekly average ~460. The tier ladder is unaffected below the top rung.

### D-011 · Chart clips do not score toward the chart — 2026-07-31

`The Count` airs 20 tracks a week as 30–40 second clips. If those counted as airplay, this week's
top 20 would arrive at next week's calculation carrying 20 free plays each and the chart would
promote whatever it had just played until nothing new could enter. That is a feedback loop, not
inertia — inertia is the `previous position` term, bounded at 0.20 and decaying.

`airplay.context` therefore distinguishes `rotation` from `chart_clip`, and **the 0.45 airplay term
excludes `chart_clip`.** The rows are still written, because rotation separation must know the track
was heard — playing it again an hour later is the audible clash the separation rules exist to
prevent, whether the earlier play was a clip or not.

### D-012 · Agents draft tasks; the operator accepts them — 2026-07-31

"An agent may not add tasks" assumed an operator who could write task cards. **The operator is not a
developer**, so the rule as written had no path forward: nobody could author the first `TASKS.md`
and the project could not start.

The rule now separates **authorship** from **authority**. An agent drafts cards in a **declared
planning session**; the operator accepts, rewrites or rejects each one; nothing lands without an
explicit yes. The anti-sprawl intent is untouched, because the failure mode §33 describes is an
agent *deciding what work exists* as a side effect of doing other work — and that stays forbidden.
Outside a planning session, a session still ends with `## Observations` and nothing else.

**A planning session covers one phase of `docs/PHASES.md` and stops.** Planning all phases up front
is a phase pack, which §34 records as the specific thing that killed the previous attempt, and the
10-item cap on `TASKS.md` is what makes it impossible. The roadmap already exists; it does not get
restated as tasks ahead of time.

**Consequence for the task format:** `Goal` and `Check` are written so a non-developer can judge
them — what will be true, and what they will see or hear. `Reads` and `Files` are agent bookkeeping.
And **WIP 1 applies to agent tasks only**: operator content items marked `[operator]` sit in
`TASKS.md` without consuming the slot, or writing the canon seed would block every code task for a
fortnight.

### D-013 · The roadmap gets its own document — 2026-07-31

A phase grouping was briefly added to ARCHITECTURE §35 and has been removed: §35 is the *technical*
build order, and sequencing, milestones, hardware lead times, accounts and the outward-facing work
are not architecture. **`docs/PHASES.md`** now holds eleven phases, A–K, each with a goal, an
observable outcome, its hardware / accounts / content prerequisites, and its dependencies on other
phases. It is the unit a planning session works in (D-012).

**This raises the documentation cap from eight to nine**, which is a real cost and taken knowingly.
The justification: the roadmap had no home, so it was being reconstructed in conversation every
time it was needed, and the outward-facing half of the product — the site, the YouTube channel,
support, social, the licence — appeared in no document at all. §35 covers what to build; nothing
covered how the station reaches anyone.

**It is a roadmap, not a phase pack.** One paragraph per phase, no tasks, no checklists, no
per-phase sub-documents, and it generates no work by existing. §34's rule stands: if it ever starts
producing work by being read, it has become the thing that killed the previous attempt and should be
cut back to the table of contents.

**Two things the phase map made visible that no document had said.** Phase J is entirely new
scope — YouTube's synthetic-content settings, Ko-fi, social presence, stream directory listings and
the LICENSE decision were scattered across §18, PRODUCT §10 and C10, and never sequenced. And
**Ko-fi is a compliance input**, not just a donations link: it is what puts the station outside the
AI Act's purely-personal-use carve-out, which is why phase G gates phase J.

### D-014 · §19's figure screen runs in C, not G — 2026-07-31

`PHASES.md` assigned the whole of §19 to phase G. §19 fixes the opposite order: the real-person
screen runs on the world tick's **proposed** figures, before they are committed, because anything
already in `figures` is exempt from the screen permanently. A phase-C tick that commits unscreened
names cannot be repaired in G — the exemption is the bug. **The deterministic screen therefore moves
to C**; the model check, profanity, structural checks and the quarantine path stay in G, and G still
reviews the whole gate with the lawyer.

**The screen is engineering, not a config file**, and was reading as content because it sat beside
C8. It is a ~1.5M-name Wikidata extract behind two structures — a bloom filter for exact match, a
trigram-indexed surname table for the fuzzy pass — with the ≥5-sitelink floor applied at query time.
Phase C now lists the download as a prerequisite in its own right.

### D-015 · Phase H is measured in archive hours; there are two pools — 2026-07-31

`PHASES.md` gave phase H the outcome "a pool deep enough that nothing recurs inside a fortnight,
`make pool-check` green". Those are two different pools. `pool_items` is back-timing filler — 37
pieces in three length bands, finished at step 13c in phase F, and the only thing `make pool-check`
counts (§13). The **archive** is §14's `A` tier at a 135-hour floor and 165-hour target, counted in
hours and reported by the digest and the rundown.

`make pool-check` goes green in F and stays green through H whether or not one archive hour exists,
so **the longest phase in the project had no valid observable check** — which under §33 means it was
not yet a phase that could be planned. H's check is now the digest's archive line at or above the
135-hour floor, held for a week without top-up falling behind.

**No new `make` target was added.** §24 already reports archive hours against target in the nightly
digest; inventing `make archive-check` would have been surface area for a number that is already
printed every morning.

### D-016 · Every architecture section has a phase, and every open decision has a closing phase — 2026-07-31

An audit of `PHASES.md` against all thirty-eight architecture sections found nine with no phase at
all. Five mattered: **§29 testing**, **§30 CI** and **§31 code standards** — which `CLAUDE.md`
requires from the first task and which are inside build step 0 — now land in **A**; **§4's Studio
half** splits, with the external volume layout and the Postgres mount guard in **C** and the process
model in **E**; and **§26** beyond its indexes distributes across C, E and F. §27's Studio posture
goes to E, §6's on-air writeback to E, and §36's planner budget enforcement — the mechanism that
refuses a grid exceeding `measured × 0.8`, and which no phase owned — to E.

**Two ordering conflicts are corrected.** §36.2's real measurement needs real canon and a real world
slice, so only the cheap week-one version belongs to A; the honest one is C. And D depends on **B**,
not just A and C, because its outcome is a show playing on the Transmitter.

**§38 gained a row and a home.** Nothing in the architecture measures listeners, yet PRODUCT §9
makes return listening and time in stream two of the five signals that matter — so it is recorded as
an open decision closing at phase J rather than quietly assumed. `PHASES.md` now carries a table
mapping all nine §38 rows to the phase that closes them; a register nothing references is a register
that rots.

### D-017 · The writer is 9–10B, not 9–12B — 2026-07-31

§2 stated the writer slot as "9–12B dense @ Q4 (**≤6GB** + KV)". Those are not compatible. MLX
4-bit costs ~0.56 bytes per parameter — 4 bits per weight plus a scale and bias per group of 64 —
so 9B ≈ 5.1 GB and 10B ≈ 5.6 GB fit, while **11B ≈ 6.2 GB and 12B ≈ 6.8 GB are over the profile
before any KV**. The band was written as 9–12B in three places (§1, §2, §36.2) and once in
`PHASES.md`, all now 9–10B.

**The profile wins, not the parameter count.** §2 already says "the commitment is the profile, not
the name", and the ≤6 GB figure is derived with reasoning — at 8 GB the Think phase reaches
~13.5 GB and leaves nothing for a re-render or the KV growth of a long act. The named candidate
was always Qwen 3.5 **9B**, so nothing about the intended build changes; what changes is that task
zero can no longer waste a day on a 12B that was never going to fit.

### D-018 · Capacity tiers count fresh speech only, and must be read one notch down — 2026-07-31

`PROGRAMMING.md` §9 and ARCHITECTURE §36 both tier the grid by fresh speech-minutes — ~200 at
RTF 0.7, ~300 at 1.0, ~460 at 1.5 — against usable nightly budgets of 216, 308 and 462. **Neither
table subtracts §14's ~30 speech-min/day of archive top-up, which comes out of the same budget.**
Every tier is therefore about 30 minutes over-subscribed, and the ~200 tier at RTF 0.7 does not
actually fit the machine it is named for.

**It is less bad than the arithmetic suggests, and still worth fixing.** Archive sits last on the
priority ladder and is built to be dropped on a long night, and retired floating shows and 28-minute
news programmes enter the pool for free after 30 days (§28) — which is the same mechanism M4
describes. At the ~300 tier the day makes ~300 broadcast minutes of programme material against an
archive appetite of ~60, so a modest time-neutral fraction covers it.

**But the fraction is unknown and news-shaped output goes stale fast**, so it is not safe to assume
pre-launch. Both tier tables now say to plan one notch below what the measured RTF appears to buy,
and to relax it once the digest shows what retirement actually contributes. **Recorded as a
measurement to take, not an open decision** — it resolves with three months of real retirement data
and needs no §38 row.

### D-019 · The cast engine is chosen on sound, never on watermarking — 2026-07-31

Chatterbox was picked partly for its built-in PerTh watermark, which supplies the second of §18's
two inaudible marking layers for Art. 50(2). That made a compliance property into a hidden input to
a voice-quality decision — and the engine is chosen in phase A while the lawyer reviews the marking
in phase G, so the two could diverge for months without anyone noticing.

**The voices are the product; the marking is an obligation with more than one implementation.** So
the commitment is the **two layers**, not the engine that happens to provide one of them. The cast
engine is chosen on how it sounds. If the winner does not watermark, a standalone watermarking pass
applied after render supplies the second layer, and that is **phase G work** — planned, not
discovered.

**Task zero records the fact rather than acting on it**: for every TTS candidate it resolves, one
extra column saying whether it watermarks and by what mechanism. No extra work, and phase G inherits
an answer instead of a recollection. §38's "Chatterbox vs Qwen3-TTS" row loses its compliance limb
and becomes what it should always have been — a listening test.

### D-020 · The assemble window is measured in phase A, and the night moves before the product does — 2026-07-31

§14 allots 06:30 → 06:50 to mixing, loudness normalisation, C2PA signing and cue sheets, and that
20 minutes was written down rather than measured — the only tight window in the system without a
number behind it, while TTS RTF gets an entire phase. Signing is per-file across several hundred
files and is the part most likely to surprise.

**It is measured in phase A (§36.3) and it is a budget, not a gate.** ~50 representative segments
through the real assemble path, timed, extrapolated to a night's output at the tier the RTF
measurement bought. The figure goes in `config/measured.yaml` beside the RTF.

**The reason to measure it early is that one of the fixes is a design decision.** If assembly is
slow the levers are, in order: start the night earlier, move the render/assemble boundary earlier,
or assemble incrementally as each render completes. The third removes the deadline entirely and is
cheap before step 11 exists and a rewrite afterwards. **The fresh tier is not a lever** — speech is
the product and the window is not, so the night moves before the programming does.

### D-021 · The archive is elastic; the separation window never moves — 2026-07-31

§38 asked whether to build 135 hours or shorten the 14-day separation window. **Neither: build
whatever the separation window requires, and let the launch date absorb it.** If the rotation
simulation says the pool needs 300 or 400 hours at the tier the station ships at, that is 300 or 400
hours of render — nights, not compromises. D-003's two declined levers (a 10-day window, a shorter
Night Watch) stay declined permanently. 165 hours becomes a target with no ceiling above it.

**This is affordable only because there is no launch date (D-006)**, and it is the cheapest trade in
the project: pre-launch render time costs calendar and nothing else, while a shortened separation
window costs audible repetition forever, on the one thing the product is actually about.

**It also gives phase H a real check, which it did not have.** The promise — no programme twice
inside a fortnight — is only *audible* after two weeks on air (phase K), but it is fully
*computable* now: run the archive scheduler forward over 30 synthetic days and assert no item is
drawn twice inside the window. It passes, or it returns the shortfall in hours, which is the
instruction for what to do next. H can no longer fail, only run late.

### D-022 · Precedence between documents is stated once, in §32 — 2026-07-31

Which document wins was stated in four places — `CLAUDE.md`, `PHASES.md`'s preamble, §35 and §15 —
in terms that did not agree: the `PHASES.md` preamble said `ARCHITECTURE.md` was right about any
shared detail, while §35 said `PHASES.md` wins on ordering. An agent cross-checking documents
mid-session could reach opposite conclusions depending on which it read first.

**§32 now carries the only precedence table**, covering all nine documents, and the other four
places point at it instead of restating it. Two rules resolve nearly every real case: **on *when*,
`PHASES.md` wins; on *what* or *how*, `ARCHITECTURE.md` wins** — and a later `DECISIONS.md` entry
beats both, which is what append-only means.

**Two concrete collisions were fixed at the same time.** §35's content track gated C7 on step 13c
alone while `PHASES.md` needed pool pieces in phase E; it now names both steps and what each one
means. And **"pool" meant two unrelated things** — the 37-piece back-timing pool and the 135-hour
archive pool — which had already produced one wrong phase check (D-015); §13 now carries a naming
table, and the full name is used in code, tasks and prose.

### D-023 · Canon lives at the repo root; frontmatter is what makes a file world content — 2026-08-01

The bible was carried over from the previous app in `docs/canon/`, where a **numeric filename
prefix** decided what the seeder loaded and an unprefixed name (`README.md`, `SPIRIT.md`,
`TAGS.md`, `AUDIT.md`) marked an authoring guide. §21 puts canon at `canon/` and §7 gives every
file YAML frontmatter, but **neither says what happens to a file in `canon/` that has none** — and
`SPIRIT.md` has to live there and never reach the DJs.

**The rule: frontmatter is the marker.** A file with `id / domain / scope / status / supersedes` is
world content; a file without it is an authoring guide and `canon-check` and `canon-sync` skip it.
This replaces the numeric-prefix rule, which now carries no meaning at all — prefixes are kept
purely as human reading order, and `id` and `domain` do the work. Chosen over a hardcoded skip-list
because a list has to be maintained and a missing entry silently seeds a brief into the world.

Consequences applied in the same session: `docs/canon/` → **`canon/`**; all 25 content files given
frontmatter; **`90-cast.md` → `cast/CAST.md`**, because cast cards are item C2, ship verbatim in
Tier 0 and are never retrieved, so they must not be visible to canon tooling at all. `cast/` is a
new root directory not named in §21, chosen to parallel `canon/`, `music/` and `voices/`.

### D-024 · Canon carries no tags — 2026-08-01

The inherited bible tagged every fact with 4–12 free-form words (286 bullets across 26 files) to
feed a `store.canon_by_tags` set-overlap match. **No such mechanism exists in this architecture and
none is planned.** §5 narrows canon by `facts.domain` (one of the seventeen, closed), BM25 over
`tsvector` for proper nouns, dense bge-m3 embeddings for meaning, and a generated `context_prefix`
that does what the tags were reaching for. `TAGS.md` and every tag bullet were removed.

**This is not neutral cleanup.** A fact is indexed as `context_prefix + "\n" + text`, so a trailing
twelve-word tag list inside a two-sentence fact lands in both the tsvector and the embedding as
noise — on the shortest facts, outweighing the signal. Leaving them would have degraded retrieval
while costing authoring time for no effect.

### D-025 · A recurring observance is canon; a dated instance of it is a beat — 2026-08-01

`95-events.md` hand-authored nine dated occurrences (`In-world datetime: 2627-06-24T20:00`) with a
"roll-forward policy" requiring the operator to bump each year by hand after it passed. In this
architecture dated occurrences are **beats**, written by the nightly tick (§6), and hand-authored
events have no table to land in.

The content itself is good world material and was kept in full: the file is now
**`canon/51-observances.md`** (`domain: culture`), holding each observance as prose — its shape,
its meaning, what people do — with the datetime and cadence-label bullets dropped and a stable
`{#anchor}` added per entry. **Write the institution, never the instance**, which is the same rule
that already forbids a fixed year anywhere in canon.

This also settles the `fact_key` anchor syntax §7 leaves open: **`{#slug}` appended to the
heading**. Needed because §7 makes `fact_key` permanent while a slugified subject line is not —
anything the world refers back to needs a name the author controls.

### D-026 · `canon/AUDIT.md` deleted; its screens are owed to `banned-entities.yaml` — 2026-08-01

A 188-line agent runbook carried over from the previous app: "audit `docs/canon/<file>`" → validate
against five gates → fix → overwrite the file → re-seed. Deleted, for three reasons.

**It was redundant.** `canon-check` performs five of its six live gates mechanically on every commit
and push, rather than when the operator remembers to invoke it: parse (pass 1), IP boundary and
franchise echoes (pass 5), floating year (pass 7), tone and register (pass 6), and consistency with
the rest of the bible (pass 2, which retrieves the 8 nearest facts and asks whether they clash). The
sixth gate — tag conventions — died with D-024. Its Step 1 script imported `src.world.canon_source`,
a module of the previous design.

**It answered a question this project does not have.** The runbook is scoped to a file *an external
writer has changed*. There is no external writer, and §33 puts canon in the never-delegated column —
"Writing canon. Resolving canon conflicts." An agent overwriting a canon file is that delegation.

**It is the shape §34 forbids first** — "no phase packs, no task-generating documents. The failure
mode of the last attempt." A runbook whose output is findings and whose findings become edits is a
work generator, and a stale one is a trap rather than a dead letter.

**Owed to `config/banned-entities.yaml` when C8 is written** (an agent may edit it, §33) — these are
the screens the file held that no pass currently covers:

- **modern-AI tropes** (SPIRIT §2, not covered by any pass): `singularity`, `superintelligence`,
  `upload(ing|ed|s)`, `chatbot`, `neural net`, `machine learning`, `LLM`
- **franchise-echo proper nouns** (pass 5 fuzzy, needs the terms): `core worlds`, `outer worlds`,
  `federation`, `the empire`, `jedi`, `terran`, `spice`, `ansible`, `foundation`
- **author-name leak into prose** (pass 5 exact): Asimov, Clarke, Heinlein, Bradbury, Le Guin, Lem,
  Butler, Herbert, Dick, Tolkien, Strugatsky, Miller, Brunner, Delany, Russ, Tiptree
- **floating-year violations** (pass 7 has the rule, not the patterns): a bare `\b2[0-9]{3}\b` in
  canon, and `(hundred|thousand|N) years? (since|ago|after|of counting)` — the `+600` is the gap to
  *our* present, never an in-world count that goes stale

One screen has no home and is not worth a document: British spelling normalisation (`honoured`,
`neighbours`). If it matters, it is a pre-commit hook, not a runbook.

### D-027 · `canon/COMMISSION.md` — a commissioned-writer brief, at the operator's request — 2026-08-02

The operator asked for a single self-contained document to hand a writer producing the missing
canon. §32 permits a new document when the operator asks for one; this is that. It carries no
frontmatter, so it is invisible to `canon-check` and `canon-sync` (D-023).

**Why not fold it into `canon/README.md`.** README is the authoring contract and already covers the
header block and the format. Three things it cannot do: name what is *currently* missing (that
changes per commission), consolidate the forbidden-fact rules — which are spread across
`PROGRAMMING.md` §3's per-domain traps, `SPIRIT.md` §2 and §5a, and `75-technology.md`'s hard
ceiling — and stand alone for a writer with no access to the repo or the architecture. `canon/` now
holds three authoring guides and no more.

**This partly reverses a reason given in D-026.** That entry argued `AUDIT.md` should go partly
because "there is no external writer." There is one. The other two reasons hold and the deletion
stands: `canon-check` performs five of its six live gates mechanically, and every mechanic in it
was written against the previous design. What was actually missing was a brief for the *input* side,
which is this file — not a runbook for auditing the output.

**Note the standing tension, unresolved.** §33 puts canon in the never-delegated column — "Writing
canon. Resolving canon conflicts." A commissioned writer is a delegation of exactly that. The
operator has made the call; recorded here so nobody re-derives it as an inconsistency later. The
mitigation is that `canon-check` gates everything a writer submits, and the operator still resolves
every conflict it reports.

### D-028 · The missing canon, named — 2026-08-02

Fact-level coverage of the seventeen domains, measured across 267 facts in 25 files: `culture` 58
and `technology` 28 are buckets holding several unrelated files; `celebrity` has **zero**; and two
domains are covered on paper only — `crime` shows 12 facts but `40-law.md` is jurisprudence, of
which perhaps three are crime-desk material, while `logistics` shows 10 but `78-communication.md` is
signal routing, not freight (the convoy and cargo material sits in `35-economy.md` under `finance`).

The commission in `COMMISSION.md` §1 follows from this: new `72-celebrity.md`, `41-crime.md`,
`36-logistics.md`, `11-earth.md`, `12-crossings.md`, and top-ups to sport, fashion, health and
peoples. History gets two new files despite already having 21 facts because it carries the overnight
block and the bulk of the pre-launch archive — the heaviest load in the build order sits on one of
the smaller piles.

**Not fixed, and deliberately.** The `culture` and `technology` buckets cannot be split — the
seventeen are closed — so each keeps one Tier 1 summary spanning unrelated material, and that
summary ships on every call. And `40-law.md` keeps `domain: crime` rather than being re-filed to
`politics`, so the domain is not left empty while `41-crime.md` is written.

### D-029 · `80-cosmos.md` refiled to `geography`; the `culture` bucket is left alone — 2026-08-02

D-028 recorded two domains holding unrelated files, each of which therefore gets one Tier 1 summary
spanning material that does not cohere — and that summary ships on every generation call. Half of it
is now fixed and half is deliberately not.

**Fixed.** `80-cosmos.md` moves `technology` → `geography`. Its content is the shape of the settled
region and its edge, the sky as seen from the worlds, reading the sky, the observatory — the map one
zoom level out, sitting naturally beside `05-worlds.md` and `06-gazetteer.md`. `technology` drops
28 → 18 and reads coherently as the made world and its limits; `geography` rises 20 → 30 across
three files on a single axis. Frontmatter only; no prose touched.

**Not fixed: `culture`, at 58 facts across six files.** Three of the six match `PROGRAMMING.md` §3's
culture exactly (`50-daily-life`, `51-observances`, `55-language`); `58-knowledge` is education and
research-as-custom, defensible and with no better home among the seventeen. The two that genuinely
do not belong are `00-station.md` and `01-time.md` — station identity, the in-world premise and the
clock concept, which §5 names as **Tier 0**: always-present cached prefix, never retrieved. Moving
them is the correct answer and was declined anyway, for one reason:

**§7 defines no source location for Tier 0 text, and no code exists yet.** Moving the premise facts
out of `canon/` today would take them out of the only pipeline that is specified, and put them
somewhere nothing is built to read — a regression dressed as a fix. `cast/` was moved because §35
C2 and §5 together name cast cards as a distinct content item; station identity has the §5 half and
not the C2 half. Resolving where Tier 0 text lives is an architecture decision and its own task
(§33), not a frontmatter edit. Until then `culture` carries a summary broader than it should, which
is a cost worth paying over a gap that hides the premise.

Also considered and declined: `51-observances.md` → `religion`. §3's religion names "observances"
and §3's culture names "festivals", so both have a claim; the file's content is largely civic
remembrance rather than faith, it carries 0 facts (prose only), and the default on a judgment call
is no change.

### D-030 · Tier 0 text lives in `core/`, loaded whole and verbatim — 2026-08-02

§5 defined Tier 0 — "the station's identity, the in-world premise, the register rules, the cast
cards" — as fixed text in the cached prefix, but **never said where that text comes from.** In
practice `00-station.md` and `01-time.md` sat in `canon/` carrying `domain: culture`, which made the
station's own premise a *retrievable* fact competing for twelve seats against food and festivals,
and forced the `culture` Tier 1 summary to cover both what people eat and what this station is
(D-028, D-029). The gap surfaced three times before it was closed.

**The rule.** `core/*.md` is Tier 0 source: loaded **whole and verbatim**, in filename order, into
the cached prompt prefix, on every generation call. It is **not canon and is never parsed** — no
frontmatter, no atomising, no `fact_key`, no embedding, no retrieval. `canon-check` and `canon-sync`
do not read it. It is prompt text, and that is the entire contract.

`00-station.md` → `core/STATION.md`; `01-time.md` → `core/TIME.md`. Canon frontmatter stripped (it
was actively wrong), the `## Canon facts` headings retitled so neither file reads as parser input,
and every assertion kept verbatim. `canon/` drops to 23 files; `culture` drops 58 → 38 facts across
four files that all match `PROGRAMMING.md` §3's definition.

**Tier 0 has no growth mechanism, deliberately.** It is the one tier every call pays for in full, so
a file added to `core/` raises the floor of every prompt in the station. Two files is the intended
size and the ~2–3k budget is shared with the cast cards; a third file needs a reason.

**Why a folder rather than a config key.** Tier 0 is text a human writes and reads aloud in their
head, not configuration — the same argument that puts canon in markdown. A directory also makes the
boundary enforceable by looking: anything in `core/` always ships, anything in `canon/` is searched.

§5 and §21 updated to name the source; `canon/README.md` §5 now carries the canon-vs-core boundary
with the test — *if it would be embarrassing for the station not to know it, it belongs in `core/`*.

### D-031 · Prose is not atomised; the `## Canon facts` list is the only source of Tier 2 facts — 2026-08-02

Reviewing the first commissioned file raised what looked like a duplication problem: its prose
subsections and its numbered facts state the same things about the same figures, as every inherited
canon file does. If `canon-check` pass 1 atomised whole files — which is what `canon/README.md` §4
claimed — each of those would yield two near-identical facts competing for the same twelve
per-domain seats, and pass 2 would raise roughly fifteen duplicate conflicts per file across
twenty-four files. That is the work-generating machine §34 exists to prevent.

**It was never the design; the README was wrong.** §7's "Where it runs" puts pass 1 among the
deterministic passes that "need no model and finish in seconds". A model-free pass cannot atomise
free prose — deciding where one assertion ends is exactly a model judgement. Pass 1 can only be
parsing an explicit structure, which is the `## Canon facts` numbered list. §5 says the same thing
in one line: **"Detail is retrieved; structure is always resident."** Detail is the fact list →
Tier 2; structure is the prose → the Tier 1 domain summary.

So restating a prose point in the fact list is **correct, not redundant** — the prose explains, the
list declares what is searchable — and the inherited files were right all along.

**The consequence worth stating to authors, now in `README.md` §4 and `COMMISSION.md` §3:** the fact
list is the only part of a canon file that can ever be quoted on air. A detail left in a paragraph
shapes the station's sense of a domain and is never spoken. If it should reach the microphone, it
has to be a fact. This makes fact-list density an authoring lever rather than a formality —
`72-celebrity.md` turns 1,876 words of prose into 15 reachable facts, and the specific texture in
between (a Meridian racing patch and its mismatched Cold Harbor copy) is currently unreachable.

No files moved and no content changed; this corrects a document, not the world.

### D-032 · C10 closed: content all-rights-reserved, `src/` MIT — 2026-08-02

§35 item **C10** required a licence decision "before the repo is public". The repo has been public
since 2026-07-29 and canon was pushed into it on 2026-08-02, so the item was overdue rather than
upcoming — 313 facts and five commissioned files were published under no stated terms at all.

**The decision, implementing C10's split.** The repository default is **all rights reserved**,
covering `canon/`, `core/`, `cast/`, `voices/`, `music/`, `docs/` and `prompts/` — no right to copy,
adapt, broadcast, train models on, or make derivative works. **MIT** is stated in advance for the
code paths (`src/`, `tests/`, `migrations/`, `web/`, `panel/` and the build files), none of which
exist yet; C10 offered MIT or Apache-2.0 and MIT was taken as the simpler of the two. Because no code
is committed, that half is still free to change.

**Default-deny rather than default-permit** is the whole shape of it: a bare MIT file at the root
would have been read as covering the world bible, which is the one asset that cannot be rebuilt.

**Absence of a licence was not neutral, but it was not catastrophic either.** No licence means
default copyright — the holder keeps everything, and GitHub's Terms grant platform users only view
and fork. That is close to the posture C10 wanted for canon. What was missing was the *declaration*,
and the code half, and the two things below.

**Two things this cannot settle, both recorded rather than resolved:**

1. **Commissioned work.** Five canon files were written by a commissioned writer. An
   all-rights-reserved statement asserts the operator's position; whether it is effective per file
   depends on the written agreement with the author. **Each commission should carry a written
   assignment or licence of rights**, and that is cheapest to obtain while the relationship is
   active.
2. **It is not legal advice.** Written by a non-lawyer from public sources, in the same class as
   §18. It is explicitly in scope for the §35 step 15 legal review, alongside the disclosure package
   and the music licence evidence. The copyright line carries a placeholder until a legal name or
   entity is set.

**Music is the operator's own material, not third-party.** The library is generated under a **Suno
Pro subscription**, whose terms grant the subscriber ownership of the output and commercial-use
rights, so `music/` sits under Part 1's all-rights-reserved statement like the rest of the content
rather than in a third-party carve-out. The subscription evidence remains a required step 15
artefact (§35, C5) — that requirement is about proving the grant, not about who owns the result.

**Also closed in the same pass:** a `.gitignore`, which the architecture had assumed since §7
("`canon-report.md` — a derived artifact, gitignored like the rundown") and §23 (`.env` gitignored,
`.env.example` committed) without one ever existing. Two `.DS_Store` files were untracked.

### D-033 · Two duplicate canon facts resolved after the first global audit — 2026-08-03

The first deterministic audit across the whole bible — all-pairs similarity over 353 facts, ~62,000
comparisons — found two genuine duplicates. Both were in the **inherited** files, none in the nine
commissioned ones, which is the expected shape: the new material was reviewed file by file as it
arrived and the older material never had been.

**Concordance was defined twice, in the same domain** (`05-worlds.md` #4 and `06-gazetteer.md` #1,
both `geography`, similarity 0.38 — the highest in the corpus). Two facts competing for the same
twelve retrieval seats to say the same thing. The gazetteer's version was richer on every point
except one clause, so `05-worlds.md` #4 was removed and **"and the world others measure distance
from" moved into the gazetteer fact** — the operator's own words relocated, nothing rewritten.

**The station's observatory was stated in two tiers at once.** `80-cosmos.md` #8 compressed
`core/STATION.md` #10 and #12 — the dome, the wall of photographs, the drift, the good-luck custom
of sighting your home world. `core/` ships verbatim on **every** generation call, so the retrieved
copy told the model nothing it did not already have, while occupying a `geography` seat. Removed.
It also carried a small inconsistency worth losing: it had the dome tracking stars, where Tier 0 has
the automated instruments tracking the relay network and only the telescope manual.

Canon drops 333 → 331 facts; `geography` 30 → 28; no domain falls below the twelve-fact cap. Facts
renumbered sequentially in both files, which is safe because `fact_key` derives from an anchor or
the fact's subject, never from position (§7 pass 1).

**The audit is worth keeping as a pass.** It is deterministic, model-free, and ran in seconds, and it
found something nine individual file reviews had missed. §7's seven passes do not include it, and
**pass 2 structurally cannot** — it detects contradictions, and near-identical facts do not
contradict, they agree. Resolution stayed with the operator (§33); the deletions were mechanical
once the choice was made.

### D-034 · `cast/COMMISSION.md` — a cast-writer brief, at the operator's request — 2026-08-03

The operator asked for a self-contained document to hand an external writer producing the C2 cast
cards. §32 permits a new document when the operator asks for one; this is that, and it is the exact
parallel of D-027's `canon/COMMISSION.md` — same class, same reason, sitting beside the thing it
commissions. It is prose for a human and is never loaded by anything: §5 loads only the `### `
presenter cards of `cast/CAST.md`, and `canon-check` / `canon-sync` do not see `cast/` at all.

**Why not fold it into `CAST.md`'s header.** That header is Tier 0-adjacent text in a file whose
whole cost model is "every word ships on every call". A 300-line brief cannot live there, and the
brief has to stand alone for a writer with no repo access — restating the premise, the seventeen
domains, the register bounds, the separation rule and the IP firewall, all of which currently sit in
four different documents the writer will not have.

**What the audit that produced it found**, recorded because it is the input to the next cast task
and will otherwise be re-derived: the ten inherited cards carry none of §11's five concrete things;
they describe a music station's dayparts (night shift, weekend afternoons, live sport) against
`PROGRAMMING.md` §8's speech grid; four of them are field-based on a premise that structurally
forbids the `two_way`, which is the workhorse item of every fresh daytime programme; the `D9.4` tag
paragraph and its eleven-name `DOMAINS` list died with D-024 and never matched the seventeen; the
`R7.0` public-bio contract is named in no document and no code path publishes it; and several sample
lines are aphorisms or state the clock, which §11a and §13 invariant 2 respectively forbid — and
sample lines are the strongest steer in the card, so a card that models the failure teaches it.

**Note the same standing tension D-027 recorded.** §33 puts cast cards and speech profiles in the
never-delegated column. A commissioned writer is a delegation of exactly that; the operator has made
the call. The mitigation is weaker here than for canon — `canon-check` gates canon, and no
equivalent gate exists for cards. What does gate them is `grid-sync` validations 1 and 2 (a profile
for the register kind each role requires; the co-host separation rule), which catch a missing or
undifferentiated profile but nothing about the writing. The register itself stays a judgement by ear.

### D-034 · Canon links by naming the thing, never the filename — 2026-08-03

Twenty-two filename references had accumulated inside canon **prose** sections — `"The Carrying
Lists in \`11-earth.md\` establish…"`, `"as \`55-language.md\` records"`, `"the Thaw Docket from
\`41-crime.md\`"`. Each marked a genuine cross-file extension, which is the strongest thing in the
bible; the citation *form* was the problem.

**Prose is what generates the Tier 1 domain summary, and that summary ships on every generation
call** (§5). A file path in a paragraph therefore ends up inside the digest the station carries into
every programme it makes. The count had reached 22 across eight files, and was rising by six or
eight per new file as the writer's cross-referencing got better — the better the writing, the worse
the leak.

**The rule: name the thing, never the file.** A named entity is what retrieval matches on (§3, and
§7 pass 4 resolves references by name), it survives any rename or merge, and it reads as world
rather than as apparatus. A path is invisible to retrieval and breaks on contact with
reorganisation.

**All 22 removed. Twenty-one were pure deletions** — dropping " in `20-peoples.md`" from "the
ordinary Forge knock in `20-peoples.md`, where sound tests whether a surface can be trusted" leaves
the sentence intact and the link fully carried by the named custom. That is the proof the paths were
decoration: in every case the entity was already doing the work. The twenty-second needed a real
rewrite, because the sentence *was* the cross-reference, and the operator supplied it.

Fact counts unchanged at 370, all seventeen domains intact, and every linked entity still appears in
both files of its pair. `COMMISSION.md` §3 now carries the rule with worked examples, and the
closing test: **if a reader would not understand the link without the filename, the named thing is
not established clearly enough yet — fix that instead.**

### D-035 · `core/` carries the same music-station mismatch as the old cast; commissioned — 2026-08-03

`cast/CAST.md` was rewritten because it described presenters for a music station rather than the
speech service the grid actually schedules. **`core/` has the same defect, and it matters far more**,
because Tier 0 ships whole and verbatim on *every* generation call rather than only when a given
presenter is on air.

Three passages in `STATION.md` contradict `PROGRAMMING.md` §8 outright: the premise says the station
"plays music, reads the news"; fact 9 gives presenters "wide latitude in programming" when the
schedule is fixed in config; and fact 9 reserves "the midnight hour" for listener requests when the
grid has a 28-minute news programme at 00:04 and a history documentary at 00:32.

**One line in `TIME.md` is worse than a mismatch — it teaches a rule violation.** *"The DJ gives
real-feeling time checks ('coming up on two in the morning, settlement time')"* instructs the model
to do the one thing §13's air-time rule forbids for floating content and enforces with a regex
acceptance test that regenerates on failure. It has been shipping in every prompt, with a worked
example, while `cast/COMMISSION.md` §4 correctly tells the writer never to state the clock.

**Tier 0 is also over budget.** `STATION.md` 807 words + `TIME.md` 421 + two cast cards 682 is
~2,578 tokens against §5's 2,000–3,000 ceiling — and `prompts/register.md`, the third Tier 0
component (§11a), is not written yet. A three-voice programme breaches it today. The commission
targets ~800 words for `core/`, roughly a third off, which is where the slack has to come from since
D-030 gave Tier 0 no growth mechanism on purpose.

**A standalone `core/COMMISSION.md` was created at the operator's request** (§32 permits a document
when the operator asks). The recommendation had been a section inside `cast/COMMISSION.md`, because
Tier 0 is a single budget shared between core text and cast cards and a writer needs to see that
trade-off in one place; the operator chose separation for traceability, and the budget table is
reproduced in the new file so the shared ceiling stays visible.

**Standing observation:** this is the third place the previous app's music-station framing has
surfaced — the cast cards, the canon header notes naming the non-existent programmes "The Fit" and
"The Ward" (D-029 era), and now `core/`. Anything not yet re-read should be assumed to carry it.

### D-036 · The cast is six speech presenters, not eight music DJs — 2026-08-03

`cast/CAST.md` inherited eight character cards written for a music station: DJs with a `Logical
voice:` registry key, wide programming latitude, night-shift framing and setlists. The station the
grid actually schedules is a **speech service** — an hourly bulletin, a three-part breakfast strand,
an evening flagship, correspondents, documentaries, and one weekly chart show, with music leading
only overnight. The cards described a different product.

**Replaced with the six the architecture specifies** (§35 C2): breakfast host, evening host,
`scripted` newsreader, chart voice, and two beat correspondents — Wren, Vell, Thorn, Mira, Joss,
Nera. Every card carries the nine required fields, and every speech profile sits inside §11a's
bands. The `grid-sync` separation gate passes on all three conversational pairs before the gate
exists: hedge rates 18 / 38 / 58, no shared `hedge_form`, no shared `disagreement` mode.

**Five inherited fields were retired**, each for its own reason: `Logical voice:` (a voice is a
committed WAV plus a fixed seed, both operator-owned — there is no registry key, §3); `Public bio:`
(nothing publishes cards to the web, so it cost tokens on every call for no effect on air); `Tags:`
(D-024); `Based: station | field` (superseded — see below); and `Voice (for TTS):` (timbre comes
from the reference recording, not from a sentence describing it).

**The finding that shaped the roster: a correspondent is at the station, not out in the worlds.**
The commonest item in news radio is the two-way — host asks, correspondent answers, live, in the
moment. In this world an *addressed* message takes days to weeks, so a genuinely field-based
correspondent can never do one; they can only send finished dispatches. Correspondents therefore
work the relay traffic for their beat from the newsroom, which is why `Based:` no longer does any
work. Travelling correspondents remain possible and rare, and are not part of the roster.

Two canon repairs were needed. Wren was "born aboard the generation ship *Long Patience*", which
`12-crossings.md` writes in the past tense and whose next section establishes that generation ships
were dismantled at landfall; she is now "born a Betweener, raised aboard ship", using the category
`20-peoples.md` already defines and inventing no new entity. Thorn's card was left as written
because `06-gazetteer.md` already says "the station's Thorn learned the news trade as a stringer"
on Forge — the writer built on an existing canon reference rather than around it.

**C2 is closed.** Engineering step 8 — one show, two speakers, rendered and mixed onto the
transmitter, which §35 calls the go/no-go moment — is unblocked. C3 (reference clips plus
`voices/PROVENANCE.md`) is the remaining content item before hardware.

### D-037 · Voice reference clips are committed to the public repo; the cloning risk is accepted — 2026-08-03

§3 requires a decision here rather than a default: *"anyone can clone your presenters' voices… the
choice to accept it belongs in `DECISIONS.md` rather than being made by default."* Nothing had been
recorded, the repo has been public since 2026-07-29, and **git history is permanent — once a
reference WAV is committed publicly, deleting it later does not un-publish it.** The choice is free
until the first clip lands and irreversible afterwards, so it is taken now, before C3.

**Decision: commit the six reference WAVs to `voices/` in the public repository, and accept that
they can be cloned.**

**Why.** The clips are synthetic and reference no real person, so this is not a deepfake or
compliance question — §18's rule is about never cloning a *real* voice, and that rule is unaffected.
What remains is impersonation-of-the-station risk, and it is small: a fictional presenter's voice has
little value to an attacker, the station's identity is protected by the all-rights-reserved terms
covering `voices/` in `LICENSE` (D-032), and the disclosure layers in §18 — spoken ident, hourly
sting, C2PA, watermark, stream metadata — are what actually distinguish genuine output.

**Against the alternatives.** Gitignoring `voices/` was declined because §3 makes the WAV the
canonical artifact — *"you own that file; a vendor voice ID is a dependency, a WAV is not"* — and
§35 calls the directory irreplaceable; moving the least reproducible asset in the project out of
version control to avoid a low-value attack is a bad trade. Making the repository private was
declined because the public position is deliberate and now stated in `LICENSE`: the project can be
read and its methods learned from, while nothing is licensed for reuse.

**What this does not decide.** The voice-identity lock-in (§35 step 13b) is separate and still open:
once an archive exists in a voice, changing it orphans every show in it, and the choice between bulk
re-render and an in-world host change must be made **before 50 shows exist**. This entry is only
about publication.

**Consequence for C3.** `voices/PROVENANCE.md` still carries its full §18 burden — per clip: engine
and model version, prompt or preset, seed, date, and an explicit statement that no real person's
voice was used or referenced. That record must be written **at the moment each clip is made**; a
seed or a model revision cannot be reconstructed six months later. C3 itself remains gated on phase
A, because the engine must be chosen before a clip is worth making (`PHASES.md`).
