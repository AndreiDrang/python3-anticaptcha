# AGENTS.md

## Scope and inheritance

Applies to: `tests/`. Inherits repo-wide guidance from `../AGENTS.md`.

## What lives here

```text
tests/
├── conftest.py            # BaseTest class + delay fixtures
├── test_<module>.py       # one test module per source module
└── __init__.py
```

There is **no** `tests/static/` directory and no shared response fixture file. Mocking is
done inline with `pytest-mock` (`mocker.patch` / `mocker.spy`); no tests make real API calls.

## Conventions

- `asyncio_mode = auto` (`pyproject.toml`) — async test functions run without
  `@pytest.mark.asyncio`.
- Test classes inherit `BaseTest` from `tests.conftest`:
  ```python
  from tests.conftest import BaseTest


  class TestReCaptchaV2(BaseTest): ...
  ```
  `BaseTest` provides `API_KEY` (env or mock default), `sleep_time`, `get_proxy_args()`,
  `get_random_string()`, `read_file()`, and the `delay_func` / `delay_class` fixtures.
- Naming: class `Test<Type>`; methods `test_sio_*` (sync) / `test_aio_*` (async).
- Import classes from their module, not the package root:
  `from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2`.
- Avoid real network: spy on the context managers from `core.context_instr`
  (`SIOContextManager.__enter__`, `AIOContextManager.__aenter__`) and patch the instruments.
- Validate returned dicts against `GetTaskResultResponseSer` from `core.serializer`.

## Validation

```bash
make tests              # coverage run + pytest + html/xml reports (from repo root)
pytest                  # plain run
pytest -k recaptcha     # filter by name
```

Coverage is configured in `.coveragerc` (includes `*/src/*`, omits `__init__` and tests).
