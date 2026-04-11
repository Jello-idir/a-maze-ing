install:
	pip install -r requirements.txt

run:
	@python3.14 a-maze-ing.py config.txt

debug:
	@python3.12 -m pdb a-maze-ing.py

clean:
	@rm -rf __py* */__py*

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict
