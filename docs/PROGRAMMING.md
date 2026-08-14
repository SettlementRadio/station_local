# Settlement Radio — Programming

*The editorial reference. What subjects the station covers, which format each is best served by,
when it airs, and who presents it. This is the input to `grid.yaml`.*

> **Ownership:** the operator's, like canon. Agents read this **only** when working a grid or
> showrunner task. It is reference material, not process documentation, and it generates no tasks.

---

## 1. The organising principle: clock speed

A subject does not map to a format. It maps to a **rate of change**, and the rate of change decides
almost everything else — the format, the daypart, whether it can carry a daily programme, and how
much of its context comes from the living world versus the static bible.

| Speed | Domains | Changes | Native shape |
|---|---|---|---|
| **Fast** | politics · finance · sport · conflict | daily | Reports, two-ways, bulletins, magazines. Perishable |
| **Medium** | crime · technology · health · celebrity · fashion · music (catalogue) | weekly | Explainers, reviews, interviews, profiles |
| **Slow** | history · religion · art · culture · music (heritage) | rarely | Features, essays, documentaries. Evergreen |

**Every domain sits in exactly one of the three**, because the speed picks the `context_mix` and
there is no ratio for "slow-medium". Where a domain has two speeds it is because it has two bodies
of material — music is the only one, and it is split explicitly: the catalogue is medium, the
heritage is slow, and the two are different programmes. The per-domain entries in §3 carry the same
label as this table; if they ever disagree, this table is the one that is wrong, because §3 is where
the editorial thinking happens.

Three things fall straight out of this, and they line up exactly with the architecture:

**Fast domains are daytime and perishable.** They belong in bulletins and magazines, they reference
the clock through their surrounding links, and they are worthless a week later.

**Slow domains are the overnight block.** A feature on the founding of Cold Harbor is as good in
March as in January. Slow domains are therefore *time-neutral by construction* — the floating class
— which makes them the cheapest content to make, the safest to repeat, and the natural backbone of
01:00–07:00 and the pre-built archive.

**The context mix follows the speed.** A politics programme is mostly world state with a little
canon; a history programme is mostly canon with a little world. This is a per-programme parameter
(`context_mix` in `grid.yaml`), not a global setting, and getting it wrong is the most common way a
programme comes out flat:

| Speed | canon : world |
|---|---|
| Fast | 30 : 70 |
| Medium | 50 : 50 |
| Slow | 80 : 20 |

---

## 2. The second axis: treatment

Within a domain, the same material supports different treatments. This is the "informational versus
discussion" distinction, made usable:

| Treatment | What it is | Typical items |
|---|---|---|
| **Report** | What happened | `bulletin_story`, `two_way`, `package` |
| **Analysis** | What it means | `two_way`, `interview`, `talk` |
| **Discussion** | Who disagrees and why | `discussion`, `vox` |
| **Narrative** | The story told properly | `feature`, `package` |
| **Review** | Judgement on a work or event | `talk`, `interview` |

Time decides which is available. Five minutes gets a report. Twenty minutes gets a discussion. Half
an hour gets narrative. A domain with only five minutes of material does not get a programme; it
gets an item inside one.

---

## 3. The domains

Each entry: what it covers in-world, its best formats, where it sits, and its trap.

**This list is canonical — seventeen domains, and nothing may invent an eighteenth.**
`facts.domain`, `domain_floor`, the 12-per-domain diversity cap and the Tier 1 canon summaries all
key off it. Fourteen carry a **strand of their own**; three do not, and appear only as items inside
other programmes and as seats in a `domain_floor`: **logistics**, **geography**, **peoples**. That
is why `Early Watch` can be `logistics · religion` without owning a logistics strand — it is a
supply-and-recap magazine, not "the logistics programme". Canon's older names map on — `war` →
`conflict`, `tech` → `technology`. `news` and `weather` are **programme types, not domains**: a
bulletin's domain is whatever the bulletin is about.

### Politics — fast
Council votes, tariffs, appointments, factional manoeuvre, settlement autonomy.
**Formats:** bulletin story · two-way with a political correspondent · 8–15 min discussion · 10 min
interview. **Feature form:** the anatomy of a decision, months later.
**Daypart:** morning magazine, evening magazine. **Trap:** all process, no consequence. Every
political item must reach someone it affects.

### Finance — fast
Tariffs, shortages, freight rates, labour disputes, the relay economy, a label folding.
**Formats:** short market/supply report · analysis two-way · weekly round-up.
**Daypart:** early morning and end of trading. **Trap:** abstraction. Prices are people's rent.

### Sport — fast
Ice racing, relay-run, settlement leagues, results, transfers, rivalries.
**Formats:** results item · preview/review two-way · 25 min weekly round-up · athlete interview.
**Feature form:** a rivalry's history, a career.
**Daypart:** afternoon and weekend. **Trap:** invented results are meaningless unless a standings
table persists. Sport needs its own continuity or it is noise.

### Conflict and military — fast, sensitive
Border disputes, blockades, patrol incidents, veterans, the aftermath of the old war.
**Formats:** correspondent dispatch (`package`) · analysis two-way · veteran interview.
**Feature form:** an oral history.
**Daypart:** evening magazine. **Trap:** spectacle. Cover consequence and cost, never hardware or
tactics. Nothing here should read as thrilling.

### Crime — medium, sensitive
*(the report is perishable; the case narrative is not, which is why the domain sits at medium)*
Inquiries, tribunals, smuggling, salvage disputes, fraud.
**Formats:** court/inquiry report · 25 min case narrative · interview with an investigator.
**Daypart:** the report is daytime; the case narrative is **night** — the long-form true-crime shape
suits the overnight block. **Trap:** no method detail, no glorification, no victims used as colour.

### Technology — medium
Relay engineering, life support, salvage, agriculture, failures and fixes.
**Formats:** explainer `talk` · builder interview · review · 25 min feature on a system.
**Daypart:** midday and evening. **Trap:** specification lists. Technology is interesting when it
breaks or changes what someone can do.

### Health — medium, sensitive
Recycled-air conditions, low-gravity medicine, outbreaks, public information, clinic access.
**Formats:** explainer · clinician interview · public information item.
**Daypart:** midday. **Trap:** this is fiction and must never read as actionable medical advice.
In-world conditions and in-world treatments only.

### Art — slow
Sculpture in low gravity, light works, muralists, station architecture.
**Formats:** review · artist profile · 25 min feature · essay.
**Daypart:** evening and night. **Trap:** describing visual work on radio. Talk about the maker, the
argument and the room, not the image.

### Culture — slow
Customs, food, language drift, festivals, generational difference, life aboard.
**Formats:** magazine item · vox pop · essay · 25 min feature.
**Daypart:** midday and evening. **Trap:** anthropological tone. Culture is what people do without
noticing.

### History — slow
The migration, the founding, the old war, lost settlements, Earth as memory.
**Formats:** **documentary feature** (the strongest format on the station) · essay · anniversary
item · archive interview.
**Daypart:** **overnight backbone**, plus an anniversary item in daytime bulletins.
**Trap:** none, really. This is the format the world is best suited to. Make more of it than feels
necessary — it is also the cheapest and the most reusable.

### Religion — slow
Faiths formed in transit, observances, doubt, chaplaincy, dispute between traditions.
**Formats:** 3–5 min reflection · interview · essay · observance item.
**Daypart:** **early morning (05–07) and late night** — exactly where real radio puts it, because it
suits the hour and the audience awake at it. **Trap:** advocacy or mockery. Report belief as
practice.

### Celebrity — medium, light
Musicians, racers, presenters, officials with reputations; feuds, appearances, gossip.
**Formats:** light magazine item · interview · chart adjacency.
**Daypart:** afternoon. **Trap:** in-world figures only, always. This is also the domain where the
station's own presenters can appear as subjects, which is one of the cheapest ways to make the
station feel real.

### Fashion and style — medium
What people wear in a place with fabric scarcity, salvage aesthetics, uniform, status.
**Formats:** light magazine item · designer profile · essay.
**Daypart:** afternoon and weekend. **Trap:** it only works when tied to material constraint. Style
under scarcity is interesting; style in the abstract is not.

### Music — fast catalogue, slow heritage
New releases, the chart, labels, scenes, session players, the old recordings.
**Formats:** music show · chart · **specialist retrospective** · artist profile.
**Daypart:** night for the retrospectives; the chart is the only daytime music (§7). **Trap:**
covered in ARCHITECTURE §8. Rotation and separation rules, not random selection.

---

## 4. The day

*Dayparts and their character. This is the shape, not the schedule — §8 is the actual clock, hour
by hour, with every minute accounted for.*

| Daypart | Character | Domains |
|---|---|---|
| **05:00–07:00** Early | Quiet, slow, one voice | religion · reflection · weather · overnight recap |
| **07:00–11:00** Morning | Fast, informational | politics · finance · sport · technology |
| **11:00–14:00** Midday | Explanatory | culture · health · technology · a lighter magazine |
| **14:00–17:00** Afternoon | Lighter talk, the chart | music (chart) · sport · fashion · celebrity |
| **17:00–21:00** Evening | Considered | politics · conflict · discussion · art |
| **21:00–01:00** Night | Long-form, reflective | religion · essay · analysis · music heritage |
| **01:00–05:00** Overnight | Archive and narrative | **history** · crime narrative · features · music |

Fresh generation goes where listeners are (morning and evening). The overnight is slow-domain
material that stays good, which is why it can be pre-built months ahead and reused — and it is the
only part of the day where music leads.

---

## 5. Presenters and beats

The question of "who delivers it" has two halves, and only the first is obvious.

### Strand hosts

Each recurring programme has **one regular host**. The host is the strand — listeners attach to a
voice and a time, not to a format. A host may present more than one programme but should not present
across dayparts, or the station loses its shape.

Hosts are `cast` members with authored `conversational` speech profiles (ARCHITECTURE §11a). A host
may carry several strands **within one daypart** — that is normal radio, and it is what makes a
roster of five cover a grid of twenty-odd strands. The full station needs about five: a morning
host, an evening host, a music host, a night voice, and a newsreader with a `scripted` profile.
Launch needs three or four (ARCHITECTURE §35 C2); the roster grows with the freshness tier.

### Beat correspondents — the thing that makes it feel like an institution

**A correspondent belongs to a domain, not a programme**, and appears wherever that domain does. The
same political correspondent does the two-way in the morning magazine, is quoted in the bulletin,
and presents the weekly politics discussion. That recurrence across contexts is most of what makes a
station feel like an organisation rather than a set of unrelated shows.

`cast.beat` names the domain. Five or six correspondents covers the station: politics/finance,
conflict, sport, science/technology/health, culture/art, music.

Correspondents use the **`scripted`** register — they are reporting, not chatting — even when
answering a host's question in a two-way.

### Everyone else

Interviewees, panellists and vox-pop voices are `figures`, not cast. They draw a stock voice on
first appearance and keep it forever (ARCHITECTURE §3). They are allowed to sound ordinary; the
distinctiveness rules apply to presenters only.

### The pattern in practice

A tariff vote produces: a bulletin story read by the newsreader → a two-way between the morning host
and the political correspondent → a five-minute interview with a freight operator → a vox pop from
the market → an evening discussion with three figures → and, three months later, a 25-minute feature
narrated by the same correspondent. **One event, six formats, four domains touched, and every voice
recurring.**

---

## 6. Editorial guardrails

Four domains carry standing constraints, enforced by the safety gate (ARCHITECTURE §19) and worth
stating as editorial policy rather than filtering:

- **Conflict** — consequence and cost, never hardware, tactics or spectacle.
- **Crime** — no method detail, no glorification, victims are people not colour.
- **Health** — in-world conditions and treatments only; nothing that reads as actionable advice.
- **Religion** — belief reported as practice; neither advocacy nor mockery.

And one that applies everywhere: **every domain must reach a person.** A tariff is a rent rise. A
patrol incident is somebody's brother. A relay failure is a missed funeral. The domain is the
subject; the person is the story.

---

## 7. The clock

Built on the BBC World Service pattern, which is the closest real model to what this station is:

```
:00  NEWS — 4 min, dedicated newsreader, its own sting          ← every hour, no exceptions
:04  PROGRAMME — 56 min (to :00), or 28 min (to :32)
:32  PROGRAMME — 28 min (to :00), in hours running two
```

**Three slot lengths only: 4, 28 and 56.** Every hour closes on the minute — `4 + 56` or
`4 + 28 + 28` — and because `56 = 2 × 28`, a long programme is exactly two acts of a short one and
the mixer never needs a special case. Radio 4 uses 15 / 30 / 45 / 60 with news at the top of every
hour; the World Service uses a five-minute bulletin at `:00` and programmes from `:06`. This station
takes the World Service clock and Radio 4's discipline of **fixtures** — the same programme, at the
same time, every weekday. That is what makes a schedule learnable, and being learnable is what makes
someone come back.

**The junction is always four minutes; its content is not always four minutes of speech.** A daytime
bulletin runs four to six stories and fills the slot. The four overnight junctions — **01:00, 02:00,
03:00 and 04:00** — carry a summary instead: the clock, a recap, the disclosure, roughly two minutes
of speech in the same four-minute slot, with imaging and a bed carrying the rest. The 05:00 junction
is a full bulletin again. The slot never varies; the writing does. This is why the capacity line in
§9 reads `20 × 4 + 4 × 2 = 88` against 24 identical slots.

**No music sequences.** This is a speech station. The only music programme in the daytime is the
chart, and it is weekly. Music returns overnight, where it belongs.

---

## 8. The grid

**One clock, seven days** (`DECISIONS.md` D-001). The hour skeleton is identical every day of the
week: the same junction at `:00`, the same slot lengths, the same daypart character. Only the
*occupant* of a slot and its *freshness* vary by day.

**Slot lengths are day-invariant.** A 56-minute weekend programme may not sit in an hour that runs
`4 + 28 + 28` on weekdays. This is the constraint that makes one clock possible, and it is what
`grid-sync` validation 5 checks once instead of three times.

The weekend is still lighter — because **lightness is a freshness property, not a clock property**.
The 17:04 slot holds a fresh flagship on Monday and a repeat on Sunday. Twelve slots carry weekend
overrides; everything else is identical all week.

`F` = fresh daily · `W` = fresh weekly · `A` = archive, generated far in advance ·
`R` = a repeat of a `W` edition aired earlier, billed as a repeat on air.

The **`Type`** column carries a legal `programme_type` from ARCHITECTURE §11 and nothing else, so
`grid.yaml` can be written from this table directly (D-005).

### The clock, Monday to Friday

| Time | Programme | Min | Domain | Type | Pace | Fresh |
|---|---|---|---|---|---|---|
| **05:00** | **NEWS** | 4 | — | bulletin | — | F |
| 05:04 | **Early Watch** — overnight recap, supply, weather; closes with **Reflection** | 28 | logistics · religion | magazine | slow | F |
| 05:32 | **The Long Record** — history documentary | 28 | history | feature | slow | A |
| **06:00** | **NEWS** | 4 | — | bulletin | brisk | F |
| 06:04 | **First Shift** — the breakfast strand, part 1 | 56 | politics · finance | magazine | fast | F |
| **07:00** | **NEWS** | 4 | | bulletin | | F |
| 07:04 | **First Shift** — part 2 | 56 | politics · sport · culture | magazine | fast | F |
| **08:00** | **NEWS** | 4 | | bulletin | | F |
| 08:04 | **First Shift** — part 3 | 56 | politics · technology | magazine | fast | F |
| **09:00** | **NEWS** | 4 | | bulletin | | F |
| 09:04 | **The Long Question** — one guest, one subject | 28 | rotating | interview_programme | measured | F |
| 09:32 | **Relay** (M/W/F) · **Body & Air** (Tu/Th) | 28 | technology · health | magazine | measured | W |
| **10:00** | **NEWS** | 4 | | bulletin | | F |
| 10:04 | **The Common Table** — life aboard, customs, food, language | 56 | culture | magazine | warm | W |
| **11:00** | **NEWS** | 4 | | bulletin | | F |
| 11:04 | **Ledger** — tariffs, freight, labour, scarcity | 28 | finance | newsreel | brisk | F |
| 11:32 | **Dispatch** — from the borders and the patrol lines | 28 | conflict | newsreel | grave | W |
| **12:00** | **NEWS** | 4 | | bulletin | | F |
| 12:04 | **The Midday Report** — second news pillar of the day | 56 | politics · conflict | magazine | fast | F |
| **13:00** | **NEWS** | 4 | | bulletin | | F |
| 13:04 | **The Bench** — inquiries, tribunals, salvage disputes | 28 | crime | feature | measured | W |
| 13:32 | **Vantage** — a single voice, a single argument | 28 | rotating | feature | slow | A |
| **14:00** | **NEWS** | 4 | | bulletin | | F |
| 14:04 | **The Count** *(Fri)* — the chart, 20 down, most-played · **Dispatch** *(Mon–Thu)* | 28 | music · conflict | chart · newsreel | bright | W · R |
| 14:32 | **Cut** — dress, salvage, status, scarcity | 28 | fashion | magazine | light | A |
| **15:00** | **NEWS** | 4 | | bulletin | | F |
| 15:04 | **Ice & Iron** — results, standings, the racing | 28 | sport | newsreel | fast | F |
| 15:32 | **Relay** · **Body & Air** *(repeat of 09:32)* | 28 | technology · health | magazine | measured | R |
| **16:00** | **NEWS** | 4 | | bulletin | | F |
| 16:04 | **The Gallery** — makers, light works, station architecture | 28 | art | magazine | measured | A |
| 16:32 | **Names** — who is being talked about, and why | 28 | celebrity | magazine | light | A |
| **17:00** | **NEWS** | 4 | | bulletin | | F |
| 17:04 | **The Evening Report** — the flagship | 56 | politics · conflict | magazine | fast | F |
| **18:00** | **NEWS** | 4 | | bulletin | | F |
| 18:04 | **The Six** — the main news programme of the day | 28 | politics · conflict | news_programme | grave | F |
| 18:32 | **Crossfire** — three voices who disagree | 28 | politics | discussion | fast | F |
| **19:00** | **NEWS** | 4 | | bulletin | | F |
| 19:04 | **Assembly** — the council, the factions, the manoeuvre | 56 | politics | discussion | measured | W |
| **20:00** | **NEWS** | 4 | | bulletin | | F |
| 20:04 | **The Documentary** — the station's long-form strand | 56 | rotating | feature | slow | W |
| **21:00** | **NEWS** | 4 | | bulletin | | F |
| 21:04 | **Faith in Transit** | 28 | religion | magazine | slow | A |
| 21:32 | **The Bench** *(repeat of 13:04)* | 28 | crime | feature | measured | R |
| **22:00** | **NEWS** | 4 | | bulletin | | F |
| 22:04 | **The Late Report** — the day analysed, not repeated | 56 | politics · conflict | newsreel | measured | F |
| **23:00** | **NEWS** | 4 | | bulletin | | F |
| 23:04 | **Night Record** — heritage music, one label or one year | 56 | music | music_show | slow | A |
| **00:00** | **NEWS** | 4 | | bulletin | | F |
| 00:04 | **The Midnight Report** | 28 | politics · conflict | news_programme | grave | F |
| 00:32 | **The Long Record** — history documentary | 28 | history | feature | slow | A |
| **01:00** | **SUMMARY** | 4 | — | bulletin | — | F |
| 01:04 | **The Night Watch** — documentary or essay | 56 | history · art · culture | feature | slow | A |
| **02:00** | **SUMMARY** | 4 | | bulletin | | F |
| 02:04 | **The Night Watch** — label retrospective, artist profile, album story | 56 | music | music_show | slow | A |
| **03:00** | **SUMMARY** | 4 | | bulletin | | F |
| 03:04 | **The Night Watch** — specialist music | 56 | music | music_show | slow | A |
| **04:00** | **SUMMARY** | 4 | | bulletin | | F |
| 04:04 | **The Night Watch** — music to the hour | 56 | music | music_sequence | slow | A |

Every hour is `4 + 56` or `4 + 28 + 28`; every hour sums to 60; the day sums to 1,440. Twenty of the
junctions are full bulletins and four (01:00–04:00) are 2-minute summaries in the same 4-minute
slot (§7).

**Reflection is an item, not a slot.** At five minutes it was never a programme; it closes
`Early Watch`, which is where a reflective piece belongs in a 05:00 hour anyway.

**The Night Watch is music-led in three of its four hours.** This is a cost decision, not a taste
one: a talk archive hour costs ~42 speech-minutes to build, a music-led one ~6, and the archive pool
is the most expensive single thing the station has to make (§9, `DECISIONS.md` D-003).
`music_sequence` is legal here and nowhere else.

### Weekend overrides

Twelve slots differ. Everything not listed is identical to Monday–Friday.

| Slot | Mon–Fri | Saturday | Sunday |
|---|---|---|---|
| 06:04 | First Shift 1 | **Sixth Day** — lighter breakfast, 56, `F` | **Sixth Day**, `F` |
| 07:04 | First Shift 2 | The Common Table `R` | The Common Table `R` |
| 08:04 | First Shift 3 | archive feature `A` | archive feature `A` |
| 09:04 | The Long Question | archive interview `A` | **Observance** — religion, `A` |
| 09:32 | Relay · Body & Air | archive `A` | archive `A` |
| 10:04 | The Common Table | archive feature `A` | archive feature `A` |
| 11:04 | Ledger | archive `A` | archive `A` |
| 12:04 | The Midday Report | **The Week in Ice** — sport round-up, 56, `W` | The Week in Ice `R` |
| 14:04 | The Count · Dispatch | The Count `R` — Friday's countdown, billed as a repeat | archive `A` |
| 15:32 | Relay · Body & Air repeat | archive `A` | archive `A` |
| 18:32 | Crossfire | archive `A` | archive `A` |
| 22:04 | The Late Report | archive feature `A` | archive feature `A` |

`Assembly` (19:04) and `The Documentary` (20:04) keep their slots all week and air as `R` at the
weekend; `Dispatch` (11:32) and `The Bench` (13:04) do the same. `Ice & Iron` stays fresh on both
weekend days — sport belongs to the weekend (§3). The junctions, `The Evening Report`, `The Six` and
`The Midnight Report` never vary.

Sunday is the quietest day: it carries one fewer `W` slot than Saturday and no chart.

### The weekly strands and where they repeat

Validation 9 requires every `W` programme to declare a `production_day` and at least one
`repeat_slot`. Production nights are two days ahead of first air (the D+2 rule, ARCHITECTURE §14),
and no night carries more than two.

| Strand | Min | Fresh | Repeats | Airings/wk | Produced |
|---|---|---|---|---|---|
| Relay | 28 | Mon 09:32 | Wed · Fri 09:32 · same-day 15:32 | 6 | Sat night |
| Body & Air | 28 | Tue 09:32 | Thu 09:32 · same-day 15:32 | 4 | Sun night |
| Dispatch | 28 | Mon 11:32 | 11:32 Tue–Sun · 14:04 Mon–Thu | 6 | Sat night |
| The Bench | 28 | Tue 13:04 | 13:04 daily · 21:32 daily | 6 | Sun night |
| The Common Table | 56 | Wed 10:04 | 07:04 Sat · Sun | 3 | Mon night |
| Assembly | 56 | Thu 19:04 | 19:04 daily | 5 | Tue night |
| The Documentary | 56 | Fri 20:04 | 20:04 daily | 5 | Wed night |
| The Week in Ice | 56 | Sat 12:04 | Sun 12:04 | 2 | Thu night |
| The Count | 28 | Fri 14:04 | Sat 14:04 | 2 | Wed night |

**`The Count` is `W`, not `F`.** It is produced once a week and repeats — which is the definition of
a weekly strand — and the Saturday airing is Friday's audio, billed as a repeat. It is not a second,
longer edition: the chart computes 40 positions but 40 will not fit 28 minutes, so Saturday reruns
the same top 20 (ARCHITECTURE §8).

Production nights: Sat 2 · Sun 2 · Mon 1 · Tue 1 · Wed 2 · Thu 1 · Fri 0 — all within the cap, and
weighted onto the two weekend nights, which is exactly the render slack the lighter weekend creates.

**Nine strands, 364 minutes of production a week.** `Relay` and `Body & Air` share the 09:32 slot
but are two separate productions, which is easy to miscount as one and was, in the version of this
table before `DECISIONS.md` D-002.

**Repeat count is editorial, not architectural** (D-002). A `W` edition costs its production night
once whether it airs twice or six times; a further airing costs only audible repetition. Same-day
double-runs — `Relay` at 09:32 and 15:32, `Dispatch` at 11:32 and 14:04 — are standard practice for
explainer and dispatch strands.

---

## 9. Does it fit — and what to cut

**This grid is a full BBC-style speech station and it costs far more than a Mac mini can render.**
Saying so plainly is the point; the previous version of this section hid the problem by filling the
day with music, which quietly turned the product into something else.

Speech is ~75% of a talk slot; the rest is imaging, beds and links.

**A weekday**, in aired slot minutes, which must sum to 1,440:

| | Slot min | Speech |
|---|---|---|
| 24 × 4-min junctions (20 bulletins + 4 overnight summaries) | 96 | 88 |
| Fresh `F` programmes as listed | 532 | ~399 |
| Weekly `W` editions aired | 252 | 0 |
| Repeats `R` | 84 | 0 |
| Archive `A` | 476 | 0 |
| **Total slot minutes** | **1,440** | |
| *plus* `W` production amortised across the week — 364 min/wk = 52 slot min/day | | ~39 |
| **Fresh speech, weekday** | | **~526 min** |

Airings cost nothing; **only production costs render time**, which is why the `W` and `R` rows carry
zero and the amortised production line carries 27.

**A weekend day** is the same 1,440 minutes with twelve slots overridden. `F` falls from 532 to 224
slot minutes and archive rises to 784 (Sat) / 812 (Sun):

| | Weekday | Saturday | Sunday |
|---|---|---|---|
| Fresh speech | ~526 min | ~295 min | ~295 min |
| Archive consumed | 7.9 h | 13.1 h | 13.5 h |

Across the week that averages **~460 fresh speech-minutes and ~9.5 archive hours per day**. The
second number is the expensive one and it is what sets the archive pool at 135 hours
(`DECISIONS.md` D-003) — lightness at the weekend is bought with archive, not for free.

Against ~216 usable minutes at RTF 0.7× (ARCHITECTURE §36). **A weekday is roughly two and a half
times the budget**, the week as a whole a little over two. So it is built in tiers, and the tier is
a capacity decision, not an editorial one:

| Capacity | What goes fresh |
|---|---|
| **~200 min** (RTF 0.7) | All junctions · `First Shift` cut to one hour · `The Evening Report` · `The Six` · `The Count` · everything else weekly or archive |
| **~300 min** (RTF 1.0) | Add `The Midday Report`, `Ledger`, `Ice & Iron`, `The Midnight Report` |
| **~460 min** (RTF 1.5) | Add `First Shift` full 3 hours, `The Late Report`, `Crossfire`, `The Long Question` |
| **~526 min** | The weekday as written |

Every tier costs less at the weekend, because the weekend overrides bite first: at the ~200 tier a
Saturday runs on junctions, `Sixth Day`, `The Evening Report` and `The Six` alone.

**These numbers are fresh speech only — the archive still has to be fed.** ARCHITECTURE §14 puts
steady-state archive top-up at ~30 speech-min/day, which comes out of the same nightly budget, so
each tier above is about 30 minutes more expensive than it looks (216 usable against ~200,
308 against ~300, 462 against ~460). Retired daytime programmes refill the pool for free after 30
days and probably cover most of it, but only the time-neutral ones survive the staleness rule, and
nobody knows that fraction until the station has run. **Choose the tier one notch below what the
measured RTF appears to buy**, and relax it when the digest shows what retirement actually
contributes.

**Repeats are not a compromise, they are how radio works.** The BBC repeats constantly — Radio 4
Extra is an entire station of it, and the World Service reruns its documentary strands several times
a week across time zones. A `W` programme aired Tuesday at 09:30 and again Thursday at 21:30 is
normal practice, not a shortfall, and it should be billed on air as a repeat.

**The cut order, if capacity falls short of the tier you are on.** Each step costs a listener less
than the one before:

1. Move an `F` programme to `W` with declared repeat slots — the cheapest cut there is, and the one
   the listener notices least, because a repeat is announced rather than hidden.
2. Move a `W` programme to fortnightly.
3. Shorten a 56-minute programme to 28 — it is already two acts, so this is dropping one.
4. Move `The Documentary` permanently to archive.

**Extending the overnight archive block is not on this ladder**, though it looks like it belongs.
It buys fresh render minutes by spending archive hours, and archive hours are the scarcer resource
(§9, `DECISIONS.md` D-003). Reach for it only when the pool is above target.

**Never cut**: the hourly junction, `The Evening Report`, or — from week three, when
`requires_airplay_days: 21` first allows it on air — `The Count`. Those three are the station's
identity: the clock, the flagship, and the one thing that is fun.

---

## 10. Programme metadata

These are the **editorial** fields — the ones this document owns and a schedule cannot be built
without. ARCHITECTURE §17a holds the full `grid.yaml` schema, which adds the mechanical fields
(`slot_minutes`, `format_class`, `register_kind`, `max_lead_hours`, `schedule`, `hour_clock`).

| Field | Example |
|---|---|
| **Jingle set** | `open`, `close`, `bed`, and for news a `sting`. One identity per strand — this is the single cheapest way to make a schedule feel like a station, and it is a one-off render |
| **Pace** | fast · brisk · measured · warm · light · slow · grave. Sets link length, item count and the emotion band |
| **Presenter** | one strand host, plus the beat correspondents who appear inside it (§5) |
| **Domain floor + context mix** | retrieval seats and the canon : world ratio (§1) |
| **Item mix** | the running order shape (ARCHITECTURE §11) |
| **Freshness** | `F` daily · `W` weekly with repeats · `A` archive |
| **Days** | which days the strand occupies its slot, and where its repeats land (§8) |

---

## 11. How to grow this

Start with four, not thirty. The rest of the day runs on repeats and archive, which is exactly what
a new speech station does — the World Service reruns its strands several times a week and nobody
considers it a placeholder.

Four to build first: **the hourly bulletin** (the spine, and the thing that makes it a station),
**The Evening Report** (the flagship magazine), **The Count** (the chart), and **The Long Record**
(one history documentary for the archive). They cover the three clock speeds, the three context mixes and the three
presenter roles, and they will tell you more about what works than a full grid of untested formats.

**Build all four early; air `The Count` last.** `requires_airplay_days: 21` keeps the chart off air
until three weeks of real airplay exist (ARCHITECTURE §8), which is why it is build step 19 rather
than an opening-night programme. Building it early is still right — it is the format that exercises
the discography, and its failure mode is only that it waits.

### `The Count` is a most-played chart, not a new-release chart

**Nothing in the catalogue is dated later than 2624 and the present is 2626**, because the present
is the real year plus six hundred and moves every January while a written release year does not.
A chart of new releases would therefore have nothing to count, and would have less every year.

It counts plays instead. ARCHITECTURE §8 already computes it that way — 45% decayed airplay, 25%
in-world requests, 20% previous position, 10% editorial nudge, and no release-date term anywhere in
the score — so this is a note saying out loud what the score already does, written because
`COMMISSION.md` §5 asked the catalogue for *"≥80 songs current at any time"* and a writer could
read that as a commissioning target for records dated this year. It is not one. **"Current" means
in rotation, not newly released**, and 500 playable songs satisfy it on the day the station opens.

What this costs: a presenter may not say a record is new because it entered the chart. **A new
entry is a record that has started being played**, which is what movement language on a most-played
chart means everywhere — "in at eleven", "up four", "a re-entry after nine weeks" all still work,
and "out this week" does not. The editorial-nudge term is where an actual new release enters the
chart, and it needs a beat behind it (M-15, D-080).

Add a programme only when there is a domain producing more material than its current slot can hold.
An empty programme is worse than no programme, and the world tick's output is the constraint —
never the ambition.
