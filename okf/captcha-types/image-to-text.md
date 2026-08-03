---
type: Captcha Solver
title: ImageToText
description: Image-based captcha solver for text extraction from images
resource: src/python3_anticaptcha/image_to_text.py
tags:
  - image
  - captcha
  - ocr
  - text-extraction
---

# ImageToText

Solver class for image-based captchas where the solution is text extracted from an image. This includes classic "type the text you see" captchas.

## Overview

ImageToText handles captchas that present an image containing distorted text. AntiCaptcha workers view the image and type the text they see. The solver supports three input methods:
1. Local file path
2. URL to an image
3. Base64-encoded image bytes

## Constructor

```python
def __init__(
    self,
    api_key: str,
    captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.ImageToTextTask,
    sleep_time: int = 5,
    save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
    img_clearing: bool = True,
    img_path: str = "PythonAntiCaptchaImages",
):
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | Yes | - | AntiCaptcha API key |
| `captcha_type` | CaptchaTypeEnm or str | No | ImageToTextTask | Type of image captcha task |
| `sleep_time` | int | No | 5 | Seconds between polling attempts (shorter than default) |
| `save_format` | SaveFormatsEnm or str | No | TEMP | How to handle downloaded images |
| `img_clearing` | bool | No | True | Whether to delete files after solving |
| `img_path` | str | No | "PythonAntiCaptchaImages" | Directory for saving images |

### Save Format Options

| Value | Behavior |
|-------|----------|
| `SaveFormatsEnm.TEMP` or "temp" | Temporary file, deleted after solving |
| `SaveFormatsEnm.CONST` or "const" | Persistent file, kept after solving |

## Task Parameters

```python
{
    "type": captcha_type
}
```

The actual image data is passed separately to the handler methods, not in the constructor.

## Handler Methods

### `captcha_handler(captcha_link, captcha_file, captcha_base64, **additional_params) -> dict`

Synchronous method for solving image captchas.

**Parameters:**
- `captcha_link`: URL to a captcha image
- `captcha_file`: Path to a local captcha image file
- `captcha_base64`: Base64-encoded captcha image bytes
- `**additional_params`: Additional task parameters

**Returns:**
- Dictionary with full server response

**Behavior:**
- Exactly one of captcha_link, captcha_file, or captcha_base64 must be provided
- Image is read/encoded as base64 and added to task body
- Delegates to SIOCaptchaInstrument.processing_image_captcha()

**Citations:**
[1] `src/python3_anticaptcha/image_to_text.py:60-80` — Implementation.

### `aio_captcha_handler(captcha_link, captcha_file, captcha_base64, **additional_params) -> dict`

Asynchronous method for solving image captchas.

**Parameters:**
- Same as `captcha_handler`

**Returns:**
- Dictionary with full server response

**Behavior:**
- Same as synchronous version but uses async transport
- Delegates to AIOCaptchaInstrument.processing_image_captcha()

**Citations:**
[1] `src/python3_anticaptcha/image_to_text.py:82-102` — Implementation.

## Response Format

Successful response includes:
```python
{
    "errorId": 0,
    "status": "ready",
    "solution": {
        "text": "qGphJD",
        "url": "http://69.65.31.125/986/172815194092195.jpg"
    },
    "cost": 0.002,
    "ip": "46.53.249.230",
    "createTime": 1679004358,
    "endTime": 1679004368,
    "solveCount": 0,
    "taskId": 396687629
}
```

The `text` field contains the extracted text solution.

## Usage Examples

### From Local File
```python
from python3_anticaptcha import ImageToText
from python3_anticaptcha.core.enum import SaveFormatsEnm

result = ImageToText(
    api_key="YOUR_API_KEY",
    save_format=SaveFormatsEnm.CONST
).captcha_handler(captcha_file="files/captcha-image.jpg")

print(result["solution"]["text"])
```

### From URL
```python
from python3_anticaptcha import ImageToText

result = ImageToText(
    api_key="YOUR_API_KEY"
).captcha_handler(captcha_link="https://example.com/captcha-image.jpg")

print(result["solution"]["text"])
```

### From Base64
```python
from python3_anticaptcha import ImageToText
import base64

# Read image and encode
with open("captcha.png", "rb") as f:
    image_bytes = f.read()

result = ImageToText(
    api_key="YOUR_API_KEY"
).captcha_handler(captcha_base64=image_bytes)

print(result["solution"]["text"])
```

### Async from URL
```python
import asyncio
from python3_anticaptcha import ImageToText

async def solve():
    result = await ImageToText(
        api_key="YOUR_API_KEY"
    ).aio_captcha_handler(captcha_link="https://example.com/captcha-image.jpg")
    return result

result = asyncio.run(solve())
```

## File Handling

### Local File Processing
1. File is read as bytes using `_local_file_captcha()`
2. Bytes are base64-encoded
3. Encoded string is added to task body as `"body"`

### URL Processing
1. Image is downloaded via `_url_read()` (GET request)
2. If `save_format == CONST`, image is saved to `img_path` directory
3. If `img_clearing == True`, saved file is deleted after encoding
4. Bytes are base64-encoded
5. Encoded string is added to task body as `"body"`

### Base64 Processing
1. Bytes are base64-encoded
2. Encoded string is added to task body as `"body"`

## Design Notes

- **Shorter sleep_time**: Default is 5 seconds (vs 10-15 for token captchas) since image solving is typically faster
- **File Cleanup**: Temporary files are automatically cleaned up by default
- **Flexible Input**: Supports three input methods for maximum flexibility
- **Persistent Files**: Use `SaveFormatsEnm.CONST` to keep downloaded images for debugging

## Relationships

* Inherits from [CaptchaParams](../core-components/captcha-params.md)
* Uses [SaveFormatsEnm](../api-contract/enums.md) for save format options
* Uses [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for synchronous file processing
* Uses [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for asynchronous file processing

## Citations

[1] `src/python3_anticaptcha/image_to_text.py` — Complete implementation.
[2] `src/python3_anticaptcha/core/enum.py:30` — Defines ImageToTextTask and SaveFormatsEnm.
[3] `src/python3_anticaptcha/core/base.py:10` — Inherits from CaptchaParams.
[4] `src/python3_anticaptcha/core/captcha_instrument.py:10` — FileInstrument provides file handling.
[5] `https://anti-captcha.com/apidoc/task-types/ImageToTextTask` — Official API documentation.
