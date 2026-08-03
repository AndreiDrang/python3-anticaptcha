---
type: Transport Base
title: Captcha Instrument
description: Base class for captcha solving instruments with file handling capabilities
resource: src/python3_anticaptcha/core/captcha_instrument.py
tags:
  - base-class
  - transport
  - file-handling
---

# Captcha Instrument

The `CaptchaInstrument` class and its `FileInstrument` parent provide the base functionality for captcha solving, including file handling operations that are shared between synchronous and asynchronous transports.

## Class Hierarchy

```
FileInstrument
└── CaptchaInstrument
    ├── SIOCaptchaInstrument
    └── AIOCaptchaInstrument
```

## FileInstrument

Static utility class for file operations related to captcha solving, particularly for image-based captchas.

### Methods

#### `_local_file_captcha(captcha_file: str) -> bytes`

Reads a local file and returns its contents as bytes.

**Parameters:**
- `captcha_file`: Path to the local captcha image file

**Returns:**
- File contents as bytes

**Citations:**
[1] `src/python3_anticaptcha/core/captcha_instrument.py:10-14` — Implementation.

#### `_file_const_saver(content: bytes, file_path: str, file_extension: str = "png") -> str`

Saves content to a file in the specified directory with a generated unique filename.

**Parameters:**
- `content`: Bytes to save
- `file_path`: Directory path for saving
- `file_extension`: File extension (default: "png")

**Returns:**
- Full path to the saved file

**Behavior:**
- Creates the directory if it doesn't exist
- Generates a unique filename using UUID
- Saves the content to the file

**Citations:**
[1] `src/python3_anticaptcha/core/captcha_instrument.py:17-30` — Implementation.

#### `_file_clean(full_file_path: str) -> None`

Deletes a file or directory.

**Parameters:**
- `full_file_path`: Path to the file or directory to delete

**Behavior:**
- Uses `shutil.rmtree` with `ignore_errors=True`
- Will delete directories recursively

**Citations:**
[1] `src/python3_anticaptcha/core/captcha_instrument.py:33-34` — Implementation.

## CaptchaInstrument

Base class for captcha solving instruments. Inherits from `FileInstrument` to gain file handling capabilities.

### Class Attributes

| Attribute | Type | Value | Description |
|-----------|------|-------|-------------|
| `NO_CAPTCHA_ERR` | str | "You did not send any file, local link or URL." | Error message for missing captcha input |

### Instance Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `result` | GetTaskResultResponseSer | Response struct for storing intermediate results |

### Constructor

```python
def __init__(self):
    self.result = GetTaskResultResponseSer()
```

Initializes the instrument with a default response struct.

## Design Rationale

- **Shared File Logic**: Image captcha handling (reading files, base64 encoding) is identical between sync and async, so it's centralized here
- **Error Constants**: Common error messages are defined at the base level
- **State Container**: The `result` attribute provides a place to store intermediate state during processing

## Relationships

* Inherits from `FileInstrument` for file operations
* Used as base by [SIOCaptchaInstrument](sio-instrument.md)
* Used as base by [AIOCaptchaInstrument](aio-instrument.md)
* Uses [GetTaskResultResponseSer](../api-contract/serializer.md) for result storage

## Citations

[1] `src/python3_anticaptcha/core/captcha_instrument.py` — Defines FileInstrument and CaptchaInstrument classes.
[2] `src/python3_anticaptcha/core/sio_captcha_instrument.py:10` — SIOCaptchaInstrument inherits from CaptchaInstrument.
[3] `src/python3_anticaptcha/core/aio_captcha_instrument.py:10` — AIOCaptchaInstrument inherits from CaptchaInstrument.
[4] `src/python3_anticaptcha/core/serializer.py:35` — Defines GetTaskResultResponseSer used by CaptchaInstrument.
