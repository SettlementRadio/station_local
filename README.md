# Settlement Radio

A 24/7 radio station for a fictional world, written and voiced by models, generated in a nightly
batch on one Mac mini and streamed from one small Linux box. One operator. No live inference.

- `docs/PRODUCT.md` — what it is for
- `docs/ARCHITECTURE.md` — how it works, and why
- `docs/ADMIN.md` — how to run it
- `docs/TASKS.md` — what is being built right now

The code is public and readable. Nothing here is licensed for reuse — see `LICENSE`.

## Install from scratch

macOS on Apple Silicon, with [Homebrew](https://brew.sh) already installed.

```bash
git clone <this repo> settlement-radio
cd settlement-radio
make setup
```

`make setup` installs `uv` and `gitleaks` if they are missing, creates the virtual environment from
`uv.lock` (exactly the pinned versions, never a fresh resolve), and installs the git hooks.

Then create your configuration:

```bash
cp .env.example .env
chmod 600 .env
$EDITOR .env            # DATABASE_URL and MEDIA_ROOT are required
make doctor             # says what is missing, or "ready"
```

`.env` is never committed. Every command refuses to start while a required line is missing, and
names the line — that failure belongs at startup, not at 02:00 in the middle of a render.

## System tools

Installed with Homebrew. `make doctor` reports which are present.

| Tool | Version | Where it runs | Required |
|---|---|---|---|
| Python | 3.12 (`.python-version`; `uv` fetches it) | Studio | yes |
| uv | ≥ 0.12 | Studio | yes |
| gitleaks | ≥ 8.30 | Studio (hooks) + CI | yes |
| ffmpeg | 8.x | Studio | yes — mix, loudness, `ffprobe` |
| postgresql@16 | 16.x | Studio | yes — the world database |
| liquidsoap | 2.4.x | Transmitter | no, locally |
| icecast | 2.4.x | Transmitter | no, locally |

Liquidsoap and Icecast run on the Transmitter (`ARCHITECTURE.md` §4), so a Studio without them is
fine; `make doctor` says "absent" rather than failing.

## Working in the repo

```bash
make help     # the targets that exist today
make check    # ruff + mypy + module sizes + unit tests — the gate that must be green
make doctor   # configuration and system tools on this machine
```

`ARCHITECTURE.md` §17 lists the full target surface. A target appears in `make help` and in
`ADMIN.md` when it exists, and not before.

The git hooks run on every commit — formatting, lint, types on changed files, a large-file guard
and a `gitleaks` scan of the staged diff — and `make check` on every push. The repository is
public, so a committed secret is a public secret instantly; the scan is not optional and
`--no-verify` is not a workaround.
