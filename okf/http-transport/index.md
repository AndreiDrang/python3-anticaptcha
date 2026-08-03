# HTTP Transport

The dual HTTP client implementations that handle communication with the AntiCaptcha API.

## Synchronous Transport

* [SIO Captcha Instrument](sio-instrument.md) - Synchronous HTTP client using requests library

## Asynchronous Transport

* [AIO Captcha Instrument](aio-instrument.md) - Asynchronous HTTP client using aiohttp library

## Shared Components

* [Captcha Instrument](captcha-instrument.md) - Base class and shared file handling logic

## Relationships

Both transports must stay in lockstep - they implement the same API contract and must produce identical request/response shapes. The transports depend on the [API Contract](../api-contract/) for serialization and constants.
