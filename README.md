# python3-anticaptcha

[![PyPI version](https://badge.fury.io/py/python3-anticaptcha.svg)](https://badge.fury.io/py/python3-anticaptcha)
[![Python versions](https://img.shields.io/pypi/pyversions/python3-anticaptcha.svg?logo=python&logoColor=FBE072)](https://badge.fury.io/py/python3-anticaptcha)
[![Downloads](https://static.pepy.tech/badge/python3-anticaptcha/month)](https://pepy.tech/project/python3-anticaptcha)
[![Static Badge](https://img.shields.io/badge/docs-Sphinx-green?label=Documentation&labelColor=gray)](https://andreidrang.github.io/python3-anticaptcha/)
[![Test](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/test.yml)
[![Lint](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/AndreiDrang/python3-anticaptcha/actions/workflows/lint.yml)

Python 3 client library for [AntiCaptcha](https://getcaptchasolution.com/vchfpctqyz) service - solve reCAPTCHA, hCaptcha, image captchas, and more programmatically.

## Why use this library?

AntiCaptcha is a paid captcha solving service. This library provides a clean Python interface to:
- Submit captchas to AntiCaptcha's worker network
- Poll for results automatically
- Handle proxy rotation for high-volume requests
- Support both synchronous and asynchronous workflows

## Supported Captcha Types

| Type | Class | Use Case |
|------|-------|----------|
| reCAPTCHA v2 | `ReCaptchaV2` | Google reCAPTCHA V2 checkbox/invisible |
| reCAPTCHA v3 | `ReCaptchaV3` | Google reCAPTCHA V3 score-based |
| Image Captcha | `ImageToText` | Classic text-from-image captchas |
| Image Coordinates | `ImageToCoordinates` | Click-on-image captchas |
| FunCaptcha | `FunCaptcha` | Arkose Labs (formerly FunCaptcha) |
| GeeTest | `GeeTest` | Chinese GeeTest captcha |
| Turnstile | `Turnstile` | Cloudflare Turnstile |
| FriendlyCaptcha | `FriendlyCaptcha` | FriendlyCaptcha puzzles |
| Prosopo | `Prosopo` | Prosopo captcha |
| Amazon WAF | `AmazonWAF` | AWS WAF Captcha |

## Quick Start

### 1. Install

```bash
pip install python3-anticaptcha
```

### 2. Get Your API Key

1. Log into [AntiCaptcha](https://getcaptchasolution.com/vchfpctqyzclients/settings/apisetup)
2. Copy your API key from the "Setup" section

### 3. Solve a reCAPTCHA

```python
from python3_anticaptcha import ReCaptchaV2
from python3_anticaptcha.core.enum import CaptchaTypeEnm

# Basic usage (no proxy)
result = ReCaptchaV2(
    api_key="YOUR_API_KEY",
    captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
    websiteURL="https://example.com/page-with-captcha",
    websiteKey="6LeIxAKTAAAAAJ309xRj9YBN2aaaaaaaaa",  # sitekey from the page
).captcha_handler()

print(result["solution"]["gRecaptchaResponse"])
```

### 4. Solve with Proxy

```python
from python3_anticaptcha import ReCaptchaV2
from python3_anticaptcha.core.enum import CaptchaTypeEnm, ProxyTypeEnm

result = ReCaptchaV2(
    api_key="YOUR_API_KEY",
    captcha_type=CaptchaTypeEnm.RecaptchaV2Task,
    websiteURL="https://example.com/page-with-captcha",
    websiteKey="6LeIxAKTAAAAAJ309xRj9YBN2aaaaaaaaa",
    proxyType=ProxyTypeEnm.HTTP,
    proxyAddress="123.45.67.89",
    proxyPort=8080,
    proxyLogin="proxy_user",
    proxyPassword="proxy_pass",
    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
).captcha_handler()
```

### 5. Async Usage

```python
import asyncio
from python3_anticaptcha import ReCaptchaV2
from python3_anticaptcha.core.enum import CaptchaTypeEnm

async def solve():
    result = await ReCaptchaV2(
        api_key="YOUR_API_KEY",
        captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
        websiteURL="https://example.com/page-with-captcha",
        websiteKey="6LeIxAKTAAAAAJ309xRj9YBN2aaaaaaaaa",
    ).aio_captcha_handler()
    return result

result = asyncio.run(solve())
```

## Environment Variable

Set `API_KEY` to avoid passing it in code:

```bash
export API_KEY="your_api_key_here"
```

```python
# Now you can omit api_key parameter
from python3_anticaptcha import ImageToText

result = ImageToText(captcha_file="captcha.png").captcha_handler()
```

## Configuration Options

All captcha classes support these common parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | str | Your AntiCaptcha API key (or set `API_KEY` env var) |
| `sleep_time` | int | Seconds between result polls (default: 10) |

## Documentation

- [Full Documentation](https://andreidrang.github.io/python3-anticaptcha/) - Detailed API reference
- [AntiCaptcha Errors](https://getcaptchasolution.com/vchfpctqyzapidoc/errors) - Error code meanings

## Development

```bash
# Run tests
make tests

# Run linters
make lint

# Build package
make build
```

## Contacts

- Telegram: [pythoncaptcha](https://t.me/pythoncaptcha)
- Email: python-captcha@pm.me

---

Love Rust? Check out [Rust-AntiCaptcha](https://crates.io/crates/rust-anticaptcha) - same API for Rust projects.
