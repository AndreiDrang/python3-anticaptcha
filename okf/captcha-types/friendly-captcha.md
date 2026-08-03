---
type: Captcha Solver
title: FriendlyCaptcha
description: FriendlyCaptcha puzzle solver
resource: src/python3_anticaptcha/friendly_captcha.py
tags:
  - friendly-captcha
  - puzzle
  - token
---

# FriendlyCaptcha

Solver class for FriendlyCaptcha puzzles.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `FriendlyCaptchaTaskProxyless` | FriendlyCaptcha without proxy | No |
| `FriendlyCaptchaTask` | FriendlyCaptcha with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `websiteKey`: FriendlyCaptcha sitekey
- Proxy parameters (for FriendlyCaptchaTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with a `solution` field containing the puzzle solution.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/friendly_captcha.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/FriendlyCaptchaTaskProxyless` — Official API documentation.
