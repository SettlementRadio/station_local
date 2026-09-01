# Suno licence — what applies to the songs generated 2026-09

> **The terms in force on 2026-09-01 are the ones already captured in `2026-08-suno-terms.pdf`.**
> The operator has confirmed that Suno's terms do not change until **2026-09-03**, so the six songs
> generated on 2026-09-01 were made under the **March 26, 2026** revision — the same document the
> 2026-08 note reads, page for page. **The evidence for this period is that file**, and the reading
> that applies is the 2026-08 note.
>
> **A separate 2026-09 capture is still worth taking**, because the terms change on 2026-09-03 and
> anything generated from that date on is under a different document. That capture belongs to the
> period that starts on the 3rd, not to these six songs.

**What is outstanding:** nothing for these six songs. **From 2026-09-03**, capture the new terms as
`2026-09-suno-terms.pdf` before generating anything else, and read them properly — they are a
different document, not a re-issue. That is M-40's job for the rest of September.

| | |
|---|---|
| Evidence file | `2026-08-suno-terms.pdf` — the same revision was in force on 2026-09-01 |
| Source | <https://suno.com/terms> |
| Date of last revision, as stated on the page | **March 26, 2026** — unchanged until 2026-09-03 (operator, 2026-09-01) |
| Captured | 2026-08-15, as `2026-08-suno-terms.pdf` |
| Covers generation month | 2026-09 |
| Songs generated under it | **6** — `s_0796` (track 1 of `al_098`, regenerated after the dispatch proved it had never been made) and all five of `al_102` |
| Model version used | v5.5 |
| Subscription tier at generation | **Pro** — confirmed by the operator 2026-09-01 |
| Remix features | **disabled** — confirmed by the operator 2026-09-01 |
| `licence_period` recorded in the lyrics files | `suno-pro-2026-09` |
| Complete? | **Yes for these six songs.** Anything generated from 2026-09-03 needs its own capture |

## Why this period is not a formality

**2026-08's capture recorded a banner on Suno's own page: _"Our terms are changing soon. See here to
view the new terms."_** The March 26 2026 revision was on its way out when that PDF was taken on
2026-08-15. So the September terms may genuinely differ from the ones the 2026-08 note reads, and
the two sets of songs may not be covered by the same clauses. That is precisely why COMMISSION §9
files evidence **per generation period** rather than once per project, and it is why carrying
August's reading forward is an assumption and is labelled as one above.

**What is not in doubt:** the operator has confirmed the account was on **Pro** with **remixing
disabled** on 2026-09-01, which is what COMMISSION §9 conditions commercial rights on — rights
attach to output generated while the subscription is active, and a remix-enabled track is
non-commercial even on a paid tier. The substance is confirmed; the record of the terms it was
confirmed against is what is missing.

## The one album that spans two periods

`al_098` *The Room at Terrace Road* is the only record in the catalogue whose tracks were made in
two different licence periods. Track 1 was regenerated on 2026-09-01 after `make music-dispatch`
proved it had never been generated at all (D-097); tracks 2–13 were made on 2026-08-30. The album's
`generation:` block states `suno-pro-2026-08` and **track 1's own `take:` block overrides it with
`suno-pro-2026-09`**, which is D-062's resolution order — the song's block first, the album's for
anything null in it. Each mp3 carries the period it was actually made under in its own tags, which
is what §9 asks for and what a hand-off will read.

## Cross-references

- `music/licence-evidence/2026-08-suno-licence-note.md` — the reading that covers the other 348 takes
- `music/licence-evidence/2026-08-suno-terms.pdf` — the evidence for those
- COMMISSION.md §9 — what actually applies, and why it is captured per period
- `music/MUSIC_TASKS.md`, M-40 — the card that owns this folder
