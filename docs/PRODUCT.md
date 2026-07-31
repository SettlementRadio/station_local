# Settlement Radio — Product

*What we're building and why. Non-technical. `docs/ARCHITECTURE.md` covers how.*

> **This document sits outside the six-document cap in ARCHITECTURE §32.** It is operator- and
> outward-facing — the source for the About page, grant applications, and explaining the project to
> people. It is **not** in the agent reading path and generates no tasks.

---

## 1. The idea in one paragraph

Settlement Radio is a radio station broadcasting from six hundred years in the future. It runs
around the clock. A newsreader gives the bulletin on the hour; a presenter hosts a morning magazine
built from short reports, a correspondent two-way and an interview; late at night someone plays
records and knows who played bass on them. The news
is invented, the music is generated, the voices are synthetic, and every hour the station says so
out loud. Nothing about it is hidden. What makes it worth listening to is that the world **keeps
going whether or not you are listening**: the convoy that was late this morning docks this
afternoon, and next week somebody mentions it again.

---

## 2. Why this exists

Most generative-AI media is a demo. You look at it once, think *huh*, and never return, because
there is nothing to return to — no continuity, no accumulation, nothing that was true yesterday.

Radio is the opposite shape. It is ambient, it is continuous, you join it in the middle, and its
whole appeal is that it was running before you arrived. That makes it the format where machine
generation has the most to offer and the least to fake: nobody expects to be told everything, and
half of good radio is the sense that there is a room somewhere with people in it.

So the bet is simple. **The product is not the generation. The product is the continuity.**

There is a second reason, and it is a tribute. Golden-age and modern science fiction built worlds
you could live in for the length of a book. This is an attempt to build one you can leave running
in the background for a year — the *spirit* of the genre, never its property.

---

## 3. Core principles

**A world that keeps its own time.** Events are scheduled in advance and happen whether anyone is
listening. Some are delayed. Some are cancelled. Stories run for weeks and resolve. A year on,
somebody mentions the fire. This is the whole product; everything else is delivery.

**Tribute, never derivative.** No existing franchises, characters, trademarks or living authors'
creations. An original world, in the spirit of the genre. This is a hard rule with a screening
process behind it, not an aspiration.

**Fiction that never pretends.** The news is shaped like news, so the station states plainly and
hourly that it is invented and machine-made. Disclosure is a design feature, placed where it
belongs — not a legal cost minimised in a footer.

**Built like radio, not like a podcast.** Programmes are running orders of short items — a link, a
two-minute report, a four-minute interview, a vox pop — not long conversations. Nothing runs past
half an hour. Most items have one voice. This is not a stylistic preference; it is the difference
between something you can leave on and something you switch off at minute six.

**Presenters, not narrators.** A host who links, hedges, trails off, gets things slightly wrong and
has running private business. Correspondents who report. Ordinary people from the settlements who
turn up for twenty seconds in a vox pop and are never heard from again. Each recurring voice speaks
differently from the others, and the same way next week as this week.

**Small on purpose.** One Mac mini in a flat in Kraków, a €11-a-month server, and a nightly batch.
No data centre, no per-word bill, no dependency on anyone's API pricing. That constraint is not a
compromise; it is what makes the station able to run for years.

**Nothing waits for a human.** The operator can be asleep, travelling, or bored for a month. The
station broadcasts anyway. Anything that would block on a person is designed out.

**Open.** The code is public. The build is documented as it happens.

---

## 4. What a listener actually gets

You open a page or a YouTube stream. Audio is already playing — you have joined something in
progress.

**On the hour**, a bulletin: the time, four to six stories from the settlements, what is coming
later today, and the statement that this is a fictional AI-generated broadcast.

**Between the hours**, a programme with a shape. The morning magazine opens with the host, goes to a
correspondent for two minutes on the tariff vote, runs a five-minute interview with someone affected
by it, plays ninety seconds of settlement voices reacting, reads a letter, and hands back to the
newsroom. In the afternoon, a chart with real movement — the one music programme of the day. Late
at night the music returns properly: a show whose host knows which label released the record, then
one long piece — a label retrospective, an artist profile, the story of an album.

**If you come back tomorrow**, the story has moved. If you come back in a month, some of it has
resolved and something else has started. If you want to catch up without listening, there is a page
that tells you what is going on in the world right now, written in-world.

**The station is always on.** There is no dead air, ever, by design.

---

## 5. What's on air

| | |
|---|---|
| **Hourly bulletin** | 2–4 min, on the hour, all 24 hours. Four to six stories, the clock, the disclosure. One newsreader, proper broadcast register — no hedging, no banter |
| **Magazine** | 28 or 56 min. One host linking six to eight short items: reports, a correspondent two-way, an interview, a vox pop, a letter. The default talk format |
| **Interview** | 28 min with one figure from the world |
| **Discussion** | 28 min, host plus two or three voices who disagree |
| **Feature** | 28 or 56 min, one narrator, documentary shape. Timeless, and the backbone of the overnight |
| **Music shows** | Overnight only. Original music with hosts who know the discography — artists, labels, years, who played on what |
| **The chart** | Weekly, with real movement derived from actual airplay, not invented |
| **Specialist shows** | Label retrospectives, artist profiles, single-album stories. Timeless by design |
| **Overnight** | Archive, long-form and music, with the hourly bulletin still fresh |
| **The world page** | A readable digest of what is happening — the story surface for people who won't listen for hours |
| **The discography** | A browsable encyclopedia of the world's music: artists, albums, credits |

---

## 6. Who it's for

Honestly: this is a small, specific audience, and pretending otherwise would produce a worse
product.

**Primary — science-fiction readers who want ambience with substance.** People who read Le Guin,
Robinson, Chiang, Tchaikovsky. They already enjoy sitting inside a world for hours and are the
people most likely to notice, and care, that the convoy came back.

**Secondary — worldbuilders and tabletop people.** A setting that generates its own history daily is
directly useful to them, and they are the audience most likely to go deep on the world page and the
discography rather than the audio.

**Third — background listeners who want an alternative to lofi.** Something with a pulse and a
sense of place to leave on while working. This is likely the largest group by hours listened and the
least engaged by story.

**Fourth — people interested in how it's made.** Builders, AI-curious readers, journalists. They
come for the making-of and some stay for the station. The public repo serves them.

**Explicitly not for:** anyone looking for real news, music discovery, or something to talk to. It
is not interactive and there is no plan for it to be.

---

## 7. What this is not

- **Not a chatbot or an assistant.** You listen; you do not talk to it.
- **Not a music service.** The music exists to furnish a world, not to be discovered.
- **Not a podcast.** Podcasts are on-demand and complete. This is continuous and you join it late.
- **Not a news source**, and it says so every hour.
- **Not a demo of AI capability.** If the only interesting thing about it is that a machine made it,
  it has failed.
- **Not a platform.** One station, one world. A second station is a someday, not a plan.

---

## 8. Milestones

Phrased as what a listener could experience, not as engineering steps.

**M0 — It exists.** A stream that never dies, playing placeholder audio on a loop. Nobody is
listening but the URL is real and the clock is right. *This is the milestone the previous attempt
never reached in two months of building, and reaching it is the point.*

**M1 — It sounds like a station.** One real magazine with a proper running order, one real bulletin,
imaging and music around them. Judged by one question, in one sitting: would you leave it playing while someone else was in
the room?

**M2 — It runs itself.** A full day generated overnight and broadcast without intervention. The
operator sleeps through it. The world moves during the day.

**M3 — It's legal and it's public.** Disclosure package complete, lawyer signed off, the site up.
The stream is listed. Anyone can listen.

**M4 — It has a memory.** Ninety days on air. Stories that started in month one have resolved.
Presenters refer back to things. The overnight block has begun to fill with the station's own
retired programmes rather than the pool built before launch.

**M5 — It has regulars.** Not many. People who return, notice when a story moves, and know which
presenter they prefer. That is the real finish line and it is the only one that can't be engineered.

---

## 9. How we'll know it's working

The wrong metrics are obvious and tempting: listener counts, hours streamed, GitHub stars.

The right ones are harder and fewer:

- **Return listening.** Does anyone come back on a different day? One returning listener means more
  than a thousand who arrived from a link once.
- **Does the world feel alive to its own operator at 90 days?** If the person who built it stops
  finding the rundown interesting, no listener will.
- **Can you tell the presenters apart** with the names stripped off?
- **Time in stream.** Ambient media lives or dies on whether it survives the first four minutes.
- **Cost per broadcast day stays near zero.** The moment it doesn't, the project has a shelf life.

Quality is judged by ear, by one person, on a blind sample. Nothing automated grades it.

---

## 10. Sustainability

Running costs are electricity, a €11 server and a domain — deliberately small enough that the
station's survival never depends on anyone's goodwill or funding round.

Beyond that: a Ko-fi for listeners who want to contribute, and infrastructure or credit grants where
they fit. No advertising, no sponsorship reading, no paywall on the stream. If it can't run on
roughly the cost of a coffee a week, the design is wrong.

---

## 11. The honest risks

**The writing might not be good enough.** A local model on a small machine writing broadcast dialogue
is the single unproven assumption. A cheap version of the test — one hand-written 20-minute
two-hander, no pipeline — runs in week one; the real measurement, on retrieved context, lands a few
weeks later. If it fails,
the choices are better hardware or a small paid budget for the flagship shows — not more
architecture.

**The voices might be too flat.** Expressive speech synthesis running locally is at the edge of what
the hardware allows. If the cast engine fails mid-batch the station keeps broadcasting on a
plainer fallback voice and marks the day degraded, because silence is worse than flatness — but
that is a failure mode, not a plan. The plan, if the voices are simply not good enough, is fewer
fresh hours.

**The audience might be very small.** Accepted. The station is built to cost almost nothing precisely
so that a small audience is survivable.

**The regulatory picture is live.** EU transparency rules for AI-generated content apply from
2 August 2026 and the guidance is still settling. The disclosure design is deliberately more thorough than the
minimum, and reviewed by a lawyer before anyone can listen.

**The operator might get bored.** The most likely failure of all, and the reason the station is built
to keep broadcasting without him — and the reason the daily rundown exists, so there is something to
read each morning that is about the world rather than the code.
