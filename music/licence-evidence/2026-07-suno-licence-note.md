# Suno licence — what applies to the 132 assets generated 2026-07

> **There is no separate PDF for this month, and none is needed.** The evidence is the file already
> beside this one — `2026-08-suno-terms.pdf`, captured 2026-08-15, stating a revision date of
> **March 26, 2026**. That revision predates every generation date below and was still the revision
> in force when this note was written, so it is the governing text for these assets as well as for
> the 45 songs. `COMMISSION.md` §9 files evidence **per generation month** because terms change
> between months; here they did not, and this note is the record of that having been checked.

**What this covers.** Two piles, both generated in July 2026 on the same account and under the same
terms, and this is the only evidence either of them has.

1. **The 56 station imaging assets** in `music/jingles/` — idents, stings, beds, programme opens and
   the fallback bed.
2. **The 76 songs of the July collection** in `music/audio/unsigned/`, filed by M-54 on 2026-09-02
   and carrying `licence_period: suno-pro-2026-07` in their own tags. They are the played half of a
   135-take pile made before `COMMISSION.md` was written; `music/wiki/independents.yaml` is what
   they are in the world and `music/production/lyrics/al_170.yaml` … `al_211.yaml` is where each
   one's date and generation id are written down.

Not covered here: the catalogue's other songs, which are `2026-08-` and `2026-09-suno-licence-note.md`.

| | |
|---|---|
| Evidence file | `2026-08-suno-terms.pdf` — **shared with 2026-08, not duplicated** |
| Source | <https://suno.com/terms> · <https://suno.com/terms-of-service> — confirmed the same document (operator, 2026-08-22) |
| Date of last revision, as stated on the page | **March 26, 2026** |
| Still the revision in force | **yes**, verified 2026-08-22 |
| Covers generation month | 2026-07 |
| Assets generated under it | **132** — 56 imaging and 76 songs, below |
| Imaging, by date | **56** — 25 on 2026-07-04, 22 on 2026-07-08, 9 on 2026-07-20 |
| Songs, by date | **76** — 2 on 07-03, 1 on 07-04, 22 on 07-05, 1 on 07-06, 3 on 07-08, 8 on 07-11, 31 on 07-21, 1 on 07-24, 7 on 07-25 |
| Subscription tier at generation | **Pro** — the account has been on Pro from day 0, continuously (operator, 2026-08-22) |
| Remix features | **never enabled on this account** (operator, 2026-08-22) |
| Model version used | **v5.5** — operator, 2026-08-23. The same model the 45 songs record |
| `licence_period` to record per asset | `suno-pro-2026-07` |
| Complete? | **Yes** |

---

## Why the tier answer settles it

The clause is the same one quoted at length in `2026-08-suno-licence-note.md`: Suno assigns Output to
the account holder **if that account is on the Pro or Premier paid tier**, and the assignment is
**scoped to the subscription term** — rights attach at the moment of generation, to output made while
the subscription was active. The account was on Pro on every date in the table above — 2026-07-03
through 2026-07-25 — as it has been since day 0, so the assignment applies to all 132 unqualified.

**Remix does not bite.** A remix-enabled output is restricted to non-commercial use *"regardless of
whether you are a free Service tier user or a subscriber to a paid Service tier"* — the one
restriction that survives the paid-tier assignment. The feature has never been switched on for this
account, so the clause never attaches. It has to stay off.

**The two URLs are one document.** `suno.com/terms` and `suno.com/terms-of-service` resolve to the
same terms, confirmed by the operator 2026-08-22. There is no second set of conditions to capture.

## Model version

`COMMISSION.md` §9 wants the model version recorded per generated item, because models are on a
published deprecation path and work generated across a model change will not match itself.

**All 132 were generated on v5.5** — the operator's own record, given 2026-08-23 for the 56 imaging
assets and **2026-09-01 for the 76 songs**, and the same model version the 45 songs carry. The files
themselves do not say so: their Suno tags hold only `made with suno`, a creation timestamp and a
generation id, with no model field. That is a limit of what the vendor writes into an export, not a
gap in the provenance, and this line is the record.

**The 76 songs are tagged already.** `make music-tag` writes the four values into every file under
`music/audio/`, and the July collection went through it on 2026-09-02 like every other take. The
imaging half is still waiting on `make imaging-tag` below.

`ARCHITECTURE.md` §9 names `make imaging-tag` as the command that writes the licence period,
generation date, model version and AI marker into the **imaging** files (D-093). It does not exist yet;
`IMAGING_TASKS.md` I-03 builds it and this is the value it writes.

---

*Read from the full terms by a non-lawyer, and to be reviewed properly before launch (COMMISSION §9,
and Phase G's legal review). `2026-08-suno-terms.pdf` beside this file is the record; this is only
the reading, and the facts about the account are the operator's, recorded on the date given.*
