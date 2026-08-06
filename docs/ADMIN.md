# Settlement Radio — operating manual

Every line here works today. A target arrives in this file when it runs, never before
(`ARCHITECTURE.md` §32). `ARCHITECTURE.md` §17 is the design of the full surface; this is what
exists.

Run everything from the repository root.

---

## The three commands that exist

### `make setup`

Installs `uv` and `gitleaks` through Homebrew if they are missing, builds the virtual environment
from `uv.lock`, and installs the git hooks (pre-commit and pre-push). Safe to re-run at any time —
it changes nothing that is already correct.

Run it after a fresh clone, and after any change to `pyproject.toml` or `uv.lock`.

### `make check`

Formatting, lint, types, the module-size rule and the unit tests. Model-free and fast. This is the
gate: it also runs automatically before every `git push`.

### `make doctor`

Says whether this machine can run the station: configuration loaded, the external volume mounted,
and each system tool present. Ends in `ready`, or names what is missing.

`make help` lists the targets.

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

### A commit is refused for a large file

Audio does not go in git — it lives on the external volume (§4). The exception is `voices/`
reference clips, which are committed and are small. If a legitimate file is genuinely over the
limit, that is a decision for `DECISIONS.md`, not a flag on one commit.
