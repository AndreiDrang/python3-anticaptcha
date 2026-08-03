# AGENTS.md

## Scope and inheritance

Applies to: `src/python3_anticaptcha/core/` (shared infrastructure).

Inherits from `../AGENTS.md` (package) and `../../../AGENTS.md` (repo). This file
defines only the core-subsystem contract.

## What lives here

```text
core/
├── base.py                    # CaptchaParams — parent of all captcha param classes
├── enum.py                    # CaptchaTypeEnm, ProxyTypeEnm, ResponseStatusEnm,
│                              #   EndpointPostfixEnm, ControlPostfixEnm, SaveFormatsEnm (all subclass MyEnum)
├── serializer.py              # msgspec structs: request/response serializers
├── const.py                   # BASE_REQUEST_URL, endpoint postfixes, RETRIES, ASYNC_RETRIES, APP_KEY
├── utils.py                   # attempts_generator (retry/poll loop)
├── captcha_instrument.py      # FileInstrument + CaptchaInstrument (shared base)
├── sio_captcha_instrument.py  # SIOCaptchaInstrument — SYNC, requests session
├── aio_captcha_instrument.py  # AIOCaptchaInstrument — ASYNC, aiohttp session
└── context_instr.py           # SIOContextManager / AIOContextManager wrap the instruments
```

Note: there is **no** `CaptchaResponse` class. `base.py` declares only `CaptchaParams`,
whose handler stubs are annotated `-> dict`. Response shapes are msgspec structs in
`serializer.py` (`BaseAPIResponseSer`, `CreateTaskResponseSer`, `GetTaskResultResponseSer`, …).

## Local boundaries and invariants

- **HTTP is split across three instrument files** (not one):
  - `captcha_instrument.py` — `FileInstrument` (file/body prep) and shared `CaptchaInstrument`.
  - `sio_captcha_instrument.py` — `SIOCaptchaInstrument`, the **sync** `requests` client.
  - `aio_captcha_instrument.py` — `AIOCaptchaInstrument`, the **async** `aiohttp` client.
  The sync and async clients must stay in lockstep: same endpoints (`CREATE_TASK_POSTFIX`,
  `GET_RESULT_POSTFIX`), same request/response shapes. A change to one usually requires the other.
- **API URLs and retry config live in `const.py`**, not in top-level `config.py`:
  `BASE_REQUEST_URL`, `RETRIES` (`requests` `Retry`), `ASYNC_RETRIES` (tenacity `AsyncRetrying`).
- **Enums are the source of truth** for accepted `captcha_type` / `proxyType` strings.
  Adding a `CaptchaTypeEnm` member requires the matching handler support; do not add enum
  values in isolation.
- **`context_instr.py`** owns session lifecycle (`SIOContextManager.__enter__/__exit__`,
  `AIOContextManager.__aenter__/__aexit__`). Tests spy on these to avoid real network I/O.

## Safe change rules

- **`verify=False` at `sio_captcha_instrument.py:32` is intentional** (proxy support).
  `urllib3.InsecureRequestWarning` is suppressed in both `config.py` and `const.py`.
  Do not "fix" it, and do not re-enable warnings.
- When changing a serializer struct, every handler that builds or parses that struct may
  be affected — check call sites in the sibling captcha modules.
- Retry/backoff tuning belongs in `const.py` (`RETRIES`, `ASYNC_RETRIES`).

## Validation

Repo-wide commands live in the root `AGENTS.md`. To target this subsystem:

```bash
pytest tests/test_core.py
```
