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

**The accounts are `music/wiki/anchors.yaml` and are not repeated here** (M-15). What is left is the
index: the year, the one phrase that names it, and the label it binds. A second copy of eight
stories in a file nothing reads is how the two come to disagree.

| Year | In a phrase | Binds to |
|---|---|---|
| **2559** | the *Lanternlight* première — **layer B only, and permanently** (D-079) | slot 1 |
| **2583** | the *Station Cycles* in general circulation | slot 2 |
| **2594** | the first freight-circuit burn festival | slots 5, 2 |
| **2600** | shipboard presses adopt a shared format | slot 5 |
| **2607** | Meridian's storm-coast studios reopen | slot 3 |
| **2612** | Lower Bell Editions folds, catalogue disputed | **slot 6 — this is its fold year** |
| **2619** | the altered-credit edition surfaces | many |
| **2624** | the Long Assembly reopens | slot 1 |

**Window check** (§3): six anchors inside the last thirty-five years, two in the old-standards
window. Correct as specified.

**Final state, M-15 (2026-08-14): the wiki is frozen and these counts cannot move.** Seven of the
eight carry layer A and all seven are satisfied — ≥25 playable songs across ≥4 bands and ≥2 labels.
In order: 2583 · 39/5/4 · 2594 · 42/6/4 · 2600 · 51/7/5 · 2607 · 62/8/6 · 2612 · 52/7/4 · 2619 ·
160/18/6 · 2624 · 94/12/6. The thinnest is 2583, and it is clear of §5's floor on every count.

- **2559 is settled, not short** (D-079). COMMISSION §3 puts layer A in 2566–2626, so no playable
  song can carry that year and none ever will; it stands at zero and that is the finished state. It
  stays an anchor because it is the year *Lanternlight* was premièred and the year every competing
  house scheduled itself around — layer B carries it, and the way it reaches the air is `al_163`,
  seven of the cycle's twelve movements recorded in 2624. §5's year edition is built from the other
  seven. **Do not widen §3's window to fill it, and do not drop the row.**

**The stories have moved out of this section** (M-15, job 3). The eight accounts of what happened in
each year now live in `music/wiki/anchors.yaml`, with the records each year actually produced beside
them, because `PROGRAMMING.md`'s year edition is built on those stories and could not reach them
here — this is a working file the station never reads. **The table above stays**: `check.py` reads
the eight years out of its first column, which is all it ever read.

**The anchors now bind layer A only** (§12 rule 7, D-081). Every playable album sits on one of the
eight; layer B was re-dated across 2552–2626 and now carries 55 distinct release years, with 38
albums left on an anchor because the anchor's own event is their story.

**This table is read by `make check`.** The eight years in the first column are the only release
years a **layer-A** album may carry — layer B carries the rest of the calendar (§12 rule 7) — and
`src/station/music/check.py` takes them from here rather than keeping a second copy. Each row must
keep its `| **YYYY** |` shape; if it stops matching, `make check` stops with a message saying so
rather than quietly finding no anchors.

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
> one. **A layer-A record made before 2592 credits its band members and nobody else** — that is 39
> songs across 5 albums after M-14, and it is the finished state, not a gap waiting to be filled. Do
> not invent an elder to fill it and do not credit any of the eight below outside their dates.
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
| **Calo Meret** | piano, compact studio keyboards | Arrives with the arrangement copied out, then removes half of it once the band starts playing |
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
| void-lounge | 2026-08-13 | 153 | nothing matched |
| core-harmonies | 2026-08-14 | 43 | nothing matched — rescreened after M-15 retitled `al_161` *Nobody Had a Seat*, the only new name in the catalogue |
| void-ballads | 2026-08-14 | 44 | nothing matched |
| **independents** | 2026-09-02 | 221 | nothing matched **on the second run** — see below. Not a genre: this is the July collection (`wiki.COLLECTIONS`), 42 bands · 75 albums · 135 titles, M-53 |

**The collection's first run found two, and both were moved rather than argued about** (M-53). The
rule is D-009's — an exact full-name match against an entity with ≥5 sitelinks — and these were the
first two hits in nine screens:

| Name | What came up | Verdict |
|---|---|---|
| **The Commons** | *House of Commons*, 81 sitelinks — an institution, not a musician | **moved.** Nobody would mistake an unsigned orbital protest record for a parliament, but the title was a generic two-word noun phrase carrying no work of its own. Vera Cross's record is now **Hands Off the Air**, after the song on it |
| **Wings** | the real band, 40 sitelinks | **moved, and it was not a close call** — §8 rule 1 forbids a real band's name outright. It is a layer-B title on `al_223` and is now **Patchwork Wings (Late Cut)**, which is what that take is |

Both were retitled and the whole collection rescreened the same day: 221 distinct names, nothing
matched.

Notes kept because §19 says fuzzy and surname-only matches are flagged, never blocked:

| Name | What came up | Verdict |
|---|---|---|
| **Ivena Sorn** | *Sorn* is the mononym of a real, notable Thai singer | keep — but it is a **musician**, so the flag is worth remembering if the name ever moves to a lead artist |
| **Oren Saye** | *Owen Saye*, a hockey player, one letter away | keep — below the notability floor and a different first name |
| **Miro Olt** | *Miro* is a well-known software company; Joan Miró surname-only | keep — organisations are screened too, but "Miro Olt" is clear |
| Nessa Dray · Brin Noll · Talla Venn · Sel Ardin | surname-only echoes only | keep, unremarkable |
| **Corah Ames** · **Kell Moray** | *Ames* and *Moray* are both real places; neither is a person | keep — surname-only, and the first names are invented |
| **Saira Dunn** · **Bran Teale** | common surnames, nothing notable at the full name | keep, unremarkable |

**Flagged — none outstanding.**

**Rejected on screen, never reuse:**

| Name | Why |
|---|---|
| **Deym Rusk** | Read as a filed-off *Dean Rusk* — US Secretary of State, Wikipedia in dozens of languages; the search engine suggested the correction unprompted. It passed the mechanical rule (fuzzy, not exact) and failed §8's litmus test, which asks whether a reader could name the source. **Replaced by Calo Meret**, who is the eighth player in the table above and appears across five labels in five genre files. Deym Rusk appears nowhere in `music/wiki/` and never did — the replacement was made as the genres were written and only the record of it was missing, which M-15 closed. |

**From canon, already fixed and not to be reinvented:**
Odessa Vail · Corin Hale · Adra Pell · Lio Tern

All four are now written into the wiki and are not to be written again. **Odessa Vail is `b_073` in
`core-harmonies.yaml`**, layer B, with *Lanternlight* as `al_164` dated 2559 and a seven-movement
layer-A performance of it in 2624 (M-13). **Adra Pell and Lio Tern are `b_006` Pell and Tern in
`relay-pop.yaml`**, layer B. **Corin Hale is `b_076` in `void-ballads.yaml`**, layer B, with the
*Station Cycles* as `al_169` dated 2583 — twelve songs, unplayable, and unplayable permanently: the
rota at Verrin Reach lets anybody copy them and lets nobody sell them, so no house has ever pressed
them and the station cannot hold them (M-14).

*(the rejection list is above, with the flags it came from.)*

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
| 1 | Concordance, prestige | Civic Lantern | 3 | 65 |
| 2 | Cold Harbor, frontier | Harbor Standard | 5 | 85 |
| 3 | Meridian, dance | Stormline Issue | 3 | 45 |
| 4 | Forge, industrial | Deep Register | 3 | 75 |
| 5 | haulers, co-op | Common Wake Cooperative | 4 | 95 |
| 6 | late-club, folded 2612 | Lower Bell Editions | 3 | 45 |
| 7 | old-system importer | Relay Road Import | 4 | 90 |

**The table above is the finished state, recounted after M-14 and confirmed unchanged by M-15**
(2026-08-14) — the catalogue-wide pass moved release years and prose, and no song, band, album or
label assignment with it. The wiki is written and frozen:
500 playable songs, 25 layer-A bands, 63 layer-A albums, and every one of the seven labels clear of
§5's floor of three bands, six albums and forty songs. M-44's demotion had taken a band and 25 songs
off label 2, a band and 20 off label 4, a band and 25 off label 5, and all of label 3's layer A but
one band and 20 songs (D-068); M-46 put 35 songs and one band back, M-48 put 30 more, M-49 added 30
and a fourth band to label 7, M-12 put two bands and 25 songs on label 3 and two bands and 30 songs
on label 6 — the two labels the re-weight left standing on nothing — M-13 put a third band and three
albums on label 1, and M-14 put two bands, four albums and 25 songs on label 2, which needed none of
them. **Label 3 is the only label sitting on the floor exactly**, at 3 bands, 6 albums and 45 songs.
Label 2 finishes furthest past it, at 5 bands, 11 albums and 85 songs.

**Which card finishes which label**, once the re-weight is done — the numbers are in
`music/plan.yaml` and are not repeated here:

| Label | Short of | Finished by |
|---|---|---|
| 1 Concordance | nothing — **M-13** took it to 3 bands, 7 albums and 65 songs | finished |
| 2 Cold Harbor | nothing — **M-48** landed its third band | **M-14** added two more and 25 songs |
| 3 Meridian | nothing — **M-12** took it to 3 bands, 6 albums and 45 songs | finished |
| 4 Forge · 5 haulers | nothing — both clear the floor without help | **M-46** and **M-48** added to both |
| 6 late-club | nothing — **M-12** took it to 3 bands, 6 albums and 45 songs | finished |
| 7 Relay Road Import | nothing — **M-49** took it to 4 bands and 90 songs | finished |

**The cornerstone list stands at six** (D-067, recounted at M-44). It was full at eight until
`al_055` *Count It Twice* and `al_117` *The Long Cordon* went down to layer B with their genres — a
record the station does not hold cannot carry a 56-minute programme, so neither is a cornerstone any
more. What is left is `al_001`, `al_009`, `al_034`, `al_039`, `al_078` and `al_098`, all 12 or 13
songs, which is inside §5's 6–8 band **with no margin under it**. D-067 stands unchanged: **M-12,
M-13 and M-14 designated none**, and the longest album any of them wrote is seven songs. **The wiki
is written, so six is now the finished number** unless the operator reopens it — the two freed slots
can only be filled by promoting an existing album, which is an edit to `cornerstone:` and to nothing
else. That call has not been made.

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
| Void-lounge | 55 | 55 | — |
| Void Ballads | 25 | 25 | — |
| Core Harmonies | 20 | 20 | — |
| **Deck-talk** | **0 — layer B** | **0 — demoted at M-44** | — |
| **Pulse-dance** | **0 — layer B** | **0 — demoted at M-44** | — |
| | **500** | **500** | |

**All 500 are written.** Nine genre files, seven of them carrying layer A, and no card owes any
genre a song. The 130 songs deck-talk and pulse-dance gave up are still in the wiki and still
readable; they are titles now, like the rest of layer B.

**COMMISSION §3's half-recent rule closes at 254 of 500** — 51%, over half, and no longer a running
requirement handed from card to card. M-14 put 13 of its 25 on 2619 and 2624 against the 9 D-077
asked for, because the two records that had to be old were old for reasons in the story: Cold
Harbor's first void ballad record could only be the year the *Station Cycles* went round, and the
second could only be the year records started travelling. The chain of shares ends here: 56%
(D-073) → 49% → 48% → 51% (D-076) → 36% (D-077) → **satisfied**.

**Layers B and C are not tallied.** They have no hard floor — more is better, and nothing breaks if
one genre carries more history than another.
