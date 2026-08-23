# Settlement Radio — Phases

*The road from nothing to a station with listeners. Eleven phases, each with a goal, an outcome you
can see or hear, and what it needs before it can start.*

> **Ownership: the operator's.** Agents read this **only in a planning session** (ARCHITECTURE §33),
> where one phase is turned into `TASKS.md` cards. It is not read during normal work and it
> generates no tasks by itself.
>
> **This document says *what* and *when*. `ARCHITECTURE.md` says *how*.** Each phase names the
> architecture sections it completes and does not restate them; each phase names the §35 build steps
> it contains and does not re-describe them.
>
> **Where the two disagree, ARCHITECTURE §32's precedence table decides — it is the only place
> precedence is stated.** In short: on **when**, this document wins; on **what** or **how**,
> `ARCHITECTURE.md` wins; and a later `DECISIONS.md` entry beats both.

---

## How to read this

**A phase is the unit a planning session works in.** One phase is planned into cards, shipped, and
only then is the next planned. Planning all eleven up front is a phase pack, which ARCHITECTURE §34
records as the specific thing that killed the previous attempt.

**Each phase lists four kinds of prerequisite**, because they have different lead times and only one
of them is the operator's own hours:

| | Lead time |
|---|---|
| **Hardware** | Weeks — order early |
| **Accounts** | Hours, but some need a card and one needs a lawyer |
| **Content** | The operator's own hours. Cannot be delegated (§33), cannot be parallelised |
| **Depends on** | Other phases |

**Content is the long pole in every phase that has any.** Code is delegated to agents and is cheap;
canon, cast cards, speech profiles, voice clips, music, imaging and pool pieces are the operator's
alone. A phase whose content is not started will not finish on time regardless of how the code goes.

---

## The map

| Phase | Name | Milestone | Blocked by |
|---|---|---|---|
| **A** | Foundations | — | hardware |
| **B** | The Transmitter | **M0** | — |
| **C** | The World | — | A |
| **D** | The Voice | *go/no-go* | A, B, C |
| **E** | The Day | **M2** | B, D |
| **F** | Music and Imaging | **M1** | E |
| **G** | Compliance and Legal | *hard gate* | E, F |
| **H** | The Archive | — | F |
| **I** | The Public Face | — | E, G |
| **J** | Launch and Audience | **M3** | G, H, I |
| **K** | After | **M4 → M5** | J |

**A and B are independent and either may go first.** B needs no Studio at all, so it is the phase to
run while hardware is in transit. Everything from C onward is serial.

**M1 and M2 complete out of numerical order** — the batch learns to run itself (E) before the station
sounds finished (F). PRODUCT §8 numbered the milestones as listener experience, not as build order,
and that is fine.

**D's question and M1's question are the same sentence about two different things.** Both ask
*would you leave this playing while someone else was in the room?* — but D asks it of a bare show
with no imaging and no music, where the only variables are the writing and the voices (§36.2), and
**M1 asks it of the finished sound** in F, with the hour clock, the beds and the station furniture
around it. Answering it once in D does not discharge it in F, and a no in D means something quite
different from a no in F.

---

## The content track

**Content is not a phase. It is a band running under all of them**, with a due date per phase — and
it is the operator's own hours, which makes it the only genuinely scarce resource in the project.
ARCHITECTURE §35 warns that it is "the half most likely to be forgotten when the work is split into
tasks," so it gets one view of its own here.

Each phase lists what it needs. This table is the same information ordered by *maker* rather than by
phase, so the person who has to write all of it can see it at once.

| Item | Due for | Rough size | Can start |
|---|---|---|---|
| **Canon seed** (C1) | **C** | ~150 facts minimum, all seventeen domains present | **now** — markdown, no machine |
| **`banned-entities.yaml`** (C8) | **C** | a list, grown by `make banned-add` thereafter | **now** |
| **Cast cards + speech profiles** (C2) | **D** | six people: breakfast host, evening host, scripted newsreader, chart voice, two beat correspondents | **now** — drafting; the profiles need the register spec |
| **Voice reference clips** (C3) | **D** | 6 × 10–20s WAV, committed, with `voices/PROVENANCE.md` | after the TTS engine is chosen (A) |
| **Stock voice bank** (C9) | **D** | 12–20 clips, varied by age, register and settlement | after A |
| **`grid.yaml`** (C4) | **D** | ~30 programme entries from PROGRAMMING §8 | **now** — the grid is written and validated |
| **Pool pieces** (C7) | **E** | 37 minimum across three length bands, all filler — idents are imaging (D-008) | after D |
| **Imaging + jingles** (C6) | **F** | **~30 jingle sets** — one per strand, each an open, close and bed, plus a sting for news — and the station furniture on top. Call it 100+ pieces, listed in `imaging/catalogue.yaml` (D-093). **56 already exist** — see `music/jingles/README.md` | **partly done** — the remainder after F's Suno account |
| **Music wiki** (C5a) | **F** | **~100 musicians · ~195 albums · ~1,700 song titles**, spanning ~200 years in three layers (D-044) | **now** — text only, no account, no hardware |
| **Music audio** (C5b) | **F** | **500 songs** — the playable layer of the wiki, plus lyrics and style cards | after F's Suno account |
| **The archive** | **H** | ~4,000 speech-minutes, ~165 hours | **not before F** (D-006) |
| **LICENSE decision** (C10) | **J** | code and canon almost certainly want different terms | **now** |

**Four items can start before any hardware arrives** — canon, banned entities, cast drafting and
`grid.yaml`. Canon is the big one: it gates phase C and is the largest single thing only the
operator can make.

> **Imaging is not "a pack."** The grid has around thirty named strands and ARCHITECTURE §17a makes
> a `jingle_set` mandatory for every one of them, so this is a hundred-odd short pieces, not a dozen.
>
> **C6 is roughly a third done before F starts, and the done third is the cheap one.**
> `music/jingles/README.md` is the inventory: **56 assets** carried over from the previous attempt,
> licensed and filed — the station furniture almost complete, and ~29 programme opens. **Read it
> before drafting any C6 card.** What is missing is the expensive two-thirds: **~30 programme
> closes, ~30 link beds, 5 opens with no candidate, and `news_bed`** — a minimum of ~36 new pieces,
> or ~64 if every strand gets its own bed rather than sharing. Two gates sit in front of all of it,
> both in that README: the operator's listen to the signature ident, which the whole family hangs
> on, and the naming, which cannot be settled until C4 fixes the programme slugs.

> **The music catalogue is not a pile of tracks; it is a wiki with a record library inside it**
> (D-044). §8 gives rotation weights and separation rules but never said how big the catalogue must
> be, and the grid asks a harder question than "how many tracks".
>
> **The real constraint is shape, not size.** `Night Record` is "one label or one year"; the Night
> Watch runs label retrospectives, artist profiles and single-album stories. None of those can be
> made from a flat pile of unrelated tracks. But neither do they need audio for everything a
> presenter *mentions* — real presenters reference far more music than their station owns, and text
> is around a hundred times cheaper than generated and auditioned audio.
>
> **So the catalogue splits in three.** ~500 songs with audio (last ~60 years); ~1,200 more that
> exist in the world and the station does not hold; and ~30 historical figures whose recordings are
> lost, reaching back two centuries. Roughly **100 named musicians, 195 albums, 1,700 song titles.**
> Full detail is in `music/COMMISSION.md`; the operator's procedure is `music/RUNBOOK.md`.
>
> **This is why C5 splits into C5a and C5b in the table above.** The wiki — the larger part, and the
> part the presenters actually use — is text and needs no vendor account and no hardware. It is
> genuinely startable now, and it was previously and wrongly gated behind phase F's Suno account.
>
> **A `playable` flag carries the split into the schema** (§8): retrieval may reach any song, but
> rotation, the playlist builder and the chart filter on it. That is a code requirement, and it lands
> before `rotation.py` is written.

---

## The open decisions and where they close

ARCHITECTURE §38 keeps a register of what has not been decided, each with the test that decides it.
Every one of them has a phase, and this table is the only place that says which — **a register
nothing references is a register that rots.** §38 stays the authority on what each decision *is*;
this says *when*.

| §38 decision | Closes in |
|---|---|
| Chatterbox vs Qwen3-TTS for cast | **A** — the same 90-second two-hander through both. **A listening test and nothing else** (D-019): watermarking is recorded, never weighed |
| Which freshness tier the grid ships at | **A** — falls out of the RTF measurement against `PROGRAMMING.md` §9 |
| Writer model | **narrowed in A, settled in C** — `make benchmark` disqualifies candidates cheaply on synthetic context; choosing between the survivors is a blind read (§36.2) and needs real canon |
| ~~The catalogue's shape~~ | **closed** — D-040, then superseded by **D-044**: a wiki of ~1,700 songs across three layers, of which **500** are recorded |
| Voice identity when the archive is deep | **F**, at step 13b — before 50 shows exist, not 500 |
| Sign the Code of Practice deployer section | **G** — the lawyer |
| Panel screens | **K** — whatever was actually reached for in the first 30 days |
| **Listener telemetry — whether to collect it at all** | **J** — added here; PRODUCT §9 wants return listening and time in stream, and no section of the architecture provides either |

**A and C close three of the eight between them**, which is what makes the front of the project the
part that can least afford to be rushed — the cast engine and the freshness tier are both
irreversible in practice once content exists. One row left the register entirely: the archive is
elastic and the separation window never moves (D-021). One was narrowed rather than closed — the
cast engine is now a pure listening test, because watermarking no longer bears on it (D-019).

---

## A · Foundations

**Goal.** Establish that the machine can do the work at all, before any pipeline exists.

**Outcome.** Two numbers written into `DECISIONS.md`: the measured sustained TTS real-time factor,
and a first verdict on whether a 9–10B local model writes radio worth broadcasting — taken on a
hand-written brief, which is the cheap version of the test. A repo that lints, types and tests green
on an empty project. **Two of §38's open decisions close here** — the cast TTS engine and which
freshness tier the grid ships at — and the writer-model field is narrowed to the candidates
`make benchmark` did not disqualify.

- **Hardware** — Mac mini M4 16GB + external Thunderbolt SSD 2TB. Nothing in this phase starts
  without both.
- **Accounts** — Hugging Face (model downloads) · **GitHub** (the repo and its three CI workflows).
- **Content** — none.
- **Depends on** — nothing.

**Completes in ARCHITECTURE:** §21 repo layout · §22 toolchain · §23 config and secrets ·
§29 the five kinds of test and `make benchmark`'s pass thresholds · §30 the three CI workflows ·
§31 code standards · §2's model table resolved to real artifacts, **with each TTS candidate's
watermarking recorded as a fact** (D-019) · **§36.1** the RTF measurement · **§36.3** the assemble
budget.
**Build steps:** 0, 0b, 1, and §36.2's cheap week-one version.

> **The cold read is model-bound, not hardware-bound.** Whether a 9–10B model writes usable radio is
> a property of the model, so it can be answered on rented hardware months before the mini arrives.
> The RTF measurement cannot — "on this machine" means the mini.
>
> **Only the cheap version of §36.2 lands here.** The real measurement needs real canon, a real
> world slice and a real brief, so §36 puts it after build step 7 — it belongs to **C**, not to this
> phase. Running the week-one hand-written version now is what stops the question waiting until
> month three.
>
> **§29 and §30 are not deferrable.** `CLAUDE.md`'s definition of done requires the one kind of test
> that applies to *every* task from the first one, and `make benchmark` is the gate the writer-model
> decision is settled with — so the taxonomy and the workflows are built here, not retrofitted.
>
> **The repo stays private until J.** §27's public-repo hygiene and §30's no-secrets-on-forks rule
> are built now and become load-bearing then; gitleaks runs from the first commit regardless. This
> is why C10 sits in J rather than here.
>
> **§36.3 is an afternoon and it decides a design question.** The batch gives assembly 20 minutes at
> 06:30 and nobody has timed it. Measure it here, because the fix for a slow assemble — building the
> batch to mix and sign continuously rather than in one pass — is cheap before step 11 exists and a
> rewrite afterwards. It is a budget, not a gate: a slow figure moves the night, never the product.

---

## B · The Transmitter

**Goal.** A stream that never dies, before there is anything worth putting on it.

**Outcome.** **M0.** A URL playing placeholder audio on a loop, surviving a week unattended, with
the hourly junction slot pinned and the disclosure sting firing whether or not any content exists.
Kill the source and it keeps playing.

- **Hardware** — none. This runs on a rented Linux box.
- **Accounts** — Hetzner (CX32, ~€11/mo) · Tailscale (free, for SSH).
- **Content** — a handful of placeholder audio files. Any audio will do.
- **Depends on** — nothing. Fully parallel to A.

**Completes in ARCHITECTURE:** §4's Transmitter half · §15 playout and the six-level failure
chain, including the explicit 300-client Icecast cap · §27's transmitter firewall posture.
**Build steps:** 2.

> **Keep it unlisted and access-restricted until G closes.** A public stream before the legal review
> raises a placing-on-the-market question that has not been asked yet (§18).
>
> **M0's URL is a bare host until I.** The domain and its DNS are I's account item; nothing here
> needs a name, and buying one early only starts a clock on a public surface G has not cleared.

---

## C · The World

**Goal.** A world that keeps its own time, with a canon behind it that retrieval can actually reach.

**Outcome.** `make tick` advances threads, schedules beats, and writes items — and the result is
readable prose you can judge. Retrieval returns the right facts for a hand-written query. **The real
§36.2 measurement is run and its verdict written down**, on retrieved context rather than
hand-written context — which is also where **§38's writer-model decision closes**, between the
candidates A did not disqualify.

- **Hardware** — the Studio, from A.
- **Accounts** — none new. One **download**: Wikidata's `humans` and organisations subsets (CC0),
  filtered to entities carrying sitelinks — the real-person screen, refreshed quarterly.
- **Content** — **C1 canon seed** (~150 facts, all seventeen domains present) and **C8
  `banned-entities.yaml`**. C1 is the largest single operator item in the project and gates most of
  what follows; start it the moment A's cold read passes.
- **Depends on** — A.

**Completes in ARCHITECTURE:** §5 knowledge architecture · §6 the world, **less the on-air
writeback, which belongs to E** · §7 canon ingestion · §13's clock and phrase renderer ·
§19's deterministic screen on *proposed* figures · §26's indexes, its prompt-prefix ordering and
the canon-side caches (embeddings, domain summaries) · §4's Studio half — the external volume
layout and the Postgres mount guard.
**Build steps:** 3, 4, 5, 6, 7, and **§36.2 in earnest**.

> **§19's figure screen cannot wait for G.** §19 fixes the order: the gate runs on the world tick's
> *proposed* figures, **before they are committed**, because anything already in `figures` is exempt
> forever. A tick that commits unscreened names in this phase permanently exempts them, and G cannot
> undo it. Only the deterministic screen moves here — the model check, profanity, structural checks
> and the quarantine path stay in G with the rest of §19.
>
> **The real-person screen is a build task, not a config file.** ~1.5M names behind two structures,
> because one will not do: a bloom filter for the exact-match pass and a trigram-indexed surname
> table for the fuzzy pass, with the ≥5-sitelink notability floor applied at query time. Budget it
> as engineering, separately from C8, which is a hand-written list.
>
> **Postgres must not start before `/Volumes/station` mounts**, or the database comes up empty and
> the batch writes into nothing. That guard belongs with the schema, which is why §4's volume half
> lands here rather than in E.

---

## D · The Voice

**Goal.** Find out whether the writing and the voices are good enough. This is the phase that can
end the project.

**Outcome.** One complete floating show — written, rendered, mixed, playing on the Transmitter. You
listen to it away from the screen and answer one question, written down in advance: *would you leave
this playing while someone else was in the room?*

- **Hardware** — the Studio.
- **Accounts** — none new.
- **Content** — **C2 cast cards and speech profiles** (six: breakfast host, evening host, scripted
  newsreader, chart voice, two beat correspondents) · **C3 voice reference clips** · **C9 stock
  voice bank** for guest figures · **C4 `grid.yaml`**.
- **Depends on** — A, C, and **B** — the outcome is a show *playing on the Transmitter*.

**Completes in ARCHITECTURE:** §3 both seams and their conformance · §11 shows and the script
schema · §11a register, direction and DNA, including the distinctiveness check · §12 the voice
pipeline · §17a `grid.yaml` · §17's `make sample`.
**Build steps:** 8.

> **This is the go/no-go.** If the answer is no, there are three moves and none of them is more
> architecture: larger hardware, a small paid budget for flagship scripts, or — if the *voices*
> rather than the writing are what failed — **fewer fresh hours**, which is a freshness-tier
> decision against `PROGRAMMING.md` §9 and costs nothing but airtime. Nothing in E onward is worth
> starting until it lands.
>
> **`make sample` is built here, not in E.** §17 calls it the one admin target worth having on day
> one, and this is the phase whose entire outcome is a blind listening judgement. Deferring it to
> E's `make` surface would mean making the project's largest decision without the instrument the
> architecture nominates for it.
>
> **The mix here is bare.** §9's mix specification — beds, opens, closes, the hour clock — is F. A
> show in this phase is voices concatenated with the §12 pipeline and nothing around them, which is
> enough to judge writing and performance and is not yet what **M1** asks for.
>
> **`grid.yaml` names imaging ids that do not exist yet, and that is expected.** §17a validation 6
> requires every referenced imaging id and `jingle_set` to resolve, and the catalogue they resolve
> against — `imaging/catalogue.yaml` — is not built until F (D-093). C4 declares the names; F fills
> them. Whoever writes the grid should know the target file exists by decision before it exists on
> disk, so the naming is chosen once rather than twice.

---

## E · The Day

**Goal.** The station runs itself overnight and broadcasts a full day without anyone awake.

**Outcome.** **M2.** You go to sleep; a day is generated, rendered, mixed and pushed; you wake to a
rundown telling you what will air, and it airs. The hour lands on `:00`.

- **Hardware** — the Studio, plus its power and sleep settings hardened (§21).
- **Accounts** — offsite object storage for backups · an outbound email path for the daily digest
  and the one alert · a password manager entry for `BACKUP_ENCRYPTION_KEY`.
- **Content** — **C7 pool pieces**, enough to back-time from — needed here because back-timing draws
  on the pool roughly 24 times a day from the first night. §35 gates C7 on steps 10 and 13c: this
  phase is step 10 and needs *some* pool, **F** is step 13c and is where the 37-piece minimum is
  reached and `make pool-check` goes green.
- **Depends on** — B (somewhere to push to), D (something worth pushing).

**Completes in ARCHITECTURE:** §13 the clock contract and back-timing · §14 the nightly batch and
freshness tiers · §14a the rundown · §17 the `make` surface · §20 failure behaviour ·
§24 logging and the daily digest · §25 errors, timeouts, idempotency · §26's performance budgets ·
§28 backups and retention · §4's process model — the model load windows and the poller under
launchd · §6's on-air writeback — the one-minute `now.json` poller, `coverage`, `airplay` and the
`played.log` backfill · §27's Studio posture — no inbound, Tailscale only, services on `127.0.0.1` ·
**§36's planner budget enforcement**.
**Build steps:** 9, 10, 11, 11b.

> **The planner must refuse a grid it cannot render.** §36 sets `planned_speech_minutes ≤ measured ×
> 0.8` and requires the batch planner to fail with the overage named in minutes. A measured RTF that
> nothing enforces is a number in a file; this is the mechanism that stops the station quietly
> programming more talk than the machine can make and discovering it at 04:00.
>
> **`coverage` and `airplay` are written by polling, not by the playlist.** They land here rather
> than in C because neither exists until something actually airs, and deriving them from the built
> plan instead would be wrong in exactly the state you least observe — playout fallen through to
> levels 2–5.

---

## F · Music and Imaging

**Goal.** Make it sound like a radio station rather than a podcast with music after it.

**Outcome.** **M1.** Station identity on every junction and every programme; a music show whose host
knows who played bass; the hour clock executing without anyone thinking about it. The voice-identity
question is settled and written down before the archive makes it expensive.

- **Hardware** — the Studio.
- **Accounts** — **Suno, paid plan with a commercial-use grant.** Keep the licence evidence; §18
  makes `tracks.licence_note` mandatory and the answer changes the day a third-party track enters
  the catalogue.
- **Content** — **C5 Suno catalogue** + `music/catalogue.yaml` + licence evidence · **C6 imaging
  pack** (logo, stings, beds, opens and closes, disclosure sting) + `imaging/catalogue.yaml` and its
  licence evidence · manual correction of track **and imaging** intro ramps by ear.
- **Depends on** — E.

**Completes in ARCHITECTURE:** §8 the music data model, rotation and the chart's scoring — the
chart *show* waits for K and three weeks of real airplay · §9 station imaging and the mix
specification, **including `imaging/catalogue.yaml` and `make imaging-sync`/`-analyse`/`-tag`**
(D-093) · §10 music shows and render economics · §26's remaining caches — track durations,
which the hourly playlist build depends on never re-probing, and rendered pool and imaging, which
are never invalidated because that is the point of rendering them once.
**Build steps:** 12, 13, 13b, 13c.

> **The catalogue's shape was the prerequisite and is now closed** (D-040), so C5 is a structure
> rather than a track count and F can start on the content whenever the account exists. **One §38
> decision still closes inside this phase**: voice identity at step 13b — bulk re-render versus an
> in-world host change, forced before 50 shows exist. **The music catalogue no longer shares this
> trap** — D-045 replaced voice personas with text style cards held in the repository, precisely
> because the vendor's models are on a published deprecation path.
>
> **Step 13c's `make pool-check` is the back-timing pool, not the archive.** It counts `pool_items`
> per length band (§13) and says nothing about H's 165 hours. The two are different pools with
> different floors and different checks; see H.

---

## G · Compliance and Legal

**Goal.** Make the fiction unmistakable, mark everything machine-readably, and have a professional
confirm it is enough. **This is a hard gate: no public listener before it closes.**

**Outcome.** Written sign-off from a Polish media lawyer with EU AI Act familiarity, covering the
disclosure package, the news-shaped-fiction question, the Suno commercial-use evidence, and whether
KRRiT registration applies. A `DECISIONS.md` entry recording which marking mechanisms were chosen
and why. Disclosure surviving all six playout levels, verified after push.

- **Hardware** — none new.
- **Accounts** — **a lawyer.** Long lead: start looking during C or D, engage here.
- **Content** — the written statement of what the station broadcasts, for the lawyer to review.
- **Depends on** — E (real output to gate), F (Suno licence evidence).

**Completes in ARCHITECTURE:** §18 compliance in full — **including a standalone watermarking pass
if the cast engine chosen in A does not supply one** (D-019) · §19's remaining limbs — the model
check, profanity, structural checks and the quarantine path — plus the whole gate, C's figure screen
included, reviewed end to end · §27's prompt-injection and public-repo posture.
**Build steps:** 14, 15.

> Every date and instrument named in §18 is unverified and gets checked here, against primary
> sources, with the lawyer — not against the document.
>
> **§38's Code of Practice question closes here** — whether to sign the deployer section. The
> initial-signatory window has closed; joining later remains possible, and it is a lawyer question,
> not an engineering one.

---

## H · The Archive

**Goal.** Build the 165 hours of reusable programming the grid consumes, before it is consumed.

**Outcome.** An archive deep enough that nothing recurs inside a fortnight, and an overnight block
with its own identity. **The check is a rotation simulation, not a wait:** run the archive scheduler
over a simulated 30 days at the tier the station actually ships at, and assert no item is drawn
twice inside the 14-day separation window. It either passes or it names the shortfall in hours.

- **Hardware** — the Studio, running most nights.
- **Accounts** — none new.
- **Content** — the archive itself: history documentaries and music retrospectives first, being
  time-neutral and the cheapest per render-minute.
- **Depends on** — F. **Not earlier** — 165 hours is ~165 programmes, well past the point where
  changing a presenter's voice orphans the lot (`DECISIONS.md` D-006).

**Completes in ARCHITECTURE:** §14's `A` tier and its lifecycle mechanics.
**Build steps:** 16.

> **This phase is not measured by `make pool-check`.** There are two pools and they are not the same
> thing: `pool_items` is back-timing filler — 37 pieces in three length bands, finished in F, and
> what `make pool-check` counts — while the **archive** is §14's `A` tier at a 135-hour floor and a
> 165-hour target, counted in hours and reported by the digest and the rundown. `make pool-check`
> goes green in F and stays green throughout this phase whether or not a single archive hour exists,
> so it cannot be H's check.
>
> **The simulation is the check because a fortnight cannot be waited out.** What H promises — you
> will not hear the same programme twice in two weeks — is only *audible* after the station has run
> two weeks, which is phase K. But it is fully *computable* now: the pool, the daily consumption and
> the separation window are all known, so the scheduler can be run forward over a month of synthetic
> days before a single hour airs. A shortfall comes back as a number of hours, which is exactly the
> instruction for what to do next.
>
> **165 hours is a target, not a budget (D-021).** If the simulation wants 300 or 400 hours, the
> answer is more nights of render — never a shorter separation window, and never a thinner Night
> Watch. There is no launch date (D-006), so this phase simply takes as long as it takes and
> everything after it waits. That is what makes it the longest phase and also the least risky one:
> it cannot fail, it can only run late, and running late costs nothing but calendar.

> **The longest phase by far: ~4,000 speech-minutes, roughly 19 nights of pure render and
> realistically a couple of months alongside everything else.** There is no launch date, so this is
> a long task rather than a risk (D-006) — but it cannot be compressed and it cannot start early.

---

## I · The Public Face

**Goal.** A place for the station to live that is not a raw stream URL — the player, the schedule,
and the two surfaces that bring people back without listening.

**Outcome.** A site on Vercel: the player with now-playing and the AI-disclosure line above the
fold; the week's grid; programme and presenter pages; **the world page**, a readable in-world digest
of what is happening; **the discography**, browsable; about; `/ai-transparency`; the archive.
Stale metadata says so rather than confidently showing yesterday.

- **Hardware** — none. Vercel builds it; the Studio publishes JSON snapshots.
- **Accounts** — Vercel · the domain and its DNS.
- **Content** — the About page copy and the tribute framing. Everything else is generated.
- **Depends on** — E (snapshots to read), G (disclosure copy that has been reviewed).

**Completes in ARCHITECTURE:** §16 the public web in full.
**Build steps:** 17.

> The world page and the discography are the story surfaces for the audiences who will not listen for
> hours — PRODUCT §6's worldbuilders and tabletop people. They are cheap off the existing schema and
> they are what makes the project legible to someone who arrives from a link.

---

## J · Launch and Audience

**Goal.** Turn a working station into one that people can find, follow, and support — and tell the
story of how it is made to the people who care about that.

**Outcome.** **M3.** The stream is listed and anyone can listen. There is somewhere to follow it,
somewhere to support it, and a public repo with a licence that says what may be reused.

- **Hardware** — none.
- **Accounts** — **YouTube channel** with the channel-level synthetic-content setting and the
  per-broadcast altered-content flag (§18) · **Ko-fi** · **social presence**, chosen for PRODUCT §6's
  audiences rather than for reach: somewhere for science-fiction readers and worldbuilders, and a
  devlog for the how-it's-made audience · stream directory listings.
- **Content** — **C10 the LICENSE decision** (code and canon almost certainly want different terms)
  · launch copy · the first devlog entries.
- **Depends on** — G (nothing public before sign-off), H (an archive deep enough to survive), I (a place
  to point people).

**Completes in ARCHITECTURE:** §15's YouTube relay path, including the static video card · §18's
distribution-chain limb · §27's public-repo hygiene becoming load-bearing · PRODUCT §10
sustainability, including the infrastructure and credit grant applications the About copy feeds.
**Build steps:** 18.

> **Nothing yet measures whether the station is working, and this is the phase where that stops
> being free.** PRODUCT §9 names return listening and time in stream as two of the five signals that
> matter — and the architecture has no listener telemetry of any kind. It does not need a dashboard:
> Icecast already emits per-mount connection durations, so the question is whether to collect them
> and where they land. **This is an open decision (§38), not a settled design**, and it is the one
> §38 row that has no deciding test yet.

> **Ko-fi is a compliance input, not only a donations link.** It is what puts the station outside the
> AI Act's purely-personal-use carve-out (§18), which is why G comes first.
>
> **The honest framing is the marketing.** PRODUCT §7 is explicit that if the only interesting thing
> about the station is that a machine made it, it has failed. The story is the world that keeps going
> whether or not you are listening — the convoy that was late this morning and docks this afternoon.
> Lead with that; the AI is disclosure, not a pitch.

---

## K · After

**Goal.** Let the station accumulate the thing that cannot be built in advance — history, and people
who come back for it.

**Outcome.** **M4** at ninety days: stories opened in month one have resolved, presenters refer back,
and the overnight has begun filling with the station's own retired programmes. **M5** when there are
regulars — the only milestone that cannot be engineered.

- **Hardware** — none, unless the RTF measurement argued for more.
- **Accounts** — none new.
- **Content** — ongoing canon, and whatever the world turns out to need.
- **Depends on** — J, and time.

**Completes in ARCHITECTURE:** §8's chart show, once three weeks of real airplay exist · §17's ops
panel, built from what was actually reached for in the first thirty days — which is where §38's
panel-screens question closes · §37 if the hardware improves.
**Build steps:** 19, 20.

---

## What is deliberately not a phase

- **A second station.** `scope` and `station_id` exist; nothing else does, and nothing else should
  until a second station actually exists (ARCHITECTURE §34).
- **An ops panel before day 30.** Build what you reached for, not what you imagined.
- **Anything that grades the product automatically.** Quality is judged by ear, by one person, on a
  blind sample. That is a standing rule, not a phase.
