---
type: Captcha Solver
title: AmazonWAF
description: AWS WAF Captcha solver
resource: src/python3_anticaptcha/amazon_waf.py
tags:
  - amazon
  - waf
  - aws
  - captcha
---

# AmazonWAF

Solver class for AWS WAF Captcha challenges.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `AmazonTaskProxyless` | AWS WAF without proxy | No |
| `AmazonTask` | AWS WAF with proxy | Yes |

## Constructor Parameters

- `api_key`: AntiCaptcha API key
- `websiteURL`: URL of the webpage
- `websiteKey`: AWS WAF sitekey
- `iv`: Optional initialization vector
- `context`: Optional context parameter
- `challenge_script`: Optional challenge script
- `captcha_script`: Optional captcha script
- Proxy parameters (for AmazonTask)
- `sleep_time`: Polling interval

## Response Format

Returns a solution with AWS WAF-specific token.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)

## Citations

[1] `src/python3_anticaptcha/amazon_waf.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/AmazonTaskProxyless` — Official API documentation.
