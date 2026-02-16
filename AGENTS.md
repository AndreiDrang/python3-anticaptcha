# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-15
**Commit:** 3a0e55c
**Branch:** master

## OVERVIEW
Python client for AntiCaptcha service API. Supports 12 captcha types with sync/async handlers using msgspec for serialization.

## STRUCTURE
```
python3-anticaptcha/
├── src/python3_anticaptcha/    # Main package
│   ├── core/                   # Shared: base classes, enums, serializer
│   ├── recaptcha_v2.py         # Individual captcha modules
│   ├── recaptcha_v3.py
│   └── ...                     # 10 more captcha types
├── tests/                      # pytest + asyncio
├── docs/                       # Sphinx documentation
├── Makefile                    # Build/test/lint commands
└── .github/workflows/          # 5 CI workflows (test, install, lint, build, sphinx)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Add new captcha type | `src/python3_anticaptcha/` | Copy existing module pattern |
| Base classes | `core/base.py` | CaptchaParams, CaptchaResponse |
| Enums | `core/enum.py` | CaptchaTypeEnm, ProxyTypeEnm, ResponseStatusEnm |
| HTTP handling | `core/captcha_instrument.py` | SynchronousInstrument, AsyncInstrument |
| Serialization | `core/serializer.py` | msgspec.Struct base |
| Config | `config.py` | API key, urls |
| Tests | `tests/` | pytest-asyncio, mock server |
| CI | `.github/workflows/` | 5 separate workflows |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| ReCaptchaV2 | Class | recaptcha_v2.py | Google reCAPTCHA v2 |
| ReCaptchaV3 | Class | recaptcha_v3.py | Google reCAPTCHA v3 |
| ImageToText | Class | image_to_text.py | Text from image |
| FunCaptcha | Class | funcaptcha.py | Arkose Labs |
| GeeTest | Class | geetest.py | GeeTest captcha |
| Turnstile | Class | turnstile.py | Cloudflare Turnstile |
| FriendlyCaptcha | Class | friendly_captcha.py | FriendlyCaptcha |
| Prosopo | Class | prosopo.py | Prosopo captcha |
| AmazonWAF | Class | amazon_waf.py | Amazon WAF captcha |
| CustomTask | Class | custom_task.py | Custom task template |
| Control | Class | control.py | Balance/status |
| CaptchaParams | Base | core/base.py | Parent for all params |
| CaptchaResponse | Base | core/base.py | Parent for responses |
| SynchronousInstrument | Class | core/captcha_instrument.py | Sync HTTP client |
| AsyncInstrument | Class | core/captcha_instrument.py | Async HTTP client |

## CONVENTIONS
- **Format**: Black + isort (120 char, py310 target)
- **Imports**: isort with black profile, length_sort
- **Docstrings**: Google-style (Args/Returns/Examples/Notes)
- **Serialization**: msgspec.Struct with type annotations
- **Type hints**: Union[X,Y], Optional[X] syntax (not |)
- **Async**: All captcha classes have `captcha_handler()` sync + `aio_captcha_handler()` async

## ANTI-PATTERNS (THIS PROJECT)
- **SSL**: `verify=False` in captcha_instrument.py:32 - INTENTIONAL for proxy support, suppresses urllib3 warnings
- **apiDomain**: DO NOT use in ReCaptcha - deprecated by AntiCaptcha
- **Proxy restrictions**: Never use hostnames, transparent proxies, local networks (192.*.*, 10.*.*, 127.*.*)
- **Exceptions**: Only ValueError raised - no custom exception hierarchy
- **Bare except**: Used in some cleanup - avoid expanding
- **Type hints**: Use `Union[X,Y]`, `Optional[X]` - NOT `X | Y` (py310+ syntax forbidden)
- **msgspec version**: Pinned <0.21 in pyproject.toml - may need updates for newer versions

## COMMANDS
```bash
make tests          # pytest + coverage
make lint           # autoflake/black/isort --check
make build          # python3 -m build
make doc            # sphinx-build
make upload         # twine upload dist/*
```

## NOTES
- API_KEY required as env var or constructor param
- Tests use mock server (tests.static.responses)
- Manual PyPI upload (make upload) - no auto-publish
- Docs deploy only on release branch
