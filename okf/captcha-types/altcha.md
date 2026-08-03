---
type: Captcha Solver
title: Altcha
description: Altcha captcha solver
resource: src/python3_anticaptcha/altcha.py
tags:
  - altcha
  - captcha
  - token
---

# Altcha

Solver class for Altcha captchas.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `AltchaTaskProxyless` | Altcha without proxy | No |
| `AltchaTask` | Altcha with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `websiteKey`: Altcha sitekey
- `action`: Optional action parameter
- `cache_key`: Optional cache key
- Proxy parameters (for AltchaTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with Altcha-specific token.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/altcha.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/AltchaTaskProxyless` — Official API documentation.
