VENV_DIR := .venv

.PHONY: start venv seed-countries

start:
	fastapi dev src/main.py

seed-countries:
	cd src && python -m countries.infrastructure.mongodb.seed_countries

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python -m venv $(VENV_DIR) >&2; \
	fi
	@if [ -f "$(VENV_DIR)/Scripts/activate" ]; then \
		echo "$(VENV_DIR)/Scripts/activate"; \
	else \
		echo "$(VENV_DIR)/bin/activate"; \
	fi
