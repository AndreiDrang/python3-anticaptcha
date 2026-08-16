# AGENTS.md

## Scope and inheritance

Applies to: `okf/`. Inherits repo-wide guidance from `../AGENTS.md`.
This file defines only local rules for the knowledge bundle.

## What lives here

```text
okf/
├── index.md            # bundle entry point + navigation
├── core-components/    # CaptchaParams, config, utils, context managers
├── api-contract/       # enums, constants, serializer structs
├── http-transport/     # sync/async instruments, shared base
└── captcha-types/      # one concept page per captcha type (+ index.md)
```

## Local boundaries and invariants

- The bundle declares **OKF v0.1** (`okf_version` frontmatter in `okf/index.md`).
  Concept pages are kebab-case, one concept per file; filenames are stable identities
  for retrieval — rename or merge only deliberately, never in passing.
- Every section directory has its own `index.md`. When adding, moving, or removing a
  page, update both that section `index.md` and the links in `okf/index.md`.
- Concept pages describe behavior for retrieval; they are not user-facing docs. Link to
  `README.md` usage examples instead of copying them.
- `captcha-types/` intentionally includes types with **no handler module** (e.g.
  `hcaptcha.md`, which exists only in `CaptchaTypeEnm`). A missing implementation is
  documentation, not a bug to fix here.
- When code behavior changes, update the matching concept page in the same change
  (e.g. `core/serializer.py` ↔ `api-contract/serializer.md`).

## Nearby docs

- `ARCHITECTURE.md` — canonical system map; this bundle mirrors it concept-by-concept.
- `okf/index.md` — bundle navigation entry point.
