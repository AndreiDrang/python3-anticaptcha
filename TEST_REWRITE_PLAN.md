# Test Suite Rewrite Plan

Status: **Implemented**

## Goals

- Remove all live AntiCaptcha API calls from the default test suite.
- Mock only external HTTP transport (`requests.Session` and `aiohttp.ClientSession`).
- Assert observable request URLs, JSON payloads, parsed responses, state transitions, and file effects.
- Mirror the source structure with dedicated `tests/core/` coverage.
- Keep sync and async behavior in lockstep.
- Remove artificial test delays and credential dependencies.

## Initial audit

The previous suite contained 109 test functions / 162 collected cases. Approximately 40
cases made live API calls, causing hangs and failures without a valid `API_KEY`. Existing
tests also used `sleep(1)` and `sleep(2)` fixtures for every test, mocked
`processing_captcha` instead of HTTP, and often asserted only truthiness or dictionary type.
Core serializers, file handling, contexts, retry utilities, and HTTP state machines lacked
dedicated tests. `friendly_captcha.py` and `prosopo_captcha.py` had no tests.

## Implementation phases

### Phase 1: test scaffolding and core coverage

- Replaced delayed fixtures in `tests/conftest.py` with a fixed, obviously fake API key.
- Added `tests/core/conftest.py` with deterministic sync/async transport fakes, response
  builders, FIFO response queues, and no-op sleep patches.
- Added dedicated tests for:
  - serializers and wire defaults;
  - enums and endpoint constants;
  - retry generators and retry configuration;
  - sync/async context managers;
  - file and captcha instruments;
  - `CaptchaParams` delegation and callback URLs;
  - sync/async create-task and result-polling state machines.
- Updated `tests/AGENTS.md` with the new mirrored structure and no-live-network rule.

### Phase 2: captcha-module tests

Rewrote the module tests to cover constructor payload assembly, accepted and rejected captcha
types, proxy-field passthrough, optional fields, exact image payload encoding, and selected
sync/async handler flows for:

- Altcha;
- Amazon WAF;
- CustomTask;
- FunCaptcha;
- GeeTest;
- ImageToText;
- ImageToCoordinates;
- ReCaptcha V2;
- ReCaptcha V3;
- Turnstile.

Added new coverage for FriendlyCaptcha and Prosopo. Removed the obsolete flat `test_core.py`
after moving its useful assertions into `tests/core/`.

### Phase 3: Control endpoint tests

Rewrote `tests/test_control.py` to cover all eight Control endpoint families in sync and
async forms. Each test asserts the exact endpoint postfix, client key, task/queue/statistics
payload, and returned response instead of making an account-dependent API call.

## Production defects found and fixed by boundary tests

1. `SIOCaptchaInstrument._get_result` did not return on terminal `ready` or error responses,
   resulting in all 29 polling attempts even when the first response was terminal. It now
   returns immediately and only retries while processing.
2. `FileInstrument._file_clean` used `shutil.rmtree` for the file path returned by
   `_file_const_saver`. It now removes either a file or a directory tree, making
   `img_clearing=True` effective.

## Validation

- `pytest tests/`: **203 passed** in under one second.
- `make tests`: passed with **99.825% coverage** (573 statements, one defensive fallback line
  uncovered).
- `ruff check src tests`: passed.
- `ruff format --check src tests`: passed.
- No live API calls, real credentials, or generated artifacts are required by the suite.
