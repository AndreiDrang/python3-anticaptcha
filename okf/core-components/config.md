---
type: Configuration Module
title: Package Configuration
description: Package-level configuration and urllib3 warning suppression
resource: src/python3_anticaptcha/config.py
tags:
  - configuration
  - warnings
---

# Package Configuration

The `config.py` module at the package root contains package-level configuration settings and warning suppressions.

## Contents

### urllib3 Warning Suppression

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

This suppresses `InsecureRequestWarning` warnings that would otherwise be emitted when using `verify=False` in HTTP requests. This is intentional to support proxy configurations that may use self-signed certificates.

### Duplicate attempts_generator

```python
def attempts_generator(attempts: int = 5) -> Iterator[int]:
    for i in range(1, attempts + 1):
        yield i
```

**Note**: This is a duplicate of the function in `core/utils.py`. The instruments import from `core/utils.py` (which defaults to 30 attempts), making this version **unused/dead code**. The default of 5 here differs from the 30 in `core/utils.py`.

## Design Rationale

- **Warning Suppression**: The `verify=False` setting in [SIOCaptchaInstrument](../http-transport/sio-instrument.md) is intentional for proxy support. Suppressing the warning prevents noise in user applications.
- **Centralized Configuration**: Package-level settings that affect the entire library are placed here

## Relationships

* Suppresses warnings that would be triggered by [SIOCaptchaInstrument](../http-transport/sio-instrument.md)
* Contains duplicate of [attempts_generator](utils.md) (unused)

## Citations

[1] `src/python3_anticaptcha/config.py` — Package configuration module.
[2] `src/python3_anticaptcha/core/const.py:1` — Also suppresses InsecureRequestWarning.
[3] `src/python3_anticaptcha/core/sio_captcha_instrument.py:32` — Sets session.verify = False.
[4] `AGENTS.md` — Documents the duplicate attempts_generator issue and verify=False intent.
