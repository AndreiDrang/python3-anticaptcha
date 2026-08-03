---
type: Captcha Solver
title: ReCaptchaV2
description: Google reCAPTCHA v2 solver (checkbox and invisible variants)
resource: src/python3_anticaptcha/recaptcha_v2.py
tags:
  - recaptcha
  - google
  - token
  - v2
---

# ReCaptchaV2

Solver class for Google reCAPTCHA v2 captchas, supporting both standard checkbox and invisible variants, as well as Enterprise versions.

## Overview

ReCaptchaV2 handles Google's reCAPTCHA v2 service, which presents users with a checkbox challenge ("I'm not a robot") or operates invisibly in the background. The solver submits the page URL and sitekey to AntiCaptcha workers who solve the challenge and return a solution token.

## Supported Variants

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `RecaptchaV2TaskProxyless` | Standard reCAPTCHA v2 without proxy | No |
| `RecaptchaV2Task` | Standard reCAPTCHA v2 with proxy | Yes |
| `RecaptchaV2EnterpriseTaskProxyless` | Enterprise reCAPTCHA v2 without proxy | No |
| `RecaptchaV2EnterpriseTask` | Enterprise reCAPTCHA v2 with proxy | Yes |

## Constructor

```python
def __init__(
    self,
    api_key: str,
    captcha_type: Union[CaptchaTypeEnm, str],
    websiteURL: str,
    websiteKey: str,
    recaptchaDataSValue: Optional[str] = None,
    isInvisible: bool = False,
    enterprisePayload: Optional[dict] = None,
    apiDomain: Optional[str] = None,
    proxyType: Optional[Union[ProxyTypeEnm, str]] = None,
    proxyAddress: Optional[str] = None,
    proxyPort: Optional[int] = None,
    proxyLogin: Optional[str] = None,
    proxyPassword: Optional[str] = None,
    userAgent: Optional[str] = None,
    cookies: Optional[str] = None,
    sleep_time: int = 10,
):
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | Yes | - | AntiCaptcha API key |
| `captcha_type` | CaptchaTypeEnm or str | Yes | - | Type of reCAPTCHA task (see Supported Variants) |
| `websiteURL` | str | Yes | - | URL of the webpage containing the captcha |
| `websiteKey` | str | Yes | - | reCAPTCHA sitekey from the webpage |
| `recaptchaDataSValue` | str | No | None | Value of 'data-s' parameter (Google sites only) |
| `isInvisible` | bool | No | False | Whether reCAPTCHA is invisible |
| `enterprisePayload` | dict | No | None | Additional parameters for Enterprise reCAPTCHA |
| `apiDomain` | str | No | None | Domain for serving reCAPTCHA script (www.google.com or www.recaptcha.net) |
| `proxyType` | ProxyTypeEnm or str | No | None | Proxy protocol type |
| `proxyAddress` | str | No | None | Proxy IP address |
| `proxyPort` | int | No | None | Proxy port |
| `proxyLogin` | str | No | None | Proxy username |
| `proxyPassword` | str | No | None | Proxy password |
| `userAgent` | str | No | None | Browser User-Agent string |
| `cookies` | str | No | None | Additional cookies for Google domains |
| `sleep_time` | int | No | 10 | Seconds between polling attempts |

## Task Parameters

The `task_params` dictionary is constructed based on the captcha_type:

### RecaptchaV2TaskProxyless / RecaptchaV2Task
```python
{
    "type": captcha_type,
    "websiteURL": websiteURL,
    "websiteKey": websiteKey,
    "recaptchaDataSValue": recaptchaDataSValue,
    "isInvisible": isInvisible
}
```

If `captcha_type == RecaptchaV2Task`, also includes:
```python
{
    "proxyType": proxyType,
    "proxyAddress": proxyAddress,
    "proxyPort": proxyPort,
    "proxyLogin": proxyLogin,
    "proxyPassword": proxyPassword,
    "userAgent": userAgent,
    "cookies": cookies
}
```

### RecaptchaV2EnterpriseTaskProxyless / RecaptchaV2EnterpriseTask
```python
{
    "type": captcha_type,
    "websiteURL": websiteURL,
    "websiteKey": websiteKey,
    "enterprisePayload": enterprisePayload,
    "apiDomain": apiDomain
}
```

If `captcha_type == RecaptchaV2EnterpriseTask`, also includes proxy parameters.

## Response Format

Successful response includes:
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

The `gRecaptchaResponse` token is what you submit to the target website to verify the captcha was solved.

## Usage Examples

### Basic (Proxyless)
```python
from python3_anticaptcha import ReCaptchaV2
from python3_anticaptcha.core.enum import CaptchaTypeEnm

result = ReCaptchaV2(
    api_key="YOUR_API_KEY",
    captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
    websiteURL="https://example.com/page-with-captcha",
    websiteKey="6LeIxAKTAAAAAJ309xRj9YBN2aaaaaaaaa"
).captcha_handler()

print(result["solution"]["gRecaptchaResponse"])
```

### With Proxy
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
    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
).captcha_handler()
```

### Async
```python
import asyncio
from python3_anticaptcha import ReCaptchaV2
from python3_anticaptcha.core.enum import CaptchaTypeEnm

async def solve():
    result = await ReCaptchaV2(
        api_key="YOUR_API_KEY",
        captcha_type=CaptchaTypeEnm.RecaptchaV2TaskProxyless,
        websiteURL="https://example.com/page-with-captcha",
        websiteKey="6LeIxAKTAAAAAJ309xRj9YBN2aaaaaaaaa"
    ).aio_captcha_handler()
    return result

result = asyncio.run(solve())
```

## Validation

The constructor validates that `captcha_type` is one of:
- `RecaptchaV2Task`
- `RecaptchaV2TaskProxyless`
- `RecaptchaV2EnterpriseTask`
- `RecaptchaV2EnterpriseTaskProxyless`

If an invalid type is provided, raises `ValueError` with a message listing the available types.

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Uses [CaptchaTypeEnm](../api-contract/enums.md) for type validation
* Uses [ProxyTypeEnm](../api-contract/enums.md) for proxy type validation
* Uses [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for synchronous solving
* Uses [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for asynchronous solving

## Citations

[1] `src/python3_anticaptcha/recaptcha_v2.py` — Complete implementation.
[2] `src/python3_anticaptcha/core/enum.py:20-23` — Defines RecaptchaV2Task* enum values.
[3] `src/python3_anticaptcha/core/base.py:10` — Inherits from CaptchaParams.
[4] `README.md` — Contains usage examples for ReCaptchaV2.
[5] `https://anti-captcha.com/apidoc/task-types/RecaptchaV2TaskProxyless` — Official API documentation.
[6] `https://anti-captcha.com/apidoc/task-types/RecaptchaV2Task` — Official API documentation.
