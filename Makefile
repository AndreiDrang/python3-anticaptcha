install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

test:
	coverage run --rcfile=.coveragerc -m pytest -s tests --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d html/ && \
	coverage xml -o coverage.xml

refactor:
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python3_anticaptcha/ setup.py && \
	black python3_anticaptcha/ setup.py && \
	isort python3_anticaptcha/ setup.py

lint:
	autoflake --in-place --recursive python3_anticaptcha/ --check && \
	black python3_anticaptcha/ --check && \
	isort python3_anticaptcha/ --check-only

release:
	pip install twine
	python setup.py upload
