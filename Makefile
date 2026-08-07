# Settlement Radio — every operation has a target (ARCHITECTURE §17).
# Targets appear here only when they run; ADMIN.md documents them only after that.

SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help setup check doctor music-brief music-check music-style music-songs

help:  ## list the targets that exist today
	@echo "Settlement Radio — make targets"
	@echo
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-14s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "  ARCHITECTURE §17 lists the rest. They arrive with the task that builds them."

setup:  ## install deps and hooks, check system tools
	@command -v brew >/dev/null || { echo "Homebrew is required: https://brew.sh"; exit 1; }
	@command -v uv   >/dev/null || brew install uv
	@command -v gitleaks >/dev/null || brew install gitleaks
	uv sync --frozen
	uv run pre-commit install --install-hooks
	@echo
	@if [ ! -f .env ]; then \
		echo "next: cp .env.example .env && chmod 600 .env, then fill in every line"; \
		echo "      then: make doctor"; \
	else \
		$(MAKE) --no-print-directory doctor; \
	fi

check:  ## ruff + mypy + module sizes + unit tests (fast, model-free; the pre-push gate)
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy
	@over=$$(find src tests -name '*.py' ! -name 'store.py' -exec wc -l {} + \
		| awk '$$2 != "total" && $$1 > 400 {print "  " $$2 ": " $$1 " lines"}'); \
	if [ -n "$$over" ]; then echo "§31: modules over 400 lines:"; echo "$$over"; exit 1; fi
	uv run pytest tests/unit

doctor:  ## check config and system tools on this machine
	@uv run station doctor

music-brief:  ## build one genre's writer brief → clipboard (GENRE=relay-pop)
	@test -n "$(GENRE)" || { echo "usage: make music-brief GENRE=relay-pop"; exit 2; }
	@uv run station music-brief "$(GENRE)" --out music/briefs/$(GENRE)-write.md
	@pbcopy < music/briefs/$(GENRE)-write.md && echo "  → on your clipboard. Paste it into a NEW chat."

music-check:  ## build one genre's checker brief → clipboard (GENRE=relay-pop)
	@test -n "$(GENRE)" || { echo "usage: make music-check GENRE=relay-pop"; exit 2; }
	@uv run station music-brief "$(GENRE)" --kind check --out music/briefs/$(GENRE)-check.md
	@pbcopy < music/briefs/$(GENRE)-check.md && echo "  → on your clipboard. Paste it into a DIFFERENT chat."

music-style:  ## build the style-card brief for one genre's bands → clipboard (GENRE=relay-pop)
	@test -n "$(GENRE)" || { echo "usage: make music-style GENRE=relay-pop"; exit 2; }
	@uv run station music-style "$(GENRE)" --out music/briefs/$(GENRE)-style.md
	@pbcopy < music/briefs/$(GENRE)-style.md && echo "  → on your clipboard. Save the reply to music/production/styles.yaml"

music-songs:  ## build one album's lyrics + prompts brief → clipboard (ALBUM=al_001)
	@test -n "$(ALBUM)" || { echo "usage: make music-songs ALBUM=al_001"; exit 2; }
	@uv run station music-songs "$(ALBUM)" --out music/briefs/$(ALBUM)-songs.md
	@pbcopy < music/briefs/$(ALBUM)-songs.md && echo "  → on your clipboard."
