"""`make music-analyse` — the ramp and the ending, on signals whose answer is known.

Why synthesised audio rather than a fixture take: the measurement is only worth anything if it
separates *a voice entering* from *the band getting louder*, and no real take can prove that,
because a real take has no ground truth attached (ARCHITECTURE §9: the last half-second is a
listening judgement). A tone that shakes, mixed centre, over tones that do not, mixed wide, has
one. The numbers here are what the pilot's 45 takes measured, not stand-ins for them.

No test decodes a file. `decode()` is one ffmpeg call and §29 does not want a test of it; what
follows this line is the arithmetic.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from station.music import analyse

SR = analyse.SR


def _tones(seconds: float, freqs: tuple[float, ...], spread: bool) -> np.ndarray:
    """Steady partials — a band holding a chord. `spread` pans them away from the centre."""
    t = np.arange(int(seconds * SR)) / SR
    channels = []
    for offset in (0, 1):
        parts = freqs[offset::2] if spread else freqs
        channels.append(sum(np.sin(2 * np.pi * f * t) for f in parts) / max(len(parts), 1))
    return np.array(channels, dtype=np.float32)


def _voice(seconds: float, base: float = 320.0) -> np.ndarray:
    """A tone that shakes — 6 Hz vibrato and its harmonics, dead centre, as a singer is mixed."""
    t = np.arange(int(seconds * SR)) / SR
    wobble = np.cumsum(base * (1 + 0.04 * np.sin(2 * np.pi * 6 * t))) / SR
    one = sum(np.sin(2 * np.pi * k * wobble) / k for k in (1, 2, 3))
    return np.array([one, one], dtype=np.float32)


def _take(intro_s: float, sung_s: float) -> tuple[np.ndarray, np.ndarray]:
    """A record: the band alone, then the band and the singer."""
    band = _tones(intro_s + sung_s, (300.0, 450.0, 700.0, 1100.0), spread=True)
    voice = np.pad(_voice(sung_s), ((0, 0), (int(intro_s * SR), 0)))
    mix = (band + 1.2 * voice[:, : band.shape[1]]).astype(np.float32)
    return mix[0].copy(), mix[1].copy()


def _evidence(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return analyse.curves(left, right).evidence


def test_the_voice_is_what_moves_the_feature() -> None:
    """The band alone and the band with a singer over it are the same loudness, not the same score.

    Asserted in the units the detector actually uses — the opening's depth under the body of the
    song, in the curve's own spread — because that is the number `DEPTH_CLAIM` is compared against.
    """
    left, right = _take(intro_s=10, sung_s=20)
    v = analyse.smooth(_evidence(left, right), analyse.SLOW_S)
    depth, _, _ = analyse._opening_depth(v, start=0)
    assert depth > analyse.DEPTH_CLAIM


@pytest.mark.parametrize("intro", [6.0, 10.0])
def test_the_ramp_lands_within_half_a_second(intro: float) -> None:
    """The half-second in the card's check, against a signal that knows its own answer."""
    left, right = _take(intro_s=intro, sung_s=24)
    ramp, confidence, note = analyse.intro_ramp(_evidence(left, right), start=0)
    assert confidence == "firm", note
    assert abs(ramp - intro) <= 0.5


def test_singing_from_the_top_is_no_ramp_rather_than_a_small_one() -> None:
    """A record with no run-up must not be given one; the mixer would talk over the first word."""
    left, right = _take(intro_s=0, sung_s=30)
    ramp, confidence, _ = analyse.intro_ramp(_evidence(left, right), start=0)
    assert ramp == 0.0
    assert confidence == "firm"


def test_a_rise_that_does_not_hold_is_not_the_vocal() -> None:
    """A sung phrase inside the intro is a hook. The link has to survive it, so the ramp must too."""
    left, right = _take(intro_s=10, sung_s=24)
    fill = np.pad(_voice(1.0), ((0, 0), (int(4 * SR), 0)))
    left[: fill.shape[1]] += 1.2 * fill[0]
    right[: fill.shape[1]] += 1.2 * fill[1]
    ramp, confidence, note = analyse.intro_ramp(_evidence(left, right), start=0)
    assert confidence == "firm", note
    assert abs(ramp - 10.0) <= 0.5


def _ending(shape: str) -> tuple[np.ndarray, np.ndarray]:
    """A song of the same body, ended three ways."""
    left, right = _take(intro_s=2, sung_s=26)
    tail = int(4 * SR)
    if shape == "cold":
        return left.copy(), right.copy()  # the file simply stops at full level
    ramp = np.linspace(1.0, 0.0, tail, dtype=np.float32)
    if shape == "fade":  # the band plays on under the fader
        left[-tail:] *= ramp
        right[-tail:] *= ramp
        return left, right
    band = _tones(2 + 26, (300.0, 450.0, 700.0, 1100.0), spread=True)  # a chord left to ring
    left[-tail:] = band[0, -tail:] * ramp
    right[-tail:] = band[1, -tail:] * ramp
    return left, right


@pytest.mark.parametrize("shape", ["cold", "fade", "sustain"])
def test_the_ending_is_named_for_what_it_does(shape: str) -> None:
    left, right = _ending(shape)
    kind, _ = analyse._outro(left, right, analyse.curves(left, right).onset)
    assert kind == shape


def test_a_file_that_cannot_be_read_is_reported_not_skipped() -> None:
    """§25's unbreakable rule: a song that dropped out silently becomes a link over a vocal."""
    measured, failed = analyse.measure_all([Path("music/audio/does-not-exist.mp3")])
    assert measured == []
    assert len(failed) == 1


def test_only_audio_is_walked(tmp_path: Path) -> None:
    (tmp_path / "al_001").mkdir()
    (tmp_path / "al_001" / "01.mp3").write_bytes(b"")
    (tmp_path / "al_001" / "notes.md").write_text("not audio")
    (tmp_path / "dispatch-manifest.json").write_text("{}")
    assert [p.name for p in analyse.audio_files(tmp_path)] == ["01.mp3"]
