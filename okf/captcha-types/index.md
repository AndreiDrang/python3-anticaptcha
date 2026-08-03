# Captcha Types

Individual captcha solver implementations. Each type is a subclass of [CaptchaParams](../core-components/captcha-params.md).

## Token-Based Captchas

* [ReCaptchaV2](recaptcha-v2.md) - Google reCAPTCHA v2 (checkbox and invisible)
* [ReCaptchaV3](recaptcha-v3.md) - Google reCAPTCHA v3 (score-based)
* [Turnstile](turnstile.md) - Cloudflare Turnstile
* [FunCaptcha](fun-captcha.md) - Arkose Labs FunCaptcha
* [GeeTest](gee-test.md) - GeeTest captcha
* [HCaptcha](hcaptcha.md) - hCaptcha
* [FriendlyCaptcha](friendly-captcha.md) - FriendlyCaptcha puzzles
* [Prosopo](prosopo.md) - Prosopo captcha

## Image-Based Captchas

* [ImageToText](image-to-text.md) - Text from image captchas
* [ImageToCoordinates](image-to-coordinates.md) - Click coordinates captchas

## Cloud Provider Captchas

* [AmazonWAF](amazon-waf.md) - AWS WAF Captcha
* [Altcha](altcha.md) - Altcha captcha

## Special Types

* [Control](control.md) - Account balance and reporting operations
* [CustomTask](custom-task.md) - Custom task types

## Implementation Pattern

All captcha types follow the same pattern:
1. Inherit from `CaptchaParams`
2. Define `__init__` that validates `captcha_type` and sets `task_params`
3. Optionally override `captcha_handler` or `aio_captcha_handler` for special processing
4. Expose both sync and async solving methods

## Relationships

All captcha types:
- Inherit from [CaptchaParams](../core-components/captcha-params.md)
- Use [CaptchaTypeEnm](../api-contract/enums.md) for type validation
- Use [SIOCaptchaInstrument](../http-transport/sio-instrument.md) for synchronous solving
- Use [AIOCaptchaInstrument](../http-transport/aio-instrument.md) for asynchronous solving
