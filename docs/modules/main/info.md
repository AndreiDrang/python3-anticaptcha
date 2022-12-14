# Introduction

## Welcome to python3-anticaptcha

![](../../_static/AntiCaptcha.png)

[![PyPI version](https://badge.fury.io/py/python3-captchaai.svg)](https://badge.fury.io/py/python3-captchaai)
[![Python versions](https://img.shields.io/pypi/pyversions/python3-captchaai.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python3-captchaai)
[![Downloads](https://pepy.tech/badge/python3-captchaai/month)](https://pepy.tech/project/python3-captchaai)

[![Maintainability](https://api.codeclimate.com/v1/badges/3431fd3fe71baf7eb9da/maintainability)](https://codeclimate.com/github/AndreiDrang/python3-captchaai/maintainability)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/323d4eda0fe1477bbea8fe8902b9e97e)](https://www.codacy.com/gh/AndreiDrang/python3-captchaai/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndreiDrang/python3-captchaai&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/AndreiDrang/python3-captchaai/branch/main/graph/badge.svg?token=2L4VVIF4G8)](https://codecov.io/gh/AndreiDrang/python3-captchaai)

[![Build check](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/test_build.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/test_build.yml)
[![Installation check](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/install.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/install.yml)
[![Test](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-captchaai/actions/workflows/lint.yml)


Python3 library for [Capsolver](https://capsolver.com/) service API.

Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [Capsolver](https://capsolver.com/) service API.

## How to install?

We recommend using the latest version of Python. `python3-captchaai` supports Python
3.7+.

### pip

```bash
pip install python3-captchaai
```

### Source
```bash
git clone https://github.com/AndreiDrang/python3-captchaai.git
cd python3-captchaai
python setup.py install
```

## How to test?

1. You need set ``API_KEY`` in your environment(get this value from you account).
2. Run command ``make tests``, from root directory.
