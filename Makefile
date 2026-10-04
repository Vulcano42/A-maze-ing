SCRIPT = a_maze_ing.py
CONFIG = config.txt
PYTHON = python3
ENV = . env/bin/activate

.PHONY: all install run clean lint lint-strict debug

all: fclean install run

install:
	cd mlx-2.2 && tar -xzf mlx-2.2.tgz
	$(PYTHON) -m venv env
	$(ENV) && pip install mlx-2.2/ubuntu/mlx-2.2-py3-none-any.whl build

# $(PYTHON) -m pip install setuptools wheel flake8 mypy build mlx
# $(PYTHON) -m pip install -e .

run:
	$(ENV) && $(PYTHON) $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__.py .mypy_cache build dist *.egg-info */__pycache__

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

fclean: clean
	rm -rf env 
	rm -rf maze.txt
	rm -rf mlx-2.2/fedora mlx-2.2/src mlx-2.2/ubuntu
	rm -rf dist mazen.egg-info
