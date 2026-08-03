---
type: Captcha Solver
title: HCaptcha
description: hCaptcha solver
resource: src/python3_anticaptcha/core/enum.py
tags:
  - hcaptcha
  - captcha
  - token
---

# HCaptcha

Solver class for hCaptcha challenges.

## Overview

hCaptcha is a privacy-focused alternative to reCAPTCHA. The python3-anticaptcha library supports hCaptcha through the enum definitions, though a dedicated module may not exist in the current version.

## Supported Types (from enum)

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `HCaptchaTaskProxyless` | hCaptcha without proxy | No |
| `HCaptchaTask` | hCaptcha with proxy | Yes |

## Usage

hCaptcha can be used via the [CustomTask](custom-task.md) class:

```python
from python3_anticaptcha import CustomTask
from python3_anticaptcha.core.enum import CaptchaTypeEnm

result = CustomTask(
    api_key="YOUR_API_KEY",
    captcha_type=CaptchaTypeEnm.HCaptchaTaskProxyless,
    websiteURL="https://example.com",
    websiteKey="YOUR_SITEKEY"
).captcha_handler()
```

## Relationships

* Type defined in [CaptchaTypeEnm](../api-contract/enums.md)
* Can be used with [CustomTask](custom-task.md)

## Citations

[1] `src/python3_anticaptcha/core/enum.py:39-40` — Defines HCaptchaTask and HCaptchaTaskProxyless.
[2] `https://anti-captcha.com/apidoc/task-types/HCaptchaTaskProxyless` — Official API documentation.
