# Changelog

All notable changes to the `smallpict` crate will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-22

### Added
- Official Rust SDK implementation for SmallPict OpenAPI 3.1.0 API.
- Zero-leak credential security with `SecretRedacted<T>` wrapper and regex masking in `Display` and `Debug`.
- High-concurrency asynchronous client `Client` powered by `tokio` and `reqwest`.
- Synchronous client `BlockingClient` enabled via the `blocking` feature flag.
- 4 unified core client methods: `optimize()`, `get_quota()`, `purge_cdn()`, and `validate_key()`.
- Helper `get_job_status()` for polling asynchronous image conversion tasks.
- Builder pattern for `ClientBuilder`, `BlockingClientBuilder`, and `OptimizeOptionsBuilder`.
- Resilient HTTP transport with 30s timeouts, exponential backoff, jitter, and automatic `Idempotency-Key` UUID injection.
- Optional `FallbackMode::Passthrough` for uninterrupted availability on quota limit exhaustion.
