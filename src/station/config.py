"""The only place the environment is read (§23, §31).

Why it fails at import: a missing value must stop the process at startup, where the operator is
looking at it, rather than at 02:00 in the middle of a render. Importing this module is therefore
the fail-fast gate, and `cli.py` turns the resulting `ConfigError` into a message that names the
line to add.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ENV_FILE = ".env"


class ConfigError(RuntimeError):
    """The environment cannot produce a valid `Settings`. Carries an operator-readable message."""


class TTSSettings(BaseModel):
    """Voice pipeline knobs (§12, §25). Callers branch on capabilities, never on these names."""

    cast_engine: str = "chatterbox"
    fallback_engine: str = "kokoro"
    target_lufs: float = -16.0
    per_turn_timeout_s: int = 120


class BatchSettings(BaseModel):
    """The nightly window (§14). `must_finish_by` is audio pushed, not the digest."""

    start_hour: int = 20
    unload_writer_at: str = "00:00"
    must_finish_by: str = "06:50"
    show_lead_days: int = 2
    junction_lead_days: int = 1


class Settings(BaseSettings):
    """Everything tunable. Nested values take `TTS__TARGET_LUFS` form in the environment."""

    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    # Required — absent means every command stops at startup and names the line.
    database_url: PostgresDsn
    media_root: Path

    # Optional — the command that needs one fails naming it, rather than blocking every command.
    icecast_source_password: SecretStr | None = None

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    tts: TTSSettings = TTSSettings()
    batch: BatchSettings = BatchSettings()

    # `.env.example` ships every line with an empty value, so a blank means "not set" rather than
    # "set to nothing" — otherwise a freshly copied .env configures an empty log level.

    @field_validator("log_level", mode="before")
    @classmethod
    def _blank_log_level(cls, value: object) -> object:
        return value.strip().upper() or "INFO" if isinstance(value, str) else value

    @field_validator("icecast_source_password", mode="before")
    @classmethod
    def _blank_secret(cls, value: object) -> object:
        return None if isinstance(value, str) and not value.strip() else value


def _explain(exc: ValidationError) -> str:
    """Render a pydantic error as the `.env` lines the operator has to fix."""
    lines = []
    for err in exc.errors():
        name = "__".join(str(part) for part in err["loc"]).upper()
        if err["type"] == "missing":
            lines.append(f"  {name:<26} required, and set in neither .env nor the environment")
        else:
            lines.append(f"  {name:<26} {err['msg']}")
    return (
        "Configuration is incomplete. These lines are missing or wrong:\n\n"
        + "\n".join(lines)
        + "\n\n.env.example lists every line with an empty value. Copy it to .env and fill it in."
    )


def load_settings(env_file: str | Path | None = DEFAULT_ENV_FILE) -> Settings:
    """Build `Settings`, converting pydantic's report into one an operator can act on."""
    try:
        return Settings(_env_file=env_file)  # type: ignore[call-arg]  # pydantic-settings kwarg
    except ValidationError as exc:
        raise ConfigError(_explain(exc)) from exc


settings = load_settings()
