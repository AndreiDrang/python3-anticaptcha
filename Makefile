install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

test:
	pip install pytest pytest-cov pytest-asyncio requests_mock
	pytest tests --cov=python3_anticaptcha/ -v

refactor:
	pip install black isort
	black python3_anticaptcha/
	isort -rc python3_anticaptcha/

upload:
	pip install twine
	python setup.py upload
