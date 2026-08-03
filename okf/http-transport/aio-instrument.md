---
type: HTTP Transport
title: AIO Captcha Instrument
description: Asynchronous HTTP client for AntiCaptcha API using aiohttp library
resource: src/python3_anticaptcha/core/aio_captcha_instrument.py
tags:
  - asynchronous
  - aiohttp
  - http-client
  - transport
---

# AIO Captcha Instrument

The asynchronous HTTP transport implementation using the `aiohttp` library. This instrument handles all communication with the AntiCaptcha API for asynchronous captcha solving operations.

## Overview

`AIOCaptchaInstrument` (AIO = Asynchronous I/O) provides the asynchronous implementation of the captcha solving workflow:
1. Create a task
2. Poll for results until complete
3. Return the solution

It uses `aiohttp.ClientSession` with async retry configuration for each request.

## Constructor

```python
async def __init__(self, captcha_params: "CaptchaParams"):
    super().__init__()
    self.captcha_params = captcha_params
```

**Parameters:**
- `captcha_params`: The [CaptchaParams](../core-components/captcha-params.md) instance containing solver configuration

**Initialization:**
- Calls parent constructor
- Stores captcha_params reference
- Note: Does NOT create a session in the constructor (sessions are created per-request)

## Main Methods

### `processing_captcha() -> dict`

Orchestrates the complete asynchronous captcha solving workflow.

**Workflow:**
1. Merges task_params into the create_task_payload
2. Awaits `_create_task()` to submit the captcha
3. If successful (errorId == 0), stores the taskId
4. Awaits asyncio.sleep for `sleep_time` seconds
5. Awaits `_get_result()` to poll for the solution
6. Returns the result as a dictionary

**Returns:**
- Dictionary with full server response

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:20-32` — Implementation.

### `processing_image_captcha(...) -> dict`

Handles image-based captcha solving with file processing asynchronously.

**Parameters:**
- `save_format`: How to save downloaded images (TEMP or CONST)
- `img_clearing`: Whether to delete files after solving
- `captcha_link`: URL to a captcha image
- `captcha_file`: Path to a local captcha image file
- `captcha_base64`: Base64-encoded captcha image
- `img_path`: Directory path for saving images

**Workflow:**
1. Awaits `__body_file_processing()` to handle the image source
2. If successful, delegates to `processing_captcha()`
3. Returns the result

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:34-44` — Implementation.

## Internal Methods

### `_create_task(url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer`

Submits a new captcha solving task to the AntiCaptcha API asynchronously.

**Parameters:**
- `url_postfix`: URL postfix for the endpoint (default: CREATE_TASK_POSTFIX)

**Returns:**
- CreateTaskResponseSer struct with task creation response

**Behavior:**
- Creates a new `aiohttp.ClientSession` for this request
- POSTs the payload to `BASE_REQUEST_URL + url_postfix`
- Returns parsed response as CreateTaskResponseSer
- Raises ValueError on HTTP errors

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:75-85` — Implementation.

### `_get_result(url_response: str = GET_RESULT_POSTFIX) -> dict`

Polls for captcha solving results until the task is complete asynchronously.

**Parameters:**
- `url_response`: URL postfix for the endpoint (default: GET_RESULT_POSTFIX)

**Returns:**
- Dictionary with full task result

**Behavior:**
- Uses `attempts_generator()` for polling loop (default 30 attempts)
- Creates a new `aiohttp.ClientSession` for each request
- POSTs to `BASE_REQUEST_URL + url_response` with taskId
- If status is "processing", awaits asyncio.sleep for `sleep_time` and continues
- If status is "ready" or "error", adds taskId to result and returns
- Note: Unlike sync version, this does NOT close a persistent session (each request has its own)

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:87-104` — Implementation.
[2] `src/python3_anticaptcha/core/utils.py` — Provides attempts_generator.

### `__body_file_processing(...) -> None`

Processes image captcha file sources asynchronously (local file, base64, or URL).

**Parameters:**
- Various parameters for file handling (see processing_image_captcha)

**Behavior:**
- For local file: reads file synchronously (blocking), base64-encodes, adds to task body
- For base64: encodes bytes, adds to task body
- For URL: downloads via `_url_read()`, optionally saves, base64-encodes, adds to task body
- Sets error on result struct if no valid source provided

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:46-68` — Implementation.

### `_url_read(url: str, **kwargs) -> bytes`

Downloads content from a URL asynchronously.

**Parameters:**
- `url`: URL to download
- `**kwargs`: Additional arguments passed to session.get()

**Returns:**
- Bytes of the downloaded content

**Behavior:**
- Creates a new `aiohttp.ClientSession`
- Uses ASYNC_RETRIES for retry logic via tenacity
- Returns the content bytes

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:106-113` — Implementation.
[2] `src/python3_anticaptcha/core/const.py` — Provides ASYNC_RETRIES.

## Static Methods

### `send_post_request(payload, url_postfix) -> dict`

Static method for sending a POST request to the AntiCaptcha API asynchronously.

**Parameters:**
- `payload`: Request payload as dictionary
- `url_postfix`: URL postfix for the endpoint

**Returns:**
- Dictionary with JSON response

**Citations:**
[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py:115-127` — Implementation.

## Design Notes

- **Per-Request Sessions**: Unlike the sync version, this creates a new `aiohttp.ClientSession` for each request. This is because aiohttp sessions are not designed for long-lived reuse in the same way as requests sessions.
- **Async Retry**: Uses ASYNC_RETRIES from [constants](../api-contract/constants.md) for async retry with tenacity
- **Blocking File I/O**: Local file reading is synchronous (blocking) within async context. This is a known limitation but acceptable for typical file sizes.
- **Lockstep with Sync**: This must stay in sync with [SIOCaptchaInstrument](sio-instrument.md) in terms of endpoints and request/response shapes

## Key Differences from SIOCaptchaInstrument

| Aspect | SIOCaptchaInstrument | AIOCaptchaInstrument |
|--------|---------------------|---------------------|
| Library | requests | aiohttp |
| Session Lifecycle | Persistent session (created in __init__) | Per-request sessions |
| Retry | requests.adapters.Retry | tenacity.AsyncRetrying |
| Sleep | time.sleep | asyncio.sleep |
| File Reading | Synchronous | Synchronous (blocking in async) |
| URL Joining | urllib.parse.urljoin | urllib.parse.urljoin |

## Relationships

* Inherits from [CaptchaInstrument](captcha-instrument.md)
* Uses [aiohttp](https://docs.aiohttp.org/) library for HTTP
* Uses [ASYNC_RETRIES](../api-contract/constants.md) for async retry configuration
* Uses [BASE_REQUEST_URL](../api-contract/constants.md) for base API URL
* Uses [attempts_generator](../core-components/utils.md) for polling loop
* Used by [CaptchaParams](../core-components/captcha-params.md) for asynchronous operations

## Citations

[1] `src/python3_anticaptcha/core/aio_captcha_instrument.py` — Complete implementation.
[2] `src/python3_anticaptcha/core/const.py` — Provides constants used by the instrument.
[3] `src/python3_anticaptcha/core/base.py:49` — CaptchaParams.aio_captcha_handler creates AIOCaptchaInstrument.
[4] `AGENTS.md` — States that sync and async transports must stay in lockstep.
