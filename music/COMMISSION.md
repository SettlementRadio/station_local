# COMMISSION.md — building the music catalogue for Settlement Radio

> **For the operator and a commissioned writer.** Everything needed to design and generate the
> station's discography: the shape it must have, the volumes, the release timeline, the IP firewall,
> and the production workflow. Read it once end to end before generating a single track. It assumes
> no access to the repository and no knowledge of the architecture.
>
> **This file is not world content and is never broadcast.** It names real-world genres and craft
> references freely so that Suno prompts can be written against them; **the catalogue you produce may
> not** (§8).

**The premise, in four lines.** Humanity lives scattered across many settled worlds, six centuries on
from now. Travel between worlds takes **weeks**; there is no faster-than-light anything and never
will be. Radio is the thread that connects them, and Settlement Radio is the station that broadcasts
it. Earth is distant history, spoken of fondly.

**What the station is.** A **speech station**. News, magazines, documentaries, one weekly chart.
Music leads in exactly four hours a day, all of them overnight: `Night Record` at 23:04 (56 min,
heritage — "one label or one year") and three `Night Watch` hours at 02:04, 03:04 and 04:04 (label
retrospectives, artist profiles, single-album stories, and one unhosted music sequence). Plus
`The Count`, the weekly chart, 28 minutes on Friday afternoon.

**Why this document exists.** The catalogue's shape is a formally open decision — the architecture
gives rotation weights and separation rules but has never stated how big the library must be, and
the phase plan blocks the whole of phase F on settling it. It is recorded here as a *structure*,
because the binding constraint is not a track count.

---

## 0. What the catalogue is, and where it goes

It is **not a folder of audio files with tags.** It is a discography that belongs to the world: labels
with house styles, artists with careers, albums with release years, tracks with credits. The audio
lives on an external volume; the meaning lives in `music/catalogue.yaml`, which is read into the
database and joined to the rest of the world.

Three things consume it, and each one asks for something different:

| Consumer | What it asks the catalogue for |
|---|---|
| **Rotation** — picks tracks for a music hour | breadth: enough distinct tracks, artists, albums and labels to satisfy the separation rules |
| **The shows** — a retrospective, a profile, an album story | depth: one label with several artists behind it, one artist with a real body of work |
| **The chart** — 40 positions computed weekly, top 20 aired | turnover: a front end of recent releases that keeps changing |

**Breadth is easy and depth is not.** A flat pile of 500 unrelated songs satisfies rotation and makes
every other programme unmakeable. That is the whole reason this is specified as a structure.

**Artists are people in the world.** Every artist becomes a `figures` row, which means a musician can
be quoted in a bulletin, die in a nightly world event, turn out to be someone's cousin, and have the
overnight back-announce pick it up without anyone writing that connection by hand. Labels can fold.
Recordings can surface. **This only works if the catalogue is written as biography rather than as
metadata.**

---

## 1. The shape — the decision

> *n* labels × artists per label × albums per artist × tracks per album, and the count falls out.

| Tier | Labels | Artists each | Releases each | Tracks | Subtotal |
|---|---|---|---|---|---|
| **Flagship** — deep enough to carry a 56-minute retrospective *and* two artist profiles | 2 | 5 | 2–3 | 8–12 | **~215** |
| **Standard** — deep enough for one retrospective | 4 | 3–4 | 2 | 8–10 | **~250** |
| **Import house** — old-system records, arriving late (§4) | 1 | 4 | 1–2 | 6–10 | **~45** |
| **Unaffiliated** — independents, one-offs, field recordings, observance music | — | ~6 | singles/EPs | 3–6 | **~30** |
| | **7** | **~32 artists** | **~68 releases** | | **~540 tracks** |

At the duration profile in §7 that is **roughly 34 hours of music**.

### The floors, staged by phase

**Do not treat 540 as a gate.** The catalogue is built in label-shaped batches and each completed
batch unlocks real programming, so the useful numbers are the staged ones:

| Milestone | Floor | What it buys |
|---|---|---|
| **Phase F** — "a music show whose host knows who played bass" | **140 tracks** — one flagship label and one standard label, both *complete* | one `Night Record`, one label retrospective, one artist profile. Proves the whole pipeline before 400 more tracks are committed to it |
| **Phase H** — the pre-built archive | **450 tracks** — all seven labels present | ~70 music-led archive hours can be built without a track recurring more than about twice across the whole pool |
| **Target** | **540 tracks** | comfortable rotation, a chart with somewhere to move |
| **Ongoing** | **40–60 tracks a year** | keeps the front end current as the in-world year advances (§3) |

**Below about 300 tracks the rotation's cold-start relaxations fire constantly** — the scheduler
starts dropping the label, album and artist separation rules to fill an hour, and logs a warning
every time. That is the real floor signal, and it is mechanical rather than a matter of taste.

### Rotation categories — how the 540 divides

Each track carries one category, and the category sets how often rotation reaches for it.

| Category | Weight | Meaning | Share | Tracks |
|---|---|---|---|---|
| A | 1.00 | heavy rotation | 12% | ~65 |
| new | 0.85 | released in-world within 8 weeks | 6% | ~30 (rolling) |
| B | 0.60 | | 24% | ~130 |
| gold | 0.45 | catalogue, ≥5 in-world years old | 28% | ~150 |
| C | 0.30 | | 21% | ~115 |
| specialist | 0.10 | only reachable when a programme asks for it by name | 9% | ~50 |

**`gold` is the largest single category, but current music is the majority of the catalogue** — the
two are not in conflict, because `gold` only means "at least five in-world years old", which most of
a working station's library always is. The overnight is heritage-*led*, not heritage-only, and a
`Night Record` built on records from the last twenty years is exactly right. **`specialist` is where
long pieces, observance and funeral music, degraded copies and anything else too strange for a normal
hour lives** — not a dumping ground, but the material that makes the Night Watch worth staying up for.

---

## 2. The genres — a closed list

The world's musical forms are already fixed in canon. **There are eight, and nothing may invent a
ninth** — a new form is a canon edit, not a catalogue decision, in the same way that the station's
seventeen subject domains are closed.

**All eight are current, living music.** This is not a stylistic preference; it is what the canon
facts actually say. `70-music.md` carries seventeen numbered facts, and the eight forms below are
each one of them. Two further names appear in that file — *Exodus Hymns* and *Drift Songs* — and
they appear **only in its prose, never in the fact list**. That distinction is load-bearing: prose
feeds a generated domain summary, while the fact list is the only route by which a specific detail
ever reaches the microphone. **Exodus Hymns and Drift Songs are period labels historians use. They
are not programming forms, they were never sayable on air, and the catalogue does not carry them.**

| Form | What it is | Tracks |
|---|---|---|
| **Relay-pop** | bright hooky harmony songs about love across the lag; the young form, and the station's biggest | ~115 |
| **Lane-rock** | freight-crew driving music, engine rhythms, whole-crew choruses; its occasion is *burn day* | ~90 |
| **Frontier Reels** | fast, rhythmic, danceable, played on salvaged and improvised instruments; music for hard work and harder celebration | ~80 |
| **Old-system sessions** | current releases arriving down the longest relay road from Earth's home system — blues, rock, the folk rounds | ~70 |
| **Pulse-dance** | four-on-the-floor from Meridian's sealed storm season; the living Synthesist argument | ~65 |
| **Void-lounge** | the core's late-club standard, slow and smoky, for the hour the honest and the hopeless rhyme | ~60 |
| **Core Harmonies** | big, layered, many-voiced; the sound of musicians who can rehearse in the same room | ~40 |
| **Void Ballads** | slow and spare, single voices over the drone of life support | ~20 |

### The production palette — what these actually sound like

The in-world name is what the station says. The real-genre words below are what you put in a
generation prompt, and they never leave this file (§8). **This table is the whole point of the two
vocabularies**, and it is where the pop, rock, rock-and-roll and blues live.

| In-world form | Prompt palette |
|---|---|
| **Relay-pop** | pop. Close-harmony, hook-first, three minutes, big chorus. Girl-group and Merseybeat shapes, power-pop, sunshine pop, modern radio pop |
| **Lane-rock** | rock. Driving four-piece, riff-led, singalong chorus, working-band swagger. Pub rock, heartland rock, boogie, hard rock at the edges |
| **Frontier Reels** | rock and roll and its roots. Rockabilly, skiffle, jump blues, bluegrass and reel tempos, zydeco stomp, upright bass and slapback. **This is the fastest, most joyful music on the station** |
| **Old-system sessions** | blues and early rock and roll — twelve-bar, slide guitar, piano triplets, jump and shuffle — plus folk rounds and country blues |
| **Pulse-dance** | dance pop. Four-on-the-floor, synth bass, big vocal hook. Italo, hi-NRG, house, synth-pop |
| **Void-lounge** | torch songs and slow blues. Smoky standards, brushed drums, late piano, soul ballads |
| **Core Harmonies** | choral and vocal-led large ensemble. Gospel mass, doo-wop stacked harmony, orchestral pop, big-band vocal |
| **Void Ballads** | spare solo song. Single voice and one instrument, drone underneath, country-gothic and folk-ballad shapes |

**Nothing in that right-hand column is ever spoken on air**, with one canon exception noted in §8.

**The three movements are an argument, not a genre.** The Purists (acoustic only), the Synthesists
(embrace what technology allows) and the Localists (each world grows its own language) cut *across*
the eight forms. Every artist should be placeable in that argument, and some should have changed
sides. It is the single richest source of DJ talk in the catalogue and it costs nothing to write down.

**Signature instruments are canon and must be audible.** Forge's **resonance pipes** — long alloy
tubes, deep organ-like tones, originally signalling devices. Concordance's **synth-harpsichord** —
plucked electronic strings, ancient and new at once. The Freeholds' **percussion built from
survival** — oxygen-tank drums, stripped-wire chimes, hands on metal. On the frontier, instruments
made of engineered composite rather than wood: thinner, brighter, prone to strange overtones. Real
wood and gut strings are luxuries of the core, and a core record should sound like it.

---

## 3. Now and past — the depth of field

**The listener lives in 2626 and this is their music, not a museum.** That single sentence governs
the whole section, and getting it wrong is the most likely way to make a catalogue nobody wants to
leave running.

### The diaspora is not in living memory and no one sings about it

Humanity left Earth six hundred years ago. For a listener in 2626, that is as remote as the fifteenth
century is to us. **Nobody writes chart songs about the fifteenth century.** A catalogue full of
solemn departure hymns and long patient crossing pieces would be a catalogue about grief for a home
that no living person, and no living person's great-great-grandparent, ever saw. It would sound
exactly like what it is: a station explaining its own premise to people who live inside it.

So the rule is blunt. **No song is about leaving Earth.** No song mourns the crossing, the cradle, or
the long dark. The songs are about what songs are always about — someone who isn't here, a shift
that won't end, a fight, a town, a night out, weather, money, wanting somebody. The setting does the
science fiction. The songs do the human part.

The one place the past is genuinely *present* is the old-system sessions, and even there it is
**current**: those are new records, made now, by people living now in Earth's home system, that take
a season to arrive. They are exciting because they are new and far away, not because they are old —
the way a new record from another continent was exciting on the radio in 1962. **Never present them
as archive.**

### Three depths — the same depth of field a real station has

Our own radio reaches back sixty or seventy years and no further. Theirs does the same.

| Depth | In-world age | What it is | Share |
|---|---|---|---|
| **Current** | 0–8 years | artists working now: touring, feuding, releasing, in the chart | **~50%** |
| **The last generation** | 8–35 years | the records their parents played. Mostly clean; a few survive only as damaged copies or as a review of a lost original | **~35%** |
| **The old standards** | 35–80 years | the founding recordings of the living forms — the first lane-rock record, the void-lounge singers everyone still covers | **~15%** |

**Anything older than that is not in the catalogue.** A handful of very old melodies do survive — a
tune people have sung so long that nobody can trace it, the way a carol works — and those appear
**only as recordings made now, by current artists, carrying current release years.** Cap them at
about ten tracks, all `specialist`, and never let a note frame one as a relic. "Nobody knows who
wrote it" is interesting. "It has been sung since the crossing" is the cry we are avoiding.

**A small set should sound genuinely old.** Ten or twelve tracks deliberately degraded — narrow band,
mono, tape noise, a dropout — presented as a surviving copy of a record from the old-standards
window. All `specialist`. Damaged audio is a spice; an hour of it is unlistenable.

### The release timeline

The in-world year is **the real year plus six hundred**, computed at generation time, so a catalogue
written now against a present of **2626** ages correctly by itself: a 2618 album is eight years old
today and nine next year, with nobody editing anything.

| Window | Years (present = 2626) | Share | Feeds |
|---|---|---|---|
| Current | 2619–2626 | 50% | `new`, `A`, `B`, the chart |
| The last generation | 2592–2618 | 35% | `B`, `gold` |
| The old standards | 2546–2591 | 15% | `gold`, `specialist` |

**Write the year. Never write the age.** No note may say "eight years ago", "last decade", "her
final record before she died last year", or "the twenty-year-old classic" — the station computes all
of that from the year and the current date, and a hardcoded age is wrong within twelve months. This
is the exact inverse of the rule for the world bible, where fixed years are forbidden: **in the
catalogue, years are mandatory and ages are banned.**

### Anchor years — what makes "one year" a programme

`Night Record` is *"one label or one year"*, and a year with nine tracks in it is not a programme.
**Do not spread releases evenly.** Cluster them into about **eight anchor years, each carrying ≥25
tracks across ≥4 artists and ≥2 labels.** Real music history clusters like this anyway — a scene
peaks, a label has a run, everyone releases at once. **Put five or six of the eight inside the last
thirty-five years**, where the listener's own memory is, and only two or three back in the
old-standards window.

Anchor years should sit on something that happened: a label founded, a label folded, a festival, a
disaster, a movement's turning point. That is what gives the host a reason to say *why* the year
mattered, and it lets the world's own nightly events generate anniversaries for free.

### The drip reserve — how the chart keeps moving

The chart needs new entries or it is a static list with a countdown read over it. The catalogue is
generated in a handful of sessions, but it must not all *arrive* at once.

**Hold back about 20% of the catalogue — roughly 100 tracks — as a reserve with staggered in-world
release dates**, entering rotation over the first six to twelve months. They are generated at the
same time as everything else; they simply carry a later date. This gives the chart a genuine front
end, gives the presenters something to introduce, and buys a year before the first top-up is needed.

---

## 4. The seven labels — slots, not names

Names, house styles, founding stories and rosters are the writer's to invent. What is fixed is the
**slot**: which scene, which world, which era, which role in the station's programming. Every world
named below is already canon.

| # | Tier | Home | Scene | Era | Role |
|---|---|---|---|---|---|
| 1 | Flagship | **Concordance** (core) | Core Harmonies and relay-pop, the establishment | old, still running | prestige and hits at once; the big vocal sound; the label the frontier resents and buys anyway |
| 2 | Flagship | **Cold Harbor** or the near frontier | Frontier Reels and Void Ballads | founded in living memory | the frontier's own voice; salvaged instruments; the fastest, loudest, most danceable roster on the station |
| 3 | Standard | **Meridian** storm coast | pulse-dance, Synthesist | recent, fast-growing | the young dance label; the loudest argument against the Purists |
| 4 | Standard | **Forge** | resonance pipes, heavy, lane-rock adjacent | industrial, long-lived | the workshop sound; makes instruments as well as records |
| 5 | Standard | **the between** — a hauler co-operative, no fixed world | lane-rock | member-owned, awkward, beloved | pressed off ships; distribution is its whole drama |
| 6 | Standard | **Concordance** or **Halcyon**, late-club | void-lounge | **defunct** — folded 10–25 years ago | the back-catalogue label; a folded label is the best retrospective in the building |
| 7 | Import house | routes to **the Old System** | old-system sessions | old, thin, precarious | not a label the station has a relationship with — an importer. It carries **current** Earth-system releases that took a season to arrive — blues, rock, the folk rounds — new at home and newer here |

**At least one label must be defunct and one must be in trouble.** A folded label has a story, a
disputed back-catalogue, a founder who will not talk about it, and a reason for a 56-minute
retrospective to exist at all. A label that is currently struggling gives the nightly world events
somewhere to go.

**The three big forms belong to no single label.** Relay-pop should appear on at least four of the
seven, lane-rock on three, Frontier Reels on three. Relay-pop in particular is canonically the form
found *everywhere the relays reach*; confining the station's biggest genre to one roster would make
it the property of one company, and would make every pop record on the air sound the same.

### Two obligations to existing canon

Four musicians are already named in the world bible and the catalogue must honour them rather than
work around them. **All four are dead**, which is why they are in canon at all — the bible names only
the dead and the legendary.

- **Odessa Vail**, composer of one towering Core Harmony cycle, *Lanternlight*, written for a Lumen
  Festival, who then stopped. Canon does not date her, so **place her in the old-standards window** —
  she died within living memory and people who saw the première are elderly, not legendary. Her own
  recording exists; the catalogue also carries later **performances** of *Lanternlight*, by different
  artists, disagreeing about it.
- **Corin Hale, the Vigilkeeper**, who spent a lifetime on one relay outpost and emerged with the
  *Station Cycles* — Void Ballads built around the outpost's life-support drone, which Hale refused
  to have repaired because it had become the tonic note. Canon says other stations keep a Hale piece
  within reach, so **the recordings are playable and Hale sits in the old-standards window at the
  latest.** The drone is the sound: build it into the palette rather than describing it in a note.
- **Adra Pell and Lio Tern**, relay-pop partners who recorded apart, passing verses between two
  settlements, and whose public quarrel over an altered credit was never resolved while they lived.
  Their last shared recording carries no spoken introduction. Both are dead — **recently enough that
  the argument is still live**. Give them a real discography; the quarrel is worth three programmes
  on its own.

**The bible names only the dead and the legendary — living musicians belong to the catalogue and to
the world's own record, never to canon.** So the living artists you invent go in
`music/catalogue.yaml`, and that is the correct and only home for them.

---

## 5. What each programme needs — the makeability rules

These are the constraints the structure exists to satisfy. Check the catalogue against them before
declaring a batch finished.

| Programme | Length | Needs |
|---|---|---|
| **Label retrospective** (Night Watch) | 56 min, 14 tracks | one label with **≥3 artists, ≥6 releases and ≥40 tracks**, so no artist appears more than four times in the hour |
| **Artist profile** (Night Watch) | 56 min, 14 tracks | one artist with **≥18 tracks** — 14 is the arithmetic minimum and leaves the second profile of that artist identical to the first |
| **Album story** (Night Watch) | 56 min | a **cornerstone album of 12–14 tracks**. Designate **6–8** of these across the catalogue; a standard 8-track album cannot fill the hour without padding |
| **One year** (Night Record) | 56 min, 14 tracks | an **anchor year: ≥25 tracks, ≥4 artists, ≥2 labels** (§3) |
| **Music sequence** (04:04, unhosted) | 56 min | no talk, so it needs **mood coherence** — enough tracks sharing a mood tag to build an unbroken hour. It still runs on songs; there is no instrumental hour |
| **The Count** (weekly chart) | 28 min, 20 of 40 positions aired as 30–40s clips | **≥80 tracks eligible** as current at any moment, and turnover from the drip reserve |
| **Rotation** (any music hour) | separation: same track ≥4h, artist ≥60min, album ≥90min, label ≥30min | ≥7 labels, ≥30 artists, ≥60 releases — the label rule at 30 minutes is the one a small catalogue breaks first |

**The artist-profile rule is the one that sets the shape.** Fourteen tracks an hour means an artist
needs two or three real albums before a profile is possible, and that single requirement is what turns
"generate 500 songs" into "generate sixty albums".

---

## 6. What to write for each entry

Deliver as `music/catalogue.yaml`. Four lists — `labels`, `artists`, `albums`, `tracks` — plus
credits. Every entry needs an id, and ids never change once assigned.

**Label** — name · home settlement · founded year (· defunct year) · **house style in one concrete
phrase** ("close-mic, unhurried" is the example the architecture gives; "warm" is not a house style)
· two or three sentences of story: who founded it, what it believed, what went wrong.

**Artist** — name · kind (solo, group or collective) · home settlement · label · scene · active_from
(· active_to) · members with roles and years for groups · **a bio of two to four sentences in plain
speech**. Where they stand in the Purist/Synthesist/Localist argument, and whether they moved. What
they are actually like. Not "a haunting voice from the outer dark" — *"records everything in one
take because she thinks second takes sound like apologies."*

**Album** — title · artist · label · release year · kind (album, EP, single, live) · **notes: the
story.** What was happening when it was made, what it cost, who left the band during it, whether it
sold. This field is where a retrospective comes from.

**Track** — title · album · track number · duration · mood tags · tempo · energy · category ·
`intro_ramp_sec` · `outro_type` · `licence_note` · **and one fact.**

> ### The one-fact rule — the most important line in this document
>
> The overnight host's `back_announce` link is defined as *"what just played, with one fact."* If a
> track has no fact attached, that link has nothing to say and the model will invent something —
> which is exactly the failure the whole discography exists to prevent.
>
> **Every track carries one concrete, sayable fact.** Who played the part everyone remembers. Which
> take it is. What it was written about. Where it was recorded and why that was a bad idea. What it
> replaced on the record. Which argument it settled. One sentence. Five hundred and forty of them is
> the single largest piece of writing in this commission and it is what makes the station sound like
> it knows things.

**Lyrics** — written by hand, never generated (§8). What they are about is the single biggest lever
on whether the station sounds inhabited or explained.

> **Write about the thing, not about the setting.** A song is somebody who left, a shift that will
> not end, a fight in a bar, money, weather, a town, wanting somebody who is a long way off. The
> world supplies the *furniture* — the relay, the burn day, the storm season, the ice, the last ferry
> — and never the subject. "I'll be on the thread at the hour, same as always" is a love song that
> happens to live here. "Six hundred years ago our ancestors left the cradle" is a history lesson
> with a tune.
>
> **The test:** if the lyric would still work with the science-fiction nouns swapped for ordinary
> ones, it is right. If swapping them leaves nothing, the song was about the premise.

**Credits** — writer, player, producer, per track, each linked to a person in the world.
**Six to ten recurring session players who appear across at least three labels.** This is the cheapest
possible way to make a discography feel like an industry rather than a spreadsheet, and the station's
music presenter is written specifically to notice it — her habit is to name the overlooked player
before giving an opinion. Give her someone to name.

---

## 7. The technical spec

Audio the mixer has to work with, not audio in the abstract.

**Duration.** A 56-minute music show is 14 tracks and about six minutes of speech, so the
**rotation-eligible average must land near 3:30**. Longer pieces are legitimate but they are
`specialist` and they displace two other tracks.

| Band | Share |
|---|---|
| 2:00–3:00 | 28% |
| 3:00–4:00 | 42% |
| 4:00–5:30 | 22% |
| 5:30–8:00 | 7% |
| 8:00–11:00 | 1% — `specialist` only |

**Most of this catalogue is pop and rock, so most of it is under four minutes**, which is what a
song of that kind is. The long tail exists for the Core Harmony cycles and the odd Void Ballad, and
that is all it is for.

**Nothing under 2:00 belongs in the catalogue.** Short pieces are station imaging, which is a
separate commission with its own rules.

**Intro ramps.** The host talks over the intro and must stop before the vocal, so the ramp length is
a hard input to the writer, timed to the second.

- **≥40% of tracks must have an intro ramp of ≥8 seconds.** Below this, the `ramp_talk` link becomes
  unmakeable and the overnight loses its best-sounding move.
- **≥15% should have a ramp of ≥15 seconds** — the long ones a host actually enjoys.
- Ramps are **measured by ear and corrected by hand** after generation. The generator does not know
  what it produced and an automatic estimate will clip a vocal.

**Outros.** Roughly **30% cold, 45% fade, 25% sustain**. Cold endings are what let the hour hit the
junction on time; a catalogue of long fades makes every back-time a compromise.

**Every track has a vocal. There are no instrumentals in the catalogue.** A song has a singer; that
is what makes it a song, what gives a listener something to hold, and what stops the overnight
sliding into wallpaper. Instrumental *passages* are fine and wanted — intros, breaks, a solo, an
outro — but no track is wordless end to end, and **Core Harmonies are choral and vocal-led rather
than orchestral**, which is also the reading the canon supports.

Two things this does not break, since both look like they might:

- **The intro-ramp requirement is unaffected.** Every song has an instrumental intro before the first
  line; that is what the host talks over, and the ramp is measured to the vocal entry.
- **Beds, underscore and anything that plays beneath speech are imaging, not catalogue.** They are a
  separate commission with their own rules, and pulling them out of here is what lets this rule be
  absolute.

**Language.** Everything sung is in **Standard** — which is English — or is wordless. Regional
character comes from instrumentation, rhythm, arrangement and accent, never from switching language.
**Do not generate lyrics in a real minority or indigenous language to signal "frontier".** It is not
ours to borrow, it will not survive the first listener who speaks it, and the world already gives
better tools for the job.

**Loudness.** Master everything to one consistent target and check it. A catalogue that jumps six
decibels between tracks sounds like a playlist; radio's whole texture depends on it not doing that.

**Files.** One directory per album, tracks numbered: `music/<label>/<album>/03.mp3`. The path is
recorded in the catalogue, so the layout is fixed once and never reorganised.

---

## 8. IP — the hard rules

The station is a **tribute, not a derivative**, and the music library is the place where that is
easiest to breach without noticing, because generative music tools are trained on real records and
will happily be steered toward one.

### The two vocabularies

This is the whole mechanism, and it is the same trick the world bible uses to name real authors in a
brief that is never broadcast.

| | Where it is used | May contain |
|---|---|---|
| **Production vocabulary** | Suno prompts, the provenance record | real **genre and technique** words — "brushed drums", "close-mic'd fiddle reel", "four-on-the-floor synth", "smoky late-night jazz ballad". These describe a *sound*, and a sound is not property |
| **In-world vocabulary** | `catalogue.yaml`, the air, the website | **only the eight canon forms.** On air it is a Frontier Reel, never a rockabilly number; a void-lounge standard, never a torch song |

**The prompts must never reach the catalogue file**, because the catalogue is read into the station
and its text can reach the microphone. Prompts live in the provenance record (§9) and nowhere else.

**One canon exception, and it is exactly three words wide.** Canon fact 17 says the old system is
where *"blues, rock, and the folk rounds"* never died. **Those three terms — `blues`, `rock`, `the
folk rounds` — are air-legal, and only for old-system material.** Nothing else on the palette is:
not "rock and roll", not "rockabilly", not "country", not "soul", not "house". A host may say a
record is *blues* if it came down the long relay road, and must otherwise say *void-lounge*.

It is a good detail rather than a grudging carve-out: the old words survive in exactly the one place
the old music does, which is precisely why those records feel like they come from somewhere else.

### The eight rules

1. **Never prompt with a real artist, band, producer, album, song or label name.** No "in the style
   of", no "sounds like", no "meets", no era-plus-artist shorthand. Not once, not for a test. The
   prompt is logged, so this is auditable after the fact.
2. **Never prompt for a real singer's voice**, by name, by description of a specific person, or by
   uploading a real person's audio. The station's rule against cloning any real voice covers singing.
3. **Write the lyrics yourself and paste them in.** Do not let the generator write them. Generated
   lyrics are unscreened, they can reproduce fragments of real songs, and lyrics are broadcast
   content that has to pass the same safety gate as a news script. This is the single most likely
   route to an actual infringement and it is entirely avoidable.
4. **Lyrics may not name any real person, brand, company, franchise, work or event.** The only real
   places that may be named are the ones canon already allows for the old system: Earth, Mars,
   Europa, Titan, Saturn, the Belt.
5. **Every artist, group and label name is screened as a real-world entity** before it is committed —
   the same screen the station runs on invented people: an exact full-name match against a notable
   real person or organisation is an error and gets regenerated; a partial or fuzzy match is flagged
   for the operator to judge. Group names and label names go through the organisation list.
6. **Album and track titles are screened too, and this is a gap worth closing deliberately.** The
   existing screen covers persons and organisations, not *works*. Song titles are short and collide
   constantly, so the workable rule is: **titles of two or more words**, avoiding any title famous
   enough that a listener would recognise it, checked against a well-known-recordings list as a flag
   rather than a block. Anything that fires gets added to the banned-entities list so it never
   recurs.
7. **No real-world cover art, logos, typography or design lifted from a real label.** The public
   discography page is a publication like any other.
8. **Keep the licence evidence, per generation period.** The plan tier, the date, and a copy of the
   commercial-use terms as they read on that date. Every track records which period it was made
   under (`suno-pro-2026-08` and so on). If the terms change or the plan lapses, tracks made earlier
   keep their original note — that is the entire point of recording it per track rather than once.

**The litmus test, unchanged from the rest of the world:** if a listener could name the real artist
or record from what they hear or from what the host says about it, it has crossed the line. Regenerate
until only the *feeling* remains, dressed in the world's own specifics.

---

## 9. Production — how to actually make 540 tracks

**Generate in album-shaped batches, never as singles.** One label at a time, complete: label →
artists → albums → tracks → credits. A finished batch is immediately worth something — it unlocks a
retrospective — whereas 500 scattered singles unlock nothing until the last one lands.

**One style palette per label.** Fix the label's production prompt vocabulary before generating its
first album, and reuse it across every artist on the roster. This is what makes "labels have a house
style" audible rather than a sentence in a database. Vary within the palette per artist; vary
within the artist per track.

**One voice per artist, held across albums.** Whatever the tool offers for voice consistency, use it
and record the identifier. An artist profile is 56 minutes of one artist; if the voice changes
between albums, the show does not work. **This is the setting most worth getting right before
volume.**

**Order of work.**

1. **Pilot — one label, ~70 tracks.** Take a flagship label all the way through: generate, master,
   measure ramps by ear, write the catalogue entries, write the one-fact line for every track. Then
   build one label retrospective from it and *listen to the hour*. Everything about the remaining 470
   tracks should be decided by that hour and not before.
2. **Second label** — reach the phase F floor of 140.
3. **The remaining five labels**, one per session.
4. **The drip reserve**, dated forward.

**Provenance, written as each track is made.** Per track: the exact prompt, the voice or persona
identifier, the model version, the date, the licence period, and an explicit statement that no real
artist, work or voice was named or referenced. **This cannot be reconstructed six months later** — a
model version and a prompt are gone the moment the session closes. The station already runs this
discipline for its presenters' voice clips and it exists for exactly this reason. `music/PROVENANCE.md`
is the natural home; **it does not exist yet and creating it needs the operator's word.**

**The honest effort estimate.** At several attempts per keeper and a few minutes of listening each,
540 tracks is on the order of **30–40 hours of operator time**, plus the writing. Call it eight to ten
working sessions, and note that the *writing* — 32 bios, 68 album notes and 540 one-fact lines — is
comparable again. It is the largest single content item in the project after the world bible, and it
is why the phase F floor is 140 and not 540.

---

## 10. Never — the hard list

- **Never name a real artist, band, label, producer, album or song** in a prompt, a lyric, a
  catalogue field, or anything the station can say.
- **Never prompt for a real person's singing voice**, or upload one.
- **Never let the generator write the lyrics.**
- **Never put a Suno prompt in `catalogue.yaml`.** It can reach the microphone.
- **Never invent a ninth musical form.** The eight are canon; Exodus Hymns and Drift Songs are period
  labels that live in canon prose and were never sayable on air, and neither is a form the catalogue
  carries.
- **Never write a song about leaving Earth**, the crossing, the cradle, or the long dark. Six hundred
  years have passed and nobody is still crying about it.
- **Never present an old-system record as archive.** They are current releases that arrived late.
- **Never generate an instrumental.** Every track has a vocal; beds and underscore are imaging.
- **Never write an age, a relative date, or "recently".** Write the year; the station does the rest.
- **Never write a track without its one fact.**
- **Never write a bio in the station's late-night register.** Plain speech, concrete detail, the way
  people at work talk about their colleagues. The lyricism belongs in the songs.
- **Never spread release years evenly.** Cluster into anchor years or `Night Record` has no premise.
- **Never generate a track under two minutes** and call it catalogue.
- **Never seed fake airplay** to make the chart look established. Airplay is 45% of the chart score
  and invented plays corrupt it permanently.
- **Never rename an id** once it is committed. Titles can be edited; identity cannot.

---

## 11. Before you hand it back

- [ ] Seven labels, at least one defunct and one in trouble.
- [ ] Every label has a house style stated as a concrete production phrase.
- [ ] Two labels satisfy the retrospective rule: ≥3 artists, ≥6 releases, ≥40 tracks.
- [ ] At least four artists have ≥18 tracks (artist profiles).
- [ ] Six to eight cornerstone albums of 12–14 tracks (album stories).
- [ ] Eight anchor years, each ≥25 tracks across ≥4 artists and ≥2 labels; five or six of them
      inside the last thirty-five years.
- [ ] All eight canon forms present, in roughly the stated proportions — and relay-pop, lane-rock and
      Frontier Reels together are half the catalogue.
- [ ] Every track has a vocal. No instrumentals anywhere.
- [ ] No lyric is about leaving Earth, the crossing or the long dark; every lyric passes the
      swap-the-nouns test.
- [ ] Half the catalogue is under eight in-world years old; nothing is older than eighty.
- [ ] Six to ten session players recurring across ≥3 labels.
- [ ] Odessa Vail's cycle performed; Pell and Tern have a real discography and a last recording.
- [ ] Every track has a category, a mood, a measured intro ramp, an outro type, a licence note —
      **and one fact.**
- [ ] ≥40% of ramps at 8 seconds or more; ≥15% at 15 or more.
- [ ] Rotation-eligible average duration near 3:30; nothing under 2:00.
- [ ] Roughly 20% of the catalogue held back as drip reserve with forward dates.
- [ ] No age, no relative date, no fixed "today" anywhere in the notes.
- [ ] Every artist, group, label and title through the real-entity screen; every hit recorded.
- [ ] Provenance written for every track, at the time it was made.
- [ ] Licence evidence captured for the generation period.

---

## 12. Working the commission — the practical loop

*This section is for the operator, not the writer. It is how the rest of this document gets used
while no code exists yet. Everything it produces loads unchanged once `make music-sync` is built.*

### The one thing to understand first

**This document is the writer's system prompt.** It is deliberately self-contained and assumes no
access to the repository, so the workflow is: paste `COMMISSION.md` whole as the writer's context,
then give a short per-batch instruction. That is why the two briefs below are four lines each
instead of four pages.

**Work one label at a time, start to finish.** A finished label unlocks a real programme. Seven
half-finished labels unlock nothing.

### The split that makes the whole thing work

Two artefacts come out of every batch, and **they must never merge**:

| File | Contains | Reaches the air? |
|---|---|---|
| `catalogue.yaml` fragment | labels, artists, albums, tracks, credits, the one-fact lines | **yes** — this is read into the station |
| production sheet | Suno prompts, lyrics, persona ids, seeds, model version, dates | **never** — prompts and real genre words live here and nowhere else (§8) |

Suggested layout, one directory per batch:

```
music/
  COMMISSION.md
  batches/
    01-<label>/
      catalogue.yaml      → merged into music/catalogue.yaml when the batch is done
      production.md       → prompts, lyrics, provenance. Never parsed by anything
      audio/<album>/NN.mp3
```

### Four nested levels — read this before the step list

Almost every ordering question answers itself once the nesting is clear. **Each level is a different
unit of a different thing:**

```
LABEL     ← one batch, one working session, one style palette
  ARTIST  ← one voice. The persona is pinned here and nowhere else
    ALBUM ← one message to the writer. Lyrics arrive an album at a time
      TRACK ← one generation
```

**You never invent a band.** You pick a *slot* — one row of §4 — and write ten lines of constraint.
The writer invents the label, its roster, its albums and its titles inside that constraint. Your job
is choosing, screening and listening; the writer's job is inventing; Suno's job is performing.

### Stage 0 — the catalogue constants, decided once before batch 1

**Two things cannot be decided per batch, and this is the gap that ruins a catalogue quietly.** If
each label picks its own years and its own players independently, nothing ever lines up and two of
the programmes in §5 become unmakeable.

| Constant | Why it cannot wait |
|---|---|
| **The eight anchor years** | `Night Record` plays "one label or **one year**". A year is only a programme if ≥25 tracks across ≥4 artists and ≥2 labels landed in it. Labels written independently will scatter across eighty years and cluster in none |
| **The 6–10 recurring session players** | §6 requires them to appear across **≥3 labels**. A player invented during batch 4 cannot retroactively have played on batches 1–3 |

Both are one short conversation with the writer, before any label exists. Keep the results in a file
you paste into **every** later brief, alongside the running list of names already used.

```
Brief 0 — the constants. Read COMMISSION.md first.

Return two lists and nothing else:

1. Eight anchor years, present = 2626. Five or six inside the last thirty-five
   years, two or three in the old-standards window. One line each: what happened
   in the world of music that year that made everyone release at once.

2. Six to ten session players — name, instrument, one line of character. These
   are the people who turn up on everybody's records. Spread the instruments;
   include at least one resonance-pipe player and one synth-harpsichord player.
```

### The loop, per label

| # | Who | Step | Level |
|---|---|---|---|
| 1 | you | **Write the slot card** — ten fields, below. This is the only creative decision you make per batch | label |
| 2 | writer | **Brief A — the roster.** Returns the label, its artists, its albums, and every track *title* with its one-fact line. **No lyrics, no prompts, no durations** | label |
| 3 | you | **Screen the names** (§8 rules 5–6). Search every artist, group, label and title. A collision costs one message now and a re-record later | label |
| 4 | you | **Assign ids and file paths.** `t_0141`, `music/<label>/<album>/03.mp3`. Before generation, so the audio has somewhere to land | label |
| | | **↓ then repeat 5–8 for each artist on the roster** | |
| 5 | writer | **Brief B — the artist's first album.** Returns, per track: lyrics plus a style prompt from the §2 palette | album |
| 6 | you | **Cast the voice.** Generate 3–5 of those tracks. Pick the best *voice*. Pin it as a persona named the artist's id | artist |
| 7 | you | **Generate the rest of that album** with the persona applied. Log as you go | track |
| 8 | writer→you | **Brief B for their next album, generate, repeat.** The persona is already fixed — no second audition | album |
| | | **↑ next artist** | |
| 9 | you | **Measure** every keeper: real duration, intro ramp to the vocal entry, outro type | track |
| 10 | you | **Complete the catalogue entries** with the measured fields. Batch closed | label |

**So the lyrics always exist before the audition** — they arrive at step 5 and the casting at step 6
uses them. You are never generating against placeholder words, and the audition takes are usually
keepers, so nothing is wasted.

### Step 1 in detail — the slot card

**Ten fields. Nothing else.** Eight of them you copy from §4 and §1; only two are a real judgement
call, and those two are the ones that make this label different from the other six.

| # | Field | Where it comes from |
|---|---|---|
| 1 | **Slot** | the §4 row number |
| 2 | **Home** | §4 — a world already in canon |
| 3 | **Forms and the split** | §4, with track counts that respect §2's totals |
| 4 | **Era** | §4 — founded when, still running or folded |
| 5 | **Roster size** | §1 — flagship, standard or import |
| 6 | **House style** | **yours.** One concrete production phrase |
| 7 | **Standing** | Purist, Synthesist or Localist — and whether they moved (§2) |
| 8 | **Its trouble** | **yours.** What is going wrong for it now |
| 9 | **Anchor years** | which of Stage 0's eight this label lands on |
| 10 | **Must make possible** | which §5 programmes this batch has to unlock |

**Field 6 is the one that carries the sound.** "Warm" is not a house style; it tells the writer
nothing and tells Suno less. A house style is a phrase an engineer could act on — the architecture's
own example is *"close-mic, unhurried"*. Everything the label releases has to be recognisably that.

**Field 8 is what gives the world something to do with the label.** A label with no trouble generates
no beats, no anniversaries and no retrospective worth 56 minutes.

> **Worked example — slot 1. Copy the shape; replace every value with your own.** Fields 6 and 8
> below are placeholders standing in for your decisions, not recommendations.

```
1  Slot            1 — flagship, core prestige
2  Home            Concordance
3  Forms           Core Harmonies ~40 (the whole world's supply — this is its home)
                   relay-pop ~45 (its commercial half)
                   void-lounge ~20 (the core's late clubs)
4  Era             Old. Founded generations back, still running, still the incumbent
5  Roster          5 artists · 2–3 albums each · 8–12 tracks · ~105 tracks total
                   at least 2 artists with 18+ tracks (artist profiles)
                   at least 1 cornerstone album of 12–14 (album story)
6  House style     <yours> — e.g. "room mics, real players, nothing hurried,
                   every record sounds like it was made in the same hall"
7  Standing        Purist by conviction and Synthesist in practice; they deny this
8  Its trouble     <yours> — e.g. not failing, just complacent: an ageing roster,
                   and the young acts keep signing with the frontier instead
9  Anchor years    lands on Stage 0 anchors <A>, <C>, <F>
10 Must unlock     one label retrospective · two artist profiles · one album story
```

That is the whole of your creative input for a batch of a hundred tracks. Everything else — the
label's name, its founders, its five artists, their albums, every title and every one-fact line —
comes back from the writer in step 2.

### Brief A — the roster

> Paste after `COMMISSION.md`. Always include the Stage 0 constants and the running names list, or
> the writer will scatter the years and reinvent the same three surnames every batch.

```
Write batch <N>: label slot <#> from §4.

<your ten lines: home world, forms it carries, era, house style, its trouble>

Return YAML only, in the §17a shape: one label, its artists, its albums, and every
track with title, track_no, and its one-fact line. Follow §3 for release years and
§5 for how deep the roster has to be. No lyrics, no prompts, no durations.

Anchor years — put most releases on these:
<paste Stage 0 list 1>

Session players available to credit:
<paste Stage 0 list 2>

Names already used elsewhere in the catalogue, do not reuse or echo:
<paste running list>
```

### Brief B — songs

> **One album per message**, in the same conversation as Brief A so the writer still has the roster.
> Smaller messages hold the palette far better than one enormous one.

```
Album: <title>, <artist>, <year>, <form>.

For each track return:
  1. lyrics — §6's subject rules and the swap-the-nouns test.
     Open with an instrumental-intro tag before the first verse.
  2. a Suno style prompt from the §2 palette for this form, and an
     exclude-styles line.

Every track has a vocal. Nothing about leaving Earth. Keep the label's
house style audible across all of them — this is one label's record.
```

**On the artist's *first* album, add one line:** `Order the tracks so the first three are the most
typical of this singer` — those are the three you audition with, and you want them representative
rather than the three strangest things on the record.

### The two-pass rule for track fields

**Half the track fields cannot exist before the audio does.** Trying to write them up front produces
fiction, and the mixer will believe it.

| Written at Brief A | Written after generation, by ear |
|---|---|
| title · track_no · album · artist · category · mood · one fact | `duration_sec` · `intro_ramp_sec` · `outro_type` · `bpm` · `licence_note` |

**`intro_ramp_sec` is the one that must be measured rather than estimated.** It is the exact number
of seconds until the first sung word, and the overnight host talks across it. An estimate that is
two seconds long clips a vocal on air, every time that track plays, forever.

### Generating — what actually matters in the session

- **Use custom mode** — your lyrics, your style prompt. Never let the tool write lyrics (§8 rule 3).

#### One voice per artist — the audition, and why it comes first

**The artist is the unit of voice identity, not the track.** An artist profile is 56 minutes of one
artist and an album story is 12–14 tracks off one record. Generate those track by track without
pinning a voice and you get fourteen different singers, the host says *"another one from her second
record"* over a stranger, and the programme is unmakeable. This is the single most expensive mistake
available in the whole commission, and it is invisible until you build the show.

So, before generating an artist's catalogue, spend twenty minutes casting them:

1. **Audition.** Generate three to five tracks for that artist on the label's style palette. Use real
   lyrics from their album — this is not wasted work, one of these usually becomes a keeper.
2. **Choose on voice, not on song.** You are casting a singer, not picking a single. The best song
   with the wrong voice loses to a mediocre song with the right one.
3. **Pin it.** Make that take into a reusable voice — whatever the current interface calls a
   *persona* — and **name it exactly the artist's id** (`marren`, not "cool folk singer 2"), so the
   log, the catalogue and the tool all say the same word.
4. **Generate the artist's whole discography with it applied**, varying the style prompt per track
   only *within* the label's palette. Push the prompt far from the persona's origin and the two
   fight; you get drift, which is the thing the persona existed to prevent.
5. **A group with two lead singers needs two personas.** Record which sings what in the credits —
   "the other one sings this one" is exactly the detail the music presenter is written to notice.

**Finish an artist inside one model version.** If the tool upgrades mid-catalogue, the same persona
can come back subtly different, and an artist whose albums straddle two versions will not sound like
one person. Record the version per track; if an upgrade lands mid-artist, finish that artist on the
old version rather than starting the next album on the new one.

> **This is the same trap as the presenters' voices, and it bites earlier.** The architecture forces
> a decision at build step 13b — bulk re-render versus an in-world change — *before fifty shows exist
> in a voice*, because after that it is unaffordable. Artist voices have the identical shape: losing
> a persona means re-rendering that artist's **entire catalogue**, not one track. Decide how you are
> storing and backing up persona ids at the pilot, not at label six.
- **Force the intro ramp with a structure tag.** Put an explicit instrumental-intro tag at the top of
  the lyric before the first verse. This is the practical lever for §7's rule that 40% of tracks need
  a ramp of eight seconds or more — you cannot get there by hoping.
- **Use the exclude-styles field.** It is what stops a Frontier Reel drifting into something else
  halfway through, and it costs one line.
- **Keep the reject.** When a take is nearly right, the next prompt is a small edit of the last one,
  not a fresh idea.
- **Check your plan's monthly generation allowance against the real number.** At several attempts per
  keeper, 540 tracks will very likely span more than one billing month — which means **more than one
  licence period**, and `licence_note` must record which period each track was actually made in
  (§8 rule 8). Capture the plan's commercial-use terms as they read **at the start of each month you
  generate in**, not once at the end.

### Logging as you go — what that actually means

**Write the row at the moment you keep the take, not at the end of the session.** Two of these
fields cannot be reconstructed afterwards: the exact prompt (you will have edited it six times) and
the model version (an upgrade rewrites what "current" means). The tool's own history will not save
you, because it cannot tell you *which* take you kept or why.

Three things happen the moment a take is a keeper, in this order:

1. **Download it and rename it to the assigned path immediately** —
   `music/<label>/<album>/03.mp3`. The tool's default filenames are unusable and after forty tracks
   you will not know which is which. This is the step people skip and regret.
2. **Paste the prompt block into `production.md`** — the style prompt, the exclude-styles line, and
   the persona used. Verbatim, not summarised.
3. **Add the log row.**

One table per batch, at the top of `production.md`:

```
| track id | title | attempts | persona | model ver | date | licence period |
```

Plus, once per batch rather than per track, the line §8 rule 8 requires: **an explicit statement
that no real artist, work, band, label or voice was named, referenced or uploaded anywhere in this
batch.** That sentence, and the prompts sitting underneath it as evidence, are what the phase G
lawyer review is actually going to read.

### A batch is done when

- [ ] Every name in it has been screened and the hits recorded.
- [ ] Every track has audio, a measured ramp, a real duration and an outro type.
- [ ] Every track has its one fact.
- [ ] The catalogue fragment contains no prompt text and no real genre word.
- [ ] The production sheet contains every prompt, persona and date.
- [ ] You have listened to fourteen of them back to back as if it were the hour. **That listen is
      the only quality gate in this project** — nothing automated grades the product.

### Where to start

**Do the pilot before anything else.** One flagship label, roughly seventy tracks, all the way
through — then build a label retrospective hour from it and *listen to it*. Everything about the
remaining 470 tracks should be decided by that hour. If the palette is wrong, it is one label's work
to redo, not seven.
