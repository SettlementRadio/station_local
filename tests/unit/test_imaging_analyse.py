"""`make imaging-analyse` — the run-up, the energy and the loop seam, on signals with a known answer.

Synthesised rather than fixture audio, for the reason `test_music_analyse.py` gives: a real take
carries no ground truth, and the whole claim of the loop measure is that it separates a piece that
repeats its own ending from one that merely sounds similar to itself throughout. A pattern built
twice from the same samples has an answer; the fallback bed does not, whatever it sounds like.

No test decodes a file. What follows is the arithmetic.
"""

from __future__ import annotations

import numpy as np

from station.imaging import analyse

SR = analyse.SR


def _tone(seconds: float, freq: float, level: float = 1.0) -> np.ndarray:
    t = np.arange(int(seconds * SR)) / SR
    return (level * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def _stereo(mono: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return mono.copy(), mono.copy()


def _energy_of(mono: np.ndarray) -> np.ndarray:
    return analyse.frame_energy(*_stereo(mono))


def _band(seconds: float, freqs: tuple[float, ...]) -> tuple[np.ndarray, np.ndarray]:
    """Steady partials panned away from the centre — the arrangement, with the middle left empty."""
    t = np.arange(int(seconds * SR)) / SR
    channels = [
        np.sum([np.sin(2 * np.pi * f * t) for f in freqs[offset::2]], axis=0) / 2
        for offset in (0, 1)
    ]
    return channels[0], channels[1]


def _flat(channel: np.ndarray) -> np.ndarray:
    """One channel at a level that never moves, so only the voice measure has anything to find."""
    width = 2048
    envelope = np.sqrt(np.convolve(channel**2, np.ones(width) / width, mode="same")) + 1e-9
    return (channel / envelope * 0.2).astype(np.float32)


def _cell(seconds: float, seed: int) -> np.ndarray:
    """A few seconds of a fixed arrangement — several partials, one particular mix of them."""
    rng = np.random.default_rng(seed)
    freqs = rng.uniform(200, 3000, 6)
    weights = rng.uniform(0.3, 1.0, 6)
    parts = [_tone(seconds, f, w) for f, w in zip(freqs, weights, strict=True)]
    return np.sum(parts, axis=0) / 6


# --- the run-up ---------------------------------------------------------------------------------


def test_a_quiet_opening_is_a_run_up_and_is_measured_to_where_the_body_lands() -> None:
    """Two seconds at -20 dB, then the piece proper. That is exactly what a swell into a motif is."""
    piece = np.concatenate([_cell(2.0, 1) * 0.1, _cell(8.0, 1)])
    ramp, confidence, _ = analyse.lead_in(_energy_of(piece))
    assert 1.6 < ramp < 2.4
    assert confidence == "firm"


def test_a_piece_at_full_level_from_the_top_has_nothing_to_talk_over() -> None:
    ramp, confidence, note = analyse.lead_in(_energy_of(_cell(10.0, 2)))
    assert (ramp, confidence, note) == (0.0, "firm", "")


def test_an_opening_only_a_little_under_the_body_is_a_judgement_and_says_so() -> None:
    """-4 dB is inside `LEAD_QUIET`: the number is reported, and it is reported as unsure."""
    piece = np.concatenate([_cell(2.0, 3) * 0.63, _cell(8.0, 3)])
    ramp, confidence, note = analyse.lead_in(_energy_of(piece))
    assert ramp > 0
    assert confidence == "check"
    assert "under the body" in note


def test_where_a_piece_sings_the_sung_entry_is_the_post_and_the_level_measure_does_not_get_a_vote() -> (
    None
):
    """The station name arrives at 8s at no change in level — only the voice measure can find it."""
    band = _band(24.0, (300.0, 450.0, 700.0, 1100.0))
    t = np.arange(int(24.0 * SR)) / SR
    wobble = np.cumsum(320 * (1 + 0.04 * np.sin(2 * np.pi * 6 * t))) / SR
    voice = np.sum([np.sin(2 * np.pi * k * wobble) / k for k in (1, 2, 3)], axis=0)
    voice[: int(8.0 * SR)] = 0.0
    left, right = (_flat(c + 1.2 * voice) for c in band)

    ramp, _, note = analyse.run_up(left, right, analyse.frame_energy(left, right))
    assert 7.0 < ramp < 9.0
    assert "sung entry" in note


# --- the loop seam ------------------------------------------------------------------------------


def test_the_return_point_is_the_start_of_the_repeat_not_the_start_of_the_file() -> None:
    """An intro that happens once, then the same eight seconds twice. The loop returns to the second."""
    cell = _cell(8.0, 4)
    piece = np.concatenate([_cell(8.0, 5), cell, cell])
    point, confidence, _ = analyse.loop_point(*_measurable(piece))
    assert point is not None
    assert abs(point - 16.0) < 0.5
    assert confidence == "firm"


def test_a_piece_that_never_repeats_its_ending_gets_no_loop_point() -> None:
    """A slow sweep is self-similar everywhere and identical nowhere — the case a threshold is for."""
    t = np.arange(int(30.0 * SR)) / SR
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 60 * t) / SR).astype(np.float32)
    point, confidence, _ = analyse.loop_point(*_measurable(sweep))
    assert point is None
    assert confidence == "firm"


def test_a_piece_too_short_to_loop_is_not_asked_to() -> None:
    assert analyse.loop_point(*_measurable(_cell(6.0, 6))) == (None, "firm", "")


def _measurable(mono: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    left, right = _stereo(mono)
    _, bands = analyse.spectra(left, right)
    return bands, analyse.frame_energy(left, right)


# --- energy -------------------------------------------------------------------------------------


def test_energy_puts_the_night_tier_under_the_bright_one() -> None:
    """§2's tiers are a brightness ladder, and the scale has to agree with them or it is not one."""
    felt_piano = analyse.energy_level(*_energy_inputs(_tone(6.0, 300)))
    sweeper = analyse.energy_level(*_energy_inputs(_tone(6.0, 4000)))
    assert felt_piano < 0.35
    assert sweeper > 0.75
    assert all(0.0 <= v <= 1.0 for v in (felt_piano, sweeper))


def test_energy_ignores_the_silence_a_piece_ends_in() -> None:
    """A tail of digital black is not a dark piece; it is no piece at all."""
    bright = _tone(6.0, 4000)
    padded = np.concatenate([bright, np.zeros(int(6.0 * SR), dtype=np.float32)])
    assert (
        abs(
            analyse.energy_level(*_energy_inputs(bright))
            - analyse.energy_level(*_energy_inputs(padded))
        )
        < 0.05
    )


def _energy_inputs(mono: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    left, right = _stereo(mono)
    centroid, _ = analyse.spectra(left, right)
    return centroid, analyse.frame_energy(left, right)
