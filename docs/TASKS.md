# Settlement Radio — Tasks

Current work only, maximum 10 items (ARCHITECTURE §33). WIP is 1 for agent tasks; `[operator]`
items sit alongside them and do not consume the slot.

**Phase B · The Transmitter**, running beside the part of **Phase A** that needs no hardware
(`docs/PHASES.md`: A and B are independent, and B is the phase to run while hardware is in transit).
A's five hardware-bound cards — T-005, T-006, T-008, T-009 — are out until the machine arrives and
return with those numbers.

**Numbers are identities, not order.** What runs next is the card marked IN PROGRESS; what runs
after it is the next card in this file whose `Depends on:` line is satisfied.

---

## Agent track — one at a time, top to bottom

### T-004 · The three CI workflows — **IN PROGRESS**
Goal: Every push is checked by GitHub before it reaches you, and a leaked key cannot get in — the
repo is already public.
Reads: ARCHITECTURE §29, §30, §27
Files: `.github/workflows/pr.yml`, `nightly.yml`, `web.yml`
Check: Open a pull request: the checks run and finish under three minutes. A pull request opened
from someone else's fork gets no access to any secret. A deliberately committed fake key turns the
build red. Every action used is pinned to an exact version.
Note: `nightly.yml` runs only the suites that exist today; it gains the smoke and conformance jobs
in C and D as those pipelines get built.
Depends on: T-003

### T-011 · Liquidsoap, Icecast and the six-level failure chain
Goal: A stream that never goes silent, whatever is missing behind it. This is the milestone the
previous attempt never reached.
Reads: ARCHITECTURE §15, §4, §23 · PHASES B
Files: `config/liquidsoap/`, `config/icecast/`, `Makefile`, `docs/ADMIN.md`
Check: A URL plays audio. Forcing each level in turn works: take away the built hour and it falls to
today's buffer, take that away and it falls to the archive pool, then to music, then to a bed and
ident loop that never goes quiet. Icecast is set to a hard limit of 300 listeners rather than
discovering the limit. `make deploy` pushes the configuration from your Mac.
Depends on: T-003, T-010

### T-012 · The pinned junction slot and the disclosure sting
Goal: The hour always starts on the hour, and the station says what it is every hour — including in
the states you are least likely to be listening to.
Reads: ARCHITECTURE §15, §18, §13 · PHASES B
Files: `config/liquidsoap/`, `docs/ADMIN.md`
Check: At `:00` the junction plays and interrupts whatever was on. It does this at every one of the
six levels, including when playout has fallen all the way through to the bed loop, and the stream's
track metadata carries an AI marker at every level too. Listen at `:00` on three consecutive hours
with the source machine switched off.
Note: this is the compliance-critical half of the transmitter. §18 requires the sting be
hard-scheduled independently of content precisely so that it still fires at 04:00 when playout has
fallen through to music.
Depends on: T-011

### T-013 · The transmitter's security posture
Goal: The one machine exposed to the internet is exposed only where it has to be.
Reads: ARCHITECTURE §27, §4, §23
Files: `config/`, `docs/ADMIN.md`
Check: From the open internet, only ports 80 and 443 answer and everything else is refused —
including SSH, which works only over Tailscale. There is no password login and no root login, and
fail2ban is running. Icecast's admin page cannot be reached from outside the box, its default
passwords are gone, and its source password is read from `/etc/settlement/env`, which is owned by
root and readable only by root. Exactly two secrets live on the box.
Note: §4's inbound/outbound line is where §27's firewall rules are derived from — keep the two
agreeing. The stream stays unlisted and access-restricted until Phase G's legal review closes.
Depends on: T-011

### T-014 · The week unattended — M0
Goal: **M0.** Prove the stream survives a week with nobody looking at it. Kill the source and it
keeps playing.
Reads: PHASES B · ARCHITECTURE §15, §20 · PRODUCT §8
Files: — (a week of not touching it)
Check: Leave it running for seven days without intervening. At the end it is still playing, it
started every hour on `:00`, and the disclosure fired every one of those hours. Switch the source
machine off mid-week and it carries on.
Depends on: T-012, T-013

---

## Operator track — yours, any time, in any order

These do not consume the WIP slot. T-001 and T-010 unblock agent cards; the other two do not.

### T-001 · [operator] Order the Studio, and open the three accounts
Goal: The machine is ordered now so it arrives while Phase B is being built, and the accounts the
project needs are open.
Reads: PHASES A · ARCHITECTURE §4, §22
Files: — (bought and clicked, not written)
Check: A Mac mini M4 16GB and a 2TB Thunderbolt SSD are ordered and you know the delivery date. You
can sign in to Hugging Face and to GitHub, and Renovate is installed on the repo. The card closes
when the machine is on the desk and `/Volumes/station` mounts with 2TB free.
Note: weeks of lead time, and it is the only thing in the project waiting on a delivery date. Four
Phase A cards cannot be redrafted until it lands. **Do this first.**

### T-010 · [operator] The server, private access, and something to play
Goal: Phase B has a machine to broadcast from, a private way in, and audio to put on air.
Reads: PHASES B · ARCHITECTURE §4, §27
Files: `/srv/audio/` on the transmitter (the audio files themselves)
Check: Three things. A Hetzner CX32 is running Linux and you are paying about €11 a month for it.
Tailscale is installed on it and on your Mac, and you can reach the box by its Tailscale name. And a
handful of audio files exist to broadcast — any audio will do — plus one short spoken sting that
says the station is fictional and machine-made.
Note: the sting is a placeholder for the real one, which is C6 imaging in Phase F. It still has to
say the right thing, because from T-012 onward it is what carries the station's disclosure.
**T-011 cannot start until this is done.**

### T-002 · [operator] The two hand-written pieces phase A measures with
Goal: The two Phase A measurements have something real to measure when the machine arrives. Both are
yours to write; nothing else can produce them, and they are the long pole in A.
Reads: ARCHITECTURE §36.1, §36.2 · PROGRAMMING §5
Files: `tests/fixtures/measure/` (the render mix), `tests/fixtures/coldread/` (the brief)
Check: Two things exist. First, a set of scripts totalling 60 minutes of speech — realistic 4-minute
two-handers with overlaps, nonverbal beats and idents, not one long monologue. Second, one
hand-written context for a 20-minute two-hander: a page of world detail, who the two speakers are,
and what the programme is about. No retrieval, no canon pipeline, no grid.
Note: `PHASES.md` says Phase A needs no content. It does — neither piece has a C-number in the
content track, and the phase document needs the correction.

### T-015 · [operator] The music pilot — one flagship label
Goal: Find out whether the catalogue's approach works while it still costs one label's work to redo,
rather than after 540 tracks are committed to it.
Reads: `music/COMMISSION.md` §12 (the loop), §1, §4, §5
Files: `music/batches/01-<label>/{catalogue.yaml,production.md,audio/}`
Check: One flagship label is complete — roughly seventy tracks with lyrics, credits, measured intro
ramps and a one-fact line each — and you have listened to fourteen of them back to back as if it
were the hour. That listen decides everything about the remaining 470.
Note: runs in parallel with everything; it needs no code and no hardware. C5 is formally due in
Phase F, and this card is the pilot only, not the catalogue.
