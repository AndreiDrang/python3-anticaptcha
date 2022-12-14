install:
	cd src/ && pip install -e .

tests:
	cd src/ && \
	coverage run --rcfile=.coveragerc -m pytest -s tests --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

refactor:
	black docs/
	isort docs/

	cd src/ && \
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python3_anticaptcha/ tests/ && \
	black python3_anticaptcha/ tests/ && \
	isort python3_anticaptcha/ tests/

lint:
	cd src/ && \
	autoflake --in-place --recursive python3_anticaptcha/ --check && \
	black python3_anticaptcha/ --check && \
	isort python3_anticaptcha/ --check-only

release:
	pip install twine
	python setup.py upload

upload:
	pip install twine
	cd src/ && python setup.py upload

doc:
	cd docs/ && \
	make html -e
