install:
	python setup.py install

remove:
	pip uninstall python3-anticaptcha -y

refactor:
	pip install black isort
	black python3_anticaptcha/
	isort -rc python3_anticaptcha/

upload:
	pip install twine
	python setup.py upload
