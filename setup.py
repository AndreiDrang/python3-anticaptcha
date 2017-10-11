from setuptools import setup

setup(
	name='python-anticaptcha',
	version='0.9.8.b',
	author='AndreiDrang, redV0ID',
	
	packages=['python_anticaptcha'],
	install_requires=[
		'requests>=2.18',
	],
	description='Python 3 AntiCaptcha library.',
	author_email='drang.andray@gmail.com',
	license='MIT',
	keywords='''captcha 
				anticaptcha 
				python3
				flask
				recaptcha
				captcha
				security
				api
				python-library
				python-anticaptcha
				rucaptcha-client''',
	python_requires='>=3.3',
)
