# Changelog

All notable changes to the `smallpict/smallpict-php` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-22

### Added
- Official PHP SDK implementation for SmallPict OpenAPI 3.1.0 API.
- Broad compatibility supporting **PHP 7.4 through PHP 8.4**.
- Zero external dependencies with high-performance native cURL client (`CurlHttpClient`).
- PSR-18 HTTP client interface support (`HttpClientInterface`).
- 4 unified core client methods: `optimize()`, `getQuota()`, `purgeCdn()`, and `validateKey()`.
- Helper `getJobStatus()` for polling asynchronous image conversion tasks.
- Optional Laravel 10/11 auto-discovery support via `SmallPictServiceProvider` and `SmallPict` Facade.
- Automatic secret masking to ensure API keys and HMAC signatures never leak in error messages or exception stack traces.
- Resilient HTTP transport with 30s timeouts, exponential backoff, jitter, and automatic `Idempotency-Key` UUID injection.
- Optional `FallbackMode::PASSTHROUGH` mode for uninterrupted availability on quota limit exhaustion.
