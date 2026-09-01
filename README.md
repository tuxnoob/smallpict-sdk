# SmallPict Official SDK Ecosystem

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenAPI 3.1.0](https://img.shields.io/badge/OpenAPI-3.1.0-green.svg)](../smallPict-api/docs/openapi.yaml)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](#)

Welcome to the **SmallPict SDK Ecosystem** — official developer tools for integrating the [SmallPict Image Optimization API](https://smallpict.app) across **7 programming languages**.

---

## 📦 Official Client Libraries

| Language | Directory | Official Package | Package Registry | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Node.js / TypeScript** | [`smallpict-node/`](smallpict-node/) | [`@smallpict/sdk`](https://npmjs.com/package/@smallpict/sdk) | [npm](https://npmjs.com/package/@smallpict/sdk) | [![npm](https://img.shields.io/npm/v/@smallpict/sdk.svg)](https://npmjs.com/package/@smallpict/sdk) |
| **Python** | [`smallpict-python/`](smallpict-python/) | [`smallpict`](https://pypi.org/project/smallpict) | [PyPI](https://pypi.org/project/smallpict) | [![PyPI](https://img.shields.io/pypi/v/smallpict.svg)](https://pypi.org/project/smallpict) |
| **PHP** | [`smallpict-php/`](smallpict-php/) | [`smallpict/smallpict-php`](https://packagist.org/packages/smallpict/smallpict-php) | [Packagist](https://packagist.org/packages/smallpict/smallpict-php) | [![Packagist](https://img.shields.io/packagist/v/smallpict/smallpict-php.svg)](https://packagist.org/packages/smallpict/smallpict-php) |
| **Go** | [`smallpict-go/`](smallpict-go/) | [`github.com/tuxnoob/smallpict-go`](https://pkg.go.dev/github.com/tuxnoob/smallpict-go) | [pkg.go.dev](https://pkg.go.dev/github.com/tuxnoob/smallpict-go) | [![Go Reference](https://pkg.go.dev/badge/github.com/tuxnoob/smallpict-go.svg)](https://pkg.go.dev/github.com/tuxnoob/smallpict-go) |
| **Rust** | [`smallpict-rust/`](smallpict-rust/) | [`smallpict`](https://crates.io/crates/smallpict) | [crates.io](https://crates.io/crates/smallpict) | [![crates.io](https://img.shields.io/crates/v/smallpict.svg)](https://crates.io/crates/smallpict) |
| **Ruby** | [`smallpict-ruby/`](smallpict-ruby/) | [`smallpict`](https://rubygems.org/gems/smallpict) | [RubyGems](https://rubygems.org/gems/smallpict) | [![Gem Version](https://badge.fury.io/rb/smallpict.svg)](https://badge.fury.io/rb/smallpict) |
| **Java / Kotlin** | [`smallpict-java/`](https://github.com/tuxnoob/smallpict-java) | [`io.github.tuxnoob:smallpict-java`](https://central.sonatype.com) | [Maven Central](https://central.sonatype.com) | [![Maven Central](https://img.shields.io/maven-central/v/io.github.tuxnoob/smallpict-java.svg)](https://central.sonatype.com) |

---

## 📚 Developer Documentation Guides

- 🚀 [**Quickstart Comparison Matrix**](docs/QUICKSTART.md) — Side-by-side hello-world in all 7 languages.
- 🏛️ [**Architectural Blueprint**](docs/ARCHITECTURE.md) — 4 unified methods, idempotency UUIDs, backoff retries, and fallback modes.
- 🔐 [**Authentication & HMAC Signing**](docs/AUTHENTICATION.md) — HMAC-SHA256 vs Bearer Auth guide and walkthroughs.
- 🛑 [**Unified Error Handling**](docs/ERROR_HANDLING.md) — Complete error code taxonomy and typed exception handling.
- 🌊 [**Streaming Guide**](docs/STREAMING_GUIDE.md) — Memory-efficient large image optimization pipelines.
- 🛠️ [**Framework Integration Recipes**](docs/FRAMEWORK_INTEGRATIONS.md) — Next.js, FastAPI, Laravel, Gin, Rails, Spring Boot.

---

## 🛡️ Core Guarantees Across All SDKs

1. **4 Unified Core Methods:** `optimize()`, `getQuota()`, `purgeCdn()`, `validateKey()` + helper `getJobStatus()`.
2. **Zero-Leak Privacy:** All API keys and HMAC secrets are automatically redacted in logs, `toString()`, and exceptions.
3. **Resilience & Fault Tolerance:** Automatic `Idempotency-Key` UUID injection, exponential backoff with jitter on HTTP 429/5xx.
4. **Passthrough Fallback:** High-availability mode ensures graceful handling during quota exhaustion without breaking user applications.

---

## 🧪 Master Contract Verification

Run the automated contract validator locally:

```bash
./scripts/check-sdk-contract.sh
```

---

## 📄 License

MIT © [SmallPict Engineering](https://smallpict.app)
