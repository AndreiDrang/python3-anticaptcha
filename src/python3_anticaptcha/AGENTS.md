# python3_anticaptcha Package

## OVERVIEW
Main package - 12 captcha handler classes with sync/async API.

## STRUCTURE
```
python3_anticaptcha/
├── __init__.py          # Exports version only
├── config.py            # API URLs, key handling
├── core/                # Shared utilities (see core/AGENTS.md)
├── recaptcha_v2.py      # Captcha type modules
├── recaptcha_v3.py
├── image_to_text.py
├── funcaptcha.py
├── geetest.py
├── turnstile.py
├── friendly_captcha.py
├── prosopo.py
├── amazon_waf.py
├── custom_task.py
└── control.py
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Add captcha type | Copy existing module, register in CaptchaTypeEnm |
| Modify HTTP client | `core/captcha_instrument.py` |
| Change serialization | `core/serializer.py` |
| Add enum | `core/enum.py` |

## CONVENTIONS
- Each captcha module: one class with `captcha_handler()` + `aio_captcha_handler()`
- Inherit from `CaptchaParams` (core/base.py)
- Params passed as constructor kwargs
- Return `CaptchaResponse` subclass

## ANTI-PATTERNS
- Don't add to `__init__.py` exports - users import directly
- Don't modify core enums without updating all handlers
