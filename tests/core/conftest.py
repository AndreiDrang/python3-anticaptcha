"""HTTP-boundary fixtures for the test suite.

The single most important rule of this rewrite: **mock only the true external
boundary**. For this library that boundary is the HTTP transport
(``requests.Session`` for sync, ``aiohttp.ClientSession`` for async). Everything
upstream — payload assembly in the captcha-type classes, the
create-task/get-result state machine in the instruments, and msgspec
serialization — runs for real.

These fixtures also neutralize ``time.sleep``/``asyncio.sleep`` so the polling
loops in ``_get_result`` do not slow the suite down.
"""

from copy import deepcopy
from unittest.mock import MagicMock

import pytest


# --------------------------------------------------------------------------- #
# Sync (requests) helpers
# --------------------------------------------------------------------------- #
def resp(payload: dict, status_code: int = 200, content: bytes = b"") -> MagicMock:
    """Build a fake ``requests.Response`` with the bits the instruments touch."""
    mock = MagicMock(name="response")
    mock.status_code = status_code
    mock.json.return_value = payload
    mock.content = content
    mock.raise_for_status.return_value = None
    return mock


class SIOHTTPBoundary:
    """Controller returned by the :func:`sio_http` fixture."""

    def __init__(self, post_mock, get_mock):
        self.post = post_mock
        self.get = get_mock

    # convenience: enqueue a FIFO sequence of create-task / result responses
    def post_sequence(self, *payloads, status_code: int = 200):
        self.post.side_effect = [resp(p, status_code=status_code) for p in payloads]


@pytest.fixture
def sio_http(mocker):
    """Patch ``requests.Session.post``/``.get`` and ``time.sleep``.

    Returns a :class:`SIOHTTPBoundary` exposing the two method mocks. The real
    ``SIOCaptchaInstrument`` still builds its own ``requests.Session`` and runs
    full serialization/orchestration; only the network call is intercepted.
    """
    mocker.patch("time.sleep")  # polling loops must not actually wait
    post = mocker.patch("requests.Session.post")
    get = mocker.patch("requests.Session.get")
    return SIOHTTPBoundary(post, get)


# --------------------------------------------------------------------------- #
# Async (aiohttp) helpers
# --------------------------------------------------------------------------- #
class _FakeAioContent:
    def __init__(self, data: bytes):
        self._data = data

    async def read(self) -> bytes:
        return self._data


class FakeAioResp:
    """Minimal stand-in for an ``aiohttp.ClientResponse``."""

    def __init__(self, payload: dict, status: int = 200, reason: str = "OK", content: bytes = b""):
        self._payload = payload
        self.status = status
        self.reason = reason
        self.content = _FakeAioContent(content)

    async def json(self) -> dict:
        return self._payload


class _FakeAioCM:
    """Async context manager wrapping a :class:`FakeAioResp`."""

    def __init__(self, response: FakeAioResp):
        self._response = response

    async def __aenter__(self):
        return self._response

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAioSession:
    """Async-context-manager session that draws responses from shared queues.

    ``aiohttp.ClientSession()`` is patched to return one of these, so multiple
    sessions created during a single handler call (create-task then get-result)
    share the same response stream.
    """

    def __init__(self, post_queue: list, get_queue: list):
        self._post_queue = post_queue
        self._get_queue = get_queue
        self.post_calls: list = []
        self.get_calls: list = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def post(self, *args, **kwargs):
        self.post_calls.append({"args": args, "kwargs": kwargs})
        item = self._post_queue.pop(0)
        return _FakeAioCM(FakeAioResp(**item))

    def get(self, *args, **kwargs):
        self.get_calls.append({"args": args, "kwargs": kwargs})
        item = self._get_queue.pop(0)
        return _FakeAioCM(FakeAioResp(**item))


class AIOHTTPBoundary:
    """Controller returned by the :func:`aio_http` fixture."""

    def __init__(self, post_queue, get_queue, sessions):
        self._post_queue = post_queue
        self._get_queue = get_queue
        self._sessions = sessions

    def enqueue_post(self, payload, status: int = 200, reason: str = "OK"):
        # aiohttp returns a freshly decoded JSON object. Copy here so the
        # instrument's ``json_result.update({"taskId": ...})`` cannot mutate
        # shared response constants and contaminate later tests.
        self._post_queue.append({"payload": deepcopy(payload), "status": status, "reason": reason})

    def enqueue_get(self, content: bytes = b"", status: int = 200):
        self._get_queue.append({"payload": {}, "content": content, "status": status})

    @property
    def post_calls(self) -> list:
        """All ``session.post(...)`` calls across every session created."""
        calls = []
        for session in self._sessions:
            calls.extend(session.post_calls)
        return calls

    @property
    def get_calls(self) -> list:
        calls = []
        for session in self._sessions:
            calls.extend(session.get_calls)
        return calls


@pytest.fixture
def aio_http(mocker):
    """Patch ``aiohttp.ClientSession`` and ``asyncio.sleep``.

    Every ``aiohttp.ClientSession()`` instantiation yields a
    :class:`FakeAioSession` backed by shared FIFO queues, so the full async
    create-task/get-result flow runs without network or real waiting.
    """
    mocker.patch("asyncio.sleep")
    post_queue: list = []
    get_queue: list = []
    sessions: list = []

    def _factory(*args, **kwargs):
        session = FakeAioSession(post_queue, get_queue)
        sessions.append(session)
        return session

    mocker.patch("aiohttp.ClientSession", side_effect=_factory)
    return AIOHTTPBoundary(post_queue, get_queue, sessions)


# --------------------------------------------------------------------------- #
# Independent response oracles (NOT copied from production code)
# --------------------------------------------------------------------------- #
CREATE_TASK_OK = {"errorId": 0, "taskId": 4242}

RESULT_PROCESSING = {"errorId": 0, "status": "processing"}

RESULT_READY = {
    "errorId": 0,
    "status": "ready",
    "solution": {"gRecaptchaResponse": "FAKE_SOLUTION_TOKEN"},
    "cost": 0.002,
    "ip": "1.2.3.4",
    "createTime": 1679004358,
    "endTime": 1679004368,
    "solveCount": 1,
}

RESULT_ERROR = {
    "errorId": 15,
    "errorCode": "ERROR_NO_SUCH_CAPTCHA_ID",
    "errorDescription": "task not found",
}
