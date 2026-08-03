---
type: Utility Class
title: Context Managers
description: Session lifecycle management for synchronous and asynchronous HTTP operations
tags:
  - context-manager
  - session
  - lifecycle
resource: src/python3_anticaptcha/core/context_instr.py
---

# Context Managers

The context manager mixins provide session lifecycle management for HTTP operations, ensuring proper cleanup of resources in both synchronous and asynchronous contexts.

## Overview

Two mixin classes are defined in `context_instr.py`:
- `SIOContextManager` - for synchronous `requests.Session` management
- `AIOContextManager` - for asynchronous `aiohttp.ClientSession` management

These are used as mixins by `CaptchaParams` to provide `__enter__`/`__exit__` and `async with` support.

## SIOContextManager

Provides synchronous context manager protocol for `requests.Session` instances.

### Methods

#### `__enter__(self) -> SIOCaptchaInstrument`

Creates and returns a new `SIOCaptchaInstrument` instance when entering the context.

#### `__exit__(self, exc_type, exc_val, exc_tb) -> None`

Closes the session and cleans up resources when exiting the context.

## AIOContextManager

Provides asynchronous context manager protocol for `aiohttp.ClientSession` instances.

### Methods

#### `__aenter__(self) -> AIOCaptchaInstrument`

Creates and returns a new `AIOCaptchaInstrument` instance when entering the async context.

#### `__aexit__(self, exc_type, exc_val, exc_tb) -> None`

Closes the async session and cleans up resources when exiting the async context.

## Usage Pattern

```python
from python3_anticaptcha import ReCaptchaV2

# Synchronous context manager
with ReCaptchaV2(api_key="...", captcha_type="...") as solver:
    result = solver.captcha_handler()

# Asynchronous context manager
async with ReCaptchaV2(api_key="...", captcha_type="...") as solver:
    result = await solver.aio_captcha_handler()
```

## Design Rationale

- **Resource Safety**: Ensures HTTP sessions are properly closed even if exceptions occur
- **Transport Isolation**: Each context creates a fresh instrument instance, preventing session leakage between operations
- **Protocol Support**: Implements both sync (`__enter__`/`__exit__`) and async (`__aenter__`/`__aexit__`) protocols

## Relationships

* Used by [CaptchaParams](captcha-params.md) as mixin classes
* Creates instances of [SIOCaptchaInstrument](../http-transport/sio-instrument.md)
* Creates instances of [AIOCaptchaInstrument](../http-transport/aio-instrument.md)

## Citations

[1] `src/python3_anticaptcha/core/context_instr.py:1-20` — Defines SIOContextManager and AIOContextManager classes.
[2] `src/python3_anticaptcha/core/base.py:10` — CaptchaParams inherits from both context managers.
