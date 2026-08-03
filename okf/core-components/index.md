# Core Components

Shared infrastructure that all captcha handlers depend on.

## Base Classes

* [CaptchaParams](captcha-params.md) - Base class for all captcha solver classes
* [Context Managers](context-managers.md) - Session lifecycle management for sync/async

## Utilities

* [Utilities Module](utils.md) - Polling loop and helper functions
* [Configuration](config.md) - Package configuration and warnings suppression

## Relationships

All captcha type handlers inherit from [CaptchaParams](captcha-params.md) and depend on components in this directory. The core components form the foundation layer that must remain stable as new captcha types are added.
