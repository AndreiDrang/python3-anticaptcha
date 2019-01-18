from setuptools import setup

setup(
    name = 'python3-anticaptcha',
    version = '1.2.1',
    author = 'AndreiDrang, redV0ID',

    packages = ['python3_anticaptcha'],
    install_requires = [
                        'requests==2.21.0',
                        'aiohttp==3.5.4',
                        'pika==0.12.0'
    ],
    description = 'Python 3 Anti-Captcha service library with AIO module.',
    package_dir={'python3-anticaptcha': 'python3_anticaptcha'},
    include_package_data=True,
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
    zip_safe=False
)
