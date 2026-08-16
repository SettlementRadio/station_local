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

### D-038 · The scaffold's judgment calls: what is required at startup, and what `make setup` installs — 2026-08-06

T-003 built the repository skeleton, and four details §21–§24 leave open had to be settled. All four
took the smallest option that keeps the rules of §31 mechanical.

**Two lines are required at startup, not five.** `DATABASE_URL` and `MEDIA_ROOT` have no defaults,
so a missing one stops every command at process start and names itself. `ICECAST_SOURCE_PASSWORD`
is optional and defaults to unset — it is a §23 secret, but the server it belongs to does not exist
until T-010, and making it required would have blocked every command in Phase B behind a password
for a machine nobody has yet. The command that needs it fails naming it. The rule: a value is
required at startup when *any* command needs it, and optional when *one* does.

**System tools split by machine rather than by §22's list.** §22 names ffmpeg, liquidsoap, icecast
and postgresql@16 together, but §4 puts Liquidsoap and Icecast on the Transmitter. So `make doctor`
treats `uv`, `gitleaks`, `ffmpeg` and `psql` as required on the Studio and reports the two
Transmitter tools as "absent" without failing. A check that fails for a tool the machine does not
need is a check the operator learns to ignore.

**`make doctor` exists and is not in §17's list.** §17's `make setup` line says "check system
tools"; that check is worth having on its own, because it is also how the operator sees the
fail-fast behaviour of §23 working. `setup` calls it when a `.env` is already present.

**Hooks run local tools, not mirrored ones.** `.pre-commit-config.yaml` invokes `uv run ruff`,
`uv run mypy` and the Homebrew `gitleaks` rather than pinning separate hook repositories, so the
version that gates a commit is the version in `uv.lock` and cannot drift from CI. The
`canon-check --fast` hook §22 asks for is absent until that command exists.

**Two smaller things.** ruff excludes `*.md`: ruff 0.16 formats Python inside markdown code blocks,
and it rewrote the examples in `ARCHITECTURE.md` on its first run — the documents are prose and
their code is illustration. And §23's middle configuration layer, `config/*.yaml` between code
defaults and `.env`, is not implemented: no such file exists yet, and the task that introduces the
first one is where the loader for it belongs.

### D-039 · CI installs gitleaks from a pinned release, and the nightly runs only what exists — 2026-08-06

T-004 built the three workflows of §30. Four things had to be settled, and the constraint behind all
four is the same: the repository is public, so a fork's pull request must never be able to reach a
secret.

**gitleaks is installed from its pinned release tarball, not from the marketplace action.** The
official `gitleaks/gitleaks-action` requires a licence key for organisation-owned repositories, and
a licence key is a secret — which is exactly what a fork-triggered run does not get. Wiring one in
would either break the scan on forks or, worse, invite `pull_request_target` to make it work. So CI
downloads `gitleaks_8.30.1_linux_x64.tar.gz`, verifies its SHA-256, and runs the same binary the
pre-commit hook runs. Renovate can bump the version; the checksum moves with it.

**The trigger is `pull_request`, never `pull_request_target`.** That is the whole of the "no secrets
to forks" control (§30). `pull_request` runs the fork's code with a read-only token and no
repository secrets; `pull_request_target` runs it with the base repository's secrets and would hand
a stranger the keys. No workflow in this repository reads `secrets.*` at all, so there is nothing
to leak even if the trigger were changed by mistake.

**CI runs `make check`, not its own list of commands.** §30's table names ruff, mypy and the unit
tests separately, and mirroring them as separate CI steps was the obvious reading. It was rejected:
two lists of the same commands drift, and the moment CI checks something the local gate does not,
`make check` passing stops meaning a push will pass. One step, one definition, and the pre-push hook
and the pull request cannot disagree. `uv lock --check` and the secret scan sit outside it because
neither belongs in a gate the operator runs a hundred times a day.

**`nightly.yml` runs `make check` and a full-history secret scan, and nothing else.** §30 puts the
CI smoke run, the conformance suite and the retrieval goldens in this file, but none of those
pipelines exists yet. Writing the jobs now would mean either skipped jobs that are green for the
wrong reason or a workflow that is red on the day it is created — and "never document a command
before it exists" (§32) applies to a workflow step for the same reason. The jobs arrive with the
pipelines, in phases C and D. What the nightly does add today is real: it builds without the uv
cache, which is the only place a clean-machine install is proved daily, and it scans the whole
history, which catches a key that was committed and then removed inside a single pull request.

**`web.yml` exists before `web/` does.** Its path filters mean it never fires today, and each matrix
leg checks for a `package.json` before doing anything, because `panel/` arrives about thirty days
after `web/` (§16) and a run that touched only the application that exists is a pass. The Node
version and the pnpm version come from the application's own `.nvmrc` and `packageManager` field
(§22), so the workflow never has to be edited to follow them.

### D-040 · The catalogue's shape — seven labels, ~540 tracks, and a staged floor — 2026-08-04

§38 has carried "the catalogue's shape" as an open decision since v9, and `PHASES.md` gates the
whole of phase F on it: **C5 cannot start without it.** It is closed here.

**Decision: seven labels · ~32 artists · ~68 releases · ~540 tracks, roughly 34 hours of music.**
Two flagship labels of ~215 tracks between them, four standard labels of ~250, one old-system import
house of ~45, and ~30 unaffiliated one-offs. Genre allocation across the eight canon forms, category
weights, duration bands, intro-ramp and outro proportions are all recorded in `music/COMMISSION.md`,
which is the working brief for the commissioned writer and sits outside the §32 cap in the same
class as `canon/COMMISSION.md` and `cast/COMMISSION.md`.

**Why the count is derived rather than chosen.** A 56-minute artist profile is 14 tracks by one
artist, so a profilable artist needs ~18 tracks, so two or three real albums. That single rule is
what turns "generate 500 songs" into "generate sixty albums", and every other volume falls out of a
programme in §10 that has to be makeable: a label retrospective needs a label with ≥3 artists and
≥40 tracks; an album story needs a cornerstone album of 12–14; `Night Record`'s "one year" needs an
anchor year carrying ≥25 tracks across ≥4 artists and ≥2 labels.

**The staged floor is the operative part, not the total.** Phase F ships on **140 tracks** — two
complete labels — because F's outcome is *one* music show whose host knows the discography, and
proving the pipeline on two labels before committing 400 more tracks to it is the whole point. The
archive (H) needs **450**. Below roughly **300** the cold-start relaxations in §8 fire on most hours
and log a warning every time, which is the real floor signal and is mechanical rather than a matter
of taste. Ongoing cost is **40–60 tracks a year** to keep the front end current as the in-world year
advances.

**What this does not decide.** The names of anything. Labels, artists, albums, titles and lyrics are
the operator's and the commissioned writer's, per `CLAUDE.md`. This entry fixes only the structure
and the volumes.

### D-041 · Canon says the music is current and popular; two era-names are demoted — 2026-08-04

`70-music.md` had two defects that only showed up when the catalogue was specified against it.

**First, an era-scheme that could shape every prompt in the station while never being sayable.** The
prose named the *Exodus Hymns* and the *Drift Songs*; neither ever entered the `## Canon facts` list.
Per `canon/README.md`, prose feeds the generated domain summary — shipped on **every call** — while
the fact list is the only route by which a specific detail reaches the microphone. So the two names
were steering the whole station toward departure-grief and long patient crossing pieces, and no
presenter could ever actually say either of them.

**Second, canon gave no basis for popular music at all.** Every passage was elegiac. A writer reading
only canon would produce a catalogue of solemn ballads, which is not a radio station.

**Decision: eight forms, all of them living.** The prose now says that only recent eras can still be
*heard* and that anything older reaches a listener as **repertoire rather than record**; a new section,
"What people actually put on", establishes that most listening is current, short and cheerful, that
songs are about someone far off, money, weather, a fight, a night out, and that the distances are
the setting and never the subject. **The settled worlds do not dance to their own founding.** Facts
18–25 added. The Exodus remains a great subject for *drama* — `65-arts.md` fact 4 — and fact 21
scopes the exclusion to songs so the two do not collide.

**Two premise breaks fixed in passing.** Listeners "called in" and requested songs, which the world
forbids — there is no instant communication; they now write in, and requests arrive by relay days or
weeks later. And the playlist held "music centuries old" as playable recordings, which contradicts
the repertoire repair; the oldest material now reaches air as performances made since.

**No fact was removed, renumbered or re-anchored**, so every `fact_key` is stable and nothing already
aired is orphaned. **The `music` domain summary will change**, which is the highest blast radius in
the system: `canon-check` pass 3 pins summaries and will block the push until it is reviewed. That is
the correct behaviour and is why this was done *before* the catalogue rather than after.

### D-042 · The retired presenters are out of canon — 2026-08-04

D-036 replaced eight inherited music DJs with six speech presenters. Canon still named three of the
retired ones: *Sera*, *Orin* and *Zhe* in `80-cosmos.md` prose, and *Zhe* in `06-gazetteer.md` — in
the prose **and in fact 8**. A fact reaches the microphone directly, so the station could have named
a presenter who does not exist, on air, as an assertion about its own staff.

Fixed. ES-447 is now known by the instruments left there, which is a better line anyway — the place
is defined by nobody being on it. `80-cosmos.md`'s passage no longer names anyone and no longer
frames them as "correspondents in the field": the dispatches now **arrive finished, because nobody
out there can be asked a follow-up question**, which repairs the same impossibility D-036 identified
in the cast. Fact 9's "DJs" became "presenters", and the file's three remaining prose instances
followed so it does not contradict itself.

**This is the fourth site of the inherited music-station framing** — after `cast/CAST.md` (D-036),
`core/` (D-035) and the standing observation D-035 records. The word "DJs" survives in five further
canon files and in `core/COMMISSION.md`; most are harmless, and `15-figures.md`'s "night-shift DJs
across the settled worlds" is correct, since those are *other* stations' presenters. One is not:
`51-observances.md` has presenters choosing what fills the relay-maintenance hours, which
`core/COMMISSION.md` states plainly is false — the schedule is fixed in config and presenters choose
nothing. That remains open. A `banned-entities.yaml` line carrying the retired presenter names would
make at least the cast half of this mechanical instead of a recurring discovery.

### D-043 · The catalogue is produced by slot cards, global constants and one voice per artist — 2026-08-04

No code exists yet, so C5 has to be runnable entirely by hand while producing artefacts that load
unchanged once `make music-sync` is built. The workflow is recorded as §12 of `music/COMMISSION.md`.

**Four decisions worth recording.**

**Two artefacts per batch that never merge.** A `catalogue.yaml` fragment, which is read into the
station and can reach the microphone, and a production sheet holding prompts, lyrics, persona ids,
model versions and dates, which nothing ever parses. This split *is* the enforcement mechanism for
§8's two vocabularies: real genre words — the ones that make the catalogue sound like pop and rock
rather than like a concept album — are legal in prompts and illegal on air, and keeping them in a
file nothing reads is what makes that hold.

**Stage 0 constants, decided once before batch 1.** The eight anchor years and the six-to-ten
recurring session players cannot be decided per batch. A year is only a `Night Record` if ≥25 tracks
land on it across ≥2 labels, and labels written independently scatter across eighty years and cluster
in none; a session player invented during batch 4 cannot retroactively have played on batches 1–3,
which §6 requires. Both were previously implicit and would have failed silently at batch six.

**One persona per artist, pinned by audition on the first album**, and an artist finished inside one
model version. An artist profile is 56 minutes of one artist; generating track by track yields
fourteen different singers and an unmakeable programme, and the failure is invisible until the hour
is assembled.

**The slot card is ten fields**, of which eight are transcription from §4 and §1 and only two — the
house style and the label's trouble — are a creative decision. That is the operator's entire input
per batch of ~100 tracks.

**The lock-in, which is open.** Losing an artist's persona means re-rendering that artist's **entire
catalogue**, not one track. This is identical in shape to the presenter voice-identity trap forced at
build step 13b, and it bites earlier and more often. Persona ids live in a vendor account rather than
in the repository, and there is no backup story; whether the audition take is archived locally as a
recoverable seed is undecided. **Related: 540 tracks at several attempts per keeper will span more
than one billing month**, so `licence_note` must record the period each track was actually made in
and the plan's commercial-use terms must be captured at the start of each month generated in — §18
makes that field mandatory and phase G's legal review is what reads it.

### D-044 · The music catalogue is a wiki with a record library inside it — 2026-08-07

D-040 fixed the catalogue's shape as ~540 tracks and treated the catalogue and the audio as the same
thing. **They are not, and that conflation was the mistake.** Real presenters reference far more
music than their station owns, and the thing that makes the overnight worth hearing is not the songs
— it is a presenter who knows who played bass, which label folded, and why the singer stopped
speaking to the drummer. Writing text is roughly a hundred times cheaper than generating and
auditioning audio, so the reference material should be several times larger than the library.

**Decision: three layers.**

| Layer | What | Window | Size | Audio |
|---|---|---|---|---|
| **A — Played** | the record library | last ~60 years | ~25 bands · ~55 albums · **500 songs** | yes |
| **B — Referenced** | records that exist in the world; the station does not hold them | last ~80 years | ~45 bands · ~140 albums · ~1,200 songs | no |
| **C — Historical** | musicians whose recordings are lost | 80–200 years back | ~30 figures, scenes, movements | none survive |

Roughly **100 named musicians, 195 albums, 1,700 song titles, and 500 of them recorded.** Layer A
carries full album stories and the one-fact rule; layer B gets a line per album and titles only;
layer C gets three sentences per figure and **no albums or track lists at all**.

**Layer C is the operator's two hundred years, and it does not contradict D-041.** Canon fact 22 says
recordings from beyond living memory do not survive — so going back two centuries means going back
to *documented history without audio*, exactly as pre-1900 music reaches us. We know who they were
and what was written about them; nobody has the record.

**A `playable` flag is now load-bearing.** A presenter may discuss any layer; the scheduler may only
select layer A. §8's `tracks.file_path` must be nullable and every rotation, chart and playlist query
must filter on it. **This is a code requirement, not a documentation one**, and it lands before
`rotation.py` is written.

**Consequence for ordering: the wiki needs no vendor account and no hardware.** `PHASES.md` gated all
of C5 on "after F's Suno account"; that is now only true of the audio half. The whole wiki — the
largest part of the work and the part the presenters actually use — can start immediately.

### D-045 · Band style cards replace voice personas — 2026-08-07

D-043 made a persona per artist "the single most important setting", on the grounds that a
56-minute artist profile is fourteen tracks by one band and a drifting voice makes the show
unmakeable. **That was overstated and is reversed here.**

**Three arguments against it, and the third is decisive.** The vendor's persona feature is a
similarity nudge rather than a clone and promises no accuracy. Personas live in a vendor account
rather than in the repository, which D-043 itself recorded as an unresolved lock-in with no backup
story. And the vendor has announced that **the current models will be deprecated** as licensed
replacements ship — so 500 tracks anchored to personas pinned to a retiring model is a bad bet on a
known schedule.

**Decision: every layer-A band gets a six-line style card** — voice, backing, instruments,
production, tempo range, exclusions — fixed for the life of the band and pasted into every prompt for
it, with per-song variation inside it. The voice line never changes between albums. The cards are
text, live in `music/production/`, survive model upgrades, and cost no audition step. Personas may
still be used opportunistically; **nothing may depend on them.**

**What this gives up.** Vocal timbre will drift somewhat between songs. That is accepted: the
station discloses hourly that it is machine-generated, and a band that is recognisably the same
*band* across an hour is what the format actually needs. If the pilot hour reveals otherwise, the
fallback is to build artist profiles as label or year shows instead — a scheduling change, not a
re-render.

### D-046 · The licence position is a perpetual commercial licence, not copyright — 2026-08-07

Checked against current public sources rather than assumed, because D-032 states that music is "the
operator's own material, not third-party" and puts `music/` under the repository's all-rights-reserved
terms.

**That is right about commercial rights and shaky about copyright.** A paid plan grants the right to
use output commercially, including streaming, for material generated **while the subscription is
active**. But the vendor remains the technical author and grants a perpetual licence to exploit; it
makes **no warranty that any copyright vests** in the output, and US law may not grant one for purely
machine-generated material. The station may broadcast and publish freely; whether it could stop a
third party copying a track is a separate and weaker question. **The all-rights-reserved statement
over `music/` may therefore assert more than it can enforce** — for the legal review at step 15, not
for a fix now.

**Litigation is live**: one major label settled and signed a licensing partnership in late 2025; two
others remain in active suit, with a summary-judgment hearing set for mid-2026.

**Three operational consequences, now recorded in `music/COMMISSION.md` §9 and `RUNBOOK.md` step 11.**
Rights attach at the moment of generation, so licence evidence is captured **per generation month**
as a dated PDF in `music/licence-evidence/`, not once for the project. Every song carries a
`licence_note` naming its period. And the licence period, generation date, model version and an
AI-generated marker are written **into the audio file's own tags** — the audio and the wiki will be
separated eventually, by a backup or a move or a hand-off, and the file has to carry its own
provenance.

### D-047 · The music brief is assembled by a make target, not by hand — 2026-08-07

The operator was assembling each genre's brief by copying between `COMMISSION.md`, `CONSTANTS.md`
and a label plan held in conversation. That is three files stitched by hand, eight times, and it is
where the thread was repeatedly being lost — the reported symptom was "I still have no idea how the
whole thing will work", which is a fair verdict on a procedure that exists only as prose.

**Decision: `make music-brief GENRE=<genre>` and `make music-check GENRE=<genre>`.** Each assembles
one complete, self-contained block and copies it to the clipboard: the whole brief, the fixed
points, and that genre's allocation, with nothing left to paste afterwards. The operator triggers
one command and passes one word.

**The allocation moves out of prose and into `music/plan.yaml`** — 500 songs and 25 bands across
eight genres and seven labels. Every number is arithmetic from constraints already fixed in
`COMMISSION.md`; none of it is content, so it is config in the sense §33 allows. `tests/unit/
test_brief.py` asserts the totals and, more usefully, that **every label ends with ≥3 bands and ≥40
playable songs** — the condition that decides whether a label retrospective can be made at all, and
one that is free to fix now and very expensive once 500 songs exist.

**No model is called.** The command concatenates files the operator owns and fills in fixed numbers.
The writing stays with the operator's writer and the checking stays in a second conversation,
because a writer marking its own homework always passes.

**A latent bug surfaced and was fixed.** The CLI callback validated configuration before *every*
command, so building a text brief demanded a filled `.env` and a mounted media volume — and
`version` was equally blocked. §23's gate exists to stop the *station* running mis-configured, not
to stop the operator writing content, so a `CONFIG_FREE` set now skips it for commands that read
only files already in the repository. This matters beyond convenience: D-044 makes the wiki
startable before any hardware exists, and the gate was quietly contradicting that.

**`pyyaml` is now a declared dependency.** It was already resolvable, but only transitively through
`pre-commit`, so importing it in `src/` worked by luck and would have broken a production install.
It earns its place regardless: `grid.yaml`, `models.yaml`, `catalogue.yaml` and `banned-entities.yaml`
are all YAML by design.

### D-048 · The lyric and style briefs are assembled from the wiki, not from the operator — 2026-08-07

D-047 automated the brief that produces a genre. The two steps after it were still manual: choosing
which songs to record, and telling the writer what each one should sound like.

**Choosing needs no step at all.** `playable: true` *is* the selection, decided when the genre was
written. There is no second pass in which songs are picked; the wiki already says which 500 exist as
audio and which 1,200 only exist as references.

**Two more targets, following D-047's pattern.** `make music-style GENRE=<genre>` asks for one style
card per layer-A band, built from the line-ups the writer already invented — so a card is written
against real players rather than in the abstract. `make music-songs ALBUM=<id>` assembles one
album's lyric brief: the record's story, the band's style card, and every playable song with its
mood tags and its existing fact. That last join is the point — **a song's fact is already true of
it, so the lyric must fit the fact**, and a lyric writer who cannot see the fact will contradict
what a presenter is going to say on air.

**`src/station/music/wiki.py` reads the writer's output back as typed objects**, and earned its place
immediately: it rejected three real shape mismatches on the first genre — `movement` given as a
mapping recording a change of sides, `section` as a header block, and label ids given as numbers in
one file and slugs in another. All three are *correct* things for a writer to have written, so the
models now accept them rather than the wiki being made to conform. The one field that was genuinely
over-specified — `section`, which nothing reads — was deleted instead: declaring fields nothing uses
only creates ways for a valid wiki to be rejected.

**A test was wrong and was fixed rather than the code.** `test_check_brief_refuses_when_the_genre_has_not_been_written`
asserted against the real repository and started failing the moment the first genre was actually
written. It now builds a temporary root, so it tests the behaviour rather than the state of the
working tree.

### D-049 · A ninth form, deck-talk; the palette is modernised; the movements are demoted — 2026-08-08

The operator's reality check on the catalogue: is it boring, is Core Harmonies too heavy, and where
is anything resembling the dominant popular music of the present day. Three findings, of which the
first is the one that mattered.

**The palette had no rhythmic spoken form, and that dated the world to about 1985.** The eight canon
forms mapped to pop, rock, rockabilly, blues, dance, torch, choral and folk ballad — a record
collection that stops before hip-hop exists. Over six centuries a form built on spoken rhythm over a
beat is *more* likely to survive than choral music: it needs one voice and something to hit, and it
travels. Its absence was a hole, not a choice.

**Canon had already built the derivation without anyone noticing.** `70-music.md` gives the Freeholds
percussion made from survival — oxygen-tank drums, stripped-wire chimes; `35-economy.md` gives
Clearing Day, where *"the old ledgers are **read aloud** one last time and struck through"*; and the
Embargo left Freehold workshops with rough self-built industry "worn with enormous pride". Salvage
drums, a ceremony of reciting a list aloud, and competitive pride in what you made yourself.

**Decision: `deck-talk` is the ninth form** — rhythmic spoken verse over salvage percussion, born on
the station decks and in the Freehold workshops, where counting turned into competing and the
admired skill is carrying a long list furthest without dropping the beat. Canon facts 26–28 added;
fact 19 and the "what people actually put on" prose updated to name it among the forms carrying most
listening. At **70 songs it is the second-largest form in layer A**, which is the point: it is not a
curiosity. The name was chosen over "tally" — which collides with *The Count* on air — and over
"lane-talk", which would wrongly imply freight lanes.

**Relay-pop's palette was sixty years old.** Canon calls it "the young form"; the brief described it
as "girl-group and Merseybeat shapes". A 2626 teenager listening to 1963-shaped pop is exactly the
museum effect the catalogue is supposed to avoid, so the palette now reads contemporary produced
pop — big groups, several vocalists trading lines, sharp production. **No canon change was needed**;
`72-celebrity.md` already carries the fandom machinery. The governing principle, stated once here:
**retro setting, contemporary music.** The world is imagined the golden-age way because that is the
tribute; the music is the one thing in it that has to sound alive.

**Core Harmonies and Void Ballads were not the problem the operator thought, but the wording was.**
At 55 of 500 they were 11% — a spice level. But "gospel mass" and "drone underneath" read as organ
music when the intent was wall-of-sound vocal pop and one voice close to a microphone. Palettes
retuned, and both trimmed — to 15 and 10 — taking the difficult share to 5%.

**The three movements are demoted from "the richest source of presenter talk" to biography.** That
claim was mine and it was wrong: it invited a wiki in which every band is a philosophy seminar, and
it contradicts `SPIRIT.md` R1, which says interest comes from concrete stakes rather than
meditation. Purist/Synthesist/Localist now explains a split, a sound or a sacked player, and nothing
more. **This is the change that would have quietly made the overnight sound like a lecture.**

**Consequence: `relay-pop.yaml` was written under the old palette** and needs a revisit. Cheap now —
it is text, and no audio exists.

**`CONSTANTS.md` stopped duplicating the plan.** Its tally tables carried planned figures already
held in `music/plan.yaml` and enforced by tests; the planned columns were removed and replaced with
a pointer, leaving only the running count of what has actually been written. Two copies of a number
are one copy too many.

### D-050 · The album listing, and `py.typed` — 2026-08-08

Two small corrections, both found by the operator running the thing rather than reading about it.

**`make music-songs ALBUM=<id>` had no way to discover an id.** The ids exist only inside the wiki
YAML, so the first question after building the command was "what do I put there, and how would I
know". `make music-albums` now lists every album across every written genre with its id, band, year
and playable-song count, and **a column saying whether that band has a style card yet** — which is
the actual precondition for `music-songs` producing anything useful. A tool that requires an
identifier must also be able to produce the list of identifiers; that is not a convenience.

**The package never declared itself typed.** `station.music` is a new subpackage, and mypy resolved
it from the *installed* distribution rather than from `src/`. Under PEP 561 an installed package is
untyped without a `py.typed` marker, so the import failed type-checking — but only in the pre-commit
hook, never in `make check`.

**The two gates were not running the same command, and that is the finding worth keeping.**
`make check` runs `uv run mypy` and takes `files = ["src", "tests"]` from configuration; the hook
runs `uv run mypy <changed files>`, and passing filenames *overrides* that setting. Same tool, same
version, different scope, different answer — so a defect could pass the gate the operator runs and
fail the gate that runs itself. `src/station/py.typed` fixes the immediate cause. Making the hook
pass no filenames would remove the divergence entirely, and is not done here: at ten source files
the whole-project run is under a second, so the per-file optimisation buys nothing, but changing a
hook is the operator's call.

### D-051 · The album listing shows both layers; lyrics and style cards live in git — 2026-08-08

**`make music-albums` was showing layer A only, which is a minority of the discography.** The model
behind it declared just `layer_a`, so twenty of relay-pop's thirty-one albums were invisible to the
tool that exists to answer "what albums are there". Layer B is the larger half by design (D-044) and
is exactly the material a presenter reaches for, so a listing that hides it hides the point.

Fixed, and it surfaced a shape difference worth recording: **layer A lists albums beside the bands
and points back with a `band` field, while layer B nests each album inside the band that made it.**
Both are natural YAML and both occur in the same file. `Album.band` is now optional and the band is
recovered from the nesting.

The listing gains an **L** column (A or B) and a **PLAY** column (how many songs become audio, always
0 for layer B), and **`make music-songs` now refuses a layer-B id** with a message that says why
rather than "not found" — the failure the listing itself invites.

**Lyrics, prompts and style cards are committed text, and that is deliberate.** They go to
`music/production/lyrics/<album>.yaml` and `music/production/styles.yaml`, both tracked. The vendor
is a renderer, not a store: with the words and the prompt in git, changing one line of one song a
year from now means regenerating that one song, and a lost account costs audio rather than work.
Only `music/audio/` and `music/briefs/` are ignored — generated bytes and derived briefs.

### D-052 · `TASKS.md` runs at 11 items while the music track is planned — 2026-08-08

§33 caps `TASKS.md` at ten and says "to add one, ship or remove one". The music work needed three
cards — the id-and-check fix, the eight remaining genres, and the pilot — and only one slot came
free, because the pilot is a rewrite of T-015 rather than an addition. The operator was offered a
card to park and **chose to run at eleven instead.** Recorded here so it is a decision rather than
drift: the cap is the anti-sprawl mechanism (§34) and a file that quietly grows past it has stopped
being one.

**It closes by shipping, not by pruning.** T-004 ships and the file is back at ten.

Two things the planning session settled, worth keeping:

**The wiki is written horizontally, production vertically.** One genre at a time for the writing,
because ids and the used-names list are sequential and the second genre written today would reuse
`al_001`. Then one pass across all nine at once, because three of the rules — anchor years,
cornerstone count, session players spanning three labels — are properties of the whole catalogue and
cannot be checked a genre at a time. Only then lyrics, per album, because moving an album's release
year is free before songs exist against it and expensive after.

**The pilot is four albums, not a label.** T-015 asked for a complete flagship label, but
Concordance's 70 songs are spread across relay-pop, void-lounge and core-harmonies, and two of those
three are unwritten. Waiting for them would delay the only question the pilot exists to answer.
`al_001`–`al_004` — 45 songs, two bands, one label, already written — answers it now.

### D-053 · The music content track gets its own file — 2026-08-08

**Supersedes D-052.** That entry recorded `TASKS.md` running at eleven items to fit three music
cards. The operator's objection was the right one: three cards did not describe the job, and the
real sequence — tooling, nine genres, a pilot, 25 style cards, ~55 albums of lyrics, 500 Suno
generations, measurement and handover — is 42 cards that will never fit a ten-item window.

**`music/MUSIC_TASKS.md` now holds the whole music job and `TASKS.md` holds none of it.** `TASKS.md`
is back to eight items and its cap is intact.

This is a tenth document, against §32's cap of nine, **created by explicit operator instruction.**
Recorded here rather than argued: the cap exists to stop agents generating documents as a side
effect of work, and an operator asking for one directly is the case it was never meant to cover.

**Why one file rather than a ten-item window.** §33's cap is an anti-sprawl mechanism for work whose
shape is unknown — it stops the work generating more work. The music job is the opposite: its scope
is closed and arithmetic, fixed by `music/plan.yaml` at 500 songs, 25 bands and nine genres. Nothing
in it can generate more of itself. Showing a third of it at a time hid the sequence and cost the
operator the thread repeatedly, which is the failure the cap was supposed to prevent, arriving by
the other door.

**Three things the sequence settled, worth keeping:**

- **The wiki is written horizontally, production vertically.** One genre at a time for the text,
  because ids and the used-names list are sequential. Then one catalogue-wide pass, because anchor
  years, the cornerstone count and session players spanning three labels are properties of the whole
  catalogue. The wiki freezes there, before any lyrics — moving a release year is free until songs
  exist against it.
- **The pilot is four albums, not a label.** `al_001`–`al_004`, 45 songs, already written.
  Concordance's other 25 songs live in two unwritten genres, and waiting for them would delay the
  only question the pilot exists to answer.
- **`music/catalogue.yaml` is on the critical path, not a Phase F afterthought.** It is the only
  thing that turns the wiki into something a presenter can say. Without it the whole catalogue is
  inert, and that was not visible while the work sat in three cards.

### D-054 · The wiki is counted by code; the id counter is derived, not written down — 2026-08-09

**`make music-check` asked a model to count 105 songs across eleven albums.** A model that miscounts
and a wiki that is wrong produce the same reply, which makes the check worth nothing at exactly the
moment it matters. The countable half moves into `src/station/music/check.py` and runs inside
`make check`: a label whose playable songs do not match `music/plan.yaml`, a layer-A song with no
fact, a layer-B song that has one, a release year that is not one of the eight anchors, and any id
used twice. Each failure names the genre and both numbers. The half that is a judgement — whether a
bio reads well, whether an invented name is too close to a real one — stays with the operator and
with M-03's screen. Nothing here grades the writing.

**No new target.** The checks are unit tests over the real `music/wiki/`, so `make check` gains them
without the operator learning a command, and CI runs them on every push for free. A second target
would only be a second thing to remember to run.

**The id counter in `CONSTANTS.md` §4 is deleted rather than corrected.** It said `s_0001` while 265
songs existed — a hand-kept high-water mark goes stale the first time someone forgets it, and the
failure it causes is the one it exists to prevent: the second genre reusing the first one's ids.
The next free id is now derived from the wiki and printed at the top of every writer brief. Ids are
never renumbered (`COMMISSION.md` §10), so the high-water mark is the only possible answer.

**Labels, session players and band members are allowed to share an id across genres, and that is
not a loophole.** They are one entity appearing in several files by design — §6 wants a player
across three labels. A repeat is a collision only when two uses disagree about the name, which is
checked. Songs, albums, bands and lost figures may never repeat.

**The eight anchor years are read out of `CONSTANTS.md` §1 rather than copied into code.** The table
is the operator's, and two copies of eight numbers is one copy too many; if the table's row shape
changes, `make check` stops with a message saying so rather than silently finding no anchors and
passing everything. Note that `COMMISSION.md`'s checker prompt allows an off-anchor year "or a
stated reason" — the code allows none, per M-01's check line.

### D-055 · The paste loop is retired; the music track is worked in the repository — 2026-08-09

**Six music commands become two.** `make music-brief`, `music-check`, `music-style` and
`music-songs` are gone, with `src/station/music/brief.py` and the git-ignored `music/briefs/`.
`make check` and `make music-albums` remain. `RUNBOOK.md` no longer describes copying anything to a
clipboard, because nothing is copied anywhere any more.

**What the loop was for.** Every one of those targets concatenated files the operator already owns
— `COMMISSION.md`, `CONSTANTS.md`, a row of `plan.yaml`, a band's line-up — and put the result on
the clipboard so it could be pasted into an external chat. An agent working a card in this
repository reads those files directly. The brief carried no information the agent lacks, so it was
a transport mechanism for a workflow that has been replaced by `music/MUSIC_TASKS.md`: open a
session, say the card number, the file lands in git.

**M-02 depended on M-07 — the first agent-written genre — and was done before it.** The dependency
existed to prove the loop unnecessary. Nothing about relay-pop or lane-rock changes what the brief
contained, so the proof was not worth blocking on; git holds the deleted module if the judgement
turns out wrong.

**`plan.yaml` moves to `check.py` and `brief.py` is deleted rather than emptied.** `Plan` was the
only part of the brief module with a life after the briefs, and a module called `brief.py`
containing no briefs is how dead concepts survive. `wiki.find_album`, `Band.line_up` and
`Band.movement_line` went the same way: their only callers were the deleted commands.
`tests/unit/test_brief.py` is now `tests/unit/test_music.py`.

**What was lost, and is not.** The checker brief's twelve prose checks are not replaced one for
one: five of them are now `make check` (D-054), the name screen becomes M-03, and the rest —
"bios are plain speech, not lyrical", "no song is about leaving Earth" — were always judgements a
model marking its own homework passed anyway. They stay in `COMMISSION.md` §3 and §8, where the
agent writing the genre reads them, and they are checked by the operator reading the result.

### D-056 · The music name screen queries Wikidata live, and screens for people and organisations only — 2026-08-09

**M-03 asks the query service, it does not download the 1.5M-name extract.** D-014 specifies an
extract behind a bloom filter and a trigram table for §19's figure screen, and that is right for
that screen: it runs inside the nightly batch, on every figure the world tick proposes, and cannot
depend on somebody else's uptime. `make music-screen` is the opposite case — an operator command
run nine times in the life of the catalogue, on about 320 names a genre, where a stale extract and
the machinery to refresh it cost more than they save. One genre is seven SPARQL requests and under
a minute. If the two screens ever want to share code, the extract is the direction to move in, not
the query service.

**The rule is D-009's, unchanged**: exact match on the full name, entity with ≥5 sitelinks. What
this card adds is a type filter — the match only counts if the entity is a human or an organisation
(`wdt:P31/wdt:P279*` up to `Q5` or `Q43229`), with administrative and geographic entities excluded.
Without that exclusion every one-word title matches a village in Turkey, because administrative
areas reach `organization` through the subclass tree, and a report nobody can read is a screen
nobody runs. Places, films, species and songs sharing a name are therefore silent: the risk §19
names is an invented person or band colliding with a real notable one.

**Layer B is screened as hard as layer A.** A presenter says a layer-B title on air exactly as
readily as a layer-A one. Whether the record was ever made has nothing to do with whether its name
belongs to somebody.

**It is not a gate and `make check` does not run it.** It exits 0 whatever it finds, because every
finding is a judgement — replace the name, or record why it stays. What it must never do is print
an empty report when the endpoint was unreachable: that reads as "every name is clear", so a screen
that could not run raises after three attempts (§25) instead.

**Where it does not live.** The HTTP call sits in `src/station/music/screen.py`, not in
`providers/`. §3's two seams are the LLM and TTS; §21's rule is that vendor *SDKs* stay in
`providers/`, and this is 20 lines of `urllib` against a public endpoint with no SDK and no seam to
protect. If a second caller ever wants Wikidata — §19's screen is the candidate — that is the point
at which it earns a provider module.

### D-058 · `CONSTANTS.md` §3 records screen results, not a copy of every used name — 2026-08-09

Section 3 was written as *"the running names list — paste this into every Brief A"*, to be extended
after every batch. Writing lane-rock (M-07) is the first time that instruction came due, and it was
not followed. The section now keeps the eight session players and the canon four, and beside them a
table of what `make music-screen` returned per genre and when. The names themselves stay in
`music/wiki/<genre>.yaml`.

**Why.** The instruction is left over from the brief-and-paste loop, which D-055 retired. Its
purpose was to stop a writer with no repository access reinventing the same three surnames; an agent
working in the repository reads the genre files directly, and `make check` already fails on a
duplicate id. Copying 228 lane-rock names into a second file would add 550 names by the ninth genre,
each one a place the two copies can disagree, and nothing would read them — the same argument D-054
made against the hand-kept id counter, which is the failure this file has already had once.

**What is kept is the thing the files do not hold**: that a genre was screened, on what date, over
how many distinct names, and with what result. That is a fact about an action, not a copy of data,
so there is no second copy to go stale.

**Sections 5 and 6 were also brought up to date** in the same pass. They read 0 for every label and
every form while relay-pop had been written and screened, which makes a table nobody trusts. They
now count layer-A bands and playable songs actually in the wiki, and §5 gained the label's name as
written so the seven slots can be matched to the seven invented labels without opening nine files.

### D-059 · A layer-B band may carry no label, written as `label: unsigned` — 2026-08-09

Deck-talk's `Half a Shift` (`b_036`) presses its own records and has turned down every label. It is
written with `label: unsigned` on the band and on both of its albums, which is the first non-numeric
label reference anywhere in `music/wiki/`.

**Why it is allowed.** `COMMISSION.md` §4 says in terms that layer B and C artists "may belong to any
label, to a label that no longer exists, or to none", and §2 says deck-talk is the form that is cheap
to make and travels furthest. A wiki in which every crew in that form has a contract does not have
the form in it. The crew nobody's catalogue lists is the fact a presenter can actually say.

**Why it is safe.** `check.py` counts songs per label from layer A only (`_layer_a_albums`), so an
unlabelled layer-B album is never compared against `plan.yaml`, and `wiki.py`'s `label_number`
already returns `None` for anything that does not end in digits rather than failing. The count that
matters — 70 playable songs split 25 / 20 / 25 — is unaffected.

**The scope.** Layer A always carries a real label, because §4's floor of three bands and forty songs
per label is what makes a retrospective possible and an unsigned layer-A band would be forty songs
nobody can programme. This is a layer-B affordance and nothing else.

### D-060 · `MUSIC_TASKS.md` is ordered by dependency; the M- numbers stay identities — 2026-08-09

The file was written grouped by *kind of work* — tooling, wiki, pilot, style cards, lyrics, audio,
measurement — and numbered straight down that grouping. The dependencies run across the grouping,
so the two could not both hold, and it was the dependencies that gave way:

| Card | Printed at | Actually needs | Consequence |
|---|---|---|---|
| M-04, M-05, M-06 | 4–6, top of file | M-18 | three tooling cards at the top that cannot run until the pilot is generated |
| M-02 | 2 | M-07 | resolved by doing it early (D-055), but the inversion stayed on the page |
| M-16 … M-19 | 16–19 | only M-01 | **the decision point parked behind seven wiki cards it does not depend on** |
| M-40 | 40 | M-18 | its own note says do it at the start of the first generation month |
| M-30 … M-38 | after all of M-21 … M-29 | one lyrics card each | M-30 needs M-21, not M-29 |

The operator hit this directly: reading top to bottom made M-05 look like the next card, and it is
blocked behind four others and an unwritten metadata block.

**The file is now printed in dependency order and the numbers were left alone.** `M-05` names one
card for the life of the project — four commit messages, six references in `RUNBOOK.md`, seven in
this file, plus `styles.yaml`, `check.py`, `wiki.py` and `test_music.py`. Renumbering would make the
git history point at different cards than it did on the day it was written, and commit messages
cannot be edited. `TASKS.md` already resolves this the same way — *"numbers are identities, not
order"* — so the music file now says it too, and the card to work is the one marked **NEXT**.

**Two things changed besides the order.**

**The pilot moved ahead of the wiki.** M-16 depends on M-01 alone and the pilot uses relay-pop's four
albums, which were written before any of this. So M-19 — the project's only quality gate — was
reachable the whole time and was scheduled nineteenth. It now comes fifth. Stage 2's wiki cards are
all `[agent]` and M-18 is `[you]`, so the seven remaining genres get written *during* the Suno
sittings rather than before them, which is what the `[you]`/`[agent]` split in *Who does what* is
for. Writing 330 more songs of text before knowing whether the approach sounds right is the risk the
pilot exists to remove.

**Lyrics and audio are paired per genre.** A genre goes lyrics → audio → measured before the next
begins, because M-30 depends on M-21 and on nothing else. M-39 already asked for this in its own
note — *"run after each genre's audio lands rather than once at the end"* — and could not get it
while every audio card was printed after every lyrics card. A take distribution that misses
COMMISSION §7 is now found at 60 songs instead of 455, and the fix for that is choosing different
takes, so finding it late is finding it useless. Generating one band per sitting (§9) is unaffected:
the pairing decides which genre you sit down to, never how a band is made.

### D-061 · Where the wiki does not fix a lead singer's voice, the style card does — 2026-08-09

M-16's five voice lines are fixed for the life of each band (`COMMISSION.md` §7), so each one had to
be decided now rather than at generation time. Three of the five were already decided: `relay-pop.yaml`
uses female pronouns for Vara Ennel (`b_001`), Sena Quill (`b_002`) and Nara Veck (`b_003`), and a
style card that contradicted the wiki would put the presenter and the record in disagreement.

**Ressa Morn (`b_004`) and Mela Jorn (`b_005`) carry no pronoun anywhere in the wiki.** Their cards
read *male lead* and *female lead* respectively. Cabin Treaty takes the male voice because its
signature is the whole-crew unison chorus and five female leads in a row is one relay-pop voice
wearing five band names — §2 makes this genre 105 songs, the largest in the catalogue, and the
station plays them in the same hour.

**This is a production decision, not a wiki edit.** Nothing was written into `music/wiki/`, and
`styles.yaml` never reaches the air (§8). It is reversible for exactly as long as no audio exists:
`b_004`'s songs are generated at M-30, in stage 5, behind M-15, M-19, M-20 and M-21. If the operator
hears Ressa Morn differently, the fix before then is one word in one line.

### D-062 · The per-album lyrics file, and where M-18's generation metadata lives — 2026-08-09

M-17 was asked to fix the shape of the block M-18 fills in at Suno and M-05 later reads into the
audio files' own tags. It is **one `generation:` block per album plus one `take:` block per song**,
and the resolution rule is: M-05 reads the song's `take:` first and falls back to the album's
`generation:` for anything null there. A band generated in one sitting — which `COMMISSION.md` §9
asks for, because a band split across two model versions will not sound like one band — fills the
album block once and leaves the song blocks carrying only `attempts`. Per-song fields exist for the
song that had to be regenerated three months later against a newer model, which is the case that
makes a single album-level record wrong.

`al_001.yaml` carries the full field-by-field description of the file and the other three point at
it. Every lyrics file from M-21 onward uses this shape.

**The style card's production line is the one line an arrangement note may bend; the voice line is
never bent.** `al_001` was recorded in a small committee chamber and `b_001`'s card says *large
reflective hall*, because the card was written from the band's later records. The prompts ask for
the room the wiki states and leave voice, backing, instruments and exclude untouched — which is what
§7 means by *"then per song, inside that card"*. The same applies to the second half of `al_002`,
which the wiki says was mixed in a smaller room and audibly differs.

**No test was written.** §29 lists five kinds and none covers a hand-written content file that no
code reads yet; the counts, the id and title agreement with the wiki, and the §7 distributions were
checked with a throwaway script rather than a committed one. `make music-analyse` (M-04) measures
the real ramps and durations once audio exists, and M-39 is where the distribution is enforced.

### D-063 · Layer-A records made before 2592 carry no session players — 2026-08-10

Frontier Reels puts three layer-A albums in 2583 — `al_078`, `al_081` and `al_083`, twenty-six
playable songs. None of them credits a session player. The players appear only from `al_079` (2594)
onward, and the 2583 records are played by their four band members alone.

**Why.** `CONSTANTS.md` §2 is explicit that the eight session players are *one generation* who work
**2592–2626**, and that the old-standards window needs its own set of three or four elders,
commissioned separately as Brief 0b. That brief has not been written. The earliest date any player
carries is Oren Saye's 2588, and the rest start 2591–2596. Crediting any of them to a 2583 session is
the exact failure §2 warns about — "a batch will credit someone to a session they were eleven years
old for."

**Why it is not a hole.** §6 says to use the session players; it does not say every album has one,
and a first record made by four people in a rented hall with two microphones is the more likely
artefact anyway. The three 2583 albums are the band alone, which is what their notes describe.

**What it costs.** Frontier Reels is the first genre whose layer A sits mostly before 2592, so it is
the first to hit this. Every genre still to be written that aims at 2583 will hit it too —
old-system sessions (M-10) most of all, since §4 makes label 7 old and thin. Until the elders exist,
pre-2592 layer A has band members and nothing else, and §11's "every session player appears across
≥3 labels" is carried entirely by the post-2592 records.

### D-064 · Brief 0b is declined; the pre-2592 window keeps no session players — 2026-08-10

D-063 recorded that the three 2583 frontier-reels albums credit no session player, and left open
whether `CONSTANTS.md` §2's *elders* — the three or four players it reserves for the old-standards
window, as "Brief 0b" — would ever be commissioned. **They will not be.** The operator was given the
choice on 2026-08-10 and chose to leave it.

**What that settles.** A layer-A record dated before 2592 carries its band members and nobody else,
permanently. That is **33 playable songs across 4 albums** — frontier-reels `al_078`, `al_081` and
`al_083` (26 songs) and relay-pop's one label-6 album at 2583 (7 songs). §2 has been edited to say
so, because a working file that reserves a brief nobody intends to write is how a later agent comes
to invent a cast member to fill it.

**Why it costs nothing measurable.** All four albums are debut records made by young bands in
borrowed rooms, which is precisely where hired players would not be. §11's requirement that every
session player appear across ≥3 labels inside their active years is carried entirely by the 282
songs on 2592-or-later records and passes today.

**Why it will not grow.** COMMISSION §3 wants half the catalogue inside the last eight years: 250
songs on 2619 and 2624, of which 144 are written, leaving 106 of the remaining 185 songs pinned to
those two years. The five genres still to write are under pressure toward recent releases, not old
ones — and old-system sessions, the genre that reads oldest, is by §3 and §10 a set of *current*
releases that took a season to arrive and must never be presented as archive. The 33 is close to the
final number.

### D-065 · Old-system sessions credits no session player, permanently — 2026-08-10

`CONSTANTS.md` §2's eight players work in the settled worlds. Every record in
`music/wiki/old-system-sessions.yaml` was cut on Mars, Titan or Europa, by people who have never
been down the road, and COMMISSION §2 defines the whole genre that way — *current releases arriving
down the longest relay road from Earth's home system*. So the genre's `session_players:` block is
empty and stays empty: **60 playable songs across 7 albums with no hired credit on any of them.**

**Why not commission a home-system set.** That is Brief 0b again, and D-064 declined it. A second
roster invented to fill a gap is exactly the failure that decision closed, and it would buy nothing
§6 asks for — the rule is that *each player* appears across ≥3 labels, not that each label has
players. Nothing in §11's checklist goes red.

**What replaces it.** The genre's three layer-A bands guest on each other's records: Tel Brask of
Undershore Local plays harmonica on the Mars record, Saira Dunn plays piano on the Titan one, Amon
Furlow crosses from Mars for the Shore Rounds' EP. Same effect as a session roster and truer to the
world — the home system is dense and connected, and it is the road *out here* that is long.

**Two permanent holes now.** D-064's pre-2592 window (33 songs) and this (60). Together that is 93
of 500 playable songs with band credits only, and both are stable rather than pending.

### D-066 · Label 7 is Relay Road Import, and `release_year` there is the year it was *imported* — 2026-08-10

Three conventions were fixed writing M-10, all of them binding on every later card that touches
label 7 — M-06's catalogue, M-20's style cards, M-25's lyrics.

**The name.** Label 7 is **Relay Road Import**: two people, a rented press at the road head, one
shipment a year, and a catalogue it did not make. §4 asks for a label in trouble and this is it.

**`release_year` is the issue year, not the cut year.** A record cut on Mars in 2623 and sold at the
road head in 2624 carries 2624, and its notes name 2623. This is the only genre where the two
differ, and it has to be the issue year because the anchor years are years in which *the settled
worlds* saw a lot of records — that is what `Night Record` plays. Both dates are sayable facts and
the album notes carry them.

**Layer B uses `label: not imported`.** Two of the five layer-B bands are records that exist in the
home system and never came down the road at all — a distinction only this genre can make, and the
most useful thing its layer B does. `check.py` reads labels on layer-A albums only, so the string is
free text there and nothing counts it.

### D-067 · The eighth and last cornerstone is `al_117`; the list is closed — 2026-08-11

COMMISSION §5 wants **6–8 cornerstone albums of 12–14 songs**, one per album-story hour. Seven
existed before M-11. Pulse-dance designates the eighth — `al_117` *The Long Cordon*, Cordon Hours,
2624, thirteen songs — and **that is the last one the catalogue gets.**

**Why pulse-dance gets one.** Every genre of comparable size already has one or two: relay-pop 2 in
105 songs, lane-rock 2 in 75, deck-talk 1 in 70, frontier-reels 1 in 65, old-system sessions 1 in
60. Pulse-dance is 60 songs and 12% of the played catalogue. Leaving it without one would be the
single largest form in the library that cannot carry an album-story hour, and the album-story is one
of only five programme formats §5 defines.

**Why it closes the list.** Eight is the ceiling, not a target with room above it. The three genres
still to write are void-lounge (40 songs), core-harmonies (15) and void-ballads (10) — the whole
remaining catalogue is 65 songs, and none of the three needs an hour built on one record. Label 6's
programme is the **retrospective** built out of its disputed catalogue, which is a label hour and
not an album hour, so M-12 loses nothing by having no cornerstone available.

**What this binds.** M-12, M-13 and M-14 set `cornerstone: false` on every album they write. M-15
inherits eight and may move one, never add a ninth. Recorded in `CONSTANTS.md` §5 so the next agent
reads it before numbering anything.

### D-068 · The library becomes rock, blues, folk and jazz; deck-talk and pulse-dance stop being pressed — 2026-08-12

**The station's record library was 47% pop, hip-hop and house** — relay-pop 105, deck-talk 70,
pulse-dance 60 of 500 — and 54% of the 435 songs actually written. The operator does not listen to
any of the three. `PRODUCT.md` §9 makes *"does the world feel alive to its own operator at 90 days"*
a success metric and §11 names operator boredom as the most likely failure of the whole project, so
a library half-built from music he would never put on is that risk already realised, not a matter of
taste.

**The new split**, in `plan.yaml` and `COMMISSION.md` §2: relay-pop 105 · lane-rock 110 · Frontier
Reels 95 · old-system sessions 90 · void-lounge 55 · void-ballads 25 · core harmonies 20 ·
deck-talk 0 · pulse-dance 0.

**Relay-pop keeps its size and changes its sound.** Its prompt palette moves from produced dance-pop
to power-pop, jangle, sunshine and soft rock. This was the cheapest large win available: the wiki
never names a real genre, so 105 songs change character through one table edit and no wiki entry
moves. It is also what saves the pilot — `al_001`–`al_004` are relay-pop, and rewriting the form's
size would have thrown away the four albums M-18 is about to generate.

**Deck-talk and pulse-dance stay in the world.** Both keep their canon, their bands, their albums,
their credits and their stories, and become layer B — records the world knows about and the station
does not hold. `COMMISSION.md` §1 designed exactly this: *"most of the music you invent will never
be recorded, and that is correct."* Two reasons beyond taste, and they are independent: competitive
spoken verse over salvage percussion is the least leave-it-on music there is, and `PRODUCT.md` §5
puts music overnight only for background listeners; and it is the hardest form for a generator to
produce without the result being unintentionally funny — 14% of the library on the riskiest form.

**The canon edit came first and is already made.** `70-music.md` line 24 and fact 19 now name
lane-rock, Frontier Reels and old-system sessions as the most-listened forms; fact 28 and the
deck-talk paragraph drop the claim that it travels furthest, replacing it with a positive reason it
*doesn't* — a verse that could only have come from its own deck. Nothing else in `canon/` needed
changing: `06-gazetteer.md` states only where pulse-dance was born, which stays true.

**What it costs.** 130 written layer-A songs demote (their facts are deleted; everything else
survives), 95 new ones get written across three finished genre files, and two labels break §5's
floor. Label 2 falls to two bands and is repaired by M-48. **Label 3 is the real casualty** —
Meridian's house is left with 20 songs and one band — and it takes void-lounge's Meridian share
instead: a Synthesist core house pressing late-club torch, with its dance records still in layer B.

**One tension is kept on purpose.** Canon fact 19 now ranks old-system sessions among the three
most-listened forms while `COMMISSION.md` §4 keeps its import house *"old, thin, precarious"*. The
most-loved music in the settled worlds arriving on the most fragile route is what fact 17 already
implies, and it is a better permanent stake for the station than making the house comfortable.

**Cards:** stage R — M-43 (re-weight) · M-44 (demote) · M-45 (the writing rules in `make check`) ·
M-47 (redo the pilot's lyrics) · M-46, M-48, M-49 (the three genres grow). M-18 now depends on M-47
rather than M-17. M-15 gains four catalogue-wide jobs. **M-12 loses its NEXT marker** — void-lounge
grows from 40 to 55 and writing it first would mean writing it twice.

### D-069 · Where the re-weight's 130 songs go, and the `owed_to:` marker — 2026-08-12

D-068 fixed the nine genre totals. M-43 had to turn them into `plan.yaml`, which allocates by
**label**, and two constraints did the deciding: 500 songs and 25 bands, and COMMISSION §5's floor
of **≥3 layer-A bands and ≥40 playable songs on every one of the seven labels**. Three of those
labels lost a band when deck-talk and pulse-dance stopped being pressed.

**The four new bands.** Lane-rock takes a fifth on the hauler co-operative, Frontier Reels a fourth
on Cold Harbor — which is where label 2's third band comes back — old-system sessions a fourth
importer, and **void-ballads a second solo voice**. The last is the least obvious: 25 songs of one
voice and one instrument from a single artist is one texture, and §5's rotation rule separates by
band, so the form arrives on air as the same record twice a night. Two voices cost nothing to write
and fix it. Everything else grows inside bands that already exist.

**Void-lounge leaves Concordance and takes Meridian instead.** It was 10 songs on label 1 and 30 on
label 6; it is now 25 on label 3 and 30 on label 6, and label 1's third band comes from
core-harmonies, which grows to 20. That is what D-068's *"Meridian takes void-lounge's share"* costs
elsewhere, and it is a better trade than it looks: void-lounge on the prestige core label was the
one place it was competing with a genre that label already owns.

**Nobody's floor is met by accident.** Concordance 65 songs / 3 bands · Cold Harbor 85 / 5 ·
Meridian 45 / 3 · Forge 75 / 3 · the haulers 95 / 4 · the folded house 45 / 3 · the importer 90 / 4.
The two thinnest, Meridian and the folded house, are both finished by **M-12 alone**, which is why
that card now carries four bands and a note saying so.

**The `owed_to:` marker, and why the count check needed one.** `plan.yaml` now describes a catalogue
that five written genre files do not match — lane-rock is 35 songs short, Frontier Reels 30,
old-system sessions 30, and deck-talk and pulse-dance are 130 songs too many until M-44 demotes
them. `make check` had to stay green through that without the counting quietly going away for
weeks. So a genre may carry `owed_to: M-46`, naming the card that closes the gap; while it stands,
`check.py` does not count that genre against the plan — **and it goes red the moment that card is
marked DONE in `MUSIC_TASKS.md`, or if the card does not exist.** The marker and the card have to be
retired in the same edit, which makes removing it part of the growing card rather than a tidy-up
nobody owns. It is the same principle as M-45: the rules that survive are the ones that go red.

### D-070 · What "demote to layer B" actually did — and the cornerstone list falls to six — 2026-08-12

M-44 said *demote deck-talk and pulse-dance to layer B* and *nothing is deleted*. Three things had
to be decided to carry that out.

**The five bands moved with their records.** Read It Back, The Long Tally, The Wake Count, Cordon
Hours and Bright Hazard are now layer-B bands, sitting beside the crews that were always layer B,
and their sixteen albums sit under `layer_b.albums` pointing back at them by `band:`. The
alternative — leaving them in layer A with unplayable songs — is what a band that has records but no
recordings would look like, and there is no such thing: layer A *is* what the station holds. Both
files now open with `layer_a: {bands: [], albums: []}` and a comment saying why.

**The song facts went; everything else stayed.** 130 `fact:` lines are gone, because a fact is the
one sentence a presenter says over a record that is playing and there is no record to play. The
bios, the album stories, the credits, the mood tags, the release years and every title are untouched
— 182 deck-talk songs and 140 pulse-dance songs still exist as text, which is 322 titles a presenter
can name and 24 + 16 albums they can tell the story of.

**`al_055` and `al_117` stop being cornerstones, and the list falls from eight to six.** D-067 closed
the list at eight; two of those eight were in the demoted genres. A cornerstone is an album that
carries a whole 56-minute programme, so a record the station does not hold cannot be one — leaving
the flag set would have put an album with no audio in front of the operator building a *Night
Record*. §5 allows 6–8 and six is inside it, **with no margin under it**. D-067's instruction to
M-12, M-13 and M-14 is unchanged: they designate none. Whether the two freed slots go to a later
genre is the operator's call and is not made here.

### D-071 · The writing rules move into `COMMISSION.md` §12, and a rule may be owed to a card — 2026-08-12

M-45 asked for eight prose rules and `make check` enforcing them, and said *"green on the wiki as it
stands."* Measured against the repository, three of the eight cannot be green today and one of them
contradicts a rule already in force. Three things were decided to carry the card out.

**§12 is where the rules live, and it is the only part of `COMMISSION.md` a machine reads.**
`writing.py` takes the eight thresholds, the album floor, the world-noun list and the
studio-anecdote vocabulary out of §12's tables rather than keeping a copy, and stops with a message
naming the table if one changes shape — the same arrangement as the anchor years in `CONSTANTS.md`
§1. The alternative, numbers in code and numbers in the writer's brief, drifts inside a week, and
the writer's copy is the one that gets read. The rules themselves are separated from `check.py` into
`writing.py` because `check.py` is the counting of identity and arithmetic and would have gone past
§31's 400 lines besides.

**A rule may be owed to a card, exactly as a genre may be** (D-069). Rules 1–5 read
`music/production/lyrics/`, where the only file is the pilot's 45 songs, and all four albums fail
four rules apiece — which is not news, it is the finding M-47 was written to fix, and M-47's own
check already reads *"all 45 pass M-45's rules."* Rules 7 and 8 are properties of the whole
catalogue that no single genre can satisfy, and M-15's job list states both of them in words. So §12
carries an **Owed to** column: the rule is counted and reported, and it becomes fatal the moment the
card it names is marked DONE. **Marking M-47 and M-15 done today turns `make check` red with twenty
named findings**, so the deferral cannot outlive the work and cannot quietly become permanent.

**Rule 7 replaces a rule rather than adding one.** `check.py` required every album in both layers to
sit on an anchor year, which is why all eighty layer-B albums sit on eight of them and two hundred
years of music history happened on eight days. Rule 7 asks layer B for forty distinct years instead,
and the two cannot both hold. `year_layers()` keys the swap to M-15: until it lands the anchors bind
both layers, after it they bind layer A and rule 7 binds layer B. There is no window in which
neither applies.

**What the rules found, and it is worse than the card assumed.** With the deferrals lifted, the
pilot's four albums report: one section structure across 9 of 12, 8 of 11, 11 of 11 and 8 of 11
songs; the echoed answer in 45 of 45; the song's own title as the hook in 41 of 45; and **not one of
the 45 lyrics carries two of the world's own nouns.** §3 asks the world to supply the furniture and
the swap-the-nouns test to be survivable; these lyrics would read unchanged on Earth, which is the
test passing so completely that it inverts. The wiki itself is green on rule 6 with **very little
margin** — the worst band sits at 10 studio anecdotes in 21 facts against a ceiling of half.

### D-072 · The answering voice stays, the parenthesis goes — 2026-08-13

M-47 rewrote the pilot's 45 lyrics against `COMMISSION.md` §12's rules 1–5. Rule 3 counts the echoed
answer — a parenthetical repeat inside a sung line — and M-17 had used it in 45 songs out of 45. But
the answering voice is not a tic: `styles.yaml` fixes *"three group voices answering the lead line
for line across the chorus"* as b_001's backing line, and b_002's is *"all four voices shouting the
hook together."* Deleting the device from the arrangement would have changed what both bands sound
like in order to pass a lyric rule.

**So the arrangement moved out of the lyric and into the section tag and the prompt.** A chorus is
now tagged `[Chorus - answers entering a bar early]` or `[Chorus - band stops dead under the title
line, whispered answer only]`, and the prompt says the same thing in production vocabulary. The
words in the lyric are the words that are sung; who answers them, and how, is the mixer's and the
engine's business — the same seam §3 draws for timing. `writing.py` strips bracketed tags before
counting, so this is not a way around the rule; it is the rule finding the right place to put the
instruction. Three songs an album keep the written parenthetical, because the device is good and it
is the failure mode that is bad.

**Two smaller calls fell out of the same rewrite.** No song title changed: titles are the wiki's,
`COMMISSION.md` §10 forbids renaming an id, and editing 45 titles to satisfy rule 4 would have
edited the wiki from the production side. So 25 of the 45 songs now take their title from an image
in the lyric and say something else in the chorus, which is what rule 4 was asking for anyway. And
every song's mood, fact, intro ramp, outro type and target duration was left byte-identical, so
§7's three distributions — which M-17 aimed rather than left to chance, and which land exactly — did
not have to be re-derived to fix the words.

### D-073 · Where lane-rock's 35 new songs went, and what it costs M-48 and M-49 — 2026-08-13

M-46 said 110 songs split 15 / 50 / 45 and named the shape — a short Second Hitch record, 15 between
the two Forge bands, a second hauler band on label 5 — and left the years and the split inside label
4 open. Both were decided against constraints outside the card.

**Pipe and Hammer take 8 of the 15 and their record is dated 2612,** because `CONSTANTS.md` §1 asks
M-46, M-48 and M-49 each to land a release on that anchor with a band not already on it: M-44's
demotion had left 2612 at 25 songs across 3 bands, one band short of a programme. The band already
owned the year — Saul Ravik left over the amplified pipes in 2612 and Ade Prosk replaced him — so
the anchor repair and the best untold story in the genre are the same record. 2612 now reads 33
songs / 4 bands / 4 labels, and **seven of the eight anchors are satisfied.** M-48 and M-49 are
released from that instruction; 2612 sits on the four-band floor with no margin, so landing there is
still worth doing and is no longer owed.

**The other 27 songs went to 2619 and 2624**, which is not a preference. COMMISSION §3 wants half of
layer A inside the last eight years; the catalogue stands at 161 of 340, 250 is the target, and the
remaining 160 songs must supply 89 of them — **56% of everything M-48, M-49, M-12, M-13 and M-14
write has to be dated 2619 or 2624.** M-11 recorded the rule as "only just reachable" and 27 of
M-46's 35 landing recent is what has kept it that way rather than worse: the
demotion took recent songs out, void-lounge's label-6 half cannot be dated past the 2612 fold, and
M-15's job 4 still has nothing later than 2624 to work with. Any card that spends a slot on an old
anchor for atmosphere makes the arithmetic worse for the ones after it.

**Turn and Burn's lead voice is female**, fixed here rather than by M-20, because `b_061`'s bio and
five of its facts use Rhea Molt's pronoun and §7 makes the voice line load-bearing and unchangeable.
Same call as D-061 and reversible on the same terms — until M-31 generates the band, nothing depends
on it.

### D-074 · Frontier Reels' 30 new songs, and the one band that could not make them — 2026-08-13

M-48 named the split — 45 / 25 / 25 across labels 2, 4 and 5, with a fourth band on label 2 — and
left three things open that the wiki as written had already half-decided.

**Label 2's fourth band is Suli Orley's, and she is the one player in the genre who could carry it.**
`b_062` Board and Bow are Cold Harbor's current reel band, formed in 2612 by the guitarist Wire and
Rosin hired off the dance floor in 2604 without an audition. A new band with no line into the
existing file would have been a fifth sealed world inside a sealed genre; this one inherits Wire and
Rosin's whole argument about halls that charge the dancers, and its two records are 2619 and 2624,
which is where the calendar needed them. **Her voice line needs no decision** — `al_080` already
uses her pronoun, so unlike D-061 and D-073 there is nothing here for M-20 to fix.

**Label 4's ten songs are a live issue, because The Foundry Set stopped in 2599 and that is fixed.**
The band's two anchors inside its own life, 2583 and 2594, are both already spent, and extending a
band that broke up over a named argument would have rewritten committed prose to buy a release year.
`al_136` *Played and Never Pressed* is instead ten dance tunes Orsa Lipp recorded for himself between
2591 and 2599 and Deep Register issued in 2619 with a sleeve crediting Dane Verrow throughout, which
Bree Hollan disputed on the strength of the four-way agreement she had forced in 2594 (`s_0675`).
That lands on 2619's own anchor story — the altered-credit edition, the reply records, the competing
versions — and it credits no session player, because nobody hires a fiddler for a dance they are
playing anyway.

**Label 5's five went to 2594 rather than to a recent anchor**, the only place in this card where
the half-recent arithmetic was spent rather than served. `al_085` is written as Loose Cargo's last
record and 2612 is their last year, so a recent release meant editing that line; 2594 is the first
burn-festival year and Loose Cargo are a hauler crew who played the dances at both ends of their own
route, so the record wrote itself and the year gained a fifth band. **The arithmetic still improved.**
25 of the 30 new songs are dated 2619 or 2624, taking the catalogue to 186 of 370 inside the last
eight years: the remaining 130 songs now need 64 of them to be recent, **49% against the 56% D-073
handed on.** M-49, M-12, M-13 and M-14 inherit a rule that is easier than they were promised.

**One line of existing prose was edited.** `b_044` The Turning Room claimed to be the only frontier
reel band still working, which Board and Bow makes false. It now says the two share the Cold Harbor
halls and that The Turning Room asked Suli Orley to join them first — a contradiction removed and a
rivalry gained, in the same sentence count layer B allows (§6).

### D-075 · Old-system sessions' 30 new songs all went to one new band — 2026-08-13

M-49 asked for 90 playable songs on label 7 across four bands, one of them new. **The three written
bands could not take a single song of the 30**, and that is a property of the file rather than a
choice. Every anchor year inside Terrace Road Four's and The Shore Rounds' lives is already spent —
al_099 is written as the first record one band made and al_100 as the first the other sent down the
road, so an earlier release contradicts committed prose, and both already hold 2624. Undershore
Local stopped in 2612 and al_104 is written as its last. The one device that would have freed a
release, an issue of unreleased material, is what COMMISSION §10 forbids for this genre by name:
*never present an old-system record as archive.* So all 30 songs and all four albums belong to
`b_063`, which makes the newest band the genre's largest at 30 songs, and that is the finished
state.

**The fourth band is from Earth, which no layer-A record had ever come from.** `b_063` The Ninefoot
Cut work the locks on eleven miles of Earth canal, and their first record reached the road head in
2607 because a clerk on Earth misread the address on a letter meant for the Bell Yard Rounds — the
band every account of the form gets round to, and the one everybody out here assumed the first Earth
import would be. **The argument about whether the importer landed the wrong band has run ever
since**, which is the permanent live stake the card asked for, sitting on top of the one canon fact
19 and COMMISSION §4 already hold in tension: the most-loved music arrives on the thinnest route.
An Earth record takes two crossings rather than one, so all four are cut two years before they are
issued, and the 2621 record only exists because its first copy was in the crate that went astray in
2622 and Fenna Crole had kept a second on the lock house shelf.

**Nobody guests on their records and nobody can.** D-065 fixed that this genre credits no session
player and that what carries it instead is the three bands guesting on each other; Earth is too far
for that, so the connection runs on paper and on repertoire — the importer sent a Shore Rounds
pressing up the road in 2619 with no name on the sleeve, the band spent a season working out whose
it was, and `s_1165` is that round sung with the four voices entering together where Titan enters a
line apart. It is the only record in the house's list on which anything went the other way.

**Two lines of existing prose were edited, both of them already false.** `al_098` claimed nothing
else came down the road in its season while `al_102` and `al_114` were both dated to that same
season, and it dated the near-closure as *"the year before"*, which §10 forbids outright; it now
names 2622 and says the house put the largest part of one crossing behind the record. `al_114`'s
*"the only import that season besides the Terrace Road record"* was the other half of the same
contradiction and now says it shared the season.

**16 of the 30 new songs are dated 2619 or 2624**, taking the catalogue to 202 of 400 inside the last
eight years. COMMISSION §3's half-recent rule now needs 48 of the remaining 100 — **48%, against the
49% D-074 handed on**, and the three genres left can supply at most 70 between them, because
void-lounge's 30 label-6 songs cannot be dated later than the 2612 fold. **Anchor 2612 gains its
margin**: it stood on §5's floor at 33/4/4 and reads 40/5/4, so no anchor now sits on the floor.

### D-076 · Void-lounge is one story told twice — the house that folded and the coast that took the form up — 2026-08-13

M-12 asked for 55 songs across two labels that had nothing in common except that stage R had left
both of them standing on almost nothing: label 6, which folded in 2612, and label 3, which lost its
whole layer A when pulse-dance went down to layer B. **They are written as one story rather than
two.** Lower Bell Editions existed for this form and nothing else and went under owing the Gantry
Street plant two years of pressing; Juna Carrow sang its second band, could not get the records
back, took a hall job on Meridian in 2617, and the season sealed with her on the coast — which is
why the most Synthesist house in the settled worlds started pressing the core's slow music in 2619.
**She is the only person in the wiki who is in two layer-A bands** (`b_065` Coldwater Court and
`b_066` The Quiet Half), and the crossing is what stops the two labels reading as two unrelated
allocations.

**The founder is in the band.** `p_maro_deyn` founded the house in 2589 out of the room his own band
had played for eleven years, borrowed against the catalogue in 2610 to buy that room, and lost both.
Relay-pop already said the founder has refused every catalogue interview since 2612; he now has a
name, a piano, and a last recorded figure played alone. It makes the fold a thing that happened to
five named people rather than an event in a label's history.

**Every label-6 song is dated 2612 or earlier and that was forced**, not chosen — a house that
folded cannot press afterwards. All 25 label-3 songs are therefore dated 2619 or 2624, which is the
most the card could give COMMISSION §3. The catalogue stands at **227 of 455 inside the last eight
years, one song under half**, and the remaining 45 need 23 of them recent — **51%, against the 48%
D-075 handed on.** It is the first time the share a card hands on has gone up rather than down, and
it is arithmetic rather than neglect.

**Nine Lamps refuse the name of the form they are filed under.** `b_067` play the last hour of the
coast's dance nights and hold that it grew out of those nights rather than arriving down the relay
from the core; Stormline Issue files them as void-lounge and prints their objection on the sleeve.
This is an argument inside the world and not a tenth form — COMMISSION §2's list of nine is
untouched, and the house's filing is what the wiki records. It gives a presenter a live stake in a
genre whose other three bands all agree with each other.

**What the numbers did.** Labels 3 and 6 both land on exactly 3 bands, 6 albums and 45 songs, so
**six of the seven labels now clear §5's floor and only label 1 is short** — by a band and two
albums, which is M-13. Anchor 2612 goes 40/5/4 → 52/7/4 on the house's last two records, and **2583
at 33/4/4 is now the thinnest anchor** and the only one still on the floor for bands and labels.
Rule 6 reports **zero studio anecdotes across all four bands**, the safest reading of any genre so
far; `make music-screen` returned nothing on 153 distinct names.

---

### D-077 · Core harmonies is Concordance's own argument about credit, and *Lanternlight* becomes playable — 2026-08-14

M-13 wrote `music/wiki/core-harmonies.yaml`: 20 playable songs on label 1 across three albums, one
layer-A band, Odessa Vail as the whole of layer B, and two lost figures. It finishes Civic Lantern,
which stood at 2 bands and 4 albums and is the last label that was short of §5's floor.

**Three albums rather than the two the card asked for.** Label 1 needed a third band and two albums;
a third album costs nothing at this stage and gives the house 7 albums instead of exactly 6. M-12
left labels 3 and 6 sitting on the floor with no margin and that was noted at the time as the
weakness of that card; this one had the room to avoid repeating it.

**The recency split is 14 of 20.** The three records are dated 2607, 2619 and 2624, and only the
first is old — it exists because the ensemble's first record has to come before the hall shut. That
takes COMMISSION §3's half-recent rule to **241 of 475, over half for the first time since the
re-weight**, and leaves M-14 needing 9 of its 25 recent, or 36%. The chain of shares handed on now
reads 56% (D-073) → 49% → 48% → 51% (D-076) → **36%**. The cost is that **2583 got nothing** and
stays the thinnest anchor at 33/4/4, on §5's floor for both bands and labels; M-14 is the last card
that can lift it, and `CONSTANTS.md` §1 now says so.

**Odessa Vail is written as a layer-B band with one member.** Canon fixes her and COMMISSION §4 puts
her in the deep end of layer B, so `b_073` is a solo entry whose single member `p_odessa_vail`
exists for one reason: the credits on the 2624 record have to point at a person id, and a composer
who is only a band cannot be credited as a writer. *Lanternlight* is `al_164`, 2559, twelve
movements, unplayable.

**Seven of those twelve movements are layer A.** COMMISSION §4 says later performances of the cycle
may be, and the 2624 anchor — Concordance's largest public hall reopening — is where one belongs.
The layer-A songs carry the same titles as the layer-B originals, because it is the same piece and
an id, not a title, is what identity means here. This is the first record in the wiki that a
presenter can play *and* attribute to a canon figure who never made another.

**The hall now has a name.** Four anchors' worth of records refer to Concordance's largest public
recording hall and no file had named it; it is **the Long Assembly**, and the band is named for its
standing rail. Naming it was additive rather than a correction — no existing line contradicts it —
and the ensemble's whole story is that room, so leaving it anonymous would have made three album
notes vaguer than the wiki can afford.

**What the band is for.** The Standing Gallery formed in the cheap standing rail of that hall out of
people who could not afford a seat, and their argument with Civic Lantern is about money and names
rather than about music: until 2619 the house paid a chorus a flat fee for a night, printed no
singer's name, and paid its hired players by the hour. The 2619 record prints all thirty-one, and it
happened in that year because the altered-credit edition had made refusing into a story. That is the
form's grandeur given a concrete stake, which is what COMMISSION §2 asks for and warns is usually
lost to a philosophy seminar.

`make check` is green including §12's rules, and **rule 8 is satisfied by this file already** —
it names Measure Kindly, Open Parallax, Pell and Tern and The Quiet Half, four bands that live in
other genre files, against the three the rule asks for. The rule stays owed to M-15 because five of
the other six written genres still name none. Rule 6 reads **2 studio anecdotes in 20 facts**.
`make music-screen` returned nothing on 43 distinct names.

### D-078 · The most-loved void ballad is one nobody may sell, and layer A exists because of it — 2026-08-14

M-14 wrote `music/wiki/void-ballads.yaml`: 25 playable songs on label 2 across four albums, two
layer-A bands, Corin Hale as the whole of layer B, and one lost figure. It is the last genre, and
**the wiki's layer A is complete at 500 songs, 25 bands and 55 albums.**

**Corin Hale is layer B, and the reason is permanent.** Canon fixes Hale — a lifetime on one relay
outpost, the *Station Cycles*, the life-support drone left unrepaired because it had become the
tonic note — and says nothing about who pressed them. This card decides that nobody did and nobody
can: Hale left the recordings to the outpost's rota under one rule the rota has never bent, *anybody
may copy them and nobody may sell them*. So what circulates is copies of copies, and the settled
worlds' most-loved record in this form is one no station's library holds. That is a stronger use of
layer B than the wiki has made anywhere else — COMMISSION §1 says most of the music invented will
never be recorded, and this is the case where the presenter's inability to play it *is* the story
rather than a limitation to work around.

**Both layer-A voices are consequences of that rule**, which is what stops a 25-song genre from
being two singers with nothing between them. In 2583 the Cycles reached general circulation, every
house wanted the form, and Harbor Standard was not allowed to sell the one record everybody wanted —
so it went to its own relay berth and recorded the gate clerk who sang to the night traffic. That is
`b_074` **Nera Ostell**, who has never sung a Hale song and is asked every time, and who in 2612 put
her name on a rota and went out to an outpost herself. `b_075` **Aro Vantry** built a box that holds
one note, the note is the Cycles' tonic, and he prints where it came from on every sleeve unasked —
which he first did in 2619, the year the whole industry was arguing about a credit. His 2624 record
was made at Hale's own outpost, where the plant had been replaced and the note was gone. **They have
never met and one will not answer the other.**

**Two solo voices, per D-069, and the file fixes both textures.** Ostell is a low voice and a
composite guitar strung with wire off a scrap yard; Vantry is a high one, a hand-pumped reed organ
and the drone box. M-16's D-061 showed what happens when a band's voice is left for the style card
to decide, so the pronouns and the instrument are settled in the bio here and M-20 has nothing to
choose. **Exactly one session player appears in the whole file** — Ivena Sorn, holding one note on
one song in 2600 — because COMMISSION §2's palette allows a held note underneath and nothing else,
and a second player would be a different form.

**2583 came off the floor and the recency rule closes satisfied.** The anchor stood at 33/4/4, the
thinnest of the eight and the only one on §5's band floor; Ostell's first record takes it to 39/5/4,
and 2600 gains a fifth label. 13 of the 25 songs are dated 2619 or 2624 against the 9 D-077 asked
for, so COMMISSION §3's half-recent rule **ends at 254 of 500 — 51%**, and the chain of shares
handed from card to card (56% → 49% → 48% → 51% → 36%) stops here. The two old records are old for
reasons in the story: Cold Harbor's first void ballad could only be the year the Cycles went round,
and its second could only be the year the shared press format let records travel.

**One line of `CONSTANTS.md` was wrong and is corrected.** §1 said Cold Harbor carried no 2583
release and used that to argue M-14 could lift the anchor; `al_078` — Wire and Rosin's *Nobody Sat
Down*, thirteen songs — has been a 2583 label-2 release since M-09. What was true is that the year
needed a fifth band, which is what it got. **No existing prose in any genre file was edited.**

`make check` is green including §12's rules. Rule 6 reads **zero studio anecdotes across both
bands**, and **rule 8 is satisfied by this file** — it names Wire and Rosin, The Turning Room, Board
and Bow, Loose Cargo and Harbor Late, five bands that live in other genre files. The rule stays owed
to M-15 because the other six written genres still name none. `make music-screen` returned nothing
on 44 distinct names.

---

### D-079 · Anchor 2559 stays an anchor and stays unplayable — 2026-08-14

M-15 asked which of two rules had to give. `COMMISSION.md` §3 puts layer A in 2566–2626, so no
playable song can carry 2559; §5 asks every anchor year for ≥25 playable songs across ≥4 bands and
≥2 labels. Both cannot hold. **Operator decision: §5 gives.** The year edition is built from the
seven anchors that carry layer A, all seven of which clear the floor with margin.

**Why not the other two options.** Widening §3's window to 2559 would mean pressing a record
sixty-seven years old, which contradicts §1's *"last ~60 years"* and would reopen a wiki this card
exists to freeze. Dropping the row would need `ANCHOR_COUNT` changed to seven and would delete the
year *Lanternlight* was premièred — the record Civic Lantern's entire standing rests on, and the
reason the other seven anchors have a calendar to be scheduled against at all.

**What it costs is nothing the station notices.** 2559 was always a layer-B year: `al_164` is the
première recording and `al_030` is Patient Weather answering it, and neither was ever going to be
playable. The way the year reaches the air is a later performance, which §4 has allowed from the
start — `al_163`, seven of the cycle's twelve movements, recorded in the reopened hall in 2624. So a
`Night Record` on 2559 is makeable; it is simply made out of 2624's record and the story, which is
what a programme about a year nobody has a copy of would be anywhere.

`COMMISSION.md` §5 and §11 and `CONSTANTS.md` §1 now say so in those words, so the contradiction
cannot be rediscovered and re-argued by the next card that counts the anchors.

### D-080 · The chart counts plays, not release years — 2026-08-14

M-15's fourth job: nothing in the catalogue is dated later than 2624 while the present is 2626, and
because the present is the real year plus six hundred, that gap widens every January. §5 asked for
*"≥80 songs current at any time"*, which reads as a standing commission for records dated this year.
**Operator decision: the chart is most-played, and §5's wording was the thing that was wrong.**

**ARCHITECTURE §8 already computed it this way.** The score is 45% decayed airplay, 25% in-world
requests, 20% previous position and 10% editorial nudge — there is no release-date term in it and
never was. So this decision changed two documents to match the code rather than changing any code,
which is the direction CLAUDE.md requires when the architecture and a rule disagree.

**The alternative was barred by rules already in force.** Giving a small tier a derived release year
— the `clock.py` rule applied to the catalogue — would date layer-A albums 2625 and 2626, which are
not anchor years, so `make check` would go red on every one of them; and §3 forbids inventing a
ninth anchor by name. It would also mean a release year that moves, which §3's *"write the year,
never the age"* exists to prevent.

**What it costs a presenter** is one sentence they may not say: a record is not new because it
entered the chart. *In at eleven*, *up four* and *a re-entry after nine weeks* all still work,
because they are facts about plays. An actual new release enters through the editorial-nudge term
and needs a beat behind it. `PROGRAMMING.md` carries that in the section on `The Count`.

### D-081 · Layer B gets the calendar, and three albums could not move — 2026-08-14

`COMMISSION.md` §12 rule 7, owed to M-15 since D-071, went live with this card. All 106 layer-B
albums sat on the same eight anchor years, so two hundred years of music history had happened on
eight days. 68 of them were re-dated across 2552–2626 and the wiki now carries **55 distinct
layer-B release years** against the 40 the rule asks for.

**38 albums stayed on an anchor, and that is the point rather than a shortfall.** §3 still says
*put most releases on the anchors*, and a layer-B record keeps its anchor whenever the anchor's own
event is its story: the fold took `al_053`, `al_128` and `al_158`, the burn festival took `al_044`,
`al_066` and `al_155`, the shared press format took five, the Cycles took three. The anchors are
still the busiest years in the file — 2619 carries seven layer-B albums, 2624 seven, 2612 six — and
the years between them are no longer empty.

**Three albums looked movable and were not, and only a catalogue-wide pass could tell.** `al_095`
and `al_097` are each dated by a *different record's* prose — `al_138` says it came out the same
year The Turning Room recorded in the exchange hall, and `al_139` says it was reviewed alongside The
Long Ferry's record — and `al_118` says the year it landed was the year Lower Bell Editions folded.
Moving any of the three would have made a layer-A album's story false, which is the failure mode a
per-genre card cannot see. **Six more albums named their own release year in their own notes**, and
those notes were edited with the year.

**Rule 8 reads raw file text, and that is a real constraint on how prose is written.** Six of the
nine genre files named no foreign band at all; all nine now name three or more. One reference did
not count on the first attempt because *The Quiet Half* had been broken across a line by the folded
scalar — a name split by a line wrap is invisible to the rule, and to anything else that greps the
wiki. Worth knowing before the next card writes wiki prose.

### D-082 · The anchor stories live in the wiki, in a file that is not a genre — 2026-08-14

M-15's third job. `CONSTANTS.md` §1 held eight good accounts of what happened in each anchor year,
and `CONSTANTS.md` is a working file the station never reads — `check.py` takes the eight numbers
out of its first column and nothing else. `PROGRAMMING.md`'s `Night Record` year edition is supposed
to be built on those accounts and had no way to reach them.

They are now `music/wiki/anchors.yaml`: one entry per year with the story, what the station actually
holds from it, and the records a programme would be built on. **They were moved, not copied** —
§1's table keeps the eight years and the `| **YYYY** |` shape `check.py` reads, and its long
accounts are replaced by a one-phrase index. Two copies of eight stories in a file nothing reads is
how the two come to disagree, which is the same reasoning that keeps the anchor years and §12's
thresholds out of code.

**It is not a genre and is named as such.** `wiki.NOT_A_GENRE` holds `anchors`, and
`written_genres()` skips it, so every pass that walks the wiki — the count check, the year check,
rules 6, 7 and 8, `next_free_ids`, `make music-albums`, `make music-screen` — ignores it. The skip
is by name rather than by shape on purpose: a genre file that failed to parse would otherwise be
silently reclassified as "not a genre" instead of failing loudly. Three tests hold it: that every
anchor year in `CONSTANTS.md` has a story, that the file is not counted as a genre, and that 2559 is
the only year marked unprogrammable.

### D-083 · The ramp is measured from what moves in the middle of the mix, and only claimed when the evidence is there — 2026-08-15

M-04. `make music-analyse` had to find, in 500 finished mixes, the moment the singer comes in.
Loudness cannot do it: on the pilot the band is already playing at full level when the voice
arrives, and the mixture barely changes. What changes is that a sung note *moves* — its partials
glide and shake where a keyboard's sit still — and that the voice is mixed dead centre. So the
measurement is the energy-weighted rate of change of instantaneous frequency, taken from the phase
vocoder's own phase advance across 250–3500 Hz, weighted by how equal the two channels are at each
bin, and divided by all the energy in the band. That last denominator is not a detail: dividing by
the *centred* energy instead was the first attempt, and in a passage with nothing in the middle of
the mix it divides leakage by leakage and reports a singer who is not there.

**A harmonic/percussive median filter was tried on top and removed.** It is the standard first move
and it made the separation between an intro and a first verse *worse* — 1.98 against 2.41 robust
standard deviations on one pilot take, 2.85 against 3.49 on another — while costing five times the
runtime. The centre weighting was already doing the job the percussive filter was there to do.

**numpy, not librosa.** ARCHITECTURE §9 names librosa, and §22 asks a dependency to save more than
~200 lines. librosa would have supplied a spectrogram and a general onset detector, neither of
which is the feature above; what it would actually have saved is the dozen lines of framed FFT in
`analyse.py`, at the cost of eleven transitive packages including numba on the machine that also
has to run MLX. The disagreement with §9 is recorded rather than silently taken: if the imaging
pass in §9 later wants beat tracking and key detection, that is the card that should re-open it.

**Nothing is claimed that is not measured.** A run-up is reported only where the opening of the
record sits at least 1.8 of the curve's own standard deviations under the body of it *and* the rise
out of it holds for fifteen seconds; everything else reads `0.0`, which the report and `ADMIN.md`
both define as "no run-up you could talk over" rather than "the vocal starts at sample zero".
Nothing here resolves an intro shorter than about two seconds, and two seconds is not a link. Every
row carries `firm` or `check` with a reason, because §9 already says the last half-second is a
listening judgement, and a tool that printed 500 confident numbers — some of them wrong — would be
worse than no tool at all.

**The ending is two measurements, not one.** The time the level takes to fall from 3 dB to 20 dB
under the body of the song separates `cold` (under 0.6 s) from the two slow endings; the share of
fresh attacks during that fall separates a `fade`, where the band plays on under the fader, from a
`sustain`, where a chord is left to ring. On the pilot this agrees with what the brief asked for on
11 of 14 cold endings and 10 of 12 sustains — and disagrees on the fades, because Suno mostly did
not fade. That disagreement is a finding about the takes, not an error in the measurement, and it
belongs to M-39.

### D-084 · The four licence tags are written by ffmpeg, into a copy that is checked before it replaces the original — 2026-08-16

M-05. `COMMISSION.md` §9 requires the licence period, the generation date, the model version and an
AI-generated marker inside every audio file. Three things had to be decided.

**No tagging library.** ffmpeg is already a required system tool and already decodes for
`analyse.py`; it writes ID3 too, and maps any key it does not recognise onto a `TXXX` frame it and
every tag editor read back unchanged. §22 asks a dependency to save more than ~200 lines and a
tagging library here saves about thirty. Hand-writing ID3 frames was never on the table — that is
the case the ffmpeg call avoids, not one it creates.

**The four values are four plain keys, and nothing else in the file is touched.**
`AI_GENERATED=true`, `AI_MODEL_VERSION`, `LICENCE_PERIOD` and `GENERATION_DATE` — one key per value
the commission names, no fifth. In particular Suno's own `comment`, carrying the generation id and
the vendor's creation timestamp, is left where it is: M-18 verified the whole 45-song dispatch
against those timestamps and overwriting them would cost that evidence. The vendor and the tier are
already inside the licence period itself (`suno-pro-2026-08`), so nothing about the tool is invented
here that the metadata block did not already say.

**A take is never edited in place.** ffmpeg cannot write tags in place, so each file is copied with
`-c copy` — the mp3 bitstream passed through, not re-encoded — the copy's audio checksum and its
four tags are checked against the original, and only then does it replace the original in one
`os.replace`. An interrupted run leaves whole files behind. Measured over the pilot: all 45 audio
streams are byte-identical before and after, and a re-run rewrites nothing at all, which is what
lets M-39 run this after every genre rather than once at 500 songs.

**It is a gate, unlike the other music commands.** It exits red if a file failed or if any audio
under `music/audio/` is not recorded as a take in `music/production/lyrics/`. `make music-analyse`
can afford to shrug at a file it could not read; a file with no licence attached is one nobody may
broadcast, and the only moment it is cheap to notice is now. A song whose lyrics exist but whose
audio does not is reported as `waiting for audio`, not as a failure — that is a Suno card that has
not run yet.

### D-085 · `catalogue.yaml` derives its rotation category, keeps `playable` meaning "there is a file", and is checked against the wiki rather than trusted — 2026-08-16

M-06. The file `make music-sync` will ingest joins three sources that until now only a person could
read. Four things had to be decided, and one defect turned up while deciding them.

**`category` is derived from §8's own definitions and nothing else.** §8 names six rotation weights
and defines exactly two of them by a rule: `new` is a record released within eight in-world weeks,
`gold` is one five in-world years old or more. Release dates in this world are years, so `new`
cannot be expressed at all and is never written. Everything old enough is `gold`, everything else is
`A`, and **`B`, `C` and `specialist` are never written** — they are editorial demotions nobody has
made, and choosing them here would be authoring content on the operator's behalf (CLAUDE.md). On the
pilot that reads 11 in heavy rotation and 34 gold. Because an age is a fact about the present rather
than about the record, `present_year` is written into the file, taken from the `section:` block every
genre file already carries, and `make check` goes red if the wiki's present moves past it — which
forces the yearly rebuild that `CONSTANTS.md` §1's "recomputed every year" already implies.

**`playable` means the audio exists, and a layer-A song with no take is indistinguishable from a
layer-B title.** §8 is explicit that `playable` is audio and that `file_path` is null wherever it is
false, because a scheduler that picks an unplayable track produces dead air. So the 455 songs whose
Suno card has not run yet are unplayable rows today, exactly like the 858 records the world knows and
the station will never hold, and the distinction disappears when M-38 lands. A **track that could not
be measured is left unplayable** rather than given a ramp of zero (§25's ffprobe rule): a guessed
run-up is a link that clips the first sung word.

**Where the wiki and §8 do not line up, the file carries what the wiki states and the report says
so.** Three cases. `fact` is on the track row although §8's `tracks` table has no such column —
the whole point of the card is a DJ able to say something about a record, and the fact is the only
place that lives; the missing column is §8's to grow. `artists.kind` allows three words and the wiki
writes six, so `crew`, `duo` and `partnership` are all written as `group`. And **no genre file states
a house style**, which §8 gives every label, so all seven are null and the command says so every run.
Twenty bands and albums carry `unsigned`, `not imported` or `not for sale` instead of a label; those
are facts about the world (D-059, D-066, D-078) and become a null label, while anything else that
fails to resolve is counted and named, so a typo cannot become a silent null.

**The check is a separate pass, and it does not read the audio.** `catalogue.py` writes the file;
`catalogue_check.py` reads it back — the same split as `writing.py` from `check.py` (M-45), for the
same reason: a builder can only be wrong in ways it already believes. The file is committed, so the
failure worth catching is not a bad build but a good one going stale, and the check compares every
id and title against the wiki, resolves every reference, and asserts a row carries a whole take or
none of one. Nothing under `music/audio/` is touched, so it runs in CI (§30) and on a fresh clone.

**A defect the pass found, and fixed.** Twenty-five layer-B song titles were truncated in the wiki:
songs are written as YAML flow mappings, and `{title: Two Callers, One Sheet, track_number: 6}`
splits at the comma into the title `Two Callers` and a stray key. It is valid YAML and a valid
title, so nothing had ever failed on it — and a truncated title is a record a presenter names
wrongly on air. All twenty-five are re-quoted, in five genre files, with no other change; §10 permits
a title edit, and restoring text already present in the file is less than that. `wiki.Song` now keeps
what it does not recognise and the catalogue check reports it, so the same bug cannot return quietly.

**Two housekeeping notes.** `cli.py` had reached 391 lines against §31's cap of 400, so the five
music printers moved to `music/console.py` unchanged — the command output is byte-identical, and the
next music target has room. And `music/catalogue.yaml` is 577KB of committed YAML; it is derived, but
it is small enough that keeping it in git is what makes the staleness check possible at all.

### D-086 · The pilot passed, so stages 4–6 run as written — 2026-08-16

M-19, the only quality gate in the project. The operator listened to the pilot's songs and passed
them: *"I listened to all the songs under M-19, it sounds OK."* Nothing automated grades the product
and nothing was ever going to; `MUSIC_TASKS.md` made stages 4, 5 and 6 conditional on this sitting,
and the answer is yes, so **they run as written rather than being rewritten.** M-20 is unblocked and
455 songs of lyrics and audio follow it.

**Two things carried forward rather than settled here.** The operator's standing expectation is
*"better variety in the future with more styles"* — the pilot was one genre on one label and §2's
palette for relay-pop is guitar pop, so uniformity there said nothing about the catalogue and could
not have. Variety is stage 5's to deliver across eight more forms and twenty more bands, and the
honest place to test it is after the second or third genre's audio lands, not at M-42 with 455 songs
already made. And **the duration shortfall stands**: the 45 average 2:29 against COMMISSION §7's
3:30 with fourteen under 2:00, so fourteen of them make about 35 minutes rather than 56. The
operator has accepted the short songs twice. It is M-39's to fix by choosing different takes — the
reason that card runs per genre — and downstream it is arithmetic for back-timing and for how many
songs an hour needs, not a reason to stop.
