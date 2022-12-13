install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

test:
	pip install pytest coverage pytest-asyncio requests_mock
	coverage run -m pytest tests -v --disable-warnings
	coverage report -m python3_anticaptcha/*.py

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
