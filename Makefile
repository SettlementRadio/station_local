# Settlement Radio — every operation has a target (ARCHITECTURE §17).
# Targets appear here only when they run; ADMIN.md documents them only after that.

SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help setup check doctor music-albums

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

check:  ## ruff + mypy + module sizes + unit tests + the music wiki (fast, model-free; the pre-push gate)
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy
	@over=$$(find src tests -name '*.py' ! -name 'store.py' -exec wc -l {} + \
		| awk '$$2 != "total" && $$1 > 400 {print "  " $$2 ": " $$1 " lines"}'); \
	if [ -n "$$over" ]; then echo "§31: modules over 400 lines:"; echo "$$over"; exit 1; fi
	uv run pytest tests/unit

doctor:  ## check config and system tools on this machine
	@uv run station doctor

music-albums:  ## list every album in the wiki, with its id and layer (GENRE= optional)
	@uv run station music-albums $(if $(GENRE),--genre $(GENRE),)
