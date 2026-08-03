# AGENTS.md

## Repository overview

Python 3.9+ client library for the **AntiCaptcha** paid captcha-solving service. One
class per captcha type, each exposing a synchronous (`requests`) and an asynchronous
(`aiohttp`) handler. Serialization uses `msgspec`; package uses a `src/` layout.

- Version: `src/python3_anticaptcha/__version__.py` (single source of truth).
- API key: read from the `API_KEY` env var or passed as `api_key=` to each handler.
- Base URL and retry config live in `src/python3_anticaptcha/core/const.py`
  (`BASE_REQUEST_URL`, `RETRIES`, `ASYNC_RETRIES`) — **not** in `config.py`.

## Where to work

```text
src/python3_anticaptcha/   # the library — see src/python3_anticaptcha/AGENTS.md
├── core/                  # shared infra (base, enums, serializer, HTTP) — see core/AGENTS.md
├── config.py              # attempts_generator + urllib3 warning suppression (small)
├── __version__.py         # version string
└── <captcha_type>.py      # one module per captcha type
tests/                     # pytest + pytest-asyncio — see tests/AGENTS.md
docs/                      # Sphinx RST docs (docs/modules/<type>.rst per type)
.github/workflows/         # 5 CI workflows: test, install, lint, build, sphinx
Makefile, pyproject.toml   # build / lint / test / format config
```

## Architecture and boundaries

- Each captcha type is a class inheriting `CaptchaParams` (`core/base.py`).
- Every class exposes `captcha_handler()` (sync) and `aio_captcha_handler()` (async);
  both return a `dict` (built from msgspec structs in `core/serializer.py`).
- Sync path = `requests` session; async path = `aiohttp` session. The two HTTP
  instruments must stay in lockstep (same endpoints, same request/response shapes).
- Accepted `captcha_type` strings are enumerated in `CaptchaTypeEnm` (`core/enum.py`) —
  the enum is the source of truth.

## Context routing

Read the relevant file before editing:

- Adding or changing a captcha type → `src/python3_anticaptcha/AGENTS.md`
- Touching HTTP clients, serialization, enums, or base classes → `src/python3_anticaptcha/core/AGENTS.md`
- Writing or changing tests → `tests/AGENTS.md`
- Editing docs → `docs/` (Sphinx RST; each type has a `docs/modules/<name>.rst`)
- Usage/reference intent → `README.md` (note: its `from python3_anticaptcha import X`
  quick-start does **not** match `__init__.py`; import classes from their module — see below)

## Change rules (repo-wide invariants)

- **Type hints use `Union[X, Y]` / `Optional[X]`** — never PEP 604 `X | Y`. This is the
  established convention across every module.
- **Only `ValueError` is raised** (12 raise sites). Do not introduce other exception
  types without strong reason; there is no custom exception hierarchy.
- **Do not add re-exports to `src/python3_anticaptcha/__init__.py`** — it exports only
  `__version__`. Import public classes from their module, e.g.
  `from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2` (this is what the tests do).
- **`src/` layout**: run `pip install -e .` (or `make install`) before importing the
  package outside the installed environment.

## Validation

Run from the repo root (defined in `Makefile`):

```bash
make tests    # coverage run + pytest + reports (html/xml)
make lint     # autoflake + black + isort --check on src/
make build    # python3 -m build
make doc      # sphinx-build (cd docs && make html)
make refactor # autoflake + black + isort applied to src/ tests/ (format/fix)
```

- Lint config: black `line-length=120`, `target-version=['py310']`; isort `profile=black`,
  `length_sort=true` (`pyproject.toml`).
- Tests: `asyncio_mode=auto` (no `@pytest.mark.asyncio` needed); `pytest -k <name>` to filter.

## Repository-specific gotchas

- **`verify=False` is intentional.** `core/sio_captcha_instrument.py:32` sets
  `self.session.verify = False` for proxy support, and `urllib3.InsecureRequestWarning`
  is suppressed in both `config.py` and `core/const.py`. Do **not** "fix" this — see
  `src/python3_anticaptcha/core/AGENTS.md`.
- **No auto-publish.** `make upload` runs `twine upload dist/*` manually; there is no
  release automation in CI.
- **`msgspec` is pinned** `>=0.18,<0.22` (`pyproject.toml`). A newer msgspec may break
  the `Struct`-based serializers — check before bumping.
- **Duplicate `attempts_generator`** exists in both `config.py` and `core/utils.py`;
  the instruments import from `core/utils.py`. Edit the `core/utils.py` copy for retry
  behavior.

## Key docs

- `README.md` — supported types, usage examples (import style caveat noted above).
- `CONTRIBUTING.md` — fork → PR to `main`.
- `docs/` — Sphinx source; `make doc` builds it.
