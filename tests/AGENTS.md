# Tests

## OVERVIEW
pytest + pytest-asyncio with mock server responses.

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Test patterns | tests/*.py |
| Mock responses | tests/static/responses.py |
| Fixtures | tests/conftest.py - BaseTest class |

## CONVENTIONS
- asyncio_mode = auto (pyproject.toml)
- API_KEY from env or mock
- Each captcha type has dedicated test file
- Test class naming: `Test<CaptchaType>`
- Method naming: `test_sio_*` (sync), `test_aio_*` (async)
- Response validation: `GetTaskResultResponseSer` from serializer

## TEST PATTERNS
- **BaseTest class**: Provides `get_proxy_args()`, `read_file()`, delay fixtures
- **Parametrized tests**: `@pytest.mark.parametrize` for proxy types, captcha types
- **Mocking**: `mocker.patch()` and `mocker.spy()` from pytest-mock
- **Context managers**: Test via `mocker.spy(ContextManager, "__enter__")`
- **Assertions**: `isinstance(result, dict)` + serializer validation

## ANTI-PATTERNS
- Don't skip BaseTest inheritance unless truly needed
- Don't use real API calls in unit tests (use mocker)

## COMMANDS
```bash
pytest                    # Run all tests
pytest -k recaptcha       # Run specific tests
make tests                # pytest + coverage
```
