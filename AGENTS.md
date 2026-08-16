# AGENTS.md

## Repository overview

Python 3.9+ client library for the **AntiCaptcha** paid captcha-solving service. One
class per captcha type, each exposing a synchronous (`requests`) and an asynchronous
(`aiohttp`) handler. Serialization uses `msgspec`; package uses a `src/` layout;
all tooling runs through **uv**.

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
tests/                     # pytest + pytest-asyncio, HTTP fully mocked — see tests/AGENTS.md
docs/                      # Sphinx RST; docs/modules/<type>/example.rst per type
okf/                       # OKF v0.1 knowledge bundle — see okf/AGENTS.md
.github/workflows/         # 5 CI workflows: test, install, lint, build, sphinx
Makefile, pyproject.toml   # uv-based build / lint / test / format config
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

Read only when relevant:

- Architectural or cross-module changes → `ARCHITECTURE.md` (layer map, request flows, invariants)
- Adding or changing a captcha type → `src/python3_anticaptcha/AGENTS.md`
- Touching HTTP clients, serialization, enums, or base classes → `src/python3_anticaptcha/core/AGENTS.md`
- Writing or changing tests → `tests/AGENTS.md`
- Editing the knowledge bundle → `okf/AGENTS.md` (entry point: `okf/index.md`)
- Sphinx docs changes → `docs/` (per-type pages live at `docs/modules/<type>/example.rst`,
  registered in the `docs/index.rst` toctree)
- Usage/reference intent → `README.md` (note: its `from python3_anticaptcha import X`
  quick-start does **not** match `__init__.py`; import classes from their module — see below)

## Change rules (repo-wide invariants)

- **Type hints use `Union[X, Y]` / `Optional[X]`** — never PEP 604 `X | Y`. The library
  supports Python 3.9 (`requires-python = ">=3.9"`), where PEP 604 is not available.
- **Only `ValueError` is raised** (12 raise sites). Do not introduce other exception
  types without strong reason; there is no custom exception hierarchy.
- **Do not add re-exports to `src/python3_anticaptcha/__init__.py`** — it exports only
  `__version__`. Import public classes from their module, e.g.
  `from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2` (this is what the tests do).
- **`src/` layout**: run `uv sync` (or `make install`) before importing the package
  outside the uv-managed `.venv`; all repo commands run through uv.

## Validation

Run from the repo root (targets defined in `Makefile`; CI runs the same ones):

```bash
make install  # uv sync — create/refresh the .venv
make tests    # uv run --extra test: coverage run + pytest + html/xml reports
make lint     # ruff check + ruff format --check on src/ and tests/
make build    # uv build
make doc      # sphinx-build (docs/ → docs/_build)
make refactor # ruff check --fix + ruff format applied to src/ tests/
```

- Lint/format is **ruff** (`style` extra, pinned `0.16.*`): `line-length=120`,
  `target-version="py39"`, rules `F,E,W,I` — configured in `pyproject.toml`.
- Plain pytest needs the test extra: `uv run --extra test pytest` (`-k <name>` filters).
- CI test/lint matrix runs Python 3.12 only; the library itself supports 3.9–3.14.

## Repository-specific gotchas

- **`verify=False` is intentional.** `core/sio_captcha_instrument.py:32` sets
  `self.session.verify = False` for proxy support, and `urllib3.InsecureRequestWarning`
  is suppressed in both `config.py` and `core/const.py`. Do **not** "fix" this — see
  `src/python3_anticaptcha/core/AGENTS.md`.
- **No auto-publish.** `make upload` runs `uv build && uv publish` manually; there is no
  release automation in CI.
- **`msgspec` is pinned** `>=0.18,<0.22` (`pyproject.toml`). A newer msgspec may break
  the `Struct`-based serializers — check before bumping.
- **Duplicate `attempts_generator`** exists in both `config.py` and `core/utils.py`;
  the instruments import from `core/utils.py`. Edit the `core/utils.py` copy for retry
  behavior.

## Key docs

- `ARCHITECTURE.md` — canonical system map: layers, code map, request/data flows, invariants.
- `README.md` — supported types, usage examples (import style caveat noted above).
- `CONTRIBUTING.md` — fork → PR to `main`.
- `okf/index.md` — OKF v0.1 knowledge bundle navigation (concept-oriented docs).
- `docs/` — Sphinx source; `make doc` builds it.
