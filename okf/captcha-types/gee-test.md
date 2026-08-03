---
type: Captcha Solver
title: GeeTest
description: GeeTest captcha solver
resource: src/python3_anticaptcha/gee_test.py
tags:
  - geetest
  - captcha
  - token
---

# GeeTest

Solver class for GeeTest captchas, commonly used on Chinese websites.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `GeeTestTaskProxyless` | GeeTest without proxy | No |
| `GeeTestTask` | GeeTest with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `gt`: GeeTest GT parameter
- `challenge`: GeeTest challenge parameter
- `api_server`: Optional API server subdomain
- Proxy parameters (for GeeTestTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with GeeTest-specific token fields.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/gee_test.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/GeeTestTaskProxyless` — Official API documentation.
[3] `https://anti-captcha.com/apidoc/task-types/GeeTestTask` — Official API documentation.
