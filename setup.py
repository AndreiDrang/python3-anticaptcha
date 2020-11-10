import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = "python3-anticaptcha"
DESCRIPTION = "Python 3 Anti-Captcha service library with AIO module."
URL = "https://github.com/AndreiDrang/python3-anticaptcha"
EMAIL = "drang.andray@gmail.com"
AUTHOR = "AndreiDrang, redV0ID"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.7"
REQUIRED = ["requests==2.23.0", "aiohttp==3.7.2", "pika==1.1.0"]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
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
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

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
    author_email=EMAIL,
    license="MIT",
    keywords="""
                captcha 
                anticaptcha 
				python3
                recaptcha
                security
                api
                python-library
                python-anticaptcha
                anticaptcha-client
               """,
    python_requires=REQUIRES_PYTHON,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    # Build and upload package: python3 setup.py upload
    cmdclass={"upload": UploadCommand},
)
