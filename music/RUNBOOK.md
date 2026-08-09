# RUNBOOK.md — the music, start to finish

> **`music/MUSIC_TASKS.md` is the sequence. This page is the method.** That file says which card is
> next; this one says what actually happens when you run it, and what only you can do.
>
> Do the card marked **NEXT**. That is the whole method.

---

## The commands, all of them

| Command | What it does |
|---|---|
| `make check` | Counts the wiki against the plan. Green means it adds up |
| `make music-albums` | Lists every album with its id and layer (use `GENRE=` to filter) |

**Two commands, and neither one asks you to paste anything anywhere.** The wiki, the style cards
and the lyrics are written by an agent in this repository, one card at a time. You open a session
and say the number — "Do M-07" — and the file lands in git where it belongs.

## The nine genres

`relay-pop` · `lane-rock` · `deck-talk` · `frontier-reels` · `old-system-sessions` ·
`pulse-dance` · `void-lounge` · `core-harmonies` · `void-ballads`

## Where things live

| File | What goes in it |
|---|---|
| `music/wiki/<genre>.yaml` | one genre's bands, albums and songs. **All nine files exist** |
| `music/CONSTANTS.md` | anchor years, session players, the used-names list |
| `music/plan.yaml` | how the 500 songs divide. The authority for every count |
| `music/production/styles.yaml` | the band style cards, keyed by band id |
| `music/production/lyrics/<album>.yaml` | one file per album, lyrics + prompts |
| `music/audio/<label>/<album>/NN.mp3` | the audio. Not in git — it lives on the volume |

---

# Part 1 — the wiki

**Nine genres. No Suno, no hardware, nothing to buy.** This is the bulk of the work and the part
the presenters actually use.

## Step 0 · Two loose ends in `CONSTANTS.md`, still open

Neither has a card, and both are cheap now and awkward once eight more genres cite them:

- **"Deym Rusk" reads as a filed-off Dean Rusk** (§3 flags it and recommends replacing). Same
  instrument, same character, new name.
- **The session players in §2 have no dates, and there are no elders.** The eight are one
  generation working roughly 2592–2626; the old-standards window (2546–2591) needs three or four
  of its own. Without dates, a batch will credit someone to a session they were eleven for.

`music/wiki/relay-pop.yaml` already gave its seven players dates — §2 has not caught up.

## Step 1 · Run the card

Open a session in this repository and say the card number. The agent reads `MUSIC_TASKS.md`,
`COMMISSION.md`, `CONSTANTS.md` and that genre's row of `plan.yaml`, writes
`music/wiki/<genre>.yaml`, and runs `make check` before it finishes.

**One card per session.** Two cards in one session is how the thread gets lost.

## Step 2 · Read `make check`

Green means the counting is right: every label has its share of playable songs, every layer-A song
has a fact, no layer-B song has one, every album is dated to an anchor year, and no id is used
twice. Red names the genre and both numbers.

**Green is not "good".** It means nothing is miscounted. Whether the bios read well is yours.

## Step 3 · Screen the names

Every band, label, album title, song title and person the genre invented. `make music-screen`
(M-03) narrows the pile to exact matches against real notable names; the rest is your judgement.

| What you find | Verdict |
|---|---|
| Nothing at all | ✅ keep — the normal result |
| A LinkedIn profile, a forum user, a private person | ✅ keep |
| Only the surname matches something real | ✅ keep |
| A real notable person with that **exact full name** | ❌ replace |
| A name that reads as a famous name with a letter changed | ❌ replace |

**Record what you cleared** in `music/CONSTANTS.md` §3, so the next genre does not reuse it. Record
what you rejected too — otherwise the same collision gets proposed twice.

## Step 4 · The catalogue-wide pass

After the ninth genre, M-15 checks the things that are properties of the whole catalogue rather
than of one genre: 500 songs, 25 bands, every anchor year carrying enough records, every label able
to make a retrospective. **The wiki freezes when that card closes**, and no lyrics are written
before it does — moving a release year is free until songs exist against it.

---

# Part 2 — the songs

**Only after Part 1 is finished.** Now you need a Suno account.

## Step 5 · Style cards and lyrics

M-16 and M-20 write the style cards; M-17 and M-21 … M-29 write the lyrics and generation prompts,
a whole album at a time. Both are agent cards. `make music-albums` shows a `yes` in the STYLE
column once a band has its card.

> **These files are yours and they stay in git.** Suno only turns them into audio; it is not where
> your work lives. Lyrics, prompts and style cards are all committed text, so a year from now you
> can change one line of one song and regenerate just that song. Nothing important is stored inside
> the tool.

## Step 6 · Generate in Suno

**Custom mode** — your lyrics, your prompt. Never let Suno write the lyrics.

The moment a take is a keeper, in this order:

1. **Download and rename it immediately** to `music/audio/<label>/<album>/03.mp3`. Suno's own
   filenames are unusable and after forty songs you won't know which is which.
2. Paste the exact prompt into that album's lyrics file.
3. Add a log line: `song id | attempts | model version | date | licence period`.

**Finish a band in as few sittings as possible** — Suno's current models are being retired, and a
band split across two model versions won't sound like one band.

## Step 7 · Measure and tag

`make music-analyse` (M-04) measures each song's duration, the seconds until the first sung word,
and its outro type. `make music-tag` (M-05) writes the licence period, generation date, model
version and AI marker into every file.

**Never estimate the intro ramp by eye.** Two seconds too long clips a vocal on air, on every play,
forever. The tool measures and flags the borderline ones; you re-listen only to those.

At the **start of every month you generate in**, save Suno's commercial-use terms as a dated PDF
into `music/licence-evidence/`. Rights attach at the moment of generation, so the evidence is per
month, not per project. It cannot be reconstructed later.

---

## When it's done

- [ ] All nine genres written, checked and screened.
- [ ] 500 songs have audio, a measured ramp, a duration and an outro type.
- [ ] Every audio file carries its own licence tags.
- [ ] **You have listened to fourteen songs back to back, as if it were the hour.**

That last one is the only quality gate in this project. Nothing automated grades the product.

---

## If something goes wrong

| It says | Do this |
|---|---|
| `make check` red, naming a genre and a number | The wiki does not match `plan.yaml`. The message says which label, which song, which id |
| `make check` red on the anchor years | `CONSTANTS.md` §1's table lost its `\| **YYYY** \|` row shape |
| `missing music/wiki/x.yaml` | That genre has not been written — its card in `MUSIC_TASKS.md` |
| `no style card yet` | That band's style card is missing — M-16 or M-20 |
| You do not know where you are | Ask "what's next in music". The answer is the card marked **NEXT** |

## The words

**Layer A** — the 500 songs that become audio. **Layer B** — music that exists in the world but the
station doesn't own; a presenter can mention it, the scheduler can never play it. **Layer C** —
musicians whose recordings are lost; history only, no albums.

**Band** — a singer or group with albums and a career.

**Session player** — a hired musician who plays on *other people's* records. No albums of their
own, no career, no voice. They exist only as credits, so a presenter can say *"that's Ivena Sorn on
pipes — she's on half the Forge catalogue too."*

**Style card** — six lines fixing how a band sounds. Written once per band, reused in every prompt.

**Anchor year** — one of eight years when a lot of records happened to come out, so the overnight
show can do "one label or one year". Every album in the wiki is dated to one of them.
