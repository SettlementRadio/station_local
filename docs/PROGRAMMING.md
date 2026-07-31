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
| **Fast** | politics · finance · sport · conflict · crime | daily | Reports, two-ways, bulletins, magazines. Perishable |
| **Medium** | technology · health · celebs · music (catalogue) · fashion | weekly | Explainers, reviews, interviews, profiles |
| **Slow** | history · religion · art · culture · music (heritage) | rarely | Features, essays, documentaries. Evergreen |

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
key off it. Fourteen carry programmes; three exist only in canon and never do: **logistics**,
**geography**, **peoples**. Canon's older names map on — `war` → `conflict`, `tech` →
`technology`. `news` and `weather` are **programme types, not domains**: a bulletin's domain is
whatever the bulletin is about.

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

### Culture — slow-medium
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

### Fashion and style — slow-medium
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
| **21:00–00:00** Night | Long-form, reflective | religion · essay · analysis · music heritage |
| **00:00–05:00** Overnight | Archive and narrative | **history** · crime narrative · features · religion |

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
bulletin runs four to six stories and fills the slot. Overnight (01:00–05:00) the junction carries a
summary — the clock, a recap, the disclosure — roughly two minutes of speech in the same four-minute
slot, with imaging and a bed carrying the rest. The slot never varies; the writing does. This is why
the capacity line in §9 reads `19 × 4 + 5 × 2` against 24 identical slots.

**No music sequences.** This is a speech station. The only music programme in the daytime is the
chart, and it is weekly. Music returns overnight, where it belongs.

---

## 8. The grid

Every programme the station airs. `F` = fresh daily · `W` = fresh weekly, repeats through the week ·
`A` = archive, generated far in advance.

### Weekday

`R` marks a repeat of a `W` programme aired earlier in the week — billed as a repeat on air.

| Time | Programme | Min | Domain | Format | Pace | Fresh |
|---|---|---|---|---|---|---|
| **05:00** | **NEWS** | 4 | — | bulletin | — | F |
| 05:04 | **Early Watch** — overnight recap, supply, weather; closes with **Reflection** | 28 | logistics · religion | short items | slow | F |
| 05:32 | Music to the hour | 28 | music | sequence | slow | A |
| **06:00** | **NEWS** | 4 | — | bulletin | brisk | F |
| 06:04 | **First Shift** — the breakfast strand, part 1 | 56 | politics · finance | magazine | fast | F |
| **07:00** | **NEWS** | 4 | | | | F |
| 07:04 | **First Shift** — part 2 | 56 | politics · sport · culture | magazine | fast | F |
| **08:00** | **NEWS** | 4 | | | | F |
| 08:04 | **First Shift** — part 3 | 56 | politics · technology | magazine | fast | F |
| **09:00** | **NEWS** | 4 | | | | F |
| 09:04 | **The Long Question** — one guest, one subject | 28 | rotating | interview | measured | F |
| 09:32 | **Relay** (M/W/F) · **Body & Air** (Tu/Th) | 28 | technology · health | explainer | measured | W |
| **10:00** | **NEWS** | 4 | | | | F |
| 10:04 | **The Common Table** — life aboard, customs, food, language | 56 | culture | magazine | warm | W |
| **11:00** | **NEWS** | 4 | | | | F |
| 11:04 | **Ledger** — tariffs, freight, labour, scarcity | 28 | finance | analysis | brisk | F |
| 11:32 | **Dispatch** — from the borders and the patrol lines | 28 | conflict | package + two-way | grave | W |
| **12:00** | **NEWS** | 4 | | | | F |
| 12:04 | **The Midday Report** — second news pillar of the day | 56 | politics · conflict | magazine | fast | F |
| **13:00** | **NEWS** | 4 | | | | F |
| 13:04 | **The Bench** — inquiries, tribunals, salvage disputes | 28 | crime | report + narrative | measured | W |
| 13:32 | **Vantage** — a single voice, a single argument | 28 | rotating | essay | slow | A |
| **14:00** | **NEWS** | 4 | | | | F |
| 14:04 | **The Count** *(Fri)* — the chart, 20 down · **Dispatch** *(Mon–Thu)* | 28 | music · conflict | chart / package | bright | F · R |
| 14:32 | **Cut** — dress, salvage, status, scarcity | 28 | fashion | magazine | light | A |
| **15:00** | **NEWS** | 4 | | | | F |
| 15:04 | **Ice & Iron** — results, standings, the racing | 28 | sport | results + two-way | fast | F |
| 15:32 | **Relay** · **Body & Air** *(repeat of 09:32)* | 28 | technology · health | explainer | measured | R |
| **16:00** | **NEWS** | 4 | | | | F |
| 16:04 | **The Gallery** — makers, light works, station architecture | 28 | art | review + profile | measured | A |
| 16:32 | **Names** — who is being talked about, and why | 28 | celebrity | magazine | light | A |
| **17:00** | **NEWS** | 4 | | | | F |
| 17:04 | **The Evening Report** — the flagship | 56 | politics · conflict | magazine | fast | F |
| **18:00** | **NEWS** | 4 | | | | F |
| 18:04 | **The Six** — the main news programme of the day | 28 | politics · conflict | news programme | grave | F |
| 18:32 | **Crossfire** — three voices who disagree | 28 | politics | discussion | fast | F |
| **19:00** | **NEWS** | 4 | | | | F |
| 19:04 | **Assembly** — the council, the factions, the manoeuvre | 56 | politics | discussion + interview | measured | W |
| **20:00** | **NEWS** | 4 | | | | F |
| 20:04 | **The Documentary** — the station's long-form strand | 56 | rotating | feature | slow | W |
| **21:00** | **NEWS** | 4 | | | | F |
| 21:04 | **Faith in Transit** | 28 | religion | talk + interview | slow | A |
| 21:32 | **The Bench** *(repeat of 13:04)* | 28 | crime | report + narrative | measured | R |
| **22:00** | **NEWS** | 4 | | | | F |
| 22:04 | **The Late Report** — the day analysed, not repeated | 56 | politics · conflict | analysis | measured | F |
| **23:00** | **NEWS** | 4 | | | | F |
| 23:04 | **Night Record** — heritage music, one label or one year | 56 | music | specialist | slow | A |
| **00:00** | **NEWS** | 4 | | | | F |
| 00:04 | **The Midnight Report** | 28 | politics · conflict | news programme | grave | F |
| 00:32 | **The Long Record** — history documentary | 28 | history | feature | slow | A |
| **01:00–05:00** | **The Night Watch** — archive block, `4 + 56` each hour. Documentaries, retrospectives, essays, music. The `:00` junction is a 2-minute summary in a 4-minute slot | 4×60 | history · art · music | feature + sequence | slow | A |

**Reflection is an item, not a slot.** At five minutes it was never a programme; it closes
`Early Watch`, which is where a reflective piece belongs in a 05:00 hour anyway.

**Repeat slots, as validation 9 requires.** The three 28-minute `W` strands repeat in-week:
`Relay`/`Body & Air` at 15:32, `The Bench` at 21:32, `Dispatch` at 14:04 Mon–Thu. The three
56-minute `W` strands — `The Common Table`, `Assembly`, `The Documentary` — repeat at the weekend,
which is where a long repeat belongs and what the weekend already implies.

### Weekend

Same clock, different fixtures. `First Shift` becomes **Sixth Day** (lighter, 2 hours). The weekday
strands are replaced by: **The Week in Ice** (sport round-up, 56), **The Count** full rundown,
**The Long Question** long edition (56), **Observance** (religion, 28), and the three 56-minute `W`
repeats. Saturday carries the chart's full rundown; Sunday is the quietest day on the station.

**The weekend is not yet a grid.** It has fixtures but no hour-by-hour clock, and validation 8
covers Saturday and Sunday too — so `grid.yaml` cannot be completed until this table exists at the
same resolution as the weekday one.

---

## 9. Does it fit — and what to cut

**This grid is a full BBC-style speech station and it costs far more than a Mac mini can render.**
Saying so plainly is the point; the previous version of this section hid the problem by filling the
day with music, which quietly turned the product into something else.

Speech is ~75% of a talk slot; the rest is imaging, beds and links.

| | Slot min/day | Speech/day |
|---|---|---|
| 24 × 4-min junctions (19 bulletins + 5 overnight summaries) | 96 | 86 |
| Fresh `F` programmes as listed, chart amortised | 536 | ~400 |
| Weekly `W` programmes, amortised across the week | 36 | ~27 |
| Archive `A` and repeats | 460 | 0 |
| **Total fresh speech per day** | | **~515 min** |

Against ~216 usable minutes at RTF 0.7× (ARCHITECTURE §36). **The grid is roughly two and a half
times the budget** — down from three, because the chart went weekly and five slow strands went to
archive. So it is built in tiers, and the tier is a capacity decision, not an editorial one:

| Capacity | What goes fresh |
|---|---|
| **~200 min** (RTF 0.7) | All junctions · `First Shift` cut to one hour · `The Evening Report` · `The Six` · `The Count` · everything else weekly or archive |
| **~300 min** (RTF 1.0) | Add `The Midday Report`, `Ledger`, `Ice & Iron`, `The Midnight Report` |
| **~460 min** (RTF 1.5) | Add `First Shift` full 3 hours, `The Late Report`, `Crossfire`, `The Long Question` |
| **~515 min** | The grid as written |

**Repeats are not a compromise, they are how radio works.** The BBC repeats constantly — Radio 4
Extra is an entire station of it, and the World Service reruns its documentary strands several times
a week across time zones. A `W` programme aired Tuesday at 09:30 and again Thursday at 21:30 is
normal practice, not a shortfall, and it should be billed on air as a repeat.

**The cut order, if capacity falls short of the tier you are on.** Each step costs a listener less
than the one before:

1. Move a `W` programme to fortnightly.
2. Shorten a 56-minute programme to 28 — it is already two acts, so this is dropping one.
3. Extend the overnight archive block to 06:00.
4. Move `The Documentary` permanently to archive.

**Never cut**: the hourly junction, `The Evening Report`, or — from week three, when
`requires_airplay_days: 21` first allows it on air — `The Count`. Those three are the station's
identity: the clock, the flagship, and the one thing that is fun.

---

## 10. Programme metadata

Every programme in the grid needs six things defined before it can be scheduled. This is what
`grid.yaml` encodes.

| Field | Example |
|---|---|
| **Jingle set** | `open`, `close`, `bed`, and for news a `sting`. One identity per strand — this is the single cheapest way to make a schedule feel like a station, and it is a one-off render |
| **Pace** | fast · brisk · measured · warm · light · slow · grave. Sets link length, item count and the emotion band |
| **Presenter** | one strand host, plus the beat correspondents who appear inside it (§5) |
| **Domain floor + context mix** | retrieval seats and the canon : world ratio (§1) |
| **Item mix** | the running order shape (ARCHITECTURE §11) |
| **Freshness** | `F` daily · `W` weekly with repeats · `A` archive |

---

## 11. How to grow this

Start with four, not thirty. The rest of the day runs on repeats and archive, which is exactly what
a new speech station does — the World Service reruns its strands several times a week and nobody
considers it a placeholder.

Four to build first: **the hourly bulletin** (the spine, and the thing that makes it a station),
**The Evening Report** (the flagship magazine), **The Count** (the chart), and **The Long Record**
(one history documentary for the archive). They cover the three clock speeds, the three context mixes and the three
presenter roles, and they will tell you more about what works than a full grid of untested formats.

Add a programme only when there is a domain producing more material than its current slot can hold.
An empty programme is worse than no programme, and the world tick's output is the constraint —
never the ambition.
