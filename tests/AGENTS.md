# AGENTS.md

## Scope and inheritance

Applies to: `tests/`. Inherits repo-wide guidance from `../AGENTS.md`.

## What lives here

```text
tests/
├── conftest.py            # BaseTest + root HTTP-fixture exports
├── core/
│   ├── conftest.py        # sync/async transport fakes and response builders
│   └── test_<module>.py   # one test module per core source module
├── test_<module>.py       # one test module per top-level source module
└── __init__.py
```

There is **no** `tests/static/` directory. Transport fakes and deterministic response builders
live in `tests/core/conftest.py`; no tests make real API calls.

## Conventions

- `asyncio_mode = auto` (`pyproject.toml`) — async test functions run without
  `@pytest.mark.asyncio`.
- Test classes inherit `BaseTest` from `tests.conftest`:
  ```python
  from tests.conftest import BaseTest


  class TestReCaptchaV2(BaseTest): ...
  ```
  `BaseTest` provides `API_KEY` (env or mock default), `sleep_time`, `get_proxy_args()`,
  `get_random_string()`, and `read_file()`. It intentionally has no delay fixtures.
- Naming: class `Test<Type>`; methods describe observable behavior. Async tests use
  `async def` without `@pytest.mark.asyncio`.
- Import classes from their module, not the package root:
  `from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2`.
- Never make real network calls. Use `sio_http` / `aio_http`; they patch only the HTTP
  transport, allowing payload assembly, serialization, and polling to run for real.
- Assert exact returned fields and request URL/JSON payloads; avoid truthiness-only assertions.


## Validation

```bash
make tests              # coverage run + pytest + html/xml reports (from repo root)
pytest                  # plain run
pytest -k recaptcha     # filter by name
```

Coverage is configured in `.coveragerc` (includes `*/src/*`, omits `__init__` and tests).
