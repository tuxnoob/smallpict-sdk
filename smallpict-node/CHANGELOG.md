# Changelog

All notable changes to the `@smallpict/sdk` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-21

### Added
- Official TypeScript & Node.js SDK implementation for SmallPict OpenAPI 3.1.0 API.
- Zero external runtime HTTP dependencies using standard Web Fetch and Web Crypto APIs.
- 4 unified client methods: `optimize()`, `getQuota()`, `purgeCdn()`, and `validateKey()`.
- Helper `getJobStatus()` for asynchronous image conversion tracking.
- Universal HMAC-SHA256 request signing and Bearer token fallback.
- Support for `Buffer`, `Uint8Array`, `ArrayBuffer`, `Blob`, `File`, `ReadableStream`, and URL image sources.
- Resilient HTTP transport with 30s `AbortController` timeout, exponential backoff, jitter, and automatic `Idempotency-Key` UUID injection.
- Automatic secret masking to prevent credentials leaking in error messages and stack traces.
- Optional `fallbackMode: 'passthrough'` for continuous availability on quota exhaustion.
- Dual ESM and CJS bundle distribution with full TypeScript declarations.
