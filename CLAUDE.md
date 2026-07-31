# CLAUDE.md

Settlement Radio — a 24/7 AI radio station. One operator, one Mac mini, nightly batch generation.

**This page is the whole contract. `docs/ARCHITECTURE.md` is the reference — consult it by section,
never read it whole.** If a rule here and the architecture disagree, the architecture is right —
record the disagreement under `## Observations` and carry on. Fixing it is the operator's call and
its own task (§33); it does not get folded into the one in progress.

## Before you write anything

1. Read `docs/TASKS.md`. **WIP is 1** — work the one task at the top, finish it, start nothing
   else. If none is marked in progress, ask which. An empty `TASKS.md` means ask, never invent.
2. Read the architecture sections the task's `Reads:` line names, **plus Part II (§21–32), which
   binds every task.** An agent that has read only Part I is not ready to write code.
3. On a grid or showrunner task, also read `docs/PROGRAMMING.md` — the editorial reference and the
   input to `grid.yaml`. On any other task, never.
4. If the task has no observable check, it is not a task. Ask.

## Never

- **Never add a task to `TASKS.md`.** End the session with an `## Observations` list instead. The
  operator decides what becomes work.
- **Never create a document.** Eight exist — the six in the §32 cap, plus `PRODUCT.md` and
  `PROGRAMMING.md` outside it — and that is the cap. Two files are not documents and may be
  created on a task that names them: `voices/PROVENANCE.md` and `README.md`.
- **Never author content** — canon, cast cards, speech profiles, voice reference clips, pool
  pieces, or any audio asset. That is the operator's, always. Structured config with validations
  behind it — `grid.yaml`, `banned-entities.yaml`, imaging placement, `music/catalogue.yaml` — is
  fair game on a task that names it (§33).
- **Never regenerate something because it could be better.** Ship it; note it in Observations.
- **Never take a destructive action without asking.** `make reset-world` and anything irreversible.

## Code rules — all mechanically checkable

| Rule | Where |
|---|---|
| All model calls go through `generate_structured()` | `providers/llm.py` |
| No prose parsing of model output. JSON + Pydantic, one repair, then fail | — |
| Vendor SDKs imported only inside | `providers/` |
| `os.getenv` only in | `config.py` |
| `datetime.now()` only in | `clock.py` |
| Raw SQL only in a | `store.py` |
| No `print()` — structlog only | `log.py` |
| Modules ≤400 lines, functions ≤50 (`store.py` exempt from lines, not cohesion) | — |
| Timestamps UTC and tz-aware in the DB; in-world time is derived | `clock.py` |
| Dataclasses/Pydantic across module boundaries, never bare dicts | — |
| Every external call: explicit timeout, bounded retry, defined fallback | §25 |
| Never silently produce nothing — fall back or raise | §25 |

## Two seams (§3)

- **LLM** — per-job config in `models.yaml`; nothing outside `providers/llm.py` knows a model name.
- **TTS** — callers branch on declared `Capabilities`, never on engine names. Timing is the
  mixer's job, never the engine's.

## Definition of done

Code · the one kind of test that applies (§29) · `ADMIN.md` if a command changed · a `DECISIONS.md`
line if a decision was made · `make check` green.

**Nothing else.** No summary document, no new pack, no gate.

## Defaults

- **The default for any judgment call is no change.**
- **A null result is a completed task.** "Measured, no improvement, reverted" is success.
- If a detail is unspecified, choose the simplest option that respects the two seams and say so.
- Use `make` targets. If an operation has no target, add one — do not document a raw command.
- **Never document a command in `ADMIN.md` before it exists.** (§17's list is design, not `ADMIN.md`.)

## End every session with

1. What changed.
2. Exactly how the operator verifies it.
3. `## Observations` — anything you noticed. Findings, not tasks.

---

*Quality is judged by ear, by the operator, on `make sample`. No test, gate or harness grades the
product. Do not build one.*
