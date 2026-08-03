---
type: Base Class
title: CaptchaParams
description: Base class for all captcha solver classes in python3-anticaptcha
tags:
  - base-class
  - captcha
  - handler
resource: src/python3_anticaptcha/core/base.py
---

# CaptchaParams

The `CaptchaParams` class is the abstract base class that all captcha solver classes inherit from. It provides the common interface and shared functionality for both synchronous and asynchronous captcha solving.

## Overview

`CaptchaParams` extends both `SIOContextManager` and `AIOContextManager` to provide context management capabilities for both sync and async HTTP sessions. It encapsulates the common parameters and methods needed to interact with the AntiCaptcha API.

## Key Responsibilities

- Initialize and manage API client key
- Configure sleep/polling intervals
- Prepare task creation payloads
- Prepare task result retrieval parameters
- Dispatch to appropriate HTTP transport (sync or async)

## Class Hierarchy

```
CaptchaParams(SIOContextManager, AIOContextManager)
├── ReCaptchaV2
├── ReCaptchaV3
├── ImageToText
├── ImageToCoordinates
├── FunCaptcha
├── GeeTest
├── Turnstile
├── FriendlyCaptcha
├── HCaptcha
├── Prosopo
├── AmazonWAF
├── Altcha
└── CustomTask
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | AntiCaptcha API key |
| `sleep_time` | int | 15 | Seconds between result poll requests |

## Public Methods

### `captcha_handler(**additional_params) -> dict`

Synchronous method for captcha solving. Creates a `SIOCaptchaInstrument` instance and processes the captcha through the synchronous transport.

**Parameters:**
- `additional_params`: Additional parameters passed to the task payload under the `task` key

**Returns:**
- Dictionary with full server response

### `aio_captcha_handler(**additional_params) -> dict`

Asynchronous method for captcha solving. Creates an `AIOCaptchaInstrument` instance and processes the captcha through the asynchronous transport.

**Parameters:**
- `additional_params`: Additional parameters passed to the task payload under the `task` key

**Returns:**
- Dictionary with full server response

### `set_callback_url(callbackUrl: str) -> None`

Sets an optional callback URL where captcha results can be sent via AJAX POST request.

**Parameters:**
- `callbackUrl`: Web address for receiving results

## Instance Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `sleep_time` | int | Polling interval in seconds |
| `create_task_payload` | CreateTaskBaseSer | Payload for task creation requests |
| `task_params` | dict | Task-specific parameters for the `task` body |
| `get_result_params` | GetTaskResultRequestSer | Payload for result retrieval requests |
| `_captcha_handling_instrument` | CaptchaInstrument | The transport instrument (sync or async) |

## Design Principles

- **Single Responsibility**: Each captcha type subclass is responsible only for assembling its specific `task_params`
- **Transport Agnostic**: The base class doesn't know which transport (sync/async) will be used; it's determined at call time
- **Payload Separation**: Task creation payload and result retrieval payload are kept separate for clarity

## Relationships

* Inherits from [SIOContextManager](context-managers.md) for synchronous session management
* Inherits from [AIOContextManager](context-managers.md) for asynchronous session management
* Uses [CreateTaskBaseSer](../api-contract/serializer.md) for task creation payload structure
* Uses [GetTaskResultRequestSer](../api-contract/serializer.md) for result retrieval payload structure
* Instantiates [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for synchronous operations
* Instantiates [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for asynchronous operations

## Citations

[1] `src/python3_anticaptcha/core/base.py` — Defines the CaptchaParams class and its methods.
[2] `src/python3_anticaptcha/core/serializer.py` — Defines CreateTaskBaseSer and GetTaskResultRequestSer structs.
[3] `src/python3_anticaptcha/core/context_instr.py` — Defines SIOContextManager and AIOContextManager mixins.
