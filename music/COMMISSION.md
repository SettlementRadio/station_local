# COMMISSION.md — the music of the settled worlds

> **For a commissioned writer.** Everything needed to invent the station's music: what to write, how
> much, and the one rule that must never be broken. Read it once end to end before writing anything.
> It assumes no access to the repository and no knowledge of the architecture.
>
> **This file is never broadcast.** It names real-world genres freely so that generation prompts can
> be written against them; **what you write may not** (§8).
>
> The operator's procedure — briefing, screening, generating, filing — is `RUNBOOK.md`, and is not
> yours to read.

---

## What you are making, in five lines

A **wiki of an entire music industry** — genres, bands, musicians, labels, albums, songs, feuds,
sessions — spanning about two hundred years and ending in the present, which is **2626**.

Then a **small part of it becomes actual audio**: five hundred songs.

**The wiki is the product.** The station is a speech station; music leads only four hours a night.
What makes those hours worth hearing is not the songs — it is a presenter who knows who played bass,
which label folded, and why the singer stopped speaking to the drummer. **You are writing the thing
the presenters know.**

---

## 1. Three layers

The single most important idea here. **Most of the music you invent will never be recorded, and that
is correct** — real presenters reference far more music than any station owns.

| Layer | What it is | When | Size | Audio |
|---|---|---|---|---|
| **A — Played** | the station's record library | last ~60 years | ~25 bands · ~55 albums · **500 songs** | ✅ |
| **B — Referenced** | records that exist in the world; the station does not hold them | last ~80 years | ~50 bands · ~155 albums · ~1,330 songs | ❌ |
| **C — Historical** | musicians whose recordings are lost | 80–200 years back | ~30 figures, scenes, movements | ❌ none survive |

**Roughly 100 named musicians, 195 albums, 1,700 song titles — and 500 of those songs get made.**

**Why layer C has no recordings.** Nothing survives past living memory: not the damp, not the moves,
not the salvage crews. So the deep past reaches a listener the way pre-1900 music reaches us — we
know who they were, what they did, what was written about them, and nobody has the record. Write
them as history, never as a track you could play.

**The writing effort is deliberately lopsided.** Layer A gets full album stories and a fact per song.
Layer B gets one line per album and titles only. Layer C gets three lines per figure. This is what
makes two hundred years affordable.

### Every song carries a `playable` flag

`true` for layer A, `false` for B, absent for C. **A presenter may talk about anything; the scheduler
may only play layer A.** Getting this wrong is dead air.

---

## 2. The nine genres — a closed list

The world's musical forms are fixed. **There are nine and you may not invent a tenth.**

| Form | What it is | Layer A songs |
|---|---|---|
| **Lane-rock** | freight-crew driving music, engine rhythms, whole-crew choruses; its occasion is *burn day* | 110 |
| **Relay-pop** | the young bright form: hooks, harmony, songs about love across the lag | 105 |
| **Frontier Reels** | fast, rhythmic, danceable, played on salvaged and improvised instruments | 95 |
| **Old-system sessions** | current releases arriving down the longest relay road from Earth's home system | 90 |
| **Void-lounge** | the core's late-club standard, slow and smoky, after the last ferry | 55 |
| **Void Ballads** | one voice, one instrument, close to the microphone | 25 |
| **Core Harmonies** | big, many-voiced, unashamedly grand — the sound of a room full of singers | 20 |
| **Deck-talk** | rhythmic spoken verse over salvage percussion; competitive, cheap to make, and specific to the deck that made it | **0 — layer B** |
| **Pulse-dance** | four-on-the-floor from Meridian's sealed storm season | **0 — layer B** |

`music/plan.yaml` holds the same numbers label by label and `make check` counts the wiki against
them. Layers B and C spread across the same nine, and are thickest where layer A is thinnest.

**The top four are 80% of everything, and two of the nine are not pressed at all.** That is
deliberate. This is the record library of a living station, not a survey of a tradition — the forms
people actually put on outnumber the forms people admire, and the small forms are a spice measured
in tens of songs, not hundreds.

**Deck-talk and pulse-dance are the two the station does not hold.** Both stay canon and both keep
everything they have — bands, albums, credits, feuds, album stories — and none of it is recorded.
That is §1's layer B working exactly as designed: *most of the music you invent will never be
recorded, and that is correct.* A presenter may talk all night about a record the station cannot
play. **Write both forms as fully as any other; simply give their songs no facts and no audio.**

### The production palette

The left column is what the station says. The right column is what goes in a generation prompt, and
**never leaves this file** (§8). This is where the pop, rock, rock-and-roll and blues live.

| Form | Prompt palette |
|---|---|
| **Relay-pop** | **guitar pop, sung in harmony.** Power-pop, jangle, sunshine pop and soft rock: chiming twelve-string, ringing bass, several voices trading lines, stacked harmony, a chorus engineered to be sung back. Electric piano and organ at the keyboard end, acoustic guitar at the soft end. **Never dance-pop, never modern produced radio pop** |
| **Lane-rock** | rock. Driving four-piece, riff-led, singalong chorus. Pub rock, heartland rock, boogie, hard rock at the edges |
| **Deck-talk** | **rhythmic spoken verse over a beat.** Dense rhyme, conversational delivery, call-and-response, crews trading verses. Percussion built from struck metal and found objects, sparse bass, a sung hook only sometimes |
| **Frontier Reels** | rock and roll and its roots. Rockabilly, skiffle, jump blues, bluegrass and reel tempos, upright bass, slapback |
| **Old-system sessions** | blues and early rock and roll — twelve-bar, slide guitar, piano triplets, shuffle — plus folk rounds and country blues |
| **Pulse-dance** | dance pop. Four-on-the-floor, synth bass, big vocal hook. Italo, hi-NRG, house, synth-pop |
| **Void-lounge** | torch songs and slow blues. Smoky standards, brushed drums, late piano, soul ballads |
| **Core Harmonies** | **big vocal pop.** Wall-of-sound production, stacked doo-wop harmony, orchestral pop, big-band vocal — gospel *lift* rather than gospel liturgy. Grand and warm, never devotional |
| **Void Ballads** | one voice and one instrument, close-mic'd and intimate. Folk ballad, country-gothic, torch. A held note underneath at most — **never an ambient drone piece** |

**Nothing in that right-hand column is ever spoken on air**, with one canon exception in §8.

**Two of those palettes are never used.** Nothing is generated from the deck-talk or pulse-dance
rows, because neither form has a layer-A song. They stay in the table because the forms stay in the
world and a writer still has to know what they sound like.

**Deck-talk is the newest form here and the one most likely to be got wrong.** It is not a novelty
and not a frontier curiosity. Canon gives it two parents: the Freeholds' percussion built from
survival, and the older habit of reading a ledger aloud so a whole room can hear it and nobody can
claim afterwards they did not. Counting turned into competing. The skill people admire is carrying a
long list furthest without dropping the beat, and a verse that could only have come from its own
deck. **Write it as current, confident and popular** — made by the people who had least of
everything else and know exactly what they built. The station holds none of it, and that changes
nothing about how it is written: the presenters talk about it, they just cannot play it.

**The three movements are biography, not a subject.** The Purists (acoustic only), the Synthesists
(embrace what technology allows), the Localists (every world grows its own language). Note where a
band stands and whether they changed sides: it explains a split, a sound, a sacked player. **Do not
make it the point.** Canon's register rule is explicit that interest comes from concrete stakes —
prices, disputes, someone's bad day — and a wiki in which every band is a philosophy seminar
produces exactly the overnight nobody wants. The richest presenter talk is people and consequences:
who left, who paid, who would not play.

**Signature instruments, from canon, and they must be audible.** Forge's **resonance pipes** — long
alloy tubes, deep organ tones. Concordance's **synth-harpsichord** — plucked electronic strings. The
Freeholds' **percussion built from survival** — oxygen-tank drums, stripped-wire chimes. On the
frontier, instruments of engineered composite rather than wood: thinner, brighter, strange overtones.

---

## 3. Time

**Present is 2626** — always the real year plus six hundred, recomputed when the station speaks.

| Layer | Window | Share |
|---|---|---|
| **A — Played** | 2566–2626, with **half inside the last eight years** | 500 songs |
| **B — Referenced** | 2546–2626 | ~1,200 songs |
| **C — Historical** | 2426–2546 | no songs, only people and events |

**Write the year. Never write the age.** No "eight years ago", no "her last record before she died
last year", no "the twenty-year-old classic". The station computes all of that. A hardcoded age is
wrong within twelve months.

### The listener lives here; this is not a museum

**No song is about leaving Earth**, the crossing, the cradle, or the long dark. The diaspora is six
hundred years gone — as remote to them as the fifteenth century is to us, and nobody writes chart
songs about the fifteenth century.

Songs are about what songs are always about: someone who isn't here, a shift that won't end, money,
weather, a fight, a town, a night out, wanting somebody. **The world supplies the furniture — the
relay, burn day, the storm season, the last ferry — and never the subject.**

> **The test:** if the lyric would still work with the science-fiction nouns swapped for ordinary
> ones, it is right. If swapping them leaves nothing, the song was about the premise.

The old-system sessions are the one place the past is genuinely present, and even there it is
**current** — new records, made now, by people living now in Earth's home system, that took a season
to arrive. Exciting because they are new and far away, not because they are old. **Never present
them as archive.**

### Anchor years

Eight in-world years where a great many records happen to have been released, given to you by the
operator. `Night Record` plays *"one label or one year"*, and a year is only a programme if **≥25
playable songs across ≥4 bands and ≥2 labels** land on it. **Put most releases on the anchors** and
never invent a ninth anchor year.

**The anchors bind layer A only** (§12 rule 7, D-081). Every playable album sits on one of the
eight; layer B carries the rest of the calendar, because layer B has no floor to hit and something
has to account for the other two hundred years. A layer-B record still lands on an anchor whenever
the anchor's own event is its story — the fold, the festival, the reopening — and 38 of them do.
The eight stories themselves are `music/wiki/anchors.yaml`, which is where a year edition reads
them from.

---

## 4. Labels

Seven, and they matter because three programme formats are built on them: the label retrospective,
the artist profile and the album story.

| # | Tier | Home | Scene | Era |
|---|---|---|---|---|
| 1 | Flagship | **Concordance** (core) | Core Harmonies and relay-pop; the establishment | old, still running |
| 2 | Flagship | **Cold Harbor** / near frontier | Frontier Reels and Void Ballads | founded in living memory |
| 3 | Standard | **Meridian** storm coast | Synthesist: the pulse-dance house, and it presses late-club torch | recent, fast-growing |
| 4 | Standard | **Forge** | resonance pipes, heavy, lane-rock adjacent | industrial, long-lived |
| 5 | Standard | **the between** — a hauler co-operative | lane-rock | member-owned, awkward, beloved |
| 6 | Standard | core late-club | void-lounge | **folded 2612**, catalogue disputed |
| 7 | Import | routes to the **Old System** | old-system sessions | old, thin, precarious |

**Layer A bands carry the label depth.** Each label needs **≥3 layer-A bands and ≥40 playable
songs**, or its retrospective cannot be made. Layer B and C artists may belong to any label, to a
label that no longer exists, or to none.

**At least one label defunct, at least one in trouble.** A folded label has a disputed
back-catalogue, a founder who will not talk about it, and a reason for a 56-minute programme.

**The big forms belong to no single label.** Relay-pop appears on at least four of the seven;
lane-rock and Frontier Reels on at least three each. Deck-talk left this rule when its layer A went
— its crews are still spread across three labels, in layer B, where nothing counts them.

### Four musicians canon already fixed

All four are dead — the world bible names only the dead and the legendary. Honour them; do not work
around them.

- **Odessa Vail** — composer of one towering Core Harmony cycle, *Lanternlight*, written for a Lumen
  Festival, who then stopped. Place her in the deep end of layer B. Later performances of
  *Lanternlight* can be layer A.
- **Corin Hale, the Vigilkeeper** — a lifetime on one relay outpost, emerged with the *Station
  Cycles*, Void Ballads built around the outpost's life-support drone, which Hale refused to have
  repaired because it had become the tonic note.
- **Adra Pell and Lio Tern** — relay-pop partners who recorded apart, passing verses between two
  settlements; their quarrel over an altered credit was never resolved while they lived, and their
  last shared recording has no spoken introduction.

---

## 5. What each programme needs

Check layer A against these before declaring it finished. Everything here counts **playable songs only**.

| Programme | Length | Needs |
|---|---|---|
| **Label retrospective** | 56 min, 14 songs | a label with **≥3 bands, ≥6 albums, ≥40 songs** |
| **Artist profile** | 56 min, 14 songs | a band with **≥18 songs** — 14 is the bare minimum and makes every edition identical |
| **Album story** | 56 min | a **cornerstone album of 12–14 songs**. Designate **6–8** across the catalogue |
| **One year** | 56 min, 14 songs | an **anchor year: ≥25 songs, ≥4 bands, ≥2 labels** — of the eight, the seven that carry layer A |
| **Music sequence** (unhosted) | 56 min | mood coherence — enough songs sharing a mood tag. Still songs; there is no instrumental hour |
| **The chart** | weekly, 40 positions | **≥80 songs in rotation**, plus turnover. **Most-played, never new-release** |

**The chart counts plays, not release years** (D-080). ARCHITECTURE §8 scores it on decayed airplay,
in-world requests and previous position, with no release-date term at all, and nothing in this
catalogue is dated later than 2624 while the present is 2626 and moves every January. *Current*
here means in rotation. **Do not write records dated to the present year to feed it** — that is a
ninth anchor by another name, and §3 forbids it. `PROGRAMMING.md` carries what it costs a presenter.

**2559 is an anchor the station cannot play, and that is finished rather than outstanding** (D-079).
§3 puts layer A in 2566–2626, so no playable song can carry 2559; the year is an anchor because it
is when *Lanternlight* was premièred and when every competing house scheduled itself around it. The
"one year" edition is therefore built from the other seven, all of which clear the floor above. The
way 2559 reaches the air is a later performance — `al_163`, seven of the cycle's twelve movements,
recorded in 2624 — which is what §4 has always allowed. **Do not widen §3's window to fill it.**
| **Rotation** | separation: same song ≥4h, band ≥60min, album ≥90min, label ≥30min | ≥7 labels, ≥25 bands, ≥55 albums |

**The artist-profile rule sets the shape.** Fourteen songs an hour means a band needs two or three
real albums before a profile exists, which is what turns "write 500 songs" into "write 55 albums".

---

## 6. What to write

### A band (layer A)

Name · kind (solo, group, collective) · home settlement · label · genre · active_from · active_to ·
members with instruments and years · **bio of three to five sentences in plain speech.**

Where they stand in the Purist/Synthesist/Localist argument, and whether they moved. What they are
actually like. Not *"a haunting voice from the outer dark"* — **"records everything in one take
because she thinks second takes sound like apologies."**

### A band (layer B)

Name · kind · label · genre · active years · **two sentences.** Enough for a presenter to place them
in a scene and say one true thing.

### A figure (layer C)

Name · what they played · roughly when · **three sentences**, one of which is why anyone still
mentions them. **No albums, no track lists** — the recordings are gone. What survives is the story,
the influence, and sometimes a tune everybody still knows without knowing whose it was.

### An album (layer A)

Title · band · label · release year · kind (album, EP, single, live) · **notes: the story.** What was
happening, what it cost, who left during it, whether it sold. **This field is where a retrospective
comes from.**

### An album (layer B)

Title · band · label · year · **one line.** What it is remembered for.

### A song

| Layer A | Layer B |
|---|---|
| title · album · track number · genre · mood tags · `playable: true` · **and one fact** | title · album · track number · `playable: false` |

> ### The one-fact rule — the most important line here
>
> The overnight presenter's back-announce is defined as *"what just played, with one fact."* A song
> with no fact means the presenter invents something, which is the exact failure this whole wiki
> exists to prevent.
>
> **Every layer-A song carries one concrete, sayable fact.** Who played the part everyone remembers.
> Which take it is. What it was written about. Where it was recorded and why that was a bad idea.
> What it replaced on the record. Which argument it settled. One sentence.
>
> **Five hundred of them, and layer B needs none.**

### Credits and session players

Writer, player, producer, per layer-A song, linked to people in the world. The operator gives you a
fixed list of **recurring session players who appear across at least three labels** — the same bassist
on forty records by forty bands. Use them. It is the cheapest way to make a discography feel like an
industry, and the station's music presenter is written to notice exactly this.

**Session players have careers, not eternities.** A session career runs about thirty-five years.
Respect the dates you are given; nobody plays a date they were eleven for.

### Lyrics — layer A only, written by hand

Never generated by the music tool (§8). Follow §3's subject rules and the swap-the-nouns test. Open
every song with an instrumental-intro tag before the first verse — the presenter talks across it.

---

## 7. Sound and shape — layer A only

### The band style card

**Every layer-A band has one, and it is fixed for the life of the band.** It is what makes a band
sound like itself across three albums, and it replaces any reliance on a vendor's voice-cloning
feature — which is unreliable, lives outside the project, and is tied to models that get retired.

```
voice        female lead, low register, slightly hoarse, unpolished
backing      two-part male harmony on choruses only
instruments  fiddle, upright bass, brushed kit, no keys
production   room mics, first take, minimal overdub
tempo range  100–140
exclude      synths, heavy compression, modern pop production
```

Then **per song**, inside that card: mood, tempo, arrangement note, structure tags.

**The voice line is the load-bearing one.** Lead singer's gender, register, texture and delivery stay
fixed across every song that band ever releases. A band whose singer changes sex between albums is
not a band.

### Duration

A 56-minute music hour is 14 songs plus about six minutes of speech, so the average must land near
**3:30**.

| Band | Share |
|---|---|
| 2:00–3:00 | 28% |
| 3:00–4:00 | 42% |
| 4:00–5:30 | 22% |
| 5:30–8:00 | 7% |
| 8:00–11:00 | 1% |

**Most of this is pop and rock, so most of it is under four minutes.** Nothing under 2:00.

### Everything else

- **Every song has a vocal. No instrumentals.** Instrumental passages are wanted; wordless tracks are
  not. Beds and underscore are station imaging, a separate job.
- **Intro ramps:** ≥40% of songs need ≥8 seconds before the first sung word; ≥15% need ≥15 seconds.
  Measured by ear after generation, never estimated.
- **Outros:** roughly 30% cold, 45% fade, 25% sustain.
- **Language:** everything sung is in Standard — English — or wordless within a song. Regional
  character comes from instrumentation, rhythm and accent. **Never write lyrics in a real minority or
  indigenous language to signal "frontier".**

---

## 8. IP — the hard rules

The station is a **tribute, not a derivative**, and generative music tools are trained on real
records and will happily be steered toward one.

### The two vocabularies

| | Used in | May contain |
|---|---|---|
| **Production vocabulary** | generation prompts, the production sheet | real **genre and technique** words — "brushed drums", "close-mic'd fiddle reel", "four-on-the-floor synth". A sound is not property |
| **In-world vocabulary** | the wiki, the air, the website | **only the nine canon forms** |

**Prompts and style cards never enter the wiki**, because the wiki is read into the station and can
reach the microphone.

**One exception, exactly three words wide.** Canon says the old system is where *"blues, rock, and
the folk rounds"* never died. Those three terms are air-legal **for old-system material only**. Not
"rock and roll", not "rockabilly", not "soul", not "house".

### The rules

1. **Never name a real artist, band, producer, album, song or label** in a prompt, a lyric, a wiki
   entry, or anything the station can say. No "in the style of", no "sounds like". Not once.
2. **Never prompt for a real singer's voice**, by name, by description, or by uploading audio.
3. **Write the lyrics by hand.** Never let the music tool generate them — generated lyrics are
   unscreened, can reproduce fragments of real songs, and are broadcast content.
4. **No lyric names a real person, brand, company, franchise, work or event.** The only real places
   nameable are the ones canon allows for the old system: Earth, Mars, Europa, Titan, Saturn, the Belt.
5. **Every band, artist and label name is screened** against real people and organisations before it
   is committed.
6. **Album and song titles are screened too** — two or more words, avoiding anything famous enough
   that a listener would recognise it.
7. **No real cover art, logos or typography.**
8. **Licence evidence is captured per generation period.** See §9.

**The litmus test:** if a listener could name the real artist from what they hear, or from what the
presenter says about it, it has crossed the line.

---

## 9. Licence — what actually applies

*Written from public sources by a non-lawyer, and reviewed properly before launch.*

- **A paid plan is mandatory.** Free-tier output is non-commercial and unusable here. Commercial
  rights attach to output generated **while the subscription is active**.
- **Commercial rights are not copyright.** The vendor remains the technical author and grants a
  perpetual licence to exploit; it makes **no warranty that any copyright vests** in the output. The
  station may broadcast and publish; whether it could stop someone else copying a track is a separate
  and weaker question.
- **The vendor is in active litigation** with two major labels, and models are being replaced by
  licensed ones with the current generation deprecated. **Finish a band in one sitting**, and record
  the model version per song, or a band's albums will not match each other.
- **Per generation month:** save the commercial-use terms as a dated PDF into `music/licence-evidence/`.
- **Per song:** a `licence_note` naming the period it was made in — `suno-pro-2026-08`.
- **In the file itself:** write the licence period, generation date, model version and an
  AI-generated marker into the audio file's own tags. The audio and the wiki will be separated
  eventually — by a backup, a move, a hand-off — and the file has to carry its own provenance.

---

## 10. Never

- Never name a real artist, band, label, producer, album or song, anywhere.
- Never let the tool write the lyrics.
- Never put a prompt or a style card in the wiki.
- Never invent a tenth musical form.
- Never write a song about leaving Earth, the crossing, the cradle or the long dark.
- Never present an old-system record as archive.
- Never write an instrumental.
- Never write an age, a relative date, or "recently". Write the year.
- Never write a layer-A song without its one fact.
- Never give a layer-C figure an album or a track list. The recordings are gone.
- Never mark a song `playable` unless audio for it actually exists.
- Never write a bio in a late-night lyrical register. Plain speech, concrete detail.
- Never spread release years evenly. Cluster on the anchors.
- Never change a band's lead voice between albums.
- Never rename an id once committed. Titles can be edited; identity cannot.

---

## 11. Before you hand it back

- [ ] All nine forms present; the seven that are pressed carry layer-A songs in the stated
      proportions, and deck-talk and pulse-dance carry none.
- [ ] Lane-rock, relay-pop, Frontier Reels and old-system sessions together are about 80% of layer A.
- [ ] Every song has a `playable` flag, and `true` appears exactly 500 times.
- [ ] Every layer-A song has one concrete fact. No layer-B song has one.
- [ ] No layer-C figure has an album or a track list.
- [ ] Each label has ≥3 layer-A bands, ≥6 albums and ≥40 playable songs.
- [ ] At least four bands have ≥18 playable songs.
- [ ] Six to eight cornerstone albums of 12–14 songs.
- [ ] Every anchor year that carries layer A at all — seven of the eight — carries ≥25 playable
      songs across ≥4 bands and ≥2 labels. **2559 carries none and never can** (§5, D-079).
- [ ] Every layer-A band has a style card, and its voice line never changes.
- [ ] Every band and session player has active years, and nobody's career exceeds ~35 years.
- [ ] No age, no relative date, no fixed "today" anywhere.
- [ ] No lyric is about leaving Earth; every lyric passes the swap-the-nouns test.
- [ ] Every name has been screened.
- [ ] The wiki contains no prompt text and no real genre word.
- [ ] **`make check` is green, which is §12.**

---

## 12. The eight writing rules — the ones the command counts

> **§1–§11 say what to write. This section says what `make check` refuses**, and it is the only part
> of this file a machine reads. `src/station/music/writing.py` takes its numbers and its two word
> lists out of the tables below rather than keeping a copy of them, so editing a number here changes
> what the command does. Keep every table's shape; if one stops matching, `make check` stops with a
> message saying so rather than quietly finding no rules.

**Why this section exists.** Across six writing sessions the counting rules in `check.py` held
perfectly — no id collision, no wrong count, no album off an anchor. The prose rules in §1–§11
failed over the same span. Same writers, same instructions; the difference is that one set went red.
Every rule below is a way the wiki or the pilot lyrics have already gone wrong once, rewritten as
arithmetic. **A rule that cannot go red is a preference.**

None of these are new advice. They are §3's swap-the-nouns test, §6's one-fact rule and §7's shape
rules, counted instead of asked for.

| # | Goes red on | Counted over | Owed to |
|---|---|---|---|
| 1 | more than `40%` of an album's songs sharing one section structure | album | `M-47` |
| 2 | fewer than `3` of an album's songs in the third person or carrying a named character | album | `M-47` |
| 3 | the echoed answer — a parenthetical repeat inside a sung line — in more than `33%` of an album's songs | album | `M-47` |
| 4 | the song's own title used as the hook in more than `50%` of an album's songs | album | `M-47` |
| 5 | a lyric carrying fewer than `2` of the world's own nouns | song | `M-47` |
| 6 | a band more than `50%` of whose song facts are studio anecdotes | layer-A band | — |
| 7 | layer-B albums spanning fewer than `40` distinct release years | the whole wiki | `M-15` |
| 8 | a genre file naming fewer than `3` bands that live in other genre files | genre file | `M-15` |

**Rules 1–4 are shares of an album and are counted only on albums of `5` songs or more.** A share of
four songs is not a distribution, and a two-track single would fail rule 1 for existing.

Rules 1–5 read `music/production/lyrics/`. Rules 6–8 read `music/wiki/`.

### Owed to a card

The last column works exactly like `owed_to:` in `plan.yaml` (D-069). A rule owed to a card is
**counted but not fatal** until that card is marked `DONE` in `MUSIC_TASKS.md`, and it goes red the
moment it is — so the card cannot be closed while the work it names is still undone, and the
deferral cannot quietly become permanent. Both of the cards named below already say so themselves:
M-47's check is *"all 45 pass M-45's rules"*, and M-15's job list is rules 7 and 8 in words.

**Rules 1–5 · `M-47`.** The only lyrics that exist are the pilot's 45, and M-47 rewrites all of them.

**Rules 7–8 · `M-15`.** Both are properties of the whole catalogue rather than of one genre, and
neither can be satisfied by the genre being written today. **Rule 7 replaces an existing rule rather
than adding to one**: until M-15 closes, every album in both layers must sit on an anchor year
(§3, and `CONSTANTS.md` §1); after it, the anchors bind layer A and layer B has to carry the rest of
the calendar instead. The swap happens with the card, so there is no window in which neither applies.

### Rule 5 · the world's own nouns

§3 gives the principle — *"the world supplies the furniture — the relay, burn day, the storm season,
the last ferry — and never the subject"* — and a principle is what the pilot's 45 songs failed. This
is the list, drawn from `canon/55-language.md`'s coined words and from the freight, dock and
life-support vocabulary the wiki already runs on. Matched as written, whole words, any case.

**It is a floor and not a vocabulary.** Add to it as the world grows; never write to it.

> burn day · burn festival · lane · relay · relay road · the lag · last ferry · ferry · hauler ·
> freight crew · hold · deck · berth · manifest · cargo · transfer hall · port hall · siding ·
> storm season · storm coast · sealed season · airlock · bulkhead · scrubber · blowout · ration ·
> oxygen tank · stripped wire · resonance pipe · synth-harpsichord · the dark · the drift ·
> ground-sick · settlement · outpost · shipboard press · carrier wave · the core · the frontier ·
> the between · Lumen Festival · Clearing Day · vigil

### Rule 6 · what counts as a studio anecdote

§6's one-fact rule lists what a fact can be: *who played the part everyone remembers, which take it
is, what it was written about, where it was recorded and why that was a bad idea, what it replaced,
which argument it settled.* Six of those seven are about people; one is about the room. A band whose
facts are mostly the room has a discography a presenter cannot say anything human about.

A fact counts as a studio anecdote when it uses any of these words. Matched as written, whole words,
any case.

> take · takes · overdub · overdubs · microphone · mic · studio · session · sessions · engineer ·
> engineers · tape · playback · booth

**Being a studio anecdote is not a fault.** *"The issued take keeps a false start, because Tor
Dolo's count-in landed with the hall's ventilation and the band could not repeat it"* is a good
fact. Half a band's records being one is the fault.
