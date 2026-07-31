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
