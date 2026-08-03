---
type: HTTP Transport
title: SIO Captcha Instrument
description: Synchronous HTTP client for AntiCaptcha API using requests library
resource: src/python3_anticaptcha/core/sio_captcha_instrument.py
tags:
  - synchronous
  - requests
  - http-client
  - transport
---

# SIO Captcha Instrument

The synchronous HTTP transport implementation using the `requests` library. This instrument handles all communication with the AntiCaptcha API for synchronous captcha solving operations.

## Overview

`SIOCaptchaInstrument` (SIO = Synchronous I/O) provides the synchronous implementation of the captcha solving workflow:
1. Create a task
2. Poll for results until complete
3. Return the solution

It uses `requests.Session` with retry configuration and TLS verification disabled for proxy support.

## Constructor

```python
def __init__(self, captcha_params: "CaptchaParams"):
    super().__init__()
    self.captcha_params = captcha_params
    self.session = requests.Session()
    self.session.mount("http://", HTTPAdapter(max_retries=RETRIES))
    self.session.mount("https://", HTTPAdapter(max_retries=RETRIES))
    self.session.verify = False
```

**Parameters:**
- `captcha_params`: The [CaptchaParams](../core-components/captcha-params.md) instance containing solver configuration

**Initialization:**
- Creates a `requests.Session` instance
- Mounts HTTP adapters with retry configuration for both http:// and https://
- **Sets `session.verify = False`** - This is intentional for proxy support (see [AGENTS.md](../../AGENTS.md))

## Main Methods

### `processing_captcha() -> dict`

Orchestrates the complete synchronous captcha solving workflow.

**Workflow:**
1. Merges task_params into the create_task_payload
2. Calls `_create_task()` to submit the captcha
3. If successful (errorId == 0), stores the taskId
4. Sleeps for `sleep_time` seconds
5. Calls `_get_result()` to poll for the solution
6. Returns the result as a dictionary

**Returns:**
- Dictionary with full server response

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:28-40` — Implementation.

### `processing_image_captcha(...) -> dict`

Handles image-based captcha solving with file processing.

**Parameters:**
- `save_format`: How to save downloaded images (TEMP or CONST)
- `img_clearing`: Whether to delete files after solving
- `captcha_link`: URL to a captcha image
- `captcha_file`: Path to a local captcha image file
- `captcha_base64`: Base64-encoded captcha image
- `img_path`: Directory path for saving images

**Workflow:**
1. Calls `__body_file_processing()` to handle the image source
2. If successful, delegates to `processing_captcha()`
3. Returns the result

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:42-52` — Implementation.

## Internal Methods

### `_create_task(url_postfix: str = CREATE_TASK_POSTFIX) -> CreateTaskResponseSer`

Submits a new captcha solving task to the AntiCaptcha API.

**Parameters:**
- `url_postfix`: URL postfix for the endpoint (default: CREATE_TASK_POSTFIX)

**Returns:**
- CreateTaskResponseSer struct with task creation response

**Behavior:**
- POSTs the payload to `BASE_REQUEST_URL + url_postfix`
- Returns parsed response as CreateTaskResponseSer
- Raises ValueError on HTTP errors

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:77-87` — Implementation.

### `_get_result(url_response: str = GET_RESULT_POSTFIX) -> dict`

Polls for captcha solving results until the task is complete.

**Parameters:**
- `url_response`: URL postfix for the endpoint (default: GET_RESULT_POSTFIX)

**Returns:**
- Dictionary with full task result

**Behavior:**
- Uses `attempts_generator()` for polling loop (default 30 attempts)
- POSTs to `BASE_REQUEST_URL + url_response` with taskId
- If status is "processing", sleeps for `sleep_time` and continues
- If status is "ready" or "error", closes session and returns
- Closes session on any error

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:95-109` — Implementation.
[2] `src/python3_anticaptcha/core/utils.py` — Provides attempts_generator.

### `__body_file_processing(...) -> None`

Processes image captcha file sources (local file, base64, or URL).

**Parameters:**
- Various parameters for file handling (see processing_image_captcha)

**Behavior:**
- For local file: reads file, base64-encodes, adds to task body
- For base64: encodes bytes, adds to task body
- For URL: downloads via `_url_read()`, optionally saves, base64-encodes, adds to task body
- Sets error on result struct if no valid source provided

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:54-75` — Implementation.

### `_url_read(url: str, **kwargs) -> requests.Response`

Downloads content from a URL using the configured session.

**Parameters:**
- `url`: URL to download
- `**kwargs`: Additional arguments passed to session.get()

**Returns:**
- requests.Response object

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:89-92` — Implementation.

## Static Methods

### `send_post_request(payload, session, url_postfix) -> dict`

Static method for sending a POST request to the AntiCaptcha API.

**Parameters:**
- `payload`: Request payload as dictionary
- `session`: requests.Session instance to use
- `url_postfix`: URL postfix for the endpoint

**Returns:**
- Dictionary with JSON response

**Citations:**
[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py:111-122` — Implementation.

## Design Notes

- **Session Reuse**: The session is created once in the constructor and reused for all requests in a solving operation
- **Retry Configuration**: Uses RETRIES from [constants](../api-contract/constants.md) for automatic retry on server errors
- **TLS Verification Disabled**: `session.verify = False` is intentional for proxy support
- **Lockstep with Async**: This must stay in sync with [AIOCaptchaInstrument](aio-instrument.md) in terms of endpoints and request/response shapes

## Relationships

* Inherits from [CaptchaInstrument](captcha-instrument.md)
* Uses [requests](https://docs.python-requests.org/) library for HTTP
* Uses [RETRIES](../api-contract/constants.md) for retry configuration
* Uses [BASE_REQUEST_URL](../api-contract/constants.md) for base API URL
* Uses [attempts_generator](../core-components/utils.md) for polling loop
* Used by [CaptchaParams](../core-components/captcha-params.md) for synchronous operations

## Citations

[1] `src/python3_anticaptcha/core/sio_captcha_instrument.py` — Complete implementation.
[2] `src/python3_anticaptcha/core/const.py` — Provides constants used by the instrument.
[3] `AGENTS.md` — Documents that verify=False is intentional for proxy support.
[4] `src/python3_anticaptcha/core/base.py:36` — CaptchaParams.captcha_handler creates SIOCaptchaInstrument.
