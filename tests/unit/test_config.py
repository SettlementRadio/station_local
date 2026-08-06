"""The one behaviour of §23 with a consequence: a missing line stops the process and names itself.

§29 says not to test config plumbing, and this is not plumbing — it is the mechanism that turns a
02:00 failure into a startup failure. Nothing else here tests configuration.
"""

from __future__ import annotations

import pytest

from station.config import ConfigError, load_settings

REQUIRED = ("DATABASE_URL", "MEDIA_ROOT")


def test_missing_required_lines_are_named(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in REQUIRED:
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ConfigError) as caught:
        load_settings(env_file=None)

    message = str(caught.value)
    for key in REQUIRED:
        assert key in message
    assert ".env.example" in message


def test_a_complete_environment_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://station:pw@localhost:5432/station")
    monkeypatch.setenv("MEDIA_ROOT", "/Volumes/station")

    settings = load_settings(env_file=None)

    assert settings.media_root.name == "station"
    assert settings.tts.cast_engine == "chatterbox"
