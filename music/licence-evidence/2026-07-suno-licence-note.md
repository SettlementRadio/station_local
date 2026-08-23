# Suno licence — what applies to the 56 imaging assets generated 2026-07

> **There is no separate PDF for this month, and none is needed.** The evidence is the file already
> beside this one — `2026-08-suno-terms.pdf`, captured 2026-08-15, stating a revision date of
> **March 26, 2026**. That revision predates every generation date below and was still the revision
> in force when this note was written, so it is the governing text for these assets as well as for
> the 45 songs. `COMMISSION.md` §9 files evidence **per generation month** because terms change
> between months; here they did not, and this note is the record of that having been checked.

**What this covers.** The 56 station imaging assets in `music/jingles/` — idents, stings, beds,
programme opens and the fallback bed. Not music: the catalogue's 45 songs are covered by
`2026-08-suno-licence-note.md`.

| | |
|---|---|
| Evidence file | `2026-08-suno-terms.pdf` — **shared with 2026-08, not duplicated** |
| Source | <https://suno.com/terms> · <https://suno.com/terms-of-service> — confirmed the same document (operator, 2026-08-22) |
| Date of last revision, as stated on the page | **March 26, 2026** |
| Still the revision in force | **yes**, verified 2026-08-22 |
| Covers generation month | 2026-07 |
| Assets generated under it | **56** — 25 on 2026-07-04, 22 on 2026-07-08, 9 on 2026-07-20 |
| Subscription tier at generation | **Pro** — the account has been on Pro from day 0, continuously (operator, 2026-08-22) |
| Remix features | **never enabled on this account** (operator, 2026-08-22) |
| Model version used | **not recorded** — see below |
| `licence_period` to record per asset | `suno-pro-2026-07` |
| Complete? | **Yes**, subject to the model-version gap below |

---

## Why the tier answer settles it

The clause is the same one quoted at length in `2026-08-suno-licence-note.md`: Suno assigns Output to
the account holder **if that account is on the Pro or Premier paid tier**, and the assignment is
**scoped to the subscription term** — rights attach at the moment of generation, to output made while
the subscription was active. The account was on Pro on 2026-07-04, 07-08 and 07-20, as it has been
since day 0, so the assignment applies to all 56 unqualified.

**Remix does not bite.** A remix-enabled output is restricted to non-commercial use *"regardless of
whether you are a free Service tier user or a subscriber to a paid Service tier"* — the one
restriction that survives the paid-tier assignment. The feature has never been switched on for this
account, so the clause never attaches. It has to stay off.

**The two URLs are one document.** `suno.com/terms` and `suno.com/terms-of-service` resolve to the
same terms, confirmed by the operator 2026-08-22. There is no second set of conditions to capture.

## The one gap: model version

`COMMISSION.md` §9 wants the model version recorded per generated item, because models are on a
published deprecation path and a band's albums will not match each other across a model change.
**These 56 assets do not carry it.** Their Suno tags hold only `made with suno`, a creation timestamp
and a generation id — no model field. The 45 songs record `v5.5`; July's model is unknown from the
files alone.

This is a provenance gap, not a licence gap — nothing about which model produced them changes who
owns them. It is recoverable: each asset's generation id is in its own ID3 comment tag and the
account still holds the generations. `ARCHITECTURE.md` §9 now names `make imaging-tag` as the command
that will write licence period, generation date, model version and the AI marker into these files
(D-093); it does not exist yet, and this is the gap it closes.

---

*Read from the full terms by a non-lawyer, and to be reviewed properly before launch (COMMISSION §9,
and Phase G's legal review). `2026-08-suno-terms.pdf` beside this file is the record; this is only
the reading, and the facts about the account are the operator's, recorded on the date given.*
