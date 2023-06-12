# Introduction

## Welcome to python3-anticaptcha

![](../../_static/AntiCaptcha.png)

<a href="https://dashboard.capsolver.com/passport/register?inviteCode=kQTn-tG07Jb1">
    <img src="https://cdn.discordapp.com/attachments/1105172394655625306/1105180101802471575/20221207-160749.gif" alt="Capsolver's Banner">
</a>
<br>
At the lowest price on the market, you may receive a variety of solutions, including reCAPTCHA V2, reCAPTCHA V3, hCaptcha, hCaptcha Click, FunCaptcha, picture-to-text, and more. With this service, 0.1s is the slowest speed ever measured.
<hr>

[![PyPI version](https://badge.fury.io/py/python3-anticaptcha.svg)](https://badge.fury.io/py/python3-anticaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python3-anticaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python3-anticaptcha)
[![Downloads](https://pepy.tech/badge/python3-anticaptcha/month)](https://pepy.tech/project/python3-anticaptcha)

[![Code Climate](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha/badges/gpa.svg)](https://codeclimate.com/github/AndreiDrang/python3-anticaptcha)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7f49780f2edb48d4b133833887c850e8)](https://www.codacy.com/gh/AndreiDrang/python3-anticaptcha/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndreiDrang/python3-anticaptcha&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/AndreiDrang/python3-anticaptcha/branch/master/graph/badge.svg?token=W92nfZY6Tz)](https://codecov.io/gh/AndreiDrang/python3-anticaptcha)

[![Build check](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test_build.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test_build.yml)
[![Installation check](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/install.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/install.yml)
[![Test](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/lint.yml)


Python 3 library for [AntiCaptcha](https://anti-captcha.com/) service API.

Tested on UNIX based OS.

The library is intended for software developers and is used to work with the [AntiCaptcha](https://anti-captcha.com/) service API.

## How to install?

We recommend using the latest version of Python. `python3-anticaptcha` supports Python 3.7+.

### pip

```bash
pip install python3-anticaptcha
```

### Source
```bash
git clone https://github.com/AndreiDrang/python3-anticaptcha.git
cd python3-anticaptcha
python setup.py install
```

## How to test?

1. You need set ``API_KEY`` in your environment(get this value from you account).
2. Run command ``make tests``, from root directory.
