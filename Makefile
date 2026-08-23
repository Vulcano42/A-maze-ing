SCRIPT = a_maze_ing.py
CONFIG = config.txt
PYTHON = python3

.PHONY: all install run clean lint lint-strict debug

all: run

install:
	$(PYTHON) -m pip isntall --upgrade pip
	$(PYTHON) -m pip install setuptools wheel flake8 mypy build mlx
	$(PYTHON) -m pip install -e .

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__.py .mypy_cache build dist *.egg-info */__pycache__

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .