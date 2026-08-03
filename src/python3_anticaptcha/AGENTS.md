# AGENTS.md

## Scope and inheritance

Applies to: `src/python3_anticaptcha/` (the library package).

Inherits repo-wide guidance from `../../AGENTS.md`. This file defines only the
captcha-class contract and local naming rules.

## What lives here

```text
python3_anticaptcha/
├── __init__.py            # exports ONLY __version__ — do not add re-exports here
├── __version__.py         # version string (single source of truth)
├── config.py              # attempts_generator + urllib3 warning suppression
├── core/                  # shared infra — see core/AGENTS.md
└── <type>.py              # one module per captcha type (see map below)
```

Captcha-type modules and their classes (file→class names are intentionally irregular):

| File | Class |
|------|-------|
| `recaptcha_v2.py` | `ReCaptchaV2` |
| `recaptcha_v3.py` | `ReCaptchaV3` |
| `image_to_text.py` | `ImageToText` |
| `image_to_coordinates.py` | `ImageToCoordinates` |
| `fun_captcha.py` | `FunCaptcha` |
| `gee_test.py` | `GeeTest` |
| `turnstile.py` | `Turnstile` |
| `friendly_captcha.py` | `FriendlyCaptcha` |
| `prosopo_captcha.py` | `Prosopo` |
| `amazon_waf.py` | `AmazonWAF` |
| `altcha.py` | `Altcha` |
| `custom_task.py` | `CustomTask` |
| `control.py` | `Control` (balance / task status, not a captcha solver) |

## The captcha-class contract

- Inherit `CaptchaParams` from `core/base.py`.
- Constructor takes `api_key`, `captcha_type` (a `CaptchaTypeEnm` value or string),
  type-specific params, and `sleep_time: int = 10`.
- Expose **both** `captcha_handler()` (sync) and `aio_captcha_handler()` (async).
  Both return a `dict` — there is no `CaptchaResponse` base class; responses are
  msgspec structs in `core/serializer.py`.
- Each module defines `__all__ = ("<ClassName>",)`.

## Adding a new captcha type

1. Copy the closest existing module (e.g. `turnstile.py`) and rename the class.
2. Add the new value(s) to `CaptchaTypeEnm` (and `EndpointPostfixEnm` if a new endpoint
   is needed) in `core/enum.py` — the enum is the source of truth for accepted strings.
3. If new request/response fields are needed, extend the msgspec structs in
   `core/serializer.py` (do not bypass it).
4. Add `tests/test_<type>.py` mirroring an existing test (see `tests/AGENTS.md`).
5. Add `docs/modules/<type>.rst`.

## Safe change rules

- Do **not** edit HTTP clients or serializers directly here — those live in `core/`
  (see `core/AGENTS.md`); changes there affect every handler.
- Keep sync and async handlers symmetric: same params, same return shape.
- Follow repo type-hint and exception conventions from the root `AGENTS.md`
  (`Union`/`Optional`, `ValueError` only).
