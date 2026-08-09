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

**There are no other music commands.** The wiki, the style cards and the lyrics are written by an
agent working one card of `music/MUSIC_TASKS.md` — you open a session and say the card number
(D-055). Nothing is copied to a clipboard and nothing is pasted anywhere.

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
