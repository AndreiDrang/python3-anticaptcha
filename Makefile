install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

test:
	pip install pytest coverage pytest-asyncio requests_mock
	coverage run -m pytest tests -v --disable-warnings
	coverage report -m python3_anticaptcha/*.py

refactor:
	pip install black isort
	black python3_anticaptcha/
	isort -rc python3_anticaptcha/

release:
	pip install wheel twine
	python setup.py upload
