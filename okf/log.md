# Knowledge Bundle Update Log

## 2025-01-15

* **Initialization**: Created OKF knowledge bundle for python3-anticaptcha repository root.
* **Creation**: Added [Core Components](core-components/) directory with base class and utility concepts.
  * Added [CaptchaParams](core-components/captcha-params.md) - base class for all captcha solvers
  * Added [Context Managers](core-components/context-managers.md) - session lifecycle management
  * Added [Utilities](core-components/utils.md) - polling loop and helper functions
  * Added [Configuration](core-components/config.md) - package configuration and warnings
* **Creation**: Added [API Contract](api-contract/) directory with wire-level contract definitions.
  * Added [Serializer](api-contract/serializer.md) - msgspec Struct definitions
  * Added [Enums](api-contract/enums.md) - all captcha types and status values
  * Added [Constants](api-contract/constants.md) - base URLs, retry config, and app key
* **Creation**: Added [HTTP Transport](http-transport/) directory with sync/async client implementations.
  * Added [Captcha Instrument](http-transport/captcha-instrument.md) - base class with file handling
  * Added [SIO Instrument](http-transport/sio-instrument.md) - synchronous requests-based transport
  * Added [AIO Instrument](http-transport/aio-instrument.md) - asynchronous aiohttp-based transport
* **Creation**: Added [Captcha Types](captcha-types/) directory with individual solver implementations.
  * Added [ReCaptchaV2](captcha-types/recaptcha-v2.md) - Google reCAPTCHA v2 solver
  * Added [ReCaptchaV3](captcha-types/recaptcha-v3.md) - Google reCAPTCHA v3 solver
  * Added [Turnstile](captcha-types/turnstile.md) - Cloudflare Turnstile solver
  * Added [FunCaptcha](captcha-types/fun-captcha.md) - Arkose Labs FunCaptcha solver
  * Added [GeeTest](captcha-types/gee-test.md) - GeeTest captcha solver
  * Added [FriendlyCaptcha](captcha-types/friendly-captcha.md) - FriendlyCaptcha puzzle solver
  * Added [Prosopo](captcha-types/prosopo.md) - Prosopo captcha solver
  * Added [AmazonWAF](captcha-types/amazon-waf.md) - AWS WAF Captcha solver
  * Added [Altcha](captcha-types/altcha.md) - Altcha captcha solver
  * Added [ImageToText](captcha-types/image-to-text.md) - text extraction from image captchas
  * Added [ImageToCoordinates](captcha-types/image-to-coordinates.md) - coordinate selection captchas
  * Added [HCaptcha](captcha-types/hcaptcha.md) - hCaptcha solver
  * Added [Control](captcha-types/control.md) - account management and reporting
  * Added [CustomTask](captcha-types/custom-task.md) - generic custom task solver
* **Creation**: Added root [index.md](index.md) with OKF version declaration and navigation.
* **Creation**: Added [log.md](log.md) for change tracking.
