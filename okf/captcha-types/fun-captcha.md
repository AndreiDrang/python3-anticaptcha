---
type: Captcha Solver
title: FunCaptcha
description: Arkose Labs FunCaptcha solver
resource: src/python3_anticaptcha/fun_captcha.py
tags:
  - funcaptcha
  - arkose
  - token
---

# FunCaptcha

Solver class for Arkose Labs FunCaptcha (formerly known as FunCaptcha).

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `FunCaptchaTaskProxyless` | FunCaptcha without proxy | No |
| `FunCaptchaTask` | FunCaptcha with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `websiteKey`: FunCaptcha sitekey
- `surl`: Optional SURL parameter
- `userAgent`: Optional browser User-Agent
- `data`: Optional data blob parameter
- Proxy parameters (for FunCaptchaTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with a `token` field containing the FunCaptcha token.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/fun_captcha.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/FunCaptchaTaskProxyless` — Official API documentation.
[3] `https://anti-captcha.com/apidoc/task-types/FunCaptchaTask` — Official API documentation.
