# Settlement Radio — Architecture v9

The complete design for a talk-led, 24/7 AI radio station built and operated by one person.
This is the only architecture document. Scope is what's in here.

**Part I (§1–20)** describes the system. **Part II (§21–32)** describes how it is built: repo
layout, config, secrets, logging, errors, caching, security, testing, CI. **Part III (§33–37)** is
the working agreement, the build order, and what changes if the hardware improves. Part II binds
every task; an agent that has read only Part I is not ready to write code.

---

# Part I — The system

---

## 1. Constraints and targets

| | |
|---|---|
| Studio | **Mac mini M4, 16GB, 256GB** + external Thunderbolt SSD (2TB) |
| Transmitter | Hetzner CX32, ~€11/mo |
| Generation | **Nightly batch, 20:00–06:50.** Nothing is generated near air time |
| Broadcast | 24/7 speech. Fresh talk through the day, archive overnight and at the weekend |
| Marginal cost | Electricity + VPS + domain. No per-token or per-character spend |
| Jurisdiction | Poland / EU — **AI Act Art. 50 applies from 2 August 2026** |
| Operator | One person, working through Claude Code |

**Why batch rather than continuous.** All broadcast audio is pre-rendered files played by
Liquidsoap. Nothing is generated live, so *when* generation runs is a scheduling choice, not an
architectural one. Running it in a single overnight window means the writer model and the TTS
model are never resident simultaneously, which is what makes 16GB sufficient. It also means
generation latency stops mattering — a retrieval call taking 1.5 seconds instead of 500ms costs
forty seconds across an entire night.

**The two numbers that gate everything** (measure before writing pipeline code, §36):

1. Sustained TTS real-time factor over 60 minutes on this machine.
2. Whether a 9–10B local model writes radio you want to broadcast.

Everything else in this document is solvable engineering. Those two are not.

---

## 2. The stack

| Layer | Choice | Why |
|---|---|---|
| **Writer LLM** | dense, **≤6GB at Q4** + KV — which is **9–10B**, not 9–12B (see the memory budget) | The only LLM. Does scripts, world tick, items, canon checks. Named candidate: Qwen 3.5 9B |
| **LLM runtime** | **LM Studio (MLX backend)**, OpenAI-compatible on `:1234` | MLX is typically faster than GGUF on Apple Silicon. OpenAI-compatible keeps the seam honest |
| **Cast TTS** | **Chatterbox Multilingual v3** (Resemble, MIT) | Emotion exaggeration + paralinguistic tags. Its built-in PerTh watermark is a **bonus, not a requirement** (D-019) — the engine is chosen on how it sounds |
| **Second TTS** | **Qwen3-TTS** (Alibaba, Apache 2.0, 0.6B) | Different control vocabulary (natural-language direction). Two implementations is what proves the seam (§3) |
| **Fallback TTS** | **Kokoro-82M** (Apache 2.0) | Circuit-breaker spill and CI smoke. **Never *scheduled*** — it reaches air only when the cast lane trips, and the day is marked degraded (§20) |
| **Database** | **Postgres 16** + `pgvector` + `tsvector` | One datastore for world, canon, music, retrieval, queue, metrics |
| **Embeddings** | `bge-m3` | Multilingual, strong on short facts and paragraphs |
| **Reranker** | `bge-reranker-v2-m3`, **on CPU** | Avoids GPU compute contention and a second Metal context. **Not** a RAM saving — Apple Silicon is unified memory, so the bytes cost the same either way. Latency is free in batch |
| **Playout** | Liquidsoap 2.x + Icecast 2 | |
| **Public web** | Next.js (App Router) on Vercel | Read-only |
| **Admin** | `make` targets, plus a small Next.js panel after 30 days on air | No admin framework; the panel is deferred to day 30 (§34) |
| **Orchestration** | Python 3.12, one batch process under launchd | No Celery, no Redis, no broker |
| **Migrations** | Alembic, forward-only | |

> **The commitment is the profile, not the name.** Named models age out; write down the
> requirement so the table refreshes without re-deciding anything.
>
> | Slot | Profile | Current candidate | Verified |
> |---|---|---|---|
> | Writer | dense, **≤6GB at Q4**, ≥32k context, OpenAI-compatible, passes the benchmark (§29) | `Qwen/Qwen3.5-9B` (released 2026-03-02) | **unverified — task zero** |
> | Cast TTS | zero-shot cloning, emotion control, ≤5GB. **Watermarking is recorded, never required** (D-019) | Chatterbox (Resemble, MIT, PerTh watermark) | base confirmed; the *Multilingual v3* revision must be verified |
> | Second TTS | cloning + a *different* control vocabulary | `Qwen/Qwen3-TTS-12Hz-0.6B-Base` + `Qwen/Qwen3-TTS-Tokenizer-12Hz` (Apache 2.0, 2.52GB, 3-second cloning) | **unverified — task zero** |
> | Embeddings | multilingual, ≤1.5GB, dimension declared in config | `BAAI/bge-m3` | confirmed |
> | Reranker | cross-encoder, CPU-viable at 60 candidates in <1.5s | `BAAI/bge-reranker-v2-m3` | confirmed |
>
> **"Verified" means downloaded, not read about.** Every row above marked unverified is a name from
> a document, and a name from a document is not an artifact. Task zero resolves them.
>
> **Task zero, before the §36 measurements:** resolve all five slots to real downloadable artifacts
> and record exact repo + revision + quantisation in `models.yaml`. If the Chatterbox revision does
> not resolve, the fallback second engines in order are **Dia2**, **Fish Speech S2**, **CosyVoice
> 3.0**. Kokoro cannot serve as the second implementation — it has no control vocabulary, which is
> the entire point of the pairing (§3).
>
> **Task zero also records, for every TTS candidate it resolves, whether it emits an inaudible
> watermark and by what mechanism** — one extra column, no extra work. The engine is not chosen on
> that column (D-019), but §18's marking posture reads it, and Phase G needs the answer as a fact
> rather than as a recollection. An engine with no watermark is acceptable and makes standalone
> watermarking a Phase G task.
>
> Before pinning any name, verify it is a real downloadable MLX artifact and record the **exact HF
> repo, revision and quantisation** in `config/models.yaml`. **The embedding dimension is read
> from that config when the migration is generated** — never hand-written into a `vector(n)`
> column, because a mismatch is expensive to unwind once the HNSW index exists.

### Memory budget

The batch runs in phases so these are never resident together:

The baseline — macOS, Postgres, Python — is **~5 GB and always resident**. Every figure below is
total system pressure, baseline included.

| Phase | Loaded | Processes | **Total** |
|---|---|---|---|
| **Think** — retrieve (20:00–20:40) | bge-m3 + reranker | ~2.1 GB | **~7.1 GB** |
| **Think** — write (20:40–00:00) | writer + KV | ~6.5 GB | **~11.5 GB** |
| **Speak** (00:05–06:30) | Chatterbox only | ~5 GB | **~10 GB** |
| **Assemble** (06:30–06:50) | ffmpeg | ~1 GB | **~6 GB** |

**Retrieval and writing are sequenced, not concurrent.** The whole night's context is retrieved
first, the embedder and reranker are unloaded, and only then does the writer load. Holding all three
would cost ~14 GB and leave nothing for the machine — this ordering is what makes the phase fit.

The writer profile is therefore **≤6 GB at Q4**, not 6–8: at 8 GB the Think phase reaches ~13.5 GB,
leaving 2.5 GB — inside the 2 GB floor, but with nothing left for a re-render, a browser, or the
KV growth of a long act. Peak at ≤6 GB is ~11.5 GB against 16 GB, leaving **~4.5 GB headroom, and
the target is never to go below 2 GB**.

**What ≤6 GB means in parameters, because the two were stated inconsistently.** MLX 4-bit costs
about **0.56 bytes per parameter** — 4 bits per weight plus a scale and bias per group of 64, i.e.
4.5 effective bits. So 9B ≈ 5.1 GB, 10B ≈ 5.6 GB, **11B ≈ 6.2 GB and 12B ≈ 6.8 GB — both already
over the profile before a single KV token**. The band is therefore **9–10B**, and it was written
as 9–12B in three places. Where a parameter count and the ≤6 GB profile ever disagree again, **the
profile is the commitment** and the count is the thing that yields.

**The §36 gate is stated as total system memory pressure, not process RSS** — the 5GB baseline is
what determines whether the machine swaps, and swapping during a four-hour Think phase is the
failure this budget exists to prevent. Phase 1 is the tight one. **The writer is explicitly
unloaded before TTS starts** — call the runtime's unload endpoint and assert free memory; do not
trust eviction.

---

## 3. Portability — the seams

Every model here will be superseded. The interface is the easy part; lock-in accumulates around
it — in prompt tuning, in prose parsing, in voice identity, and in an archive that cannot be
re-rendered.

Three layers make a seam real: **config** (what is selected), **protocol** (what is promised),
**conformance** (what is proven). A seam with only the first two has never been tested.

### The LLM seam

Routing is per **job**, not per application, even though today every job points at the same model:

```yaml
# config/models.yaml
jobs:
  writer:      { base_url: "http://localhost:1234/v1", model: "qwen3.5-9b-mlx-4bit",
                 temperature: 0.9, max_tokens: 10000, timeout_s: 300 }
               # 10k, not 6k: a 25-minute act is ~3,750 words ≈ 5,000 tokens of *prose*,
               # and the script schema (items, turns, emotions, offsets) roughly doubles
               # it. A cap that truncates mid-JSON looks like a model failure, not a
               # config one, and costs a day to find
  tick:        { base_url: "http://localhost:1234/v1", model: "qwen3.5-9b-mlx-4bit",
                 temperature: 1.0, max_tokens: 4000, timeout_s: 180 }
  items:       { base_url: "http://localhost:1234/v1", model: "qwen3.5-9b-mlx-4bit",
                 temperature: 1.1, max_tokens: 1500, timeout_s: 90 }
  canon_check: { base_url: "http://localhost:1234/v1", model: "qwen3.5-9b-mlx-4bit",
                 temperature: 0.2, max_tokens: 2000, timeout_s: 90 }
```

Keeping them separate now costs nothing and means moving one job to a larger model later is three
edited values.

**Two disciplines make the seam real:**

**1. Never parse prose.** Every generation returns JSON validated against a Pydantic schema, with
bounded retries and one repair prompt. The moment any code does `text.split("---")` or regexes a
heading out of a response, you are coupled to one model's formatting habits.

```python
def generate_structured[T: BaseModel](job: str, prompt: str, schema: type[T],
                                       *, attempts: int = 2) -> T:
    """The ONLY way any caller obtains model output. No raw-text path exists."""
```

Ask for JSON in the prompt, validate, retry once, then fail. **The contract is prompt-and-validate,
always.** But asking a 9B model for one JSON object containing a 25-minute script is a real
reliability risk, and LM Studio supports JSON-schema-constrained decoding. So: an optional per-job
`structured_output: true` flag in `models.yaml` that an adapter **may** honour and that nothing in
the codebase may depend on. You keep the seam and take the reliability where it is available; a
provider without it behaves identically, just with more repair attempts.

**2. Prompts are versioned files with a golden set.** `prompts/*.jinja` in git, plus 15–20 stored
inputs and their outputs in `tests/golden/`. Swapping a model means `make golden` and reading the
diffs. Without it you can swap in five minutes but cannot tell whether you should have.

**What you get for free:** canon is markdown and the world is structured rows, so swapping the
writer invalidates nothing already generated. Protect that property — never store a model's raw
output as the source of truth for anything.

### The TTS seam

Capabilities are **declared, not assumed**:

```python
@dataclass(frozen=True)
class Capabilities:
    supports_cloning: bool
    supports_emotion: bool
    nonverbal_tags: frozenset[str]      # {"laugh","breath","sigh"} — may be empty
    max_speakers_per_call: int          # 1 = per-turn rendering required
    native_sample_rate: int
    typical_rtf: float                  # measured on this machine, not vendor-claimed
    deterministic_with_seed: bool

@dataclass(frozen=True)
class SpeechRequest:
    text: str
    voice: VoiceRef                     # reference clip path OR preset name
    emotion: str | None                 # OUR vocabulary, never a vendor's
    nonverbal: str | None
    seed: int | None

class TTSEngine(Protocol):
    name: str
    capabilities: Capabilities
    def synthesize(self, req: SpeechRequest) -> RenderedAudio: ...
```

Callers branch on capabilities, never on engine names. There is no `if engine.name == "..."`
anywhere in the codebase.

**Control vocabulary stays yours.** `warm|wry|somber|bright|urgent` and
`laugh|breath|sigh|half_laugh`. Each adapter owns a mapping table — Chatterbox's exaggeration
scalar and inline tags, Qwen3-TTS's natural-language direction, Kokoro's nothing. An engine that
cannot express a value **accepts and ignores it**, never raises. Degradation is silent in the
audio and loud in the logs.

**Normalise at the boundary.** Every engine returns 48kHz mono WAV, loudness-normalised to a fixed
LUFS target, before anything downstream sees it. Skip this and a swap changes the station's
perceived volume.

**RTF is part of the contract.** An engine three times slower breaks the render window while every
test passes. The batch planner reads `typical_rtf` from `config/measured.yaml` and derives planned
fresh hours from it, so a slower engine visibly reduces planned output rather than silently
falling behind.

### Guest voices — figures who are not presenters

Two-ways, interviews, vox pops and packages all put non-presenters on air. A `figures` row is not a
`cast` row and must not become one — there will eventually be hundreds of figures and they cannot
each have an authored speech profile.

- **A stock voice bank of 12–20 reference clips**, varied by age, register and settlement, rendered
  once and committed alongside the cast clips.
- `figures.voice_ref` assigns one deterministically on first speaking appearance and **never
  changes** — the same official sounds the same in March as in January, which is most of what makes
  a world feel populated.
- Guests get a **role-derived register**, not an authored profile: `guest` and `vox` sit mid-band on
  the conversational scale; `correspondent` uses the `scripted` bounds, because a correspondent is
  reporting, not chatting.
- The distinctiveness rule (§11a) applies to presenters only. Guests are allowed to sound ordinary.

### Voice identity

Listeners notice a changed voice far more than they notice better prosody.

- **The reference clip is the canonical artifact.** A 10–20 second WAV per DJ in `voices/`,
  committed to git, with provenance in `voices/PROVENANCE.md`.
  **Note the consequence of a public repo:** anyone can clone your presenters' voices. Not a
  compliance issue — they are synthetic, not real people — but it is impersonation-of-the-station
  risk, and the choice to accept it belongs in `DECISIONS.md` rather than being made by default. You own that file; a vendor voice
  ID is a dependency, a WAV is not.
- **Prefer cloning-capable engines** for cast voices so the same clip reproduces the same voice
  across engines. Preset-only engines are fine for the pool.
- **Fixed seed per DJ**, stored on the `cast` row.
- **The archive is the deepest lock-in and has no technical fix.** Once 500 shows exist in a voice,
  changing it orphans them. Two honest options: give it an in-world explanation (a host leaves,
  another arrives — a *feature* in a world that progresses), or bulk re-render, which is cheap
  when TTS is local. Decide before you are 500 shows deep.

### Conformance

**Ship two implementations of the TTS seam from day one.** Chatterbox *and* Qwen3-TTS — two
expressive engines with genuinely different control vocabularies, which is a far better test of
the seam than two similar ones. Kokoro is the third, fallback-only. The LLM seam ships one
implementation and is conformance-tested instead; the reasoning is at the end of this section.

```python
@pytest.mark.parametrize("engine", all_registered_engines())
def test_tts_conformance(engine: TTSEngine):
    req = SpeechRequest(text=CONFORMANCE_SCRIPT, voice=TEST_VOICE,
                        emotion="wry", nonverbal="laugh", seed=42)
    out = engine.synthesize(req)

    assert out.sample_rate == 48_000 and out.channels == 1
    assert abs(out.lufs - TARGET_LUFS) < 1.0
    # expected_sec comes from the duration estimator (§11a) applied to CONFORMANCE_SCRIPT
    assert 0.8 < out.duration_sec / expected_sec < 1.25
    assert not out.is_silent and not out.is_clipping
    assert engine.synthesize(replace(req, emotion="nonsense")) is not None
    if engine.capabilities.deterministic_with_seed:
        assert out.checksum == engine.synthesize(req).checksum
```

**Timed assembly is tested separately from the engines**, because TTS output length is inherently
variable and asserting on a live engine measures the wrong component. Feed the assembler synthetic
fixed-duration audio and assert the *mixer* is accurate:

```python
def test_assembly_timing():
    # synthetic(seconds, ...) returns silence of exactly that length
    turns = [synthetic(1.0),
             synthetic(2.0, overlap_prev_ms=-200),
             synthetic(1.5, pause_before_ms=500)]
    out, cue = assemble(turns)
    for entry in cue:
        assert abs(measured_offset(out, entry) - entry.offset_ms) < 50
    assert abs(out.duration_sec - 4.8) < 0.05
```

A 20ms systematic error in overlap handling compounds across 300 turns into a show that misses its
slot by six seconds, and back-timing absorbs the drift silently until the hour no longer fits.

For the LLM seam: every configured job returns schema-valid output for its golden inputs, three
runs, zero validation failures. **The LLM seam is conformance-tested rather than dual-implemented** —
every job points at the same local model today, and a second provider is a `models.yaml` entry away
rather than a refactor. Only the TTS seam ships two implementations on day one.

---

## 4. Topology

```
┌──────────────── STUDIO — Mac mini M4 16GB (Tailscale) ────────────────┐
│                                                                       │
│  Internal 256GB:  macOS · models (~15GB) · repo · code                │
│                                                                       │
│  External SSD /Volumes/station:                                       │
│    pgdata/  segments/  archive/  music/  pool/  imaging/  rundown/    │
│    voices/  backups/  logs/                                           │
│                                                                       │
│  Postgres 16 (pgvector + tsvector)                                    │
│    facts · domains · dayparts · settlements · threads · beats · items │
│    figures · quotes · coverage · thread_figures · thread_settlements  │
│    artists · artist_members · albums · tracks · labels · charts       │
│    chart_entries · airplay · track_credits · imaging · programmes     │
│    programme_hosts · cast · cast_profiles · segments · archive_items  │
│    pool_items · render_queue · metrics                                │
│                                                                       │
│  LM Studio :1234 — writer (loaded 20:00–00:00 only)                   │
│  TTS worker      — Chatterbox (loaded 00:05–06:30 only)               │
│  now.json poller — 1/min, writes coverage + airplay (§6)              │
│                                                                       │
│  batch.py — launchd, one run per night:                               │
│    world tick · junctions · shows · render · mix · playlist · push    │
└───────────────────────────────┬───────────────────────────────────────┘
                                │ rsync push (content) + read-only pulls:
                                │ now.json poll (§6) and verify-marking (§18)
                                ▼
┌──────────── TRANSMITTER — Hetzner CX32 ────┐      ┌──── Vercel ────┐
│  /srv/audio/{hours,shows,pool,archive,     │      │  Next.js       │
│              music,imaging}                │─────▶│  public site   │
│  Liquidsoap → Icecast → HLS + YouTube RTMP │ JSON │  player · grid │
│  pinned hourly junction slot               │      │  about · AI    │
│  no DB · no models · no inbound but 80/443 │      │                │
│  one outbound: RTMP→YouTube · 2 secrets    │      │                │
└────────────────────────────────────────────┘      └────────────────┘
```

The Transmitter is deliberately stupid: it plays files from directories and serves `now.json`. It
holds no database, runs no model, and cannot fail in a way that requires intelligence to recover
from.

Precisely: **inbound** 80/443 public plus 22 on Tailscale; **outbound** exactly one destination, the
RTMP push to YouTube; **secrets** exactly two, `ICECAST_SOURCE_PASSWORD` and `YOUTUBE_STREAM_KEY`
(§23). §27's firewall rules are derived from this line, so keep it accurate. **The worst realistic outage sounds like the overnight block.**

**Two operational notes about the external volume**, which will otherwise bite:

- **Postgres must not start before the volume mounts.** Run it under launchd with a mount check,
  or the database comes up empty and the batch writes into nothing.
- Audio grows ~1GB per broadcast hour per day. Retention (§28) is not optional here; it is what
  keeps the disk alive.

---

## 5. Knowledge architecture

Four tiers, assembled for every generation call — three of canon and world knowledge, plus the
moving present. **Constant cost regardless of how large the
world grows** — this is what lets the canon expand for years without the prompt expanding with it.

### Tier 0 — Station core (always present, cached, ~2–3k tokens)

The station's identity, the in-world premise, the register rules, the cast cards for whoever is on
air. Fixed text, never retrieved, sits in the cached prompt prefix.

**Where it comes from** (D-030 — this was previously unstated, and the text sat in `canon/` where
retrieval could reach it):

| Source | Loaded |
|---|---|
| `core/*.md` — station identity, premise, the clock concept | **whole and verbatim**, in filename order |
| `cast/CAST.md` — cards for whoever is on air (§35 C2) | the cards for that programme's speakers only |
| the register spec (§11a) | assembled from `grid.yaml` and the speech profile on the `cast` row |

**`core/` is not canon and is never parsed.** No frontmatter, no atomising, no `fact_key`, no
embedding — `canon-check` and `canon-sync` do not read it, and nothing in it is retrievable. It is
prompt text. That is the whole contract, and it is what keeps this tier a fixed cost.

**Tier 0 has no growth mechanism on purpose.** It is the only tier every call pays for in full, so
a file added to `core/` raises the floor of every prompt in the station. Two files is the intended
size; a third needs a reason.

### Tier 1 — Domain summaries (always present, ~3k tokens)

**This is the piece that prevents flatness.** Every canon domain — the seventeen of
`PROGRAMMING.md` §3, and only those — has a 150–200 word summary, regenerated whenever that
domain's files change. **All summaries always ship.**

The effect: the model always knows the *shape* of the world — that a religion exists, roughly what
the war was about, that the currency is tied to relay time — even when no religion fact was
retrieved. Detail is retrieved; structure is always resident. Seventeen domains is ~4k tokens, and
the mechanism would still hold at twice that — but the domain list is closed at seventeen
(`PROGRAMMING.md` §3), so this tier does not grow with the world. Only Tier 2 does.

> **Plain text and retrieval are both used, deliberately.** Tiers 0 and 1 are *always* included
> verbatim — they are small, fixed, and cacheable, and they are what gives the model a sense of the
> world's shape. Only Tier 2 is retrieved. Selecting canon at the file level ("sports show reads
> sports.md") is what makes a world flat; shipping all of it is what stops scaling. The split is
> the answer to both.

### Tier 2 — Retrieved detail (hybrid + rerank)

> **One budget of 40, shared with Tier 3.** Tiers 2 and 3 together contribute **40 entries** to the
> assembled context, split by the programme's `context_mix` (§11): a slow-domain feature at
> `{canon: 0.8}` takes 32 facts and 8 world entries, a fast-domain magazine at `{canon: 0.3}` takes
> 12 and 28. The pipeline below always ranks down to 40 candidates; the `context_mix` decides how
> many of them are actually seated. There is no second budget anywhere.

```
query = programme brief  +  today's top beats  +  the show's declared angle
   │
   ├─ sparse: Postgres tsvector / BM25          → top 50
   └─ dense:  pgvector, bge-m3 embeddings       → top 50
              │
        Reciprocal Rank Fusion (k=60)           → top 60 candidates
              │
        bge-reranker-v2-m3 cross-encoder (CPU)  → top 40
              │
        diversity shaping: hard cap 12/domain,
        soft bonus for unrepresented domains     → final slice
```

- **Hybrid, not pure vector.** BM25 beats dense retrieval on proper nouns — "Cold Harbor",
  "ES-447", a figure's name — which is most of what a radio script needs. Pure semantic search
  systematically misses exact names. Postgres does both natively.
- **Contextual retrieval at index time.** Each fact is stored with a one-line generated situating
  prefix ("From the finance cornerstone, on the post-war relay tariffs: …"). One-time cost per
  fact; it makes short atomic facts retrievable.
- **Diversity shaping, not filtering and not a hard floor.** A hard "minimum 3 domains" injects
  weak facts whenever the ranked list is legitimately single-domain. Instead: a hard cap of 12
  facts per domain plus a soft **rank offset** for domains with no representation yet: an
  unrepresented domain's best candidate is promoted by 5 rank positions. Expressed as a rank offset
  rather than a score bonus because cross-encoders emit unbounded logits, not 0–1 scores, so a fixed
  additive constant would mean nothing. Money and politics stay in reach without junk being forced in.
- **Retired facts are excluded.** Retrieval reads `status='active'`; the only consumer of retired
  facts is historical coverage rendering (§7).

**Retrieval is measured, not tuned by feel.** Maintain `tests/eval/retrieval.yaml`: 30 hand-written
queries each with 5–10 `fact_key`s that *should* be retrieved. Report **Recall@10** and
**Recall@40**. Without this you will eventually change the embedding model or the fusion constant
and have no idea whether you improved anything — which is exactly how retrieval quietly degrades.

**The retrieval strategy is versioned like a prompt.** `retrieval_version` covers the embedding
model, reranker, fusion constant, slice size and diversity parameters, and is recorded on every
golden output.

### Tier 3 — World slice

Ranked beats, items and coverage — the moving present. Recency (36h half-life) × thread stage ×
domain floor × breaking-ness, plus a title-only tail. **It draws on the same 40-entry budget as
Tier 2, split by `context_mix` (§11) — there is no separate seat count.**

### The embedding pipeline

Real vectors, computed locally, stored in Postgres. Operationally:

**What a "fact" is.** One atomic assertion, typically 1–3 sentences, extracted by `canon-check`
pass 1. Not a paragraph, not a file. Granularity matters: too coarse and retrieval returns
irrelevant material bundled with the relevant; too fine and facts lose the context that makes them
meaningful. The `context_prefix` compensates for the latter.

**When embeddings are computed.** Only in `make canon-sync`, only for facts whose `text_hash`
changed, and always for the **prefixed** text (`context_prefix + "\n" + text`) — never the bare
fact. A changed prefix therefore forces re-embedding, which is why the prefix is regenerated on the
same trigger.

**Cost.** bge-m3 on the mini embeds a few hundred facts in seconds. A full re-embed of a
10,000-fact canon is minutes, not hours, so a model change is annoying rather than blocking. Record
`embedding_model` and its revision on every row so a partial re-embed is detectable.

**The sparse half.** `tsv` is a generated `tsvector` column maintained by Postgres, with a GIN
index. No separate search engine, no separate index to keep in sync.

**Fusion.** Reciprocal Rank Fusion with k=60 over the two ranked lists. RRF needs no score
normalisation between BM25 and cosine similarity, which is exactly why it is the right choice here
— comparing raw scores across those two spaces is meaningless.

### Room to grow

```sql
facts(
  fact_key   text primary key,   -- assigned once, stable across edits
  text_hash  text,               -- SHA of normalised text; drives re-embedding
  supersedes text[],
  domain     text,
  text       text,
  context_prefix text,
  embedding  vector(N),          -- N is substituted from models.yaml when the migration
                                 -- is GENERATED; never hand-written (§2)
  tsv        tsvector,
  source_file text,              -- which canon/*.md it came from; canon-sync retires
                                 -- facts whose source file no longer contains them
  scope      text,               -- 'universe' | 'station'
  station_id int null,
  status     text                -- 'active' | 'retired'
)
```

`scope` and `station_id` are present but unused today. They cost nothing and mean a second station
sharing the universe is a query change rather than a migration. **Do not build anything else for
multi-station until a second station actually exists.**

---

## 6. The world

Four layers, distinguished by how fast they change. Confusing them is what makes a world flat.

### Canon — static, hand-authored, yours

Markdown under `canon/`. Changes only when you change it. Never selectively included at the file
level; see §5.

### Threads — slow arcs, weeks to months

```sql
threads(id, scope, station_id, title, domain text[], stage, opened_at, summary)
        -- related figures/settlements live in join tables (below), not arrays
        -- stage: rumoured|building|active|resolving|closed
```

### Beats — the timeline, and the reason time is sayable

```sql
beats(
  id, thread_id,
  occurs_at   timestamptz,   -- in-world
  certainty   text,          -- scheduled | expected | rumoured
  status      text,          -- planned | happening | resolved | slipped | cancelled
  horizon     text,          -- hours | days | weeks | months
  headline    text,
  detail      text,
  outcome     text,          -- null until it fires
  created_by  text
)
```

**This table is why a DJ can say "tomorrow" or "next month".** The nightly tick writes beats across
the horizon: the convoy docks at 14:20 today, the council votes at 18:00, the inspection is
expected this week, the harvest festival is in six weeks. A presenter can trail all of them because
they already exist as rows.

**Horizon floor** — always ≥6 beats within 24h, ≥10 within the week, ≥5 within the season. When it
thins, the tick refills. This is what stops the world collapsing into an eternal present.

**Horizon ceiling** — a floor-only rule densifies the world every night until retrieval is noise:

| Bound | Value |
|---|---|
| Max **new** beats per tick | 8 total, 3 per domain |
| Max **open** beats (`planned` + `happening`) | 40; above it the tick creates none |
| Max open threads per stage | 6 `active`, 10 `building` |

```sql
domains(id, name, summary, prompt_version, source_tree_hash, updated_at)
        -- name is one of the seventeen in PROGRAMMING.md §3, and nothing may invent another
        -- summary is the Tier 1 always-ship digest (§5), regenerated when source_tree_hash moves

pool_items(id, kind, file_path, duration_sec, band, last_used_at, plays)
        -- band: '15_30' | '30_90' | '90_240' — what `make pool-check` counts
        -- kind: trail | letter | vignette | weather | travel | archive_quote
        -- NOT idents or sonic logos: anything carrying a programme or station
        --   identity is an `imaging` row (§9), and one object may not live in
        --   two tables. The boundary is ownership, not length:
        --     imaging    = station furniture, placed by the hour clock
        --     pool_items = back-timing filler, chosen by length (§13)
```

**Precedence: the ceiling wins.** If the horizon floor is unmet but the open-beat ceiling is
reached, the tick creates nothing and logs a WARNING that surfaces in the rundown. A world with 40
unresolved beats does not need more beats; it needs the tick to resolve some, which is the next
night's work.

**Stale-beat retirement.** A `planned` beat whose `occurs_at` has passed without firing, and which
nothing has referenced, is retired after 72 hours as `cancelled` with a one-line outcome ("the
inspection was quietly dropped"). Without this, cancelled and slipped beats occupy horizon slots
forever and the floor never triggers a refill.

**No thread stalls silently.** A thread `active` with no beat for 5 days is flagged to the next
tick as requiring either a beat or a stage change. Otherwise a long-running arc drifts into
permanent background hum, referenced in summaries and never advancing.

**Beats pass the same gates as scripts** — register check and safety gate (§19) before being
written. A beat is a factual assertion every later script treats as true; far cheaper to reject at
20:00 than to unwind after it has aired.

### Items — disposable texture

```sql
items(id, text, domain, settlement_id, created_at, expires_at)
```

One-liners with a 36-hour read window and 7-day retention. A ferry ran late, a birth, a rota
swap. Sixty a night. This is what a real newsroom runs on between its big stories, and it is why
the same three threads don't get named in every programme.

**`expires_at` holds the read window** (created_at + 36h) — it is what retrieval filters on.
Deletion at 7 days is a separate retention sweep keyed on `created_at`, so an expired item is still
available to explain something that aired.

### Settlements, factions and ships

```sql
settlements(id, name, kind, founded_year, population, parent_id, summary)
            -- kind: station | ring | surface | ship | outpost
```

**Ruling on factions and ships, because §7 pass 4 validates references to them:** factions and named
ships are **canon facts, not rows** — they change only when you change the bible, and they carry no
per-day state. Link integrity therefore resolves a reference by looking for a `fact_key` matching
`faction:*` or `ship:*`. Settlements *are* rows because five tables join to them. Anything that
needs a foreign key is a row; anything that is only ever named is a fact.

### Programmes, segments and charts

```sql
dayparts(id, name, from_time, to_time, energy_lo, energy_hi, bpm_lo, bpm_hi)
         -- the seven of PROGRAMMING.md §4; written by grid-sync from grid.yaml.
         -- Drives rotation energy/tempo (§8) and modifier selection (§11a)

programmes(id, slug, name, programme_type, format_class, brief, domain_floor,
           context_mix, slot_minutes, register_kind, pace, jingle_set,   -- slot_minutes: 4|28|56
           freshness, production_day, repeat_slots, chart_id,
           item_mix jsonb, hour_clock jsonb, schedule jsonb,
           max_lead_hours, requires_airplay_days, active)
           -- schedule: [{days: [...], at: "HH:MM"}] verbatim from grid.yaml — the
           --   only place that says WHEN a programme airs, and what the playlist
           --   builder reads. One clock, seven days: `days` is what varies (D-001)
           -- item_mix / hour_clock: stored verbatim from grid.yaml (§17a).
           --   item_mix is read by script validation 6; hour_clock by the mixer (§9)
           -- format_class: junction | floating | pool
           -- register_kind: conversational | scripted
           -- slot_minutes: 4 | 28 | 56   (the only legal values; 56 = 2 acts of 28)
           -- pace:       fast|brisk|measured|warm|light|slow|grave
           -- freshness:  F (nightly) | W (weekly, repeats) | A (archive) — §14
           -- repeat_slots: where a W programme airs again in the week
           -- written by grid-sync from grid.yaml; never edited directly

segments(id, programme_id, air_date, air_time, format_class, status,
         script_json, file_path, duration_sec, cue_sheet_json,
         engine, worker_version, generated_at, rendered_at, aired_at,
         is_repeat bool, original_segment_id)
         -- a repeat reuses the audio of original_segment_id, airs with a
         -- "first broadcast on…" line prepended, and writes NO new coverage
         -- rows (§6) — the station said it once, not twice
         -- status: planned|written|quarantined|rendered|mixed|pushed|aired|dropped

charts(id, slug, name, size, cadence)      -- 'main' 40 weekly; specialist charts later
                                           -- size is what is COMPUTED (40). The Count airs the
                                           -- top 20 of it in 28 minutes; the rest exists so
                                           -- positions 21–40 can move, re-enter and be referenced
```

`segments` is the spine: `coverage.segment_id`, the quarantine path, and the `segment_id` logging
field all point here, and its `status` column is what makes a partially-completed batch resumable.

### The render queue

```sql
render_queue(id, job_type, target_id, air_date, priority, status,
             worker_id, worker_version, leased_until, attempts,
             engine, error, created_at, started_at, finished_at)
             -- status: pending|running|done|failed
             -- UNIQUE (job_type, target_id, air_date)   ← the idempotency key (§25)
```

### Figures and coverage

```sql
figures(id, name, role, settlement_id, stance, first_seen, voice_ref)
        -- no is_artist flag: artistry is expressed by artists.figure_id, and a
        -- duplicated boolean would drift
        -- voice_ref: assigned from the stock voice bank on first speaking
        --   appearance and NEVER changed (§3). Null until they speak
thread_figures(thread_id, figure_id)         -- join tables, not int[] arrays:
thread_settlements(thread_id, settlement_id) -- arrays make §7 link integrity much harder
quotes(id, figure_id, text, said_at, thread_id)

coverage(id, thread_id, beat_id, aired_at, programme_id, dj_id,
         angle, one_line, segment_id)
-- written when a segment AIRS, never when it is generated: a script the safety
-- gate rejects or back-timing drops must leave no trace claiming it was said
```

Coverage is continuity. It produces *"the convoy we told you about this morning has docked"*
instead of the same paragraph twice, and across days it gives "still no word", "three days after",
"a week ago now".

### How `coverage` and `airplay` actually get written

`coverage` rows are written on air, and `airplay` drives every rotation separation rule and 45% of
the chart score. Neither can be written by the Transmitter, which has no database. **The Studio
polls.**

A one-minute poller on the Studio reads the Transmitter's `now.json` (published by Liquidsoap on
every element change, not only on playlist build — see §16) and writes what actually aired:

- element matches the built plan → promote the segment's `planned_coverage` into `coverage`, write
  `airplay` for any track, set `segments.aired_at`
- element came from fallback levels 2–5 → write `airplay` only, and mark the hour `off_plan`
- poller cannot reach the Transmitter → gap, backfilled on recovery from the Transmitter's own
  rolling `played.log`

Polling keeps the data direction push-only for *content* and read-only for *telemetry*, so the
Transmitter still needs no keys, no database and no outbound call to the Studio. Deriving airplay
from the built playlist instead would be free but wrong exactly when playout has fallen to
fallback — which is the state you least observe.

**Retention:** items 7 days. Everything else forever — threads, beats, coverage and quotes are the
world's history, and anniversary references ("a year ago this week, the Halcyon fire") are the
cheapest depth you will ever get.

---

## 7. Canon ingestion, validation, and seeding

Canon is **markdown in git**; the database is **derived and disposable**. That direction never
reverses.

```
canon/
  00-premise.md
  10-history.md
  15-figures.md
  20-geography.md
  30-finance.md
  40-music.md          ← artists, labels and scenes live here as prose
  ...
```

Each file carries YAML frontmatter:

```yaml
---
id: finance
domain: finance
scope: universe
status: active
supersedes: []
---
```

### `make canon-check` — the validation gate

**Where it runs.** The deterministic passes (1, 4, 5, 7) run on **pre-commit**, as
`canon-check --fast` — they need no model and finish in seconds, and they are listed among the
pre-commit hooks in §22. The model passes (2, 3, 6) need a loaded writer, so they run in the full
`make canon-check` on **pre-push**, and never inside `make check`, which stays fast and model-free
so the definition of done means the same thing on every machine. Putting seven passes with per-fact
LLM calls on pre-commit would violate §22's fast-hooks rule and get bypassed inside a week.

**Anything a model pass blocks, it blocks at push, not at commit** — including pass 3's summary
review. The wording matters because the two hooks are different gates.

Seven passes on the local model, cost zero:

1. **Parse & atomise.** Split into facts. **Identity and version are separate columns** —
   `fact_key` is the identity, `text_hash` is the version. There is no third column.
   `fact_key` comes from an explicit `#anchor` in the markdown, or is slugified from the fact's
   subject on first sight and then never changes. `text_hash` drives re-embedding **and
   contextual-prefix regeneration** — the prefix is part of the indexed text and must move with it.

   **Why not a SHA primary key:** if identity were the hash of the text, fixing a typo would
   create a "new" fact, retire the old one, and orphan every `coverage` and `quotes` row pointing
   at it — silently breaking continuity for material that has already aired. With the split, an
   edit is a version change and history survives. Where a fact is genuinely *replaced*,
   `supersedes` records it; retrieval reads active facts only, and historical coverage resolves
   through the supersession chain to render what was said at the time.

2. **Contradiction detection.** For each new or changed fact, retrieve the 8 most similar existing
   facts using the same hybrid retriever, then ask the model whether they conflict.

   **`canon-check` computes query embeddings ephemerally and does not persist them** — persistence
   is `canon-sync`'s job, and it runs after. Without this the dense half of the retriever has no
   vector for the new fact and pass 2 silently degrades to BM25-only, which is exactly when
   contradiction detection matters least and you would not notice. Output names
   both `fact_key`s and the nature of the clash.

3. **Domain summaries are pinned.** The summary prompt is versioned and frozen; each summary
   stores its prompt version and source tree hash. A summary regenerating in a different register
   shifts *every prompt in the station at once* — the highest blast radius of any change in the
   system.

   **A changed summary is an `error`, not a `warn`.** It blocks the **push** until the diff is
   reviewed and explicitly accepted (`make canon-sync ACCEPT_SUMMARIES=1`). The same applies to a
   canon edit pushing a domain's aphorism density above the ceiling. This is the one place a review
   gate earns its cost, because the alternative is the whole station's voice shifting as a side
   effect of fixing one paragraph.

4. **Link integrity.** Every referenced settlement, figure, faction, ship or year resolves to a
   known entity or is explicitly declared new in the same commit. Dangling references fail.

5. **IP / copyright screen.** String and fuzzy match against `banned-entities.yaml` (real
   franchises, trademarks, living authors' creations), plus a model pass asking whether any passage
   reads as derived from an identifiable existing work. Flags for adjudication, never auto-rejects.

6. **Register check.** Epigram density, banned abstractions, hedge rate. Applied to canon **because
   canon is what the world tick imitates** — fix the register at the source or every figure becomes
   an aphorist regardless of how the DJ cards are written.

7. **Timeline sanity.** No fact dated after in-world now; no birth after death; no settlement
   founded before the migration.

Output is `canon-report.md` — a derived artifact, gitignored like the rundown, and not one of the
six documents in §32. It carries severities. `error` blocks the commit; `warn` prints. Resolution
per conflict: **keep both** (compatible), **supersede** (new wins, old marked retired — never
deleted, because the world may already have aired it), or **edit**.

### Sync commands

| Command | Destructive? | Does |
|---|---|---|
| `make migrate` | no | Alembic schema only |
| `make canon-sync` | no | Idempotent upsert by `fact_key`; embeds changed only; regenerates affected domain summaries; marks removed facts retired |
| `make music-sync` | no | Idempotent upsert of artists/albums/tracks from `music/*.yaml`; ffprobes durations; flags orphans both ways |
| `make music-analyse` | no | Ramp/outro/bpm/energy analysis pass (§9) |
| `make grid-sync` | no | Programmes, dayparts, briefs, host rotas from `grid.yaml` |
| `make reset-world` | **yes** | Wipes threads/beats/items/coverage/charts only. Never touches facts, music, grid, cast, imaging. Typed confirmation, and refuses while any render job references rows it would wipe |

Everything a human edits is a file in git. Everything generated is in Postgres. That line is what
keeps the system understandable a year from now.

---

## 8. Music — the data model

Music is not files with tags; it is a discography that belongs to the world.

```sql
labels(id, name, settlement_id, founded_year, defunct_year, house_style)

artists(id, figure_id, name, kind, settlement_id, active_from, active_to,
        scene, bio, label_id)                    -- kind: solo|group|collective
artist_members(artist_id, figure_id, from_year, to_year, role)

albums(id, artist_id, label_id, title, release_year, kind, notes)
                                                 -- kind: album|ep|single|live

tracks(id, album_id, artist_id, title, track_no, duration_sec, file_path,
       mood text[], tempo, energy, language, category, licence_note,
       in_world_first_aired,
       intro_ramp_sec, outro_type, bpm, key)
                                                 -- category:   A|B|C|gold|new|specialist
                                                 -- outro_type: cold|fade|sustain

track_credits(track_id, figure_id, role)         -- writer, player, producer
airplay(id, track_id, aired_at, programme_id, context)
                                                 -- context: rotation | chart_clip | specialist
                                                 -- chart_clip counts for separation, NOT for
                                                 -- the chart score — see "The chart" below
chart_entries(chart_date, chart_id, position, track_id, prev_position, weeks_on, peak)
```

Three consequences worth the schema:

- **Artists are figures.** `artists.figure_id → figures.id`. A musician can die in a beat, be
  quoted in a bulletin, be someone's cousin, and have the back-announce pick it up automatically.
  That is what "baked into the reality" means concretely.
- **Albums carry in-world years**, so a DJ says "from their 2618 record on Halcyon Sound" without
  inventing it, and the tick can generate a beat — a label folds — that changes what the station
  can say about a back-catalogue.
- **Labels have a house style**, which gives scenes, rivalries, and a reason a specialist show
  exists.

### Rotation

- **Categories** with rotation weights: A (heavy), B, C, gold, new, specialist.
- **Separation rules** against `airplay`: same track ≥4h, same artist ≥60min, same album ≥90min,
  same label ≥30min.
- **Artist fatigue** alongside the hard rules — a decaying score incremented on every play,
  subtracted from selection weight rather than blocking outright. Hard rules prevent the audible
  clash; fatigue spreads a small catalogue evenly across days. Commercial schedulers all do this
  and it is what stops a small library feeling smaller than it is.
- **Daypart profiles** in `grid.yaml`: energy and tempo ranges per hour.

**Cold start.** At launch `airplay` is empty and a small catalogue cannot satisfy every rule. Do
**not** pre-seed synthetic airplay — airplay carries 45% of the chart score, so fake plays corrupt
the chart from day one. Relax in a fixed order, logging which rule dropped:

```
label ≥30m  →  album ≥90m  →  artist ≥60m  →  track ≥4h  →  random within category
```

`WARNING` on any relaxation. Persistent relaxation means the catalogue is too small for the
rotation weights — a real signal worth seeing rather than papering over.

### The chart

Computed nightly. Inertia is what makes it a chart rather than a random draw:

```
score = 0.45 · airplay(7d, decayed)     ← context != 'chart_clip'
      + 0.25 · in-world "requests"   (a generated figure with its own drift)
      + 0.20 · previous position
      + 0.10 · editorial nudge       (a beat: the artist died, the album dropped)
```

**The chart's own plays are excluded from the chart's score**, and this is not a detail. The Count
airs 20 tracks a week as clips; if those counted as airplay, this week's top 20 would arrive at next
week's calculation carrying 20 free plays each, and the chart would promote whatever it played until
nothing else could enter. That is a feedback loop, not inertia — inertia is the `previous position`
term, which is bounded at 0.20 and decays.

So `airplay` rows carry a `context`, and `context = 'chart_clip'` is written but not scored. The
rows still exist because rotation separation must know the track was heard (§8) — playing it again
an hour later is exactly the clash the separation rules prevent, whether the earlier play was a clip
or not.

Write the top 40 to `chart_entries` with `prev_position`, `weeks_on`, `peak`. The chart show then
gets movement language for free — "up four", "new entry at eleven", "a re-entry after nine weeks".
Tie it to beats: a death produces a catalogue re-entry, which is the kind of thing that makes a
fictional world feel like it has its own physics.

**Do not air a chart in the first two to three weeks.** It needs real airplay history to move
plausibly; launching on day one means inventing the movement, which is exactly the fabrication the
cold-start rule exists to prevent.

This is enforced in code, not by memory: the `chart` format declares `requires_airplay_days: 21`,
and `grid-sync` refuses to schedule it until `airplay` holds that much history. An instruction in a
document is not a control.

---

## 9. Station imaging

Imaging is most of what makes audio sound like *radio* rather than a podcast with music after it,
and it is the cheapest content in the system: rendered once, reused forever, zero recurring cost.
Generate the sung station-name pieces in Suno alongside the music.

```sql
imaging(id, kind, file_path, duration_sec, programme_id null,
        bed_loop_sec, intro_ramp_sec, energy, tags text[])
```

| `kind` | Use |
|---|---|
| `sonic_logo` | 2–3s station signature, at joins |
| `programme_open` / `programme_close` | Per-show top and tail |
| `news_sting` / `news_bed` | Junction furniture; the bed ducks under speech |
| `sweeper` | Short voiced transition between items |
| `bumper` | Into and out of a music block |
| `bed` | Loopable underlay for links |
| `time_sting` | Under the time check |
| `disclosure_sting` | Compliance ident — hard-scheduled hourly (§18) |
| `chart_marker` | Position markers in the chart show |

**Placement is declarative per programme** — what radio calls the hour clock — so imaging is
config, never logic:

```yaml
evening_report:
  open: evening_open              # 14s, sung station name over a bed
  bed_under_links: report_bed
  sweeper_every_n_items: 2
  close: evening_close
news:
  sting: news_urgent              # 4s
  bed: news_bed_loop              # ducks to -12 dB under speech
  disclosure_sting: ai_ident
```

**Hitting the post.** `tracks.intro_ramp_sec` records the instrumental run-up before the vocal
enters; the mixer times the DJ's link to end just before it. Mechanical once the field exists, and
the single production detail that most separates real radio from a playlist. `outro_type` does the
same at the other end: `cold` means the mixer must not talk over the ending, `fade` and `sustain`
mean it can.

**Data prerequisite:** `intro_ramp_sec`, `outro_type`, `bpm`, `energy`, `mood` per track.
`ffprobe` gives duration; the rest is a one-time librosa pass (`make music-analyse`) plus **manual
correction of the ramps by ear**. Onset detection gets the ballpark; the difference between a link
that lands and one that clips the vocal is about half a second, and that is a listening judgement.

Imaging is exempt from the safety gate (hand-curated, not generated per air) but **not** from the
IP screen — run the banned-entity pass over imaging titles and any sung lyrics.

### The mix specification — how the hour clock is executed

The hour clock in `grid.yaml` is data; this is the algorithm that reads it. `mix.py` assembles a
finished programme from rendered turns, imaging and music in one deterministic pass.

**Assembly order for a floating show:**

```
1. programme_open              full level, from imaging
2. crossfade -1.5s into
3. link 1 (turns)              bed_under_links loops beneath at -12 dB
                               bed fades in 0.8s before speech, out 1.2s after
4. music slot 1
   ├ ramp_talk?  speech starts at track_start, must end by intro_ramp_sec
   ├ track plays at full level, bed muted
   └ outro_type == cold  → hard stop, 0.3s gap, next element
      outro_type == fade → back-announce may begin 4s before end over the fade
      outro_type == sustain → back-announce over the final 6s
5. every Nth item              sweeper at full level (sweeper_every_n_items)
6. …repeat…
7. programme_close             crossfade -2s
```

**Junction assembly** is different and stricter, because it is pinned:

```
1. news_sting                  full, 4s, no crossfade — a hard start marks the hour
2. bulletin turns              over news_bed at -12 dB
3. disclosure turn             over bed, or dry — never omitted (§11 invariant 3)
4. time check
5. trail for what follows
6. bed tail                    1.5s, fades to silence
```

**Rules the mixer enforces, not the writer:**

| Rule | Value |
|---|---|
| Speech peak | normalised to the target LUFS before any bed is added |
| Bed under speech | −12 dB, with 300ms attack / 800ms release ducking |
| Gap between turns, same speaker | 180 ms |
| Gap between turns, different speakers | 320 ms |
| `overlap_prev_ms` | applied as a negative offset, capped at −600 ms |
| `pause_before_ms` | inserted silence, capped at 2500 ms |
| Crossfade into/out of imaging | 1.5 s, equal-power |
| Total programme loudness | re-normalised after mixing, then measured with ffmpeg |

Every element's final offset is written to the **cue sheet**, which is what the timed-assembly
conformance test (§3) asserts against and what `now.json` uses to report what is playing inside a
programme.

**Imaging selection is deterministic but not repetitive:** where a slot allows several pieces
(sweepers, idents), choose round-robin by last-used timestamp rather than at random. Random
selection audibly clusters.

---

## 10. Music shows

### Render economics — this is the capacity lever

| Show type | 60 broadcast minutes contain | Speech to render |
|---|---|---|
| Talk magazine (28 min) | ~21 min speech | ~21 min |
| Music show (56 min) | 14 tracks + links | **~6 min** |
| Chart show (28 min) | 20 positions, tracks played as clips | ~15 min |

**A music hour costs roughly a seventh of the render time of a talk hour** — ~6 speech-minutes
against ~42. On TTS-bound hardware this moves the broadcast day further than any pipeline
optimisation, and it is also what sets the archive pool's build cost (§14). When you run short of
render capacity, the answer is usually a different grid, not a faster engine.

**The chart is the exception among music formats.** 20 positions in 28 minutes means tracks are
played as clips of roughly 30–40 seconds, not in full, and the speech-to-music ratio is closer to a
talk show than a music show. A clip is still an `airplay` row with `context = 'chart_clip'`, because
rotation separation must know the track was heard — but it is **excluded from the chart score**, or
the chart would feed on its own output (§8).

### Generation order

**Rotation runs before the writer**, because links reference specific songs:

```
rotation → 14 tracks (separation rules, daypart energy, artist fatigue)
   ↓
context = the tracks, joined to their full discography:
          artist · album · in-world year · label · scene · credits
          + figures linked to those artists
          + beats/threads touching them
          + anniversaries falling this week
   ↓
one call → script with links positioned between tracks
```

**Four link types**, declared in the script schema so the writer has somewhere to put each:

- `back_announce` — what just played, with one fact
- `forward_tease` — what is coming
- `ramp_talk` — timed against `intro_ramp_sec`, must end before the vocal
- `story_link` — the connection to the world

### Music as part of the world

The joins exist in §8; using them is what stops the discography being a reference table. The
nightly tick treats **music as a domain like any other** — a label folds, a tour is cancelled, a
lost recording surfaces, a feud starts. Without music beats the catalogue is static while the rest
of the world moves, and the seam shows.

### Specialist shows — the best archive content available

A label retrospective, an artist profile, the story of one album. Deeply uses the discography,
entirely time-neutral, therefore floating-class and ideal for the overnight block. Highest quality
per render-minute in the system, and the natural way to pre-build the archive before launch.

---

## 11. Shows — one call, N speakers

### Cast and roles

```sql
cast(id, name, persona_card, stance, blind_spot, personal_thread,
     beat, reference_clip_path, seed, active)
     -- beat: the domain a correspondent owns (politics, sport, conflict…), null
     --   for strand hosts. A correspondent appears wherever their domain does —
     --   bulletin, two-way, their own programme. See PROGRAMMING.md §5
     -- reference_clip_path: the WAV is canonical, never a vendor voice id (§3)
cast_profiles(cast_id, kind, profile jsonb, version)
     -- kind: conversational | scripted. A person may hold both (§11a)
programme_hosts(programme_id, cast_id, role, weight)
     -- role: anchor | co_host | correspondent | guest | chart_voice | newsreader
```

Two, three or more speakers are all supported because rendering is per-turn (§12). Practical
guidance: 2 is the default for conversation, 3 works for a panel if one has a clearly subordinate
role, 4+ becomes mush without visual cues. Cap at 3 **in conversation**, with `discussion` the one
declared exception at 4 — a host plus three figures, and no further.

**The cap counts voices in dialogue, not voices in an item.** `vox` runs 3–5 speakers and `package`
runs a narrator plus clips, and neither breaches it: those voices never address each other, they are
sequential monologue cut together. What the cap prevents is four people talking at once, which is
where a listener with no faces to look at loses track of who is speaking.

### Personality is five concrete things, not adjectives

1. **A stance** — what they think the world is about, stated once in the card.
2. **A blind spot** — something they are reliably wrong about. Disagreement between hosts is what
   makes dialogue instead of alternating monologue.
3. **A running personal thread** — a sibling on a slow ship, a boat being rebuilt, a feud with a
   supplier. Two lines a week, referenced across months. This does more for the illusion of a
   person than any register instruction.
4. **Memory** — their own coverage log: what they said, what they got wrong, what they promised to
   follow up. Fed back into their next show.
5. **A speech profile** — how they hedge, interrupt, trail off, disagree and handle silence, stored
   per presenter and never regenerated. See §11a; this is what stops all the DJs sounding like one
   person with different names, and what stops any one of them drifting between shows.

### A programme is a running order, not a conversation

**This is the correction that matters most in this section.** Real radio programmes are containers
of short items linked by a host. A 28-minute magazine is six to eight items of two to five minutes
each, not one long conversation. Two presenters talking continuously for twenty minutes is not a
format; it is what happens when nobody decided on a format.

The number of voices is therefore a property of the **item**, not the programme. Most items have
one voice. The most common multi-voice item in all of radio is the **two-way** — anchor asks,
correspondent answers, two to four minutes — not two co-hosts in dialogue.

**Item types**, with their real durations:

| Item | Voices | Duration | Notes |
|---|---|---|---|
| `link` | 1 (host) | 20–60 s | The connective tissue. Most of a host's airtime is links |
| `bulletin_story` | 1 (newsreader) | 20–40 s | 4–6 per bulletin |
| `two_way` | 2 (host + correspondent) | 2–4 min | The workhorse of news radio |
| `package` | 1 narrator + clips | 3–5 min | Correspondent narrates; figures speak in short clips |
| `interview` | 2 (host + figure) | 5–10 min | 10 only for a serious story |
| `vox` | 3–5 one-off voices | 60–90 s total | Settlement voices, 15–20 s each |
| `discussion` | 1 host + 2–3 figures | 8–15 min | The only genuinely multi-party item; the one exception to the cap of 3 |
| `talk` / `essay` | 1 | 5–10 min | Single voice, written to be read |
| `feature` | 1 narrator + clips | 15–30 min | Documentary. The overnight backbone |
| `music_link` | 1 | 20–60 s | Timed against `intro_ramp_sec` |
| `chart_item` | 1 | 30–60 s | Position, movement, one fact |
| `letter` | 1 | 60–90 s | In-world correspondence, read by a host |
| `weather` / `travel` | 1 | 30–60 s | Pool-class, short |

**Programme types** are containers with a declared item mix:

| Programme | Duration | Shape |
|---|---|---|
| `bulletin` | 4 min | 4–6 `bulletin_story`, one newsreader, no links. Overnight: ~2 min of speech in the same slot |
| `magazine` | 28 or 56 min | Host links + 6–8 mixed items per act. The default talk format |
| `newsreel` | 28 min | Dispatches: `two_way` and `package`, lightly linked |
| `interview_programme` | 28 min | One long `interview`, topped and tailed |
| `discussion` | 28 min | One `discussion` item plus links |
| `feature` | 28 or 56 min | One `feature`, single narrator. Time-neutral, archive-bound |
| `music_show` | 56 min | Heritage/specialist, overnight only. ~6 min speech/hour |
| `chart` | 28 min | `chart_item` + tracks. 20 positions counted down |
| `music_sequence` | 56 min | **Overnight archive block only.** Tracks with a link every 2–3 |
| `news_programme` | 28 min | A bulletin expanded: headlines, then two-ways and packages. Junction-class (states the time), pinned |

Which format suits which subject, and when it airs, is editorial rather than architectural — see
`docs/PROGRAMMING.md`, which maps the station's seventeen domains onto these containers by rate of
change.

**Three slot lengths, and the cap is on the generation call rather than the programme.**

The grid uses **4**, **28** and **56** minutes only (`PROGRAMMING.md` §7). Acts are a
**generation-time concept only** — one segment, one audio file, one cue sheet, and nothing
downstream knows a programme was written in two passes. A 56-minute magazine is ~42 minutes of
speech, which exceeds the ~25 minutes one generation call produces reliably — so it is written as
**two acts** (§11's act mechanism), each ~21 minutes of speech, the second seeing the first.
Because `56 = 2 × 28`, an act is exactly a short programme and the mixer has no special case.

| | Speech | Clock | Generation |
|---|---|---|---|
| Bulletin | 4 min | 4 min | one call |
| Overnight summary | ~2 min | 4 min | one call |
| 28-min programme | ~21 min | 28 min | one call |
| 56-min programme | ~42 min | 56 min | **two acts** |
| Music-led (overnight) | ~6 min/h | 56 min | one call |

**The 2-act cap on 16GB (§11) puts a hard ceiling of ~50 minutes of speech on any single
programme.** A 56-minute slot needs ~42, so there is roughly 8 minutes of margin and no more — 56
is the longest slot the hardware supports, and a longer strand must be split into separate
programmes with their own bulletins between them, which is what `First Shift` does across
06:00–09:00.

**This is a speech station. Music does not fill gaps.** Every minute of the broadcast day belongs to
a named programme; there is no default filler layer. The only music in the daytime is the chart
programme, and `music_sequence` exists solely for the overnight archive block (01:00–05:00) where it
is scheduled explicitly like anything else.

An unassigned minute in the grid is therefore an **error at sync time**, not a gap to be filled. A
schedule that auto-fills with music is how a speech station silently becomes a music station —
which is exactly what the earlier version of this document did.

**A solo host is the norm.** Two co-hosts is a specific breakfast/drive convention, not a default,
and even there the programme is built from short items.

### The script schema

```python
@dataclass
class Turn:
    speaker_id: int
    text: str
    emotion: str | None          # warm|wry|somber|bright|urgent
    nonverbal: str | None        # laugh|half_laugh|breath|sigh
    overlap_prev_ms: int = 0     # negative gap — this speaker cuts in
    pause_before_ms: int = 0
    trail_off: bool = False

@dataclass
class MusicSlot:
    position: int
    track_id: int | None         # null = rotation fills at build time
    link_type: str               # back_announce|forward_tease|ramp_talk|story_link

@dataclass
class Item:
    kind: str                    # link | two_way | package | interview | vox | ...
    voices: list[VoiceSlot]      # who speaks in THIS item — usually one
    turns: list[Turn]
    est_duration_sec: int
    covers: list[int]            # beat_ids this item addresses

@dataclass
class VoiceSlot:
    role: str                    # host | correspondent | guest | vox | narrator
    cast_id: int | None          # a station presenter…
    figure_id: int | None        # …or a world figure appearing as a guest (§3)
    register_kind: str           # derived from role, not from the programme (invariant 7)

@dataclass
class Script:
    programme_id: int
    programme_type: str          # bulletin | magazine | feature | music_show | ...
    format_class: str            # junction | floating
    items: list[Item]            # THE RUNNING ORDER — the unit of a programme
    music_slots: list[MusicSlot]
    planned_coverage: list[PlannedCoverage]   # promoted to `coverage` only on air (§6)
    est_duration_sec: int
```

The overlap and nonverbal fields are not decoration. Without a field for interruption there is
nowhere for interruption to exist, and **no prompt can conjure it** — a turn generated in its own
call is always a complete, well-formed utterance, and people do not produce those.

### Generation

One call per programme, producing the whole script — every turn, both hosts, links into and out of
music, the sign-off. This removes looping and inter-segment incoherence by construction rather
than by gate.

Input: Tier 0 core + Tier 1 domain summaries + Tier 2 retrieved facts + Tier 3 world slice + last
24h coverage + the programme brief. **The brief is where cross-domain connection comes from** —
one authored sentence per programme: *"Ice & Iron treats results as economics and politics."*
Retrieval cannot manufacture an editorial stance.

**Length budget.** A 20-minute talk segment is ~3,000 words ≈ 4,000 output tokens — comfortable. A
50-minute programme is not: ~10,000 output tokens is beyond what a 9–10B model produces reliably.
**Cap a single generation call at ~25 minutes of speech.** Longer programmes are generated as
**acts within one conversation**, each act seeing what came before — one context, one cache prefix,
sequential calls. Coherence is preserved without requesting a length that degrades.

**Context budget, because KV growth is what pressures 16GB.** The assembled context is capped at
**24k tokens** and the cap is enforced by trimming Tier 3 (world slice) first, then Tier 2
(retrieved facts) — never Tiers 0 or 1, which are the stable cached prefix and the source of the
world's shape.

**`context_mix` sets the Tier 2 : Tier 3 split** before either is trimmed. A history feature at
`{canon: 0.8, world: 0.2}` gets 32 canon facts and 8 world entries; a politics magazine at
`{canon: 0.3, world: 0.7}` gets the reverse. Getting this wrong is the most common cause of a
programme coming out flat — a slow-domain show fed mostly world state has nothing to say, and a
fast-domain show fed mostly canon sounds like a lecture.

**Tier 2 has a floor of 12 facts.** Twelve, not fifteen, because `context_mix` 0.3 — the standard
fast-domain ratio (`PROGRAMMING.md` §1) — allocates exactly 12, and a floor that every politics,
finance and sport programme breaches on allocation is not a floor. If trimming would go below it —
which happens at act 2 with the carried summary and verbatim tail — the assembler logs WARNING and
surfaces it in the rundown. A silently starved retrieval slice looks exactly like a model that has
stopped using the canon, and you would spend a week blaming the prompt.

Acts compound this: each act carries what came before. On 16GB, **cap at 2 acts** (~42 minutes of
speech, which is exactly a 56-minute slot), and have act 2 receive act 1 as **a 300-word summary
plus the last 800 words verbatim** rather than the whole text. The verbatim tail is what preserves the handover and the running thread; the
summary is what preserves the argument. Measure this at step 1 before relying on it.

**Output validation** — schema, plus seven structural invariants:

1. **Duration consistency.** Σ turn durations + Σ music slot durations ≈ `est_duration_sec` within
   10%. Catches the model losing the thread of a long script.
2. **No clock tokens in a floating show** (§13), by regex.
3. **Junction formats must contain a disclosure turn.** Required field of the junction schema, not
   a prompt request. Compliance cannot depend on a model remembering.
4. **Every claimed fact traceable** to something in the assembled context.
5. **Ramp talk fits.** Any `ramp_talk` link's estimated duration ≤ the track's `intro_ramp_sec`.
6. **The running order matches the declared `item_mix`** — right item kinds, right counts, each
   within its duration band. A magazine that came back as one long conversation fails here, which is
   the specific failure this invariant exists to catch.
7. **Register kind matches the slot's role, not the programme.** Each `VoiceSlot` carries its own
   `register_kind`, derived from `role`: `host` inherits the programme's kind; `correspondent` and
   `newsreader` are always `scripted`, including inside a conversational magazine; `guest` and `vox`
   sit mid-band `conversational`. `programmes.register_kind` is the default a `host` inherits, not a
   constraint on the programme. A `scripted` slot containing a `nonverbal`, a
   `trail_off`, or an `overlap_prev_ms` fails validation outright — those fields have no meaning in
   read copy and their presence means the wrong profile was loaded.

Failure gets one repair attempt with the validation error appended, then the job fails and the slot
falls to **archive** — never to the pool, which is sized for back-timing residue (§13) and cannot
fill a programme-length hole. The repair response is validated identically.

---

## 11a. Register, direction, and the voice of the world

This is the product. Everything else in this document exists so that this section can work.

Three separate problems get confused constantly, so name them: **what the words are** (register),
**how they are performed** (direction), and **whether the world sounds like itself** (DNA). Each has
a different mechanism and each fails differently.

### The register spec — station bounds, not station targets

`prompts/register.md` is included in Tier 0 and ships on every call. It defines what **human speech**
is, which is a property of people in general, not of any one presenter. Real transcribed speech is
full of repair, hedging and abandoned sentences; a model asked to "write dialogue" produces none of
it, because it is trained on written prose. It must be asked explicitly, with numbers.

But the numbers are **bounds, not targets**, and the bounds depend on what kind of speech it is.
Conversation and prepared copy are different registers, not points on one scale — a newsreader
reading a bulletin has essentially no disfluency, and that is correct rather than a failure.

Every profile therefore declares a `kind`:

| Property | `conversational` floor–ceiling | `scripted` floor–ceiling |
|---|---|---|
| Hedges per 1,000 words | 15 – 70 | **0 – 3** |
| Contractions (of eligible) | 80% – 100% | 40% – 70% |
| Sentences over 25 words | – 15% | – 8% |
| Turns with interruption or overlap | 1 in 20 – 1 in 4 | **0** |
| Turns that trail off | 1 in 30 – 1 in 8 | **0** |
| Nonverbals (laugh, breath, sigh) | as profiled | **none permitted** |
| Aphorisms per show | – 1 | – 0 |
| Banned abstract nouns | – 0 | – 0 |

Only the aphorism ceiling and the banned-noun rule are absolute across both. Everything else is a
band the presenter sits somewhere inside, permanently.

### The speech profile — how each DJ is a different person

A station-wide number produces one speaker wearing several names. Worse, without a stored profile
the same presenter drifts between shows, because nothing anchors them. So the profile lives on the
`cast` row, is written once by you, is versioned, and **is never regenerated**:

```sql
cast(id, ...)                                              -- the person
cast_profiles(cast_id, kind, profile jsonb, version)       -- kind: conversational | scripted
```

```yaml
# Wren — the anchor
rates:
  hedges_per_1000: 22            # low: she commits to statements
  interruption_rate: "1 in 6"    # high: she cuts in constantly
  trail_off_rate: "1 in 25"      # low: she finishes her sentences
  long_sentence_pct: 6
habits:
  hedge_forms: ["I mean", "sort of", "look"]   # NOT "kind of", NOT "I guess"
  sentence_shape: "short declaratives, then one long qualifying clause"
  tic: "restates the question before answering it"
  disagreement: "goes quiet, then contradicts flatly"
  silence: "comfortable — lets a beat sit"
  vocabulary: "concrete, port and logistics register; avoids abstraction"
  laughs: "rarely, and short"

# Adu — the co-host
rates:
  hedges_per_1000: 48            # high: he thinks out loud
  interruption_rate: "1 in 14"
  trail_off_rate: "1 in 9"       # high: abandons threads mid-sentence
  long_sentence_pct: 13
habits:
  hedge_forms: ["kind of", "I guess", "right?", "or — no"]
  sentence_shape: "long, self-correcting, arrives at the point late"
  tic: "answers with a question first"
  disagreement: "over-agrees, then undermines"
  silence: "fills it"
  vocabulary: "reaches for metaphor, gets it slightly wrong"
  laughs: "often, at his own lines"
```

### The news register

News is `kind: scripted`, and it is genuinely a different job. A bulletin is **read**, not spoken:
the copy exists before the microphone opens, so there is nothing to hesitate about.

```yaml
# Sella — newsreader
kind: scripted
rates:
  hedges_per_1000: 0
  interruption_rate: 0
  trail_off_rate: 0
  long_sentence_pct: 5
habits:
  sentence_shape: "one idea per sentence; attribution first, claim second"
  tense: "present and present-perfect — 'the council has voted', not 'voted'"
  voice: "active; the actor before the action"
  numbers: "rounded and spoken — 'about four hours', never '4h 12m'"
  attribution: "always named before the claim, never after"
  pace: "steady; sentence-final falling intonation"
  vocabulary: "plain, unhurried, no metaphor, no editorial adjectives"
  laughs: never
```

**The copy is written differently, not just performed differently.** Broadcast news style is a
writing constraint the prompt must carry explicitly, because a model left alone will produce
newspaper prose — subordinate clauses, buried attribution, past tense:

```
Newspaper:  "Following a lengthy debate over the tariff proposal, which had been
             delayed twice, the council voted 7-4 in favour late on Thursday."

Broadcast:  "The council has passed the tariff. The vote was seven to four.
             It came after two delays and more than three hours of debate."
```

Short sentences, one idea each, attribution and actor first, present perfect. This is a
well-established craft and worth writing into `prompts/news_register.md` as its own file.

**Delivery differs too**, and it flows through the direction layer: `emotion` is restricted to
`neutral | grave | brisk`, `nonverbal` is rejected by schema validation, and the engine's
exaggeration parameter sits low and constant. A newsreader who varies their delivery per sentence
sounds unreliable, which is the opposite of what the format needs.

**One person may hold two profiles**, because a DJ handing to the news and a DJ reading a short
bulletin are both normal radio:

```sql
cast_profiles(cast_id, kind, profile jsonb, version, PRIMARY KEY (cast_id, kind))
```

The profile is selected by the **role of the voice slot** (§11 invariant 7), not by the person and
not by the programme. A junction
selects `scripted`; a floating show selects `conversational`. A presenter with no profile for the
kind a format requires is a `grid-sync` error.

**The handover is where the two registers meet**, and it is worth writing deliberately: the DJ's
last line is conversational, the newsreader's first line is not, and the sting sits between them.
That contrast is a large part of why a station sounds like a station.

> **A safety note that follows directly from this.** A credible, professionally-read news register
> makes invented news sound *more* like real news, which raises rather than lowers the bar on
> disclosure (§18, §19). The fiction statement inside a junction must be unmistakable precisely
> because the surrounding delivery is convincing. Do not let the news voice read the disclosure in
> a way that makes it sound like a legal formality.

**Rates alone are not enough.** Two presenters at 30 hedges per 1,000 sound identical if they hedge
the *same way*. `hedge_forms` is therefore an allowlist per DJ and the forms must not overlap
between co-hosts — that single field does more for distinctiveness than any rate.

The profile is injected into the cast card in Tier 0, so it ships on every call the presenter
appears in. That is what makes them the same person on Tuesday as on Monday.

### Contrast is a property of the pair, not the person

Two well-drawn presenters can still be indistinguishable if they were drawn along the same axes. So
`programme_hosts` carries a check at `grid-sync` time: **conversational co-hosts must differ by at
least 15 hedges per 1,000 words in absolute terms, must not share a `hedge_form`, and must not
share a `disagreement` mode.** Two different things are called separation and they are not the same check: **profile separation**
is validated at `grid-sync` against the authored numbers, while **output separation** is measured on
generated scripts and reported in the rundown. The first is a gate; the second is a trend.
(Scripted profiles are exempt — newsreaders are supposed to sound alike;
that is what makes the format recognisable.) A pair failing this is a config error, reported before it ever reaches air.

The natural pairing is opposition — a committer against a qualifier, a finisher against a
trailer-off. That is where dialogue comes from, and it is the same principle as the `blind_spot`
field in §11.

### Context modifiers

The same person is not the same at 07:00 as at 23:00, or when the story is a death rather than a
tender. Modifiers are applied to the profile at generation time, never baked into it:

| Context | Effect |
|---|---|
| Overnight / late programmes | hedges ×1.2, interruptions ×0.6, longer pauses |
| Breaking or grim story | hedges ×0.7, trail-offs ×0.5, shorter sentences |
| Solo presenting | interruptions → 0, trail-offs ×1.3 (nobody to catch them) |
| Chart and light music shows | laughs ×1.5, hedges ×1.1 |

**Modifiers multiply, then clamp to the band.** Overnight × solo × breaking compose
multiplicatively, and the result is clamped to the `conversational` floor and ceiling so no
combination can push a presenter outside the human range. **One exemption: solo presenting sets
interruptions to a true zero and the clamp does not restore them** — there is nobody to interrupt,
so the floor is meaningless rather than protective. Modifiers apply to `conversational`
profiles only. A scripted profile does not loosen at 23:00 —
consistency is the point of the register.

### Measurement follows the same shape

Register metrics are computed **per presenter, against their own profile**, and reported in the
rundown (§14a) as deviation rather than as an absolute:

```
Register  Wren  hedges 24/1000 (profile 22, +9%) · interrupts 1 in 7 · trail-offs 1 in 22
          Adu   hedges 44/1000 (profile 48, −8%) · interrupts 1 in 15 · trail-offs 1 in 10
          ⚠ separation 20pp (floor 15pp) — OK
```

A presenter drifting persistently toward the station mean is the signal that matters: it means the
model is regressing to a generic voice and the profile is not carrying enough weight in the prompt.

**How each metric is computed**, because canon-check pass 6 depends on it:

| Metric | Method |
|---|---|
| Hedges | count of that presenter's own `hedge_forms` allowlist, per 1,000 words |
| Contractions | regex over an eligible-pair list |
| Sentence length | tokenised split |
| Banned abstractions | `config/banned-abstractions.yaml` wordlist — deterministic, no model |
| Aphorism density | one small-model pass per 500 words: *"how many sentences here are general maxims about life rather than statements about this world?"* Returns an integer; the only model-dependent metric here |

**None of this is asserted as a test.** A build failing because a script came in 4% under a hedge
target would be a harness grading its own output (§34). You read the deviation; you decide.

### The distinctiveness check

The real test is not numeric. Take two turns from a show, strip the speaker names, and ask whether
you can tell who is who. If you cannot, the profiles are decorative regardless of what the metrics
say. This belongs on the panel's blind sample screen alongside the quality thumbs.

### Examples, not adjectives

Every profile carries two or three lines *in that presenter's voice* — the prompt learns more from a
sample than from a description, and it is the cheapest way to stop drift:

```
Generic:  "The convoy arrived four hours late. Port authority blamed the relay."

Wren:     "Convoy's in. Four hours late, and the port's blaming the relay again."
Adu:      "So it's — the convoy, right, it's in, but late, kind of significantly?
           And the port's saying relay, which, I guess, sure. Again."
```

### The direction layer

The `Turn` schema (§11) is the *container* for performance. The prompt must be told to fill it, and
the engine adapter must be told what to do with it. Both halves are required — a field nothing
writes to is decoration, and a field nothing renders is worse.

**What the writer is asked for**, per turn: `emotion` from the fixed vocabulary; `nonverbal` where a
laugh or breath genuinely belongs; `overlap_prev_ms` when this speaker cuts in; `pause_before_ms`
when someone is thinking; `trail_off` when the thought is abandoned. The prompt states the target
frequencies from the table above, so the model has a quota rather than a vague encouragement.

**How each field reaches the engine:**

| Field | Chatterbox | Qwen3-TTS | Kokoro |
|---|---|---|---|
| `emotion` | `exaggeration` scalar, mapped per value | natural-language direction prepended | ignored |
| `nonverbal` | inline `[laugh]` / `[chuckle]` tag | direction text ("with a short laugh") | **stripped**, never spoken |
| `trail_off` | text ends with "…", exaggeration −0.1 | direction text | text ends with "…" |
| `overlap_prev_ms` | **mixer, not engine** | mixer | mixer |
| `pause_before_ms` | **mixer, not engine** | mixer | mixer |

Two things to note. **Timing is always the mixer's job**, never the engine's — that is what makes it
deterministic and testable. And **Kokoro strips nonverbals rather than reading them aloud**: an
engine that would speak the word "laugh" is worse than one that drops it, which is exactly the kind
of vendor difference the capability struct exists to absorb.

The emotion mapping table lives in the adapter, not in shared code. `warm → 0.45`,
`wry → 0.55`, `urgent → 0.75` for one engine is meaningless to another.

### How the canon's DNA reaches the microphone

The "spirit" question has a concrete answer: it travels through **three channels, and all three
must be maintained or the world sounds generic.**

**1. The always-resident tiers (§5).** Station core plus every domain summary ship on every call.
This is why a DJ can gesture at the war or the tariffs without those facts being retrieved — the
model knows the world's shape at all times. Flatness is almost always a Tier 1 problem.

**2. The register check applied to canon itself (§7, pass 6).** This is the non-obvious one and the
one that actually bit last time. The world tick imitates the canon it reads. If the bible is written
in epigrams, every generated figure becomes an aphorist, every quote becomes a maxim, and no amount
of DJ-card instruction will fix it downstream. **Fix the register at the source.**

**3. The cast card and the programme brief.** The card carries stance, blind spot and personal
thread (§11); the brief carries editorial stance in one authored sentence. Retrieval cannot
manufacture a point of view — it can only supply material for one that already exists.

There is a fourth channel worth naming because it is easy to lose: **the world tick's own prompt**
needs the register spec too. Beat headlines and figure quotes are written by the same model and end
up quoted verbatim on air.

### What no prompt can fix

Three failures live in structure, not wording, and hammering the instructions will not reach them:

- **Separate calls cannot interrupt each other.** A turn generated in its own call is always a
  complete, well-formed utterance. Whole-show generation (§11) is the precondition for overlap
  existing at all.
- **A schema without a field has nowhere to put the behaviour.** No prompt yields `trail_off` if
  `Turn` lacks it.
- **An engine without tags renders a perfect script flat.** This is why Kokoro is never *scheduled*
  (§2) regardless of how good the writing is, and why a night that spills to it is marked degraded
  rather than treated as a normal night.

### The one measurement that counts

None of the above proves the station sounds human. **The blind sample on the panel does** — three
recent segments, unlabelled, thumbs up or down. Everything in this section is instrumentation for a
judgement that stays yours (§29, §33).

---

## 12. Voice pipeline

```
Script.turns ──▶ render_queue (priority) ──▶ TTS worker ──▶ per-turn wav
                                                                │
                        assemble: overlaps as negative offsets, │
                        pauses as silence, loudness-normalise ◀─┘
                                                     │
                        mix: imaging per the hour clock, bed under
                        speech (-12dB duck), sting at junctions,
                        music slots with ramp timing
                                                     │
                        ffmpeg → show.mp3 @ 128kbps + cue sheet JSON
                                                     │
                        C2PA manifest written (§18)
```

- **Per-turn rendering is the default**, and the capability is what selects it:
  `engine.capabilities.max_speakers_per_call > 1` takes the one-pass dialogue path, everything else
  renders per turn. Today every configured engine is 1, so the branch always falls through — but it
  is a live branch with a conformance test, not a decorative field (§3).
- **Batch by voice.** Turns are independent, so group them by speaker and submit in batches — this
  is the single highest-leverage implementation detail in the pipeline and the difference between
  a full broadcast day being feasible and not.
- **Trailing-artifact check.** Some engines add artifacts at the end of longer generations. Assert
  trailing audio energy is below a threshold on every rendered turn; re-render once on failure.
- **Priority:** junctions before floating shows. Every job has a wall-clock timeout — an unbounded
  hang is worse than a crash because nothing alerts on it.
- **Two lanes:** Chatterbox for cast voices; Kokoro for emergency spill only. If the Chatterbox
  lane trips its circuit breaker (§25), jobs spill to Kokoro rather than to silence.

---

## 13. The clock contract

The load-bearing rule. Everything about scheduling follows from it.

**Class is about the clock, not about length.** A 28-minute news programme is junction-class because
it states the time; a 56-minute magazine is floating-class because it must not.

**"Junction-class" and "the pinned `:00` junction" are two different things** and the shared word
causes trouble. *Junction-class* is a content property: this format may state the time and is
generated for D+1. *Pinned* is a playout property: Liquidsoap starts this element at a wall-clock
instant regardless of what is playing. **Only the `:00` junction is pinned.** `The Six` at 18:04 is
junction-class and not pinned — it states the time, is written for D+1, and is scheduled behind the
18:00 junction like any other programme.

| Class | May state the time? | Generated for | Reused | Examples |
|---|---|---|---|---|
| **Junction** | Yes, must | **D+1** | never | 4-min bulletin, 2-min summary, **28-min news programmes** (`The Six`, `The Midnight Report`), time check, handover, disclosure |
| **Floating** | **Never** | **D+2** | archive after 30d | shows, features, chart shows, interviews, music shows |
| **Pool** | No | once | constantly | idents, generic trails, in-world weather, archive quotes, imaging |

Floating shows may reference *events* ("the convoy that came in late") because events are anchored
to the world, not the clock. They may not reference the clock itself. Enforced by one regex
acceptance test; failure regenerates.

### Timezone

**The Transmitter runs UTC and pins junctions against UTC instants.** `clock.py` on the Studio
converts to Europe/Warsaw only when rendering in-world phrases; the playlist builder emits pin times
as UTC. Two machines each doing local-time arithmetic is how you get an hour of silence twice a
year.

### Junctions are pinned to the wall clock

Each hourly junction is **hard-scheduled by Liquidsoap against the wall clock at `:00`**, not
queued behind whatever is playing. It may state the time freely because it plays at a fixed instant
regardless of what came before.

**Drift therefore cannot accumulate**, because every hour resets at a pinned junction. If a show
overruns it is faded under the news sting — which is what every real station does. If it underruns,
the pool fills the gap.

```
07:00:00  JUNCTION  pinned   news bulletin + time + disclosure   4:00
07:04:00  imaging   programme open                              0:15
07:04:15  SHOW      floating, no clock references, 56-min slot 54:45
07:59:00  pool      BACK-TIME 1:00 — trail or ident             1:00
08:00:00  JUNCTION  pinned   news bulletin
```

An hour running two 28-minute programmes hands straight from one to the next at `:32`; there is no
mid-hour summary. **The back-time gap is small — a minute or two — because slots are fixed
lengths**, which is the point of having only three of them. The pool absorbs the residue, not a
music bed.

**Back-timing:** the playlist builder sums measured durations (ffprobe, never metadata), computes
the shortfall to the next `:00`, and bin-packs from the pool by length.

**The pool must exist before launch, and it is easy to under-build.** Back-timing draws on it
roughly 24 times a day, so a thin pool becomes audible repetition within the first week — faster
than any other content shortage in the system. Minimum before going live:

| Length band | Pieces |
|---|---|
| 15–30 s | 12 (short trails, station-voice tags) |
| 30–90 s | 15 (generic trails, in-world weather, archive quotes) |
| 90 s–4 min | 10 (short features, letters, evergreen vignettes) |

Idents and sonic logos are **not** counted here — they are `imaging` (§9) and the mixer places them
from the hour clock. `make pool-check` counts only what back-timing can draw on.

Roughly 37 pieces, all rendered once, all reusable forever. `make pool-check` reports coverage per
band and is part of the launch checklist.

> **"Pool" means two different things in this document, and conflating them has already produced one
> wrong check.** Use the full name in code, in tasks and in prose:
>
> | Name | What | Size | Counted by | Built in |
> |---|---|---|---|---|
> | **the back-timing pool** (`pool_items`) | short filler that absorbs the seconds between a programme ending and the next `:00` | 37 pieces in three length bands | `make pool-check` | §35 step 13c |
> | **the archive pool** (`archive_items`) | whole retired and pre-built programmes that fill the overnight | 135 h floor, 165 h target, **no ceiling** | hours, in the digest and the rundown | §35 step 16 |
>
> They share no table, no floor, no check and no build step. `make pool-check` is green long before
> a single archive hour exists and says nothing whatever about the archive.

### Duration estimation

Six things depend on predicting speech length from text before anything is rendered: script
invariants 1 and 5 (§11), back-timing, the unit tests and benchmark measure 5 (§29), and the
planner's derate (§36). It gets one implementation, in `production/duration.py`, and one rule.

```
est_sec(turn) = words / wpm(cast_id, register_kind) * 60
              + pause_before_ms/1000
              + overlap_prev_ms/1000          # negative
              + nonverbal_allowance            # laugh 0.9s, breath 0.4s, sigh 0.7s
              + trail_off_allowance            # 0.5s
```

- **WPM is per presenter per register kind**, stored on `cast_profiles`; guest and vox voices use
  the role default (§3). Seed at **150** for
  `conversational` and **165** for `scripted`; a fast presenter and a slow one differ by more than
  10%, which is seconds per segment and compounds across an hour.
- **Recalibrated nightly** from the previous night's actual rendered turn durations: exponential
  moving average, α=0.2, so it converges in a week and does not chase one odd show.
- **Never estimate from characters.** Words, because the model writes words and the engine speaks
  them.

Estimation error is a `metrics` row (`duration_error_pct`) and appears in the digest. Persistent
one-sided error means the WPM seed is wrong for that presenter, not that the estimator is broken.

### Daylight saving

Europe/Warsaw gives one 23-hour day and one 25-hour day a year, and both touch this design.

**The decision: everything is stored and scheduled in UTC; only in-world phrase rendering uses local
time.** Consequences, accepted deliberately:

- **Spring forward** costs an hour of render window. The planner reads the actual window length
  from the calendar, so it simply schedules less that night and says so in the rundown.
- **Autumn back** duplicates 02:00–03:00. Two junctions would otherwise claim the same local hour;
  because pins are UTC instants there are simply 25 pinned junctions that day, and the second
  02:00 is generated as its own junction with its own content.
- The batch start is a UTC instant chosen to fall at 20:00 local in winter; in summer it starts an
  hour "earlier" by local clock. Nothing cares.

Both transition days carry a note in the digest. This is a decision, not an edge case to discover.

### Time rendering

```python
clock.now()                      # in-world now = real now + 600 years, same month/day/weekday
clock.phrase(target, air_time)   # → "in about three hours" | "yesterday evening" | "next month"
```

- **The model never sees a raw date and never does date arithmetic.** It sees rendered phrases.
- **Phrases are computed against air time, not generation time.** A junction written at 21:00 for
  09:00 tomorrow renders "in three hours" relative to 09:00. Context assembly takes `air_time`,
  never `now`.
- **Granularity is capped by lead time.** A format declares `max_lead`; beyond it, phrases coarsen.

The in-world calendar maps 1:1 onto the real one, +600 years — but **the weekday is inherited from
the real date and is never computed from the in-world date.**

600 Gregorian years is 219,145 days, which is 3 mod 7. Real Wednesday 29 July 2026 becomes Saturday
29 July 2626 if you let a date library compute it. Only offsets that are multiples of 400 years
preserve the weekday, and 600 is not one.

```python
def in_world(d: date) -> InWorldDate:
    # year shifts, weekday does NOT
    return InWorldDate(year=d.year + 600, month=d.month, day=d.day,
                       weekday=d.strftime("%A"))     # from the REAL date
```

This is a `clock.py` unit test, not a comment: assert that the in-world weekday for a known real
date equals the real weekday. Seasons and month names come along for free; only the weekday needs
the rule.

---

## 14. The nightly batch

```
20:00  PRE-FLIGHT    volume mounted (HARD ABORT if not) · ≥15GB free · Postgres
                     reachable AND on the external volume · models present ·
                     transmitter reachable. Any failure aborts the whole batch
                     and emails. Fail loudly NOW, not at 02:00
20:05  WORLD         nightly tick: threads advance, beats scheduled, 60 items,
                     horizon refilled — PLUS all of tomorrow's micro-ticks
                     pre-simulated in one pass
20:35  JUNCTIONS     ~24 hourly junctions for D+1, in air order. Cheap, and they
                     define the skeleton of the day
21:30  SHOWS         floating shows for D+2, in air order, each seeing the
                     previous one's coverage
23:45  RUNDOWN       write tomorrow's rundown (§14a) — the writing phase is done,
                     nothing has been rendered yet. This is the intervention point
00:00  UNLOAD        writer evicted; assert free memory before proceeding
00:05  RENDER        TTS drains the queue: junctions first, then shows, batched
                     by voice
06:30  ASSEMBLE      mix with imaging, loudness-normalise, C2PA, cue sheets
06:40  PUSH          rsync to transmitter; publish snapshots
06:45  BACKUP        pg_dump, encrypt, ship offsite (§28); prune audio if <30GB free
06:50  VERIFY        assert the 07:00 junction exists and plays
                     ⚠ this is the tightest deadline in the system: the 07:00
                     junction is rendered by 06:30 and airs 30 minutes later.
                     Record the margin as a metric (`junction_margin_min`) and
                     alert in the digest if it drops below 15 minutes
06:55  REPORT        digest email; idle until 20:00
```

### The three freshness tiers

The bottleneck is TTS: at RTF 0.7 one minute of speech takes ~90 seconds to render, and a 385-minute
window yields **~216 minutes of new speech per day** after the 0.8 derate. A weekday wants ~526
(`PROGRAMMING.md` §9). Freshness tiers are how the gap closes — three lifecycles, not one.

| Tier | Made | Airs | Retires | Daily cost |
|---|---|---|---|---|
| **F** | every night, for its air date | once | at air | full |
| **W** | once a week, on its `production_day` | as declared in `repeat_slots` | when next week's edition lands | ⅐ |
| **A** | in bulk, far ahead | many times over months | on plays, age, or staleness | ~0 |

#### F — fresh
Bulletins, the flagship magazines, the chart, anything carrying today's news. Generated for D+1
(junctions) or D+2 (floating), per §14's N+1 rule. No lifecycle: made, aired, done.

#### W — weekly, with repeats
A strand produces one edition a week and airs it as many times as its `repeat_slots` declare —
typically two to six (`PROGRAMMING.md` §8). **No pool and no retirement logic** — next week's
edition replaces this week's automatically, because the strand is weekly.

**Airings are free; only production costs render time.** An edition aired six times costs exactly
what an edition aired twice costs, so repeat count is an editorial dial with no capacity
consequence, and the only thing it spends is audible repetition (`DECISIONS.md` D-002). The daily
cost in the table above is therefore one seventh of production regardless of how often it airs.

The one rule that matters is **spread the production nights.** Every W programme declares a
`production_day`; `grid-sync` rejects a week where any night carries more than two, because eight
strands all regenerating on Sunday blows that night's budget while the rest of the week idles.

A **repeat costs nothing**: the scheduler points at the existing audio, prepends a short "first
broadcast on…" line rendered as a junction-class item, and **writes no coverage rows** — the station
said it once, not twice. Repeats are normal radio practice and must be announced.

#### A — archive, a rotating pool

Same shape as music rotation, and it needs real lifecycle mechanics.

```
generated ──▶ in_rotation ──▶ retired
                  │  ▲
                  └──┘  14-day separation between plays
```

```sql
archive_items(segment_id, first_aired, last_aired, plays,
              depends_on_threads int[], depends_on_figures int[],
              status)          -- in_rotation | stale | retired
```

| Rule | Value | Why |
|---|---|---|
| Separation | 14 days between plays | Below this, recurrence is audible. **Never shortened** (D-021) |
| Retire on plays | 12 | ≈6 months of life at 26 plays/year |
| Retire on age | 18 months | Register and world drift |
| Pool floor | **135 hours** | 9.5 h/day × 14-day separation |
| Pool target | **165 hours** | Headroom so top-up is never urgent |
| Pool ceiling | **none** | The target is a floor with a name, not a cap (D-021) |

**Where 9.5 comes from.** The grid airs 7.9 archive hours on a weekday and 13.1–13.5 at the weekend,
where lightness is bought with archive rather than with silence — 9.5 h/day averaged across the week
(`PROGRAMMING.md` §9). The floor is simply consumption × the separation window: anything less and an
item returns inside a fortnight.

**Replenishment arithmetic.** An item retires at 12 plays, which at one play per 14 days is about
five and a half months, so a 165-hour pool turns over roughly 2.2× a year: ~360 new archive hours
annually. At the pool's blended density — roughly 50% speech, because three of the four Night Watch
hours are music-led — that is **~30 minutes a day of steady-state generation, about 14% of the
budget at the 0.7× tier.** Affordable, but not free, and it is why archive top-up sits last on the
priority ladder.

**That 30 minutes assumes every archive hour is purpose-built, and it will not be.** Retired
floating shows and 28-minute news programmes enter the pool for free after 30 days (§28) — the
same mechanism PRODUCT's M4 describes as the overnight filling with the station's own past. At the
~300 tier the day produces roughly 300 broadcast minutes of programme material against an archive
appetite of ~60, so even a modest time-neutral fraction covers the hour, and purpose-built top-up
becomes headroom rather than a requirement.

**But only the time-neutral fraction survives**, and at the lower tiers most fresh output is
news-shaped — bulletins, reports, `The Six`, `Ledger` — which the staleness rule below pulls
quickly. **So the offset is real, unquantified, and not safe to assume before launch.** Size the
tier against the full ~30 (§36), let the digest's archive line report what actually arrives for
free, and revisit once three months of real retirement data exist. This is a measurement waiting to
happen, not an open decision (§38).

**The upfront cost is the longest pole in §35, and it is accepted.** 135 hours at ~50% speech
density is **~4,000 speech-minutes** — about 19 nights of pure archive render at the 0.7× tier, and
realistically a couple of months alongside everything else (§35 step 16). It is not 2,250; that
figure assumed a 90-hour pool that the grid never supported. With no launch date the render time is
free (`DECISIONS.md` D-006); what is not free is building the pool before the voice is settled.

**The archive is elastic and the launch date is what gives (D-021).** 165 hours is a target, not a
budget: if the separation simulation says the pool needs 300 or 400 hours to keep a fortnight clean
at the tier the station actually ships at, the answer is more nights of render, never a shorter
separation window. Render time before launch costs nothing but calendar, and the two levers D-003
declined — a 10-day window, a shorter Night Watch — stay declined. **Phase H finishes when the
simulation is clean, and everything downstream waits for it.**

**The cost dial is the overnight music-led share.** A talk archive hour costs ~42 speech-minutes to
build; a `music_show` or `music_sequence` hour costs ~6. Moving one more Night Watch hour to
music-led takes ~350 speech-minutes off the build. Two further levers exist and are deliberately
**not** taken: a shorter separation window at launch (10 days → ~96 h floor) and a shorter Night
Watch, both of which buy build time with audible recurrence (`DECISIONS.md` D-003).

**Staleness — the rule specific to this station.** Generic radio archive is timeless; yours is not,
because the world moves. A documentary on the migration is safe forever. A profile of a musician is
**not** safe if she dies in a beat three months later — airing it as though she is alive is a
continuity break, and the listeners who notice are exactly the ones who care most.

So every `A` item records `depends_on_threads` and `depends_on_figures` at generation. The nightly
tick checks the pool: when a referenced figure dies, or a referenced thread resolves in a way that
contradicts the item, it is marked `stale`, pulled from rotation, and the pool tops up to
compensate. Staleness is reported in the rundown.

### The priority ladder

The batch generates in strict order, and **archive is deliberately last so it can absorb shocks**:

1. **F** — bulletins, then daily programmes, in air order. Non-negotiable.
2. **W** — editions whose `production_day` is tonight. One or two.
3. **A** — top-up, **only if** the pool is below target *and* budget remains. One item, then stop.

A night that runs long drops archive top-up and nothing else suffers. You can drop it for three
weeks and no listener can tell, because the pool is 165 hours deep. That is what makes the schedule
resilient rather than brittle — and it is the reason the ladder is in this order rather than any
other.

### Generate N+1, not N

If the batch fails at 02:00 you are asleep, and at 07:00 you have nothing. So the two content
classes run on **different lead times**: floating shows for **D+2**, junctions for **D+1**.

Because floating content is time-neutral by construction, a two-day-old show is not stale. A failed
night therefore costs you only the junctions — 24 short pieces, regenerable in an hour over coffee
— while the shows for that day are already banked. **This turns a catastrophic failure into an
annoyance, and it is the highest-value rule in this document.**

### The rundown is written before rendering

Scripts exist by 23:45; audio does not exist until 00:05. That gap is deliberate — it is the only
point where changing your mind is cheap. See §14a.

### Priority order

Junctions before shows, everything in air order. If the window runs out at 05:00, the morning is
complete and the afternoon falls to archive. Never generate out of order to "balance" the day.

### Pre-simulating the day

The nightly tick fires **all** of tomorrow's micro-ticks in one pass: beats firing at 14:20,
slipping at 15:40, resolving at 18:00. Nothing in this world happens that you did not invent, so a
day scripted in advance is indistinguishable from a day reacting live — and it is what lets a 09:00
junction legitimately trail an event that "happens" at 14:20.

Each junction's context includes yesterday's coverage log, the beats that have fired **as of its
own air time**, and the beats still ahead of it. That is what produces "the convoy we told you
about this morning has docked" and "the council sits at six" from a batch written the night before.

The tick's two jobs stay distinct even when run together: **imagining** (new threads, new beats,
items) and **advancing the clock** (firing, slipping, cancelling). Keep them as separate functions
with separate prompts — imagination is expensive and gated, the clock is nearly free and mostly SQL.

---

## 14a. The rundown — knowing what the day will be

A radio station runs on a rundown: one document per day saying what is planned, in order, with what
each item covers. Without it you are listening to your own station to find out what it decided,
which is the wrong way round.

`batch.py` writes one at 23:45, after the writing phase and **before any audio is rendered**. It
lands at `/Volumes/station/rundown/2026-07-30.md`, is linked from the morning digest, and is the
one artifact you read with coffee.

**Which day it covers.** The rundown always describes **the next day that will air** — the one
starting in seven hours, not the one being written for. Because of the N+1 split (§14) its contents
come from two different nights, and it says so per item:

```
06:04  First Shift 1  [banked 2026-07-28]   ← floating, written the night before last
07:00  junction       [written tonight]     ← D+1
```

Dates inside the rundown body are **real UTC**, per §31 — only the header carries the in-world date.

That distinction matters operationally: `make regen` on a banked show is cheap because there is
still a night of render window ahead of it, while regenerating tonight's junction competes with
tonight's render queue.

**Planned coverage is not aired coverage.** `coverage` rows are written only when a segment airs
(§6), but the rundown must describe what scripts *intend* to cover, and some of them will be
quarantined or dropped. So scripts write `planned_coverage` at generation; the playout confirmation
promotes matching rows into `coverage` after air. The rundown reads `planned_coverage` and labels
it as such. Nothing ever claims the station said something it did not say.

### What it contains

```markdown
# Rundown — Thursday 30 July 2626  (real: 2026-07-30)
Batch run 4f2a · writing 20:05–23:45, used 3h33m of 3h40m · 24 junctions, 9 shows

## The day's timeline
06:20  expected   Relay maintenance window opens         [thread 41, rumoured→building]
09:00  scheduled  Grain tender closes                    [thread 38]
14:20  scheduled  Convoy ES-447 docks                    [thread 44]  ← lead
15:40  SLIPS      Convoy delayed ~40m (generated slip)
18:00  scheduled  Council votes on the tariff            [thread 38]  ← lead
21:30  rumoured   Halcyon Sound announcement             [thread 47, music]

## Thread movements
41  Relay dispute        rumoured → building    beat added
38  Tariff               active     (unchanged)  2 beats, resolves 18:00
44  Convoy               active     resolves today — closes after 15:40
47  Halcyon Sound        NEW        opened this tick (music)
52  Cold Harbor water    active     ⚠ STALLED 6 days — no beat, no stage change

## Programmes
06:04  First Shift 1     Wren + Kel   42m  covers 44, 38 · angle: what the delay costs
09:04  The Long Question Adu solo     21m  covers 38 · angle: tender as politics
11:04  Ledger            Wren + Kel   21m  covers 38 · angle: who pays the tariff
13:04  [REPEAT] The Bench                          (W, first broadcast 2026-07-28)
14:04  The Count         chart voice  15m  20 positions · 3 new entries, #1 unchanged 4w
16:04  [ARCHIVE] Halcyon Sound: the first ten years   (music_show, made 2026-06-02)
17:04  The Evening Report Wren + Kel  42m  covers 44 resolved, 47 · angle: the label story

## Junction leads
07:00 convoy due early afternoon · 09:00 tender closes · 11:00 —
13:00 convoy inbound · 15:00 convoy late, 40m · 17:00 convoy docked, cause
19:00 council result · 21:00 Halcyon rumour · 23:00 recap · 01:00–04:00 summaries

## Flags
⚠ Thread 52 stalled 6 days — needs a beat or a stage change
ℹ Archive pool 152 h / 165 target · 1 item retired (12 plays) · 1 stale (figure died, thread 47)
⚠ Rotation relaxed 3× (album ≥90m dropped) — catalogue thin for the 11:00 daypart
⚠ 1 script quarantined: Ledger draft 1, org/person name "Marren Institute" (the screen covers organisations as well as persons)
ℹ Horizon: 7 beats <24h, 11 <week, 4 <season (season floor is 5 — refill tomorrow)
ℹ Register  Wren  hedges 24/1000 (profile 22, +9%) · interrupts 1 in 7 · trail-offs 1 in 22
            Adu   hedges 44/1000 (profile 48, −8%) · interrupts 1 in 15 · trail-offs 1 in 10
            separation 20pp (floor 15pp) OK · aphorisms 0
            Sella (scripted) hedges 0 · trail-offs 0 · long sentences 4% · OK
```

### Why this shape

- **The timeline is the world's plan**, including the slips and cancellations the tick has already
  decided. You can see the day's story before it airs.
- **Thread movements** answer "is anything stuck" at a glance — the stalled-thread rule (§6) has
  somewhere to report.
- **Programme lines** show which beats each show will actually talk about, which is how you catch
  three programmes all leading on the convoy.
- **Junction leads** are the hour-by-hour spine, and reading them in sequence is how you notice the
  day has no narrative shape.
- **Flags** surface exactly the WARNINGs that would otherwise sit unread in a log file.
- **Register metrics** (§11a) go here so the trend is visible daily rather than discovered monthly.

### The D+2 section — where intervention is actually cheap

The intervention window between 23:45 and 00:05 is twenty minutes in the middle of the night, so in
practice the rundown is read as a **morning observation** document. That is fine, because the N+1
split already provides a real lever: the shows written *tonight* air the day after tomorrow, and can
be changed cheaply any time before tonight's next batch.

So the rundown has two halves: **tomorrow** (what will air in seven hours — observation) and **D+2**
(what was written tonight — still fully editable). Read the first with coffee; act on the second.

### Intervening

Because audio does not exist yet, three cheap actions are available before 00:05:

```
make hold PROGRAMME=ledger AIR=2026-07-30T11:04       # real UTC date, not in-world (§31)
make regen PROGRAMME=ledger AIR=...                   # rewrite before rendering
make beat-cancel ID=...                                # kill a beat; dependent scripts regenerate
```

After 00:05 the same actions cost a re-render, which is why the gap exists.

**The default is always "ship what was written".** The rundown is an opportunity, never a
checkpoint: nothing waits for approval, no phase blocks on a human, and an operator who is asleep,
travelling, or simply uninterested changes nothing about whether the station broadcasts tomorrow.
A 24/7 station with a manual approval step in the critical path is a station that goes quiet the
first weekend you go away.

**The rundown is generated, never hand-written, and is gitignored** — it is derived state, like
rendered audio. `make rundown DATE=...` regenerates it from the database at any time, including for
past days, which makes it the natural place to look when something aired oddly.

Later, the panel's world screen (§17) is a view over exactly this data. The markdown file comes
first because it costs an afternoon and works from day one.

---

## 15. The broadcast day

Fresh hours are limited by render capacity, not by anything else. Since everything is pre-rendered,
**where you place them is free** — and a contiguous morning block is probably not optimal.

**`PROGRAMMING.md` §8 is the schedule; this section is only the principle behind it** (§32). Fresh
generation goes where listeners are — the morning and evening blocks — and the slow-domain
overnight is where reused material belongs. The same holds across the week: **one clock, seven
days, with the weekend made lighter by freshness rather than by a different shape** (D-001). This
section deliberately restates no hours; where the two disagree, `PROGRAMMING.md` wins (§32).

**Hourly pinned junctions run across all 24 hours**, including the archive block. A current
bulletin, the correct time and the disclosure every hour is most of what makes an archive block
feel like a station rather than a playlist — and a junction is the cheapest thing on the station.

The overnight block is not a compromise. Content about the past, culture and reflection *is* the
floating class — cheapest to make, safest to reuse, and it gives the station an identity at 03:00.
Pre-build a starting archive (lead with specialist music shows), then let retired daytime material
replace it over the first months.

### Playout and the failure chain

Liquidsoap on the Transmitter, pure config, no Python, no network:

```
0. PINNED junction     wall-clock predicate at :00 — always wins
1. hour playlist       the built hour, if present and every file exists
2. today's buffer      any unaired show from today
3. archive pool        30+ days of retired shows, shuffled
4. music               rotation from the catalogue
5. bed + ident loop    never silent
```

**The YouTube relay has a gotcha worth designing for.** YouTube Live will not accept an audio-only
RTMP stream — it requires a video track. ffmpeg loops a static 1280×720 card (station logo, current
programme, and the AI-disclosure line rendered into the image) against the Icecast audio, with a
2-second keyframe interval and a low video bitrate since the frame rarely changes. The card is
regenerated on programme change from the same `now.json` the site uses. Three consequences: the
disclosure is *visible* as well as spoken on this path, which helps at first exposure (§18); the
video encode costs almost nothing because the image is static; and if the card generator fails,
fall back to a fixed image rather than dropping the stream.

**Listener ceiling, because it is the first thing that breaks if this gets attention.** At 128 kbps
a CX32's 20 TB/month allowance is roughly 480 continuous listeners; practical concurrency on 2 vCPU
is lower, around 250–300 before Icecast becomes the bottleneck. Set `<clients>` to 300 explicitly
rather than discovering the limit. Beyond that the answer is a CDN in front of the HLS output, not a
bigger box — and the YouTube relay already absorbs unbounded audience for free, which is a good
reason to point people there rather than at the raw stream.

**Disclosure must survive every level.** Levels 3–5 are exactly the states you are least likely to
be watching. Every source sets `StreamTitle` with the AI marker, and the `disclosure_sting` is
hard-scheduled hourly independently of content. The playout conformance check forces each level in
turn and asserts the metadata is present at every one.

---

## 16. Public web

Next.js App Router on Vercel, `settlementradio.com`. Read-only, no auth, no writes.

```
/                     Player. Live audio, now-playing, current programme, hosts
                      on air, AI-disclosure line + EU icon above the fold.
/schedule             The week's grid, today highlighted, "on now" marker.
/programmes           All programmes: brief, hosts, when they air.
/programmes/[slug]    Programme page + recent episodes.
/voices               The cast. Sigil, persona, which shows.
/world                Public world digest: active threads, recent beats, in-world
                      prose. The story surface — this is what brings people back.
/chart                This week's chart, with movement. (After week 3.)
/music                Artists, albums, tracks — the discography as a browsable
                      encyclopedia. Cheap off §8, disproportionate payoff.
/about                What this is, how it is made, the tribute framing.
/ai-transparency      Article 50 disclosure page (§18). Linked from every footer.
/archive              Past episodes by date and programme.
```

**Data flow:** the Studio publishes static JSON snapshots (`now.json`, `schedule.json`,
`world.json`, `chart.json`) to the Transmitter on every playlist build. Vercel fetches with
`revalidate: 30`. The public site never touches Postgres and cannot take the station down.

**`now.json` is published on every element change, not on every playlist build.** Liquidsoap writes
it from the `on_metadata` handler, so it reflects what is actually playing rather than what was
planned — which is what makes the §6 poller truthful at fallback levels 2–5. It carries
`off_plan: true` whenever the playing element did not come from the built hour. Clients interpolate
position within a programme from the cue sheet, and must not do so when `off_plan` is set.

**Staleness must be visible.** If the Studio dies the stream keeps playing but snapshots freeze,
and without a marker the site confidently shows yesterday's schedule. Every snapshot carries
`generated_at` and `max_age_s`; the player shows a quiet "schedule may be out of date" line once
exceeded. The audio is fine — it is the metadata that has gone stale, and saying so costs nothing.

`/world` is a scrape target by design, so cache it at the edge for 5 minutes and rate-limit it. It
exposes rendered prose, never raw table shape.

---

## 17. Administration

**For the first 30 days on air, `make` targets are the admin interface.** One exception worth
building on day one: `make sample` plays three recent segments unlabelled and records a thumb.
Quality judgement is the only signal that matters (§29) and it should not wait for a panel.

Building a panel before you know what you will actually
reach for is speculation, and what you reach for in the first month *is* the backlog for the panel.

```
make setup             install deps, hooks, check system tools
make check             ruff + mypy + unit tests  (fast, model-free; the pre-push gate)
make migrate           alembic upgrade head
make canon-check       validation report, no writes
make canon-sync        idempotent canon → DB
make music-sync        idempotent music → DB
make music-analyse     ramp/outro/bpm/energy pass
make grid-sync         idempotent grid → DB
make batch             run the full nightly batch now
make tick              world tick only
make sample            play 3 recent segments blind, unlabelled, record thumbs
make pool-check        pool coverage per length band
make verify-marking    assert C2PA + watermark survived the push
make rundown DATE=     regenerate the day's rundown from the database
make hold PROGRAMME=   skip a planned programme; archive fills the slot
make regen PROGRAMME=  rewrite a script before rendering
make show ID=...       generate one show end to end
make render            drain the render queue
make hour              build the next hour's playlist
make push              rsync to the transmitter
make conformance       every provider implementation against the same suite
make benchmark MODEL=  model candidate gate (§29)
make golden            regenerate golden outputs for human diff
make smoke             end-to-end run into a temp dir (Kokoro, fast)
make smoke-full        one full segment through the real cast engine
make beat-cancel ID=   cancel a beat; dependent scripts regenerate
make measure           run the §36 RTF protocol; writes config/measured.yaml
make deploy            push config + liquidsoap to the transmitter (manual, §30)
make backup            pg_dump, encrypt, ship offsite
make backup-media      weekly sync of music/imaging/pool/voices offsite
make restore-test      restore latest backup into a scratch DB and assert
make banned-add TERM=  add to the IP screen list
make reset-world       DESTRUCTIVE — generated world only, typed confirmation
```

Agents and operator both use `make`. **Never document or run a raw command that has no target.**

**After 30 days**, build a small Next.js panel, Tailscale-only, with the six screens experience has
by then justified. The expected set: on-air status, render queue, world digest with beat *review* (never approval — nothing blocks, §14a),
a **blind listening sample** (three recent segments, unlabelled, thumbs up/down — the only quality
signal that means anything), the canon-check report with keep/supersede/edit buttons, and health.

Auth is Tailscale identity. No public exposure, ever.

---

## 17a. Configuration file schemas

Config tasks are made of these files, and the validations described elsewhere are called
"`grid-sync` errors" without the file's shape ever being given. All live in `config/`, all are
committed, none contain secrets.

### `grid.yaml` — the largest one

```yaml
version: 1

dayparts:                       # the seven of PROGRAMMING.md §4, which owns the boundaries.
                                # Drives rotation energy/tempo and modifier selection (§11a)
  - { id: early,     from: "05:00", to: "07:00", energy: [0.1, 0.4], bpm: [50,  90] }
  - { id: morning,   from: "07:00", to: "11:00", energy: [0.5, 0.8], bpm: [90, 130] }
  - { id: midday,    from: "11:00", to: "14:00", energy: [0.3, 0.6], bpm: [70, 110] }
  - { id: afternoon, from: "14:00", to: "17:00", energy: [0.4, 0.7], bpm: [80, 120] }
  - { id: evening,   from: "17:00", to: "21:00", energy: [0.5, 0.9], bpm: [90, 140] }
  - { id: night,     from: "21:00", to: "01:00", energy: [0.2, 0.5], bpm: [60, 100] }
  - { id: overnight, from: "01:00", to: "05:00", energy: [0.1, 0.4], bpm: [50,  95] }
  # overnight starts at 01:00, not 00:00: it is defined by the block whose junctions
  # are 2-minute summaries and whose programmes are archive (PROGRAMMING.md §8). The
  # 00:00 hour carries The Midnight Report, which is fresh news and belongs to night

imaging:                        # station-wide defaults; programmes may override
  sonic_logo: station_logo_3s
  disclosure_sting: ai_ident

programmes:
  - slug: evening_report
    name: "The Evening Report"
    programme_type: magazine        # container shape — determines the item mix (§11)
    format_class: floating          # junction | floating | pool
    register_kind: conversational   # the default a `host` slot inherits (§11a)
    slot_minutes: 56                # 4 | 28 | 56 only — 56 is written as 2 acts (§11)
    pace: fast                      # sets link length, item count, emotion band
    jingle_set: evening_report      # open/close/bed ids from `imaging`
    freshness: F                    # F nightly | W weekly+repeats | A archive
    # W programmes additionally declare:
    # production_day: tue                            # max 2 per night across the grid
    # repeat_slots: [{ days: [sat,sun], at: "07:04" }]
    item_mix:                       # the running order the showrunner must fill.
                                    # Midpoints sum to ~40 min against a 42-min speech
                                    # budget (56 × 0.75) — validation 7
      - { kind: link,      count: 12,  sec: [25, 50] }
      - { kind: two_way,   count: 4,   sec: [140, 240] }
      - { kind: package,   count: 2,   sec: [180, 300] }
      - { kind: interview, count: 1,   sec: [300, 480] }
      - { kind: vox,       count: 2,   sec: [60, 90] }
      - { kind: letter,    count: 1,   sec: [60, 90] }
    max_lead_hours: 30              # granularity ladder cap (§13)
    brief: "Treats the day's politics as consequence. Opens on who it lands on."
    domain_floor: [politics, conflict]    # seats the domain floor in retrieval (§5)
    context_mix: { canon: 0.3, world: 0.7 }   # fast domain — mostly living world.
                                              # Slow domains invert this (PROGRAMMING.md §1)
    hosts:
      - { cast: wren, role: host }          # ONE host links the programme
      - { cast: kel,  role: correspondent } # inside two-ways and packages only; needs a
                                            # `scripted` profile, not this one (validation 1)
    hour_clock:
      open: evening_open
      bed_under_links: report_bed
      sweeper_every_n_items: 2
      close: evening_close
    schedule: [{ days: [all], at: "17:04" }]  # one clock, seven days (D-001). Programmes
                                              # start at :04 or :32 — :00 is the junction

  - slug: the_count
    name: "The Count"
    programme_type: chart
    format_class: floating
    register_kind: conversational
    slot_minutes: 28
    jingle_set: the_count
    freshness: W                    # produced once a week and repeated — that is W, not F,
    production_day: wed             # even though it carries this week's news (§14)
    requires_airplay_days: 21       # grid-sync refuses to schedule until satisfied (§8)
    chart_id: main
    hosts: [{ cast: adu, role: chart_voice }]
    schedule: [{ days: [fri], at: "14:04" }]
    repeat_slots: [{ days: [sat], at: "14:04" }]   # Saturday reruns Friday's audio, billed as a
                                    # repeat. NOT a second, longer edition — 40 positions will not
                                    # fit 28 minutes (PROGRAMMING.md §8)

  - slug: news
    name: "Settlement Radio News"
    programme_type: bulletin
    format_class: junction
    register_kind: scripted
    slot_minutes: 4
    jingle_set: news
    item_mix:
      - { kind: bulletin_story, count: 5, sec: [20, 40] }
    max_lead_hours: 1.5
    hosts: [{ cast: sella, role: newsreader }]
    hour_clock: { sting: news_urgent, bed: news_bed_loop, disclosure_sting: ai_ident }
    schedule: [{ days: [all], at: "hourly:00" }]     # pinned (§13)
```

**The nine validations `grid-sync` performs**, all of which are errors:

1. Every `hosts[].cast` has a `cast_profiles` row for the register kind **its role requires**, not
   the programme's: `host` inherits `programmes.register_kind`; `correspondent` and `newsreader`
   always need a `scripted` row, including inside a conversational magazine; `guest`, `vox` and
   `chart_voice` need `conversational` (§11 invariant 7). Checking the programme's kind alone lets a
   correspondent pass grid-sync and fail at generation.
2. Conversational co-hosts satisfy the separation rule — ≥15 hedges/1000 apart, no shared
   `hedge_form`, no shared `disagreement` mode (§11a).
3. A `requires_airplay_days` programme is not scheduled until `airplay` holds that history (§8).
4. **Total *fresh* speech minutes ≤ `measured.yaml: usable_speech_minutes`**, evaluated **per day of
   the week** and gated on the worst day. `F` programmes counted on the days they air, `W` counted
   as production on its `production_day` only, `A` and `R` counted zero. Raw grid minutes are not
   the number, and **the ×0.8 derate is not applied twice** — it is already inside
   `usable_speech_minutes` (§36).
5. `slot_minutes` is one of **4 · 28 · 56**, every hour is `4 + 56` or `4 + 28 + 28`, and every
   hour's slots sum to exactly 60. **The skeleton is day-invariant**: a slot has the same length on
   every day of the week, so this is checked once rather than seven times (`DECISIONS.md` D-001).
6. Every referenced `imaging` id, `jingle_set` and `chart_id` exists; every programme has a
   `jingle_set`.
7. `item_mix` durations, **summed at the midpoint of each band**, land within ±15% of the slot's
   **speech budget** — `slot_minutes × 0.75`, not `slot_minutes`, because the remaining quarter is
   imaging, beds and music (§10). A 28-minute magazine must therefore declare ~18–24 minutes of
   items, not 28. No single generation call exceeds ~25 minutes of speech (56-minute slots must
   declare 2 acts); every `kind` is legal for the declared `programme_type` (§11).
8. **Every day accounts for all 1,440 minutes exactly once.** Two failures, both ERRORs:
   - **An uncovered span** — not auto-filled. A speech station with holes in its grid has a
     scheduling bug, not a music policy. Checked for all seven days: a programme whose `schedule`
     covers only `mon–fri` leaves a weekend hole unless another claims it.
   - **A double-booked slot** — two programmes both claiming `sat 14:04`. Day patterns make this
     easy to do by accident and impossible to hear until the playlist builder picks one arbitrarily.
     Every `(day, start_time)` pair resolves to exactly one programme.
9. Every `W` programme has at least one `repeat_slot` and a `production_day`. A `W` programme
   without a repeat is an `F` programme wearing the wrong label, and grid-sync says so. **No night
   carries more than two W productions**; every `A` programme has neither. Repeat *count* is not
   validated — it is editorial (D-002).

### The smaller files

```yaml
# config/measured.yaml — written by `make measure`, read by the planner. Never hand-edited.
measured_at: 2026-08-03T11:40:00Z
tts_engine: chatterbox
sustained_rtf: 0.82             # third consecutive 60-min run (§36)
throttle_loss_pct: 18
peak_system_memory_gb: 12.4
render_window_minutes: 385      # 00:05 → 06:30
usable_speech_minutes: 253      # sustained_rtf × window × 0.8  (0.82 × 385 × 0.8)
```

```yaml
# config/banned-entities.yaml — the IP screen (§7 pass 5, §19). `make banned-add` appends.
franchises:  [{ term: "...", match: fuzzy, note: "trademark" }]
characters:  [{ term: "...", match: exact }]
authors:     [{ term: "...", match: exact, note: "living author" }]
organisations: [{ term: "...", match: fuzzy }]   # §19 checks orgs as well as persons
```

```yaml
# music/catalogue.yaml — read by `make music-sync`; audio lives on the external volume
labels:  [{ id: halcyon, name: "Halcyon Sound", settlement: cold_harbor,
            founded_year: 2597, house_style: "close-mic, unhurried" }]
artists: [{ id: marren, name: "Ilve Marren", kind: solo, figure: fig_marren,
            label: halcyon, scene: "relay folk", active_from: 2612 }]
albums:  [{ id: long_dark, artist: marren, label: halcyon, title: "The Long Dark",
            release_year: 2618, kind: album }]
tracks:  [{ id: t_0141, album: long_dark, title: "Ferry Song", track_no: 3,
            file: "music/halcyon/long_dark/03.mp3", category: A,
            mood: [wistful, slow], language: en, licence_note: "suno-pro-2026-03",
            intro_ramp_sec: 11.5, outro_type: fade }]
```

`models.yaml` is in §3. The imaging hour clock lives inside `grid.yaml` above rather than in a file
of its own — it is per programme, so it belongs with the programme.

**Rotation category weights** (§8), stated once so nobody invents them:

| Category | Weight | Meaning |
|---|---|---|
| A | 1.00 | heavy rotation |
| new | 0.85 | released in-world within 8 weeks |
| B | 0.60 | |
| gold | 0.45 | catalogue, ≥5 in-world years old |
| C | 0.30 | |
| specialist | 0.10 | only reachable when a programme requests it by name |

---

## 18. Compliance

> **Everything in this section is design intent, not legal advice.** It is written by a non-lawyer
> from public sources. The controls below are what a careful engineer would build; whether they
> *discharge* the obligations is a question only a qualified lawyer can answer, and §35 makes that
> review a hard gate before any public listener.

**EU AI Act Article 50 applies from 2 August 2026** — days away as this is written, not yet in
force. That is not pedantry: the doc below concludes the December transition does not help you, but
the placing-on-the-market date is still *ahead*. **Whether standing up the Transmitter before
2 August constitutes placing on the market is a lawyer question**, and it should be asked rather
than assumed away. Penalties reach €15M or 3% of worldwide
turnover. Poland is in scope.

**The guidance is final.** The Commission published the Code of Practice on Transparency of
AI-Generated Content on 10 June 2026 and adopted the Article 50 Guidelines on 20 July 2026. The
Guidelines are non-binding — only the CJEU can give an authoritative interpretation — but national
market surveillance authorities and the AI Office can be expected to follow them. **Whether the
Code has completed the Commission and AI Board adequacy assessment — the step that makes adherence
a formal route to demonstrating compliance — must be checked rather than assumed.** So the
instruction is **"review the
disclosure package against the published Guidelines and Code, and re-review when either is
updated"** — not "track the drafts".

**Two provisions matter disproportionately here:**

- **The Code has a regime for fiction.** Section 2 covers deployer obligations under Art. 50(4) and
  explicitly contemplates specific regimes for artistic, creative, satirical, fictional or
  analogous works, alongside guidance on the design, placement and presentation of labels. That is
  the news-shaped-fiction question, and it now has a documented answer to work from. **Read
  Section 2 before writing the disclosure copy.**
- **The Code has an official icon.** Annex I provides an optional EU icon in three variants. Use it
  on the player and the site rather than inventing a badge.

**Signing is an option.** The Code splits into provider and deployer sections, signable
independently; adherence is intended as a route to demonstrating compliance. The initial-signatory
window closed on 27 July 2026 but joining later remains possible. A question for the lawyer.

**The cut-off rule turns on publication, and it lands squarely on the pre-built archive (§35
step 16).** Content both *generated and published* before 2 August 2026 needs no retroactive
marking. Content generated before that date but **published on or after it is caught** — which is
exactly the archive's position: rendered in the weeks before launch, broadcast after it. **Mark
everything regardless** — it is safer and simpler — and record the rule in `DECISIONS.md`, because
it is exactly the distinction the lawyer will ask whether you understood. Verify the wording
against the adopted Guidelines rather than against this paragraph.

**Every date and instrument named in this section is unverified and must be checked against primary
sources before the lawyer is engaged** — not just the two originally flagged (the Digital Omnibus
dates and the three-variant EU icon). That includes the Article 50 application date, the Code of
Practice publication and adequacy-assessment status, the Guidelines adoption date, the
initial-signatory window, and the December 2026 transition. They were written down from public
reporting by a non-lawyer and several are load-bearing.

**This costs nothing to defer.** Step 15 is a hard gate with written sign-off before any public
listener, so the verification happens there, with a professional, against the Official Journal and
the Commission's own publications rather than against this paragraph. What this section is for is
making sure the right questions get asked — not for being right about the answers.

**The December 2026 transition probably does not help you.** Systems on the market before 2 August 2026 have
until 2 December 2026 to bring marking into compliance. A station launched after that date does not
qualify.

### The duties

- **Art. 50(2)** — synthetic audio and text must be **marked machine-readably and detectably**.
  Whether you count as provider, deployer or both is a legal characterisation, not an engineering
  one — assume the stricter reading and let the lawyer relax it. The Commission deliberately does
  not mandate one technical mechanism, so no implementation is sufficient on its own; the
  expectation is to review what is feasible, **document and justify the decision, and keep it under
  review**. Write that justification into `DECISIONS.md` — the record is part of the posture.
- **Art. 50(4)** — deployers publishing AI-generated text informing the public on matters of public
  interest must disclose. Your bulletins are fiction, which *may* place them outside this limb —
  but the fiction is **shaped like news**, and form matters. Disclose as though it applies.
- **Art. 50(5)** — disclosure must be clear, distinguishable, and at the latest at first exposure.
- **Deepfake rule** — never clone a real person's voice. Synthetic reference clips only, with
  provenance in `voices/PROVENANCE.md`.

### Implementation

| Surface | Mechanism |
|---|---|
| On air | Spoken disclosure inside every hourly junction, **plus** a `disclosure_sting` hard-scheduled hourly independently of content, so it fires when playout has fallen through to music at 04:00 |
| Stream metadata | `StreamTitle` and server name carry an AI marker on every track change, **at every fallback level** |
| Files | C2PA manifest on every rendered file; **plus a second, inaudible watermark layer** — the engine's own where it has one, otherwise a standalone watermarking pass applied after render. Complementary mechanisms supporting Art. 50(2) — not a certified answer. **The two layers are the commitment; the engine is not** (D-019): the cast engine is chosen on how it sounds, and if the winner does not watermark, supplying the second layer is Phase G work, not a reason to pick a different voice |
| Player | Persistent line above the fold, using the Annex I EU icon |
| Website | `/ai-transparency` linked from every footer: what generates what, which models, and that the world is fictional |
| YouTube (**the distribution-chain limb**) | The final Guidelines expect deployers in a production and distribution chain to take proportionate measures so the label reaches the audience at first exposure — via contractual terms and **interface settings**. Here that means: the channel-level synthetic-content setting, the per-broadcast altered-content flag, first line of the description. The spoken disclosure and hourly sting travel with the audio; **stream metadata does not survive RTMP**, which is why the spoken layer is the one that carries compliance on this path |
| Fiction | Every disclosure states the news is **invented**, not merely AI-written. That is the part a listener actually needs |

**Verification, not just emission.** Marking written and then lost in transit is worse than useless,
because you believe you are covered. Two checks:

- **Post-push:** `make verify-marking` pulls a sample of files back from the Transmitter after rsync
  and asserts the C2PA manifest and engine watermark survived. Runs at the end of every batch;
  failure is an ERROR in the digest. **The check runs on the Studio, never on the Transmitter** —
  adding verification logic to the transmitter would give it a brain, which is precisely what §4
  forbids. Pull the artefact to the machine that has judgement.
- **Playout conformance:** force each of the six playout levels (0–5) and assert `StreamTitle`
  carries the AI marker at every one (§15).

**Re-review triggers:** any update to the Article 50 Guidelines or the Code of Practice; **the
Digital Omnibus on AI**, adopted by the Council on 29 June 2026 and signed 8 July 2026, awaiting
publication in the Official Journal — it may move calendar items; and annually regardless.

**Scope note, in your favour to know:** the transparency obligations do not apply to purely
personal, non-professional use. With Ko-fi and grant applications attached, Settlement Radio is not
in that carve-out. Assume in scope, as this document does.

### Other legal surfaces

- **Music.** The library is Suno-generated. Confirm the plan's commercial-use grant covers
  streaming and keep the evidence. `tracks.licence_note` is required, not optional — the answer
  changes the moment one third-party track enters the catalogue.
- **Broadcasting licence.** Poland's KRRiT regime covers terrestrial, satellite and cable
  dissemination; internet-only streaming generally sits outside it. Confirm with a Polish media
  lawyer before launch — do not assume.
- **IP boundary.** This is a **tribute, not a derivative**. No real franchises, named characters,
  trademarks, or living authors' creations. `banned-entities.yaml` plus the `canon-check` screen is
  the enforcement mechanism, maintained via `make banned-add` so it does not rot.

---

## 19. Content safety gate

Runs on **script text, before TTS** — cheaper than re-rendering, and where the risk lives. Every
segment and every generated beat passes it.

**Deterministic checks** (no model):

- `banned-entities.yaml` — the IP boundary
- Real-person name detection: any name absent from `figures` that matches a known-persons list.
  **Order matters and it is fixed: the gate runs on the world tick's *proposed* figures, before they
  are committed.** Running it after would make it toothless — the tick writes invented names into
  `figures`, and anything in `figures` is exempt. A proposed name that passes is committed and
  permanently exempt thereafter.

  **What counts as a match, because the naive rule is unusable.** Nearly every plausible human name
  appears somewhere in a 1.5M-name list, so "matches the list → regenerate" would send the world
  tick into a loop rewriting perfectly good invented people. The rule is therefore:

  | Match | Action |
  |---|---|
  | **Full name, exact**, against an entity above the notability floor | **ERROR** — regenerate |
  | Full name, exact, below the floor | pass, and log INFO |
  | Surname only, or fuzzy on the full name | pass, and **flag in the rundown** for the operator |

  **The notability floor is ≥5 Wikidata sitelinks** — roughly "has a real article in several
  languages". Two people sharing a name is how names work; an invented council member sharing a
  full name with someone notable is the actual risk, and it is a much smaller set than 1.5M.

  **The list is a build task with a real download**: Wikidata's `humans` subset filtered to those
  with sitelinks (~1.5M names, CC0, refreshed quarterly), carrying the sitelink count so the floor
  is applied at query time rather than baked into the extract. **Two structures, because one will
  not do:** a bloom filter (~40MB on disk) answers the exact-match pass, and a separate
  trigram-indexed surname table answers the fuzzy pass — a bloom filter answers membership only and
  cannot support approximate matching. Organisations are checked against the same mechanism, and the
  same floor, using Wikidata's organisations subset
- Profanity threshold per station policy
- Structural: disclosure present in junction formats, no clock tokens in floating formats

**Model check**, one call:

- *(scripts only)* Does this read as a factual claim about the **real** world? **Beats use a
  different prompt** — every beat is by construction a factual claim about the *fictional* world, so
  the script prompt would reject the entire world tick. The beat prompt asks instead: does this
  assert anything about the real world, defame a real person, or breach the IP boundary?
- Does it defame or impersonate a real person?
- Does it read as derived from an identifiable existing work?
- Does it give medical, legal or financial advice a listener could act on?

**On failure:** quarantine to `segments/quarantine/`, log ERROR with the reason, regenerate once.
If the second attempt also fails, **drop the slot and let archive cover it** (§20) — the pool is
sized for back-timing residue and cannot fill a programme-length hole. Nothing unreviewed ever
airs.

Every gate decision is logged **including passes**, so you can audit what the station has said.

---

## 20. Failure behaviour

The degradation ladder, in order:

1. **Batch overruns** → what was generated airs; the rest falls to archive. Short day, not broken.
2. **TTS circuit breaker trips** → remaining jobs render in Kokoro rather than failing. The station
   stays on air but the voices are flat, so **the day is marked `degraded`** and that appears at the
   top of both the rundown and the digest. Silent quality loss is worse than an outage, because
   nothing tells you it happened.
3. **Batch fails entirely** → D+2 shows already exist; only junctions are missing. Regenerate them
   in the morning, or run the day on archive with junctions suppressed.
4. **Studio dies** → the Transmitter plays its buffer, then archive, then music, indefinitely.
   Inaudible to listeners for days.
5. **Transmitter dies** → the only true outage. Restore from a documented image.

**One alert, not a dashboard.** The batch writes a completion timestamp; if it is missing by 07:30,
email. Everything else is the daily digest (§24).

---

# Part II — Engineering standards

Everything above describes what the system *is*. Everything below describes how it gets built and
stays maintainable. These sections bind every task and every agent session.

---

## 21. Repository layout

```
settlement-radio/
├── pyproject.toml              # uv-managed; the single source of dependencies
├── uv.lock                     # committed
├── .python-version             # 3.12
├── Makefile                    # every operation has a target
├── .env.example                # committed, empty values, always current
├── .pre-commit-config.yaml
├── alembic.ini
├── CLAUDE.md                   # one page of non-negotiables (§32)
├── README.md                   # reproducible install from scratch (§32)
│
├── src/station/
│   ├── config.py               # pydantic-settings — THE only place env is read
│   ├── log.py                  # structlog setup, called once at process start
│   ├── clock.py                # in-world time + phrase renderer — the only "now"
│   ├── batch.py                # the nightly run: phases, ordering, pre-flight
│   ├── worker_tts.py           # render queue consumer (separate process)
│   ├── cli.py                  # typer; every make target calls into here
│   ├── providers/
│   │   ├── llm.py              # generate_structured, per-job routing
│   │   ├── embeddings.py
│   │   └── tts/
│   │       ├── base.py         # Protocol + Capabilities (§3)
│   │       ├── chatterbox.py
│   │       ├── qwen3.py
│   │       ├── kokoro.py
│   │       └── registry.py
│   ├── world/
│   │   ├── store.py            # ALL world SQL lives here
│   │   ├── tick.py             # imagine + advance, separate functions
│   │   └── ranker.py
│   ├── canon/
│   │   ├── parse.py  check.py  sync.py  summarize.py
│   ├── retrieval/
│   │   ├── hybrid.py  rerank.py  assemble.py
│   ├── production/
│   │   ├── showrunner.py  script.py  safety.py  render.py  mix.py
│   ├── music/
│   │   ├── store.py  rotation.py  chart.py  sync.py  analyse.py
│   ├── schedule/
│   │   ├── grid.py  playlist.py  backtime.py
│   └── publish/
│       ├── rsync.py  snapshots.py  credentials.py    # C2PA
│
├── prompts/                    # jinja templates, versioned
├── core/                       # Tier 0 — station identity + the clock concept (§5).
│                               # Loaded WHOLE and VERBATIM into the cached prefix.
│                               # Never parsed, never embedded, never retrieved
├── canon/                      # the bible — markdown, hand-authored, frontmatter = world content
├── cast/                       # DJ cards + speech profiles (§11a, C2) — Tier 0, not canon
├── music/                      # yaml manifests (audio files on the external volume)
├── voices/                     # reference clips — COMMITTED, irreplaceable
├── config/                     # liquidsoap, icecast, grid.yaml (dayparts live in it),
│                               # models.yaml, measured.yaml
├── migrations/
├── tests/
│   ├── unit/  conformance/  golden/  smoke/  eval/
├── web/                        # Next.js public site → Vercel
├── panel/                      # Next.js ops panel → Tailscale (after 30 days)
└── docs/
    ├── ARCHITECTURE.md  ADMIN.md  DECISIONS.md  TASKS.md
    └── PRODUCT.md  PROGRAMMING.md  PHASES.md   # operator-owned, outside the §32 cap
```

**Layer rules:**

| Rule | Why |
|---|---|
| All SQL lives in a `store.py` | One place to reason about queries, indexes, transactions |
| Vendor SDKs only inside `providers/` | The seam is meaningless if an SDK is imported in `showrunner.py` |
| `os.getenv` only in `config.py` | Otherwise config drifts everywhere and nothing is testable |
| `datetime.now()` only in `clock.py` | Time must be injectable or scheduling is untestable |
| No module imports a sibling's internals | `production` calls `world.store`, never `world.tick` |

### Process model

`batch.py` runs the nightly phases. **TTS runs in its own process** (`worker_tts.py`) consuming the
render queue. Two reasons: a stuck or crashed render must not take the batch runner with it, and
memory is easier to reason about when the writer and the TTS engine live in separate address
spaces — which matters a great deal at 16GB.

- **Supervision:** `batch.py` runs under launchd with `RunAtLoad` and a `StartCalendarInterval` at
  20:00. **`worker_tts.py` does NOT use `KeepAlive`** — it starts on a `StartCalendarInterval` at
  00:05, drains the queue, and exits. `KeepAlive` would hold Chatterbox resident through the Think
  phase, where there is no memory headroom at all (§2). If the worker dies mid-run, the batch
  restarts it; leases (§25) make that safe.
- **Restart is always safe** because jobs are idempotent and leased (§25). `kill -9` is a
  legitimate operator action and `ADMIN.md` says so in those words.
- **Memory ceiling:** `batch.py` 7GB, `worker_tts.py` 6GB (`settings.limits.*`) — process RSS, set
  so that RSS + the 5GB baseline stays inside the §2 phase budgets (~11.5GB Think, ~10GB Speak)
  rather than merely inside 16GB. A ceiling that permits 15GB of total pressure is not a ceiling.
  A process exceeding it logs ERROR and exits for the supervisor to restart it. Long-lived Python
  plus MLX will grow.

### macOS hardening

This kills more overnight jobs than any software bug.

- `sudo pmset -a sleep 0 disksleep 0` — disable sleep including on display sleep.
- **Disable automatic updates.** A 03:00 reboot mid-render is a lost night, and it will happen.
- Wrap the batch in `caffeinate -i`.
- launchd, not cron — cron does not survive a logout cleanly.
- Log to the external volume, not the internal disk.

---

## 22. Toolchain and dependencies

| Concern | Choice |
|---|---|
| Python | **3.12**, pinned in `.python-version` |
| Package manager | **uv** — `uv sync --frozen`, `uv.lock` committed |
| Lint + format | **ruff** (both), configured in `pyproject.toml` |
| Types | **mypy** — `strict` on `providers/`, `clock.py`, `*/store.py`, `retrieval/` |
| Hooks | **pre-commit**: ruff, ruff-format, gitleaks, mypy-on-changed, large-file guard, `canon-check --fast` (the model-free passes, §7). **pre-push**: `make check` and full `make canon-check`. **Never the test suite on commit** — slow hooks get bypassed |
| System tools | Homebrew: `ffmpeg`, `liquidsoap`, `icecast`, `postgresql@16` — versions in README |
| JS | **pnpm**, Node version in `.nvmrc` |
| Migrations | **alembic**, forward-only |

### Dependency policy

Add a dependency only when it saves more than ~200 lines you would otherwise maintain. Rejected,
with reasons, so nobody re-litigates:

- **No LangChain / LlamaIndex.** The retrieval in §5 is ~150 lines of SQL plus a reranker call. A
  framework here costs control over the exact thing that determines quality.
- **No Celery / Redis / RabbitMQ.** One machine, one operator. The render queue is a Postgres table
  with `SELECT … FOR UPDATE SKIP LOCKED`.
- **No Prometheus / Grafana.** Metrics go in a Postgres table and a daily email (§24).
- **No Docker on the Studio.** Native MLX and Metal access; containers cost you the GPU.

Updates: Renovate monthly, grouped, never auto-merged. Actions pinned to commit SHAs.

---

## 23. Configuration and secrets

One typed settings module. Everything tunable lives there; no magic numbers elsewhere.

```python
# src/station/config.py
class TTSSettings(BaseModel):
    cast_engine: str = "chatterbox"
    fallback_engine: str = "kokoro"
    target_lufs: float = -16.0
    per_turn_timeout_s: int = 120

class BatchSettings(BaseModel):
    start_hour: int = 20
    unload_writer_at: str = "00:00"
    must_finish_by: str = "06:50"   # audio pushed; REPORT at 06:55 is outside the deadline
    show_lead_days: int = 2
    junction_lead_days: int = 1

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
    database_url: PostgresDsn
    media_root: Path                      # /Volumes/station
    tts: TTSSettings = TTSSettings()
    batch: BatchSettings = BatchSettings()

settings = Settings()   # constructed once at import; fails fast on missing values
```

Layering, lowest priority first: defaults in code → `config/*.yaml` (non-secret, committed) →
`.env` (secrets, gitignored) → environment variables. **Fail fast at startup** — a missing required
value must crash on boot, never at 02:00 mid-render.

### Secrets

`.env` only, `chmod 600`, gitignored, with `.env.example` updated in the same commit as any new key.

| Secret | Used by | Stored | Rotate |
|---|---|---|---|
| `DATABASE_URL` | Studio | `.env` | on compromise |
| `ICECAST_SOURCE_PASSWORD` | Studio + Transmitter | `.env` / `/etc/settlement/env` | quarterly |
| `YOUTUBE_STREAM_KEY` | Transmitter | `/etc/settlement/env` | on compromise |
| `TRANSMITTER_SSH_KEY` | Studio | macOS Keychain / ssh-agent | annually |
| `BACKUP_ENCRYPTION_KEY` | Studio | **offline copy + password manager** | never (loss = no restore) |

- **Never in the repo, never in the database, never in logs, never rendered in a UI.**
- On the Transmitter: `/etc/settlement/env`, root-owned, `chmod 600`, sourced by systemd.
- **gitleaks in pre-commit *and* CI.** The repo is public — a leaked key is public instantly.
- Separate Postgres roles: `station_rw` (the pipeline), `panel_ro` (read-only plus explicit RPC
  functions for the buttons). Never one superuser for everything.

---

## 24. Logging and observability

**structlog, JSON to stdout, human renderer when attached to a TTY.** Configured once in `log.py`.
`print()` appears nowhere.

Bind context once at the top of a unit of work:

```python
log = logger.bind(run_id=run_id, phase="shows", programme_id=7, air_date="2026-07-30")
#                                          real UTC — never the in-world date (§31)
```

Standard fields: `run_id`, `phase`, `programme_id`, `segment_id`, `job`, `engine`, `duration_ms`,
`tokens_in`, `tokens_out`.

| Level | Means | Examples |
|---|---|---|
| DEBUG | Development only; includes full prompts | assembled context, raw model output |
| INFO | Lifecycle | phase start/end, script generated, render complete, playlist built, push |
| WARNING | Degraded but continuing | fell back to Kokoro, retry 2/3, rotation rule relaxed, beat slipped |
| ERROR | A human must look | render failed after retries, push failed, safety quarantine, pre-flight fail |

Every external call logs start and outcome with duration. **Never log** secrets, reference audio,
or full prompts above DEBUG.

Files: `/Volumes/station/logs/station.jsonl`, rotated daily, 30 days retained, shipped nowhere.
Single operator — `jq` is the log platform.

### Metrics

```sql
metrics(id, at timestamptz, run_id, metric text, value numeric, tags jsonb)
```

Recorded: segments produced, **archive pool hours and turnover**, render queue depth, **measured RTF per run**, buffer hours, tick
duration, phase durations, beats fired/slipped, safety rejections, back-time shortfall, rotation
relaxations, retrieval Recall@10.

### The one alert and the one report

- **Alert:** batch completion timestamp missing by 07:30 → email. That is the entire alerting
  system.
- **Daily digest, 07:00 email:** last night's phase timings, whether the window was met, segments
  produced, failures by type, buffer hours for D+1 and D+2, **archive pool hours against target**, beats fired vs slipped, quarantined
  items, measured RTF against the planned figure, and **disk free with days remaining at the
  current growth rate**. Below 30GB free the batch prunes the oldest archive audio automatically
  and says so; below 15GB it aborts in pre-flight rather than filling the volume mid-render.
  One email is the whole observability
  product.

**Watch the RTF trend.** A gradual decline is the earliest warning that the machine is thermally
degrading or the queue is growing, and it appears in the digest weeks before it becomes a short
broadcast day.

---

## 25. Error handling, timeouts, idempotency

**Every external call has an explicit timeout.** A hang is worse than a crash because nothing
alerts on it.

| Call | Timeout | On final failure |
|---|---|---|
| LLM writer (show) | 300s | fail the show; the slot falls to archive |
| LLM tick | 180s | abort the phase, log ERROR, keep yesterday's world |
| LLM small (items) | 90s | skip the item |
| TTS per turn | 120s | spill to Kokoro lane |
| Embeddings | 60s | defer to next sync |
| Reranker (CPU) | 15s | fall back to RRF order |
| rsync push | 600s | retry next cycle; transmitter has buffer |
| ffprobe | 10s | mark track unusable, log ERROR |

**Retries:** 3 attempts, exponential backoff 2s / 8s / 30s with jitter, **only for transient
failures**. Never retry a schema-validation failure — one repair prompt, then fail.

**Circuit breaker:** 5 consecutive failures on a TTS engine trips the lane to Kokoro for the rest
of the run, logs WARNING, and keeps rendering. Trips appear in the digest.

**The render queue records its own history.** Beyond `status` and `priority`: `started_at`,
`finished_at`, `worker_id`, `worker_version` (git SHA), `attempts`, `engine`, `error`. Debugging a
render that sounded wrong three months ago is impossible without knowing which code and which
engine produced it.

**Queue leases, not just locks.** `SELECT … FOR UPDATE SKIP LOCKED` hands a job to one worker, but
a killed worker leaves the row in `running` forever. Every claimed job carries `worker_id` and
`leased_until` (now + 2× timeout); a reaper pass returns expired leases to `pending` and increments
`attempts`. After 3 attempts the job is `failed`.

**Idempotency:** every job is keyed `(job_type, target_id, air_date)`. Re-running produces the same
result or a no-op. This is what makes "just run it again" safe at midnight, and what makes a
partially-completed batch resumable rather than restartable.

**The unbreakable rule:** never silently produce nothing. Fall back or raise. A quiet empty result
is the failure mode you cannot debug three weeks later.

---

## 26. Caching and performance

### Prompt prefix stability

Context is assembled in a **fixed order, stable content first**:

```
[ station core ] [ domain summaries ] [ cast cards ] │ [ facts ] [ world slice ] [ coverage 24h ] [ brief ]
└──────────── stable, cacheable ─────────────────────┘ └────────── variable ──────────────┘
```

Local runtimes reuse the KV cache across calls sharing a prefix. **Never interleave variable
content into the stable head** — one changed token at position 40 invalidates everything after it.
On a memory-bandwidth-limited machine this is the difference between a comfortable batch window and
a tight one.

*Verify empirically:* how reliably the MLX backend reuses KV cache across separate requests is
worth measuring once on the real hardware. The ordering costs nothing either way, so keep it — but
do not budget around a speedup you have not observed.

### Other caches

| Cache | Key | Invalidated by |
|---|---|---|
| Embeddings | `fact_key` + `text_hash` | text change only |
| Domain summaries | domain + git tree hash of its files | a file in that domain changing |
| Track durations | path + mtime | file replacement |
| Rendered pool + imaging | script hash + voice + engine | never — that is the point |
| `now.json` at the edge | — | `Cache-Control: max-age=15` |

The duration cache matters more than it looks: the playlist builder runs hourly and must never
re-probe the catalogue.

### Performance budgets

Batch mode relaxes almost everything. Only two things are truly time-critical: **the batch must
finish by 06:50**, and **the transmitter must hit `:00`**. Everything else is a WARNING with the
measurement logged.

| Operation | Budget |
|---|---|
| Context assembly | 2.5 s |
| Hybrid retrieval + CPU rerank | 1.5 s |
| Script generation (25-min show) | 300 s |
| Per-turn TTS | measured RTF × turn length |
| Playlist build | 10 s |
| Snapshot publish | 5 s |
| World tick, end to end | 30 min |
| **Assemble — mix, loudness, C2PA, cue sheets, for one night's fresh output** | **20 min**, measured in phase A before it is relied on (§36.3) |
| **Whole batch** | **must complete by 06:50** |

### Required indexes

Write these in the first migration; retrofitting is painful.

```sql
CREATE INDEX ON beats (occurs_at, status);
CREATE INDEX ON beats (thread_id, occurs_at);
CREATE INDEX ON coverage (thread_id, aired_at DESC);
CREATE INDEX ON coverage (programme_id, aired_at DESC);
CREATE INDEX ON airplay (track_id, aired_at DESC);
CREATE INDEX ON airplay (aired_at DESC);
CREATE INDEX ON items (expires_at);   -- NOT partial: now() is STABLE, not IMMUTABLE,
                                      -- and Postgres rejects it in an index predicate
CREATE INDEX ON facts USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON facts USING gin (tsv);
CREATE INDEX ON facts (scope, station_id, status);
CREATE INDEX ON render_queue (status, priority DESC, created_at);
CREATE INDEX ON tracks (category, energy);
CREATE INDEX ON chart_entries (chart_date, chart_id, position);
CREATE INDEX ON threads (stage);
CREATE INDEX ON facts (domain);                        -- the diversity cap counts by domain
CREATE INDEX ON render_queue (leased_until) WHERE status = 'running';   -- the reaper
CREATE INDEX ON segments (air_date, air_time);
CREATE INDEX ON settlements (parent_id);
```

---

## 27. Security

**Threat model.** Single operator, public read-only stream, no user accounts, no PII, public
source. Real risks in order: a leaked key in a public repo; an exposed admin surface; losing the
world database; supply-chain compromise; prompt injection if external text is ever ingested.

| Surface | Control |
|---|---|
| Transmitter firewall | 80/443 open; 22 restricted to Tailscale; everything else denied |
| Studio | **No inbound at all.** Tailscale only. Local services bind `127.0.0.1` |
| SSH | Key-only, no password auth, no root login, fail2ban |
| Icecast | Admin interface bound to localhost; source password from secrets; defaults removed |
| Public JSON | Rate-limited at the Vercel edge; no query parameters reaching a database |
| Panel | Tailscale identity only; `panel_ro` DB role; never internet-exposed |
| Backups | Encrypted with `age` **before** leaving the machine |
| Supply chain | `uv sync --frozen`, lockfile committed, Actions pinned to SHAs, no post-install scripts |

**Prompt injection.** Canon and grid are trusted because you write them. The moment anything
external enters — scraped text, listener submissions, a feed — it is untrusted data: wrapped in a
delimited block, never able to alter instructions. Two absolute rules regardless of source:

- **No model output is ever executed.** No `eval`, no shell interpolation, no dynamic import.
- **No model output becomes a filesystem path.** Slugify against an allowlist, join to a fixed base
  directory, then verify the resolved path is still inside it.

**Public repo hygiene.** Open code is fine; security comes from secrets and access control. But: no
real hostnames or IPs in committed config, no `.env.example` with real-looking values, gitleaks on
every commit and every CI run.

---

## 28. Data lifecycle

**Migrations.** Alembic, forward-only. Schema changes land as migrations, never truncate-and-reseed,
once the world is alive. A migration that would lose world history requires an explicit
data-preserving path.

**Backups.** Two jobs, not one. `make backup` runs nightly: `pg_dump -Fc`, encrypted with `age`,
written to the external volume and shipped offsite. `make backup-media` runs **weekly** and syncs
`music/`, `imaging/`, `pool/` and `voices/` to the same offsite bucket — these are irreplaceable
(§28's survival table requires them) and they change rarely, so a weekly delta is enough. Retain 30 daily and 12 monthly. Runs at the end of the batch, before the digest.

**Restore drills, quarterly, scripted.** `make restore-test` restores the latest backup into a
scratch database and asserts row counts across core tables. A backup you have never restored is not
a backup — put it in the calendar.

**Retention:**

| Kind | Kept |
|---|---|
| **4-minute junctions** (bulletins and overnight summaries) | deleted after air |
| **28-minute news programmes** (`The Six`, `The Midnight Report`) | 30 days, then archive pool |
| Floating shows | 30 days on the Transmitter, then archive pool |
| Pool + imaging | forever |
| Archive items | until 12 plays, 18 months, or marked stale (§14) |
| Threads, beats, coverage, figures, quotes | forever — the world's history |
| Items | 7 days |
| Logs | 30 days |

**Retention is keyed on `slot_minutes == 4`, not on `format_class == junction`.** The two used to be
the same thing; §13 made them different when 28-minute news programmes became junction-class, and
keying on the class silently deleted the main news programme of the day — which `/archive` (§16)
promises listeners they can browse. A `The Six` from last Tuesday is worth keeping for the same
reason any other programme is; a bulletin from last Tuesday is not, because it is four minutes of a
clock reading that no longer applies.

**What must survive total loss:**

| Asset | Where | Recoverable? |
|---|---|---|
| Canon | git | yes |
| Voice reference clips | git | yes |
| Music + imaging files | offsite object storage | yes |
| World database | nightly encrypted backups | yes, to last night |
| Config, prompts, grid | git | yes |
| Rendered audio | — | **no, and that is fine** — it regenerates |
| Backup encryption key | password manager + offline copy | **no. Lose this and lose everything.** |

Audio grows ~1GB per broadcast hour per day. At 8 fresh hours that is ~8GB/day before retention.
Monitor free space in the pre-flight check and the digest; the retention rules are what keep the
disk alive.

---

## 29. Testing

Test count is not the goal; catching bugs you would actually have shipped is. **Five kinds exist.
There is no sixth.**

1. **Unit** — pure logic with real consequences: the clock and phrase renderer, the back-timer, the
   world ranker, rotation separation and fatigue, chart scoring, duration estimation, the diversity
   constraint, the horizon bounds. Target ~60 tests total.
2. **Conformance** (§3) — every provider implementation against one shared suite, plus the timed
   assembly test. This is what makes the seams real.
3. **Model benchmark** (`make benchmark MODEL=…`) — the gate a candidate must pass before replacing
   a production model. Five measures: generation speed at realistic context, JSON validity across
   20 runs, retrieval faithfulness (does every claim trace to context), hallucinated-entity rate
   against `figures`/`settlements`, and script length accuracy against the duration estimate.
   **Pass thresholds, because a gate without a number is not a gate:** JSON schema validity ≥19/20
   runs; hallucinated entities 0 across 5 scripts; duration estimate accurate to ±10%; retrieval
   faithfulness ≥95% of claims traceable; generation speed such that a 25-minute script completes
   inside its 300s timeout. Results land in `DECISIONS.md`. **Prose and audio quality are not in the
   benchmark** — this
   suite disqualifies candidates cheaply, it never decides which sounds better.
4. **Golden** — two kinds, both diffed by a human, neither asserting content:
   - *Generation goldens:* prompts against stored inputs; schema validity and rough length only.
   - *Retrieval goldens:* the §5 eval set, asserting Recall@10 has not dropped below baseline.
     This catches a regression after changing the embedding model or reranker — a change that
     otherwise looks like a green build and sounds like a worse station three weeks later.
5. **Smoke** — two variants:
   - *CI smoke:* tick → script → render (Kokoro, 30s) → mix → playlist → push to a temp directory.
     Under 5 minutes. Proves the pipeline is connected.
   - *Studio smoke* (`make smoke-full`, not in CI): one full segment through the real cast engine,
     with ffprobe assertions on duration, sample rate, loudness and cue-sheet offsets. The CI
     variant cannot catch assembly bugs, loudness drift or timing error. Run before any deploy
     touching rendering.

**Explicitly do not write:** tests for glue code or config plumbing; mocks of your own store (use a
real test database); anything chasing a coverage number; tests asserting what a model said; tests
requiring a loaded model in CI.

**The deletion rule:** if a test would not have caught a bug you would actually have shipped, delete
it. Apply quarterly.

**Quality is judged by ear**, on the blind sample. No test, gate or harness grades the product.

---

## 30. Continuous integration

GitHub Actions, three workflows, no models, no production access.

| Workflow | Trigger | Does | Budget |
|---|---|---|---|
| `pr.yml` | PR + push | ruff, mypy, unit tests, gitleaks, `uv lock --check` | < 3 min |
| `nightly.yml` | cron | CI smoke (Kokoro on CPU — the one exception to "no models", it is 82M and CPU-only), conformance with stub engines, retrieval goldens against **pre-embedded fixture vectors** so no embedder runs in CI | < 15 min |
| `web.yml` | changes in `web/`, `panel/` | typecheck + lint; Vercel builds separately | < 3 min |

- Actions pinned to commit SHAs.
- **No secrets available to fork-triggered workflows** — the repo is public.
- CI never touches the production database or the Transmitter.
- **Deployment is manual**: `make push` / `make deploy` from the Studio. For a one-operator station,
  automated deploy to a live broadcast is risk without benefit.

---

## 31. Code standards

- **Type hints everywhere.** mypy `strict` on `providers/`, `clock.py`, every `store.py`,
  `retrieval/`.
- **Modules ≤ 400 lines, functions ≤ 50.** Longer means it is doing two things. **`store.py` files
  are exempt from the line limit but not from cohesion**: split by entity into
  `world/store/{threads,beats,items,figures,coverage}.py` re-exported from `world/store/__init__.py`.
  The rule is that SQL lives in the store layer, not that it lives in one file.
- **In-world dates appear in rendered prose and in the rundown header. Everywhere else — CLI
  arguments, filenames, log lines, the database — the date is real UTC.** The rundown header prints
  both, which is the one place the two are allowed to meet.
- **All timestamps UTC and timezone-aware in the database.** In-world time is *derived* in
  `clock.py`, never stored as a second column. One clock, one conversion point.
- **Structured types across module boundaries** — dataclasses or Pydantic models, never dicts as
  informal structs.
- **Docstrings say why, not what.** The signature already says what.
- **No** `print()`, **no** `os.getenv` outside `config.py`, **no** `datetime.now()` outside
  `clock.py`, **no** inline SQL outside a `store.py`, **no** vendor SDK outside `providers/`.
- Errors carry context: which show, which turn, which engine, which attempt.

---

## 32. Documentation policy

**Six documents. That is the cap**, and it is the single most important lesson from the previous
attempt, where a growing pack of phase documents became a machine for generating work.

| Document | Contains | Updated when |
|---|---|---|
| `ARCHITECTURE.md` | This document — how it works and why | a decision changes |
| `ADMIN.md` | How to operate it: every make target, every recovery procedure | a command changes |
| `DECISIONS.md` | Append-only ADR log, one paragraph each — including things tried and reverted | a decision is made |
| `TASKS.md` | Current work, maximum 10 items (§33) | every session |
| `README.md` | Reproducible install from scratch | a dependency changes |
| `CLAUDE.md` | **One page.** The non-negotiables only, pointing here for detail | rarely |

Three further files sit **outside this cap** because they are operator-owned reference material, in
the same class as canon rather than as process documentation. None generates tasks by itself:

| File | Contains | Read by an agent |
|---|---|---|
| `PRODUCT.md` | The idea, principles, audience, milestones | never |
| `PROGRAMMING.md` | Domains, formats, dayparts, presenters — the input to `grid.yaml` | only on grid or showrunner tasks |
| `PHASES.md` | The eleven phases: goal, outcome, hardware, accounts, content, dependencies | only in a planning session (§33) |

**Nine documents, and that is the cap.** `PHASES.md` was added because the roadmap had no home: §35
holds the technical build order, but sequencing, milestones, hardware lead times, accounts and the
outward-facing work (the site, the channel, support, social) had nowhere to live and were being
reconstructed in conversation each time. It is a roadmap, **not a phase pack** — it describes phases
at one paragraph each and holds no tasks, no checklists and no per-phase sub-documents. If it ever
starts generating work by existing, it has become the thing §34 forbids and should be cut back.

### Which document wins

Precedence was previously stated four times in four places, in terms that did not quite agree. **It
is stated once, here, and nowhere else.** An agent that finds two documents disagreeing consults
this table, acts on the winner, and records the disagreement under `## Observations` — it does not
stop, and it does not try to reconcile them mid-task.

| Question | Authority | Everyone else defers |
|---|---|---|
| How the system works, and why | `ARCHITECTURE.md` | all |
| **Ordering** — what is built when, phases, milestones, prerequisites, lead times | `PHASES.md` | §35 defers on ordering; it stays the *technical* build order |
| **The schedule** — hours, slots, strands, which programme sits where | `PROGRAMMING.md` §8 | §15 defers; it holds only the principle |
| **Editorial** — domains, formats, presenters, register | `PROGRAMMING.md` | — |
| What was decided, and when | `DECISIONS.md` | outranks every other document *and* memory; if it disagrees with the code, one of them is wrong and fixing it is a task |
| The non-negotiables an agent must not break | `CLAUDE.md` | but on any conflict **of fact**, `ARCHITECTURE.md` is right and the disagreement is recorded |
| How to operate it | `ADMIN.md` | and it may only describe commands that exist |
| What the product is for | `PRODUCT.md` | never read by an agent; generates no work |

**Two rules that resolve almost every real case.** A *later* `DECISIONS.md` entry beats an earlier
line anywhere else, including this document — that is what append-only means. And where the conflict
is about **when**, `PHASES.md` wins; where it is about **what** or **how**, `ARCHITECTURE.md` wins.

Rules:

- **No phase packs.** Ever.
- **An agent may not create a new document** without the operator asking for one.
- **Do not document a command in `ADMIN.md` before it exists.** `ADMIN.md` is what you follow at
  02:00 and every line in it must work. §17's target list is design — it says what the surface will
  be — and a target moves from there to `ADMIN.md` when it runs.
- **`CLAUDE.md` must stay one page.** Agents skim long documents — that is a fact about how they
  work, not a failing to design around. Claude Code loads it automatically, so the non-negotiables
  belong there and nowhere else: WIP 1 · agents may not add tasks · agents may not create documents
  · all model calls through `generate_structured` · vendor SDKs behind `providers/` · no
  `os.getenv` outside `config.py` · no `datetime.now()` outside `clock.py` · no SQL outside a
  `store.py` · the definition of done · ask before destructive actions. Every line must be
  checkable. The moment it grows a second page it stops being read.
- If a document contradicts the code, one of them is wrong — fix it in the same session.

---

# Part III — Working

---

## 33. How agents work this repo

This section is the anti-sprawl mechanism. The previous attempt failed not because the code was bad
but because **the work generated more work**, indefinitely, with no external stopping condition.

### The task format

`TASKS.md` holds **at most 10 items**. To add one, ship or remove one.

```markdown
### T-042 · Back-time the hour from the pool
Goal: the built hour lands within 500ms of :00.
Reads: ARCHITECTURE §13, §14
Files: src/station/schedule/backtime.py, playlist.py, tests/unit/test_backtime.py
Check: `make hour` on a seeded day prints a shortfall under 500ms for 24 consecutive hours.
```

If you cannot state the observable check, it is not a task yet — it is a thought.

**`Reads:` names the architecture sections the task needs.** `CLAUDE.md` tells an agent to read
only the sections a task names, so the format has to give it somewhere to name them.

**`Goal` and `Check` are written for a non-developer; `Reads` and `Files` are agent bookkeeping.**
The operator does not review implementations — they review *what will be true when this is done*,
and whether they can see or hear it. A `Check` that only another developer could evaluate is a
badly written check, not a technical necessity.

### The planning session

The operator is not a developer and cannot author task cards. Requiring it would stop the project,
so **an agent drafts cards and the operator accepts them** — authorship moves, authority does not.

Four rules keep this from becoming the thing §34 forbids:

1. **Declared, never incidental.** A planning session happens because the operator asked for one. An
   agent finishing a coding task still ends with `## Observations` and nothing else.
2. **One phase at a time.** A session covers the current phase of `docs/PHASES.md` and stops.
   **Planning every phase up front is a phase pack**, which is precisely what killed the previous
   attempt (§34), and the 10-item cap exists to make it impossible.
3. **Card by card.** Each draft is accepted, rewritten or rejected explicitly. Silence is not
   acceptance.
4. **It produces no document.** Output is cards in `TASKS.md`. Not a plan, not a roadmap, not a
   summary of the plan. §35 is already the roadmap and does not need restating.

### Definition of done

Code, plus the one kind of test that applies (§29), plus `ADMIN.md` if a command changed, plus a
`DECISIONS.md` line if a decision was made, plus `make check` green. **Nothing else.** Not a summary
document, not a new pack, not a gate.

### Standing rules

- **WIP limit 1 — for agent tasks.** One agent task at a time, finished, before the next. Operator
  content items (`[operator]`, the §35 content track) sit in `TASKS.md` alongside them and do not
  consume the slot; writing canon for a fortnight must not block every code task behind it.
- **An agent may not decide what work exists.** It may end a session with an "Observations" list;
  the operator decides what becomes a task. This is the most important rule in this document, and
  it survives the planning-session exception below intact — because the exception moves *authorship*
  to the agent while leaving *authority* with the operator.
- **A null result is a completed task.** "Measured, no improvement, reverted" is success.
- **The default for any judgment call is no change.**
- **Ask before destructive actions.** `make reset-world` and anything irreversible.
- **Never regress the plain-speech register.** It is load-bearing and hard-won.
- **Editing this document is a task like any other** — it takes a `TASKS.md` slot, obeys WIP 1, and
  lands with a `DECISIONS.md` entry. `ARCHITECTURE.md` is meant to change when decisions change.
- Every session ends with three things: what changed, exactly how to verify it, what you noticed.

### What an agent may edit

`grid.yaml`, `banned-entities.yaml`, imaging placement config and `music/catalogue.yaml` — all
structured config with mechanical validations behind them, on a task that names the file.

### What the operator owns and never delegates

Canon, cast cards, speech profiles, voice reference clips, and every audio asset. Beyond those:
deciding what is worth building. Judging whether it sounds good. Writing canon. Resolving canon
conflicts. Reviewing major beats after the fact and cancelling the ones you dislike (`make beat-cancel`) —
never approving them in advance, because nothing in the batch waits for a human. Everything else
can be delegated.

---

## 34. Anti-patterns

Each has a specific reason, recorded so nobody re-opens it in month three.

- **No phase packs, no task-generating documents.** The failure mode of the last attempt.
- **No harness that grades its own output.** Quality is judged by ear, by you.
- **No abstraction with a single implementation** — except the two seams, which ship two (§3).
- **No microservices, no message broker, no Kubernetes.** One machine, one operator.
- **No retrieval framework.**
- **No feature flags.** One deployment, one operator.
- **No admin surface reachable from the internet.** Not "behind a login" — not reachable.
- **No test whose failure would not change what you ship.**
- **No metric you will not look at.**
- **No building for a second station until you build one.** `scope`/`station_id` is enough.
- **No regenerating a segment because it could be better.** Ship it; note it in Observations.
- **No panel before 30 days on air.** Build what you actually reached for, not what you imagined.

---

## 35. Build order

Each step ends in something audible or visible.

> **The steps below are grouped into eleven phases by `docs/PHASES.md`**, which is where sequencing,
> milestones, hardware, accounts and cross-phase dependencies live. A planning session works in one
> phase at a time (§33). This section stays the *technical* build order and does not restate any of
> that; where the two disagree about ordering, `PHASES.md` wins (§32).

### The content track — runs in parallel, and half of it gates the engineering track

None of this is code, all of it is prerequisite, and it is the half most likely to be forgotten
when the work is split into tasks.

| # | Item | Gates |
|---|---|---|
| C1 | **Canon seed** — the bible at enough depth for retrieval to be meaningful (~150+ facts, all domains present) | eng 4, 6, 7 |
| C2 | **Cast cards + speech profiles.** The tier-1 grid needs **six**, not three or four: a breakfast host, an evening host, a `scripted` newsreader, a chart voice, and **two beat correspondents** — correspondents are `cast` rows with authored `scripted` profiles, not `figures`, and every two-way needs one (§11a, `PROGRAMMING.md` §5). A host may carry several strands within a daypart, so the roster grows with the freshness tier rather than with the grid | eng 8 |
| C3 | **Voice reference clips** — 10–20s synthetic WAV per presenter, committed, with `voices/PROVENANCE.md` (§3, §18) | eng 8 |
| C4 | **`grid.yaml`** — programmes, hosts, dayparts, hour clocks (§17a) | eng 9, 10 |
| C5 | **Suno catalogue** + `music/catalogue.yaml` + licence evidence | eng 13, 15 |
| C6 | **Imaging pack** — logo, stings, beds, opens/closes, disclosure sting | eng 12 |
| C7 | **Pool pieces** — 37 minimum across three length bands (§13) | eng **10** (back-timing cannot run without some pool at all) and eng **13c** (where the 37 minimum is reached and `make pool-check` goes green) |
| C8 | **`banned-entities.yaml` seed** | eng 4 |
| C9 | **Stock voice bank** — 12–20 synthetic reference clips for `figures` (§3), varied by age, register and settlement. Required by every two-way, interview, vox pop and package, i.e. by most of the grid | eng 8 |
| C10 | **LICENSE decision** — the repo is public. Code and canon/voices probably want different terms; MIT or Apache-2.0 for `src/`, a restrictive or all-rights-reserved statement for `canon/`, `voices/` and `music/` | before the repo is public |

0. **Scaffold** — repo layout, toolchain, `config.py`, `log.py`, Makefile, hooks, CI (§21–22).
0b. **Task zero: resolve the five model slots** to real downloadable artifacts and pin repo +
    revision + quantisation in `models.yaml` (§2). Before any measurement.
1. **Measure sustained RTF, 60 minutes** (§36). Goes in `config/measured.yaml` before any
   scheduling code exists.
2. **Transmitter** — Liquidsoap + Icecast + the six-level playout ladder + the **pinned hourly
   junction slot** + `disclosure_sting`, playing placeholder files. A URL that never dies. *This has
   never existed and it is the thing you are missing.*
   **Keep it unlisted and access-restricted until step 15 clears** — step 15 forbids public
   listeners, and a public stream before then would contradict it and raise a placing-on-the-market
   question you have not yet put to a lawyer (§18).
3. **Schema + Alembic + `canon-sync`** — facts, embeddings, domain summaries.
4. **`canon-check`** — conflicts, links, IP screen, register. Run it against existing canon and fix
   what it finds. You will learn a lot about your own world here.
5. **Clock + phrase renderer** — air-time rule, granularity ladder. Tested.
6. **Retrieval** — hybrid + RRF + CPU reranker + diversity shaping + the eval set. Verify by hand
   on ten queries.
7. **World schema + nightly tick** — threads, beats, items, horizon floor and ceiling, pre-simulated
   micro-ticks.
8. **One floating show** — whole script, two speakers, rendered, mixed, on the Transmitter.
   ***The go/no-go moment.*** This is where you find out whether the local writer is good enough.
9. **Junctions + the pinned-slot contract** end to end. Now the hour has a top and the day moves.
10. **Playlist builder + pool + back-timing.** The hour lands on `:00`.
11. **The batch runner** — phases, priority order, N+1 buffer, pre-flight, launchd, macOS hardening.
11b. **The rundown** (§14a) — the first thing that makes the station legible to you. An afternoon,
    and it is what you will read every morning for the next year.
12. **Imaging pack + `make music-analyse`** — the hour clocks, ramps corrected by ear.
13. **Music model + rotation + one music show** end to end. Proves the cheap format before you
    depend on it for capacity.
13b. **Force the voice-identity decision** (§3) — bulk re-render versus an in-world host change —
    **before 50 shows exist**, not before 500. Record it in `DECISIONS.md`. It costs nothing now
    and is irreversible later.
13c. **Build the pool to the §13 minimums.** `make pool-check` green.
14. **Safety gate + C2PA + disclosure + `/ai-transparency`** — including forcing all six playout
    levels (0–5), `make verify-marking` after push, and the YouTube synthetic-content flag.
    **Required deliverable: a `DECISIONS.md` entry recording which marking mechanisms were chosen
    and why they are considered to satisfy Art. 50(2).** The justification is part of the
    compliance posture, not documentation of it.
15. **Legal review — a hard gate with written sign-off.** A Polish media lawyer with EU AI Act
    familiarity reviews the disclosure package, the news-shaped-fiction question (now sharper,
    because the news register is professionally read — §11a), the Suno commercial-use evidence, and
    whether KRRiT registration applies. Three artefacts must exist before this starts: the
    `DECISIONS.md` marking justification, the Suno licence evidence file, and a written statement
    of what the station broadcasts. **No public listener before this closes**, and the outcome is
    written down rather than remembered.
16. **Pre-built archive pool — 165 hours before launch (135 is the floor).** The grid consumes
    ~9.5 archive hours a day, seven days a week — ~66 h/week — and it cannot be built after going
    live. The 14-day separation rule (§14) is what sets 135 as the floor; below it, recurrence is
    audible within a fortnight. Lead with history documentaries and music retrospectives (slow
    domains, §1 of `PROGRAMMING.md`) — time-neutral and the cheapest per render-minute.
    **~4,000 speech-minutes in total: ~19 nights of pure archive render, realistically a couple of
    months alongside everything else.** That is accepted: there is no launch date, so pre-launch
    render time is free (`DECISIONS.md` D-006) and the levers in D-003 stay unused.
    **What is not free is doing it too early.** 165 hours is ~165 programmes, well past the 50-show
    line at step 13b, and the archive is the deepest lock-in in the system (§3) — build it after the
    voice and register have survived real listening, not while waiting for them. Keep the top-up
    phase running after launch; steady state is ~30 min/day.
17. **Public site** — player, schedule, programmes, about, `/ai-transparency`.
18. **Go live.**
19. *(week 3+)* Chart show, once real airplay history exists.
20. *(day 30+)* Ops panel, built from what you actually reached for.

Steps 1–11 are the system. If those work, the rest is filling in.

---

## 36. The measurements

**Two are gates and one is a budget.** Measurements 1 and 2 can end the project; §1 calls them the
two numbers that gate everything, and that is still true. §36.3 cannot end anything — it establishes
a number the batch timetable currently assumes.

**Ordering, because these are not all doable on day one.** Measurement 1 needs only the TTS engine
and a script file — run it immediately, before any pipeline code. Measurement 2 needs real canon, a
real world slice and a real brief, so it lands after build steps 3–7; that is the first moment it
can be run honestly, and it must be run *before* step 8's pipeline work is extended any further.
§36.3 needs only rendered files and ffmpeg, so it runs alongside measurement 1.
All three verdicts go in `DECISIONS.md`.

### 1. Sustained TTS RTF — 60 minutes, not 5

A five-minute burst on an idle machine flatters you. What matters is a sustained figure under the
real resident set.

**Protocol:**

1. Warm the engine with a real script.
2. Render continuously for **60 minutes**: a realistic mix of 4-minute two-hander scripts with
   overlaps and nonverbals, plus idents.
3. Record wall-clock, RTF, **peak memory**, and whether throttling occurred — compare the first ten
   minutes against the last ten.
4. Record the number in `config/measured.yaml`. The batch planner reads it.

The render window is **00:05 → 06:30 = 6h25m (385 min)**. Speech is ~75% of a talk slot, the rest
being imaging, beds and links. On the `4 + 28 + 28` / `4 + 56` clock (`PROGRAMMING.md` §7), a
**fresh talk hour** therefore holds ~46 minutes of speech (a 4-minute junction plus 42 across the
programme slots), a **half-fresh hour** ~25, a **music hour** ~10, and an **archive hour** just its
4-minute junction. Every hour carries a junction: 4 minutes of speech by day, ~2 overnight.

**The capacity lever is the freshness tier, not the format mix.** Now that the daytime is speech
throughout, there are almost no music hours to trade against — so the way a smaller machine runs
this grid is by moving programmes from `F` to `W` to `A`, exactly as `PROGRAMMING.md` §9 tiers them.
That is an editorial decision with a stated cut order, not a silent substitution.

The grid in `PROGRAMMING.md` §8 costs this much fresh speech per day:

| | Total |
|---|---|
| 24 × 4-min junctions (20 bulletins + 4 overnight summaries) | 88 |
| Fresh (`F`) programmes as listed | ~399 |
| Weekly (`W`) programmes — nine strands, 364 min/wk amortised | ~39 |
| Archive (`A`) and repeats | 0 |
| **Weekday, fresh speech per day** | **~526** |
| **Weekend day** (twelve slots overridden, §8) | **~295** |
| **Weekly average** | **~460** |

**A weekday is roughly two and a half times a 0.7× machine's budget** and the week as a whole a
little over two, which is why it ships in tiers:

| Capacity | Tier |
|---|---|
| ~200 min (RTF 0.7) | All junctions · one hour of breakfast · the flagship · the six · the chart. Everything else `W` or `A` |
| ~300 min (RTF 1.0) | Add the midday report, finance, sport, the midnight report |
| ~460 min (RTF 1.5) | Add full breakfast, late analysis, discussion, the long interview |
| ~526 min | The weekday as written |

**Capacity is a per-night constraint, so the tier is judged against the weekday.** The two weekend
nights come in at roughly half, which is where `W` production and archive top-up are scheduled
(`PROGRAMMING.md` §8).

**The tiers count fresh speech only, and archive top-up is not free.** §14 puts steady-state
replenishment at ~30 speech-min/day, so a tier is affordable when `fresh + archive ≤ usable`, not
when `fresh ≤ usable` — and on that reading every tier above is roughly 30 minutes optimistic
(216 usable against the ~200 tier, 308 against ~300, 462 against ~460). **Two things absorb it and
neither is a reason to ignore it:** archive sits last on the priority ladder and is designed to be
dropped on a long night, and retired daytime programmes enter the pool for free after 30 days
(§28). How much the second covers depends on how time-neutral the day's output is, which is not
known until the station has run — see §14. Until then, **plan the tier one notch below the RTF
band it appears to buy.**

`PROGRAMMING.md` §9 holds the cut ladder and the three programmes that are never cut.

**Bulletins are the single largest line and the cheapest to make.** Music links are the second, and
the least noticed — 6 minutes per hour, not 12; a real music host speaks for well under a tenth of
their airtime.

| Sustained RTF | Speech in 385 min | After ×0.8 derate | Verdict against `PROGRAMMING.md` §9 |
|---|---|---|---|
| 1.5× | 578 | 462 | The ~460 tier. ~64 short of the weekday as written (~526) |
| 1.2× | 462 | 370 | Between the ~300 and ~460 tiers |
| **1.0×** | 385 | 308 | **The ~300 tier. This is the pass threshold** |
| 0.7× | 270 | 216 | The ~200 tier: bulletins, one breakfast hour, the flagship, the chart |
| 0.3× | 116 | 92 | Below every tier — bulletins plus one strand, the rest archive |

The RTF ≈ 1.0× pass threshold is not arbitrary — it is what the ~300 tier costs. Below it the lever
is **freshness, not format**: this is a speech station and there are no music hours left to trade
against (§11). Moving one 56-minute strand from `F` to `W` with two repeats cuts its cost by two
thirds, and sending `Night Record` to archive cuts it to zero and costs nothing at all, because
slow-domain music content is good for months.

**The measured figure is a ceiling, not a plan.** Real sustained throughput on this machine will
sit below a clean benchmark, and a single re-render or a late show eats the difference. So:

```
planned_speech_minutes  ≤  measured_speech_minutes × 0.8
```

**The batch planner enforces this and refuses a grid that exceeds it**, with an error naming the
overage in minutes. This is the mechanism that stops you quietly programming more talk than the
machine can render, discovering it at 04:00, and getting a short day. Any shortfall is flagged in
the rundown.

**The freshness tier is the biggest capacity lever you have.** Moving one 56-minute programme from
`F` to `W` with two repeat slots cuts its cost by two thirds; moving it to `A` cuts it to zero. That
is why the cut ladder in `PROGRAMMING.md` §9 reaches for freshness before it touches the schedule —
a repeat is invisible to the grid and audible only as an honest announcement. If throttling costs more than 30%, these numbers move
and the blocks shrink.

**Measure context and KV growth at the same time.** The Think phase is the tight one at 16GB, and
KV grows with context. Record peak memory at a realistic assembled context (Tier 0 + all domain
summaries + the 40-item Tier 2/3 budget ≈ 20–24k tokens) and again at **act 2** carrying act 1's
summary and verbatim tail — the 2-act cap (§11) makes that the largest context the system ever
builds.

**Written go/no-go, recorded in `DECISIONS.md` before any pipeline code:**

| Gate | Pass | Marginal | Fail |
|---|---|---|---|
| Sustained RTF | ≥1.0× after throttle | 0.5–1.0× | <0.5× |
| Peak Think-phase memory | ≤12 GB | 12–14 GB | >14 GB |
| Throttle loss over 60 min | <15% | 15–30% | >30% |

Marginal means proceed at a lower freshness tier (`PROGRAMMING.md` §9) — not with more music,
which this grid no longer has to trade. Fail means the hardware decision
reopens before code is written, not after.

### 2. One show script, read cold

Generate one full 20-minute two-hander with real canon, a real world slice and a real brief. Print
it. Read it away from the screen.

This is the actual risk in the project. Everything else is solvable engineering; whether a 9–10B
local model writes radio you want to broadcast is not knowable in advance and not fixable by
architecture.

**If any programme will use acts, read a 2-act script, not a 1-act one.** The act-2 handoff (a
300-word summary plus the last 800 words, §11) is the most likely coherence cliff in the system,
and a single-act sample will not reveal it.

**The criterion, written down before you read it, so you cannot negotiate with yourself
afterwards:** would you leave this playing while someone else was in the room? Not "is it
impressive for a local model" — that question has no useful answer.

If the answer is no, the choice is between larger hardware and a small paid budget for flagship
scripts only. Record the verdict and the decision in `DECISIONS.md`.

**There is a cheap week-one version of this test and a real one.** In week one, hand-write the
context for a single 20-minute two-hander — no retrieval, no canon pipeline, no grid — and read it.
That is a day of work and it answers the only question that matters: can this model hold two voices
apart for twenty minutes. The full measurement, on real retrieved context, still lands after step 7.
It is far better to face the cheap version in week one than the real one in month three.

### 3. The assemble pass — a budget, not a gate

§14 gives the whole assemble stage **20 minutes**, 06:30 → 06:50, and that figure was written down
rather than measured. It covers mixing fresh segments with imaging, loudness normalisation, C2PA
signing and cue sheets, across several hundred files. Signing is per-file and is the part most
likely to surprise.

**Protocol, an afternoon in phase A:** render ~50 representative segments, then run the real
assemble path over them — mix, normalise, sign, write cue sheets — and time it end to end. Divide
by the segment count, multiply by a full night's fresh output at the tier the RTF measurement
bought. Record the per-file and per-night figures in `DECISIONS.md` and the budget in
`config/measured.yaml` beside the RTF.

**Why it is not a gate.** A slow assemble cannot end the project, because the batch window is
adjustable in three independent ways and none of them costs a listener anything:

| Lever | What moves |
|---|---|
| **Start the night earlier** | The Think phase begins before 20:00. Costs nothing but the operator's evening |
| **Finish the render earlier** | Move the render/assemble boundary before 06:30, spending fresh speech-minutes to buy assemble time |
| **Assemble incrementally** | Sign and mix each segment as its render completes rather than in one pass at 06:30. Removes the deadline entirely, at the cost of a more complex batch |

**The reason to measure it in phase A rather than discover it in E** is that the third lever is a
design decision. Building the batch as a pipeline that assembles continuously is cheap before
step 11 exists and is a rewrite afterwards. Twenty minutes of measurement in A decides whether
step 11 needs it.

**If the measured figure exceeds 20 minutes**, reach for the levers in the order above and record
which was taken. Do not shorten the fresh tier to buy assemble time until the first two are spent —
speech is the product and the window is not.

---

## 37. If the hardware improves

Nothing here is a rewrite. In order of value:

| Upgrade | Changes |
|---|---|
| **More RAM (32–48GB)** | A larger writer, and a separate small-model tier for items and canon checks. `config/models.yaml` only |
| **A CUDA box** | `worker_tts.py` runs there against the same Postgres queue over the LAN; reranker moves to GPU; the render window shortens. Config plus one connection string |
| **Both** | The batch window widens or dissolves into continuous generation. **Keep the N+1 buffer regardless** — it is good practice, not a workaround |
| **Any** | Fresh blocks extend toward 18–24 hours as measured RTF allows. The planner already derives this from `config/measured.yaml` |

What never changes: the schema, the seams, the clock contract, the safety gate, the compliance
package, the canon pipeline, the transmitter, the working agreement.

---

## 38. Open decisions

| Decision | The deciding test |
|---|---|
| **The catalogue's shape** | Never stated: §8 gives rotation weights and separation rules but no size. The binding constraint is structure, not count — a label retrospective needs a label with artists and albums behind it (§10). Specify labels × artists × albums × tracks, and let the count fall out. Decide before phase F |
| Writer model | Same brief, same context, candidates write `The Evening Report`. Read blind (§36.2) |
| Chatterbox vs Qwen3-TTS for cast | Same 90-second two-hander through both. Listen |
| Which freshness tier the grid ships at | Falls out of the RTF measurement (§36) against `PROGRAMMING.md` §9 |
| Voice identity when the archive is deep | Bulk re-render vs an in-world host change, forced at step 13b |
| Sign the Code of Practice deployer section | Lawyer, at step 15 |
| Panel screens | Whatever you actually reached for in the first 30 days |
| **Listener telemetry — whether to collect it at all** | Nothing in this document measures listeners, yet `PRODUCT.md` §9 makes **return listening** and **time in stream** two of the five signals that matter. Icecast already emits per-mount connection durations, so the cost is collection and storage, not instrumentation. Decide at step 18 (phase J): collect and keep, or accept that the product thesis is unmeasured and say so |

**Closed since v9:** grid composition (talk : music) — §11 settles it, this is a speech station and
music does not fill gaps; where the fresh hours sit — `PROGRAMMING.md` §8 is the schedule; the
real-person match threshold (D-009); the Saturday chart slot (D-010); whether chart clips score
(D-011); whether the cast engine must watermark (D-019 — it must not be chosen on that); and the
archive pool size versus the separation window (D-021 — the pool is elastic, the window never
moves, and the launch date absorbs the difference).
