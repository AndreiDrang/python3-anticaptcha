---
type: API Contract
title: Enumerations
description: All accepted string identifiers, captcha types, and status values for AntiCaptcha API
resource: src/python3_anticaptcha/core/enum.py
tags:
  - enumeration
  - captcha-types
  - api-contract
  - status
---

# Enumerations

The `enum.py` module defines all string-based enumerations used throughout the library. These enums serve as the **source of truth** for accepted values when communicating with the AntiCaptcha API.

## Base Enum Class

### MyEnum

```python
class MyEnum(Enum):
    @classmethod
    def list(cls) -> List[Enum]:
        return list(map(lambda c: c, cls))

    @classmethod
    def list_values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_names(cls) -> List[str]:
        return list(map(lambda c: c.name, cls))
```

Provides utility methods for working with enum values:
- `list()` - returns all enum members
- `list_values()` - returns all enum values as strings
- `list_names()` - returns all enum member names

## Endpoint Postfixes

### EndpointPostfixEnm

URL postfixes for API endpoints.

| Member | Value | Description |
|--------|-------|-------------|
| `CREATE_TASK` | "createTask" | Endpoint for creating new tasks |
| `GET_TASK_RESULT` | "getTaskResult" | Endpoint for retrieving task results |

## Captcha Types

### CaptchaTypeEnm

All supported captcha task types. This is the **source of truth** for valid `captcha_type` values.

#### reCAPTCHA
| Member | Value | Description |
|--------|-------|-------------|
| `RecaptchaV2Task` | "RecaptchaV2Task" | reCAPTCHA v2 with proxy |
| `RecaptchaV2TaskProxyless` | "RecaptchaV2TaskProxyless" | reCAPTCHA v2 without proxy |
| `RecaptchaV3TaskProxyless` | "RecaptchaV3TaskProxyless" | reCAPTCHA v3 |
| `RecaptchaV2EnterpriseTask` | "RecaptchaV2EnterpriseTask" | reCAPTCHA v2 Enterprise with proxy |
| `RecaptchaV2EnterpriseTaskProxyless` | "RecaptchaV2EnterpriseTaskProxyless" | reCAPTCHA v2 Enterprise without proxy |

#### FunCaptcha
| Member | Value | Description |
|--------|-------|-------------|
| `FunCaptchaTask` | "FunCaptchaTask" | FunCaptcha with proxy |
| `FunCaptchaTaskProxyless` | "FunCaptchaTaskProxyless" | FunCaptcha without proxy |

#### GeeTest
| Member | Value | Description |
|--------|-------|-------------|
| `GeeTestTask` | "GeeTestTask" | GeeTest with proxy |
| `GeeTestTaskProxyless` | "GeeTestTaskProxyless" | GeeTest without proxy |

#### hCaptcha
| Member | Value | Description |
|--------|-------|-------------|
| `HCaptchaTask` | "HCaptchaTask" | hCaptcha with proxy |
| `HCaptchaTaskProxyless` | "HCaptchaTaskProxyless" | hCaptcha without proxy |

#### Turnstile
| Member | Value | Description |
|--------|-------|-------------|
| `TurnstileTask` | "TurnstileTask" | Turnstile with proxy |
| `TurnstileTaskProxyless` | "TurnstileTaskProxyless" | Turnstile without proxy |

#### FriendlyCaptcha
| Member | Value | Description |
|--------|-------|-------------|
| `FriendlyCaptchaTask` | "FriendlyCaptchaTask" | FriendlyCaptcha with proxy |
| `FriendlyCaptchaTaskProxyless` | "FriendlyCaptchaTaskProxyless" | FriendlyCaptcha without proxy |

#### Prosopo
| Member | Value | Description |
|--------|-------|-------------|
| `ProsopoTask` | "ProsopoTask" | Prosopo with proxy |
| `ProsopoTaskProxyless` | "ProsopoTaskProxyless" | Prosopo without proxy |

#### Amazon WAF
| Member | Value | Description |
|--------|-------|-------------|
| `AmazonTask` | "AmazonTask" | Amazon WAF with proxy |
| `AmazonTaskProxyless` | "AmazonTaskProxyless" | Amazon WAF without proxy |

#### Altcha
| Member | Value | Description |
|--------|-------|-------------|
| `AltchaTask` | "AltchaTask" | Altcha with proxy |
| `AltchaTaskProxyless` | "AltchaTaskProxyless" | Altcha without proxy |

#### Image Captchas
| Member | Value | Description |
|--------|-------|-------------|
| `ImageToTextTask` | "ImageToTextTask" | Text from image captcha |
| `ImageToCoordinatesTask` | "ImageToCoordinatesTask" | Click coordinates captcha |

#### Custom
| Member | Value | Description |
|--------|-------|-------------|
| `Control` | "Control" | Custom control tasks |
| `AntiGateTask` | "AntiGateTask" | AntiGate task type |

## Response Status

### ResponseStatusEnm

Task processing status values.

| Member | Value | Description |
|--------|-------|-------------|
| `processing` | "processing" | Task is still being processed |
| `ready` | "ready" | Task is complete; solution is available |
| `error` | "error" | Task failed |

## Proxy Types

### ProxyTypeEnm

Supported proxy protocol types.

| Member | Value | Description |
|--------|-------|-------------|
| `http` | "http" | HTTP/HTTPS proxy |
| `https` | "https" | HTTPS proxy |
| `socks4` | "socks4" | SOCKS4 proxy |
| `socks5` | "socks5" | SOCKS5 proxy |

## Control Methods

### ControlPostfixEnm

URL postfixes for control/account methods.

| Member | Value | Description |
|--------|-------|-------------|
| `GET_BALANCE` | "getBalance" | Get account balance |
| `GET_QUEUE_STATS` | "getQueueStats" | Get queue statistics |
| `GET_APP_STATS` | "getAppStats" | Get application statistics |
| `GET_SPENDING_STATS` | "getSpendingStats" | Get spending statistics |
| `REPORT_INCORRECT_IMAGE_CAPTCHA` | "reportIncorrectImageCaptcha" | Report incorrect image captcha |
| `REPORT_INCORRECT_RECAPTCHA` | "reportIncorrectRecaptcha" | Report incorrect reCAPTCHA |
| `REPORT_CORRECT_RECAPTCHA` | "reportCorrectRecaptcha" | Report correct reCAPTCHA |
| `REPORT_INCORRECT_HCAPTCHA` | "reportIncorrectHcaptcha" | Report incorrect hCaptcha |

## Save Formats

### SaveFormatsEnm

Image save format options for image captcha types.

| Member | Value | Description |
|--------|-------|-------------|
| `TEMP` | "temp" | Temporary file (deleted after solving) |
| `CONST` | "const" | Persistent file (kept after solving) |

## Design Principles

- **Single Source of Truth**: All captcha type strings are defined here; handlers validate against these values
- **String Enums**: Inherit from both `str` and `MyEnum` for string-like behavior
- **Validation**: Handlers raise `ValueError` for unknown captcha_type values
- **Extensibility**: New captcha types can be added by extending the enum

## Relationships

* Used by all captcha handler classes (e.g., [ReCaptchaV2](../captcha-types/recaptcha-v2.md)) for type validation
* Used by [Serializer](serializer.md) for type hints (e.g., ResponseStatusEnm)
* Used by [Control](../captcha-types/control.md) for control method postfixes
* Referenced in [AGENTS.md](../AGENTS.md) as the source of truth for captcha types

## Citations

[1] `src/python3_anticaptcha/core/enum.py` — Defines all enumeration classes.
[2] `src/python3_anticaptcha/recaptcha_v2.py:80` — Validates captcha_type against CaptchaTypeEnm values.
[3] `src/python3_anticaptcha/core/serializer.py:15` — Uses ResponseStatusEnm in GetTaskResultResponseSer.
[4] `AGENTS.md` — States that CaptchaTypeEnm is the source of truth for accepted captcha_type strings.
