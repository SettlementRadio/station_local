# CONSTANTS.md — the catalogue's fixed points

> **Working file, not a document.** Called for by `COMMISSION.md` §12 Stage 0. Its whole purpose is
> to be pasted into every Brief A. Nothing reads it automatically; it exists so that seven label
> batches written weeks apart still line up with each other.
>
> **Present = 2626** (real year + 600, recomputed every year — never write an age here).

---

## 1. The eight anchor years

`Night Record` plays *"one label or one year"*. A year is only a programme if **≥25 tracks across
≥4 artists and ≥2 labels** landed on it, which is why these are fixed once and every batch aims at
them.

| Year | What happened | Binds to |
|---|---|---|
| **2559** | Odessa Vail's *Lanternlight* première became the Lumen Festival's test piece; ensembles and singers across competing labels scheduled responses and rival readings around it | slot 1 |
| **2583** | The complete *Station Cycles* entered general circulation; stations commissioned new performances while artists released answers to Corin Hale's life-support drone | slot 2 |
| **2594** | The first freight-circuit burn festival linked crews, port halls and frontier dancers, prompting labels on and off the lanes to release records for the route | slots 5, 2 |
| **2600** | Shipboard presses adopted a shared format, clearing years of recording backlogs and letting hauler crews distribute releases beyond their usual lanes | slot 5 |
| **2607** | Meridian's storm-coast studios reopened after a season of closures; finished records, postponed sessions and new Synthesist collaborations arrived together | slot 3 |
| **2612** | A major late-club label folded and its catalogue became disputed; former artists made new recordings while other labels issued tributes, rebuttals and opportunistic signings | **slot 6 — this is its fold year** |
| **2619** | The altered-credit edition of an Adra Pell and Lio Tern recording surfaced; reply songs, split-vocal partnerships and competing versions filled release calendars | many |
| **2624** | Concordance's largest public recording hall reopened after structural repairs; labels booked a season of live sessions and released them before demand for the room outran access | slot 1 |

**Window check** (§3): six anchors inside the last thirty-five years, two in the old-standards
window. Correct as specified.

**State after M-49 (2026-08-13): seven of the eight are satisfied** — ≥25 playable songs across ≥4
bands and ≥2 labels. In order: 2583 · 33/4/4 · 2594 · 36/5/3 · 2600 · 39/5/3 · 2607 · 50/6/5 ·
2612 · 40/5/4 · 2619 · 133/14/6 · 2624 · 69/8/5. One falls short, and it is the one no card can fix:

- **2612 has its margin back.** M-46 repaired it from 25 songs across 3 bands to 33/4/4, which sat
  exactly on §5's floor of four bands; The Ninefoot Cut's *Everything Comes By Water* puts a fifth
  band on it and it reads 40/5/4. **No anchor now stands on the floor**, and 2583 at 33/4/4 is the
  thinnest of the seven.
- **2559 cannot be fixed by writing more.** COMMISSION §3 puts layer A in 2566–2626, so no playable
  song can carry 2559 at all; it stands at zero. M-15 is where that contradiction gets resolved.

**These counts move again.** M-12, M-13 and M-14 add 100 playable songs, so the line above is where
the catalogue stands today rather than where it is going. M-15 is where the finished state is
checked against §5.

**This table is read by `make check`.** The eight years in the first column are the only release
years any album in any genre may carry, and `src/station/music/check.py` takes them from here
rather than keeping a second copy. Each row must keep its `| **YYYY** |` shape; if it stops
matching, `make check` stops with a message saying so rather than quietly finding no anchors.

**Consequences to carry into the slot cards.** Four anchors have already committed facts about labels
that do not exist yet, and those commitments are binding:

- **Slot 6 folded in 2612**, and its catalogue is *disputed* — that is the retrospective.
- **Slot 3's studios closed for a season and reopened in 2607.**
- **Slot 5 was part of the first burn festival (2594)** and gained reach from the shared press
  format (2600).
- **Slot 1 owns both ends** — the Vail première and the hall reopening.

**Slots 4 and 7 carry no anchor of their own.** That is fine and intended: every anchor needs at
least two labels on it, so Forge and the import house should be landing releases on *other* labels'
years rather than getting one each. Field 9 of their slot cards points at years in this table —
**never invent a ninth anchor.**

---

## 2. The session players

They appear across **≥3 labels each** (§6). This is the cheapest way to make the discography feel
like an industry, and Mira's card is written to notice exactly this — her habit is to name the
overlooked player before giving an opinion.

> ### Players have careers, not eternities
>
> A session career runs about **thirty-five years**, so no single set can cover the catalogue's
> eighty-year span. **The eight below are one generation: they work 2592–2626** — the current and
> last-generation windows, which hold roughly 85% of the catalogue.
>
> **Brief 0b — the elders — will not be written. Operator decision, 2026-08-10 (D-064).** The
> old-standards window (2546–2591) was to get its own set of three or four players. It does not get
> one. **A layer-A record made before 2592 credits its band members and nobody else** — that is 33
> songs across 4 albums, and it is the finished state, not a gap waiting to be filled. Do not invent
> an elder to fill it and do not credit any of the eight below outside their dates.
>
> **Nobody has dates yet.** Every player needs an `active_from` and `active_to` before the first
> credit is written, or a batch will credit someone to a session they were eleven years old for.
>
> **The eight work in the settled worlds, and old-system sessions credits none of them (D-065).**
> Every record in that genre was cut on Mars, Titan, Europa or Earth, and none of the eight has been
> down the road. It is the second permanent hole after D-064's pre-2592 window — 90 songs across 11
> albums after M-49 — and it is not one to fill: a second roster for the home system is the same
> brief D-064 declined. What carries the industry feel there is the genre's own bands guesting on
> each other's records, and, for the Earth band nobody can reach, a round that came down the road
> and a record that went back up it.

| Name | Instrument | Character |
|---|---|---|
| **Ivena Sorn** | resonance pipes | Marks every tuning on her cuffs and refuses another take once the room has settled around the instrument |
| **Miro Olt** | synth-harpsichord | Keeps several voicings ready; hired when a crowded arrangement still needs space for the singer |
| **Nessa Dray** | composite fiddle | Carries two bows, lends neither, and can change a dance tempo from one glance across the room |
| **Brin Noll** | oxygen-tank drums, stripped-wire chimes | Retunes the room's loose metal before the engineers place a microphone |
| **Oren Saye** | upright bass | Discards the chart after one run-through and remembers every singer's original key |
| **Talla Venn** | fretted composite guitar | Repairs the same scarred instrument between sessions; keeps a handwritten record of every tuning |
| **Deym Rusk** | piano, compact studio keyboards | Arrives with the arrangement copied out, then removes half of it once the band starts playing |
| **Sel Ardin** | backing vocals, vocal arrangement | Says little in rehearsal but can build a full chorus around an uncertain lead before the session breaks |

Both canon signature instruments are covered — resonance pipes and synth-harpsichord — and a vocal
arranger is the right eighth pick, since §7 forbids instrumentals and every track needs its voices
worked out.

---

## 3. The running names list

**Paste this into every Brief A** under *"names already used, do not reuse or echo"*, and add to it
after every batch. Without it the writer reinvents the same three surnames all year.

**Screened and cleared — 2026-08-04.** No exact full-name match with any notable real person.

Ivena Sorn · Miro Olt · Nessa Dray · Brin Noll · Oren Saye · Talla Venn · Sel Ardin

**The written genres are screened by `make music-screen GENRE=<x>`, not by this list.** Every name a
genre uses is in its own `music/wiki/<genre>.yaml`, so a second copy here would only go stale. What
is recorded is the result:

| Genre | Screened | Distinct names | Result |
|---|---|---|---|
| relay-pop | 2026-08-09 | 319 | nothing matched |
| lane-rock | 2026-08-13 | 267 | nothing matched — rescreened whole after M-46 grew it to 110 |
| deck-talk | 2026-08-09 | 215 | nothing matched |
| frontier-reels | 2026-08-13 | 231 | nothing matched — rescreened whole after M-48 grew it to 95 |
| old-system-sessions | 2026-08-13 | 201 | nothing matched — rescreened whole after M-49 grew it to 90 |
| pulse-dance | 2026-08-11 | 163 | nothing matched |

Notes kept because §19 says fuzzy and surname-only matches are flagged, never blocked:

| Name | What came up | Verdict |
|---|---|---|
| **Ivena Sorn** | *Sorn* is the mononym of a real, notable Thai singer | keep — but it is a **musician**, so the flag is worth remembering if the name ever moves to a lead artist |
| **Oren Saye** | *Owen Saye*, a hockey player, one letter away | keep — below the notability floor and a different first name |
| **Miro Olt** | *Miro* is a well-known software company; Joan Miró surname-only | keep — organisations are screened too, but "Miro Olt" is clear |
| Nessa Dray · Brin Noll · Talla Venn · Sel Ardin | surname-only echoes only | keep, unremarkable |
| **Corah Ames** · **Kell Moray** | *Ames* and *Moray* are both real places; neither is a person | keep — surname-only, and the first names are invented |
| **Saira Dunn** · **Bran Teale** | common surnames, nothing notable at the full name | keep, unremarkable |

**Flagged — operator decision, not yet cleared:**

| Name | Why |
|---|---|
| **Deym Rusk** | Reads as a filed-off *Dean Rusk* — US Secretary of State, Wikipedia in dozens of languages. The search engine itself suggested the correction unprompted. Passes the mechanical rule (fuzzy, not exact) and fails the §8 litmus test, which asks whether a reader could name the source. **Recommend replacing.** |

**From canon, already fixed and not to be reinvented:**
Odessa Vail · Corin Hale · Adra Pell · Lio Tern

**Rejected on screen, never reuse:**

*(none yet — record every rejection here so the same collision is not proposed twice)*

---

## 4. Id counters — derived, never written down here

So two genres written weeks apart never collide.

**There is no number to keep in this section.** The next free song, album and band id is the
highest one already in `music/wiki/` plus one — `station.music.wiki.next_free_ids()`, which any
agent writing a genre reads before it numbers anything. A hand-kept counter is exactly how the
second genre comes to reuse the first one's ids: it goes stale the moment someone forgets to edit
it.

`make check` fails, naming both uses, if any song, album, band or figure id appears twice across
the nine genre files. Label ids, session players and band members are allowed to repeat — the same
label and the same hired player turn up in every genre they worked in — provided every use gives
them the same name.

**An id is never renumbered once committed** (`COMMISSION.md` §10). Titles can be edited; identity
cannot. A correction takes the next free id, never a recycled one.

---

## 5. The tallies — tick off as genres land

**The planned numbers are not here.** They live in `music/plan.yaml`, which `tests/unit/test_music.py`
enforces — 500 songs, 25 bands, and every label ending with at least 3 bands and 40 playable songs.
Keeping a second copy in this file would only let the two drift.

Run `make check`: it confirms both that the plan adds up and that every written genre matches it —
except a genre `plan.yaml` marks `owed_to:`, which a card has not finished growing yet (D-069).
**This section tracks only what has actually been written.**

Layer-A bands and playable songs only. §5 needs every label to end on ≥3 bands and ≥40 songs.

| # | Label | Name as written | Bands written | Songs written |
|---|---|---|---|---|
| 1 | Concordance, prestige | Civic Lantern | 2 | 45 |
| 2 | Cold Harbor, frontier | Harbor Standard | 3 | 60 |
| 3 | Meridian, dance | Stormline Issue | 1 | 20 |
| 4 | Forge, industrial | Deep Register | 3 | 75 |
| 5 | haulers, co-op | Common Wake Cooperative | 4 | 95 |
| 6 | late-club, folded 2612 | Lower Bell Editions | 1 | 15 |
| 7 | old-system importer | Relay Road Import | 4 | 90 |

**The table above is what is written today, recounted after M-49** (2026-08-13). M-44's demotion had
taken a band and 25 songs off label 2, a band and 20 off label 4, a band and 25 off label 5, and all
of label 3's layer A but one band and 20 songs (D-068); M-46 put 35 songs and one band back, M-48
put 30 more, and M-49 adds 30 and a fourth band to label 7, which never lost anything and is the one
label the re-weight grew rather than repaired. **Three labels are still short of §5's floor** of
three bands and forty songs — label 1 by a band only, labels 3 and 6 by both. Labels 2, 4, 5 and 7
clear it, and labels 5 and 7 now clear it twice over.

**Which card finishes which label**, once the re-weight is done — the numbers are in
`music/plan.yaml` and are not repeated here:

| Label | Short of | Finished by |
|---|---|---|
| 1 Concordance | a third band | **M-13** core-harmonies |
| 2 Cold Harbor | nothing — **M-48** landed its third band | **M-14** void-ballads adds two more |
| 3 Meridian | two bands and twenty songs | **M-12** void-lounge, which now presses for Meridian |
| 4 Forge · 5 haulers | nothing — both clear the floor without help | **M-46** and **M-48** added to both |
| 6 late-club | two bands and twenty-five songs | **M-12** void-lounge, on its own |
| 7 Relay Road Import | nothing — **M-49** took it to 4 bands and 90 songs | finished |

**The cornerstone list stands at six** (D-067, recounted at M-44). It was full at eight until
`al_055` *Count It Twice* and `al_117` *The Long Cordon* went down to layer B with their genres — a
record the station does not hold cannot carry a 56-minute programme, so neither is a cornerstone any
more. What is left is `al_001`, `al_009`, `al_034`, `al_039`, `al_078` and `al_098`, all 12 or 13
songs, which is inside §5's 6–8 band **with no margin under it**. D-067 stands unchanged: M-12, M-13
and M-14 designate none. Whether the two freed slots are handed to a later genre is the operator's
call and has not been made.

## 6. The genre tally

Layer A songs per form. `music/plan.yaml` is the authority; this is the running count. **Every
target below is the stage R target** (D-068), and the last column names the card that closes the
gap. **No genre now carries an `owed_to:` marker in `plan.yaml`** — every written genre matches the
plan, and the three not written at all need no marker, because an empty file is skipped.

| Form | Target | Written | Owed to |
|---|---|---|---|
| Lane-rock | 110 | 110 | — |
| Relay-pop | 105 | 105 | — |
| Frontier Reels | 95 | 95 | — |
| Old-system sessions | 90 | 90 | — |
| Void-lounge | 55 | 0 | M-12 |
| Void Ballads | 25 | 0 | M-14 |
| Core Harmonies | 20 | 0 | M-13 |
| **Deck-talk** | **0 — layer B** | **0 — demoted at M-44** | — |
| **Pulse-dance** | **0 — layer B** | **0 — demoted at M-44** | — |
| | **500** | **400** | |

**400 of the 500 are written, and stage R is finished.** The other 100 are all in the three genres
not yet written — void-lounge, void-ballads and core harmonies. The 130 songs deck-talk and
pulse-dance gave up are still in the wiki and still readable; they are titles now, like the rest of
layer B.

**Layers B and C are not tallied.** They have no hard floor — more is better, and nothing breaks if
one genre carries more history than another.
