"""Test environment.

Why this exists: importing `station.config` validates the environment (§23), so the suite supplies
its own values instead of depending on whatever `.env` the operator happens to have — and CI has
none at all.
"""

from __future__ import annotations

import os

os.environ.setdefault("DATABASE_URL", "postgresql://station:station@localhost:5432/station_test")
os.environ.setdefault("MEDIA_ROOT", "/tmp/station-test")
