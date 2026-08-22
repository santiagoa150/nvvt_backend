VENV_DIR := .venv

.PHONY: start venv

start:
	fastapi dev src/main.py

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python -m venv $(VENV_DIR) >&2; \
	fi
	@if [ -f "$(VENV_DIR)/Scripts/activate" ]; then \
		echo "$(VENV_DIR)/Scripts/activate"; \
	else \
		echo "$(VENV_DIR)/bin/activate"; \
	fi
