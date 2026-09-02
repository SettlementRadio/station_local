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
| **R · The re-weight** | M-43 · M-44 · M-45 · M-47 · M-46 · M-48 · M-49 | **M-49** old-system sessions grows to 90 · 2026-08-13 | **all done.** §12's rules 1–6 are live and green; 7–8 stay owed to M-15. No genre carries an `owed_to:` marker any more |
| 1 · The pilot — 45 songs end to end | M-16 · M-17 · M-18 · M-40 · M-51 · M-19 | **M-19** the fourteen-song listen · 2026-08-16 | **done, and the pilot passed.** 45 takes on Suno Pro v5.5, filed, licensed, measured and tagged · **the operator has listened and said yes**, so stages 4–6 run as written · **M-40 stays open until M-38, and M-51 is open and unstarted** — it counts the two licence rules that are still prose, and belongs before the next generator's first pile is filed |
| 2 · The wiki — the catalogue-wide pass | M-07 … M-15 | **M-15** the catalogue-wide pass · 2026-08-14 | **finished. The wiki is frozen.** 500 playable songs across 9 genre files, 25 bands and 63 albums · every label clears §5's floor · layer B carries 55 release years · all eight of §12's rules as they then stood live and green (M-50 has since made it ten) |
| 3 · Tooling that needed audio | M-04 · M-05 · M-06 | **M-06** `music/catalogue.yaml` · 2026-08-16 | **all done.** The takes are measured (D-083), tagged (D-084), and joined into the one file the station's database ingests — 1,358 tracks, 45 of them playable, checked against the wiki by `make check` (D-085) |
| **D · The duration rule** | M-50 | **M-50** three verses and a word floor · 2026-08-16 | **done.** §12 is ten rules: 3 verse sections and **288 sung words**, both live and green, with the pilot's four albums exempt by id and their 72 failures counted where they can be seen. Solos are §7 prose for lane-rock, Frontier Reels and void-lounge |
| **4 · Style cards — the other 20 bands** | M-20 | **M-20** style cards for the other 20 bands · 2026-08-16 | **done.** All 25 layer-A bands carry a six-line card and every one of the 63 playable albums reads `yes` in `make music-albums`. The three soloing forms name their break instrument on the card; the two forms that take no solo exclude one. Two lead voices were decided here (D-089) |
| **5 · The bulk — 7 genres, lyrics → audio → measure** | M-21 … M-39 | **M-25** old-system sessions' lyrics, 90 songs across 11 albums · 2026-08-29 | **M-34 is in progress and stays NEXT — 44 of 90 filed, 2026-08-31 and 2026-09-01**, measured, tagged and in the catalogue. `al_098` … `al_102` are all complete, so **Terrace Road Four and The Shore Rounds are finished bands** and neither is split across generators. **354 of the 500 playable songs now exist.** 46 takes are owed — Undershore Local and The Ninefoot Cut, both untouched — and the operator will make them on a different generator with its own licence evidence. **2026-09's licence PDF is not captured yet** (M-40, D-098) |
| **7 · The July collection** | M-52 · M-53 · M-54 · M-55 · M-56 | **M-53** the collection, written · 2026-09-02 | **the collection exists in the world; none of its audio is filed yet.** `music/wiki/independents.yaml` carries **42 bands, 75 albums and 135 songs — 77 the station holds and 58 titles it can only name**, all `label: unsigned`, all re-dated into 2613–2621 so the whole shelf is `gold` and none of it crowds the 500. `make check` green, the names screened clean at 221, D-100 written. **The card's 46 albums was not reachable** — `check.py` keys the fact rule on the album's layer, so 33 bands needed a layer-B record of their own (D-100). **M-54 is NEXT**: copy the 135 takes out of `music/audio/RAW/` into `music/audio/unsigned/`, write the stub lyrics files and widen the July licence note. It is an agent card, so it cannot run beside M-34. Stage 7 must close before M-42 |
| 6 · Hand over | M-41 · M-42 | — nothing yet | last |

**Read the Last done column, not your memory.** Two stages run at once (below), so "the last thing
finished" is a fact about a stage, not about the project.

**Totals when this file is finished:** 9 genres · 25 layer-A bands · **63** layer-A albums ·
500 playable songs · **858** more songs that exist as text only. Counted off the wiki on 2026-08-25
and agreeing with `music/catalogue.yaml`'s own totals; the earlier figures here — ~55 albums and
~1,330 text-only — predated D-068's re-weight and M-15's catalogue-wide pass.

**Stage R changed what the 500 are** (D-068, 2026-08-12). Deck-talk and pulse-dance stop being
records the station holds and stay in the world as text; lane-rock, Frontier Reels, old-system
sessions, void-lounge and void-ballads grow to take their place; relay-pop keeps its size and
changes its sound. **Every card printed before stage R was written against the old split** — read
its numbers as history and take the live ones from `plan.yaml`.

**M-19 is the decision point,** and it now comes fifth rather than nineteenth. Everything after it
assumes the pilot sounded right; if it did not, stages 3–6 get rewritten before they run. The pilot
needs only relay-pop, which is already written, so there is nothing to gain by writing 330 more
songs of text first and a great deal to lose.

### Where the two fronts are now

**The two fronts have merged into one line, and it runs from here to the end.** Stages 0, R, 1, 2
and 3 are all closed: the wiki is frozen, the tooling exists and is green on the pilot, and
**M-19 passed on 2026-08-16**, which was the one decision everything after it was conditional on.
Nothing is blocked on a judgement any more.

**Stage 5 was 455 songs and 285 of them are left, and it alternates.** M-50 has fixed the writing
rules the pilot showed were needed, M-20 has given the other twenty bands a fixed voice, and stage 5
goes genre by genre — an `[agent]` lyrics card and a `[you]` Suno card at a time, a genre finished
before the next one starts. That pairing is the point: a problem shows up after about sixty songs
instead of after 455. The two cards inside one genre cannot overlap, so **the sessions take turns
rather than running side by side.**

**Three genres are finished and the fourth has its words.** Relay-pop is 105 of 105, lane-rock is
110 of 110, and Frontier Reels closed on 2026-08-28 (M-33) — 95 takes generated, filed, measured and
tagged, every one of them matching its written lyric exactly. **M-25 closed on 2026-08-29** —
old-system sessions' 90 lyrics across 11 albums, written and green on all ten of §12's rules, and
written at the word floor plus eleven because M-39 asked for that in writing. **M-34 is next and it
is yours**: 90 takes, four bands, one band per sitting, and the four bands sound less like each other
than any genre so far — a Mars tram works canteen, four voices in a Titan lake yard, a cold Europa
gallery and a lock house on eleven miles of Earth canal.

**Filing a pile is now `make music-dispatch`** rather than something an agent works out each time.
Point it at the export folder; it reads the lyric out of every file's own tags, proves the whole pile
one-to-one before it moves anything, and refuses a take under 2:00. `docs/ADMIN.md` has the rest.

**One thing the pilot did not settle**, and it is the operator's own words: *"I do expect to have
better variety in the future with more styles."* The pilot is one genre on one label and could not
have shown variety. Stage 5 is where it either arrives or does not, and the place to judge it is
after the second or third genre's audio lands — not at M-42, when 455 songs exist.

**Nothing automated will tell you.** `make music-analyse` measures ramps and durations and
`make music-catalogue` puts them where the station can read them; neither says whether an hour of
this is worth hearing. Only a listen does. That was true at M-19 and it stays true for every genre
after it — which is why M-42 exists at the end, and why it should not be the first time you sit
down with a whole hour of the bulk.

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

### M-44 · `[agent]` Demote deck-talk and pulse-dance to layer B — **DONE 2026-08-12**
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
Result: both files carry an empty layer A and a comment saying why; the five layer-A bands moved
down whole and their sixteen albums with them (D-070). **322 songs survive as titles** — 182
deck-talk, 140 pulse-dance — with every bio, album story, credit and mood tag intact; the 130
`fact:` lines are the only prose that went, because a fact is what a presenter says over a record
that is playing. `plan.yaml` is clear of both `owed_to: M-44` lines and now records the layer-B band
counts the demotion produced, 10 and 7. **305 of the 500 playable songs stand**, exactly as
`CONSTANTS.md` §6 predicted, and §5's label table lands on the four rows it predicted too — label 3
down to 1 band and 20 songs, labels 2, 4 and 5 each down a band. **Two things the card did not
foresee.** `al_055` and `al_117` stop being cornerstones, so **the list falls from eight to six** and
sits on §5's floor with no margin (D-070). And **anchor year 2612 lost its fourth band** — it is
25 songs across 3 bands and 3 labels, one band short of a programme, so M-46, M-48 and M-49 are each
now asked in `CONSTANTS.md` §1 to land a release there. `make check` green.
Depends on: M-43

### M-45 · `[agent]` The writing rules, and `make check` enforcing them — **DONE 2026-08-12**
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
Result: the eight rules are `COMMISSION.md` **§12**, and `src/station/music/writing.py` reads its
thresholds, its album floor and its two word lists out of that section rather than keeping a copy —
so editing a number in the writer's brief changes what the command does (D-071). `make check` is
green. **Three of the eight cannot be green on what is written today**, and each is owed to the card
that fixes it, in a new **Owed to** column that works exactly like `plan.yaml`'s `owed_to:` (D-069):
the rule is counted and reported, and it goes red the moment that card is marked DONE. **Rules 1–5
are owed to M-47** — the only lyrics that exist are the pilot's, and M-47's own check already says
*"all 45 pass M-45's rules."* **Rules 7 and 8 are owed to M-15**, whose job list states both in
words. Marking those two cards done today turns `make check` red with **twenty named findings**, so
the deferral cannot outlive the work. **Rule 7 replaced a rule rather than adding one:** `check.py`
required both layers to sit on an anchor year, which is exactly why layer B spans eight years
instead of forty, so `year_layers()` keys the swap to M-15 — anchors bind both layers until it
lands, layer A only afterwards. **What the rules found is worse than this card assumed.** The pilot
reports one structure across 9 of 12, 8 of 11, 11 of 11 and 8 of 11 songs; the echoed answer in 45
of 45; the title as the hook in 41 of 45; and **not one of the 45 lyrics carries two of the world's
own nouns** — §3's swap-the-nouns test passing so completely that it inverts. Rule 6 is live and
green on the wiki **with almost no margin**: the worst band is 10 studio anecdotes in 21 facts
against a ceiling of half.
Depends on: M-43

### M-47 · `[agent]` Redo the pilot's 45 lyrics — **DONE 2026-08-13**
Goal: The four pilot albums are 45 different songs instead of one song 36 times, and they sound like
the new relay-pop.
Files: `music/production/lyrics/al_001.yaml` … `al_004.yaml`, `music/production/styles.yaml`
Check: all 45 pass M-45's rules. The five style cards carry the power-pop and soft-rock palette
instead of produced dance-pop. Every song still fits the fact the wiki states about it. No band's
voice line changes.
Note: replaces M-17's output and nothing is lost — no audio exists and every `take:` block is still
null. **This is the card that unblocks you**: M-18 has nothing to generate until it lands.
Note: **§12's rules 1–5 are owed to this card** (D-071). They are counted today and reported to
nobody; marking this card DONE makes them fatal, so `make check` is what says whether the rewrite
worked. As it stands they report one structure across 9 of 12, 8 of 11, 11 of 11 and 8 of 11 songs,
the echoed answer in 45 of 45, the title as the hook in 41 of 45, and **not one lyric of the 45
carrying two of the world's own nouns.**
Result: all 45 lyrics rewritten and **§12's rules 1–5 are live and green** — marking this card DONE
made them fatal, which is what says the rewrite worked. Every song's id, title, mood, fact, intro
ramp, outro type and target duration is byte-identical to M-17's, because those come from the wiki
and from §7's distributions and were never what was wrong; §7's three distributions therefore still
land exactly where M-17 left them (56% ramp ≥8s, 20% ≥15s, 31/42/27 cold-fade-sustain, average
3:30). The albums now report a top section shape of 3 of 12, 3 of 11, 3 of 11 and 2 of 11 against a
ceiling of 40%; the echoed answer in exactly 3 songs each; the title as the hook in 5 of 12 and 5 of
11; and every one of the 45 carrying at least two of the world's own nouns. **The answering voice
was kept and the parenthesis was dropped** (D-072) — a group answering the lead is an arrangement
and now lives in the section tags and the prompts, where the two seams say it belongs. **No song
title changed**, so 25 of the 45 now take their title from an image in the lyric rather than from
the sung hook. The five style cards lose "contemporary produced pop" and "synth-pop" for §2's
power-pop, jangle, sunshine and soft-rock palette, and every one of them now excludes dance-pop
production by name; **no voice line was touched.**
Depends on: M-43, M-45

### M-46 · `[agent]` lane-rock grows to 110 — **DONE 2026-08-13**
Files: `music/wiki/lane-rock.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 110 playable songs split 15 / 50 / 45 across labels 2, 4 and 5; 5 layer-A bands, the fifth on
label 5. `plan.yaml`'s `owed_to: M-46` line is gone. `make check` green including M-45's rules.
Names screened.
Note: 35 new songs. Second Hitch gains a short record on label 2, the two Forge bands gain 15
between them, and label 5 gets a second hauler band beside Burn Day Wages.
Result: 110 playable songs across 13 layer-A albums, split exactly 15 / 50 / 45. Five new records —
Second Hitch's five-song EP `al_131` *Bay Rate* (2619, label 2), Pipe and Hammer's `al_132` *Four
Won't Fill It* (2612, 8 songs), Ballast Weather's `al_133` *The Route in Order* (2619, 7), and two
for the new band. **The fifth band is `b_061` Turn and Burn** — five haulers on the co-operative's
fastest circuit who have never stayed in a port longer than a turnaround, Synthesist, the first band
the membership voted to buy amplification for. They carry `al_134` *One Day in Port* (2619, 7) and
`al_135` *Paid by the Port* (2624, 8), and their running argument with Burn Day Wages about whether
anything should be put to a vote is the thing a presenter can use all night. **Anchor year 2612 is
repaired**: Pipe and Hammer's record of the year Saul Ravik left over the amplified pipes puts a
fourth band and a fourth label on it, and the eight anchors now stand at seven satisfied and only
2559 short — which no card can fix (`CONSTANTS.md` §1). **Rule 6 got safer, not tighter:** M-45
reported Pipe and Hammer at 10 studio anecdotes in 21 facts against a ceiling of half, and the eight
new facts are all about people, so the band now reads 10 in 29. No band in the genre is over 34%.
`make music-screen` returned nothing on 267 distinct names. **27 of the 35 new songs land on 2619
and 2624**, taking the catalogue to 161 of 340 inside the last eight years — COMMISSION §3's
half-recent rule needs 89 of the remaining 160, or 56% of everything still to be written (D-073).
Depends on: M-44, M-45

### M-48 · `[agent]` Frontier Reels grows to 95 — and label 2 gets its third band — **DONE 2026-08-13**
Files: `music/wiki/frontier-reels.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 95 playable songs split 45 / 25 / 25 across labels 2, 4 and 5; 4 layer-A bands, the fourth on
label 2. Harbor Standard is back to ≥3 layer-A bands. `plan.yaml`'s `owed_to: M-48` line is gone.
`make check` green. Names screened.
Note: label 2 lost its deck-talk band in M-44 and this is where it is repaired.
Result: 95 playable songs across 12 layer-A albums, split exactly 45 / 25 / 25. **Label 2 is
repaired and needs nothing further** — Harbor Standard now has 3 layer-A bands, 60 songs and 7
albums, past §5's floor on all three counts, and void-ballads will only add to it. **The fourth band
is `b_062` Board and Bow**, formed in Cold Harbor in 2612 by Suli Orley, the guitarist Wire and Rosin
hired off the dance floor in 2604; she sings the lead now, Alis Doone calls the figures over the top
of the band on every track, and they will not play a hall that charges the dancers more than it pays
the band. Their two records are `al_138` *Learned Off the Floor* (2619, 7) and `al_139` *We Went the
Other Way* (2624, 8), the second made in Concordance's reopened hall with four hundred Cold Harbor
dancers brought along at the label's expense. **The Foundry Set could not make a new record** — the
band stopped in 2599 and both anchors inside its life were spent — so label 4's ten are `al_136`
*Played and Never Pressed*, dance tunes Orsa Lipp kept from 2591–2599 that Deep Register issued in
2619 with a disputed credit, which is 2619's own anchor story (D-074). Label 5's five are `al_137`
*Burn Festival Set*, Loose Cargo at the first burn festival in 2594, which gives that anchor a fifth
band. **25 of the 30 new songs are dated 2619 or 2624**, so the catalogue stands at 186 of 370 inside
the last eight years and COMMISSION §3's half-recent rule now needs 64 of the remaining 130 — **49%,
against the 56% D-073 handed on.** `make music-screen` returned nothing on 231 distinct names. Rule 6
got safer again: the new band reads 0 studio anecdotes in 15 facts and no band in the genre is over
24%. **One line of existing prose changed** — `b_044` The Turning Room can no longer be the only reel
band still working, and now shares the Cold Harbor halls with the band whose singer it tried to hire.
Depends on: M-46

### M-49 · `[agent]` old-system sessions grows to 90 — **DONE 2026-08-13**
Files: `music/wiki/old-system-sessions.yaml`, `music/CONSTANTS.md`, `music/plan.yaml`
Check: 90 playable songs on label 7, across 4 layer-A bands — a fourth importer band joins the
three. `plan.yaml`'s `owed_to: M-49` line is gone. `make check` green. Names screened.
Note: canon fact 19 now names old-system sessions among the three most-listened forms while
COMMISSION §4 keeps its import house *"old, thin, precarious"*. **That tension is deliberate and
stays** — the most-loved music in the settled worlds arrives on the most fragile route, which is
what fact 17 already says and is a permanent live stake for the station.
Result: 90 playable songs across 11 layer-A albums, all on label 7. **All 30 new songs went to the
new band, because the three written ones could not take any** — every anchor inside Terrace Road
Four's and The Shore Rounds' lives is spent and both already hold 2624, Undershore Local stopped in
2612 with its last record written as its last, and the one device that would have freed a release is
the archive issue COMMISSION §10 forbids for this genre by name (D-075). **The fourth band is
`b_063` The Ninefoot Cut**, five lock and lighter crew on eleven miles of Earth canal, and the first
band from Earth ever imported — their first record reached the road head in 2607 because a clerk on
Earth misread the address on a letter meant for the Bell Yard Rounds, the band everybody out here
assumed the first Earth import would be, **and the argument about whether the house landed the wrong
band has run ever since.** Their four records are `al_140` *Ten Locks to the Sea* (2607, 7),
`al_141` *Everything Comes By Water* (2612, 7), `al_142` *Not the Band You Wrote For* (2619, 9) and
`al_143` *Somebody Sent Us This* (2624, 7), each cut two years before it was issued because Earth is
two crossings out rather than one. **Nobody guests on them and nobody can** — Earth is too far for
D-065's device, so what connects the band is a Shore Rounds pressing the importer sent up the road
in 2619 with no name on the sleeve and the round the band learned off it. **Anchor 2612 gains its
margin**: it stood on §5's floor at 33/4/4 and now reads 40/5/4, so no anchor sits on the floor
except 2559, which cannot be fixed by writing. Rule 6 is safest here of any genre — the new band
reads 0 studio anecdotes in 30 facts. `make music-screen` returned nothing on 201 distinct names.
**16 of the 30 are dated 2619 or 2624**, so the catalogue stands at 202 of 400 inside the last eight
years and COMMISSION §3's half-recent rule needs 48 of the remaining 100 — **48%, against the 49%
D-074 handed on.** **Two lines of existing prose were edited, both already false before this card**
— `al_098` claimed nothing else came down the road in a season two other records are dated to, and
dated its near-closure as *"the year before"*, which §10 forbids.
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

### M-18 · `[you]` Suno — Measure Kindly and Open Parallax, 45 songs — **DONE 2026-08-15**
Goal: The pilot's audio exists.
Files: `music/audio/`
Check: 45 keeper takes downloaded and named `music/audio/<label>/<album>/NN.mp3`. Each album's
lyrics file records the exact prompt used, the attempt count, the model version and the date.
Note: Custom mode only — never let Suno write the lyrics. Finish each band in as few sittings as
possible; a band split across two model versions will not sound like one band. **While this runs,
the agent front works stage R** — M-46 onward.
Result: **45 keeper takes exist** — 12 / 11 / 11 / 11 under `music/audio/label_1/al_001…al_004/`,
named `NN.mp3` by track number. All generated on 2026-08-15 on **Suno Pro, model v5.5, remixing
disabled**, and every one of the 45 was kept on the **first** generation (`attempts: 1` throughout).
The four `generation:` blocks carry the model, the licence period `suno-pro-2026-08`, the date and
the sittings; `al_001` took two sittings and the other three took one each.
**The takes arrived as `RAW/01.mp3 … 45.mp3` with no titles**, so the mapping to song ids was
verified rather than assumed — a silent mis-file would have put the wrong fact on the wrong record,
which is the failure the wiki exists to prevent. Three independent signals agree: the embedded Suno
timestamps run strictly in filename order; the four largest generation gaps fall exactly on the
12/11/11/11 album boundaries; and tracks whose lyrics declare a `cold` outro end **11.7 dB** more
abruptly than the rest at that alignment, while every neighbouring alignment is flat or negative.
**Provenance went into the lyrics files, not just the audio** — `music/audio/` is gitignored, so
each song's `take:` block carries its Suno id, the vendor's own creation timestamp and its file
path. A `dispatch-manifest.json` in `RAW/` records every move.
**M-40's August evidence is saved**: the complete 19-page terms PDF plus a note reading the clauses
that matter. Pro tier assigns the output to the account holder and that assignment is scoped to the
subscription term, so this evidence is what makes these 45 usable.
**The operator accepts the pilot** (2026-08-15): *"They all 100% pop, similar, but sounds OK… The
pilot works, the bands sound not identical."* Both halves are what the design predicted — the pilot
is one genre on one label, and §2's palette for it is guitar pop, so uniformity here says nothing
about the catalogue; and five bands sounding distinct is M-16's style cards doing their job.
**One measured result the operator should carry into M-39.** §7 asks for an average near 3:30 and
nothing under 2:00. The 45 average **2:29**, and **14 of them are under 2:00** — Suno missed the
per-song `target_duration` by 61.7 seconds on average, always short. The bands land 31% under 2:00 /
51% at 2:00–3:00 / 16% at 3:00–4:00 / 2% above, against §7's 0 / 28 / 42 / 30. **A fourteen-song
hour of these is about 35 minutes, not 56.** The operator has accepted the short songs; what this
changes is arithmetic downstream, not this card.
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
**Open since 2026-08-15, and 2026-08 is covered.** `music/licence-evidence/2026-08-suno-terms.pdf`
is the complete 19-page terms as of revision *March 26, 2026*, with
`2026-08-suno-licence-note.md` beside it reading the clauses that decide the question: **Pro or
Premier assigns the output to the account holder, scoped to the subscription term.** The account was
Pro with remixing disabled, so the pilot's 45 are covered. Two things to watch, both in that note —
**the page says the terms are changing soon**, so the successor needs its own dated file the moment
it takes effect; and a **Remix-enabled track stays non-commercial even on a paid tier**, so remixing
has to stay off.
Depends on: M-18

### M-51 · `[agent]` The two licence invariants that are arithmetic
Goal: A take cannot claim a licence period it was not generated in, or one with no evidence behind
it. **M-40 is a prose rule — "save the PDF at the start of each month you generate in" — and it has
already been missed once**, on 2026-09-01. §12's whole argument applies: across six writing sessions
the counted rules held and the prose rules failed, and *a rule that cannot go red is a preference*.
Files: `src/station/music/check.py` and its unit test.
Check: two things go red that are green today, and the real files stay green.
  1. **The month must match.** Every take records its own `suno_created` timestamp. A take whose
     `licence_period` names a different year-month than that timestamp goes red — so
     `suno-pro-2026-08` on a take created `2026-09-01T11:29:55Z` fails. This is the one that would
     have caught a real mistake: `al_102`'s `generation:` block was written by copying another
     album's, and had the month not been edited, five September takes would have claimed August's
     terms with nothing to say so.
  2. **The named period must have evidence.** A `licence_period` of `<vendor>-<tier>-<YYYY>-<MM>`
     requires a file in `music/licence-evidence/` whose name begins `<YYYY>-<MM>-<vendor>-`. Today
     `suno-pro-2026-08` finds `2026-08-suno-terms.pdf` and `suno-pro-2026-09` finds
     `2026-09-suno-licence-note.md`; an invented period finds nothing and fails. **Match on the
     prefix, not on a PDF specifically** — 2026-09's evidence is legitimately August's PDF, named by
     that period's note, and requiring a PDF per period would go red on a state that is correct.
Note: **the third invariant is already done.** The `<vendor>-<tier>-<YYYY>-<MM>` shape check landed
at M-34 (D-098) in `tests/unit/test_music_tag.py`; it replaced a `startswith("suno-")` that passed
`suno-x` and would have gone red on the first take from any second generator. This card is the other
two. If the shape check is better placed in `check.py` alongside these, move it and say so.
**Do this before the next generator's first pile is filed**, not after — that is the sitting where a
period gets typed for the first time and there is nothing to copy it from.
Depends on: M-06 for the take blocks, M-40 for the folder. Nothing depends on it, and it does not
block M-34.

### M-19 · `[you]` The fourteen-song listen — the decision point — **DONE 2026-08-16**
Goal: Decide whether this approach is worth 455 more songs.
Check: You have listened to fourteen of the pilot's songs back to back, as if it were the hour, and
written down what you thought. **That listen decides everything after this card.**
Note: this is the only quality gate in the project. Nothing automated grades the product.
Result: **the operator listened to the whole pilot and passed it** (2026-08-16): *"I listened to all
the songs under M-19, it sounds OK."* That is the yes, and **stages 4, 5 and 6 run as written** —
they were the ones that got rewritten if the answer had been no.
Both halves of the earlier verdict stand and are kept here because they are the standing brief for
everything after this card (2026-08-15): *"I'm OK with the pilot songs. They all 100% pop, similar,
but sounds OK. I do expect to have better variety in the future with more styles. The pilot works,
the bands sound not identical."* The uniformity is one genre on one label and §2's palette for it is
guitar pop, so **the variety the operator expects is what stage 5 is for** — eight more forms, twenty
more bands, nine style-card sets. If the catalogue still sounds like one record after M-31 or M-33,
that is the moment to stop, not M-42.
**The duration arithmetic is unchanged and is now M-39's to fix by choosing takes** (D-083, M-18):
the 45 average 2:29 against §7's 3:30 and fourteen are under 2:00, so fourteen of these make about
35 minutes, not 56. The operator has accepted the short songs twice. What it changes is back-timing
and how many songs an hour needs, not whether to carry on.
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

### M-12 · `[agent]` void-lounge — 55 songs, 4 bands, and Meridian's whole layer A — **DONE 2026-08-13**
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
Result: 55 playable songs across 9 layer-A albums, split exactly 25 / 30. **Both labels are finished
and both land on exactly 3 bands, 6 albums and 45 songs** — §5's floor on all three counts with no
margin, so six of the seven labels now clear it and only label 1 is short. **The two labels are
written as one story** (D-076): Lower Bell Editions folded in 2612 owing the Gantry Street plant two
years of pressing, and `p_juna_carrow`, who sang its second band, took a hall job on Meridian in
2617 when she could not get the records back and was still there when the season sealed — which is
why Stormline Issue started pressing the core's slow music in 2619. **She is the only person in the
wiki in two layer-A bands.** The house's founder `p_maro_deyn` plays piano in one of them, so the
fold happened to five named people rather than to a label. The four bands are `b_064` After the
Ferry, who have played the Lower Bell room three nights a week since 2594 and have made no record
since 2612 because everything they own is in a receiver's room; `b_065` Coldwater Court, whose two
records are the house's first success and its last pressing; `b_066` The Quiet Half, who paid the
reopened Concordance hall's fee themselves in 2624 after the house put its season's money into a wet
hall on the coast; and `b_067` Nine Lamps, **who refuse the core's name for what they play** and
whose objection Stormline Issue prints on the sleeve — an argument inside the world, not a tenth
form. `s_1211` is `s_1197` re-recorded under a new title, because every play of the 2612 version
pays the claimants who hold that catalogue. **Every label-6 song is dated 2612 or earlier and that
was forced**, so all 25 label-3 songs are 2619 or 2624 and the catalogue stands at 227 of 455 inside
the last eight years — one under half, and the remaining 45 need 23 recent, **51% against the 48%
D-075 handed on.** Anchor 2612 goes 40/5/4 → 52/7/4 on the house's last two records and **2583 is
now the thinnest anchor at 33/4/4**. Rule 6 reads **zero studio anecdotes across all four bands**.
`make music-screen` returned nothing on 153 distinct names. No existing prose was edited.
Depends on: M-11

### M-13 · `[agent]` core-harmonies — 20 songs, 1 band — **DONE 2026-08-14**
Check: 20 playable songs on label 1 across at least two albums; 1 layer-A band; ~1 layer-B, ~2
layer-C. `make check` green. Names screened.
Note: this is label 1's third band, and Concordance cannot make a retrospective without it.
Note: Odessa Vail's *Lanternlight* is fixed canon and sits in deep layer B; later performances of it
may be layer A.
Result: 20 playable songs across **three** layer-A albums rather than the two the card asked for, so
**Civic Lantern finishes at 3 bands, 7 albums and 65 songs** and **all seven labels now clear §5's
floor** — M-12 left two of them sitting on it with no margin and this card had the room not to
repeat that. The band is `b_072` **The Standing Gallery**, thirty-one voices who formed in the cheap
standing rail of Concordance's largest public hall out of people who could not afford a seat, and
whose argument with their house is about money and names rather than music: until 2619 Civic Lantern
paid a chorus a flat fee for a night, printed no singer's name on any sleeve, and paid its hired
players by the hour. `al_162` *Thirty-One Names* (2619, 7) prints all of them, and it happened in
that year because the altered-credit edition had made refusing into the story. `al_161` *Nobody Sat
Down* (2607, 6) was made in two days Open Parallax had booked and not used. **`al_163` *Seven
Lanterns* (2624, 7) is seven of the twelve movements of Odessa Vail's *Lanternlight*** — COMMISSION
§4 allows a later performance to be layer A, and this is the first record in the wiki a presenter can
both play and attribute to a canon figure (D-077). Vail herself is the whole of layer B, `b_073`,
with the 2559 cycle as `al_164`, unplayable. **The hall is named here for the first time** — the Long
Assembly, which four anchors' worth of records refer to and no file had named — and it shut in 2615
and reopened in 2624, which is what the twelve-year gap between the first two records is. **14 of the
20 are dated 2619 or 2624**, so the catalogue stands at **241 of 475 inside the last eight years,
over half for the first time since the re-weight**, and COMMISSION §3's half-recent rule leaves M-14
needing 9 of 25 — **36%, against the 51% D-076 handed on.** **2583 got nothing and is now the
thinnest anchor at 33/4/4**, on §5's floor for both bands and labels; M-14 is the last card that can
lift it. Rule 6 reads 2 studio anecdotes in 20 facts, and **rule 8 is already satisfied by this
file** — it names four bands that live in other genre files. `make music-screen` returned nothing on
43 distinct names. No existing prose was edited.
Depends on: M-12

### M-14 · `[agent]` void-ballads — 25 songs, 2 bands — **DONE 2026-08-14**
Check: 25 playable songs on label 2; 2 layer-A bands; ~1 layer-B, ~1 layer-C. `make check` green.
Names screened.
Note: two solo voices rather than one (D-069). The whole form is one voice and one instrument, and
25 songs from a single artist is one texture the rotation cannot separate.
Note: Corin Hale's *Station Cycles* is fixed canon and belongs here.
Result: 25 playable songs across four layer-A albums on label 2, and **the wiki's layer A is now
complete at 500 songs, 25 bands and 55 albums**. **Corin Hale is layer B and permanently
unplayable** (D-078): the canon says the *Station Cycles* were built on a relay outpost's own
life-support drone, and this file gives the reason no house has ever pressed them — Hale left them
to the outpost's rota under a rule the rota has never bent, *anybody may copy them and nobody may
sell them*. So the most-loved record in this form is one the station can talk about every night and
never play, which is COMMISSION §1's layer B doing the largest job it has been given. **Both layer-A
voices exist because of that rule.** `b_074` **Nera Ostell** was a gate clerk at the Cold Harbor
relay berth whom Harbor Standard recorded in 2583 because it wanted the form, could not sell the
Cycles, and went looking for a voice of its own; she has never sung a Hale song and is asked every
time. Her records are `al_165` *Sung at the Gate* (2583, 6) and `al_166` *Further Than I Went*
(2600, 6), and in 2612 she put her name on a rota and went out to an outpost herself. `b_075` **Aro
Vantry** built a box that holds one note — the tonic of the Cycles — and prints on every sleeve
where the note came from, unasked; `al_167` *Same Note All Night* (2619, 7) and `al_168` *Nothing
Left to Tune To* (2624, 6), the second made at Hale's own outpost, where he found the plant had been
replaced and the note was gone. **The two never meet and one will not answer the other**, which is
the thing a presenter can use all night. **2583 came off the floor**: it stood at 33/4/4, the
thinnest anchor and the only one on §5's band floor, and Ostell's first record takes it to 39/5/4 —
so the thinnest anchor is now 2594 at 42/6/4 and every anchor but 2559 is clear on every count.
2600 gains a fifth label. **13 of the 25 are dated 2619 or 2624 against the 9 D-077 asked for**, so
COMMISSION §3's half-recent rule **closes satisfied at 254 of 500**. Harbor Standard finishes at 5
bands, 11 albums and 85 songs, the furthest past §5's floor of any label. Rule 6 reads **zero studio
anecdotes across both bands**, and **rule 8 is satisfied by this file** — it names Wire and Rosin,
The Turning Room, Board and Bow, Loose Cargo and Harbor Late, five bands that live in other genre
files against the three the rule asks for. `make music-screen` returned nothing on 44 distinct
names. **No existing prose was edited**; one wrong line in `CONSTANTS.md` §1 was corrected, which
had said Cold Harbor carried no 2583 release when `al_078` has been one since M-09.
Depends on: M-13

### M-15 · `[agent]` The catalogue-wide pass — and the wiki freezes — **DONE 2026-08-14**
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

Note: **jobs 1 and 2 above are §12's rules 7 and 8, and both are owed to this card** (D-071). They
are counted today and reported to nobody; marking this card DONE makes them fatal, and job 1 also
flips `check.py`'s `year_layers()` so the anchors stop binding layer B and rule 7 starts. Today the
wiki reports 8 distinct layer-B years against the 40 rule 7 asks for. **Rule 8 is two thirds
undone**: `core-harmonies.yaml` and `void-ballads.yaml` name four and five foreign bands, and the
other six files name **zero**.
Note: fixes here are edits to release years and label assignments — text only, no lyrics affected.
**The wiki freezes when this card closes.** No lyrics are written before it does, other than the
pilot's, which are already frozen by M-19. **Anchor year 2559 is unsatisfiable as written** —
COMMISSION §3 puts layer A in 2566–2626, so no playable song can carry that year, and §5 asks every
anchor for 25 of them. One of the two rules has to give, and this card is where you decide which.
Result: **the wiki is frozen.** The six catalogue-wide checks all pass and none needed a fix — 500
playable songs, 25 bands, 63 layer-A albums, every label past §5's floor, 15 bands at ≥18 songs
against the 4 asked for, six cornerstones of 12–13, and every session player inside their dates and
across ≥3 labels. **What the card was really for is the four jobs, and all four landed.**
**Job 1 — layer B has its own calendar.** 68 of the 106 layer-B albums were re-dated across
2552–2626 and the wiki now carries **55 distinct layer-B release years** against rule 7's 40, up
from 8. **38 albums stayed on an anchor because the anchor's event is their story** — the fold, the
festival, the shared press format, the Cycles going round — so the anchors are still the busiest
years in the file (2619 carries 7, 2624 7, 2612 6) and the other two hundred years are no longer
empty. Every new year sits inside its band's own active window, and **three albums that looked
movable were not**: `al_095`, `al_097` and `al_118` are each dated by another record's prose, which
is the kind of tie only a catalogue-wide pass finds (D-081).
**Job 2 — the files reference each other.** Six of the nine named no foreign band at all; all nine
now name three or more, and every reference is a real connection rather than a name-drop —
Pipe and Hammer taking The Long Tally's pipe rig as they found it, Nera Ostell learning to hold a
list through the wall from Gate Shift Callers, The Turning Room buying nine copies off one crate and
giving eight away. **Rule 8 reads raw file text, so a band name broken across a line break does not
count**, which cost one round trip and is worth knowing before the next card writes prose.
**Job 3 — the anchor stories are in the wiki.** They are `music/wiki/anchors.yaml`, one entry per
year with the story, what the station actually holds from it, and the records a year edition would
build on. **It is not a genre**, and `wiki.written_genres()` skips it by name so it can never be
counted as a tenth form. `CONSTANTS.md` §1 keeps the eight years and the table shape `check.py`
reads, and its long accounts are gone rather than duplicated.
**Job 4 — the chart is most-played** (D-080), which is what ARCHITECTURE §8 already computed: 45%
decayed airplay, 25% requests, 20% previous position, 10% editorial nudge, and no release-date term
anywhere. It was `COMMISSION.md` §5 that read as new-release, and §5 was the file that was wrong.
**2559 stays an anchor and stays unplayable** (D-079): §5's year edition is built from the seven
anchors that carry layer A, and the way 2559 reaches the air is `al_163`, seven of *Lanternlight*'s
twelve movements recorded in 2624.
**One defect was found and fixed.** `al_161` and `al_078` were both called *Nobody Sat Down* — two
layer-A records, two labels, one name — so `al_161` and its track 1 are now *Nobody Had a Seat*
(§10 permits a title edit and forbids an id edit). It is the only new name in the catalogue and
`make music-screen` returns nothing on it. **One false line was corrected**: `al_120` said Bright
Hazard were the only Stormline Issue act working in 2624, which M-12 made untrue when it put The
Quiet Half's 2624 record on that label.
Depends on: M-14

---

# Stage 3 · The tooling that needed audio

Three pieces of code that could not be written before there were files to run them against. They sat
at the top of this file for a day under the numbers M-04 … M-06 and blocked nobody, because nothing
depends on them until stage 5.

### M-04 · `[agent]` `make music-analyse` — the three numbers, measured not estimated — **DONE 2026-08-15**
Goal: You never hand-time 500 intro ramps.
Files: `src/station/music/analyse.py`, `Makefile`, `pyproject.toml`, `docs/ADMIN.md`
Check: `make music-analyse` reads every file under `music/audio/` and writes each song's duration,
seconds until the first sung word, and outro type (`cold`/`fade`/`sustain`). On the pilot's 45 songs
its ramp figures are within half a second of your ear on a spot-check of ten.
Note: ARCHITECTURE:1008 already specifies this pass and says onset detection gets the ballpark while
the last half-second is a listening judgement. So the tool measures and flags the borderline ones;
you re-listen only to those. **Not started** — the commit titled `M-04` (012a32e) contains M-07's
work and the message is simply wrong.
Result: `make music-analyse` reads every audio file under `music/audio/` and prints its duration,
its intro ramp and its outro type, with `ALBUM=` to narrow it. **45 songs in 45 seconds**, so the
whole catalogue is about eight minutes. Nothing is written to a file: the numbers are read on
screen, and M-06 imports the module rather than a derived file.
**The vocal is found by what moves in the middle of the mix, not by level** (D-083) — a sung note's
partials glide and shake where a keyboard's sit still, and the voice is mixed centre, so the
measure is the rate of change of instantaneous frequency weighted by how equal the two channels
are. A harmonic/percussive filter, the standard first move, was tried and **made the separation
worse at five times the runtime**, so it is not there. `numpy` is the one new dependency; librosa,
which ARCHITECTURE §9 names, would have saved a dozen lines of FFT and cost eleven packages.
**Nothing is claimed that is not measured.** A run-up is reported only where the opening of the
record is clearly quieter in vocal evidence than the body of it and the rise holds; **`0.0` means
"no run-up you could talk over", not "the vocal starts at sample zero"**, and nothing here resolves
an intro under about two seconds. Every row is `firm` or `check` with the reason attached.
**What the pilot measures.** Average 2:29, shortest 1:23, longest 4:12. **Eight of the 45 have a
measurable run-up** — 6.3s to 13.3s, middle 9.9s — and 37 are singing from the top. Outros are
**23 cold · 8 fade · 14 sustain**. Fourteen rows are flagged for a listen: seven because the opening
is ambiguous, nine because the ending sits within a fifth of a second of the line between a cold
stop and a short ring, and two carrying both.
**Two things corroborate the ramps without an ear.** Six of the eight run-ups are among the nine
songs written with the longest intros, while only two of the other 36 show one at all. And the
measured ending agrees with what the brief asked for on 11 of 14 cold endings and 10 of 12
sustains — but on only 3 of 19 fades, because **Suno mostly did not fade**, which is a finding
about the takes for M-39 rather than an error in the measurement.
**The card's own check is still yours.** The eight with a run-up are the ones worth the ear — there
are not ten of them to spot-check, because the other 37 have nothing to time. `ALBUM=al_001` prints
one album at a time.
Depends on: M-18 (needs real audio to run against)

### M-05 · `[agent]` `make music-tag` — licence and compliance into every file — **DONE 2026-08-16**
Goal: 500 files carry their own licence period, generation date, model version and AI marker without
you touching one.
Files: `src/station/music/tag.py`, `Makefile`, `docs/ADMIN.md`
Check: Every file under `music/audio/` carries all four tags. Reading any one file's tags tells you
what licence it was made under and that it is machine-generated.
Note: the four values come from the per-album metadata block M-17 defines and M-18 fills in. There
is nothing for this card to read until both have run.
Result: `make music-tag` reads the `generation:` and `take:` blocks in `music/production/lyrics/`
and writes four tags into every take — `AI_GENERATED`, `AI_MODEL_VERSION`, `LICENCE_PERIOD` and
`GENERATION_DATE`. **All 45 of the pilot's files carry them, written in eight seconds.** The command
ends by printing one file's four tags in full, which is the card's own check done for you; `ALBUM=`
narrows it. **Suno's own comment — the generation id and the vendor's timestamp M-18 verified the
whole dispatch against — is untouched**, as is everything else already in the file (D-084).
**Nothing was risked to do it.** ffmpeg cannot tag in place, so each file is copied with the mp3
bitstream passed through rather than re-encoded, the copy is checked against the original before it
replaces it, and the replace is atomic — an interrupted run leaves whole files behind. Measured:
**all 45 audio streams are byte-identical before and after.** No new dependency; ffmpeg was already
required and already decoding for M-04 (§22).
**Re-running rewrites nothing** — a second pass reports 45 already correct in under two seconds,
which is what lets M-39 run this after every genre rather than once at 500 songs.
**Unlike the other music commands this one is a gate.** It exits red if a file failed, or if audio
sits under `music/audio/` that no lyrics file records a take for — the case where a file would
quietly carry no licence at all. A song whose words exist but whose audio does not reads as
`waiting for audio`, not as a failure: that is a Suno card that has not run yet.
Depends on: M-04

### M-06 · `[agent]` `music/catalogue.yaml` — the file the station reads — **DONE 2026-08-16**
Goal: The wiki, the lyrics and the audio become the one file the station's database ingests. **This
is what makes a DJ able to say a fact about a record.** Without it the whole wiki is inert.
Files: `src/station/music/catalogue.py`, `music/catalogue.yaml`, `Makefile`, `docs/ADMIN.md`
Check: `make music-catalogue` produces `music/catalogue.yaml` in the shape ARCHITECTURE §17
specifies — labels, artists, albums, tracks with `file`, `category`, `mood`, `intro_ramp_sec`,
`outro_type`, `licence_note` — covering every playable song, and layer-B titles as unplayable rows.
`make check` validates it.
Note: the database ingest (`make music-sync`) belongs to the phase that has a database. This card
produces the file; nothing here needs Postgres.
Result: `make music-catalogue` writes `music/catalogue.yaml` — **7 labels, 76 artists, 169 albums
and 1,358 tracks**, of which **45 are playable** today and 1,313 are titles with no file. It joins
the wiki, the lyrics files and the audio, re-measuring every take rather than reading M-04's numbers
out of anything (a second a song, so the pilot takes under a minute and 500 will take eight). The
file is 577KB, deterministic — two runs are byte-identical — and **committed**, which is what makes
the check below possible.
**`playable` means the audio exists and nothing else** (D-085). The 455 layer-A songs whose Suno
card has not run yet are unplayable rows today, exactly like the 858 records the world knows and the
station will never hold; the distinction disappears at M-38. `file`, `duration_sec`,
`intro_ramp_sec`, `outro_type`, `licence_note` and `category` are null together on every other row,
which is §8's invariant put in the row instead of in a convention.
**`category` is derived from §8's own definitions and nothing else.** `gold` is five in-world years
old or more, everything else is `A`, and `new`, `B`, `C` and `specialist` are never written —
`new` cannot be said at year granularity and the other three are editorial demotions nobody has
made. The pilot reads 11 heavy and 34 gold. The present year is written into the file, so
**`make check` goes red the January the wiki's present moves past it**, which forces the yearly
rebuild `CONSTANTS.md` §1 already implies.
**`make check` validates it as a separate pass** (`catalogue_check.py`), reading no audio, so it
runs in CI and on a fresh clone. It compares every id and title against the wiki, resolves every
reference, and asserts each row carries a whole take or none of one. **The failure it exists for is
a good build going stale** — a genre file edited without a rebuild, leaving the station's one source
of truth describing last week's world. Verified by making the file wrong on purpose: it goes red and
names the card to run.
**One defect was found and fixed.** Twenty-five layer-B song titles were truncated in the wiki —
`{title: Two Callers, One Sheet, track_number: 6}` splits at the comma, and valid YAML with a valid
title is why nothing had ever failed on it. All twenty-five are re-quoted across five genre files
with no other change, and `wiki.Song` now keeps what it does not recognise so the check reports the
same bug rather than shipping it. **Three places the wiki and §8 do not line up** are carried as the
wiki states them and reported on every run: `fact` is on the track row although §8's table has no
such column, `crew`/`duo`/`partnership` are written as `group` because §8 allows three words, and
**no genre file states a house style** for any of the seven labels.
Depends on: M-04, M-05

---

# Stage D · The duration rule

**Added 2026-08-16 by operator instruction**, after M-19 passed. A lettered stage, like stage R, for
the same reason: it is a mid-course correction that the numbered stages were written without.

The pilot is fourteen songs of about 35 minutes where the hour needs 56, and M-18 measured why —
Suno came in 61.7 seconds under the stated `target_duration` on average, *always* short, on all 45.
**The catalogue cannot be fixed by asking for longer songs; it has to be given more to sing.**

### M-50 · `[agent]` Three verses, a word floor, and solos where the form takes them — **DONE 2026-08-16**
Goal: The 455 songs still to be written are long enough to make an hour, and `make check` says so
before they are generated rather than after.
Files: `music/COMMISSION.md` (§7 and §12), `src/station/music/writing.py`, `tests/unit/test_writing.py`
Check: `make check` goes red, naming the album and the song, on any lyric with fewer than **3 verse
sections** or fewer than **the word floor §12 states** (section tags not counted; the floor is set by
this card, and the note below says it lands near 288). §12 gains the two rules and `writing.py` reads
both thresholds *out of that section* rather than keeping a copy, as D-071 requires. §7 says which forms carry an instrumental solo and roughly how often. Green on
everything that exists today.
Note: **the pilot's four albums are exempt by name and this is settled, not deferred** (D-087). The
operator: *"I'm OK with pilot songs. They will blend in among other songs we'll have, we won't redo
them."* Forty-five short songs in five hundred is 9% and rotation spreads them. **No card proposes
re-cutting `al_001` … `al_004`.** The exemption is four album ids written into §12, not a flag in
code, and their failures are still *counted and reported* — 27 of 45 short on verses, 23 of 45 short
on words — so the rule can be seen working today on the only lyrics that exist (D-071's mechanism,
the same one that carried §12's rules 1–5 to M-47).
Note: **the number to aim at is 3:36, and the floor is near 300 words, not 200.** §7 wants the 500 to
average 3:30 and the pilot is fixed at 2:29, so the 455 still to be written have to average 3:36.
Fitting the pilot's 45 gives **0.76 seconds per sung word** (≈79 words a minute, spread 26s either
side), and that fit is what sets the floor:

| words of sung lyric | predicted take |
|---|---|
| 200 — *the pilot's own average* | 2:28 |
| 233 | 2:54 |
| 281 | 3:30 |
| **288** | **3:36** |

So **a 200-word floor changes nothing** — it sits at the mean. Three verses of the pilot's own length
reach about 215 words and 2:44, so the verse rule does not get there on its own either. The pilot's
longest lyric is 280 words and its longest take is 4:12, so ~288 is inside what Suno has already
done. **Expect the lyrics to be about 40% longer than the pilot's**, and set the floor knowing a
floor is a minimum that the distribution sits above, not a target. Where a form takes a solo the
break buys time with no words, so the three soloing forms should need less of the increase — but
nothing measures that until lane-rock's audio lands, so do not discount the floor for it in advance.
Note: **the solo rule covers lane-rock, Frontier Reels and void-lounge** — the rock form, the
dance-tune form where a fiddle break is idiomatic, and the late-club torch that is this station's
jazz. 260 songs. Not void-ballads or core harmonies: one voice with one instrument, and thirty-one
voices, are both forms defined by not having a solo. An instrumental break is a section tag in the
lyric *and* an arrangement note in the prompt; §7 is where how-often is stated.
Note: **this card also decides what to do about §7's stated targets.** The writer aims at
`target_duration` and Suno missed it by 61.7s on all 45. Either the stated targets rise to absorb
that, or they stay the honest intent and the word floor does the work. Raise it; do not guess.
Result: **§12 is ten rules.** Rule 9 goes red on a lyric with fewer than **3 verse sections**, rule 10
on one of fewer than **288 sung words**, both naming the album and the song, and `writing.py` reads
both numbers out of §12 rather than keeping a copy. `make check` is green.
**288 is measured, not chosen** (D-088). Re-fitting the pilot's 45 with the counter's own definition
of a word — anything on a line that is not a section tag, repeats included — gives **0.763 seconds of
take per word**, and 288 words lands on **216 seconds, which is 3:36 exactly**: the average the 455
still to be written have to hit for the 500 to reach §7's 3:30. §7 gains that conversion as a table,
and the warning that the rate is relay-pop's at 110–130 BPM and the only one anyone has measured.
**§7's stated per-song targets were left alone, deliberately.** Raising every `target_duration` by
the 61.7s Suno came in short would have been a fiction — the stated target never reaches the model,
and the pilot proved the take follows the word count instead. The target stays the honest intent and
the thing you judge by ear; the words are what buy the seconds.
**The floor sits above the average on purpose, and it costs §7's bottom band.** A lyric at the floor
comes back near 3:36 and the rest sit above it, so **the 2:00–3:00 band §7 asks 28% of the catalogue
to fill is now fed by Suno's own spread rather than by design.** §7 says so in those words. The trade
is deliberate: overshooting means an hour needs thirteen songs instead of fourteen; undershooting
means the hour does not exist.
**The exemption is four ids in §12 and it is doing visible work.** `al_001` … `al_004` are exempt
from rules 9 and 10 permanently, and their failures are counted and returned marked rather than
dropped: **27 of the 45 are short on verses and all 45 are short on words.** The note above predicted
23 short on words — that was the count against a 200-word floor, and against the floor this card
actually sets it is every one of them. Nothing in the pilot changed and nothing about it will.
**Solos are §7 prose, not an eleventh rule.** Lane-rock, Frontier Reels and void-lounge take a break
in **roughly one song in three, never fewer than two on an album**, written as a section tag in the
lyric *and* an arrangement note in the prompt naming an instrument the band's style card already
lists. Whether a break is a solo or a bar of vamping is a listening judgement and §12 counts
arithmetic only. **None of the pilot's 45 carries an instrumental tag of any kind**, so this is the
untested half of the rule — M-20 puts the instrument on twenty style cards, M-39 confirms it works.
**One module became two.** M-50 took `writing.py` past §31's 400 lines, so reading §12 — the
thresholds, the two word lists, the four exempt ids — is now `src/station/music/commission.py`, and
`writing.py` only counts against it.
Depends on: M-19 — **the measurement this rests on is the pilot's, so it could not have been written
before the pilot was measured and judged**

---

# Stage 4 · Style cards for the rest

### M-20 · `[agent]` Style cards for the other 20 bands — **DONE 2026-08-16**
Goal: Every layer-A band in the catalogue has a fixed voice.
Files: `music/production/styles.yaml`
Check: All 25 layer-A bands have a six-line card. `make music-albums` shows `yes` in the STYLE
column for every playable album in every genre.
Note: this is the card both chains converge on — it needs the wiki frozen **and** the pilot judged.
Note: **M-50 runs first and this card applies it.** A style card fixes a band's instruments for the
life of the band, so a lane-rock, Frontier Reels or void-lounge band that solos needs the soloing
instrument named on its card — doing M-50 afterwards would mean revisiting twenty cards.
Result: **all 25 layer-A bands are carded and every one of the 63 playable albums reads `yes` in
`make music-albums`.** The twenty new cards carry the same six lines in the same order as M-16's
five, built from each band's line-up, home, label and movement as the frozen wiki states them.
**M-50 is applied where it lands.** Every lane-rock, Frontier Reels and void-lounge band names the
instrument that takes the instrumental break inside its own `instruments` line — lead guitar in four
of the five lane-rock bands, the amplified resonance pipes in `b_017` and traded with the fiddle in
`b_038`, the fiddle in all four reel bands, the piano in three of the four void-lounge bands and the
synth-harpsichord in `b_067`, which has no piano in its line-up. The two forms §7 forbids a solo
put **`instrumental solos` in the exclude line** rather than leaving it unsaid, so M-28 and M-29
cannot be talked into one.
**Two voices had to be decided and both are male** (D-089) — Wend Amory of `b_039` Loose Cargo and
Sabin Loch of `b_067` Nine Lamps, the only two lead singers left in the wiki with no pronoun
anywhere. Same call as D-061 and reversible on the same terms until their genre's Suno card runs.
The 25 bands now read 16 female leads to 9 male, and both decisions went to the band where a fourth
female lead would have cost the most: void-lounge would otherwise have been three low female voices,
**two of them the same singer.**
**Juna Carrow is one singer in two bands and the cards say so.** `b_065`'s voice line covers two
women who held that chair thirty years apart, which works because both are low female voices and
Carrow sang it Bela Runn's way for her first two years; `b_066`'s line names her as the same voice
now singing her own way, and the two bands are separated by everything else — a Purist room with
nothing but a piano in it against a wide empty dance hall at half the tempo.
**No line-up gained a player.** Seven bands have no backing singer in the wiki, and their cards say
`backing: none` and exclude backing vocals outright, which is a real separator rather than an
omission: `b_018` is the only lane-rock band with no voice but the lead's, and `b_038` answers its
singer with resonance pipes because there is nobody else in the band to do it. Nothing here names a
real artist, band, producer or label (§8).
Depends on: M-15, M-19, M-50

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

**Seven genres, not nine, and the counts below are the wiki's, re-read on 2026-08-25.** The R
re-weight (M-43 … M-49) moved 130 songs out of deck-talk and pulse-dance into the other five genres
and this table was never updated, so every number in it was pre-re-weight and it still listed
deck-talk as a card to work. **Deck-talk and pulse-dance carry no layer-A songs at all** — they are
the two forms the station does not hold (COMMISSION §2), their bands and albums and stories are all
layer B, and there is nothing there to write words for or generate. **`M-23`, `M-32`, `M-26` and
`M-35` were deleted on 2026-08-25 by operator decision.** Their numbers are retired with them and
are never reused, because a number is an identity here and not a position in a queue.

| Order | Lyrics `[agent]` | Audio `[you]` | Layer-A songs |
|---|---|---|---|
| 1 | **M-21 relay-pop — done** | **M-30 relay-pop — done** | 60 |
| 2 | **M-22 lane-rock — done** | **M-31 lane-rock — done** | 110 |
| 3 | **M-24 frontier-reels — done** | **M-33 frontier-reels — done** | 95 |
| 4 | **M-25 old-system-sessions — done** | **M-34 old-system-sessions · NEXT** — 44 of 90 filed | 90 |
| 5 | M-27 void-lounge | M-36 void-lounge — 4 bands | 55 |
| 6 | M-28 core-harmonies | M-37 core-harmonies — 1 band | 20 |
| 7 | M-29 void-ballads | M-38 void-ballads — 2 bands | 25 |

### M-21 · M-22 · M-24 · M-25 · M-27 · M-28 · M-29 · `[agent]` Lyrics and prompts — 59 albums, 455 songs — **M-25 DONE 2026-08-29**
Files: one file per album under `music/production/lyrics/`
Check: every song has lyrics, a generation prompt and an exclude line; every lyric passes the
swap-the-nouns test; every song has a vocal. M-21 writes `al_005.yaml` … `al_011.yaml`.
Note: **extra passes go to the cornerstone albums.** Six to eight of them each carry a whole
56-minute programme; the rest is rotation and nobody leans in. Weight the effort accordingly.
Result (M-21): **relay-pop is written — 60 songs across `al_005.yaml` … `al_011.yaml`**, and the
genre's 105 playable songs now all have words. Ten for Rain Ledger's `al_005` and `al_006`, six and
seven for Cabin Treaty's two EPs, **twelve for the cornerstone `al_009`**, seven and eight for
Evening Claim's two. Every song carries its wiki fact unchanged, an arrangement note, the exact Suno
prompt built off its band's style card, an exclude line, an intended ramp, an outro type and a target
duration. **`make check` is green on all ten of §12's rules**, which is the first time any lyrics have
had to satisfy rules 9 and 10 — the pilot's four albums are exempt by id.
**The songs are 40% longer than the pilot's and the length is bought with repeated choruses** rather
than with more verses (D-090): 288 to 346 sung words, mean 308, 18,471 words in all, which predicts a
**3:51 take against §7's 3:36 average** — the deliberate overshoot M-50 chose, and an hour of these is
thirteen songs rather than fourteen. §7's three distributions are aimed and land: **57% of songs ramp
≥8s and 17% ≥15s** (§7 asks ≥40% and ≥15%), outros **18 cold / 27 fade / 15 sustain**, which is
30/45/25 exactly, and the stated targets average 3:55 with nothing under 3:00.
**Rule 4 was the one that bound.** The wiki's titles are mostly hooks, so only 24 of the 60 choruses
sing their own title and the other 36 take their title from an image in the lyric — M-47's finding
again. Rule 3 cost little (6 of 60 use the echoed answer) and rule 2 came free (42 of 60).
**Nothing was generated and nothing was measured**: every `generation:` block and every `take:` is
null until M-30, `music/catalogue.yaml` is byte-identical, and `make music-tag` still reports 45 of 45.
Result (M-22): **lane-rock is written — 110 songs across 13 albums**, `al_032` … `al_039` and
`al_131` … `al_135`, which is the biggest genre in the catalogue and the first one that takes an
instrumental break. Five bands, five different textures, and the words are written for the
difference: `b_016`'s four shed loaders shouting the last chorus, `b_017`'s hall baritone with one
low voice under him, `b_018` with **no backing vocal at all** anywhere in three records, `b_019`'s
whole-crew chorus answering line for line, and `b_061`'s clipped mezzo with two blunt voices on short
phrases. **`make check` is green on all ten of §12's rules.**
**§7's four distributions all land.** Breaks: **37 of 110, 34%** — §7's "roughly one in three" — with
never fewer than two on an album, and every one of them on the instrument its band's card names. The
keyboard takes exactly one, on `s_1107`, which is the only place `b_061`'s "where the arrangement
asks" is asked. Ramps: **63% of songs declare ≥8s and 23% declare ≥15s** against §7's ≥40% and ≥15%.
Outros: **36 cold / 49 fade / 25 sustain**, which is 33/45/23 against 30/45/25. Targets average 4:24
with nothing under 2:55.
**The lyrics are longer than relay-pop's on purpose** (D-092): 296 to 387 sung words, **mean 317**
against M-21's 308, 34,907 words in all. §7's measured 0.746 seconds per word is relay-pop's rate at
110–130 BPM and lane-rock runs 100–172 with a break in a third of the songs, so the floor is cleared
by thirty words rather than by two. If M-39 measures this genre faster per word, that is why.
**Rule 4 was the one that bound, again, and harder.** Lane-rock titles are crew shorthand and every
one of them wants to be the hook: the first pass had six albums red on rule 4 and two at 89%. **46 of
110 sing their own title** and the other 64 take it from an image in the lyric, which is M-47's
finding arriving in a genre that resists it more than relay-pop did. Rule 1 bound next — the
verse/chorus/verse/chorus/verse/bridge shape is the natural one for this form and had to be broken up
on six albums. Rule 3 came free: **the echoed answer is on 6 of 110**, because four of these five
bands answer their lead with real voices in the arrangement instead.
**Three collisions between the wiki and the style cards were resolved the wiki's way** (D-092):
`al_033` has acoustic pipes and no backing voice because Juno Kerrick amplifies nothing until 2612
and Ade Prosk is not in the band yet, `al_132` changes bass chair and amplification halfway through
and its prompts split five to three, and `al_037` has a four-man chorus and no stripped-wire chimes
because Una Brack joins in 2604. Each is written into that album's `room:` block and kept out by its
own exclude line. Two songs are written against their own facts and keep both — `s_0272` is under
three minutes *and* at the word floor, `s_0306` has one verse sung three times — and **no guest ever
takes the break**, on any of the four tracks where a guest brings an instrument the band does not own.
**Nothing was generated and nothing was measured**: every `generation:` block and every `take:` is
null until M-31, `music/catalogue.yaml` is byte-identical, and `make music-tag` reports exactly what
it reported before — 105 correct and `87_wrong.mp3` still unclaimed, which is D-091's resting state.
Result (M-24): **Frontier Reels is written — 95 songs across 12 albums**, `al_078` … `al_085` and
`al_136` … `al_139`, which is the smallest band count of any genre so far — four — and the first
whose layer A is mostly historical: three of the four bands had stopped by 2612, and one of the
twelve records is a live album of performances made twenty years before it was issued.
**`make check` is green on all ten of §12's rules.**
**The dance floor is the fifth instrument and the arrangement notes treat it as one.** It claps the
count in on `s_0635`, sings a whole chorus unaccompanied on `s_0643`, is paid at the door on `al_079`
because the band made that the condition, is absent from exactly one track in the genre (`s_0647`,
where the room tone changes with it), and is four hundred Cold Harbor dancers carried to the core at
a label's expense on `al_139`. **Eleven of the 95 are about who gets paid** — a door price, a hall
fee, a wage packet, a bench with the money on it, a fee handed over in a corridor — which is what
`s_0637`'s promoter and `s_1130`'s hall keeper have in common with each other and with §3's rule that
the world supplies the furniture and never the subject.
**§7's four distributions all land.** Breaks: **31 of 95, 33%** — §7's "roughly one in three" —
never fewer than two on an album, and every one of them on the instrument that band's card names,
which for `b_038` means the fiddle and the pipes trading it. Ramps: **73% declare ≥8s and 19%
≥15s** against §7's ≥40% and ≥15%; the overshoot is deliberate and larger than lane-rock's,
because a reel sets its tune before anybody sings and Suno still comes in early. Outros: **29 cold /
43 fade / 23 sustain**, which is 31/45/24 against §7's 30/45/25 — the closest any genre has come.
Targets average 4:05 with nothing under 3:20.
**The lyrics are the longest yet and the tempo is why** (D-095): 296 to 395 sung words, **mean 340**
against M-22's 317 and M-21's 308, 32,290 words in all. §7's measured 0.746 seconds per word is
relay-pop's rate at 110–130 BPM; this genre runs 118–184 and every band's card floor is above
relay-pop's ceiling, so words go past faster and the floor has to be cleared by fifty rather than by
thirty. If M-39 measures this genre short per word, that is why.
**Rule 4 bound hardest of the three genres so far.** Frontier reel titles are dance-floor shorthand
and every one of them wants to be the hook: the first pass had **nine of the twelve albums red on
rule 4 and two of them at 100%**. 43 of 95 sing their own title and the other 52 take it from an
image in the lyric. Rule 1 bound next, on six albums, because a reel is a shape people dance to and the
shape does not want to vary — the fix was turnarounds, called figures, pre-choruses and read-aloud
sections, not different songs. Rule 3 came free: **the echoed answer is on none of the 95**,
because these four bands answer their leads with a second fiddle, a set of pipes, a hall or a caller
— the answering voice is in the section tags and the prompts, which is where M-47 put it.
**Two collisions between the wiki and the style cards were resolved the wiki's way** (D-095), and one
of them is dated rather than permanent: `b_038`'s card says *amplified* resonance pipes and `al_081`
is a Purist record from 2583, so nothing on it is amplified and the first amplifier in the band's life
is the first sound on `al_082`; and `b_062`'s card says the caller is on every track, while the wiki's
credits put Alis Doone on four of `al_139`'s eight, so she is off the other four and their exclude
lines keep spoken calling out. **Four songs are sung by somebody other than their band's lead voice**
and every one is a wiki fact: `s_0654`, `s_1116`, `s_0697` and `s_1139`. Each is named in its own
prompt and in its album's `room:` block; no style card was amended.
**Nothing was generated and nothing was measured**: every `generation:` block and every `take:` is
null until M-33, `music/catalogue.yaml` is byte-identical, and `make music-tag` reports exactly what
it reported before.
Result (M-25): **old-system sessions is written — 90 songs across 11 albums**, `al_098` … `al_104`
and `al_140` … `al_143`, on one label, by four bands who have never heard each other: a tram works
canteen on Mars, four voices in a Titan lake yard, a cold Europa under-ice gallery and eleven miles
of Earth canal. It carries one of the catalogue's six **cornerstones** — `al_098`, thirteen
songs, one room, one whole 56-minute programme — and the extra passes §5 asks for went there.
**`make check` is green on all ten of §12's rules.**
**The lyrics are shorter than the last three genres and that is M-39's instruction carried out.**
296 to 322 sung words, **mean 299 — the floor plus eleven** — 26,949 words in all, against Frontier
Reels' 340, lane-rock's 317 and relay-pop's 308. M-39 measured three genres at three different rates
spanning eleven per cent and concluded that *"the rate is a property of the genre and only
measurement gives it — write at the floor plus a small margin and let this card find the rest."*
That is what these are. **The estimate is stated rather than compensated for** (D-096): this genre
runs 58–124 BPM where every measured genre starts at 100, so at 0.75 seconds a word these come back
near **3:44** and at 0.90 near **4:29**, and nothing in the writing narrows that. M-34 and M-39
settle it.
**§7's distributions land, and the outros are the closest any genre has come.** Outros are **25 cold
/ 39 fade / 26 sustain**, which is 28/43/29 against §7's 30/45/25. Ramps declare **61% at eight
seconds or more and 17% at fifteen**, against §7's ≥40% and ≥15% — deliberately lower than Frontier
Reels' 73%, because M-39 has now found four genres in a row where declaring the ramp did not produce
it and inflating the declaration further is the one thing already known not to work. Stated targets
average **3:50** with nothing under 3:15.
**This form takes an instrumental break three times in ninety songs and that is a decision** (D-096).
§7 gives the break to three forms by rule, forbids it to two, and leaves the rest free; no card in
this genre names a break instrument, so there was no distribution to hit and none was aimed at. The
three are Wesla Tarn's slide on `s_0803`, and Tel Brask's harmonica through a lamp horn on `s_0812`
and `s_0844` — each one the answer to a question its own wiki fact asks, on an instrument that
record's credits already put in the room.
**Rule 4 bound harder here than in any genre yet.** These titles are plain speech lifted straight out
of the lyric — *Nothing Dries Down Here*, *Two Cups and No Sugar*, *Nobody Locks It Behind Us* — and
**the first pass had four albums at 100% and two more above 70%.** 36 of 90 sing their own title and
the other 54 take it from an image or a fact in the lyric, which is M-47's finding arriving in the
genre that resists it hardest. Rule 1 cost little: every album carries seven to eleven distinct
section shapes, because a read-out list, a rota, a committee's request, a round entered a bar apart
and a room shouting back are all different shapes and this genre supplies all of them. Rule 3 came
free — **the echoed answer is on 1 of 90**, and it is a foreman being answered by a canteen.
**Rule 5 was the awkward one and it is a finding rather than a failure.** §12's noun list is the
settled worlds' furniture and these four bands live in the home system, where there is no burn day,
no relay road to speak of and no last ferry. What carries it is the freight, dock and life-support
half of the list: **21 of the 43 nouns are used** — siding, lane, deck, berth, hold, cargo, manifest,
hauler, freight crew, ration, scrubber, airlock, bulkhead, blowout, oxygen tank, stripped wire,
storm season, ferry, settlement, the dark, the lag — and every song clears the floor of two. A tram
works has sidings, a lake yard has berths, an under-ice works has a scrubber and a bulkhead, and a
canal has a freight crew and a manifest. **No song reaches the floor on a word the room would not
have said.**
**Three collisions between the wiki and the style cards were resolved the wiki's way** (D-096), and
one of them is dated rather than permanent: `b_063`'s card lists a concertina and two harmony voices,
Wenna Ferrin joins in 2610, and `al_140` was cut in 2605 — so that record has neither, by name, in
every exclude line on it, and the first concertina in the band's life is the first bar of `al_141`.
`b_048`'s exclude line says `large hall reverb` and `s_0847` is the four-second gallery decay that
song is about, so that one track lifts the exclusion and asks for the decay instead. And `b_048` has
no bass player in the wiki at all, so both Undershore Local records exclude a bass of any kind rather
than trusting the card's narrower `electric bass`.
**Four songs are sung by somebody other than their band's lead voice** and every one is a wiki fact:
`s_0818`, `s_0824`, `s_0829` and `s_0853`. Each is named in its own prompt, excludes the usual voice
explicitly, and is listed in its album's `room:` block; `b_048`'s card had already anticipated its
one in words. No style card was amended. Nothing here names a real artist, band, producer or label
(§8), and the only real places named are the six canon allows this genre — Earth, Mars, Europa,
Titan, Saturn and the Belt.
**Nothing was generated and nothing was measured**: every `generation:` block and every `take:` is
null until M-34, `music/catalogue.yaml` is byte-identical, and `make music-tag` reports exactly what
it reported before — 310 of 310.
Depends on: M-20 for M-21; thereafter each genre's lyrics card depends on the previous genre's
**audio** card being finished — that is what "one genre at a time" means. **M-25 closed on
2026-08-29, so M-34 is runnable now**, and M-27's turn comes when M-34 does.

### M-30 · M-31 · M-33 · M-34 · M-36 · M-37 · M-38 · `[you]` Suno — 455 songs — **M-33 DONE 2026-08-28 · M-34 44 OF 90 FILED 2026-09-01**
Files: `music/audio/<label>/<album>/NN.mp3`
Check: every song in that genre has a keeper take, downloaded and named, with the prompt, attempts,
model version and date recorded in the album's lyrics file. Custom mode only.
Note: **these are the long cards.** M-19 tells you how long 45 songs take you; multiply. Each
depends on its own genre's lyrics card and on nothing else.
Result (M-30): **all 60 takes exist, dispatched, tagged, measured and in `music/catalogue.yaml`** —
`music/audio/label_3/al_005…al_006/`, `label_5/al_007…al_009/`, `label_6/al_010…al_011/`, named
`NN.mp3` by track number. Suno Pro, model v5.5, remixing disabled, `suno-pro-2026-08`, every take
kept on the first generation. Eight sittings across two days, each album finished inside one of them
except `al_009`, whose track 9 took a second.
**The mapping was proved rather than inferred** (D-091). Every take carries the lyric it was
generated from in its own tags, so filing was a text match against the lyrics files rather than
M-18's statistical reconstruction — and **it caught a song that had never been generated**: at 13:54
the lyric box still held track 8's words, so what came back in track 9's slot was a second take of
`s_0086`. It was never filed, `s_0087` *Coffee After Turnover* was regenerated at 21:24 the same day,
and the rejected file is `music/audio/RAW/87_wrong.mp3`, recorded in the dispatch manifest.
**What the audio measures — the pilot's short-songs problem is solved.** The 60 average **3:48**
against the pilot's 2:29, **nothing is under 2:00** where the pilot had fourteen, the shortest is
2:59 and the longest 5:02. The take comes back at **0.746 seconds per sung word** against the 0.763
M-50 fitted, so §12 rule 10's 288-word floor lands at **3:34** and **fourteen of these make 53
minutes, not 35.** Outros measure 33% cold / 47% fade / 20% sustain against §7's 30/45/25.
**The intro ramps are the one miss**: 7 of 60 have a measurable run-up of ≥8s where §7 asks 40%, and
2 reach ≥15s where it asks 15% — every song declared a 3-to-17-second intro in both its lyric tag
and its prompt and Suno sang early anyway, exactly as on the pilot.
**Relay-pop as a whole still averages 3:14**, because the pilot's 45 sit at 2:29 inside it. An hour
built only from the new 60 is fourteen songs; an hour that reaches back into `al_001` … `al_004`
needs fifteen or sixteen.
Result (M-31): **lane-rock's 110 takes are generated, filed, tagged and in `music/catalogue.yaml`** — `music/audio/label_2/al_131…al_032/`, `label_4/al_033…al_036` and
`al_132…al_133/`, `label_5/al_037…al_039/` and `al_134…al_135/`. Suno Pro, model v5.5,
`suno-pro-2026-08`, generated across six days from 2026-08-20 to 2026-08-25. **`attempts:` is null
on all of them** — the takes carry a Suno id and a creation time and nothing about how many
generations came before, and inventing a number is worse than an empty field (D-093).
**The dispatch is a `make` target now** (D-093). `make music-dispatch` reads the lyric out of every
file's own tags, matches the whole pile, and refuses to move anything unless every take claims
exactly one song and every waiting song is claimed — which is D-091's method with its two failure
shapes under a unit test, instead of an agent doing it by hand once a genre.
**One take had to be fetched twice and it is now closed.** `s_0340` *Wages at the End of It*, the
last track of the cornerstone `al_039`, first downloaded as **8.2 seconds** against a 4:50 target —
211 KB where its siblings are 5 MB. Its tags were complete, so it matched its lyric at 88% and filed
like everything else; only a check on durations caught it. The operator re-fetched it the same
evening and the replacement is 4:27. **It is a different generation, not the same file again**
(`46c4ba85-…` against the short one's `26f811f7-…`, created three seconds apart), because Suno
returns two takes per prompt — so `s_0340` is the one song here whose `attempts:` is knowable and it
says 2. `make music-dispatch` now refuses anything under 2:00 (§7), so this cannot reach an album
folder again, and filing the replacement on its own exposed a second flaw worth knowing about
(D-093): the matcher compared a pile only to the songs still waiting, which for a one-song top-up is
a pool of one and proves nothing. It now matches against every written lyric in the genre and files
only into the gaps.
**Suno does not sing what it is given, and this is the first genre to show it.** 93 of the 110 takes
match their written lyric exactly; 17 drift. `s_1083` sings its lyric twice through, `s_0335` drops a
quarter of it, and `s_0336` and `s_1076` are reworded line by line. **Two songs fall under §12 rule
5 on what is actually sung** — `s_0336` and `s_1092` both lost the word *settlement* and carry one of
the world's own nouns instead of two. `make check` counts the written lyric and stays green, which is
correct; the station broadcasts the take. That is a finding for your ear and for M-39, not a number
to edit and not a reason to regenerate anything.
Result (M-33): **Frontier Reels' 95 takes are generated, filed, tagged and in `music/catalogue.yaml`**
— `music/audio/label_2/al_078` … `al_080` and `al_138` … `al_139`, `label_4/al_081`, `al_082` and
`al_136`, `label_5/al_083` … `al_085` and `al_137`. Suno Pro, `suno-pro-2026-08`, generated across two
days, 2026-08-27 and 2026-08-28. `attempts:` is null on all 95, as on lane-rock and for the same
reason (D-093): the takes carry a Suno id and a creation time and nothing about what came before.
**`model_version: v5.5` is read from 2026-08's own licence note rather than from the files**, which do
not carry it — if a different model was used, that one field in twelve `generation:` blocks is the
only thing to correct.
**All 95 matched their lyric exactly and the pile filed in one pass.** `make music-dispatch` reported
`lyric_match: 1.0000` on every take — no drift at all, against lane-rock's 17 of 110 that drifted and
two that fell under §12 rule 5 on what was actually sung. Whatever changed between the two sittings,
this genre is broadcasting the words that are written down.
**The word floor is working and is now over-buying by more than lane-rock's.** The 95 average **3:57**,
nothing is under 2:00, the shortest is 2:44 and the longest 5:09, and the take comes in **8.1 seconds
under the stated target** against the pilot's 61.7. **D-095's prediction was right about the rate and
wrong about what to do with it**: this genre measures **0.698 seconds per sung word** against
relay-pop's 0.746 and lane-rock's 0.779 — the fastest yet, exactly as the tempo argument said — but
the lyrics were written thirty words longer to compensate for a rate that was already going the other
way. At 0.698, §12's 288-word floor lands at **3:21** and 310 words reaches §7's 3:36. **An hour of
Frontier Reels is thirteen songs, not fourteen.**
**Two bands were finished in one sitting each and one was not.** Wire and Rosin's three records were
cut inside two hours on 2026-08-27 and Loose Cargo's four inside two and a half on 2026-08-28, which
is what COMMISSION §9 asks for. The Foundry Set is split across both days — `al_081` and `al_082` on
the 27th, `al_136` on the 28th. Same month, same licence period and the same model, so the risk §9
names does not bite here; it is worth knowing because the next split may not be so lucky.
Note (M-30, for the next sitting): **Finish one band in as few sittings as possible** (COMMISSION §9).
Each song's `prompt:` is the style box and its `lyrics:` is the lyric box, Custom mode, remixing off.
**Check the lyric box actually changed before you generate** — that is the one failure this card
found. **September needs its own licence PDF the day you start generating in it** (M-40), and the
takes generated on 2026-08-27 and 2026-08-28 are the last ones 2026-08's evidence covers.
Result (M-34, part 1, 2026-08-31): **38 of old-system sessions' 90 takes are filed, measured, tagged
and in `music/catalogue.yaml`** — `music/audio/label_7/al_098` … `al_101`. Suno Pro, v5.5,
`suno-pro-2026-08`, generated across 2026-08-30 and 2026-08-31 in seven sittings. `al_099`, `al_100`
and `al_101` are complete; `al_098` is 12 of 13. **All 38 match their lyric exactly** —
`lyric_match: 1.0000` on every one, as on Frontier Reels.
**The dispatch refused the pile twice before it filed anything and both refusals were right** (D-097).
**`s_0796` *The Room at Terrace Road* was never generated**: two takes came back nineteen seconds
apart carrying the same words — `s_0797`'s — because the lyric box did not change when the style box
did. That is D-091's failure a second time, on the title track of the genre's cornerstone. The
operator has no time to regenerate it, so its `take:` is null and it is an unplayable row; filing one
of the pair under it was refused, because a take of *Don't Wait Up for the Late Car* entering the
catalogue as a song whose one fact is a works bell it does not contain is the exact thing D-091
exists to stop. And **`s_0809` was generated from a different hand-written draft than the file held**,
caught at 21%; the file was corrected to the words actually sung rather than the take regenerated,
which is the opposite of D-093's rule for vendor drift and for a stated reason.
**52 takes are owed and the operator will make them on a different generator.** Two things follow:
`b_047` The Shore Rounds will be split across two vendors — `al_100` and `al_101` on Suno v5.5,
`al_102` elsewhere — which is the stronger form of the risk COMMISSION §9's *"finish a band in one
sitting"* names; and those takes cannot carry `suno-pro-2026-08`, so they need their own dated
evidence file and their own `licence_period` the day generation starts (M-40).
Result (M-34, part 2, 2026-09-01): **six more takes filed — `s_0796` and all five of `al_102`** —
all matching at `lyric_match: 1.0000`, generated in one sitting of under seven minutes plus one
regeneration. **`s_0796` *The Room at Terrace Road* now exists**, so the genre's cornerstone is 13 of
13, and the first attempt at it — which D-097 proved had never been made at all — is closed.
**Five records are complete and two bands are finished.** `al_098` … `al_102`, which is Terrace Road
Four's 24 songs and The Shore Rounds' 20. Both clear §5's 18-song floor, so **two artist profiles are
makeable**, and Relay Road Import reaches **44 playable songs**, past the 40 a label retrospective
needs. **No band in this genre is split across two generators any more** — the risk D-097 named is
closed rather than accepted, because `al_102` was made on Suno alongside its two sibling records.
**`al_098` is the first record in the catalogue made in two licence periods** (D-098): tracks 2–13
under `suno-pro-2026-08`, track 1 under `suno-pro-2026-09`. Nothing needed inventing — D-062 already
resolves a song's `take:` block before the album's `generation:`, so track 1 overrides that one field
and each mp3 carries the period it was actually made under.
**The September evidence is outstanding and that is the one thing owed on this card.** The operator
has confirmed Pro and remixing off on 2026-09-01, which is what §9 conditions commercial rights on,
so the six were filed. The dated capture of the terms has not been taken.
`music/licence-evidence/2026-09-suno-licence-note.md` exists and opens by saying so, because
`licence_period` is free text and **no gate in this project will ever ask** (D-098).
Note (M-34, for the remaining 46): they are **Undershore Local** (`al_103`, `al_104` — 16 songs) and
**The Ninefoot Cut** (`al_140` … `al_143` — 30 songs), and neither has a single take yet, so both can
go to a different generator without splitting a band. **Test one track before committing to 46**:
`make music-dispatch` proves a take by the lyric in its own tags and currently expects Suno's exact
`id=` and `created=` comment format, which another vendor is unlikely to write. **And run M-51 before
that pile is filed** — it counts the two licence invariants that are still prose, and the new
generator's first sitting is exactly where a wrong period would be typed.
Depends on: M-21 for M-30, M-22 for M-31, and so on down the table.

### M-39 · `[agent]` Measure and tag every song
Goal: All 500 songs carry a real duration, a measured intro ramp, an outro type and their licence
tags. **Run after each genre's audio lands, not once at the end.**
Check: `make music-analyse` and `make music-tag` cover all 500. No song is missing a ramp. The
distribution matches COMMISSION §7 — ≥40% of songs have ≥8 seconds before the first sung word, ≥15%
have ≥15 seconds, roughly 30% cold / 45% fade / 25% sustain, average duration near 3:30.
Note: where the distribution misses, the fix is choosing different takes, not editing the numbers —
which is the whole reason this runs per genre. Finding it at 500 songs is finding it too late.
Relay-pop pass, 2026-08-18 — **the first genre through, 105 songs measured and tagged.** Duration is
fixed: the 60 new takes average **3:48** and none is under 2:00, against the pilot's 2:29 and its
fourteen, so §12's word floor did what M-50 designed it to do (0.746 seconds per sung word measured,
against the 0.763 fitted). Outros land 33 / 47 / 20 against §7's 30 / 45 / 25. **The ramps miss and
the miss is not the writing's**: 7 of 60 have a measurable run-up of ≥8 seconds where §7 asks for
40%, and 2 of 60 reach 15 seconds where it asks for 15% — every one of the 60 declared an intro of
3 to 17 seconds in both its lyric tag and its prompt, and Suno started singing early anyway, exactly
as on the pilot. That is a finding for the operator's ear and for M-42, not a number to edit.
Lane-rock pass, 2026-08-25 — **the second genre through, all 110 songs measured and tagged.**
Duration holds: they average **4:08**, nothing is under 2:00, the shortest is 2:51 and the longest
7:59, and the take comes back at **0.779 seconds per written sung word** against relay-pop's 0.746.
That is the opposite of what M-22 predicted — lane-rock runs 100–172 BPM against relay-pop's 110–130
and was written thirty words long to compensate, and it turns out to run *slower* per word, not
faster, because a third of these songs carry an instrumental break and the break is time that no word
paid for. **The written floor is now over-buying: an hour of lane-rock is 13.5 songs rather than
fourteen.** Nothing needs fixing here; the next genre's lyrics card should write nearer 300 words
than 320 unless it also solos.
Outros land **26 cold / 47 fade / 26 sustain** against §7's 30 / 45 / 25 — the closest any genre has
come. **The ramps miss again and by more**: 4 of 110 have a measurable run-up at all, where §7 asks
40% to reach 8 seconds. Every one of the 110 declared a 3-to-24-second intro in both its lyric tag
and its prompt. **This is now three genres in a row** — the pilot, relay-pop, and lane-rock — and it
is no longer a finding about writing. Suno sings from the top whatever the prompt says, and either
the ramps come from choosing different takes, or from the mixer at M-42, or §7's ramp distribution is
describing something this vendor will not do.
All 215 playable songs now average **3:42** against §7's 3:30.
Frontier Reels pass, 2026-08-28 — **the third genre through, all 95 songs measured and tagged.**
Duration holds and the rate moved again: they average **3:57**, nothing is under 2:00, the shortest is
2:44 and the longest 5:09, and the take comes back at **0.698 seconds per written sung word** against
lane-rock's 0.779 and relay-pop's 0.746. **Three genres, three different rates, and the spread is now
0.08 seconds a word — eleven per cent.** D-095 predicted this one would run fast because the form is
fast, and it does; what it could not predict is by how much, and the thirty extra words written to
cover it were not needed. The lesson for M-25 is not a number of words, it is that **the rate is a
property of the genre and only measurement gives it** — write at the floor plus a small margin and let
this card find the rest.
Outros land **35 cold / 38 fade / 22 sustain**, which is 37 / 40 / 23 against §7's 30 / 45 / 25 — a
little cold-heavy and the widest miss of the three genres, though **only 36 of the 95 end the way
their lyrics file said they would**, so the distribution landing near §7 is partly luck.
**The ramps miss again and this is now four in a row.** 8 of the 95 have a measurable run-up at all,
7 of them reach 8 seconds and 2 reach 15, where §7 asks 40% and 15%. Every one of the 95 declared a
2-to-22-second intro in both its lyric tag and its prompt, and this genre declared the highest ramps
in the catalogue — 73% at 8 seconds or more — precisely because the two genres before it had missed.
**Declaring the ramp does not produce the ramp.** After the pilot, relay-pop, lane-rock and Frontier
Reels, the writing side of this has been tried as hard as it can be tried: the remaining places it can
come from are choosing different takes, the mixer at M-42, or §7's ramp distribution describing
something this vendor will not do. **That is now a decision for the operator rather than a finding**,
and it is the one thing in stage 5 that has failed the same way four times.
All 310 playable songs now average **3:46** against §7's 3:30.
Old-system sessions pass, part 1, 2026-08-31 — **38 of 90 measured and tagged, and the rate finally
moved the way the tempo said it would.** These 38 come back at **0.853 seconds per written sung
word** against Frontier Reels' 0.698, relay-pop's 0.746 and lane-rock's 0.779. **D-096 predicted
0.75 to 0.90 from the tempo alone and it landed at 0.853**, near the top of that range — the first
time the prediction has been right in direction and size, and the spread across four genres is now
0.155 seconds a word, twenty-two per cent.
**So the floor buys far more than it did.** §12's 288 words lands at **4:05** here, not 3:36; the
written mean of 299 lands at **4:15**; the 38 average **4:20**, the longest of any genre, nothing is
under 2:00, the shortest is 3:05 and the longest 5:33. **An hour of this is 12.9 songs.** Writing at
the floor plus eleven was the right call and writing at Frontier Reels' 340 words would have produced
a 4:50 average.
**This is the first genre whose takes come in OVER their stated target** — **+33 seconds on average,
over on 31 of 38** — against the pilot's 61.7 seconds under and Frontier Reels' 8.1 under. §7's note
that the stated target is *"an honest statement of the take we want"* now cuts the other way: for a
slow form the words overshoot it.
**The ramps improved and one half of §7 is met for the first time in the project.** 11 of the 38 have
a measurable run-up at all — **29%**, against 12% on relay-pop, 4% on lane-rock and 8% on Frontier
Reels. 10 reach eight seconds (26%, where §7 asks 40%) and **6 reach fifteen (16%, where §7 asks
15%)**. After four genres of *declaring the ramp does not produce the ramp*, the thing that produced
some was a slow form, not a bigger number in the prompt.
**The outros are the widest miss so far and the fade is what vanished.** Measured **22 sustain / 14
cold / 2 fade** — 58 / 37 / 5 against §7's 30 / 45 / 25 — where the lyrics declared 17 fade, 11 cold
and 10 sustain. Suno gave back two fades out of seventeen asked for and turned the rest into a held
ending. On a form this slow a sustain and a fade are a close call by ear, which is worth knowing
before the remaining 52 are made somewhere else.
All 348 playable songs now average **3:50** against §7's 3:30.
Depends on: M-05, and each genre's audio card as it lands. Closes when M-38 does.

---

# Stage 7 · The July collection — 136 takes that predate the wiki

**135 songs already exist and none of them is in the plan.** They were generated on Suno between
2026-07-03 and 2026-07-25 — one account, **Pro, v5.5** (operator, 2026-09-01), one licence period,
before the commission was written — and they sit on the volume at `music/audio/RAW/music/` with a
hand-written `tracks.yaml` describing every one. A 136th was a runaway generation and the operator
deleted it on 2026-09-01, entry and all; the ledger and the folder are back in step at 135.
**The operator wants them used.** This stage is how.

**They cannot join the 500 and they must not try.** `plan.yaml` is the authority for every count and
`tests/unit/test_music.py` asserts 500 songs, 25 bands and exactly the nine genre slugs; the wiki
froze at M-15. Nothing here moves any of that. The collection arrives as a **collection** — a wiki
file that carries records but no plan allocation — and everything else follows from that one idea.

**In the world they are what reached the station outside the seven houses.** `label: unsigned` is
already a value `catalogue.py` understands, so the collection needs no eighth label and inherits
none of COMMISSION §5's retrospective floors. It is 42 bands, most with one, two or three records each —
which is exactly what an unsigned shelf looks like, and exactly the relief ARCHITECTURE §8's
artist-separation rules want from a library of 25 bands.

**Three things make it cheap.** No band name in the pile collides with anything in `music/wiki/`.
Every one of the 135 already carries a `story_blurb` in the shape of the wiki's per-song `fact` —
the expensive part of layer A, already written. And nothing in the code reads the RAW filenames, so
the renaming is free.

**One of them is the station's own song** and gets its own card (M-55).

**Read `music/audio/RAW/music/tracks.yaml` before starting any card in this stage.** It is the only
description of these files, it is under `music/audio/` and therefore **not in git**, and it is
deleted at M-56 once its contents live in the wiki. Until then it is the source of truth for what
each file is.

### M-52 · `[agent]` The collection seam — a wiki file that is not a genre — **DONE 2026-09-02**
Goal: The code can carry a set of records that is not part of the commissioned 500, and the three
totals do not move.
Reads: ARCHITECTURE §8, §17a · COMMISSION §1
Files: `src/station/music/wiki.py`, `check.py`, `catalogue.py`, `writing.py`, and the unit tests for
each.
Check: seven things, and the last two are the ones that make it worth doing as code.
  1. `make check` is green and unchanged — 500 playable songs, 25 bands, nine genre slugs.
  2. A collection file in `music/wiki/` needs **no allocation in `plan.yaml`** and is not counted
     against one. A genre file still is.
  3. It **is** counted for id uniqueness: a song, album or band id it reuses from a genre goes red,
     naming both uses. `next_free_ids()` sees its ids, so the next genre written cannot collide.
  4. Its albums are **not** required to sit on one of §1's eight anchor years. Layer A of a genre
     still is.
  5. Its songs still obey the fact rule — layer A carries one, layer B carries none.
  6. `catalogue.py` includes it: its playable songs become rows with a file, a duration, a ramp, an
     outro and a licence, and its layer-B titles become unplayable rows.
  7. A lyrics file for a collection album with no `lyrics:` in it is **exempt** from §12's ten
     counted rules, and a genre album with the same emptiness still goes red.
Note: `anchors.yaml` is the precedent — `wiki.NOT_A_GENRE` at `wiki.py:28`. **Do not reuse that
set.** Anchors is skipped; a collection is read, by everything except the plan count and the anchor
rule. That is a third state and the code should say so in one place rather than in four `if slug ==`
tests. `make music-screen` with no argument must sweep collections too, or 42 unscreened band names
sit in the wiki and nothing ever asks about them.
Depends on: nothing.
Result: **`wiki.COLLECTIONS` — one constant, two accessors, and the state is over.** `written_slugs()`
is what everything reads (ids, facts, catalogue rows, the writing rules, `make music-screen` with no
argument); `written_genres()` is the narrower list, and only two passes take it — the plan count and
the anchor years. All seven checks proved against the real wiki with a fixture `independents.yaml`
dropped into `music/wiki/`: `make check` stayed green with no allocation and a 2615 album, an id
reused from relay-pop went red naming both files, `next_free_ids()` advanced past the collection,
and its songs came back as catalogue rows. **One thing the card did not name and this had to
decide:** §12's rule 8 stays genre-only, because it is written as *"a genre file naming bands in
other genre files"* and a shelf of unsigned records is not a tenth world to be sealed — rules 6 and
7 do read the collection. 10 new tests, `make check` green, D-099.

### M-53 · `[agent]` `music/wiki/independents.yaml` — the collection, written — **DONE 2026-09-02**
Goal: The 135 takes become part of the world, with a story that fits the canon they were made
before.
Reads: COMMISSION §1, §2, §6, §7, §8 · CONSTANTS §3, §4 · the preamble above
Files: `music/wiki/independents.yaml`, `music/CONSTANTS.md` §3, `docs/DECISIONS.md`
Check: `make check` green. `make music-screen GENRE=independents` has been run and its result — 42
bands, 46 albums and every title — is recorded in `CONSTANTS.md` §3 beside the nine genres.
**77 songs are layer A and 58 are layer B**, and the file says which is which.

The split is mechanical and these are the rules that produce it:
  - **Drop the instrumentals.** Nine are tagged `instrumental`. COMMISSION §7 wants instrumental
    passages and not wordless tracks, and the operator wants none of them. They become layer-B
    titles — the record exists, the station does not hold it.
  - **Drop everything under 2:00.** §7's floor, and 24 files are under it.
  - **One take per song.** 38 of the 135 are a second take of a song already in the pile — 18 titled
    `(Alternate Take)` and 20 more retitled (*Dockyard Heart* / *Dockyard Hearts*, *Pass It On* /
    *Let's Pass It On*, *Red Soil, Blue Guitar* / *Red Soil Sunday* / *Blue Guitar, Red Evening*).
    **Keep the longest surviving take of each cluster; the rest are layer-B titles.** Longest,
    because §7's duration arithmetic runs short everywhere else in this project.
  - **One take of 7:59 is left and it has no twin to be judged against.**
    `ysolde-mar__cargo-hold-lullaby.mp3` runs 479.4 seconds — to the tenth of a second the same
    length as the runaway the operator deleted on 2026-09-01, which is what a generation hitting the
    model's ceiling looks like rather than a piece that ends. §7 has no upper floor and the rule
    keeps it. **Listen to it and ask** before filing it.
  - **The station song keeps both takes** — see M-55.

Then five decisions the file has to make, none of which the pile makes for you:
  - **A form for every album, from the closed nine.** 52 of the 77 carry no form tag at all today,
    and two carry `pulse-dance`, which D-068 says is never pressed — retag those two or drop them.
    §2's palette table is what to read them against.
  - **Re-date the collection into 2612–2621.** `category` is derived, not chosen (D-085): five
    in-world years or older is `gold`, everything else is `A`, heavy rotation. The pile's own years
    cluster 2620–2626, so as written all 78 would land in heavy rotation, crowd the commissioned
    500 and contradict the story. Re-dating costs nothing — no lyric, no fact and no album story has
    ever been written against these years. **The eight anchors do not apply here** (M-52 check 4)
    and the collection should mostly miss them: records that arrived one at a time are not records
    that came out in the years the houses all shipped into.
  - **Nine titles collide with the wiki** — the albums *After the Last Ferry*, *Old-System
    Sessions*, *Resonance*, *Turnover*, *Under the Ice*, and the songs *Burn Day*, *Hold the Line*,
    *Second Shift Blues*, *The Long Way Round*. Retitle the collection's copy, not the wiki's. The
    wiki is frozen.
  - **`label: unsigned` throughout**, and no eighth label anywhere.
  - **The facts are already written.** Each song's `fact` is its `story_blurb` from `tracks.yaml`,
    edited only where it breaks §8. **This card's era claim was wrong** — `canon/10-history.md`
    names all three ages (the First Expansion, the Reconnection, the Age of the Relays), so nothing
    needed editing on those grounds. What did need editing was §8's production vocabulary:
    "power-pop", "folk-rock", "surf-rock", "soul-rock", "heartland-rock" — words the wiki never
    carries because the wiki reaches the microphone. Layer-B
    songs get **no** fact; §12's rule and `check.py` both say so.
Note: this is a wiki-writing card and reads like M-07 … M-14, with two differences: the songs
already exist, and the bands do not have to earn a label. Bands still need a bio, a home and a
`kind`; albums still need a title, a year and a form. **Do not write style cards for these 42
bands** — a style card fixes how a band sounds for records not yet made, and every record these
bands will ever make already exists.
Depends on: M-52
Result: **`music/wiki/independents.yaml` — 42 bands, 75 albums, 135 songs, 77 playable and 58
titles.** The split came out at exactly 77/58 from the four mechanical rules with nothing judged by
ear: 9 instrumentals, 24 takes under 2:00, 38 second takes across 33 clusters (the longest surviving
take of each kept), and the station's song keeping both. `make check` green, `make music-screen
GENRE=independents` clean at 221 distinct names, `CONSTANTS.md` §3 carries the result and D-100 the
decisions. **Three things the card did not predict.** *46 albums was not reachable*: `check.py`
keys the fact rule on the **album's** layer, so a take the station does not hold cannot sit beside
one it does — 33 of the 42 bands needed a layer-B record of their own, and the file carries 42
layer-A records and 33 layer-B ones. *42 bands rather than 43*: `First Generation` is a claim on a
sleeve and not a credit (canon 70-music fact 22 — nothing that old plays), so its one take closes
The First-Ships Choir's record and its fact says who is claiming what. *Two names moved on the
screen* — the album *The Commons* and the song *Wings*, the first two hits in nine screens; both
retitled and rescreened clean. **And one thing the card got the wrong way round**: it expected the
facts to need editing for era vocabulary, and canon 10-history has all three eras — what they
actually needed was §8, because the blurbs are full of production vocabulary ("power-pop",
"folk-rock", "surf-rock") and that never enters the wiki. 28 facts and 3 bios were edited to the
nine canon forms plus §8's three-word old-system exception. Re-dated into 2613–2621, so the whole collection is `gold` and none
of it crowds the 500. Nothing was written that the card told me not to write: no style cards, no
members, no session players, no layer C.

### M-54 · `[agent]` File the 78 takes, and the licence they were made under — **NEXT**
**Before this card copies anything, the operator listens to `s_1362` — Ysolde Mar's *Cargo-Hold
Lullaby*, `al_171` track 2, 479.4 seconds.** M-53 filed it as playable because §7 has no upper floor
and the rule kept it, but it is to the tenth of a second the length of the runaway generation the
operator deleted on 2026-09-01, and M-53 could not judge that by reading. If it is a runaway the fix
is one `playable: false` and one line moved onto a layer-B record for Ysolde Mar, and the counts
become 76 and 59.
Goal: The collection's audio sits where the station expects audio, carries its own provenance, and
reaches `music/catalogue.yaml`.
Reads: COMMISSION §9 · ARCHITECTURE §17a · RUNBOOK steps 6 and 7
Files: `music/audio/unsigned/al_NNN/NN.mp3`, `music/production/lyrics/al_NNN.yaml`,
`music/licence-evidence/2026-07-suno-licence-note.md`
Check: `make music-tag` reports **nothing unclaimed** under `music/audio/unsigned/`;
`make music-catalogue` gains 77 playable rows, each with a measured duration, intro ramp, outro type
and `licence_note: suno-pro-2026-07`, plus 58 unplayable ones; `make check` green.
  - **Copy, do not move.** `music/audio/RAW/` stays intact until M-56 says it can go. A copy that
    can be verified against its source is the whole reason the deletion is a separate card.
  - **A stub lyrics file per album**, because `tag.py` reads provenance from nowhere else: the
    album id, a `generation:` block, and `songs[]` with id, title and track number. **No lyrics** —
    these were not written here and inventing them would be a lie about what the take sings. M-52
    check 7 is what keeps `writing.py` green over the stubs.
  - **The generation block is `suno-pro-2026-07`, model version `v5.5`,** with each file's own
    `created=` date out of its Suno comment tag. **The model version is not in the files** — Suno
    writes only `made with suno`, a timestamp and a generation id — so it is the operator's to
    state, and the operator stated it on **2026-09-01**: the same v5.5 the July jingles and the
    pilot's 45 record. Nothing to ask; write it down and cite the date.
  - **Widen `2026-07-suno-licence-note.md`.** It currently says it covers 56 imaging assets and
    explicitly not music. It has to name these files too, with their count and their dates, or M-51
    finds a period with no evidence behind it.
Note: `make music-dispatch` cannot file this pile. It proves a take against the lyric the file
carries in its own tags (D-091, D-097) and these takes have no written lyric to prove against. This
is a one-time filing and belongs in this card, not in that tool.
Depends on: M-53

### M-55 · `[agent]` The station's own song
Goal: Settlement Radio has a record of its own, with a reason in the world and a place in the clock.
Reads: ARCHITECTURE §9, §18 · PROGRAMMING §7 · `music/jingles/README.md` §5a
Files: `music/wiki/independents.yaml`, `docs/DECISIONS.md`
Check: A listener could hear it. Concretely: the wiki says the station adopted it and why, a
decision line says what it is and what it is not, and the two songs are marked in the file in a way
the grid card can act on.
  - **The song is *Green Lights All the Way*, The Lane Runners, 2:39.** Its own blurb is already the
    adoption story — *"every buoy green from dock to bay. Haulers play it leaving port for luck;
    harbourmasters swear it works."* A station that opens on a luck song is a station with a
    character.
  - **Its reprise is the sign-off.** *Green Lights (Reprise)*, 2:14 — *"the same lucky run sung
    slower, the way crews hum it at the end of a shift instead of the start."* Open and close, one
    band, one tune, already made. This is the one place M-53's one-take-per-song rule is
    deliberately broken, and this card is the reason.
  - **It is not the sonic logo and must not become one.** `sonic_logo_signature.mp3` is 12 seconds
    of sung station name — *"Settlement Radio — the light between the worlds"* — approved by the
    operator on 2026-08-23, and every other imaging piece quotes its glass-bell motif
    (`jingles/README.md` §5a). Two competing signatures is how a station stops sounding like one
    station. The logo is the ident; this is the song.
  - **The pin cannot be built here.** `config/grid.yaml` does not exist yet; the hour clocks are
    `imaging/IMAGING_TASKS.md` I-14 and the pinned junction is `docs/TASKS.md` T-012. **State the
    requirement and stop**: the song is pinned to a fixed slot rather than rotated, and whatever
    selects rotation must filter pinned ids out, or the §8 separation rules will fight the pin every
    day. Do not add a card to either file to say so.
  - **Any edit of the song into a sting or a bed is the operator's**, in an editor, as an imaging
    asset. Placement is config; audio is not.
Note: record it as a decision (`D-099` or the next free number) — what the station's song is, why it
is a song and not an ident, and that the reprise is the close. A choice like this gets re-litigated
in eight months by someone reading only the wiki.
Depends on: M-53

### M-56 · `[agent]` Retire `music/audio/RAW/` — and the collection is done
Goal: One description of these 135 takes, in git, and no second copy contradicting it on the volume.
Files: deletes `music/audio/RAW/`.
Check: run in this order and stop at the first that is not true.
  1. `make check` green.
  2. Every one of the 77 has a row in `music/catalogue.yaml` with a file path that resolves, a
     measured duration, an intro ramp, an outro type and `suno-pro-2026-07`.
  3. All 58 layer-B titles are in `music/wiki/independents.yaml` and none of them has audio —
     `catalogue.py` goes red if one does, which is the check doing its job.
  4. Every band name, album title and song title from `tracks.yaml` appears in the wiki, under its
     own name or a retitle M-53 recorded. **Nothing in that file is only in that file.**
  5. `grep -r RAW` finds no reference in the repository.
Then delete `music/audio/RAW/`, `tracks.yaml` included. **Ask the operator before deleting** — it is
irreversible, the folder is not in git, and CLAUDE.md is explicit about this. If any check above is
not true, the card is not finished and nothing gets deleted.
Note: the deletion is the point of the card, not a tidy-up at the end of another one. `tracks.yaml`
is the only record of what these files are and it lives under `music/audio/`, which `.gitignore`
excludes — so until the wiki carries everything it says, deleting it loses the collection. After
this card the wiki is the only description, and it is in git.
Depends on: M-54, M-55

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

- [ ] 9 genres written, checked and screened — **1,358** songs of text, 500 of them pressed
- [ ] 25 layer-A bands with a fixed voice
- [ ] **63** layer-A albums with lyrics and prompts in git
- [ ] 500 songs with audio, a measured ramp, a duration and an outro type
- [ ] Every audio file carrying its own licence tags
- [ ] `music/catalogue.yaml` complete and validated
- [ ] Licence evidence for every month generated in
- [ ] You have listened, twice — at M-19 and at M-42
- [ ] The July collection filed — **77** unsigned records beside the 500, **58** more as titles, and `music/audio/RAW/` gone

Then the music job is done, and it hands over to the phase that has a database.
