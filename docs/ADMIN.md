# Settlement Radio — operating manual

Every line here works today. A target arrives in this file when it runs, never before
(`ARCHITECTURE.md` §32). `ARCHITECTURE.md` §17 is the design of the full surface; this is what
exists.

Run everything from the repository root.

---

## The commands that exist

### `make setup`

Installs `uv` and `gitleaks` through Homebrew if they are missing, builds the virtual environment
from `uv.lock`, and installs the git hooks (pre-commit and pre-push). Safe to re-run at any time —
it changes nothing that is already correct.

Run it after a fresh clone, and after any change to `pyproject.toml` or `uv.lock`.

### `make check`

Formatting, lint, types, the module-size rule and the unit tests. Model-free and fast. This is the
gate: it also runs automatically before every `git push`.

**It also counts the music wiki.** Every written genre in `music/wiki/` is checked against
`music/plan.yaml` and `music/CONSTANTS.md`, and the failure names the genre and both numbers: a
label with the wrong number of playable songs, a layer-A song with no fact, a layer-B song that has
one, a release year that is not one of the eight anchors, or an id used twice. A genre file that is
still an empty placeholder is skipped, not failed.

A genre `plan.yaml` marks `owed_to: M-46` is a genre a card has not finished growing yet: its counts
are not compared while that marker stands. The check reads `music/MUSIC_TASKS.md` to see whether the
card is still open, **and goes red if the card is marked DONE with the marker still there** — so the
counting cannot stay switched off by accident (D-069).

**And it checks `music/catalogue.yaml` against that wiki.** Every label, band, album and song has to
appear in both under the same name, every reference has to resolve, and a track either carries a
whole take or none of one. Red here almost always means one thing: the wiki changed and
`make music-catalogue` was not re-run. No audio is read, so this works on a fresh clone and in CI.

### `make doctor`

Says whether this machine can run the station: configuration loaded, the external volume mounted,
and each system tool present. Ends in `ready`, or names what is missing.

`make help` lists the targets.

---

### `make music-albums`

Lists every album in the wiki with its id, band, year, song counts and whether that band has a style
card yet. `GENRE=` limits it to one genre. This is how you see the catalogue without opening nine
YAML files.

The **L** column is the layer: `A` is recorded, `B` is written about and never recorded. **PLAY** is
how many of the album's songs become audio, and is always 0 for layer B. `*` marks a cornerstone
album — long enough to carry a 56-minute single-album programme.

**This command needs no `.env` and no external volume.** The music wiki is deliberately readable
before any hardware exists (`DECISIONS.md` D-044).

### `make music-screen`

Puts every invented name in a genre — every band, label, person, album title and song title, layer
B included — to Wikidata, and lists the ones that are **exactly** the name of a real notable person
or organisation. `GENRE=lane-rock` limits it to one file; without it, every file in `music/wiki/`
that is read — the genres **and the collections** (`DECISIONS.md` D-099). This is step 3 of
`music/RUNBOOK.md`, and it replaces searching several hundred names one at a time.

A genre is about 320 names, seven requests and under a minute; a dot appears for each request. The
normal result is `nothing matched`.

What it reports and what it does not:

| | |
|---|---|
| Exact full name, real person or organisation, ≥5 Wikidata sitelinks | **reported** |
| The same name below the notability floor — a forum user, a private person | not reported |
| Surname only, or a famous name with a letter changed | **not reported — still yours** (`DECISIONS.md` D-009) |
| A place, a song, a film, a species sharing the name | not reported: the screen is people and organisations |

**It is not a gate.** It always exits 0 and `make check` never runs it — it narrows the pile, and
the verdict on each name is yours. Record both the clearances and the rejections in
`music/CONSTANTS.md` §3, or the next genre proposes the same collision again.

If Wikidata cannot be reached it stops and says so rather than printing an empty report, because an
empty report reads as "every name is clear". Run it again when the connection is back.

### `make music-dispatch`

Files a pile of Suno takes into `music/audio/<label>/<album>/NN.mp3`. Point it at the export folder
and it works out which song each file is — **by reading the lyric inside the file, never by its
name.** `GENRE=lane-rock` limits which songs it will file against; `RAW=some/folder` points it
somewhere other than `music/audio/RAW`. Sub-folders are searched, so an export can stay in whatever
folder the browser made for it.

**Why it does not trust filenames.** M-18 filed the pilot by sorting the export by time and walking
the track list. M-30 checked that against the lyric Suno writes into every file's own tags and found
a song that had never been generated: at one sitting the style box moved on and the lyric box did
not, so track 9's slot held a second take of track 8 — right size, right place, plausible time
(D-091). Reading the words is the only check that catches that.

**It refuses the whole pile or files all of it.** Every take has to claim exactly one song, no song
may be claimed twice, no take may claim a song that already has audio, and every song waiting for
audio has to be claimed by something. A pile that fails any of those prints why and moves nothing,
which is the same failure shape D-091 found: one song claimed twice and another claimed by nobody.

**"claimed by more than one take" has two causes and only you can tell them apart.** Either the lyric
box did not change between two prompts, which is D-091's real failure and means a song was never
generated — or you downloaded **both** takes Suno returns from one prompt, and the pair naturally
matches one lyric twice. The command cannot distinguish them and does not guess. Look at the two
`created=` times in the files' comment tags: seconds apart is a pair, and a real miss is minutes or
hours apart with one song left unclaimed at the bottom of the report.

**If it is a pair, choose one by ear and keep the other.** Move both out of the pile, run the
dispatch again to file everything else, then put the keeper back on its own and run it once more —
the matcher compares against every written lyric in the genre, so a pile of one still has to prove
itself. Do not delete the reject: put it somewhere named, like `music/audio/RAW/M-34-REJECTED/`, and
add a row for it to the manifest with `"song": null` and a `verified:` line saying which take won and
why. M-34 did this for tracks 1 and 2 of `al_104` and it is the only record of the choice (D-105).

**Every take is matched against every written lyric in the genre and filed only against the ones
still waiting**, which is not the same thing. Topping up a single missing song against a pool of one
would make "which song is this?" a question with no wrong answer, and the take would be filed as that
song whatever it actually contained. Keeping the finished songs in the pool is what lets a take that
belongs to something already on disk say so.

**Nothing is overwritten and nothing is deleted.** A take moves only to a path that does not exist
yet, and both ends of every move go into `music/audio/RAW/dispatch-manifest.json` with the Suno id,
the vendor's own timestamp, and how much of the take is the written lyric.

A `MATCH` under 100% is not a fault — Suno rewords, drops a section and doubles another, and a take
can be a loose copy of its lyric and still unmistakably be that lyric and no other. Those rows print
in yellow because they are worth your ear, not because anything went wrong.

**It does not write the `take:` blocks.** Those go into `music/production/lyrics/` by hand from the
manifest, because a machine writing YAML back into those files would flatten every lyric and drop
every comment in them. Then `make music-tag`, then `make music-catalogue`.

### `make music-analyse`

Measures every audio file under `music/audio/` and prints three numbers per take: how long it runs,
how many seconds of instrumental run-up there are before the first sung word, and how it ends —
`cold`, `fade` or `sustain`. `ALBUM=al_001` limits it to one album. About a second a song, so the
whole catalogue is roughly eight minutes.

This is what the mixer needs and what nobody can hand-time 500 times: the run-up is how long a
presenter may keep talking over the top of a record, and `cold` means the ending must not be talked
over at all.

**A ramp of `0.0` means there is no run-up you could talk over** — not that the vocal starts at
sample zero. Nothing resolves an intro shorter than about two seconds, and two seconds is not a
link. A run-up is only ever claimed where the opening of the record is measurably quieter in vocal
evidence than the body of it.

**Rows marked `check` in yellow are the ones to listen to, and the note says why.** Either the
opening is ambiguous, or the ending sits within a fifth of a second of the line between a cold stop
and a short ring. `ARCHITECTURE.md` §9 is the reason this exists: onset detection gets the
ballpark, and the last half-second is a listening judgement. It is not a gate, it always exits 0,
and nothing is written to a file — the measurements are read on screen, and
`make music-catalogue` takes them again for the file the station reads.

If a file cannot be decoded the pass keeps going, prints `UNREADABLE` with the file named, and
counts it in the summary. A song that dropped out silently would become a track with no ramp and a
link that clips the vocal.

### `make music-tag`

Writes four things into every audio file's own tags: the licence period it was generated under, the
generation date, the model version, and a marker saying it is machine-generated. `ALBUM=al_001`
limits it to one album. The whole pilot takes about eight seconds.

**Why it matters more than it sounds.** `music/audio/` is not in git and the wiki is. One day the
audio and the wiki will be apart — a backup, a move, a new machine — and a file that cannot say what
licence it was made under is a file nobody may broadcast. `music/COMMISSION.md` §9 asks for this and
it is the half of the licence evidence that travels with the music.

Run it after every Suno sitting. It reads the `generation:` and `take:` blocks in
`music/production/lyrics/`, so **a song only gets tagged once its take is recorded there.**

What it prints at the end is the check: the counts, and then one file's four tags in full, so you
can see what any of them now says. To read another file yourself:

```bash
ffprobe -v error -show_entries format_tags -of default music/audio/label_1/al_001/01.mp3
```

**Nothing already in the file is touched and the audio is never re-encoded.** Suno's own comment,
with the generation id and timestamp, stays. Each file is copied with the audio passed through
untouched, checked against the original, and only then moved over it — so an interrupted run leaves
whole files behind, never a half-written one.

**Running it twice is safe and nearly instant** — a file already carrying the right four values is
not rewritten at all. That is what lets it run after every genre rather than once at the end.

Unlike the other music commands **this one is a gate**: it exits red if any file failed, or if there
is audio under `music/audio/` that no lyrics file records a take for. An untagged file is the one
you would not find out about until it mattered.

### `make music-catalogue`

Builds `music/catalogue.yaml` — **the one file the station's database ingests**, and the only thing
that makes any of the wiki reach the air. Everything else in `music/` is written for a person; this
is written for the machine, in the shape `ARCHITECTURE.md` §17a fixes: labels, artists, albums and
tracks, with each track's file, mood, measured run-up, ending, rotation category and licence.

It joins three things, and re-measures the audio every run, so it takes about a second a song — the
pilot's 45 in under a minute, the full 500 in roughly eight. Dots show it working.

- the **wiki** — who exists, what it is called, and the one fact per song a presenter can say
- the **lyrics files** — which take belongs to which song and what licence it was made under
- the **audio** — duration, run-up and ending, measured, never remembered from a previous run

Run it after anything changes in `music/wiki/`, after a Suno sitting, and after `make music-tag`.
**Then commit the file**, because `make check` compares it against the wiki every time and goes red
when the two have drifted apart. That red is the only thing standing between you and a station
confidently describing last week's catalogue.

**`playable: true` means the audio is on disk and measured.** Every other row is a title with no
file — either a record the world knows and the station has never held (layer B), or a song whose
Suno card has not run yet. Today that reads *45 playable, 1313 titles*; when the music job is
finished it reads 500 and 858. A track that could not be measured is left unplayable and named in
red rather than given a guessed run-up.

**Nothing in the file is hand-edited.** The next run overwrites it whole.

**There are no other music commands.** The wiki, the style cards and the lyrics are written by an
agent working one card of `music/MUSIC_TASKS.md` — you open a session and say the card number
(D-055). Nothing is copied to a clipboard and nothing is pasted anywhere.

### `make imaging-analyse`

Measures every piece of station imaging and prints four numbers per piece: how long it runs, how
much run-up there is before the first sound a presenter cannot talk over, how bright it is on a
0-to-1 scale, and — where the piece repeats its own ending — the point a loop should return to.
`PIECE=night_watch` limits it to pieces whose name contains that. The 56 files take about half a
minute, most of which is the eight-minute fallback bed.

It reads `imaging/` if that folder holds audio and `music/jingles/approved/` otherwise, and prints
which one it read. Today it is the second: the pile has not moved to the external volume yet.

**`ENERGY` is a scale, not a verdict.** 0 is a piece whose sound sits around 250 Hz and 1 is one
sitting around 5 kHz, log-spaced between them. `music/jingles/README.md` §2's three tiers — night,
day, bright — are a brightness ladder by construction, so this is the axis that separates them, and
it is the number `grid.yaml`'s daypart ranges are compared against (`ARCHITECTURE.md` §17a). It is
not loudness: the mixer normalises every piece anyway.

**`RAMP` of `0.0` means the piece is at full level from the top** — there is nothing to talk over,
not that it starts at sample zero. Where a piece sings, the run-up is measured to the first sung
word by the same measure `make music-analyse` uses, and the row says `sung entry`. Where it does
not — which today is all 56 — it is measured to where the piece reaches and holds its own body
level, which is what a swell or a riser into a motif actually is.

**`LOOP` of `—` means the piece does not repeat its own ending.** That is a fact about the audio and
not a failed measurement: most imaging is a one-shot piece with a beginning and an end, and only a
bed needs a seam. Today exactly one file has one — `fallback_bed`, which returns to 448.6 s. **The
other three beds do not**, so looping any of them will step audibly at the join until a seam is
edited in or the piece is regenerated.

**Rows in yellow marked `check` are the ones to listen to, and the note says why.** Either the
opening is only a little under the body of the piece, so where the run-up ends is a judgement, or
the pattern repeats at the point named but the join steps further than the piece steps of its own
accord. `ARCHITECTURE.md` §9 is the reason: the last half-second of a ramp and the treatment of a
seam are listening judgements, and a tool printing a hundred confident numbers, some of them wrong,
would be worse than no tool.

It is not a gate, it always exits 0, and nothing is written to a file — the numbers are read on
screen, and `imaging/catalogue.yaml` takes them again when that file is built (I-06). A file that
cannot be decoded is named as `UNREADABLE`, counted in the summary, and does not stop the pass.

### `make imaging-tag`

Writes four things into every piece of station imaging: the licence period it was generated under,
the generation date, the model version, and a marker saying it is machine-generated. `PIECE=sweeper`
limits it to pieces whose name contains that. The 56 files take about eleven seconds the first time
and under four after that.

**Why it matters more than it sounds.** The imaging audio is not in git and its whole manifest is a
`README.md` written for a person. Separate one file from that folder — a backup, a new machine, a
hand-off — and before this command it said only `made with suno`. `ARCHITECTURE.md` §9 makes
provenance mandatory in the imaging file itself for that reason, and §18 makes the AI marker a
compliance control rather than a nicety.

**Where the four values come from.** Two places, and neither is typed in here (D-095):

- **`music/licence-evidence/2026-07-suno-licence-note.md`** — the licence period and the model
  version, read out of that note's own table. Correct the note and the next run corrects the files.
- **Each file's own Suno comment** — the generation date, out of the `created=` timestamp Suno
  writes into every export. A file that has lost that comment is **failed by name, never given a
  guessed date**, because a wrong generation date inside an audio file reads as fact forever.

It also refuses, by name, any file whose Suno date falls outside the month the note covers. That is
the mistake nobody would otherwise notice: a later pile quietly tagged with an earlier pile's terms.

What it prints at the end is the check: the counts, then one file's four tags in full **plus Suno's
own comment**, so you can see both that the licence is in and that the generation id is still there.
To read another file yourself:

```bash
ffprobe -v error -show_entries format_tags -of default music/jingles/approved/time_sting.mp3
```

**Nothing already in the file is touched and the audio is never re-encoded.** Suno's comment, with
the generation id every one of these can be re-exported by, stays. Each file is copied with the
audio passed through untouched, the copy checked against the original, and only then moved over it —
so an interrupted run leaves whole files behind, never a half-written one.

**Running it twice is safe and nearly instant** — a file already carrying the right four values is
not rewritten at all.

Like `make music-tag` and unlike `make imaging-analyse`, **this one is a gate**: it exits red if any
file failed. A piece with no licence in it is a piece nobody may broadcast, and the cheap moment to
notice is before `imaging/catalogue.yaml` is built on top of it.

## What GitHub checks, and when

Three workflows, in `.github/workflows/`. None of them touches the database, the Transmitter or a
model, and none of them can reach a secret.

| Workflow | Runs when | Does |
|---|---|---|
| `pr` | every pull request, and every push to `main` | the secret scan, and `make check` |
| `nightly` | 05:30 UTC daily, or on demand from the Actions tab | the same two, without the build cache and over the whole history |
| `web` | only when `web/` or `panel/` changes | lints and typechecks them; neither exists yet, so it never runs |

`pr` finishes in about two minutes and is the one you wait for. `nightly` is read with the morning
digest, not watched.

To run the nightly by hand: the repository's **Actions** tab → **nightly** → **Run workflow**.

---

## Recovery

### A command stops immediately saying configuration is incomplete

```
Configuration is incomplete. These lines are missing or wrong:

  DATABASE_URL               required, and set in neither .env nor the environment
```

`.env` is missing a line, or has one with an empty value. `.env.example` is the full list. Add the
named line, then run `make doctor`. This is working as intended — the alternative is discovering it
at 02:00.

If `.env` does not exist at all: `cp .env.example .env && chmod 600 .env`, then fill it in. It is
never committed, and it is the only place secrets live on the Studio.

### `make doctor` reports the external volume missing

`MEDIA_ROOT` names a directory that is not there — usually the external SSD has not mounted. Plug
it in and check the path. Postgres must not start before that volume mounts (§4).

### A commit is refused by gitleaks

The staged diff contains something shaped like a key. Look at what it names. Remove the secret,
put it in `.env`, and add the line to `.env.example` with an empty value in the same commit.

Do not pass `--no-verify`. The repository is public: a committed secret is public the moment it is
pushed, and deleting it later does not un-publish it.

### A pull request check is red

Open the failing check on GitHub and read the last lines of the step that failed.

- **secret scan** — a key is in the branch's history. It is not enough to delete it in a new commit:
  the scan reads every commit, and so does anyone who clones the repository. Treat the key as
  published, rotate it, and rewrite the branch so the commit that carried it is gone.
- **make check** — run `make check` on your Mac and you will see the same failure locally. It should
  not normally get this far: the same gate runs before every `git push`.
- **uv lock --check** — `pyproject.toml` changed without the lockfile being rebuilt. Run
  `uv lock`, commit `uv.lock`, and push again.

A pull request opened from somebody else's copy of the repository runs the same checks with no
access to any secret. That is deliberate and cannot be granted per-pull-request.

### A commit is refused for a large file

Audio does not go in git — it lives on the external volume (§4). The exception is `voices/`
reference clips, which are committed and are small. If a legitimate file is genuinely over the
limit, that is a decision for `DECISIONS.md`, not a flag on one commit.
