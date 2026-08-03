# API Contract

The wire-level contract defining how python3-anticaptcha communicates with the AntiCaptcha API.

## Serialization

* [Serializer](serializer.md) - msgspec Struct definitions for request/response envelopes

## Enumerations

* [Enums](enums.md) - All accepted string identifiers and status values

## Constants

* [Constants](constants.md) - Base URLs, endpoint postfixes, and retry configuration

## Relationships

These components define the shared contract that both synchronous and asynchronous transports must adhere to. All captcha handlers and HTTP instruments depend on these definitions.
