---
type: Captcha Solver
title: CustomTask
description: Custom task type solver for AntiCaptcha
resource: src/python3_anticaptcha/custom_task.py
tags:
  - custom
  - task
  - generic
---

# CustomTask

Solver class for custom task types not covered by specialized classes.

## Overview

CustomTask provides a generic interface for working with custom captcha types or new task types that haven't been explicitly implemented in the library yet.

## Constructor

```python
def __init__(
    self,
    api_key: str,
    captcha_type: Union[CaptchaTypeEnm, str],
    sleep_time: int = 10,
    **kwargs
):
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | Yes | - | AntiCaptcha API key |
| `captcha_type` | CaptchaTypeEnm or str | Yes | - | Custom task type identifier |
| `sleep_time` | int | No | 10 | Seconds between polling attempts |
| `**kwargs` | dict | No | - | Additional task parameters passed to task body |

## Task Parameters

The `task_params` are constructed from the `**kwargs` passed to the constructor:

```python
{
    "type": captcha_type,
    **kwargs
}
```

## Usage Example

```python
from python3_anticaptcha import CustomTask

# Use a custom task type
result = CustomTask(
    api_key="YOUR_API_KEY",
    captcha_type="CustomTaskType",
    customParam1="value1",
    customParam2="value2"
).captcha_handler()
```

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Most flexible solver - can handle any task type supported by AntiCaptcha

## Citations

[1] `src/python3_anticaptcha/custom_task.py` — Complete implementation.
