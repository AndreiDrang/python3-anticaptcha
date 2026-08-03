---
type: Captcha Solver
title: Prosopo
description: Prosopo captcha solver
resource: src/python3_anticaptcha/prosopo_captcha.py
tags:
  - prosopo
  - captcha
  - token
---

# Prosopo

Solver class for Prosopo captchas.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `ProsopoTaskProxyless` | Prosopo without proxy | No |
| `ProsopoTask` | Prosopo with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `websiteKey`: Prosopo sitekey
- `data`: Optional data parameter
- Proxy parameters (for ProsopoTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with Prosopo-specific token.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/prosopo_captcha.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/ProsopoTaskProxyless` — Official API documentation.
