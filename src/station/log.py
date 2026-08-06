"""structlog setup, called once at process start (§24).

Why a module rather than a call site: the renderer choice — JSON to stdout for the log file, the
human renderer when a terminal is attached — has to be made in exactly one place, or half the
night's output arrives in the wrong shape and `jq` (the whole log platform here) stops working.
"""

from __future__ import annotations

import sys
from typing import Any

import structlog

_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}


def configure(level: str = "INFO", *, force_json: bool = False) -> None:
    """Install the processor chain. Safe to call twice; the last call wins."""
    if level.upper() not in _LEVELS:
        raise ValueError(f"unknown log level {level!r}; one of {sorted(_LEVELS)}")

    human = sys.stdout.isatty() and not force_json
    renderer: structlog.typing.Processor = (
        structlog.dev.ConsoleRenderer() if human else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(_LEVELS[level.upper()]),
        logger_factory=structlog.WriteLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(**initial: Any) -> structlog.stdlib.BoundLogger:
    """A logger with the standard fields of §24 bound: `run_id`, `phase`, `job`, and so on."""
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    return logger.bind(**initial) if initial else logger
