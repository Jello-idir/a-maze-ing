PYTHON	= python3.14
MAIN	= a-maze-ing.py
CONFIG	= config.txt

install:
	pip install -r requirements.txt

run:
	@$(PYTHON) $(MAIN) $(CONFIG)

debug:
	@$(PYTHON) -m pdb $(MAIN)

clean:
	@rm -rf __pycache__ */__pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
