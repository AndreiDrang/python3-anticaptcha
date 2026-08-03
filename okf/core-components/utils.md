---
type: Utility Module
title: Utilities
description: Polling loop generator and helper functions for the captcha solving workflow
tags:
  - utility
  - polling
  - retry
resource: src/python3_anticaptcha/core/utils.py
---

# Utilities

The `utils.py` module provides essential helper functions used throughout the library, most notably the polling loop generator.

## attempts_generator

```python
def attempts_generator(attempts: int = 30) -> Iterator[int]:
    """Generate a sequence of attempt numbers for polling loops."""
    for i in range(1, attempts + 1):
        yield i
```

### Purpose

Generates a sequence of attempt numbers used in the polling loop that waits for captcha solving results. The instrument classes use this to determine when to stop polling.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `attempts` | int | 30 | Maximum number of polling attempts |

### Returns

Iterator yielding integers from 1 to `attempts` (inclusive).

## Usage

The instruments import and use this generator in their `processing_captcha` methods:

```python
from core.utils import attempts_generator

for attempt in attempts_generator(self.captcha_params.sleep_time):
    # Poll for result
    result = self._get_result(task_id)
    if result.status != "processing":
        break
```

## Design Notes

- **Separation of Concerns**: The polling logic is centralized here rather than duplicated in each transport
- **Configurable**: The number of attempts can be adjusted, though 30 is the default
- **Lazy Evaluation**: Uses a generator to avoid creating the full list in memory

## Duplicate Note

There is a duplicate `attempts_generator` function in `config.py` at the package root. However, the instruments import from `core/utils.py`, making the `config.py` version effectively unused (dead code). The `core/utils.py` version is the authoritative one.

## Relationships

* Used by [SIOCaptchaInstrument](../http-transport/sio-instrument.md) in `processing_captcha` method
* Used by [AIOCaptchaInstrument](../http-transport/aio-instrument.md) in `processing_captcha` method

## Citations

[1] `src/python3_anticaptcha/core/utils.py:1-7` — Defines the attempts_generator function.
[2] `src/python3_anticaptcha/config.py:1-7` — Contains duplicate attempts_generator (unused).
[3] `src/python3_anticaptcha/core/sio_captcha_instrument.py:50` — Imports and uses attempts_generator.
[4] `src/python3_anticaptcha/core/aio_captcha_instrument.py:45` — Imports and uses attempts_generator.
[5] `AGENTS.md` — Documents the duplicate attempts_generator issue.
