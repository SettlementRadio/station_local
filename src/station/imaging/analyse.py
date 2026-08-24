"""The four numbers §9 asks of a piece of imaging, measured rather than hand-timed.

`duration_sec` the back-timer plans with; `intro_ramp_sec` is the run-up before the first sound a
presenter cannot talk over; `energy` is what a daypart's range is compared against (§17a); and
`bed_loop_sec` is the point a bed returns to when it loops. A hundred-odd pieces is too many to
time by ear, and §9 says imaging earns these fields exactly the way music does — a measurement
pass, then correction by ear on the ones that need it.

**The ramp is `music/analyse.py`'s, not a second one.** Where a piece sings — and one in this pile
does, and every future open quoting the sung station name will — the post is the first sung word,
and that measurement already exists (D-083). It runs first and its answer wins.

**But most imaging is instrumental, and for an instrumental the post is a different event.** There
is no vocal to enter, so the vocal measure correctly reports nothing, and a tool that printed
`0.0` for fifty-six files would be measuring none of them. What a presenter cannot talk over in an
instrumental piece is its body: the swell, riser or single held note some of these open with is
exactly the run-up the mixer is allowed. So the fallback is a level measure — how long the piece
takes to reach and hold its own body level — and it is only ever *claimed* where the opening is
measurably quieter than that body, on D-083's rule that nothing unmeasured gets claimed.

**`energy` is brightness, and that is not a compromise on this palette.** README §2's three tiers
are a brightness ladder by construction: Night is felt piano and low pads, Day is mallets and
arpeggios, Bright is pulses, claps and sweeps. Onset density and rhythmic modulation were both
measured across the 56 first and neither separated a night piece from a bright one — every piece
in the brand is slow-to-mid by rule, so tempo carries almost no information here while the
spectral centroid orders the pile the way the tiers do (D-094). One number, on a stated scale.

**`bed_loop_sec` is a seam, not an onset, and it is the one genuinely new measurement.** A loop
sounds right when the material before the end of the file is the same phase of the pattern as the
material before the point it jumps back to — so the return point is found by matching the window
that precedes the end against every earlier window, and then checked: the join has to step no
further than the piece steps of its own accord frame to frame. Both have to hold before a number
is printed, because a loop point that is merely plausible is worse than none.

numpy over ffmpeg's samples, as in music. D-083 left the librosa question to this card and D-094
closes it: nothing above is beat tracking or key detection, which were the two things librosa
would have brought.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

from station import log
from station.music.analyse import (
    FRAME_RATE,
    N_FFT,
    SR,
    AnalyseError,
    audio_files,
    audio_start,
    curves,
    decode,
    frame_energy,
    intro_ramp,
    smooth,
    stft,
)

# Re-exported deliberately: the shared primitives are `music/analyse.py`'s, and a caller of this
# module should never have to reach across to the music one to use them.
__all__ = [
    "SR",
    "AnalyseError",
    "Measurement",
    "audio_files",
    "frame_energy",
    "measure",
    "measure_all",
]

BANDS = 40  # log-spaced, coarse enough that a note bending inside one is not a new frame
BAND_FLOOR_HZ = 60.0  # under it is rumble and the DC bin, and neither identifies a moment
LIVE_DB = -50.0  # under the loudest frame: where the audio really ends, past the encoder's tail

DARK_HZ, BRIGHT_HZ = 250.0, 5000.0  # the ends of the energy scale, log-spaced between them

LEAD_SMOOTH_S = 0.15  # a swell is a shape, not a sample; smoothed past a single mallet hit
LEAD_REACH_DB, LEAD_HOLD_DB = -3.0, -6.0  # reach the body, then stay there
LEAD_HOLD_S = 1.0  # for this long, or it was a hit in the intro rather than the body
LEAD_HOLD_SHARE = 0.9  # of that window, so one dip inside a phrase does not restart the search
LEAD_QUIET, LEAD_AMBIGUOUS = 0.5, 0.8  # opening against body: under, a lead-in; over, no ramp
LEAD_MIN_S = 0.3  # shorter than this is an attack envelope, not a run-up
MAX_LEAD_S = 30.0  # past this the piece has changed section, not finished starting

SEAM_S = 3.0  # the window either side of the join that has to be the same phase of the pattern
MIN_LOOP_S = 6.0  # a shorter return is a stutter, whatever it measures
LOOP_CLAIM = 0.60  # correlation under this and nothing in the piece repeats its ending
SEAM_CLEAN = 3.0  # the join may step this many times the piece's own median frame-to-frame step

logger = log.get_logger(job="imaging-analyse")


class Measurement(BaseModel):
    """One piece of imaging, measured, and how far to trust it."""

    path: str
    duration_sec: float
    intro_ramp_sec: float
    energy: float  # 0 to 1, comparable with §17a's daypart ranges
    bed_loop_sec: float | None  # None where nothing in the piece repeats its ending
    confidence: str  # firm | check
    note: str = ""  # what the row wants you to know; empty when there is nothing

    @property
    def flagged(self) -> bool:
        return self.confidence != "firm"


# --- the spectrogram, once, in the two shapes the numbers below need --------------------------


def spectra(
    left: NDArray[np.float32], right: NDArray[np.float32]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """The mono magnitude spectrogram's centroid per frame, and its collapse into log bands.

    Two different questions want two different resolutions. Brightness wants every bin, because the
    centroid of a coarse band average is the centroid of the band edges. The loop seam wants the
    coarse version: forty bands is enough to say which moment of the pattern a frame is, and
    little enough that a note bending or a tape wobble does not make it a different moment.
    """
    length = min(len(left), len(right))
    spectrum = np.abs(stft(((left[:length] + right[:length]) / 2).astype(np.float32))).astype(
        np.float64
    )
    freqs = np.fft.rfftfreq(N_FFT, 1 / SR)
    centroid = (spectrum * freqs).sum(axis=1) / (spectrum.sum(axis=1) + 1e-12)

    edges = np.searchsorted(freqs, np.geomspace(BAND_FLOOR_HZ, freqs[-1], BANDS + 1))
    bands = np.stack(
        [spectrum[:, edges[i] : max(edges[i + 1], edges[i] + 1)].sum(axis=1) for i in range(BANDS)],
        axis=1,
    )
    return centroid, bands


def live_end(energy: NDArray[np.float64]) -> int:
    """The frame the audio really stops at, ignoring whatever silence the encoder left on."""
    floor = float(energy.max()) * 10 ** (LIVE_DB / 20)
    live = energy > floor
    return len(energy) - int(np.argmax(live[::-1])) if live.any() else len(energy)


# --- energy ------------------------------------------------------------------------------------


def energy_level(centroid: NDArray[np.float64], energy: NDArray[np.float64]) -> float:
    """Where the piece sits on the palette's own ladder, 0 at 250 Hz and 1 at 5 kHz.

    Log-spaced, because a tier is a musical distance rather than a number of hertz: the step from
    the night tier's felt piano to the day tier's mallets is about the same interval as the step
    from the mallets to a sweeper, and only a log scale says so. Measured over the frames that
    carry sound, so a long tail does not drag a bright piece down.
    """
    length = min(len(centroid), len(energy))
    live = energy[:length] > float(energy.max()) * 10 ** (-30 / 20)
    heard = centroid[:length][live] if live.any() else centroid[:length]
    mean = float(np.mean(np.log2(np.maximum(heard, 1.0))))
    scale = (mean - np.log2(DARK_HZ)) / (np.log2(BRIGHT_HZ) - np.log2(DARK_HZ))
    return round(float(np.clip(scale, 0.0, 1.0)), 2)


# --- the run-up --------------------------------------------------------------------------------


def lead_in(energy: NDArray[np.float64]) -> tuple[float, str, str]:
    """Seconds before an instrumental piece reaches and holds its own body level.

    The claim is the same shape as D-083's: the opening has to be measurably under the body before
    any run-up is reported, and where it is only a little under, the number is a judgement and
    says so. A piece that starts at full level reads `0.0` — there is nothing to talk over.
    """
    level = smooth(energy, LEAD_SMOOTH_S)
    floor = float(np.percentile(level, 90)) * 10 ** (-40 / 20)
    start = int(np.argmax(level > floor))
    live = level > floor
    body = float(np.median(level[live])) if live.any() else 0.0
    if body <= 0:
        return 0.0, "check", "no sustained level to measure a run-up against"

    opening = float(np.mean(level[start : start + int(0.5 * FRAME_RATE)])) / body
    if opening >= LEAD_AMBIGUOUS:
        return 0.0, "firm", ""

    held = int(LEAD_HOLD_S * FRAME_RATE)
    horizon = int(min(len(level) * 0.5, start + MAX_LEAD_S * FRAME_RATE))
    for i in range(start, max(horizon, start + 1)):
        if level[i] < body * 10 ** (LEAD_REACH_DB / 20):
            continue
        if (level[i : i + held] >= body * 10 ** (LEAD_HOLD_DB / 20)).mean() <= LEAD_HOLD_SHARE:
            continue
        ramp = (i - start) / FRAME_RATE
        if ramp < LEAD_MIN_S:
            return 0.0, "firm", ""
        if opening >= LEAD_QUIET:
            under = -20 * float(np.log10(opening))
            return ramp, "check", f"the opening is only {under:.0f} dB under the body of the piece"
        return ramp, "firm", ""
    return 0.0, "check", "the piece opens quietly and never settles at a body level"


def run_up(
    left: NDArray[np.float32], right: NDArray[np.float32], energy: NDArray[np.float64]
) -> tuple[float, str, str]:
    """The run-up, from the sung entry where there is one and from the level where there is not."""
    ramp, confidence, note = intro_ramp(curves(left, right).evidence, audio_start(energy))
    if ramp > 0:
        return ramp, confidence, "; ".join(x for x in (note, "sung entry") if x)
    return lead_in(energy)


# --- the loop seam -----------------------------------------------------------------------------


def _shapes(
    bands: NDArray[np.float64], end: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Two views of the same frames: one carrying level, one carrying only what is distinctive.

    The seam is judged on the first — a join into a quieter passage is audible however well the
    pattern lines up. Which moment of the pattern a frame *is* has to be judged on the second, or
    every frame of a warm pad correlates with every other at 0.99 and the measure says nothing.
    """
    level = np.log1p(bands[:end] * 1e3)
    shape = level - level.mean(axis=0, keepdims=True)
    shape = shape - shape.mean(axis=1, keepdims=True)
    return level, shape / (np.linalg.norm(shape, axis=1, keepdims=True) + 1e-9)


def loop_point(
    bands: NDArray[np.float64], energy: NDArray[np.float64]
) -> tuple[float | None, str, str]:
    """Where a bed should jump back to, or `None` where nothing in the piece repeats its ending."""
    end = live_end(energy[: len(bands)])
    window, shortest = int(SEAM_S * FRAME_RATE), int(MIN_LOOP_S * FRAME_RATE)
    if end < 2 * window + shortest:
        return None, "firm", ""

    level, shape = _shapes(bands, end)
    tail = shape[end - window :]
    scores = np.zeros(end - shortest - window)
    for band in range(shape.shape[1]):
        scores += np.correlate(shape[:, band], tail[:, band], mode="valid")[: len(scores)]
    scores /= window

    match = float(scores.max())
    point = int(np.argmax(scores)) + window
    if match < LOOP_CLAIM:
        return None, "firm", ""

    steps = np.linalg.norm(np.diff(level, axis=0), axis=1)
    jump = float(np.linalg.norm(level[point] - level[end - 1])) / (float(np.median(steps)) + 1e-9)
    seconds = round(point / FRAME_RATE, 2)
    if jump > SEAM_CLEAN:
        return seconds, "check", f"the pattern repeats here but the join steps {jump:.1f}x"
    return seconds, "firm", ""


# --- one file ----------------------------------------------------------------------------------


def measure(path: Path) -> Measurement:
    """One piece: length, run-up, energy, loop seam, and how far to trust the last three."""
    left, right = decode(path)
    duration = min(len(left), len(right)) / SR
    energy = frame_energy(left, right)
    centroid, bands = spectra(left, right)

    ramp, confidence, note = run_up(left, right, energy)
    loop, loop_confidence, loop_note = loop_point(bands, energy)
    notes = [x for x in (note, loop_note) if x]
    if loop_confidence != "firm":
        confidence = "check"
    logger.debug(
        "measured", path=str(path), duration_sec=round(duration, 2), ramp_sec=round(ramp, 2)
    )
    return Measurement(
        path=str(path),
        duration_sec=round(duration, 2),
        intro_ramp_sec=round(ramp, 2),
        energy=energy_level(centroid, energy),
        bed_loop_sec=loop,
        confidence=confidence,
        note="; ".join(notes),
    )


def measure_all(paths: Iterable[Path]) -> tuple[list[Measurement], list[str]]:
    """Measure each piece, keeping going past one that cannot be read (§25's ffprobe rule).

    Returns what was measured and what failed, because a piece that dropped out silently becomes a
    catalogue row with no numbers in it, and §17a's checks cannot tell that from a piece with none.
    """
    measured, failed = [], []
    for path in paths:
        try:
            measured.append(measure(path))
        except AnalyseError as exc:
            logger.error("unmeasurable", path=str(path), error=str(exc))
            failed.append(str(exc))
    return measured, failed
