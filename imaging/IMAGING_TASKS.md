# IMAGING_TASKS.md — the imaging half of Phase F, start to finish

Every piece of work needed to go from 56 unwired audio files to a station whose hour clock executes
without anyone thinking about it. If it is not on this page it is not part of the imaging job.

**Created 2026-08-23 by operator instruction**, in a planning session covering **Phase F only**
(`PHASES.md` F, ARCHITECTURE §33). It sits outside the §32 document cap on the same grounds
`music/MUSIC_TASKS.md` does (D-053): the operator asked for it directly, which is the case the cap
was never meant to cover.

**Phase F has two halves and this is one of them.** The music half — 500 songs, the wiki, the
catalogue — is `music/MUSIC_TASKS.md` and none of it is repeated here. `TASKS.md` holds neither.
Both halves close the same milestone, **M1**: *would you leave this playing while someone else was
in the room?* — asked this time of the finished sound, with the hour clock, the beds and the station
furniture around it (`PHASES.md`, "The map").

**Numbers are identities, not order.** `I-06` names one card for the life of the project. The order
is the order the cards are printed in; the card to work is the one marked **NEXT**.

> ### Status: every card below is a DRAFT
>
> §33 rule 3 — *card by card, and silence is not acceptance.* Nothing here is work until you have
> accepted, rewritten or rejected each card by number. When you have, this box comes out and `I-01`
> is marked **NEXT**.

---

## Who does what

| Tag | Meaning |
|---|---|
| `[agent]` | An agent does it. You read the result and say keep or redo. |
| `[you]` | Only you can do it. Suno, ears, and the words the law will read. |

**One card at a time, top to bottom.** A `[you]` card and an `[agent]` card may run at the same
time; two `[agent]` cards may not. Say the number to start one — "Do I-02" — the way music works.

### Before the session ends — every time

1. Mark the card just finished `DONE`, with the date and a `Result:` line saying what it actually
   produced.
2. Mark the next runnable card `NEXT`. Runnable means every card on its `Depends on:` line is done.
3. Bring the stage table below up to date in the same edit.
4. Tell the operator what changed and exactly how to check it.

---

## Where we are

| Stage | Cards | Status |
|---|---|---|
| **0 · What today's 56 files already allow** | I-01 · I-02 · I-03 · I-04 | **I-01 · I-02 done** · I-03 **NEXT** · I-04 waits on C8 |
| **1 · The manifest** | I-05 · I-06 · I-07 | blocked on `grid.yaml` (**C4**) |
| **2 · The gaps — the long pole, and it is yours** | I-08 · I-09 · I-10 · I-11 · I-12 · I-13 | ~36 new pieces minimum, ~64 if I-10 goes the other way |
| **3 · Execution — the hour clock** | I-14 · I-15 · I-16 · I-17 | last · this is what M1 is judged on |

**What exists:** 56 approved Suno assets in `music/jingles/approved/`, inventoried in that folder's
`README.md`, accepted by the operator 2026-08-23. Nothing is wired to anything — there is no
`imaging` table, no `imaging/catalogue.yaml`, and no `grid.yaml`.

**What is missing, in one line:** 5 strand opens · ~30 strand closes · a news bed · the disclosure
ident · and either 0 or ~28 link beds depending on I-10.

**Two things gate this whole file.** `grid.yaml` (**C4**) — programme ids do not exist until it is
written, and every `open_*` name in the pile is a guess at one. And **Phase E**, which everything in
stage 3 extends rather than builds.

---

## Stage 0 · What today's 56 files already allow

*None of this waits for the grid, the Studio, or a single new piece of audio.*

### I-01 · `[you]` Which Suno model made the July jingles — **DONE 2026-08-23**
Goal: the last unknown fact about the 56 files. Everything else about where they came from is
already written down; this one is not, and only you can look it up.
Files: `music/licence-evidence/2026-07-suno-licence-note.md`
Check: open the Suno account, find any generation from **04, 08 or 20 July 2026**, and say which
model it used. The answer goes on one line of the July licence note, replacing "not recorded".
"Suno no longer shows it" is a complete answer — it gets recorded as unknown and nothing is blocked.
Note: **the licence itself is already filed and needs nothing from you.**
`2026-07-suno-licence-note.md` records the terms in force, the Pro tier at all three dates, Remix
never enabled, and `suno-pro-2026-07` as the period to stamp on each asset. What it does not have is
the model version, which `COMMISSION.md` §9 wants inside every audio file — the 56 files' own tags
carry only "made with suno", a timestamp and a generation id, verified across all 56. An agent
cannot sign in to Suno, which is the whole reason this is yours. It blocks I-03 because that card
writes this value into the files.
**Two stale lines in `music/jingles/README.md` §1 get corrected by the agent in I-03**: the
"Outstanding" paragraph still says July has no licence file, and the generation-date table says
27 · 23 · 11 where the files themselves say **25 · 22 · 9**. The README's figures sum to 61, not 56.
Result: **v5.5, all 56** — the same model version the 45 songs carry (operator, 2026-08-23). Written
into `2026-07-suno-licence-note.md`, which now reads **Complete: yes** with no gap under it. The
files' own tags still do not carry it — Suno's export writes no model field — and I-03 is what puts
it inside them.
Depends on: —

### I-02 · `[agent]` `make imaging-analyse` — the four numbers, measured not estimated — **DONE 2026-08-24**
Goal: you never hand-time a hundred pieces. The machine measures each one and flags only the ones
worth your ears.
Reads: ARCHITECTURE §9, §22 · DECISIONS D-083
Files: `src/station/imaging/analyse.py`, `Makefile`, `docs/ADMIN.md`
Check: `make imaging-analyse` reads every file in the imaging folder and prints, per piece, its
length, its run-up before the first sound you cannot talk over, its energy, and **for a bed, the
point the loop should return to**. On the 56 its figures agree with your ear on a spot-check of ten,
and every borderline row reads `check` with the reason attached rather than a confident number.
Note: D-083 built this measurement for music and said in as many words that **the imaging pass is
the card that should re-open the librosa question** if it ever wants beat tracking or key detection.
Re-use `music/analyse.py`'s ramp measure rather than writing a second one. `bed_loop_sec` is the one
genuinely new thing here — a seam, not an onset — and `fallback_bed.mp3` is the piece to prove it
on: eight minutes long, and README §6 records that it does not resolve at its end.
Result: `make imaging-analyse` measures all 56 in about half a minute and prints four numbers each.
**Energy is the spectral centroid, log-scaled 0 at 250 Hz to 1 at 5 kHz** — onset density and
rhythmic modulation were both measured across the pile first and neither separated a night piece
from a bright one, because §2's palette holds tempo nearly constant and varies timbre (D-094). It
runs 0.11 for `open_the_night_watch_0204` to 0.95 for `sweeper_mid`. **The loop seam works and
`fallback_bed` is the only file that has one**, at 448.6 s: looping it back to zero steps 23.7× the
piece's own frame-to-frame movement, the measured point steps 2.2×. **The other three beds have no
seam at all** — `link_bed_day`, `link_bed_night` and `disclosure_bed` were generated as one-shot
pieces and do not repeat their endings, which is a finding for I-13, not a threshold to lower. The
ramp is `music/analyse.py`'s, which correctly claims nothing on 56 instrumental files, with a level
measure under it for that case; seven pieces have a run-up, 0.7 s to 4.6 s. Two rows read `check`.
librosa is declined again and the question D-083 left open is now closed (D-094).
Depends on: —

### I-03 · `[agent]` `make imaging-tag` — licence and compliance into every file — **NEXT**
Goal: every imaging file still says what it is after a backup or a hand-off separates it from the
manifest.
Reads: ARCHITECTURE §9, §18 · DECISIONS D-084 · `music/COMMISSION.md` §9
Files: `src/station/imaging/tag.py`, `Makefile`, `docs/ADMIN.md`
Check: all 56 files carry the licence period, generation date, model version and an AI marker.
Suno's own comment — the generation id every one of these can be re-exported by — is untouched.
Running it a second time reports them already correct and rewrites nothing, and the command exits
red if any file failed.
Note: D-084 settled every decision this card would otherwise re-take: ffmpeg rather than a tagging
library, four plain keys and no fifth, and a copy checked against the original before it replaces it
so an interrupted run leaves whole files behind. The one difference from music is where the values
come from — imaging has no per-album metadata block, so all four are read from
`music/licence-evidence/2026-07-suno-licence-note.md`: the period `suno-pro-2026-07`, the generation
date from each file's own Suno timestamp, and the model version I-01 supplies. **While in there,
correct README §1's two stale lines** — July's licence file exists, and the dates are 25 · 22 · 9.
**If this turns out to be a copy of `tag.py`, make it one module both call.**
Depends on: I-01

### I-04 · `[agent]` The IP screen over the pile
Goal: nothing on air quotes a real franchise, artist or composer — including the one piece that
sings.
Reads: ARCHITECTURE §9, §19 · §17a (`banned-entities.yaml`)
Files: `src/station/`, `docs/ADMIN.md`
Check: the banned-entity pass runs over every imaging id, title and the sung tagline
*"Settlement Radio — the light between the worlds"*, and reports clean. Anything it flags is named
with the file it is in.
Note: §9 exempts imaging from the safety gate — it is hand-curated, not generated per air — and
explicitly does **not** exempt it from the IP screen. `sonic_logo_signature.mp3` is the only asset
carrying words (README §5a); everything else is a title check. Owed before air, not before filing.
Depends on: C8 (`banned-entities.yaml` seed)

---

## Stage 1 · The manifest

*The route from 56 files to rows the station can read. D-093 decided this exists; none of it is
built.*

### I-05 · `[agent]` The naming convention, and the `jingle_set` ambiguity
Goal: imaging ids get one convention, decided once, before a hundred pieces are named against it.
Reads: ARCHITECTURE §9, §17a · DECISIONS D-093 · `music/jingles/README.md` §3
Files: `docs/DECISIONS.md`, `docs/ARCHITECTURE.md` §17a
Check: a `DECISIONS.md` entry answering three questions, and §17a reading the same afterwards:
(1) does a programme slug keep its article — `the_count` keeps it, `evening_report` drops it, and
§17a's own example does both; (2) does an imaging id abbreviate the slug — `evening_report` carries
`evening_open` and `report_bed`, shorter and inconsistently so; (3) **is `hour_clock` an override of
`jingle_set` or a duplicate of it?**
Note: the third is the one that matters and README §3 raises it. `jingle_set` is mandatory on every
programme (validation 6) while `hour_clock` names imaging ids directly — so a set name appears to
imply its own open/close/bed by convention whenever `hour_clock` is absent, which would make the set
name load-bearing after all and validation 6 check two overlapping things. Nothing in stage 1 or 2
can be named until this is answered. **This is a decision card: it produces a paragraph, not code.**
Depends on: C4

### I-06 · `[agent]` `imaging/catalogue.yaml` — the file the station reads
Goal: the 56 files stop being a folder and become an inventory, with the numbers already measured
and the names already right.
Reads: ARCHITECTURE §9, §17a · DECISIONS D-093, D-054 · `music/jingles/README.md` §4–§5
Files: `imaging/catalogue.yaml`, `src/station/imaging/catalogue.py`, `tests/unit/`
Check: one row per asset, carrying its id, kind, file path, the numbers I-02 measured, its tags and
its licence note — and, for the 25 reassigned opens, the strand it belongs to. `make check` goes
**red** on any of: a row whose audio file is missing, an id used twice, a `kind` that is not one of
§9's nine, a bed with no loop point, an asset with no licence note.
Note: D-093 settled that this file exists and that **placement stays in `grid.yaml`** — this file
says what pieces exist, the hour clock says when each one plays, and validation 6 checks one against
the other, which is only possible while they are separate. The checks go inside `make check` as unit
tests over the real file rather than becoming a target of their own: D-054's reasoning, and it means
CI runs them for free. README §5b's strand assignments are the input to the programme column and you
accepted all 25 on 2026-08-23. The four spares carry no programme. The second Night Watch 01:04
candidate is a row like any other until you choose. **Audio stays out of git** — `*.mp3` is already
ignored — and `file_path` points at the external volume under `imaging/`, the rule music follows.
Depends on: I-02, I-05

### I-07 · `[agent]` `make imaging-sync` — the rows into the database
Goal: the grid can finally name a piece of imaging and be told when it does not exist.
Reads: ARCHITECTURE §9, §17a validation 6, §7 (sync commands)
Files: `src/station/imaging/sync.py`, `src/station/store.py`, `Makefile`, `docs/ADMIN.md`
Check: run it and the `imaging` table holds one row per catalogue entry. `make grid-sync`'s
validation 6 then passes — every imaging id, `jingle_set` and `chart_id` named in `grid.yaml` exists
— and when it fails it names the missing id and the programme that asked for it. Running the sync
twice changes nothing.
Depends on: I-06

---

## Stage 2 · The gaps — the long pole, and it is yours

*`PHASES.md` sizes C6 at 100+ pieces and 56 exist. Everything here is Suno, ears and judgement.
Stage 3 does not need all of it — I-14 needs I-11 and I-12 — but M1 does.*

### I-08 · `[you]` The disclosure ident `ai_ident`
Goal: the one piece of imaging the law cares about. Every hour, at every one of the six playout
levels, the station says what it is and that it is machine-made.
Reads: ARCHITECTURE §18, §9, §15 · PHASES F, G
Files: the audio, and `imaging/catalogue.yaml`
Check: a finished piece exists as `ai_ident`, replaces the placeholder T-010 put on the transmitter,
and fires at `:00` with the source machine switched off — the T-012 check, re-run against the real
thing.
Note: **this one is missing and the inventory does not say so.** README §7 calls station furniture
"15 of ~16 slots filled" and names only `news_bed` as the gap; `disclosure_bed.mp3` is the underlay
for a spoken disclosure, not the ident itself. §17a's station-wide default is
`disclosure_sting: ai_ident` and §18 hard-schedules it independently of content precisely so that it
still fires at 04:00 when playout has fallen through to music. It carries words, so it is a render
over the existing bed rather than a Suno piece — and **Phase G's lawyer reads those words**, so
write them before that review rather than after it.
Depends on: —

### I-09 · `[you]` `news_bed`
Goal: the bulletin has something under it.
Check: a loopable bed exists, its seam measured by I-02, sitting at −12 dB under speech without
pumping when the mixer ducks it. Judged on one real bulletin, by ear.
Note: the single gap README §7 does name. `news_open.mp3` stays what it is — an opener, not this.
§2's brand rules bind: the glass-bell motif, night tier, Pro plan, 2–4 takes and keep the best.
Depends on: —

### I-10 · `[you]` + `[agent]` The bed decision — thirty beds, or two
Goal: settle the difference between ~36 new pieces and ~64 before either number is committed to.
Reads: ARCHITECTURE §9 · `music/jingles/README.md` §7
Files: `docs/DECISIONS.md`, `config/grid.yaml`
Check: a `DECISIONS.md` line recording the choice and why, and every programme's `bed_under_links`
filled in accordingly.
Note: `bed_under_links` is declared per programme but **nothing stops two programmes naming the same
bed**, and two generic beds — day and night — already exist. This is a design decision that lives in
`grid.yaml`, not in the inventory. The agent writes the config; the choice is yours, and the honest
version of the question is whether a listener could tell.
Depends on: C4

### I-11 · `[you]` The five missing opens
Goal: no strand goes to air without an identity of its own.
Check: opens exist for **Vantage** (13:32) · **Names** (16:32) · **The Six** (18:04) ·
**The Week in Ice** (Sat 12:04) · **Observance** (Sun 09:04), each in the 8–15 s band, each quoting
the glass-bell motif.
Note: **The Six is the main news programme of the day** — do it first and judge the other four
against it. `open_faith_in_transit.mp3` could double for Observance and README §5a leaves that to
you. Whether The Night Watch is one programme or four changes this count by three and is settled by
`grid.yaml`, not here.
Depends on: I-05, C4

### I-12 · `[you]` The ~30 closes
Goal: every strand ends the way it started. This is the largest single piece of imaging work left
and the one that most changes whether an hour sounds finished rather than stopped.
Check: every programme in `grid.yaml` has a close, and `make grid-sync` stops complaining about
incomplete sets.
Note: closes are **0 of ~30** (README §7) — the opens were the cheap third. §2's palette and the
three energy tiers bind, and the family rule is that the motif recurs while the lead instrument
changes. This is many sessions, not one; take it a daypart at a time and let the stage table carry
the count.
Depends on: I-05, C4

### I-13 · `[you]` The ear pass — trims, tails and ramps
Goal: the pile stops having known defects, and the numbers in the catalogue are the ones you
actually believe.
Reads: ARCHITECTURE §9 · `music/jingles/README.md` §6
Check: three things. Strand opens sit in the 8–15 s band — about 29 run long today, up to 49 s. The
seven defective files are fixed or re-exported from Suno: five cut off mid-body and needing a tail
fade, two with no headroom that will clip on any re-encode. And every ramp and loop seam I-02 marked
`check` has been listened to and corrected in `imaging/catalogue.yaml`.
Note: §9 is explicit that the difference between a link that lands and one that clips the vocal is
about half a second, and that no tool settles it. The generation ids in every file's comment tag
make a clean re-export possible without regenerating anything.
Depends on: I-02, I-06

---

## Stage 3 · Execution — the hour clock

*The mixer exists from build step 8 and the batch runs itself after E. These cards give the mixer
its imaging, which is the half M1 is judged on.*

### I-14 · `[agent]` The hour clocks in `grid.yaml`
Goal: every programme declares its own furniture, so imaging is config and never logic.
Reads: ARCHITECTURE §9, §17a · PROGRAMMING §8, §10
Files: `config/grid.yaml`, `docs/ADMIN.md`
Check: every programme names an open, a close, a bed and a sweeper cadence; the junction names its
sting, bed and disclosure ident; `make grid-sync` is green, validation 6 included, and no programme
is missing a `jingle_set`.
Note: this is the card where the whole file's dependencies come due — a clock cannot name a piece
that does not exist, and I-07 is what makes naming a missing one an error rather than a silence.
Depends on: I-07, I-10, I-11, I-12

### I-15 · `[agent]` The mixer plays the imaging
Goal: an hour that sounds produced rather than assembled — the difference between radio and a
podcast with music after it.
Reads: ARCHITECTURE §9 (the mix specification), §11
Files: `src/station/mix.py`, `tests/`
Check: build one floating hour and listen. The open plays at full level and crossfades 1.5 s into
the first link. The bed loops underneath at −12 dB, fading in 0.8 s before speech and out 1.2 s
after, ducking with a 300 ms attack and 800 ms release. A sweeper lands every Nth item. The close
crossfades out over 2 s. **Sweepers and idents are chosen round-robin by last-used, never at
random** — random selection audibly clusters. A cue sheet is written carrying every element's final
offset.
Note: `mix.py` already exists from Phase D; this card gives it §9's assembly order. **The same
specification's other half is the music slot** — talking over a track's run-up, and what may be said
over a `cold`, `fade` or `sustain` ending. It is one algorithm and splitting it would be artificial,
so it is here rather than in `music/MUSIC_TASKS.md`, which holds content and no engineering. Say if
you would rather it moved.
Depends on: I-14

### I-16 · `[agent]` The junction, which is stricter
Goal: the hour starts hard, on the hour, the same way every time.
Reads: ARCHITECTURE §9, §13, §18, §11 (invariant 3)
Files: `src/station/mix.py`, `tests/`
Check: at `:00` — the news sting at full level, a hard start with no crossfade, because that is what
marks the hour. Bulletin over the news bed at −12 dB. **The disclosure never omitted**, over the bed
or dry. Then the time check, the trail for what follows, and a 1.5 s bed tail to silence.
Note: the junction is pinned to the wall clock and its assembly is a different algorithm from a
floating show, not a variation on one. §11's third invariant is what makes the disclosure
unskippable in code rather than by convention.
Depends on: I-15

### I-17 · `[agent]` The timing test and the imaging cache
Goal: the hour that landed today still lands in six months, and the machine never re-measures a file
it has already measured.
Reads: ARCHITECTURE §3 (conformance), §26, §29
Files: `tests/conformance/`, `src/station/`
Check: the timed-assembly conformance test asserts a built hour's cue sheet against expected offsets
and fails on drift. Rendered imaging is cached and **never invalidated** — that is the point of
rendering it once — and an hourly playlist build re-probes no imaging file's duration.
Note: §29 allows five kinds of test and no sixth; this is the conformance one, which is what makes
the seams real. §26 names both caches. **`make check` stays under three minutes** — if the timing
test needs real audio, it belongs in `make smoke-full` rather than in CI.
Depends on: I-16

---

## What this file deliberately does not contain

- **The music half of Phase F.** `music/MUSIC_TASKS.md`, 42 cards, unchanged by this session.
- **Compliance.** I-08 makes the disclosure ident exist; **Phase G** decides whether it is enough,
  and that is a lawyer's answer, not an agent's.
- **The archive.** `PHASES.md` H, and its pool is not this pool.
