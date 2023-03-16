import io
import os
import sys
import shutil
import logging

from setuptools import Command, setup
from pkg_resources import parse_requirements

from python3_anticaptcha.__version__ import __version__

# Package meta-data.
NAME = "python3-anticaptcha"
DESCRIPTION = "Python 3 Anti-Captcha service library with AIO module."
URL = "https://andreidrang.github.io/python3-anticaptcha"
EMAIL = "python-captcha@pm.me"
AUTHOR = "AndreiDrang, redV0ID"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = __version__
with open("requirements.txt", "rt") as requirements_txt:
    REQUIRED = [str(requirement) for requirement in parse_requirements(requirements_txt)]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "../README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        logging.info("Clean builds . . .")
        shutil.rmtree("./dist/", ignore_errors=True)

        logging.info("Building Source and Wheel distribution . . .")
        os.system("python setup.py bdist_wheel")

        logging.info("Uploading the package to PyPI via Twin . . .")
        os.system("twine upload dist/* --verbose")

        logging.info("🤖 Uploaded . . .")

        logging.info("Clean builds . . .")
        shutil.rmtree("./dist/")

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=["python3_anticaptcha"],
    install_requires=REQUIRED,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"python3-anticaptcha": "python3_anticaptcha"},
    include_package_data=True,
    url=URL,
    project_urls={
        "Documentation": URL,
        "Source": "https://github.com/AndreiDrang/python3-anticaptcha",
    },
    author_email=EMAIL,
    license="MIT",
    keywords="""
                captcha 
                anticaptcha 
				python3
                recaptcha
                recaptchav2
                recaptchav3
                security
                api
				funcaptcha
				keycaptcha
				recaptcha
				geetest
				hcaptcha
                python-library
                python-anticaptcha
                anticaptcha-client
                imagecaptcha
                turnstile
               """,
    python_requires=REQUIRES_PYTHON,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: AsyncIO",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    # Build and upload package: python3 setup.py upload
    cmdclass={"upload": UploadCommand},
)
print("🤖 Success install ...")
