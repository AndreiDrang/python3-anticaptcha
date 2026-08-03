---
type: Captcha Solver
title: ReCaptchaV3
description: Google reCAPTCHA v3 solver (score-based)
resource: src/python3_anticaptcha/recaptcha_v3.py
tags:
  - recaptcha
  - google
  - v3
  - score
---

# ReCaptchaV3

Solver class for Google reCAPTCHA v3 captchas, which use a score-based system instead of user interaction.

## Overview

ReCaptchaV3 handles Google's score-based reCAPTCHA system. Unlike v2, reCAPTCHA v3 runs in the background and returns a score (0.0 to 1.0) indicating the likelihood that the user is human. AntiCaptcha workers generate tokens that achieve high scores.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `RecaptchaV3TaskProxyless` | reCAPTCHA v3 without proxy | No |

## Constructor

```python
def __init__(
    self,
    api_key: str,
    websiteURL: str,
    websiteKey: str,
    pageAction: Optional[str] = None,
    minScore: Optional[float] = None,
    sleep_time: int = 10,
    **kwargs
):
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | Yes | - | AntiCaptcha API key |
| `websiteURL` | str | Yes | - | URL of the webpage |
| `websiteKey` | str | Yes | - | reCAPTCHA v3 sitekey |
| `pageAction` | str | No | None | The action parameter for reCAPTCHA v3 |
| `minScore` | float | No | None | Minimum score required (0.0-1.0) |
| `sleep_time` | int | No | 10 | Seconds between polling attempts |

## Task Parameters

```python
{
    "type": "RecaptchaV3TaskProxyless",
    "websiteURL": websiteURL,
    "websiteKey": websiteKey,
    "pageAction": pageAction,
    "minScore": minScore
}
```

## Response Format

```python
{
    "errorId": 0,
    "status": "ready",
    "solution": {
        "gRecaptchaResponse": "3AHJ_VuvYIB..."
    },
    "cost": 0.002,
    "ip": "46.53.249.230",
    "createTime": 1679004358,
    "endTime": 1679004368,
    "solveCount": 0,
    "taskId": 396687629
}
```

## Usage Example

```python
from python3_anticaptcha import ReCaptchaV3

result = ReCaptchaV3(
    api_key="YOUR_API_KEY",
    websiteURL="https://example.com/page",
    websiteKey="6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
    pageAction="submit_form",
    minScore=0.9
).captcha_handler()

print(result["solution"]["gRecaptchaResponse"])
```

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Uses [CaptchaTypeEnm](../api-contract/enums.md) for type validation

## Citations

[1] `src/python3_anticaptcha/recaptcha_v3.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/RecaptchaV3TaskProxyless` — Official API documentation.
