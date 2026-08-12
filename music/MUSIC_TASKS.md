# MUSIC_TASKS.md — the whole music job, start to finish

Every piece of work needed to go from where we are today to 500 finished songs the station can play.
Nothing is left for later; if it is not on this page it is not part of the music job.

**Created 2026-08-08 by operator instruction** (D-053). It exists outside the §32 document cap and
outside `TASKS.md`'s ten-item cap, because the music content track is one long sequence and cutting
it into ten-item windows is what made it impossible to follow.

**`TASKS.md` holds no music cards. This file holds them all.**

**Numbers are identities, not order.** `M-05` names one card for the life of the project — in git,
in `RUNBOOK.md`, in `DECISIONS.md`. The order is the order the cards are printed in, and the card to
work is the one marked **NEXT**. The two stopped agreeing the first time a dependency crossed a
stage boundary, so the file was reordered on 2026-08-09 and the numbers were left alone (D-060).

---

## Who does what

| Tag | Meaning |
|---|---|
| `[agent]` | An agent does it. You do nothing but read the result and say keep or redo. |
| `[you]` | Only you can do it. Suno, ears, and judgements about the real world. |

**One card at a time, top to bottom.** A `[you]` card and an `[agent]` card may run at the same
time; two `[agent]` cards may not.

---

## How to run a card

**Open a new session in this repo and say the number.** "Do M-01." That is the whole interface.

The agent reads this file, works that one card, and stops to ask rather than guessing if the card
needs a decision from you.

### Before the session ends — every time, no exceptions

1. **Mark the card just finished `DONE`,** with the date, and add a `Result:` line saying what it
   actually produced — not what the card asked for.
2. **Mark the next runnable card `NEXT`,** and take the marker off the old one. Runnable means every
   card on its `Depends on:` line is done.
3. **Update the stage table.** Put the card just finished in that stage's **Last done** cell —
   number, name and date — and bring its **Status** cell up to date in the same edit.
4. **Tell the operator what changed and exactly how to check it.**

**A card is not finished until all four are done.** The table is the only place the state of the
whole job is visible at once, and a row that is one card out of date is worse than an empty one,
because it will be believed. Updating it is part of the work, not a note about the work.

**One card per session.** Two cards in one session is how the thread gets lost.

If you do not know where you are, say "what's next in music". The answer is always the one card
marked **NEXT**.

---

## Where we are

| Stage | Cards | Last done | Status |
|---|---|---|---|
| 0 · Tooling that needed nothing | M-01 · M-02 · M-03 | **M-03** name screening · 2026-08-09 | all done |
| **R · The re-weight** | M-43 · M-44 · M-45 · M-47 · M-46 · M-48 · M-49 | **M-43** the commission and the plan · 2026-08-12 | **M-44 next.** The files say the new numbers; the wiki does not yet |
| 1 · The pilot — 45 songs end to end | M-16 · M-17 · M-18 · M-40 · M-19 | **M-17** lyrics and prompts · 2026-08-09 | M-17's words are being redone by M-47; M-18 waits |
| 2 · The wiki — 7 genres left | M-07 … M-15 | **M-11** pulse-dance · 2026-08-11 | 435 songs written, 130 of them demoting at M-44 · M-12 is now 55 songs and waits its turn |
| 3 · Tooling that needed audio | M-04 · M-05 · M-06 | — nothing yet | blocked until M-18 |
| 4 · Style cards — the other 20 bands | M-20 | — nothing yet | blocked until M-15 **and** M-19 |
| 5 · The bulk — 8 genres, lyrics → audio → measure | M-21 … M-39 | — nothing yet | blocked until M-20 |
| 6 · Hand over | M-41 · M-42 | — nothing yet | last |

**Read the Last done column, not your memory.** Two stages run at once (below), so "the last thing
finished" is a fact about a stage, not about the project.

**Totals when this file is finished:** 9 genres · 25 bands · ~55 albums · 500 playable songs ·
~1,330 more songs that exist as text only.

**Stage R changed what the 500 are** (D-068, 2026-08-12). Deck-talk and pulse-dance stop being
records the station holds and stay in the world as text; lane-rock, Frontier Reels, old-system
sessions, void-lounge and void-ballads grow to take their place; relay-pop keeps its size and
changes its sound. **Every card printed before stage R was written against the old split** — read
its numbers as history and take the live ones from `plan.yaml`.

**M-19 is the decision point,** and it now comes fifth rather than nineteenth. Everything after it
assumes the pilot sounded right; if it did not, stages 3–6 get rewritten before they run. The pilot
needs only relay-pop, which is already written, so there is nothing to gain by writing 330 more
songs of text first and a great deal to lose.

### Stages 1 and 2 run at the same time

Stage 1's long card is **M-18 — you, at Suno, for 45 songs.** Stage 2 is all `[agent]`. So the wiki
genres get written while you are generating the pilot, which is what the `[you]`/`[agent]` split in
*Who does what* is for. Both chains have to finish before stage 4 either way.

---

# Stage 0 · Tooling that needed nothing — done

Three pieces of code that removed work from you, and depended on nothing but each other.

### M-01 · `[agent]` Ids that cannot collide, and a `make check` that reads the wiki — **DONE 2026-08-09**
Goal: The second genre written cannot silently overwrite the first, and the command tells you when a
genre does not match the plan — instead of you counting 105 songs by hand.
Files: `src/station/music/check.py`, `wiki.py`, `tests/unit/test_brief.py`, `music/CONSTANTS.md`
Check: `make check` goes red, naming the genre and the number, on a wrong song count for a label, a
layer-A song with no fact, a layer-B song that has one, a release year off the eight anchors, or any
id used twice. It is green on relay-pop exactly as it stands today.
Note: no existing id is ever renumbered — COMMISSION §10 forbids it. The counter becomes derived and
duplicates become an error.
Depends on: —

### M-02 · `[agent]` Retire the paste loop — **DONE 2026-08-09**
Goal: Six music commands become two, and the runbook stops describing a process you no longer use.
Files: `Makefile`, `src/station/cli.py`, `src/station/music/brief.py`, `music/RUNBOOK.md`, `docs/ADMIN.md`
Check: `make music-brief`, `music-check`, `music-style` and `music-songs` are gone, along with
`music/briefs/`. `make check` and `make music-albums` remain and work. `RUNBOOK.md` part 1 no longer
describes copying anything to a clipboard.
Depends on: M-07 (the first agent-written genre proves the loop is unnecessary) — **done ahead of
it by operator instruction; the brief carried nothing an in-repo agent cannot read (D-055)**

### M-03 · `[agent]` Name screening against Wikidata — **DONE 2026-08-09**
Goal: You stop googling several hundred invented names one at a time.
Files: `src/station/music/screen.py`, `Makefile`, `docs/ADMIN.md`
Check: `make music-screen GENRE=<x>` reports every band, label, album, song title and person in that
genre that has an exact-title match on a real notable person or organisation, and says nothing about
the rest. Run against relay-pop it returns a short list you can read in two minutes.
Note: exact matches only. "Reads like a famous name with a letter changed" stays a human judgement —
the tool narrows the pile, it does not clear it.
Result: relay-pop's 319 distinct names return **nothing at all** — the whole genre is clear on the
mechanical test. The screen is people and organisations only, live against the query service rather
than a downloaded extract (D-056).
Depends on: M-01

---

# Stage R · The re-weight — what kind of station this is

**Drafted in a planning session, 2026-08-12, and accepted whole.** The station's library was 47%
pop, hip-hop and house — 54% of what had actually been written — in genres the operator would never
put on. `PRODUCT.md` §9 makes the operator's own interest at ninety days a success metric and §11
names his boredom as the most likely failure of the project, so this is not a taste footnote.

The canon edit is already made: `70-music.md` no longer ranks deck-talk among the most-listened
forms, and no longer claims it travels furthest. **Everything in this stage follows that edit.**

**Nothing is deleted.** All nine forms stay canon; two of them stop being pressed. That is what
COMMISSION §1's layer B is for — *"most of the music you invent will never be recorded, and that is
correct."*

### M-43 · `[agent]` Re-weight the commission and the plan — **DONE 2026-08-12**
Goal: The files that say how much of each kind of music the station holds say the new numbers, and
stop describing deck-talk as the biggest thing on air.
Files: `music/COMMISSION.md`, `music/plan.yaml`, `src/station/music/check.py`,
`tests/unit/test_music.py`, `music/CONSTANTS.md`, `music/MUSIC_TASKS.md`
Check: `COMMISSION.md` §2's two tables read — relay-pop 105, lane-rock 110, Frontier Reels 95,
old-system sessions 90, void-lounge 55, void-ballads 25, core harmonies 20, deck-talk 0, pulse-dance
0. Relay-pop's prompt palette is power-pop, jangle, sunshine and soft rock rather than dance-pop.
The three sentences that now contradict canon are gone — §2's *"travels furthest"*, *"the
second-biggest thing the station plays"*, and *"the top four are 60% of everything"*. `plan.yaml`
adds to 500. M-12, M-13 and M-14 carry their new song counts. `make check` green.
Note: carries the **label 3 decision**. Demoting pulse-dance leaves Meridian's house with 20 songs
and one band, well under §5's floor of three bands and forty songs. It takes void-lounge's Meridian
share — a Synthesist core house pressing late-club torch is coherent, and its dance records still
exist in layer B. Label 2 drops to two bands and is repaired by M-48.
Result: `plan.yaml` re-cut to the new nine — deck-talk and pulse-dance carry no `labels:` block at
all, and the 130 songs they give up are spread as lane-rock +35, Frontier Reels +30, old-system
sessions +30, void-lounge +15, void-ballads +15, core harmonies +5. **500 songs and 25 bands still,
and every label still clears §5's floor**: void-lounge takes Meridian (25 songs, 2 bands) and the
folded house (30, 2), void-ballads takes a second Cold Harbor voice (25, 2), and the three growing
genres each add a band (D-069). `COMMISSION.md` §2 is reordered — lane-rock is now the biggest form
and relay-pop the second — and relay-pop's palette is power-pop, jangle, sunshine and soft rock with
*never dance-pop* written into it. **The three contradicting sentences are gone**, and so is §11's
60% line, which said the same thing a fourth time; the top four are 80% now. `check.py` gained one
rule: a genre may carry `owed_to: M-46` while its file is behind the plan, the count check stands
down for it, and **`make check` goes red the moment that card is marked DONE** — so a re-weight
cannot quietly disable the counting for good. Five genres carry a marker today.
Depends on: —

### M-44 · `[agent]` Demote deck-talk and pulse-dance to layer B — **NEXT**
Goal: 130 songs stop being records the station holds and become records the world merely knows about.
Files: `music/wiki/deck-talk.yaml`, `music/wiki/pulse-dance.yaml`, `music/CONSTANTS.md`,
`music/plan.yaml`
Check: neither file contains `playable: true`. No song in either carries a fact. Every band, album,
credit, bio and album story survives as text. **Both `owed_to: M-44` lines are gone from
`plan.yaml`** — `make check` goes red if they are left behind. `CONSTANTS.md` §1's anchor-year
counts and §5's label table are recounted against what is left. `make check` green.
Note: nothing is deleted. The Clearing Day origin, the disputed 2612 catalogue, the two bands who
have not shared a sleeve since 2618 — all still there for a presenter to talk about. A station that
can discuss records it does not own is the whole point of the three layers.
Depends on: M-43

### M-45 · `[agent]` The writing rules, and `make check` enforcing them
Goal: The next 400 songs cannot be the same song 400 times, because the command goes red when they are.
Files: `music/COMMISSION.md`, `src/station/music/check.py`, `tests/unit/test_music.py`
Check: `make check` goes red, naming the album, on any of — more than 40% of an album's songs sharing
a structure · fewer than 3 songs per album in third person or carrying a named character · the
echoed-answer device in more than a third · the title used as the hook in more than half · a lyric
carrying fewer than 2 of the world's own nouns · a band whose facts are more than half studio
anecdotes · layer-B albums spanning fewer than 40 distinct years · a genre file naming fewer than 3
bands that live in other genre files. Green on the wiki as it stands.
Note: **this is the anti-degradation card.** Across six sessions the counting rules in `check.py`
held perfectly — no id collision, no wrong count, no album off an anchor. The prose rules in
`COMMISSION.md` failed completely over the same span. Same agents, same instructions; the difference
is that one set went red. This moves the quality rules to the mechanism that works.
Depends on: M-43

### M-47 · `[agent]` Redo the pilot's 45 lyrics
Goal: The four pilot albums are 45 different songs instead of one song 36 times, and they sound like
the new relay-pop.
Files: `music/production/lyrics/al_001.yaml` … `al_004.yaml`, `music/production/styles.yaml`
Check: all 45 pass M-45's rules. The five style cards carry the power-pop and soft-rock palette
instead of produced dance-pop. Every song still fits the fact the wiki states about it. No band's
voice line changes.
Note: replaces M-17's output and nothing is lost — no audio exists and every `take:` block is still
null. **This is the card that unblocks you**: M-18 has nothing to generate until it lands.
Depends on: M-43, M-45

### M-46 · `[agent]` lane-rock grows to 110
Files: `music/wiki/lane-rock.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 110 playable songs split 15 / 50 / 45 across labels 2, 4 and 5; 5 layer-A bands, the fifth on
label 5. `plan.yaml`'s `owed_to: M-46` line is gone. `make check` green including M-45's rules.
Names screened.
Note: 35 new songs. Second Hitch gains a short record on label 2, the two Forge bands gain 15
between them, and label 5 gets a second hauler band beside Burn Day Wages.
Depends on: M-44, M-45

### M-48 · `[agent]` Frontier Reels grows to 95 — and label 2 gets its third band
Files: `music/wiki/frontier-reels.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 95 playable songs split 45 / 25 / 25 across labels 2, 4 and 5; 4 layer-A bands, the fourth on
label 2. Harbor Standard is back to ≥3 layer-A bands. `plan.yaml`'s `owed_to: M-48` line is gone.
`make check` green. Names screened.
Note: label 2 lost its deck-talk band in M-44 and this is where it is repaired.
Depends on: M-46

### M-49 · `[agent]` old-system sessions grows to 90
Files: `music/wiki/old-system-sessions.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 90 playable songs on label 7, across 4 layer-A bands — a fourth importer band joins the
three. `plan.yaml`'s `owed_to: M-49` line is gone. `make check` green. Names screened.
Note: canon fact 19 now names old-system sessions among the three most-listened forms while
COMMISSION §4 keeps its import house *"old, thin, precarious"*. **That tension is deliberate and
stays** — the most-loved music in the settled worlds arrives on the most fragile route, which is
what fact 17 already says and is a permanent live stake for the station.
Depends on: M-48

---

# Stage 1 · The pilot — 45 songs, end to end

The point of this stage is to find out whether the approach works while it costs four albums to
redo, not 470 songs. It uses relay-pop's four Concordance albums, which are already written — so
**nothing here waits on the rest of the wiki.**

### M-16 · `[agent]` Style cards for relay-pop's five bands — **DONE 2026-08-09**
Goal: Each band has the six lines that make it sound like the same band across three albums.
Files: `music/production/styles.yaml`
Check: `b_001`–`b_005` each have voice / backing / instruments / production / tempo range / exclude,
built from the line-ups already in the wiki. `make music-albums` shows `yes` in the STYLE column for
every relay-pop album.
Note: the voice line is fixed for the life of the band and never changes between albums.
Result: all five bands carded, and `make music-albums GENRE=relay-pop` shows `yes` on all eleven
layer-A albums. The five are spread across the form's palette on purpose — hall-recorded pop
(`b_001`), dry jangling guitars (`b_002`), the electronic end (`b_003`), a live room and hand-built
percussion (`b_004`), compact early-evening harmony (`b_005`) — because five bands in one hour on
the station's largest genre otherwise arrive as one sound. Three voice lines were already fixed by
the wiki's pronouns; **Ressa Morn (`b_004`) and Mela Jorn (`b_005`) carry none, so the cards decided
them — male and female respectively (D-061), reversible until M-30 generates them.**
Depends on: M-01 — **satisfied since 2026-08-09; this card has been runnable ever since**

### M-17 · `[agent]` Lyrics and prompts — al_001 … al_004, 45 songs — **DONE 2026-08-09**
Goal: Four complete albums of words, each song fitting the fact the wiki already states about it.
Files: `music/production/lyrics/al_001.yaml` … `al_004.yaml`
Check: 45 songs, each with lyrics opening on an instrumental-intro tag, a generation prompt built
from the band's style card plus that song's mood and one arrangement note, and an exclude line.
Every lyric passes the swap-the-nouns test. Nothing about leaving Earth. Every song has a vocal.
Note: written a whole album at a time, never song by song — one band, one room, one year. **This
card also fixes the shape of the per-album metadata block** that M-18 fills in and M-05 later reads.
Result: 45 songs of lyrics and prompts across four files. Every song carries its wiki fact, an
arrangement note, the exact Suno prompt, an exclude line, an intended intro ramp in seconds, an
intended outro type and a target duration. The three §7 distributions are aimed rather than left to
chance and land as written: 56% of songs ramp ≥8s and 20% ≥15s (§7 asks ≥40% and ≥15%), outros 31
cold / 42 fade / 27 sustain against 30/45/25, average target 3:30 exactly. **The metadata block is
one `generation:` block per album plus one `take:` per song, and M-05 reads the song first and falls
back to the album (D-062)** — so a band done in one sitting is recorded once. `al_001.yaml` carries
the field-by-field description and the other three point at it. The style card's *production* line is
bent by arrangement note where the wiki puts a record in a different room (al_001's committee
chamber, al_002's smaller second half); voice, backing, instruments and exclude are never bent.
Depends on: M-16

### M-18 · `[you]` Suno — Measure Kindly and Open Parallax, 45 songs — **waits for M-47**
Goal: The pilot's audio exists.
Files: `music/audio/`
Check: 45 keeper takes downloaded and named `music/audio/<label>/<album>/NN.mp3`. Each album's
lyrics file records the exact prompt used, the attempt count, the model version and the date.
Note: Custom mode only — never let Suno write the lyrics. Finish each band in as few sittings as
possible; a band split across two model versions will not sound like one band. **While this runs,
the agent front works stage R** — M-46 onward.
Depends on: M-47 (**not M-17** — the pilot's words are being rewritten under the new brief and the
new relay-pop palette; generating M-17's lyrics would waste the sitting)

### M-40 · `[you]` Licence evidence
Goal: Rights attach at the moment of generation, so the evidence is per month, not per project.
Files: `music/licence-evidence/`
Check: For every calendar month in which any song was generated, that month's Suno commercial-use
terms are saved as a dated PDF.
Note: do this at the **start** of each month you generate in. It cannot be reconstructed later,
which is why it sits beside M-18 and not at the end of the file where it used to. **The card opens
with your first Suno sitting and does not close until M-38.**
Depends on: M-18

### M-19 · `[you]` The fourteen-song listen — the decision point
Goal: Decide whether this approach is worth 455 more songs.
Check: You have listened to fourteen of the pilot's songs back to back, as if it were the hour, and
written down what you thought. **That listen decides everything after this card.**
Note: this is the only quality gate in the project. Nothing automated grades the product.
Depends on: M-18

---

# Stage 2 · The wiki — the seven remaining genres

**One genre at a time, in this order.** The order matters: ids and the used-names list only stay
unique in sequence, and the biggest genres first means a problem shows up while it is cheap.

Each card is the same three steps — agent writes the file, `make check` counts it, you screen the
names. **This stage is the agent front and runs beside stage 1**; it feeds nothing the pilot needs.

### M-07 · `[agent]` lane-rock — 75 songs, 4 bands — **DONE 2026-08-09**
Files: `music/wiki/lane-rock.yaml`, `music/CONSTANTS.md`
Check: 75 playable songs split 10 / 35 / 30 across labels 2, 4 and 5; 4 layer-A bands; about 7
layer-B bands and 4 layer-C figures. `make check` green. Names screened and recorded.
Result: 75 playable songs across 8 layer-A albums — Second Hitch 10 (label 2), Pipe and Hammer 21
and Ballast Weather 14 (label 4), Burn Day Wages 30 (label 5). Two cornerstones, `al_034` at 13 and
`al_039` at 12. 7 layer-B bands carrying 14 albums and 112 titles, 4 layer-C figures. Labels 2 and 4
are named here for the first time — **Harbor Standard** and **Deep Register** — and every later
genre on those labels uses those names. `make music-screen` returned nothing on 228 distinct names.
Note: `CONSTANTS.md` §3's "paste the running names list into every brief" instruction was not
followed; it records screen results instead (D-058). §5 and §6 were counting 0 with relay-pop
already written, and now count what is in the wiki.
Depends on: M-01

### M-08 · `[agent]` deck-talk — 70 songs, 3 bands — **DONE 2026-08-09**
Files: `music/wiki/deck-talk.yaml`, `music/CONSTANTS.md`
Check: 70 playable songs split 25 / 20 / 25 across labels 2, 4 and 5; 3 layer-A bands; ~7 layer-B,
~4 layer-C. `make check` green. Names screened.
Result: 70 playable songs across 10 layer-A albums — Read It Back 25 (label 2), The Long Tally 20
(label 4), The Wake Count 25 (label 5). One cornerstone, `al_055` at 13. 7 layer-B crews carrying 14
albums and 112 titles, 4 layer-C figures. Release years 2600 / 2607 / 2612 / 2619 / 2624 — 66% in
the last eight years, because §2 makes deck-talk the newest form and it has no deep layer-A past.
`make music-screen` returned nothing on 215 distinct names. Layer B's `Half a Shift` is unsigned
(D-059), the first band in the wiki with no label.
Note: labels 4 and 5 now clear §5's three-band floor, and label 2 reaches two.
Depends on: M-07

### M-09 · `[agent]` frontier-reels — 65 songs, 3 bands — **DONE 2026-08-10**
Files: `music/wiki/frontier-reels.yaml`, `music/CONSTANTS.md`
Check: 65 playable songs split 30 / 15 / 20 across labels 2, 4 and 5; 3 layer-A bands; ~6 layer-B,
~4 layer-C. `make check` green. Names screened.
Note: anchor year 2583 stands at 7 playable songs and needs 25 (COMMISSION §5). This is one of the
genres old enough to supply them — aim releases there.
Result: 65 playable songs across 8 layer-A albums — Wire and Rosin 30 (label 2), The Foundry Set 15
(label 4), Loose Cargo 20 (label 5). One cornerstone, `al_078` at 13, bringing the catalogue to 6 and
inside §5's 6–8 band. 6 layer-B bands carrying 12 albums and 96 titles, 4 layer-C figures.
`make music-screen` returned nothing on 194 distinct names. **The card asked for 2583 and got three
anchors:** 2583 goes 7 → 33 songs / 4 bands / 4 labels, 2594 goes 14 → 31 / 4 / 3, and 2607 gains the
fourth band it was missing to reach 42 / 5 / 5. **Seven of the eight anchors are now satisfied and
only 2559 is left**, which no genre can fix — recorded in `CONSTANTS.md` §1 for M-15. Labels 2, 4 and
5 all clear §5's floor, so three retrospectives are now makeable. **The three 2583 albums credit no
session player (D-063)** — `CONSTANTS.md` §2's generation starts 2592 and the elder set it calls for
has never been commissioned.
Depends on: M-08

### M-10 · `[agent]` old-system-sessions — 60 songs, 3 bands — **DONE 2026-08-10**
Files: `music/wiki/old-system-sessions.yaml`, `music/CONSTANTS.md`
Check: 60 playable songs, all on label 7; 3 layer-A bands; ~5 layer-B, ~4 layer-C. `make check`
green. Names screened.
Note: §10 forbids presenting an old-system record as archive. These are current releases that took a
long time to arrive. **Label 7 has no margin** — this is the only genre that feeds it, and 60 songs
across 3 bands is exactly §5's floor. A shortfall here cannot be made up elsewhere.
Result: 60 playable songs across 7 layer-A albums — Terrace Road Four 24 (Mars), The Shore Rounds 20
(Titan), Undershore Local 16 (Europa), all on label 7, which is **named here for the first time and
finished here: Relay Road Import**, 3 bands / 7 albums / 60 songs, exactly §5's floor with no genre
left to add to it. One cornerstone, `al_098` at 13, bringing the catalogue to 7 and still inside
§5's 6–8 band. 5 layer-B bands carrying 10 albums and 80 titles, 4 layer-C figures.
`make music-screen` returned nothing on 165 distinct names. 36 of the 60 songs land on 2619 and
2624, which is the share COMMISSION §3's *half inside the last eight years* needs from the genres
that remain; 2600 gains a third label and 2612 a fourth. **Two conventions are now fixed for this
label (D-066):** `release_year` is the year the importer put the record on sale out here and the
notes name the year it was cut in the home system, and layer-B bands whose records never came down
the road carry `label: not imported`. **The genre credits no session player (D-065)** — the eight
work in the settled worlds and these records were cut on Mars, Titan and Europa; the three layer-A
bands guest on each other's records instead.
Depends on: M-09

### M-11 · `[agent]` pulse-dance — 60 songs, 2 bands — **DONE 2026-08-11**
Files: `music/wiki/pulse-dance.yaml`, `music/CONSTANTS.md`
Check: 60 playable songs, all on label 3; 2 layer-A bands; ~5 layer-B, ~3 layer-C. `make check`
green. Names screened.
Result: 60 playable songs across 6 layer-A albums — Cordon Hours 32 and Bright Hazard 28, both on
label 3, which is **finished here: Stormline Issue, 3 bands / 8 albums / 80 songs**, comfortably
past §5's floor and with no genre left to add to it. 5 layer-B bands carrying 10 albums and 80
titles, 3 layer-C figures. `make music-screen` returned nothing on 163 distinct names. 42 of the 60
songs land on 2619 and 2624, which takes the catalogue to 222 of 435 inside the last eight years and
keeps COMMISSION §3's half-recent rule reachable — **it is now only just reachable**, because
void-lounge's 30 label-6 songs cannot be dated later than the 2612 fold. **The eighth and last
cornerstone is designated here** — `al_117` *The Long Cordon*, 13 songs — and §5's 6–8 band is now
full (D-067): M-12, M-13 and M-14 write no cornerstones. The genre is built on two facts a presenter
can lean on all night: the coast seals for a season, and the two bands have not shared a sleeve
since 2618 because one of them makes records to travel and the other makes them for one hall.
Five session players appear, several of them because the seal shut with them on the wrong side of it.
Depends on: M-10

### M-12 · `[agent]` void-lounge — 55 songs, 4 bands, and Meridian's whole layer A
Check: 55 playable songs split 25 / 30 across labels 3 and 6; 4 layer-A bands, two on each label;
at least four albums on each of the two labels, so both reach §5's six; ~4 layer-B, ~3 layer-C.
`make check` green. Names screened.
Note: label 6 folded in 2612 with a disputed catalogue — that dispute is the retrospective, so it
has to be in the album notes here. **This card finishes two labels on its own** — 6, which stands at
1 band and 15 songs, and 3, which stage R left at 1 band and 20 songs. **Meridian is the change**
(D-068): the storm-coast Synthesist house pressed the pulse-dance the station no longer holds, and
its layer A is now late-club torch. Nothing about the label's Synthesist character changes; what it
presses does. **No cornerstone** (D-067). Pulse-dance's layer B already puts one band on the folded
house, `b_059` Late Bell Set, whose two records are in the disputed catalogue.
Depends on: M-11

### M-13 · `[agent]` core-harmonies — 20 songs, 1 band
Check: 20 playable songs on label 1 across at least two albums; 1 layer-A band; ~1 layer-B, ~2
layer-C. `make check` green. Names screened.
Note: this is label 1's third band, and Concordance cannot make a retrospective without it.
Note: Odessa Vail's *Lanternlight* is fixed canon and sits in deep layer B; later performances of it
may be layer A.
Depends on: M-12

### M-14 · `[agent]` void-ballads — 25 songs, 2 bands
Check: 25 playable songs on label 2; 2 layer-A bands; ~1 layer-B, ~1 layer-C. `make check` green.
Names screened.
Note: two solo voices rather than one (D-069). The whole form is one voice and one instrument, and
25 songs from a single artist is one texture the rotation cannot separate.
Note: Corin Hale's *Station Cycles* is fixed canon and belongs here.
Depends on: M-13

### M-15 · `[agent]` The catalogue-wide pass — and the wiki freezes
Goal: The three rules that are properties of the whole catalogue, not of one genre, are satisfied.
These cannot be checked a genre at a time, and fixing them is free now and expensive once songs
exist against them.
Files: `music/wiki/*.yaml`, `music/CONSTANTS.md`
Check: All nine files together give exactly 500 playable songs and 25 layer-A bands. Every one of
the eight anchor years carries ≥25 playable songs across ≥4 bands and ≥2 labels. There are 6–8
cornerstone albums of 12–14 songs. Every label has ≥3 bands, ≥6 albums and ≥40 songs. At least four
bands have ≥18 songs. Every session player appears across ≥3 labels and inside their active years.
`make check` green on all of it.
**Four jobs added by the stage R planning session (2026-08-12).** All text-only, all far cheaper
before the wiki freezes than after:

1. **Spread layer B across the calendar.** All 80 layer-B albums sit on the same eight anchor years,
   so two hundred years of music history happened on eight days. `COMMISSION.md` §3 only ever asked
   for *most* releases on the anchors; `CONSTANTS.md` §1 hardened that to *only*, and `check.py`
   enforces it on both layers. Layer B has no floor to hit and should be carrying the other years.
2. **Make the genre files reference each other.** 60 named bands across the written genres and
   **zero** cross-file mentions — each genre is a sealed world, which is why the wiki reads as a
   database rather than an industry.
3. **Move the anchor-year stories into the wiki.** `CONSTANTS.md` §1 already holds eight good
   accounts of what happened in each anchor year, but that file is a working file the station never
   reads — `check.py` takes only the eight numbers out of it. A `Night Record` year programme is
   supposed to be built on those stories and currently cannot reach them.
4. **Decide the missing present.** Nothing in the catalogue is dated later than 2624 while the
   present is 2626, and because the present is the real year plus six hundred, that gap widens every
   January. The chart needs ≥80 current songs (§5) and has none. Either give a small tier a derived
   release year — the `clock.py` rule applied to the catalogue — or redefine the chart in
   `PROGRAMMING.md` as most-played rather than new-release.

Note: fixes here are edits to release years and label assignments — text only, no lyrics affected.
**The wiki freezes when this card closes.** No lyrics are written before it does, other than the
pilot's, which are already frozen by M-19. **Anchor year 2559 is unsatisfiable as written** —
COMMISSION §3 puts layer A in 2566–2626, so no playable song can carry that year, and §5 asks every
anchor for 25 of them. One of the two rules has to give, and this card is where you decide which.
Depends on: M-14

---

# Stage 3 · The tooling that needed audio

Three pieces of code that could not be written before there were files to run them against. They sat
at the top of this file for a day under the numbers M-04 … M-06 and blocked nobody, because nothing
depends on them until stage 5.

### M-04 · `[agent]` `make music-analyse` — the three numbers, measured not estimated
Goal: You never hand-time 500 intro ramps.
Files: `src/station/music/analyse.py`, `Makefile`, `pyproject.toml`, `docs/ADMIN.md`
Check: `make music-analyse` reads every file under `music/audio/` and writes each song's duration,
seconds until the first sung word, and outro type (`cold`/`fade`/`sustain`). On the pilot's 45 songs
its ramp figures are within half a second of your ear on a spot-check of ten.
Note: ARCHITECTURE:1008 already specifies this pass and says onset detection gets the ballpark while
the last half-second is a listening judgement. So the tool measures and flags the borderline ones;
you re-listen only to those. **Not started** — the commit titled `M-04` (012a32e) contains M-07's
work and the message is simply wrong.
Depends on: M-18 (needs real audio to run against)

### M-05 · `[agent]` `make music-tag` — licence and compliance into every file
Goal: 500 files carry their own licence period, generation date, model version and AI marker without
you touching one.
Files: `src/station/music/tag.py`, `Makefile`, `docs/ADMIN.md`
Check: Every file under `music/audio/` carries all four tags. Reading any one file's tags tells you
what licence it was made under and that it is machine-generated.
Note: the four values come from the per-album metadata block M-17 defines and M-18 fills in. There
is nothing for this card to read until both have run.
Depends on: M-04

### M-06 · `[agent]` `music/catalogue.yaml` — the file the station reads
Goal: The wiki, the lyrics and the audio become the one file the station's database ingests. **This
is what makes a DJ able to say a fact about a record.** Without it the whole wiki is inert.
Files: `src/station/music/catalogue.py`, `music/catalogue.yaml`, `Makefile`, `docs/ADMIN.md`
Check: `make music-catalogue` produces `music/catalogue.yaml` in the shape ARCHITECTURE §17
specifies — labels, artists, albums, tracks with `file`, `category`, `mood`, `intro_ramp_sec`,
`outro_type`, `licence_note` — covering every playable song, and layer-B titles as unplayable rows.
`make check` validates it.
Note: the database ingest (`make music-sync`) belongs to the phase that has a database. This card
produces the file; nothing here needs Postgres.
Depends on: M-04, M-05

---

# Stage 4 · Style cards for the rest

### M-20 · `[agent]` Style cards for the other 20 bands
Goal: Every layer-A band in the catalogue has a fixed voice.
Files: `music/production/styles.yaml`
Check: All 25 layer-A bands have a six-line card. `make music-albums` shows `yes` in the STYLE
column for every playable album in every genre.
Note: this is the card both chains converge on — it needs the wiki frozen **and** the pilot judged.
Depends on: M-15, M-19

---

# Stage 5 · The bulk — one genre at a time, finished before the next starts

**A genre goes lyrics → audio → measured, and only then does the next one begin.** M-30 depends on
M-21, not on M-29: relay-pop's audio needs relay-pop's words and nothing else. Pairing them means a
problem shows up after ~60 songs instead of after 455, and it is what M-39's own note already asks
for — *"run after each genre's audio lands rather than once at the end."*

Suno work inside one genre is still done **one band at a time and in as few sittings as possible**
(COMMISSION §9): models get retired mid-project and a band split across two versions will not sound
like one band. The pairing changes which genre you sit down to, never how a band is generated.

**M-40 is open throughout.** Every calendar month you generate in needs its licence PDF saved at the
start of that month.

| Order | Lyrics `[agent]` | Audio `[you]` | Songs |
|---|---|---|---|
| 1 | M-21 relay-pop — the remaining 7 albums | M-30 relay-pop — the remaining 3 bands | 60 |
| 2 | M-22 lane-rock | M-31 lane-rock — 4 bands | 75 |
| 3 | M-23 deck-talk | M-32 deck-talk — 3 bands | 70 |
| 4 | M-24 frontier-reels | M-33 frontier-reels — 3 bands | 65 |
| 5 | M-25 old-system-sessions | M-34 old-system-sessions — 3 bands | 60 |
| 6 | M-26 pulse-dance | M-35 pulse-dance — 2 bands | 60 |
| 7 | M-27 void-lounge | M-36 void-lounge — 3 bands | 40 |
| 8 | M-28 core-harmonies | M-37 core-harmonies — 1 band | 15 |
| 9 | M-29 void-ballads | M-38 void-ballads — 1 band | 10 |

### M-21 … M-29 · `[agent]` Lyrics and prompts — 51 albums, 455 songs
Files: one file per album under `music/production/lyrics/`
Check: every song has lyrics, a generation prompt and an exclude line; every lyric passes the
swap-the-nouns test; every song has a vocal. M-21 writes `al_005.yaml` … `al_011.yaml`.
Note: **extra passes go to the cornerstone albums.** Six to eight of them each carry a whole
56-minute programme; the rest is rotation and nobody leans in. Weight the effort accordingly.
Depends on: M-20 for M-21; thereafter each genre's lyrics card depends on the previous genre's
**audio** card being finished — that is what "one genre at a time" means.

### M-30 … M-38 · `[you]` Suno — 455 songs
Files: `music/audio/<label>/<album>/NN.mp3`
Check: every song in that genre has a keeper take, downloaded and named, with the prompt, attempts,
model version and date recorded in the album's lyrics file. Custom mode only.
Note: **these are the long cards.** M-19 tells you how long 45 songs take you; multiply. Each
depends on its own genre's lyrics card and on nothing else.
Depends on: M-21 for M-30, M-22 for M-31, and so on down the table.

### M-39 · `[agent]` Measure and tag every song
Goal: All 500 songs carry a real duration, a measured intro ramp, an outro type and their licence
tags. **Run after each genre's audio lands, not once at the end.**
Check: `make music-analyse` and `make music-tag` cover all 500. No song is missing a ramp. The
distribution matches COMMISSION §7 — ≥40% of songs have ≥8 seconds before the first sung word, ≥15%
have ≥15 seconds, roughly 30% cold / 45% fade / 25% sustain, average duration near 3:30.
Note: where the distribution misses, the fix is choosing different takes, not editing the numbers —
which is the whole reason this runs per genre. Finding it at 500 songs is finding it too late.
Depends on: M-05, and each genre's audio card as it lands. Closes when M-38 does.

---

# Stage 6 · Hand over

### M-41 · `[agent]` The catalogue file, complete
Goal: The station has one file it can ingest, covering everything.
Check: `make music-catalogue` produces `music/catalogue.yaml` with all 500 playable tracks — each
with its file path, category, mood tags, measured ramp, outro type and licence note — plus every
layer-B title as an unplayable row. `make check` green.
Depends on: M-06, M-39

### M-42 · `[you]` The full listen
Goal: Confirm the catalogue works as an hour, not as a spreadsheet.
Check: You have listened to fourteen consecutive songs from three different hours — a label
retrospective, an anchor year, and a plain music sequence — and each held up.
Note: if it does not hold up, the fix is more songs or different takes, not a different tool.
Depends on: M-41

---

## When this file is finished

- [ ] 9 genres written, checked and screened — ~1,700 songs of text
- [ ] 25 bands with a fixed voice
- [ ] ~55 albums with lyrics and prompts in git
- [ ] 500 songs with audio, a measured ramp, a duration and an outro type
- [ ] Every audio file carrying its own licence tags
- [ ] `music/catalogue.yaml` complete and validated
- [ ] Licence evidence for every month generated in
- [ ] You have listened, twice — at M-19 and at M-42

Then the music job is done, and it hands over to the phase that has a database.
