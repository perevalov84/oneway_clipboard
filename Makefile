PYTHON ?= ../bin/python
SETTINGS_FILENAME = pyproject.toml

PHONY = install-dev

install-dev:
	${PYTHON} -m flit install -s --env --deps=develop --symlink

test:
	${PYTHON} -m pytest --pdb -svvv tests

run:
	${PYTHON} -m flask --app src.oneway_clipboard.flask.app --debug run --host 0.0.0.0