# music/jingles — the station imaging pile

What exists, what it is for, and what is still missing before C6 is done.

**This is not a document in the §32 sense** — it is a `README.md`, which `CLAUDE.md` permits, and it
replaces three briefs carried over from the previous attempt (`JINGLE_PROMPTS.md`, `_2`, `_3`),
deleted 2026-08-22 once the parts worth keeping were folded in here.

**Nothing here is wired to anything yet.** There is no `imaging` table, no `mix.py`, no `grid.yaml`.
These are 56 audio files and a filing decision. `ARCHITECTURE.md` §9 is what will eventually read
them; `PHASES.md` calls this content item **C6**, in **Phase F**, build step 12.

**All 56 are approved.** The operator listened to the whole pile and accepted it on 2026-08-23; the
`approved/` and `review/` split has served its purpose and everything now sits in `approved/`. The
standing policy on any piece that disappoints on air: **replace the file, re-index, and redo the
licence record for the month it was regenerated in** — the assets are cheap and none of this is
load-bearing until it is in `imaging/catalogue.yaml`.

**The route into the system is now decided** (D-093, 2026-08-22). These files become rows in
`imaging/catalogue.yaml`, loaded by `make imaging-sync`, measured by `make imaging-analyse` and
stamped with their provenance by `make imaging-tag` — the same pattern `music/catalogue.yaml` and
`make music-sync` already follow. None of it is built yet; all of it is Phase F, build step 12.
The audio's eventual home is the external volume under `imaging/`, not this folder and not git —
`music/jingles/` is where they sit until the Studio arrives (§4).

---

## 1. Provenance and licence

All 56 files were generated in **Suno** during the previous attempt, on three dates:

| Generated | Files |
|---|---|
| 2026-07-04 | 25 |
| 2026-07-08 | 22 |
| 2026-07-20 | 9 |

Every file carries its Suno generation id in its own ID3 comment tag (`id=…`), so any of them can be
re-exported from the account — including as WAV — without regenerating. **No WAV masters exist**;
the pile is MP3 only, 48 kHz stereo, ~165–215 kbps.

**Licence position, confirmed by the operator 2026-08-22:**

- The account has been on **Suno Pro since day 0, continuously** — so the paid-tier assignment in
  Suno's terms applied at the moment each of these was generated.
- **Remix has never been enabled**, so the joint-work / non-commercial clause never attaches.
- `suno.com/terms` and `suno.com/terms-of-service` are the same document. Its stated revision date is
  **March 26, 2026**, which predates all three generation dates and is still the revision in force.
  The captured evidence in `music/licence-evidence/2026-08-suno-terms.pdf` is therefore the governing
  text for these files as well as for the 45 songs.

**Settled, 2026-08-24 (I-01, I-03).** Both of the things this section listed as outstanding are
done. July 2026 has its licence file — `music/licence-evidence/2026-07-suno-licence-note.md`, which
records that the same March 2026 revision governs, that the account was on Pro at all three dates,
and that **all 56 were generated on v5.5**. And `make imaging-tag` now writes the licence period,
the generation date, the model version and an AI marker into every one of the 56 files, leaving
Suno's own comment — and with it every generation id — exactly where it was.

---

## 2. The brand sound

*Carried forward from the deleted `JINGLE_PROMPTS.md` §0. It is the operator's own brief and it is
still on-canon: `core/STATION.md` standing fact 8 says the station's tone is "cozy, intelligent and a
little wry, with optimism tempered by difficult questions… neither dystopian nor camp", which is what
this palette was written to.*

Every piece must sound like it came from the same station — recognisable in two seconds, whether it
is the news sting or the night theme.

- **Era / lane:** warm analog retro-futurism — late-70s/80s sci-fi soundtrack feel, brought forward.
- **Core instruments:** warm analog synth pads, Mellotron-style strings, soft mallet/glass bells,
  gentle choir "ahh" pads, slow felt or electric piano, distant warm brass, sub-bass swells.
- **Texture:** tape warmth, soft vinyl/air hiss, deep space and great distance — *cozy vastness*,
  like a lit window seen across the dark.
- **Tempo / energy:** mostly slow–mid, unhurried, hopeful. Even the "urgent" pieces stay composed.
- **The mnemonic:** a simple **3–5 note rising glass-bell signature** that resolves warmly. This is
  the family glue. `approved/sonic_logo_signature.mp3` is its source; everything else quotes it.

**Three energy tiers, to stop the set blurring into one long jingle.** The motif is the glue, not the
palette — within a tier, change the lead instrument per piece and let only the motif recur.

| Tier | BPM | Character |
|---|---|---|
| Night | 56–75 | felt piano, low pads, distant choir |
| Day | 85–105 | arpeggios, mallets, restrained brass, motion |
| Bright | 110–132 | pulses, claps, sweeps, energy |

**Rules that still bind any future generation:**

- **Pro plan only.** Free-tier output is not cleared for air.
- **Custom Mode**, newest model. Style box = 8–15 comma tags, order is priority: genre → mood → lead
  instrument → vocal-or-instrumental → production → BPM. Past ~15 tags Suno ignores the tail.
- **Instrumental pieces:** toggle Instrumental ON *and* keep "instrumental, no vocals" in the Style
  string.
- **Sung pieces:** structure tags go in the Lyrics field, not Style. Hook of 2–4 short lines.
- **Default Exclude Styles:** aggressive EDM, trap, drill, dubstep, heavy metal, distorted, harsh,
  lo-fi tape hiss-heavy, comedic, chiptune novelty.
- **Suno generates a full song**; a sounder is 3–20 s. Generate, crop, fade the tail clean.
- **2–4 takes per asset**, keep the best.
- **IP boundary:** never name a real artist, franchise or composer in a prompt. Describe the sound
  with instruments and adjectives. Imaging is exempt from the safety gate but **not** from the IP
  screen (§9) — and `config/banned-entities.yaml` does not exist yet.

---

## 3. Naming — what these files will eventually be called

**The current names are provisional.** Two facts set the target.

**The filename is not the identifier.** §9's table is `imaging(id, kind, file_path, …)`. The `id` is
the identity; `file_path` is a column pointing at bytes. Nothing resolves by scanning a directory —
unlike the previous attempt, whose brief made the filename load-bearing. So a rename later is a data
change, not a code change, and there is no correctness pressure to settle it before `grid.yaml`
exists.

**The architecture's own convention is subject-first.** From §17a's worked example:

```yaml
- slug: evening_report
  name: "The Evening Report"
  jingle_set: evening_report        # open/close/bed ids from `imaging`
  hour_clock:
    open: evening_open
    bed_under_links: report_bed
    close: evening_close
```

Station-wide the same shape: `station_logo_3s`, `ai_ident`, `news_urgent`, `news_bed_loop`.

The names in this folder are **role-first** (`open_the_evening_report.mp3`). The target is
**subject-first** (`evening_open`), which also sorts a programme's open, close and bed adjacent — so
an incomplete set is visible at a glance. That matters, because incomplete sets are the whole of the
remaining work (§7).

**Two questions C4 settles, not this folder:**

1. **Does the slug keep the article?** The example does both — `evening_report` for "The Evening
   Report" drops it, `the_count` for "The Count" keeps it. Thirty strands, thirty judgements.
2. **Do imaging ids abbreviate the slug?** Programme `evening_report` carries imaging ids
   `evening_open` and `report_bed` — shorter, and inconsistently so.

**So: leave the names until `grid.yaml` exists, then rename once.** Nothing references these files,
so waiting costs nothing and guessing costs a second pass.

> **An ambiguity in §17a for whoever writes C4.** `jingle_set` is mandatory on every programme
> (validation 6), and `hour_clock` separately names imaging ids directly. `evening_report` and `news`
> declare both; `the_count` declares only `jingle_set`. So a set name appears to imply its
> open/close/bed ids by convention when `hour_clock` is absent — which would make the set name
> load-bearing after all, and validation 6 would be checking two overlapping things. Whether
> `hour_clock` is an override or a duplicate is not stated.

---

## 4. Station furniture — 19 files

Each has one unambiguous slot in the current design. These were never in question — they map
straight onto a §9 `kind`.

| File | §9 `kind` / role | Length |
|---|---|---|
| `top_of_hour.mp3` | junction ident | 14.8 s |
| `disclosure_bed.mp3` | underlay for the spoken disclosure (§18) | 103.8 s |
| `sweeper_calm.mp3` · `sweeper_mid.mp3` · `sweeper_bright.mp3` | `sweeper` — §9 wants several, chosen round-robin | 5.4 / 4.8 / 4.8 s |
| `news_sting.mp3` | `news_sting` — §9 specifies a 4 s hard start | 4.4 s |
| `news_open.mp3` | junction open | 7.6 s |
| `music_bumper.mp3` | `bumper` | 9.6 s |
| `time_sting.mp3` | `time_sting` | 5.0 s |
| `chart_marker_approaching/climbing/number_one.mp3` | `chart_marker` — The Count, 14:04 Fri | 4.8 / 3.0 / 5.1 s |
| `fallback_bed.mp3` | the §15 level-5 bed — playout's last resort before silence | 8:00 |
| `link_bed_day.mp3` · `link_bed_night.mp3` | generic `bed_under_links` | 31.6 / 40.4 s |
| `open_the_count.mp3` | The Count, 14:04 Fri | 9.4 s |
| `open_the_gallery.mp3` | The Gallery, 16:04 | 14.6 s |
| `open_ledger.mp3` | Ledger, 11:04 | 18.4 s |
| `open_assembly.mp3` | Assembly, 19:04 | 39.7 s |

---

## 5. Programme opens, items and spares — 37 files

### 5a. The signature — the piece the family hangs on

`sonic_logo_signature.mp3` (12.0 s) is the only sung piece in the set, and its lyric —
*"Settlement Radio — the light between the worlds"* — is **approved as the station's sung tagline**
(operator, 2026-08-23). The station name is confirmed by `core/STATION.md`; the tagline itself is
not in canon and does not contradict it.

Every other piece in the set quotes this one's 3–5 note glass-bell motif, or is meant to — §9's
round-robin ident selection and §2's family rule both rest on it.

**Still owed on this one file:** it is the only asset carrying sung words, so §9's IP screen applies
and `config/banned-entities.yaml` does not exist yet. The screen is owed before air, not before
filing.

### 5b. Programme opens — reassigned from the old grid, 25 files

Each was made for a strand that no longer exists and has been reassigned to one that does; the
operator accepted every assignment on 2026-08-23. Slots are from `PROGRAMMING.md` §8. **These
assignments are the input to `imaging.programme_id`** when the catalogue is built (D-093).

| File | Strand | Slot | Length |
|---|---|---|---|
| `open_early_watch.mp3` | Early Watch | 05:04 | 12.6 s |
| `open_the_long_record.mp3` | The Long Record | 05:32 · 00:32 | 49.0 s |
| `open_first_shift.mp3` | First Shift | 06:04 · 07:04 · 08:04 | 14.4 s |
| `open_the_long_question.mp3` | The Long Question | 09:04 | 13.6 s |
| `open_relay.mp3` | Relay | 09:32 M/W/F | 14.4 s |
| `open_body_and_air.mp3` | Body & Air | 09:32 Tu/Th | 24.5 s |
| `open_the_common_table.mp3` | The Common Table | 10:04 | 11.0 s |
| `open_dispatch.mp3` | Dispatch | 11:32 | 33.7 s |
| `open_the_midday_report.mp3` | The Midday Report | 12:04 | 9.6 s |
| `open_the_bench.mp3` | The Bench | 13:04 | 23.9 s |
| `open_cut.mp3` | Cut | 14:32 | 11.1 s |
| `open_ice_and_iron.mp3` | Ice & Iron | 15:04 | 9.0 s |
| `open_the_evening_report.mp3` | The Evening Report | 17:04 | 17.8 s |
| `open_crossfire.mp3` | Crossfire | 18:32 | 19.3 s |
| `open_the_documentary.mp3` | The Documentary | 20:04 | 24.6 s |
| `open_faith_in_transit.mp3` | Faith in Transit | 21:04 | 30.0 s |
| `open_the_late_report.mp3` | The Late Report | 22:04 | 19.9 s |
| `open_night_record.mp3` | Night Record | 23:04 | 14.4 s |
| `open_the_midnight_report.mp3` | The Midnight Report | 00:04 | 23.9 s |
| `open_the_night_watch_0104.mp3` | The Night Watch | 01:04 | 23.0 s |
| `open_the_night_watch_0104_alt.mp3` | The Night Watch — **second candidate for the same slot** | 01:04 | 14.8 s |
| `open_the_night_watch_0204.mp3` | The Night Watch | 02:04 | 15.5 s |
| `open_the_night_watch_0304.mp3` | The Night Watch | 03:04 | 18.0 s |
| `open_the_night_watch_0404.mp3` | The Night Watch | 04:04 | 24.0 s |
| `open_sixth_day.mp3` | Sixth Day | weekend 06:04 | 29.5 s |

> Two candidates compete for The Night Watch 01:04 — pick one and the other becomes spare.
>
> Whether The Night Watch is **one** programme entry or **four** is unsettled until `grid.yaml` is
> written. §17a requires a `jingle_set` per programme, so that choice changes the count by three.

### 5c. Items and events — 7 files

Not programme themes. Each had a role in the old grid that this grid handles differently, and each
is kept in the role below.

| File | Role in this design | Note |
|---|---|---|
| `open_fallback_generic.mp3` | generic open for any strand with no theme of its own | keep a fallback at all? |
| `item_letter.mp3` | the `letter` item — in-world correspondence read by a host (§11, 60–90 s) | demoted from strand theme to item |
| `item_conditions.mp3` | weather, which is an item inside Early Watch, not a strand | demoted from strand theme to item |
| `item_advisory.mp3` | all-settlements advisory | does this design have advisories? |
| `junction_handover.mp3` | handover — §13 lists it in the junction | still needed with strand hosts? |
| `event_lumen_festival.mp3` | Lumen Festival — real canon (`canon/51-observances.md`) | no strand owns it |
| `event_special_coverage.mp3` | any large event the station carries | event-agnostic; keep? |

### 5d. Spare — 4 files, no strand in this grid

Good audio, unassigned only because no current strand matches. **Kept** — the grid grows, and each is
recoverable from Suno anyway. They carry no `programme_id` and will sit in the catalogue as
unassigned pieces until a strand wants them.

| File | Was |
|---|---|
| `spare_communications.mp3` | a communications strand |
| `spare_travel.mp3` | a travel strand |
| `spare_field_dispatch.mp3` | a field-dispatch strand — Dispatch already has `open_dispatch` |
| `spare_economics.mp3` | an economics strand — duplicates Ledger |

---

## 6. Known defects

Measured 2026-08-22 with `ffmpeg ebur128` and tail-versus-body level comparison.

**Five files are cut off mid-body and need a tail fade** — or a clean re-export from the Suno
original, which the generation ids make possible:

| File | Tail vs body |
|---|---|
| `approved/time_sting.mp3` | +0.5 dB |
| `approved/chart_marker_climbing.mp3` | −1.5 dB |
| `approved/open_ledger.mp3` | −1.4 dB |
| `approved/open_the_night_watch_0304.mp3` | −0.7 dB |
| `approved/open_the_night_watch_0204.mp3` | −6.3 dB |

**Two files have no headroom** and will clip on any re-encode: `approved/chart_marker_approaching.mp3`
(0.0 dBTP) and `approved/open_the_long_record.mp3` (−0.0 dBTP).

`approved/fallback_bed.mp3` does not resolve at its end — correct for a loop, but the seam is
untreated. §9's `bed_loop_sec` field is where that gets declared rather than edited into the file.

**Everything else ends cleanly**, 20–75 dB below body level. Integrated loudness across the set sits
in a tight −12 to −19 LUFS band; §9 has the mixer normalise anyway.

**Lengths run long.** Strand opens are 9–49 s where a programme open wants roughly 8–15 s. That is
more material to cut from rather than a fault, but it is ~29 pieces to trim by ear.

---

## 7. What is missing to complete C6

`PHASES.md` sizes C6 as *"~30 jingle sets — one per strand, each an open, close and bed, plus a sting
for news — and the station furniture on top. Call it 100+ pieces."* `ARCHITECTURE.md` §17a validation
6 makes a `jingle_set` mandatory for **every** programme, which is what forces that number.

**Station furniture is essentially complete** — 15 of ~16 slots filled. The one gap:

- **`news_bed`** — a loop that ducks to −12 dB under the bulletin. `news_open.mp3` is an opener, not
  this.

**Strand sets are about one third done, and it is the cheap third.**

| | Have | Need | Missing |
|---|---|---|---|
| Strand opens | 29 | ~30 | **5** |
| Strand closes | **0** | ~30 | **~30** |
| Per-strand link beds | 0 (2 generic) | ~30, or accept shared | **~28, or a design decision** |

**Five strands have no open and no candidate:**

| Strand | Slot |
|---|---|
| Vantage | 13:32 |
| Names | 16:32 |
| The Six | 18:04 — the main news programme of the day |
| The Week in Ice | Sat 12:04 |
| Observance | Sun 09:04 — `open_faith_in_transit.mp3` could double, operator's call |

**So: roughly 36 new pieces at minimum** (5 opens + 30 closes + news_bed), or **~64** if every strand
gets its own link bed rather than sharing the two generic ones. That second number is a design
decision that belongs in `grid.yaml`, not here — §9's `bed_under_links` is declared per programme but
nothing stops two programmes naming the same bed.

**Not blocked by hardware.** What blocks the strand work is `grid.yaml` (content item **C4**), because
programme ids do not exist until it is written and this folder's `open_*` names are guesses at them.
`PHASES.md` lists C4 as startable now — it needs no machine.

---

## 8. Deleted 2026-08-22

**Five audio files**, because the current design has no place for them and cannot acquire one:

| File | Why |
|---|---|
| `d18_break_in.mp3` · `d18_break_out.mp3` · `d8_brand.mp3` | ad-break brackets and a sponsor bug. `PRODUCT.md` §10 — *"No advertising, no sponsorship reading, no paywall on the stream."* |
| `the_relay_round.mp3` · `d21_quiz_point.mp3` | a quiz theme and its scoring ding. This grid has no quiz strand. |

**Three briefs** — `JINGLE_PROMPTS.md`, `JINGLE_PROMPTS_2.md`, `JINGLE_PROMPTS_3.md`. They were
written against a repository that no longer exists: they reference `docs/ROADMAP.md`,
`docs/PHASE_D_JINGLES_TASKS.md`, `docs/PHASE_R_TASKS.md`, `docs/MEDIA_LIBRARY.md`,
`docs/programming/grid.yaml`, `src/production/media.py`, an `assets/` tree, a `make jingle-audit`
target, and a cast including Orin, Sera, Kael and an Archivist who are not in `cast/CAST.md`. Section
2 above preserves the part that survived — the palette, the motif, the tiers and the Suno rules.

All eight are recoverable: the audio from its Suno generation id, the briefs from git history of the
previous attempt if it still exists.

---

## 9. Suno recipes — the style string behind each existing piece

*Recovered 2026-08-22 from the three deleted briefs. **37 of the 56 files have their recipe here;
19 do not** — those were in sections of `JINGLE_PROMPTS.md` that were not captured before deletion.
Every one of those 19 is still recoverable from the Suno account: each file's ID3 comment tag holds
its generation id, and Suno shows the style string against the generation.*

**Why this matters:** when a closer is made for a programme, it should be built from that
programme's opener recipe — same lead instrument, same BPM, same tier — or the pair will not sound
like one set. The palette in §2 is the family rule; these are the individual ones.

### Core identity

| File | Suno Style |
|---|---|
| `approved/sonic_logo_signature.mp3` | `short sung station ident, 8 seconds, warm retro-futuristic, analog synth pads, mellotron strings, glass bell mnemonic, gentle close-mic female and male unison vocal, hopeful, wondrous, cozy, sparse arrangement, tape warmth, 75 BPM` |
| `approved/top_of_hour.mp3` | `instrumental, no vocals, short 5-second radio sounder, warm retro-futuristic, rising analog synth swell, mellotron strings, soft brass fanfare restrained, glass bell motif, hopeful and clean, deep space ambience, tape warmth, 80 BPM` |
| `approved/disclosure_bed.mp3` | `instrumental, no vocals, 15-second seamless loopable ambient underscore, soft sustained analog pad, gentle felt piano, low warm drone, neutral and honest, unhurried, spacious, very low energy, no melody hooks, 60 BPM` |
| `approved/sweeper_calm.mp3` | `instrumental, no vocals, very short 3-second radio sweeper, SOFT RISING PAD SWEEP, single glass bell motif, gentle and spacious, clean tail, 72 BPM` |
| `approved/sweeper_mid.mp3` | `instrumental, no vocals, very short 3-second radio sweeper, WARM SYNTH ARPEGGIO RUSH, mallet accent into bell motif, forward motion, clean tail, 100 BPM` |
| `approved/sweeper_bright.mp3` | `instrumental, no vocals, very short 3-second radio sweeper, BRIGHT WHOOSH AND PULSE, quick rising sparkle into bell motif, energetic and joyful, punchy clean tail, 124 BPM` |

**`sonic_logo_signature.mp3` is the only piece with lyrics.** Its Lyrics box held:

```
[Hook]
(warm, intimate, two voices in soft unison)
Settlement Radio —
the light between the worlds.
[Outro]
(a single rising glass-bell motif, resolving warmly)
```

### Junction, beds and utility furniture

| File | Suno Style |
|---|---|
| `approved/news_open.mp3` | `instrumental, no vocals, 10-second news bulletin theme opener, confident analog synth pulse, steady arpeggio, clean brass stabs restrained, glass bell accents, authoritative but warm, trustworthy, forward-moving, resolves to a clean pad, 100 BPM` |
| `approved/news_sting.mp3` | `instrumental, no vocals, very short 2-second news sting, sharp clean synth stab, single rising glass bell, tight brass hit restrained, urgent but composed, crisp, no tail, 110 BPM` |
| `approved/music_bumper.mp3` | `instrumental, no vocals, short 5 seconds music bumper, warm rising synth sweep, shimmer pad, soft four-on-floor pulse entering, anticipatory, elegant, lifts into a track, clean downbeat resolve, 100 BPM` |
| `approved/time_sting.mp3` | `instrumental, no vocals, short 4-second time-check sounder, soft ticking mallet pulse, single clear glass chime, warm pad underneath, calm and precise, reassuring, spacious, 72 BPM` |
| `approved/junction_handover.mp3` | `instrumental no vocals short 6 second transition sounder two intertwining synth motifs handing off soft Alternative Rock, Post-grunge pad single warm bell resolve passing the light feeling tender cinematic 80 bpm` |
| `approved/fallback_bed.mp3` | `instrumental, no vocals, long 3-minute ambient space-radio bed, seamless loop, warm slow analog pads, gentle evolving drone, soft glass bell motif recurring sparsely, distant choir, calm and patient, cozy vastness, tape warmth, 60 BPM` |
| `approved/link_bed_day.mp3` | `instrumental, no vocals, 30-second talk-show theme opener, loops cleanly as a bed, warm and conversational, relaxed electric piano, soft brushed groove, mellow analog bass, gentle vibraphone, friendly and curious, a little wry, intimate, 88 BPM` |
| `approved/link_bed_night.mp3` | `instrumental, no vocals, 45 seconds night-radio theme opener, warm ambient, slow felt piano, deep analog pad, distant choir, soft sub-bass swell, intimate and reassuring, starlit, unhurried, vinyl warmth, melancholic but kind, 64 BPM` |

> **`junction_handover.mp3` carries `Alternative Rock, Post-grunge` in its style string** — off-palette
> and adjacent to §2's Exclude Styles list. Whether that reads as off-family is an ear question, but
> the recipe is contaminated and should not be reused verbatim for anything else.

### Strand opens and spares

| File | Suno Style |
|---|---|
| `approved/open_first_shift.mp3` | `instrumental, no vocals, 10-second breakfast news-magazine theme opener, warm retro-futuristic, bright analog synth arpeggio, mallet bells, soft rising strings, restrained brass, awake and purposeful, optimistic morning energy, glass bell motif, tape warmth, 98 BPM` |
| `approved/open_the_midday_report.mp3` | `instrumental, no vocals, 10-second midday news theme opener, warm retro-futuristic, steady analog synth pulse, restrained brass stabs, glass bell accents, authoritative but warm, trustworthy forward motion, faint relay-signal texture, tape warmth, 100 BPM` |
| `approved/open_the_evening_report.mp3` | `instrumental, no vocals, 10-second drive-time news round-up theme, warm retro-futuristic, relaxed electric piano, soft groove, mellow analog bass, gentle brass, end-of-day warmth, composed and forward-moving, glass bell motif, tape warmth, 92 BPM` |
| `approved/open_sixth_day.mp3` | `instrumental, no vocals, 10-second daily-life magazine theme, warm retro-futuristic, soft vibraphone, brushed groove, mellow electric piano, gentle strings, friendly and human, unhurried and open, glass bell motif, tape warmth, 90 BPM` |
| `approved/open_assembly.mp3` | `instrumental, no vocals, 10-second political-affairs theme opener, warm retro-futuristic, low sustained strings, measured felt piano, noble restrained brass, deliberative and weighty, dignified never martial, slow glass bell motif, deep space ambience, tape warmth, 84 BPM` |
| `approved/spare_economics.mp3` | `instrumental, no vocals, 10-second economics-and-trade theme, warm retro-futuristic, walking synth bass, bright mallet arpeggio, soft brass, purposeful mercantile motion, busy but composed, the long haul, glass bell motif, tape warmth, 104 BPM` |
| `approved/open_dispatch.mp3` | `instrumental, no vocals, 10-second frontier-affairs theme opener, warm retro-futuristic, low tense synth pulse, distant restrained brass, sparse taut strings, watchful and composed, serious never panicked, deep space distance, glass bell motif, tape warmth, 96 BPM` |
| `approved/open_the_bench.mp3` | `instrumental, no vocals, 10-second law-and-justice theme opener, warm retro-futuristic, slow grave felt piano, deep warm pad, single sober bell, measured and considered, the weight of judgement, calm and sombre, glass bell motif, tape warmth, 80 BPM` |
| `approved/open_relay.mp3` | `instrumental, no vocals, 10-second science-and-engineering theme, warm retro-futuristic, bright analog arpeggio, glassy bells, curious mallet motifs, inventive and wondrous, forward and clean, sense of discovery, glass bell motif, tape warmth, 100 BPM` |
| `approved/spare_travel.mp3` | `instrumental, no vocals, 10-second travel theme opener, warm retro-futuristic, wandering mallet melody, soft strings, gentle analog pads, journeying and curious, the wonder of a world a week, warm open horizons, glass bell motif, tape warmth, 94 BPM` |
| `approved/open_the_long_record.mp3` | `instrumental, no vocals, 12-second deep-history theme opener, warm retro-futuristic, mellotron strings, low warm drone, sparse felt piano, distant choir, patient and ancient, the weight of ages, slow glass bell motif, vinyl warmth, 68 BPM` |
| `approved/open_the_night_watch_0104_alt.mp3` | `instrumental, no vocals, 10-second literary theme opener, warm retro-futuristic, intimate felt piano, soft mellotron strings, storytelling and tender, unhurried and human, close and inviting, glass bell motif, tape warmth, 76 BPM` |
| `approved/spare_communications.mp3` | `instrumental, no vocals, 10-second communications theme opener, warm retro-futuristic, soft radio-signal sweeps, gentle analog pulse, distant voices texture, the network that binds, connected across distance, glass bell motif, deep space ambience, tape warmth, 90 BPM` |
| `approved/open_crossfire.mp3` | `instrumental, no vocals, 10-second debate-and-ideas theme, warm retro-futuristic, lively electric piano, bright vibraphone, soft groove, engaged and a little wry, reasoned and warm, the big questions, glass bell motif, tape warmth, 96 BPM` |
| `approved/open_the_gallery.mp3` | `instrumental, no vocals, 10-second arts theme opener, warm retro-futuristic, elegant strings, soft refined brass, glass bells, graceful and celebrated, performance and craft, poised and warm, glass bell motif, tape warmth, 92 BPM` |
| `approved/open_night_record.mp3` | `instrumental, no vocals, 8-second music-show theme, warm retro-futuristic, bright rising synth sweep, shimmer pad, soft four-on-floor pulse entering, anticipatory DJ energy, elegant and lifting, glass bell motif, clean downbeat, tape warmth, 112 BPM` |
| `approved/open_the_night_watch_0204.mp3` | `instrumental, no vocals, 12-second late-night archive theme, warm retro-futuristic, low evolving drone, sparse glass bell, distant choir, dusty analog pad, mysterious and still, the deep archives at night, slow glass bell motif, vinyl warmth, 60 BPM` |
| `approved/open_the_night_watch_0304.mp3` | `instrumental, no vocals, 12-second pre-dawn cosmos theme, warm retro-futuristic, shimmering pad, soft radio-signal sweeps, deep sub-bass swell, distant wind-like synth, vast and awed, the sublime dark before dawn, sparse glass bell motif, tape warmth, 62 BPM` |
| `approved/open_the_night_watch_0104.mp3` | `instrumental, no vocals, 10-second weekend-culture theme, warm retro-futuristic, relaxed electric piano, easy strings, soft mallets, unhurried weekend warmth, culture and history blended, companionable, glass bell motif, tape warmth, 88 BPM` |
| `approved/spare_field_dispatch.mp3` | `instrumental, no vocals, 10-second field-dispatch theme, warm retro-futuristic, warm analog pad, soft radio-signal sweeps, gentle mallets, dispatches from the far edge, distance and relay warmth, expeditionary calm, glass bell motif, deep space ambience, tape warmth, 84 BPM` |
| `approved/open_the_night_watch_0404.mp3` | `instrumental, no vocals, 12-second reflective music-hour theme, warm retro-futuristic, felt piano, ambient analog pad, soft distant choir, spacious and contemplative, close listening, unhurried, sparse glass bell motif, vinyl warmth, 66 BPM` |
| `approved/open_faith_in_transit.mp3` | `instrumental, no vocals, 12-second reflective gathering theme, warm retro-futuristic, soft wordless choir ahh, warm analog pads, gentle felt piano, single warm bell, communal and humane, meaning and quiet hope, glass bell motif, tape warmth, 72 BPM` |
| `approved/open_ledger.mp3` | `instrumental, no vocals, 8-second markets-brief theme opener, warm retro-futuristic, crisp analog synth pulse, precise ticker-tape mallet ticks, restrained brass stab, dry and exact, brisk no-nonsense energy, composed urgency, glass bell motif, tape warmth, 102 BPM` |
| `approved/open_body_and_air.mp3` | `instrumental, no vocals, 10-second medical-magazine theme opener, warm retro-futuristic, gentle felt piano, soft mallet bells, warm sustained strings, caring and steady, calm competence, quietly reassuring, glass bell motif, tape warmth, 88 BPM` |
| `approved/open_the_common_table.mp3` | `instrumental, no vocals, 10-second kitchen-table theme opener, warm retro-futuristic, playful pizzicato-style mallets, soft brushed groove, warm electric piano, homely and inviting, market-stall bustle, a little playful, glass bell motif, tape warmth, 96 BPM` |
| `approved/open_the_count.mp3` | `instrumental, no vocals, 10-second chart-show theme opener, warm retro-futuristic, driving four-on-floor pulse, bright synth stabs, rising mallet run, danceable and proud, countdown excitement, glass bell motif hook, tape warmth, 122 BPM` |
| `approved/open_the_documentary.mp3` | `instrumental, no vocals, 12-second serial-drama theme opener, warm retro-futuristic, intimate felt piano, slow mellotron strings, soft page-turn-like mallet accent, a hint of cliffhanger tension, storytelling and hushed, the night settling in to listen, sparse glass bell motif, vinyl warmth, 66 BPM` |
| `approved/open_cut.mp3` | `instrumental, no vocals, 8-second style-and-fashion theme opener, warm retro-futuristic, playful pizzicato mallets, bright synth pulse, strutting groove, stylish and a little cheeky, runway energy kept warm not cold, glass bell motif, tape warmth, 116 BPM` |

| `approved/open_early_watch.mp3` | `instrumental, no vocals, 12-second sunrise radio theme opener, bright and hopeful, warm analog synth arpeggio, mallet bells, soft strings rising, gentle uplifting brass, curious and awake, optimistic, clean and airy, 96 BPM` |
| `approved/open_the_long_question.mp3` | `instrumental, no vocals, 10-second daytime radio theme opener, warm and steady, mid-tempo analog synth pulse, soft mallet bells, easy strings, gentle purposeful groove, companionable and open, optimistic workday feel, tape warmth, 92 BPM` |
| `approved/open_the_late_report.mp3` | `instrumental, no vocals, 10-second dusk radio theme opener, warm, settling synth pads, slow mallet bells, low strings entering, day winding down feeling, calm but not yet sleepy, amber and gentle, tape warmth, 84 BPM` |
| `approved/open_the_midnight_report.mp3` | `instrumental, no vocals, 12-seconds night-radio theme opener, warm ambient, slow felt piano, deep analog pad, distant choir, soft sub-bass swell, intimate and reassuring, starlit, unhurried, vinyl warmth, melancholic but kind, 64 BPM` |
| `approved/open_ice_and_iron.mp3` | `instrumental, no vocals, 10 seconds sports-broadcast theme opener, bright synth brass fanfare, driving mallet rhythm, soaring strings, triumphant but elegant, energetic and proud, celebratory, cinematic, 120 BPM` |

### Items and events

| File | Suno Style |
|---|---|
| `approved/item_letter.mp3` | `10-second nostalgic radio theme, soft wordless female humming melody, no lyrics no words, gentle felt piano, mellotron strings, distant radio static warmth, longing and tender, intimate, humming fades into warm static, slow, 70 BPM` |
| `approved/item_conditions.mp3` | `instrumental, no vocals, 10-second atmospheric theme dropping to a low bed, slow shimmering pad, soft radio-signal sweeps, distant wind-like synth, deep calm drone, gentle bell, vast and serene, contemplative, 66 BPM` |
| `approved/event_lumen_festival.mp3` | `15-second celebratory festival theme, soft wordless massed choir ahh rising warmly, no lyrics no words, glowing analog synths, twinkling bells layering in, gentle uplifting strings, communal and luminous, hopeful, building slowly never bombastic, resolving into a glowing bell motif, 84 BPM` |
| `approved/event_special_coverage.mp3` | `instrumental, no vocals, 12-second event coverage theme resolving to a low loopable pad, purposeful analog synth pulse, slow-building strings, restrained noble brass, glass bell motif, sense of occasion, dignified anticipation, neither happy nor sad, tape warmth, 96 BPM` |

> **`item_letter.mp3` and `event_lumen_festival.mp3` are not instrumental** — both carry wordless
> voice (humming, massed choir "ahh"). No lyrics, so §9's IP screen over sung words does not bite,
> but they are the only two pieces besides the signature with a human voice in them.

### Chart markers

| File | Suno Style |
|---|---|
| `approved/chart_marker_approaching.mp3` | `instrumental, no vocals, very short 2-second countdown tick sting, crisp mallet tick with soft synth pulse, matter-of-fact forward motion, clean tail, 108 BPM` |
| `approved/chart_marker_climbing.mp3` | `instrumental, no vocals, very short 3-second countdown sting, rising synth arpeggio run, quickening mallet pulse, building excitement, bright and eager, clean tail, 118 BPM` |
| `approved/chart_marker_number_one.mp3` | `instrumental, no vocals, short 4-second countdown climax sting, bright triumphant synth stab, rising sweep into a ringing bell motif hit, proud and celebratory, punchy clean resolve, 126 BPM` |

### The 2 still with no recipe

Seventeen came back from Suno on 2026-08-22 and are filed above. Two did not:

| File | Originally | Suno generation id | Why |
|---|---|---|---|
| `approved/open_fallback_generic.mp3` | `c9_talk.mp3` | `39a714de-cbf0-43de-a166-cff33b1f9e59` | not found in the account |
| `approved/item_advisory.mp3` | `d15_advisory.mp3` | `a93eef8e-64a3-471f-a105-2e3732fa1178` | found, no style string returned. **Its embedded title tag wrongly reads `d14_conditions`** — a mislabel from the previous attempt; search by the id, not the name |

Neither needs a matching partner built for it, so neither blocks anything. `open_fallback_generic`
is a candidate for regeneration anyway — §5c asks whether a generic fallback open is wanted at all.

**Model version is still unrecorded for all 56.** `COMMISSION.md` §9 wants it per item; see
`music/licence-evidence/2026-07-suno-licence-note.md`.
