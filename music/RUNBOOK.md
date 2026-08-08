# RUNBOOK.md — the music, start to finish

> **Everything you need is on this page.** Every step says what to type, what to do with the
> result, and which file to save it in. Every file and folder already exists — **you never create
> anything by hand.**
>
> Do the next unticked step. That is the whole method.

---

## The commands, all of them

| Command | What it does |
|---|---|
| `make music-brief GENRE=<genre>` | Brief for writing one genre → **clipboard** |
| `make music-check GENRE=<genre>` | Brief for checking that genre → **clipboard** |
| `make music-albums` | Lists every album with its id (use `GENRE=` to filter) |
| `make music-style GENRE=<genre>` | Brief for that genre's band style cards → **clipboard** |
| `make music-songs ALBUM=<id>` | Brief for one album's lyrics + Suno prompts → **clipboard** |
| `make check` | Confirms the plan still adds up |

**Every one of them puts the result on your clipboard.** You paste it into a chat. That's it.

## The nine genres

`relay-pop` · `lane-rock` · `deck-talk` · `frontier-reels` · `old-system-sessions` ·
`pulse-dance` · `void-lounge` · `core-harmonies` · `void-ballads`

## Where things live

| File | What goes in it |
|---|---|
| `music/wiki/<genre>.yaml` | the writer's genre reply. **All nine files already exist, empty** |
| `music/production/styles.yaml` | the band style cards. **Already exists, empty** |
| `music/production/lyrics/<album>.yaml` | one file per album, lyrics + prompts. Save as you go |
| `music/briefs/` | the briefs the commands generate. Ignore it, it looks after itself |

---

# Part 1 — the wiki

**Nine genres × one round each. No Suno, no hardware, nothing to buy.** This is the bulk of the work
and the part the presenters actually use.

## Step 1 · Fix two loose ends
**One message to your writer.** Paste `music/COMMISSION.md` first, then:

```
Three fixes to the session players in CONSTANTS.md.

1. Replace "Deym Rusk". It reads as a filed-off Dean Rusk, a real and very
   well-known person. Same instrument, same character, new name.

2. Give each of the eight an active_from and active_to. They are one generation
   working roughly 2592-2626 (present = 2626). Vary the spans.

3. Add three or four ELDERS who worked before 2592, and one player whose
   instrument suits deck-talk — a beat maker or a hook singer. Same format,
   with dates.
```

**Save into:** `music/CONSTANTS.md`, section 2.

- [ ] done

## Step 2 · Check the new names
**Google each new name in quotes.** `"Ivena Sorn"` — like that.

**Finding nothing is a pass.** You are checking the name is *not already taken* by a real famous
person. Most searches return nothing, and that is the good result.

| What you find | Verdict |
|---|---|
| Nothing at all | ✅ keep — the normal result |
| A LinkedIn profile, a forum user, a private person | ✅ keep |
| Only the surname matches something real | ✅ keep |
| A real notable person with that **exact full name** | ❌ replace |
| A name that reads as a famous name with a letter changed | ❌ replace |

**Save into:** `music/CONSTANTS.md`, section 3.

- [ ] done

## Step 3 · Write a genre
**Two chats. Repeat nine times.**

```
make music-brief GENRE=relay-pop
```

1. Open a **new chat**. Paste. It writes.
2. **Save the reply into `music/wiki/relay-pop.yaml`**, replacing everything below the `section:`
   block. The file is already there with the numbers in its header.

```
make music-check GENRE=relay-pop
```

3. Open a **different chat**. Paste. It reports failures.
4. Send the failures back to the first chat, get a fix, re-save, re-check until it passes.

> **Why two chats:** a writer marking its own homework always says it's fine.

**Do `relay-pop` first** — it's the biggest genre, so a writer who can't do the job shows up on
round one. Then the other eight.

- [ ] relay-pop  · [ ] lane-rock · [ ] deck-talk · [ ] frontier-reels · [ ] old-system-sessions
- [ ] pulse-dance · [ ] void-lounge · [ ] core-harmonies · [ ] void-ballads

## Step 4 · Screen the names in each genre
Same as Step 2, on every band, label, album title and song title the writer invented. Do it **after
each genre**, not at the end of all nine. Record cleared names in `music/CONSTANTS.md` section 3 so
the next genre doesn't reuse them.

- [ ] done for every genre

---

# Part 2 — the songs

**Only after Part 1 is finished.** Now you need a Suno account.

## Step 5 · Style cards
**Once per genre.** A style card is what makes a band sound like the same band across three albums.

```
make music-style GENRE=relay-pop
```

Paste into a chat. **Save the reply into `music/production/styles.yaml`** — the file is already
there, with the format in its header.

- [ ] done for every genre

## Step 6 · Pick an album
```
make music-albums
```

```
ALBUM    L  BAND                 YEAR   SONGS  PLAY  STYLE  TITLE
al_001   A  Measure Kindly       2619   12     12    yes    Terms of Arrival *
al_012   B  Pell and Tern        2559   8      0     -      Rooms Between Voices
```

| Column | Means |
|---|---|
| **L** | the layer. **A** = recorded. **B** = written about, never recorded |
| **SONGS** | how many songs are on the record |
| **PLAY** | how many of them become audio. Always 0 for layer B |
| **STYLE** | does that band have a style card yet? `--` means do Step 5 first |
| **`*`** | a cornerstone album, long enough to carry a whole 56-minute programme |

**Only layer A can be recorded.** `make music-songs` refuses a layer-B id and tells you so — those
albums exist so a presenter can mention a record the station doesn't own, which is most of the
discography.

**The album id is the thing you need.** `al_001`.

## Step 7 · Lyrics and Suno prompts
```
make music-songs ALBUM=al_001
```

Paste into a chat. It already contains the album's story, the band's style card, and every song's
title, mood and one fact — so the lyrics will fit what the presenters already say about them.

**Save the reply into `music/production/lyrics/al_001.yaml`** — the command tells you this too.

> **These files are yours and they stay in git.** Suno only turns them into audio; it is not where
> your work lives. Lyrics, prompts and style cards are all committed text, so a year from now you
> can change one line of one song and regenerate just that song. Nothing important is stored inside
> the tool.

- [ ] repeat per album

## Step 8 · Generate in Suno
**Custom mode** — your lyrics, your prompt. Never let Suno write the lyrics.

The moment a take is a keeper, in this order:

1. **Download and rename it immediately** to `music/audio/<label>/<album>/03.mp3`. Suno's own
   filenames are unusable and after forty songs you won't know which is which.
2. Paste the exact prompt into that album's lyrics file.
3. Add a log line: `song id | attempts | model version | date | licence period`.

**Finish a band in as few sittings as possible** — Suno's current models are being retired, and a
band split across two model versions won't sound like one band.

## Step 9 · Measure by ear
Play each keeper and write down three numbers:

- **duration** — real length
- **intro ramp** — seconds until the **first sung word** (the presenter talks across this)
- **outro** — `cold`, `fade` or `sustain`

**Never estimate the intro ramp.** Two seconds too long clips a vocal on air, on every play, forever.

## Step 10 · Tag and file
- Write into each audio file's own tags: licence period, generation date, model version, and an
  AI-generated marker.
- At the **start of every month you generate in**, save Suno's commercial-use terms as a dated PDF
  into `music/licence-evidence/`. Rights attach at the moment of generation, so the evidence is per
  month, not per project.

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
| `unknown genre 'x'` | Use one of the nine slugs above |
| `no album 'al_xxx'` | Run `make music-albums` for the real ids |
| `missing music/wiki/x.yaml` | That genre hasn't been written — Step 3 |
| `MISSING — run make music-style` | Step 5 for that genre first |
| `make check` fails | The plan no longer adds up. It names what broke |

## The words

**Layer A** — the 500 songs that become audio. **Layer B** — music that exists in the world but the
station doesn't own; a presenter can mention it, the scheduler can never play it. **Layer C** —
musicians whose recordings are lost; history only, no albums.

**Band** — a singer or group with albums and a career. The writer invents these.

**Session player** — a hired musician who plays on *other people's* records. No albums of their
own, no career, no voice. They exist only as credits, so a presenter can say *"that's Ivena Sorn on
pipes — she's on half the Forge catalogue too."*

**Style card** — six lines fixing how a band sounds. Written once per band, reused in every prompt.

**Anchor year** — one of eight years when a lot of records happened to come out, so the overnight
show can do "one label or one year".
