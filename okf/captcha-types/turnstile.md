---
type: Captcha Solver
title: Turnstile
description: Cloudflare Turnstile captcha solver
resource: src/python3_anticaptcha/turnstile.py
tags:
  - turnstile
  - cloudflare
  - token
---

# Turnstile

Solver class for Cloudflare Turnstile captchas.

## Overview

Turnstile is Cloudflare's alternative to reCAPTCHA, designed to be more privacy-friendly. It presents users with various challenges and returns a token upon successful completion.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `TurnstileTaskProxyless` | Turnstile without proxy | No |
| `TurnstileTask` | Turnstile with proxy | Yes |

## Constructor

```python
def __init__(
    self,
    api_key: str,
    websiteURL: str,
    websiteKey: str,
    sleep_time: int = 10,
    proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
    proxyAddress: Optional[str] = None,
    proxyPort: Optional[int] = None,
    proxyLogin: Optional[str] = None,
    proxyPassword: Optional[str] = None,
    userAgent: Optional[str] = None,
    **kwargs
):
```

## Task Parameters

### TurnstileTaskProxyless
```python
{
    "type": "TurnstileTaskProxyless",
    "websiteURL": websiteURL,
    "websiteKey": websiteKey
}
```

### TurnstileTask
```python
{
    "type": "TurnstileTask",
    "websiteURL": websiteURL,
    "websiteKey": websiteKey,
    "proxyType": proxyType,
    "proxyAddress": proxyAddress,
    "proxyPort": proxyPort,
    "proxyLogin": proxyLogin,
    "proxyPassword": proxyPassword,
    "userAgent": userAgent
}
```

## Response Format

```python
{
    "errorId": 0,
    "status": "ready",
    "solution": {
        "token": "0.0.AX7..."
    },
    "cost": 0.002,
    "ip": "46.53.249.230",
    "createTime": 1679004358,
    "endTime": 1679004368,
    "solveCount": 0,
    "taskId": 396687629
}
```

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Uses [CaptchaTypeEnm](../api-contract/enums.md) for type validation

## Citations

[1] `src/python3_anticaptcha/turnstile.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/TurnstileTaskProxyless` — Official API documentation.
[3] `https://anti-captcha.com/apidoc/task-types/TurnstileTask` — Official API documentation.
