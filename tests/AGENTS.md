# Tests

## OVERVIEW
pytest + pytest-asyncio with mock server responses.

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Test patterns | tests/*.py |
| Mock responses | tests/static/responses.py |
| Fixtures | Conftest in each test file |

## CONVENTIONS
- asyncio_mode = auto (pytest.ini)
- API_KEY from env or mock
- Each captcha type has dedicated test file
- Mock server responses in static/responses.py

## COMMANDS
```bash
pytest                    # Run all tests
pytest -k recaptcha       # Run specific tests
make tests                # pytest + coverage
```
