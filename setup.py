from setuptools import setup

setup(
    name = 'python3-anticaptcha',
    version = '0.9.5',
    author = 'AndreiDrang, redV0ID',

    packages = ['python3_anticaptcha'],
    install_requires = [
                        'fake-useragent==0.1.11',
                        'requests>=2.18',
                        'aiohttp>=3'
    ],
    description = 'Python 3 AntiCaptcha library.',
    url = 'https://github.com/AndreiDrang/python3-anticaptcha',
    author_email = 'drang.andray@gmail.com',
    license = 'MIT',
    keywords = '''captcha 
                  anticaptcha 
				  python3
				  recaptcha
				  captcha
				  security
				  api
				  python-library
				  python-anticaptcha
				  anticaptcha-client''',
    python_requires = '>=3.6',
)
