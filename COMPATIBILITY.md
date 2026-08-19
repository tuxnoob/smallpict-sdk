# SmallPict SDK Compatibility Matrix

This matrix defines the officially tested and supported runtimes, framework integrations, and OpenAPI 3.1.0 capabilities for each SmallPict SDK.

---

## 📊 Language Runtime Compatibility

| Language SDK | Minimum Supported Version | Recommended / Target | Tested Frameworks & Runtimes |
| :--- | :--- | :--- | :--- |
| **Node.js / TypeScript** | Node.js 18.0.0+ | Node.js 20 / 22, Bun 1.1+ | Next.js (App/Pages Router), Express, Fastify, Cloudflare Workers |
| **Python** | Python 3.8+ | Python 3.11 / 3.12 | FastAPI, Django, Flask, Celery, Pillow/PIL |
| **PHP** | PHP 8.1+ | PHP 8.2 / 8.3 | Laravel 10/11, Symfony 6/7, PSR-18 HTTP Clients (Guzzle, cURL) |
| **Go** | Go 1.21+ | Go 1.22+ | Standard `net/http`, Gin, Echo, Fiber |
| **Rust** | Rust 1.70+ (Edition 2021) | Stable Latest | Tokio, Actix-web, Axum, `reqwest` |
| **Ruby** | Ruby 3.0+ | Ruby 3.2 / 3.3 | Ruby on Rails 7+, ActiveStorage, Sinatra, Sidekiq |
| **Java / Kotlin** | Java 17+ (LTS) | Java 21 (LTS) | Spring Boot 3+, Quarkus, Micronaut, Kotlin Coroutines |

---

## 🎯 OpenAPI 3.1 Feature Matrix

| Feature | Node.js | Python | PHP | Go | Rust | Ruby | Java |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **HMAC-SHA256 Auth** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Bearer Auth Support** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Binary Stream Upload** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Multipart Form Data** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Async Job Polling** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Idempotency Header** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Exponential Backoff** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Graceful Fallback Mode** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Zero Heavy Dependencies** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
