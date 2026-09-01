# Suno licence — what applies to every song generated in 2026-08

> **The evidence is `2026-08-suno-terms.pdf`, beside this file.** That is the complete, dated record
> M-40 asks for: 19 pages, captured from <https://suno.com/terms> on 2026-08-15 at 20:46, revision
> date *March 26, 2026*, ending on the force-majeure clause and the contact block.
>
> **This file is the reading, not the evidence.** It pulls out the clauses that decide whether this
> station may broadcast what it generated, so that nobody has to re-read 19 pages to find them. Where
> the two differ, the PDF governs.

**Verified complete.** The PDF extracts to 62,580 characters and carries the *Pro or Premier*
assignment, the free/Basic non-commercial covenant, the Remix clause, the arbitration agreement,
severability and entire-agreement. An earlier text capture of the same page was truncated at ~50,000
characters part-way through *Arbitration Procedures*; the PDF is ~12,000 characters longer and is
the one to rely on.

| | |
|---|---|
| Evidence file | `2026-08-suno-terms.pdf` |
| Source | <https://suno.com/terms> |
| Date of last revision, as stated on the page | **March 26, 2026** |
| Captured | 2026-08-15 |
| Covers generation month | 2026-08 |
| Songs generated under it | **348, across 40 albums** — every take in the catalogue. The M-18 pilot's 45 (`al_001` … `al_004`) on 2026-08-15, relay-pop's 60 (M-30), lane-rock's 110 (M-31), Frontier Reels' 95 (M-33) and old-system sessions' first 38 (M-34) on 2026-08-30 and 2026-08-31. **Every one carries `suno_created` inside 2026-08**, so this one capture covers all of them. Counted off `music/production/lyrics/` on 2026-08-31 |
| Model version used | v5.5 |
| Subscription tier at generation | **Pro** — confirmed by the operator 2026-08-15, and every `generation:` block since records the same account, tier and settings |
| Remix features | **disabled** — confirmed by the operator 2026-08-15, and unchanged on every sitting since (see §Remix below: a remix-enabled track is non-commercial even on a paid tier) |
| `licence_period` recorded in the lyrics files | `suno-pro-2026-08` |
| Capture method | browser Print → PDF |
| Complete? | **Yes** — 19 of 19 pages, 62,580 characters |

**The page carried a banner: _"Our terms are changing soon. See here to view the new terms."_**
So the March 26 2026 revision is on its way out. The successor terms need capturing as their own
dated file the moment they take effect, and the songs generated under each set need to stay
distinguishable — which is exactly why COMMISSION §9 files this evidence per generation period
rather than once per project.

---

## The clause the whole question turns on

From *Intellectual Property Rights → Content*:

> Subject to your compliance with these Terms of Service, if you are a user who has subscribed to
> the **Pro or Premier** paid tier of the Service, Suno hereby assigns to you all of its right,
> title and interest in and to any Output owned by Suno and generated from Submissions made by you
> through the Service **during the term of your paid-tier subscription**. However, due to the nature
> of machine learning, Suno makes no representation or warranty to you that any copyright will vest
> in any Output.

> If you are a user of the free or **Basic** tier of the Service then, you covenant and agree that
> you will only use Outputs generated from Submissions made by you through the Service solely for
> your lawful, internal, personal and **non-commercial** purposes, provided that you give
> attribution credit to Suno in each case.

**The account was on Pro with remixing disabled when these were generated** (operator, 2026-08-15),
so the assignment above applies to all of them unqualified, and the Remix carve-out below does not
bite. **Three things still follow, and COMMISSION §9 already anticipated all three.**

1. **The tier is the whole question.** Pro or Premier assigns the output to the account holder.
   Free or Basic does not, and restricts use to personal and non-commercial — which a public
   broadcast is not, whatever the station charges.
2. **The assignment is scoped to the subscription term**, not to the account. Rights attach at the
   moment of generation, to output made *while the subscription was active*. This is the sentence
   that makes per-month evidence necessary and makes it impossible to reconstruct later.
3. **No warranty that copyright vests.** The station may broadcast and publish; whether it could
   stop somebody else copying a track is a separate and weaker question. §9 says this already.

## Commercial use

From *Conditions of Access and Use → Commercial Use*:

> **Subject to the Content Section below**, unless otherwise expressly authorized herein or in the
> Service, you agree not to display, distribute, license, perform, publish, reproduce, duplicate,
> copy, create derivative works from, modify, sell, resell, grant access to, transfer, or otherwise
> use or exploit any portion of the Service, and any Output or Voice Model, for any commercial
> purposes.

The default is a blanket prohibition, and the Content section's Pro/Premier assignment is the
carve-out that lifts it. There is no third route.

## Remix — checked, and it has to stay off

From *Intellectual Property Rights → Content*:

> If you are a user that activates features that permit other users of the Service ("Remixers") to
> remix your Outputs (each, a "Remix"), then you agree that all Remixes shall be a joint work owned
> jointly and equally by you and the Remixer […] and **regardless of whether you are a free Service
> tier user or a subscriber to a paid Service tier**, you additionally covenant and agree that the
> Remix may only be used for lawful, internal, personal and **non-commercial** purposes.

**A remix-enabled track is non-commercial even on a paid tier** — the restriction survives the
paid-tier assignment. Remixing was disabled on this account for these 45 (operator, 2026-08-15), so
the clause does not bite here. It has to stay off, or individual later songs become unusable without
anything in the audio showing it.

Output also defaults to public in some third-party surfaces:

> For the avoidance of doubt, Output may be publicly available in a third party application such as
> Discord […] provided, however, that you may change your settings to bypass these public sharing
> default settings so that Output generated will remain private.

## Output is not guaranteed unique

> Due to the nature of machine learning, Output may not be unique across users and the Service may
> generate the same or similar output for a third party. Other users may provide similar submissions
> and receive the same output.

Relevant to `PRODUCT.md`'s tribute-not-derivative posture and to the §8 litmus test: the station
cannot assume any track is exclusive to it.

## Litigation and model retirement

**The terms are silent on the vendor's litigation with major labels.** Checked against the full
PDF: the single occurrence of "litigation" is about arbitration costs, and no label is named
anywhere. COMMISSION §9 records that exposure from other sources, and nothing here confirms,
qualifies or disclaims it — the risk sits outside this document entirely.

The model-retirement risk §9 names is visible here, though: *"Suno reserves the right to modify,
suspend or discontinue, temporarily or permanently, the Service (or any part thereof) with or
without notice."* That is the clause behind §9's instruction to finish a band in one sitting and
record the model version per song, which these four albums do — all 45 on v5.5.

---

*Read from the full terms by a non-lawyer, and to be reviewed properly before launch (COMMISSION
§9, and Phase G's legal review). The PDF beside this file is the record; this is only the reading.*
