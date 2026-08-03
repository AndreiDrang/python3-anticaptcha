---
type: Service Class
title: Control
description: Account management and reporting operations for AntiCaptcha service
resource: src/python3_anticaptcha/control.py
tags:
  - account
  - balance
  - reporting
  - statistics
---

# Control

The `Control` class provides account management, balance checking, and reporting functionality for the AntiCaptcha service. Unlike other captcha solver classes, Control does not solve captchas but provides administrative and monitoring capabilities.

## Overview

Control allows users to:
- Check account balance
- Get queue statistics
- Get application statistics
- Get spending statistics
- Report incorrect solutions
- Report correct solutions

## Constructor

```python
def __init__(self, api_key: str, *args, **kwargs):
```

**Parameters:**
- `api_key`: AntiCaptcha API key (required)
- `*args`, `**kwargs`: Additional parameters passed to parent class

## Balance Methods

### `get_balance() -> dict`

Retrieves the current account balance.

**Returns:**
```python
{
    "errorId": 0,
    "balance": 14.12396
}
```

**Citations:**
[1] `src/python3_anticaptcha/control.py:115-127` — Implementation.

### `aio_get_balance() -> dict`

Asynchronous version of `get_balance()`.

**Returns:**
- Same as `get_balance()`

**Citations:**
[1] `src/python3_anticaptcha/control.py:129-141` — Implementation.

## Queue Statistics Methods

### `get_queue_status(queue_id: int) -> dict` (static)

Gets statistics for a specific queue to determine the best time for submitting new tasks.

**Parameters:**
- `queue_id`: Identifier of the queue (e.g., 1 for English ImageToText)

**Returns:**
```python
{
    "waiting": 234,
    "load": 46.58,
    "bid": 0.000576,
    "speed": 8.43,
    "total": 438
}
```

**Fields:**
- `waiting`: Number of tasks waiting in queue
- `load`: Current load percentage
- `bid`: Current bid price
- `speed`: Tasks solved per minute
- `total`: Total tasks in queue

**Citations:**
[1] `src/python3_anticaptcha/control.py:143-163` — Implementation.

### `aio_get_queue_status(queue_id: int) -> dict` (static)

Asynchronous version of `get_queue_status()`.

**Citations:**
[1] `src/python3_anticaptcha/control.py:165-185` — Implementation.

## Spending Statistics Methods

### `get_spending_stats(**kwargs) -> dict`

Gets account spending and task volume statistics for a 24-hour period.

**Parameters:**
- `softId`: Application ID (default: 867)
- `queue`: Queue name (optional)
- Other kwargs passed as query parameters

**Returns:**
```python
{
    "errorId": 0,
    "data": [
        {
            "dateFrom": 1679183850,
            "dateTill": 1679187449,
            "volume": 0,
            "money": 0
        }
    ]
}
```

**Citations:**
[1] `src/python3_anticaptcha/control.py:187-229` — Implementation.

### `aio_get_spending_stats(**kwargs) -> dict`

Asynchronous version of `get_spending_stats()`.

**Citations:**
[1] `src/python3_anticaptcha/control.py:231-273` — Implementation.

## Application Statistics Methods

### `get_app_stats(softId: int, mode: Optional[str] = None) -> dict`

Gets daily statistics for a registered application.

**Parameters:**
- `softId`: Application ID (required)
- `mode`: Statistics mode ("views", "errors", etc.)

**Returns:**
```python
{
    "errorId": 0,
    "chartData": [...],
    "fromDate": "17 Feb 23:48",
    "toDate": "19 Mar 23:48"
}
```

**Citations:**
[1] `src/python3_anticaptcha/control.py:275-297` — Implementation.

### `aio_get_app_stats(softId: int, mode: Optional[str] = None) -> dict`

Asynchronous version of `get_app_stats()`.

**Citations:**
[1] `src/python3_anticaptcha/control.py:299-321` — Implementation.

## Reporting Methods

### `report_incorrect_image(taskId: int) -> dict`

Reports an incorrectly solved image captcha.

**Parameters:**
- `taskId`: The task ID that was solved incorrectly

**Returns:**
```python
{
    "errorId": 0,
    "status": "success"
}
```

**Citations:**
[1] `src/python3_anticaptcha/control.py:323-337` — Implementation.

### `aio_report_incorrect_image(taskId: int) -> dict`

Asynchronous version.

**Citations:**
[1] `src/python3_anticaptcha/control.py:339-351` — Implementation.

### `report_incorrect_recaptcha(taskId: int) -> dict`

Reports an incorrectly solved reCAPTCHA (v2, v3, or Enterprise).

**Citations:**
[1] `src/python3_anticaptcha/control.py:353-367` — Implementation.

### `aio_report_incorrect_recaptcha(taskId: int) -> dict`

Asynchronous version.

**Citations:**
[1] `src/python3_anticaptcha/control.py:369-383` — Implementation.

### `report_correct_recaptcha(taskId: int) -> dict`

Reports a correctly solved reCAPTCHA.

**Citations:**
[1] `src/python3_anticaptcha/control.py:385-399` — Implementation.

### `aio_report_correct_recaptcha(taskId: int) -> dict`

Asynchronous version.

**Citations:**
[1] `src/python3_anticaptcha/control.py:401-415` — Implementation.

### `report_incorrect_hcaptcha(taskId: int) -> dict`

Reports an incorrectly solved hCaptcha.

**Citations:**
[1] `src/python3_anticaptcha/control.py:417-431` — Implementation.

### `aio_report_incorrect_hcaptcha(taskId: int) -> dict`

Asynchronous version.

**Citations:**
[1] `src/python3_anticaptcha/control.py:433-447` — Implementation.

## Design Notes

- **Static Methods**: Queue status methods are static because they don't require authentication
- **Instance Methods**: Balance, stats, and reporting methods require the API key from the instance
- **Consistent Pattern**: Every synchronous method has an async counterpart with `aio_` prefix
- **Error Handling**: All methods return dictionaries with errorId and other fields

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Uses [ControlPostfixEnm](../api-contract/enums.md) for endpoint postfixes
* Uses [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for synchronous HTTP
* Uses [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for asynchronous HTTP

## Citations

[1] `src/python3_anticaptcha/control.py` — Complete implementation.
[2] `src/python3_anticaptcha/core/enum.py:58-70` — Defines ControlPostfixEnm values.
[3] `src/python3_anticaptcha/core/base.py:10` — Inherits from CaptchaParams.
[4] `https://anti-captcha.com/apidoc/methods/getBalance` — Official API documentation for getBalance.
[5] `https://anti-captcha.com/apidoc/methods/getQueueStats` — Official API documentation for getQueueStats.
[6] `https://anti-captcha.com/apidoc/methods/getSpendingStats` — Official API documentation for getSpendingStats.
[7] `https://anti-captcha.com/apidoc/methods/getAppStats` — Official API documentation for getAppStats.
