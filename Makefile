.PHONY: install remove tests refactor lint build upload doc

install:
	uv sync

remove:
	uv pip uninstall python3-anticaptcha

tests:
	uv run --extra test coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --disable-warnings \
	tests/ && \
	uv run --extra test coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	uv run --extra test coverage html --precision=3 --skip-empty -d coverage/html/ && \
	uv run --extra test coverage xml -o coverage/coverage.xml

refactor:
	uv run --extra style ruff check --fix src tests && \
	uv run --extra style ruff format src tests

lint:
	uv run --extra style ruff check src tests && \
	uv run --extra style ruff format --check src tests

build:
	uv build

upload:
	uv build
	uv publish

doc:
	uv run --extra docs sphinx-build -M html docs docs/_build
