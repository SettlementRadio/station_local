"""The three numbers a mixer needs from a finished take, measured rather than estimated.

`intro_ramp_sec` is how long the mixer may keep talking over the top of a record; `outro_type`
says whether it may talk over the end at all (ARCHITECTURE §9); `duration_sec` is what the
back-timer plans with. Five hundred songs is far too many to hand-time, and a wrong ramp is
audible — the link clips the first sung word.

**What this file claims, and what it does not.** ARCHITECTURE §9 is explicit that onset detection
gets the ballpark and that the last half-second is a listening judgement. So every measurement
carries a confidence: `firm` where the evidence is unambiguous, `check` where it is not, with the
reason attached. The operator re-listens to the flagged ones and to nothing else. A tool that
printed 500 confident numbers, some of them wrong, would be worse than no tool.

**A ramp of `0.0` means "no run-up you can talk over", not "the vocal is at sample zero".** Nothing
here resolves an intro shorter than about two seconds, and nothing needs to: two seconds is not a
link. A ramp is only ever *claimed* when the opening of the record is measurably quieter in vocal
evidence than the body of it, which is the only case where the mixer has room to work with.

**How the vocal is found.** Not by loudness — the band is usually already playing when the singer
comes in, so the mixture barely changes level. Two things do change. A sung note *moves*: its
partials glide and shake where a keyboard's or a guitar's sit still, so the energy-weighted rate of
change of instantaneous frequency (from the phase vocoder's own phase advance) steps up when a
voice enters. And the voice is mixed dead centre, so weighting that measure by how equal the two
channels are at each bin discards most of what the panned instruments contribute. The two together
separate the intro from the first verse by about two robust standard deviations on the pilot; a
harmonic/percussive median filter was tried on top and made the separation *worse* while costing
five times the runtime, so it is not here (D-083).

Everything is numpy over ffmpeg's decoded samples. librosa would supply the spectrogram and an
onset detector, but not this feature — and §22 asks a dependency to save more than ~200 lines,
which the dozen lines of framed FFT below do not.

`stft`, `smooth`, `audio_start` and `intro_ramp` are public because `imaging/analyse.py` measures
the same run-up on the same evidence (§9: imaging earns its fields the same way music does). There
is one ramp measure in this repository and this is it.
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

from station import log

SR = 22050  # analysis rate; the vocal band is well under Nyquist and it halves the work
N_FFT = 2048  # 93 ms — long enough to resolve partials, short enough to see a word start
HOP = 512  # 23 ms per frame, so a ±0.5 s judgement has ~20 frames of margin
FRAME_RATE = SR / HOP
BAND = (250.0, 3500.0)  # where a sung voice puts its formants; below it is bass and kick
DECODE_TIMEOUT_S = 180  # §25: every external call has an explicit timeout
AUDIO_SUFFIXES = frozenset({".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus"})

SLOW_S = 2.0  # the window that decides *whether* there is an intro
FAST_S = 0.35  # the window that decides *where* it ends
OPENING_S = (1.0, 4.0)  # the opening, measured past the first downbeat's transient
DEPTH_CLAIM = 1.8  # how far under the body of the song the opening must sit to be an intro
DEPTH_QUIET = 1.0  # under this the opening is the song's normal level: no ramp, and sure of it
MIN_VOCAL_RUN_S, RUN_SHARE = 1.5, 0.9  # a rise held this long is a singer, not a fill
STICK_S, STICK_SHARE = 15.0, 0.7  # and it has to stay up, or it was a fill after all
MAX_RAMP_S = 30.0  # past this it is a middle-eight, not an introduction
COLD_FALL_S = 0.6  # -3 dB to -20 dB faster than this and the record simply stops
BORDER = (0.5, 0.7)  # either side of it, and which side is a listening judgement
FADE_ONSET_SHARE = 0.85  # attacks through the decay at this share of the song's rate: a fade

logger = log.get_logger(job="music-analyse")


class AnalyseError(RuntimeError):
    """A file could not be measured. §25: it is reported, never silently skipped."""


class Measurement(BaseModel):
    """One audio file, measured. The three numbers, and how far to trust two of them."""

    path: str
    duration_sec: float
    intro_ramp_sec: float
    outro_type: str  # cold | fade | sustain
    confidence: str  # firm | check
    note: str = ""  # why it is flagged, empty when firm

    @property
    def flagged(self) -> bool:
        return self.confidence != "firm"


# --- decoding and the spectrogram ---------------------------------------------------------------


def decode(path: Path) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """The file as two channels of float samples at `SR`, through ffmpeg.

    Stereo, not mono: the centre-channel weighting below is the whole reason the vocal is findable,
    and a downmix throws it away. A mono source decodes to two identical channels, which weights
    every bin as centre — correct, just less selective.
    """
    command = [
        "ffmpeg", "-v", "error", "-i", str(path),
        "-f", "f32le", "-ac", "2", "-ar", str(SR), "-",
    ]  # fmt: skip
    try:
        result = subprocess.run(command, capture_output=True, timeout=DECODE_TIMEOUT_S, check=False)
    except subprocess.TimeoutExpired:
        raise AnalyseError(f"{path}: ffmpeg did not finish inside {DECODE_TIMEOUT_S}s") from None
    except FileNotFoundError:
        raise AnalyseError("ffmpeg is not installed — `make setup`, then `make doctor`") from None
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
        raise AnalyseError(f"{path}: ffmpeg failed — {detail[-1] if detail else 'no output'}")
    samples = np.frombuffer(result.stdout, dtype=np.float32)
    if samples.size < 2 * N_FFT:
        raise AnalyseError(f"{path}: decoded to {samples.size // 2} samples, too short to measure")
    frames = samples.reshape(-1, 2)
    return frames[:, 0].copy(), frames[:, 1].copy()


def stft(y: NDArray[np.float32]) -> NDArray[np.complex64]:
    """Framed rfft. Complex, because the phase is the feature."""
    window = np.hanning(N_FFT).astype(np.float32)
    count = 1 + (len(y) - N_FFT) // HOP
    index = np.arange(N_FFT)[None, :] + HOP * np.arange(count)[:, None]
    return np.fft.rfft(y[index] * window, axis=1).astype(np.complex64)


def smooth(x: NDArray[np.float64], seconds: float) -> NDArray[np.float64]:
    """Centred moving average, edge-padded so the first and last frames stay usable."""
    width = max(1, int(seconds * FRAME_RATE))
    pad = width // 2
    padded = np.pad(x, pad, mode="edge")
    return np.convolve(padded, np.ones(width) / width, mode="same")[pad : pad + len(x)]


def _robust_z(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Standardise against the median and MAD — a chorus is an outlier and should not set the scale."""
    median = float(np.median(x))
    mad = float(np.median(np.abs(x - median))) + 1e-9
    return (x - median) / (1.4826 * mad)


# --- the features -------------------------------------------------------------------------------


class Curves(NamedTuple):
    """The two per-frame curves everything below is read off, from one pass of the spectrogram."""

    evidence: NDArray[np.float64]  # how voice-like the frame is, standardised (see `curves`)
    onset: NDArray[np.float64]  # how much of the frame is a fresh attack rather than a held note


def curves(left: NDArray[np.float32], right: NDArray[np.float32]) -> Curves:
    """Per frame, how much the sound behaves like a voice rather than like the band.

    The rate of change of instantaneous frequency, weighted by how equal the two channels are at
    each bin and by that bin's energy, over **all** the energy in the band. Dividing by the centred
    energy instead was the first attempt and is wrong: a passage with nothing in the middle of the
    mix then divides a little leakage by a little leakage and reports a voice where there is none.
    Over the whole band, "nothing centred is moving" comes out low, which is what it means.

    Returned standardised, so a number is "robust standard deviations from this song's own middle".
    """
    length = min(len(left), len(right))
    cl, cr = stft(left[:length]), stft(right[:length])
    centre = np.clip(1.0 - np.abs(cl - cr) / (np.abs(cl) + np.abs(cr) + 1e-9), 0.0, 1.0)
    spectrum = np.abs((cl + cr) / 2)

    freqs = np.fft.rfftfreq(N_FFT, 1 / SR)
    band = (freqs >= BAND[0]) & (freqs <= BAND[1])
    expected = 2 * np.pi * HOP * freqs[None, :] / SR
    advance = np.angle(np.exp(1j * (np.diff(np.angle(cl + cr), axis=0) - expected)))
    instantaneous = freqs[None, :] + advance * SR / (2 * np.pi * HOP)
    movement = np.abs(np.diff(instantaneous, axis=0))

    weight = (spectrum * centre)[2:, band]
    energy = spectrum[2:, band].sum(axis=1)
    evidence = (movement[:, band] * weight).sum(axis=1) / (energy + 1e-9)

    # The second curve, off the same spectrogram: what share of the frame is a new attack. It is
    # what tells a fade — a band still playing while the fader comes down — from a chord ringing.
    flux = np.maximum(0, np.diff(spectrum, axis=0)).sum(axis=1) / (spectrum[1:].sum(axis=1) + 1e-9)
    return Curves(
        evidence=_robust_z(np.concatenate([evidence[:1], evidence[:1], evidence])),
        onset=np.concatenate([flux[:1], flux]),
    )


def frame_energy(left: NDArray[np.float32], right: NDArray[np.float32]) -> NDArray[np.float64]:
    """Loudness per analysis frame — used only to find where the audio actually starts."""
    length = min(len(left), len(right)) // HOP * HOP
    mono = ((left[:length] + right[:length]) / 2).reshape(-1, HOP)
    return np.sqrt((mono.astype(np.float64) ** 2).mean(axis=1))


def _opening_depth(slow: NDArray[np.float64], start: int) -> tuple[float, float, float]:
    """How far the opening sits under the body of the song, in the curve's own spread.

    The comparison is against the body rather than against a threshold because nothing about this
    feature is comparable between songs: a busy arrangement raises the whole curve. What is
    comparable is "the opening of this record is two of its own standard deviations quieter in
    vocal evidence than the middle of it", and that is a sentence about an instrumental intro.
    """
    spread = float(np.std(slow)) + 1e-9
    head = slice(start + int(OPENING_S[0] * FRAME_RATE), start + int(OPENING_S[1] * FRAME_RATE))
    opening = float(np.mean(slow[head])) if slow[head].size else 0.0
    body = float(np.mean(slow[int(0.3 * len(slow)) : int(0.8 * len(slow))]))
    return (body - opening) / spread, opening, body


# --- the three numbers --------------------------------------------------------------------------


def audio_start(energy: NDArray[np.float64]) -> int:
    """First frame carrying sound, so a file with a second of digital black is not penalised."""
    floor = float(np.percentile(energy, 90)) * 10 ** (-40 / 20)
    return int(np.argmax(energy > floor))


def intro_ramp(v: NDArray[np.float64], start: int) -> tuple[float, str, str]:
    """Seconds from the first sound to the first sung word, with a confidence and a reason.

    A ramp is *claimed* only when the opening is clearly quieter in vocal evidence than the song
    and the rise out of it holds. Otherwise the answer is zero — the singer is in from the top —
    and the flag says whether that is a finding or a shrug.
    """
    slow, fast = smooth(v, SLOW_S), smooth(v, FAST_S)
    depth, opening, body = _opening_depth(slow, start)
    if depth < DEPTH_CLAIM:
        if depth < DEPTH_QUIET:
            return 0.0, "firm", ""
        return 0.0, "check", f"opening only {depth:.1f} under the song — no ramp claimed"

    middle = (opening + body) / 2
    run, stick = int(MIN_VOCAL_RUN_S * FRAME_RATE), int(STICK_S * FRAME_RATE)
    horizon = int(min(len(slow) - run, start + MAX_RAMP_S * FRAME_RATE, 0.5 * len(slow)))
    for i in range(start + int(FRAME_RATE), max(horizon, start + 2)):
        if (slow[i : i + run] > middle).mean() <= RUN_SHARE:
            continue
        if (slow[i : i + stick] > middle).mean() < STICK_SHARE:
            continue
        edge = i
        limit = max(start, i - int(3 * FRAME_RATE))
        while edge > limit and fast[edge] > middle:
            edge -= 1
        return edge / FRAME_RATE, "firm", ""  # from the top of the file: the mixer's clock
    return 0.0, "check", f"opening {depth:.1f} under the song but the rise never held"


def _outro(
    left: NDArray[np.float32], right: NDArray[np.float32], onset: NDArray[np.float64]
) -> tuple[str, str]:
    """How the record ends: `cold` stops dead, `sustain` rings out, `fade` is pulled down.

    Measured as the time the level takes to fall from 3 dB to 20 dB under the body of the song,
    and — for the two slow endings — whether anything is still being played while it falls.
    """
    envelope, rate = _envelope(left, right)
    end = _last_live_frame(envelope)
    body = float(np.median(envelope[int(0.2 * end) : int(0.8 * end)])) + 1e-12
    tail = envelope[:end] / body

    top = _last_at_or_above(tail, 10 ** (-3 / 20))
    bottom = _last_at_or_above(tail, 10 ** (-20 / 20))
    fall = max(0.0, (bottom - top) / rate)
    note = (
        f"ends on the line between cold and a ring ({fall:.2f}s)"
        if BORDER[0] <= fall <= BORDER[1]
        else ""
    )
    if fall <= COLD_FALL_S:
        return "cold", note

    during = onset[int(top / rate * FRAME_RATE) : int(end / rate * FRAME_RATE)]
    played_on = float(np.mean(during)) / (float(np.median(onset)) + 1e-9) if during.size else 0.0
    return ("fade" if played_on >= FADE_ONSET_SHARE else "sustain"), note


def _envelope(
    left: NDArray[np.float32], right: NDArray[np.float32]
) -> tuple[NDArray[np.float64], float]:
    """A 20 ms loudness envelope, smoothed just past a snare hit so a backbeat is not an ending."""
    step = int(0.02 * SR)
    length = min(len(left), len(right)) // step * step
    mono = ((left[:length] + right[:length]) / 2).reshape(-1, step)
    raw = np.sqrt((mono.astype(np.float64) ** 2).mean(axis=1))
    rate = SR / step
    width = max(1, int(0.12 * rate))
    return np.convolve(np.pad(raw, width // 2, mode="edge"), np.ones(width) / width, mode="same")[
        width // 2 : width // 2 + len(raw)
    ], rate


def _last_live_frame(envelope: NDArray[np.float64]) -> int:
    """Where the audio really ends, ignoring the encoder's trailing silence."""
    floor = float(envelope.max()) * 10 ** (-50 / 20)
    live = envelope > floor
    return len(envelope) - int(np.argmax(live[::-1])) if live.any() else len(envelope)


def _last_at_or_above(tail: NDArray[np.float64], level: float) -> int:
    """Index of the last frame at or above `level`, searching back from the end."""
    hits = tail >= level
    return len(tail) - int(np.argmax(hits[::-1])) - 1 if hits.any() else 0


def measure(path: Path) -> Measurement:
    """One file: duration, intro ramp, outro type, and how far to trust the last two."""
    left, right = decode(path)
    duration = min(len(left), len(right)) / SR
    measured = curves(left, right)
    start = audio_start(frame_energy(left, right))

    ramp, confidence, note = intro_ramp(measured.evidence, start)
    outro, outro_note = _outro(left, right, measured.onset)
    if outro_note:
        confidence, note = "check", "; ".join(x for x in (note, outro_note) if x)
    logger.debug(
        "measured", path=str(path), duration_sec=round(duration, 2), ramp_sec=round(ramp, 2)
    )
    return Measurement(
        path=str(path),
        duration_sec=round(duration, 2),
        intro_ramp_sec=round(ramp, 2),
        outro_type=outro,
        confidence=confidence,
        note=note,
    )


# --- walking the tree ---------------------------------------------------------------------------


def audio_files(root: Path) -> list[Path]:
    """Every audio file under `root`, in path order. Anything else in the tree is ignored."""
    return sorted(p for p in root.rglob("*") if p.suffix.lower() in AUDIO_SUFFIXES and p.is_file())


def measure_all(paths: Iterable[Path]) -> tuple[list[Measurement], list[str]]:
    """Measure each file, keeping going past one that cannot be read (§25's ffprobe rule).

    Returns what was measured and what failed. The caller reports both; a file that dropped out
    silently would become a track with no ramp and a link that clips the vocal.
    """
    measured, failed = [], []
    for path in paths:
        try:
            measured.append(measure(path))
        except AnalyseError as exc:
            logger.error("unmeasurable", path=str(path), error=str(exc))
            failed.append(str(exc))
    return measured, failed
