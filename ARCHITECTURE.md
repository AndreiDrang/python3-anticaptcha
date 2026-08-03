# Architecture

## 1. High-Level Overview

This repository is a Python 3.9+ client library (SDK) for the AntiCaptcha paid
captcha-solving HTTP service. It is distributed as the `python3-anticaptcha` package
built from a `src/` layout (`pyproject.toml`), and exposes one class per supported
captcha type, each offering both a synchronous and an asynchronous solving entrypoint.

The architecture is a thin public handler layer over a shared `core/` substrate. Each
handler class is a `CaptchaParams` subclass that assembles a task payload; all HTTP
transport, serialization, retry, and polling logic is centralized in
`src/python3_anticaptcha/core/` and reused by every type (`AGENTS.md`,
`src/python3_anticaptcha/AGENTS.md`). The defining structural feature is a dual transport
— `requests` for sync, `aiohttp` for async — that must stay in lockstep against a single
shared wire contract (`core/serializer.py`, `core/enum.py`, `core/const.py`).

External runtime dependencies are limited to four (`pyproject.toml`): `requests`,
`aiohttp`, `msgspec` (serialization), and `tenacity` (async retry). There is no local
persistence, server runtime, or background worker — the library is a stateless
request/response client. Version is a single source of truth in
`src/python3_anticaptcha/__version__.py`.

## 2. System Architecture (Logical)

Dependency direction (handlers depend on `core/`; `core/` never depends on handlers):

```
 <type>.py, control.py  ──►  core/base.py  ──►  core/{sio,aio}_captcha_instrument.py
        │                        │
        └────►  core/enum.py, core/serializer.py, core/const.py   (wire contract)
```

### Handler layer (public API)

- Responsibility: one class per captcha type; assemble the `task` payload from
  constructor args and expose sync/async solving entrypoints. `control.py` provides
  account/balance/reporting calls instead of solving.
- Code locations: `src/python3_anticaptcha/*.py` (e.g. `recaptcha_v2.py`, `turnstile.py`,
  `image_to_text.py`, `control.py`).
- Entry points: `captcha_handler()` (sync) and `aio_captcha_handler()` (async), both
  `-> dict`; `control.py` exposes `get_balance()`/`report_*()` plus `aio_` mirrors.
- Depends on: `core/` only (`base`, `enum`, serializer indirectly via base).
- Must not depend on: other handler modules — no handler imports another handler.
- Owns: per-type `task_params` construction and `captcha_type` validation.
- Evidence: `src/python3_anticaptcha/AGENTS.md`; grep of `from .core` across all handler
  modules confirms the only intra-package imports point into `core/`.

### Wire-contract layer

- Responsibility: define the AntiCaptcha API request/response shapes and the set of
  accepted string identifiers (captcha types, endpoint postfixes, proxy types, statuses).
- Code locations: `core/serializer.py` (msgspec `Struct`s: `CreateTaskBaseSer`,
  `CreateTaskResponseSer`, `GetTaskResultRequestSer`, `GetTaskResultResponseSer`),
  `core/enum.py` (`CaptchaTypeEnm`, `ControlPostfixEnm`, `EndpointPostfixEnm`,
  `ProxyTypeEnm`, `ResponseStatusEnm`, `SaveFormatsEnm`), `core/const.py`
  (`BASE_REQUEST_URL`, endpoint postfixes, `APP_KEY`).
- Depends on: nothing within the package (only `msgspec` + stdlib).
- Owns: the source of truth for accepted `captcha_type` strings and the serialized API
  envelope. There is no `CaptchaResponse` base class — responses are msgspec structs.
- Evidence: `core/AGENTS.md`; `core/serializer.py`; `core/enum.py`.

### Dual HTTP transport layer

- Responsibility: send `createTask`, poll `getTaskResult`, and (for image types)
  fetch/encode payload bytes. Split into a shared base plus two parallel clients.
- Code locations: `core/captcha_instrument.py` (`FileInstrument` + shared
  `CaptchaInstrument`), `core/sio_captcha_instrument.py` (sync, `requests`),
  `core/aio_captcha_instrument.py` (async, `aiohttp`).
- Depends on: the wire-contract layer (`serializer`, `enum`, `const`) and
  `core/utils.py` (`attempts_generator` polling loop).
- Owns: session creation, retry/backoff, create+poll orchestration, file/base64 body
  preparation, and the shared `send_post_request` helpers used by `control.py`.
- State and external boundaries: outbound HTTPS to `BASE_REQUEST_URL`
  (`api.anti-captcha.com`). `SIOCaptchaInstrument` holds a persistent `requests.Session`
  with a mounted `Retry` adapter and `verify=False`; `AIOCaptchaInstrument` opens a fresh
  `aiohttp.ClientSession` per request. Inferred: the sync/async session lifecycles are
  asymmetric and must be reconciled if retry semantics change.
- Evidence: `core/sio_captcha_instrument.py`; `core/aio_captcha_instrument.py`;
  `core/AGENTS.md`.

### Params base & session lifecycle

- Responsibility: the `CaptchaParams` base class every handler inherits, plus the
  context-manager mix-ins tests rely on for network isolation.
- Code locations: `core/base.py` (`CaptchaParams`, `captcha_handler`/
  `aio_captcha_handler` dispatch), `core/context_instr.py` (`SIOContextManager`,
  `AIOContextManager`).
- Depends on: serializer (`CreateTaskBaseSer`, `GetTaskResultRequestSer`) and the
  transport instruments.
- Owns: `create_task_payload`, `get_result_params`, `task_params`, `sleep_time`. The
  sync-vs-async dispatch lives here, not in each handler module.
- Evidence: `core/base.py`; `core/context_instr.py`.

## 3. Code Map (Physical)

```
python3-anticaptcha/
├── src/python3_anticaptcha/        # the library (src/ layout)
│   ├── __init__.py                 # exports ONLY __version__ — no re-exports
│   ├── __version__.py              # version string (single source of truth)
│   ├── config.py                   # duplicate attempts_generator + urllib3 warning suppress (see §5)
│   ├── <type>.py  ×12              # one handler module per captcha type (ReCaptchaV2, Turnstile, …)
│   ├── control.py                  # account/balance/reporting (not a solver)
│   └── core/                       # shared substrate — see core/AGENTS.md
│       ├── base.py                 # CaptchaParams — parent of all handlers
│       ├── enum.py                 # CaptchaTypeEnm + postfix/proxy/status enums (source of truth)
│       ├── serializer.py           # msgspec Structs for request/response envelopes
│       ├── const.py                # BASE_REQUEST_URL, endpoint postfixes, RETRIES, ASYNC_RETRIES, APP_KEY
│       ├── utils.py                # attempts_generator — the poll loop actually used by instruments
│       ├── captcha_instrument.py   # FileInstrument + shared CaptchaInstrument
│       ├── sio_captcha_instrument.py   # SYNC client (requests)
│       ├── aio_captcha_instrument.py   # ASYNC client (aiohttp)
│       └── context_instr.py        # SIO/AIO context-manager mix-ins (session lifecycle)
├── tests/                          # pytest + pytest-asyncio; one test_<module>.py per source module
├── docs/                           # Sphinx RST; docs/modules/<type> per type (make doc)
├── pyproject.toml                  # setuptools build, black/isort/pytest config, runtime deps
├── Makefile                        # install/tests/refactor/lint/build/doc/upload targets
└── .github/workflows/              # test, install, lint, build, sphinx (release → gh-pages)
```

## 4. Life of a Request / Primary Data Flow

### Captcha solve flow (token types, e.g. ReCaptchaV2 / Turnstile)

1. Trigger: caller constructs a handler and invokes `captcha_handler()` (or
   `await aio_captcha_handler()`).
2. Entry point: type module (e.g. `recaptcha_v2.py`) builds `task_params`; dispatch is in
   `core/base.py:CaptchaParams.captcha_handler`.
3. Coordination: `base.py` instantiates `SIOCaptchaInstrument` (sync) /
   `AIOCaptchaInstrument` (async) and merges `task_params` into `create_task_payload.task`.
4. Core processing: instrument POSTs `createTask` → on `errorId == 0` stores `taskId`,
   sleeps `sleep_time`, then loops `attempts_generator()` polling `getTaskResult` until
   `status != processing`.
5. Persistence / external interaction: HTTPS to `api.anti-captcha.com` (`core/const.py`);
   responses parsed into msgspec structs (`CreateTaskResponseSer`,
   `GetTaskResultResponseSer`).
6. Output: a `dict` (struct `.to_dict()`).

Architectural boundaries crossed: handler → base → transport → wire-contract → network.
The async path mirrors this exactly through `aio_captcha_instrument.py`
(`asyncio.sleep`, per-request `aiohttp.ClientSession`).

Evidence: `core/base.py`; `core/sio_captcha_instrument.py:processing_captcha` /
`_create_task` / `_get_result`; `core/aio_captcha_instrument.py`.

### Image captcha flow (ImageToText / ImageToCoordinates)

1. Trigger: caller invokes `captcha_handler(captcha_file=...)` /
   `(captcha_link=...)` / `(captcha_base64=...)`.
2. Entry point: `image_to_text.py` routes to the instrument's
   `processing_image_captcha`.
3. Coordination: `SIOCaptchaInstrument.processing_image_captcha` →
   `__body_file_processing`.
4. Core processing: `FileInstrument._local_file_captcha` / `_url_read` reads bytes →
   base64-encodes into `task["body"]`; optionally persists the downloaded image
   (`_file_const_saver`).
5. External interaction: for `captcha_link`, an extra GET fetches the image before the
   standard solve flow above.
6. Output: delegates to the standard solve flow, returning a `dict`.

Architectural boundaries crossed: handler → transport (file-prep branch reuses the same
create+poll path).

Evidence: `core/captcha_instrument.py:FileInstrument`;
`core/sio_captcha_instrument.py:processing_image_captcha` / `__body_file_processing`.

## 5. Architectural Invariants & Constraints

- Rule: One module per captcha type, each a `CaptchaParams` subclass exposing both
  `captcha_handler()` (sync) and `aio_captcha_handler()` (async), both returning `dict`.
- Rationale: uniform public contract across all solver types.
- Enforcement / Signals: convention + `src/python3_anticaptcha/AGENTS.md`; verified by
  grep that every handler imports `CaptchaParams` from `core/base.py`.

- Rule: Sync (`requests`) and async (`aiohttp`) transports must stay in lockstep — same
  endpoints (`CREATE_TASK_POSTFIX`, `GET_RESULT_POSTFIX`), same request/response shapes.
- Rationale: a single shared wire contract (`core/serializer.py`, `core/const.py`) backs
  both clients.
- Enforcement / Signals: convention documented in `core/AGENTS.md`; no test asserts
  parity.

- Rule: Dependency direction is handlers → `core/`; `core/` never imports a sibling
  handler module.
- Rationale: keeps the substrate reusable and prevents type-specific leakage into shared
  code.
- Enforcement / Signals: grep confirms `core/` contains no imports of any
  `python3_anticaptcha.<type>` module or sibling handler.

- Rule: Accepted `captcha_type` / `proxyType` / endpoint strings are enumerated in
  `core/enum.py`; the enum is the source of truth.
- Rationale: handlers validate `captcha_type` against `CaptchaTypeEnm` and `raise
  ValueError` for unknown values.
- Enforcement / Signals: e.g. `recaptcha_v2.py` constructor `else: raise ValueError(...)`.

- Rule: `core/const.py` owns `BASE_REQUEST_URL`, endpoint postfixes, and retry
  configuration — not top-level `config.py`.
- Rationale: the instruments import retry/URL constants from `core/const.py`.
- Enforcement / Signals: `core/sio_captcha_instrument.py` imports `RETRIES`,
  `BASE_REQUEST_URL` from `core/const.py`. Inferred: `config.py:attempts_generator`
  (default 5) is currently dead relative to the runtime path — instruments import
  `attempts_generator` from `core/utils.py` (default 30); the duplicate is flagged in
  `AGENTS.md`.

- Rule: TLS verification is disabled (`session.verify = False`) and
  `urllib3.InsecureRequestWarning` is suppressed.
- Rationale: proxy support; intentional, not a bug.
- Enforcement / Signals: `core/sio_captcha_instrument.py`; suppression in `config.py` and
  `core/const.py`; `core/AGENTS.md`.

- Rule: `src/python3_anticaptcha/__init__.py` exports only `__version__`; no re-exports.
- Rationale: public classes are imported from their module
  (e.g. `from python3_anticaptcha.recaptcha_v2 import ReCaptchaV2`), which is what the
  tests do.
- Enforcement / Signals: `__init__.py` content; `tests/AGENTS.md`. Note: the README
  quick-start `from python3_anticaptcha import X` does not match `__init__.py` (flagged in
  `AGENTS.md`).

- Rule: Only `ValueError` is raised; type hints use `Union`/`Optional`, never PEP 604
  `X | Y`.
- Rationale: repo-wide convention; no custom exception hierarchy.
- Enforcement / Signals: convention documented in `AGENTS.md`; not mechanically enforced.

## 6. Documentation Strategy

`ARCHITECTURE.md` (this file) owns the global architecture map, representative flows, and
invariants for the whole repository.

Repo-wide agent operating rules and task-based context routing live in `AGENTS.md`, with
local deltas in `src/python3_anticaptcha/AGENTS.md`,
`src/python3_anticaptcha/core/AGENTS.md`, and `tests/AGENTS.md`. Per-type usage and live
API references are in `README.md` and the Sphinx docs under `docs/`
(`docs/modules/<type>` per captcha type). Operational commands (install/test/lint/build/
release) are defined in `Makefile` and `.github/workflows/`.

No ADRs, `DESIGN.md`, or runbooks exist in this repository.
