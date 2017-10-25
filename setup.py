from setuptools import setup

setup(
	name='python3-anticaptcha',
	version='0.5.a',
	author='AndreiDrang, redV0ID',
	
	packages=['python3_anticaptcha'],
	install_requires=[
						'requests>=2.18',
					],
	description='Python 3 AntiCaptcha library.',
	author_email='drang.andray@gmail.com',
	license='MIT',
	keywords='''captcha 
				anticaptcha 
				python3
				recaptcha
				captcha
				security
				api
				python-library
				python-anticaptcha
				anticaptcha-client''',
	python_requires='>=3.3',
)
