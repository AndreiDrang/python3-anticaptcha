install:
	pip3 install -e .

remove:
	pip3 uninstall python3_anticaptcha -y

tests: install
	coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --pastebin=all  --disable-warnings \
	tests/ && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

refactor:
	black docs/
	isort docs/

	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/ tests/ && \
	black src/ tests/ && \
	isort src/ tests/

lint:
	autoflake --in-place --recursive src/ --check && \
	black src/ --check && \
	isort src/ --check-only

build:
	pip3 install --upgrade build setuptools
	python3 -m build

upload:
	pip3 install wheel setuptools build
	pip3 install twine==6.1.0
	twine upload dist/*

doc: install
	cd docs/ && \
	make html -e
