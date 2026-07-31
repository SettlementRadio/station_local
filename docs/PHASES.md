# Settlement Radio — Phases

*The road from nothing to a station with listeners. Eleven phases, each with a goal, an outcome you
can see or hear, and what it needs before it can start.*

> **Ownership: the operator's.** Agents read this **only in a planning session** (ARCHITECTURE §33),
> where one phase is turned into `TASKS.md` cards. It is not read during normal work and it
> generates no tasks by itself.
>
> **This document says *what* and *when*. `ARCHITECTURE.md` says *how*.** Each phase names the
> architecture sections it completes and does not restate them; each phase names the §35 build steps
> it contains and does not re-describe them. If a detail appears here that also appears there, there
> is the one that is right.

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
| **D** | The Voice | *go/no-go* | A, C |
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
| **Imaging + jingles** (C6) | **F** | **~30 jingle sets** — one per strand, each an open, close and bed, plus a sting for news — and the station furniture on top. Call it 100+ pieces | after F's Suno account |
| **Music catalogue** (C5) | **F** | *undecided — see below* | after F's Suno account |
| **The archive** | **H** | ~4,000 speech-minutes, ~165 hours | **not before F** (D-006) |
| **LICENSE decision** (C10) | **J** | code and canon almost certainly want different terms | **now** |

**Four items can start before any hardware arrives** — canon, banned entities, cast drafting and
`grid.yaml`. Canon is the big one: it gates phase C and is the largest single thing only the
operator can make.

> **Imaging is not "a pack."** The grid has around thirty named strands and ARCHITECTURE §17a makes
> a `jingle_set` mandatory for every one of them, so this is a hundred-odd short pieces, not a dozen.

> **The music catalogue has no stated size anywhere in the documentation**, and the missing number
> is not a track count. §8 gives rotation weights and separation rules but never says how big the
> catalogue must be — and the grid asks a harder question than "how many tracks".
>
> The station airs **four music-led hours a day** (`Night Record` at 23:04 and three Night Watch
> hours), and §10 puts a 56-minute music show at 14 tracks: **~56 track-plays a day**. But three of
> those four hours are archive-class, so their tracks are chosen when the *show* is generated and
> replayed with it — the pool bakes the selection in.
>
> **The real constraint is catalogue shape, not size.** `Night Record` is "one label or one year";
> the Night Watch runs label retrospectives, artist profiles and single-album stories. None of those
> can be made from a flat pile of unrelated tracks — they need labels with several artists, artists
> with real discographies, and albums with enough tracks to carry a story. So C5 is specified as a
> *structure*, and the track count falls out of it:
>
> > *n* labels × artists per label × albums per artist × tracks per album
>
> Six labels, three or four artists each, two or three albums apiece at eight to ten tracks lands
> near **450–500 tracks** — and, more usefully, says to generate music in album-shaped batches with
> credits rather than as singles. **Decide the structure before phase F starts** and record it;
> the numbers above are an illustration, not a decision.

---

## A · Foundations

**Goal.** Establish that the machine can do the work at all, before any pipeline exists.

**Outcome.** Two numbers written into `DECISIONS.md`: the measured sustained TTS real-time factor,
and a written verdict on whether a 9–12B local model writes radio worth broadcasting. A repo that
lints, types and tests green on an empty project.

- **Hardware** — Mac mini M4 16GB + external Thunderbolt SSD 2TB. Nothing in this phase starts
  without both.
- **Accounts** — Hugging Face (model downloads).
- **Content** — none.
- **Depends on** — nothing.

**Completes in ARCHITECTURE:** §21 repo layout · §22 toolchain · §23 config and secrets ·
§2's model table resolved to real artifacts · §36 both measurements.
**Build steps:** 0, 0b, 1, and §36.2's cold read.

> **The cold read is model-bound, not hardware-bound.** Whether a 9–12B model writes usable radio is
> a property of the model, so it can be answered on rented hardware months before the mini arrives.
> The RTF measurement cannot — "on this machine" means the mini.

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
chain · §27's transmitter firewall posture.
**Build steps:** 2.

> **Keep it unlisted and access-restricted until G closes.** A public stream before the legal review
> raises a placing-on-the-market question that has not been asked yet (§18).

---

## C · The World

**Goal.** A world that keeps its own time, with a canon behind it that retrieval can actually reach.

**Outcome.** `make tick` advances threads, schedules beats, and writes items — and the result is
readable prose you can judge. Retrieval returns the right facts for a hand-written query.

- **Hardware** — the Studio, from A.
- **Accounts** — none new.
- **Content** — **C1 canon seed** (~150 facts, all seventeen domains present) and **C8
  `banned-entities.yaml`**. C1 is the largest single operator item in the project and gates most of
  what follows; start it the moment A's cold read passes.
- **Depends on** — A.

**Completes in ARCHITECTURE:** §5 knowledge architecture · §6 the world · §7 canon ingestion ·
§13's clock and phrase renderer · §26's indexes.
**Build steps:** 3, 4, 5, 6, 7.

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
- **Depends on** — A, C.

**Completes in ARCHITECTURE:** §3 both seams and their conformance · §11 shows and the script
schema · §11a register, direction and DNA · §12 the voice pipeline · §17a `grid.yaml`.
**Build steps:** 8.

> **This is the go/no-go.** If the answer is no, the choice is larger hardware or a small paid budget
> for flagship scripts — not more architecture. Nothing in E onward is worth starting until it lands.

---

## E · The Day

**Goal.** The station runs itself overnight and broadcasts a full day without anyone awake.

**Outcome.** **M2.** You go to sleep; a day is generated, rendered, mixed and pushed; you wake to a
rundown telling you what will air, and it airs. The hour lands on `:00`.

- **Hardware** — the Studio, plus its power and sleep settings hardened (§21).
- **Accounts** — offsite object storage for backups · an outbound email path for the daily digest
  and the one alert · a password manager entry for `BACKUP_ENCRYPTION_KEY`.
- **Content** — **C7 pool pieces** (37 minimum across three length bands) — needed here because
  back-timing draws on the pool roughly 24 times a day from the first night.
- **Depends on** — B (somewhere to push to), D (something worth pushing).

**Completes in ARCHITECTURE:** §13 the clock contract and back-timing · §14 the nightly batch and
freshness tiers · §14a the rundown · §17 the `make` surface · §20 failure behaviour ·
§24 logging and the daily digest · §25 errors, timeouts, idempotency · §28 backups and retention.
**Build steps:** 9, 10, 11, 11b.

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
  pack** (logo, stings, beds, opens and closes, disclosure sting) · manual correction of track
  intro ramps by ear.
- **Depends on** — E.

**Completes in ARCHITECTURE:** §8 the music data model, rotation and the chart · §9 station imaging
and the mix specification · §10 music shows and render economics.
**Build steps:** 12, 13, 13b, 13c.

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

**Completes in ARCHITECTURE:** §18 compliance in full · §19 the content safety gate ·
§27's prompt-injection and public-repo posture.
**Build steps:** 14, 15.

> Every date and instrument named in §18 is unverified and gets checked here, against primary
> sources, with the lawyer — not against the document.

---

## H · The Archive

**Goal.** Build the 165 hours of reusable programming the grid consumes, before it is consumed.

**Outcome.** A pool deep enough that nothing recurs inside a fortnight, and an overnight block with
its own identity. `make pool-check` green.

- **Hardware** — the Studio, running most nights.
- **Accounts** — none new.
- **Content** — the archive itself: history documentaries and music retrospectives first, being
  time-neutral and the cheapest per render-minute.
- **Depends on** — F. **Not earlier** — 165 hours is ~165 programmes, well past the point where
  changing a presenter's voice orphans the lot (`DECISIONS.md` D-006).

**Completes in ARCHITECTURE:** §14's `A` tier and its lifecycle mechanics.
**Build steps:** 16.

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
- **Depends on** — G (nothing public before sign-off), H (a pool deep enough to survive), I (a place
  to point people).

**Completes in ARCHITECTURE:** §15's YouTube relay path · §18's distribution-chain limb ·
PRODUCT §10 sustainability.
**Build steps:** 18.

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

**Completes in ARCHITECTURE:** §8's chart, once three weeks of real airplay exist · §17's ops panel,
built from what was actually reached for in the first thirty days · §37 if the hardware improves.
**Build steps:** 19, 20.

---

## What is deliberately not a phase

- **A second station.** `scope` and `station_id` exist; nothing else does, and nothing else should
  until a second station actually exists (ARCHITECTURE §34).
- **An ops panel before day 30.** Build what you reached for, not what you imagined.
- **Anything that grades the product automatically.** Quality is judged by ear, by one person, on a
  blind sample. That is a standing rule, not a phase.
