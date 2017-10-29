from setuptools import setup

setup(
	name='python3-anticaptcha',
	version='0.6',
	author='AndreiDrang, redV0ID',
	
	packages=['python3_anticaptcha'],
	install_requires=[
		'requests>=2.18',
	],
	description='Python 3 AntiCaptcha library.',
	url='https://github.com/AndreiDrang/python3-anticaptcha',
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
