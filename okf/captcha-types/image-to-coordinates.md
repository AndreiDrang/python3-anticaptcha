---
type: Captcha Solver
title: ImageToCoordinates
description: Image-based captcha solver for coordinate selection challenges
resource: src/python3_anticaptcha/image_to_coordinates.py
tags:
  - image
  - captcha
  - coordinates
  - click
---

# ImageToCoordinates

Solver class for image-based captchas where the solution requires clicking on specific coordinates in an image.

## Overview

ImageToCoordinates handles captchas that present an image and require the user to click on specific areas (e.g., "click on all images containing cars"). AntiCaptcha workers view the image and click on the appropriate coordinates.

## Supported Types

| Captcha Type | Description | Proxy Support |
|--------------|-------------|---------------|
| `ImageToCoordinatesTask` | Coordinate selection with proxy | Yes |
| `ImageToCoordinatesTaskProxyless` | Coordinate selection without proxy | No |

## Constructor

```python
def __init__(
    self,
    api_key: str,
    captcha_type: Union[CaptchaTypeEnm, str] = CaptchaTypeEnm.ImageToCoordinatesTask,
    sleep_time: int = 5,
    save_format: Union[str, SaveFormatsEnm] = SaveFormatsEnm.TEMP,
    img_clearing: bool = True,
    img_path: str = "PythonAntiCaptchaImages",
    **kwargs
):
```

## Handler Methods

### `captcha_handler(captcha_link, captcha_file, captcha_base64, **additional_params) -> dict`

Synchronous method for solving coordinate captchas. Supports the same three input methods as ImageToText.

### `aio_captcha_handler(captcha_link, captcha_file, captcha_base64, **additional_params) -> dict`

Asynchronous version.

## Response Format

```python
{
    "errorId": 0,
    "status": "ready",
    "solution": {
        "coordinates": [
            {"x": 100, "y": 200},
            {"x": 300, "y": 400}
        ]
    },
    "cost": 0.002,
    "ip": "46.53.249.230",
    "createTime": 1679004358,
    "endTime": 1679004368,
    "solveCount": 0,
    "taskId": 396687629
}
```

The `coordinates` array contains the x,y positions that should be clicked.

## Relationships

* Inherits from [ImageToText](../captcha-types/image-to-text.md) (shares file handling logic)
* Uses [CaptchaTypeEnm](../api-contract/enums.md) for type validation

## Citations

[1] `src/python3_anticaptcha/image_to_coordinates.py` — Complete implementation.
[2] `https://anti-captcha.com/apidoc/task-types/ImageToCoordinatesTask` — Official API documentation.
