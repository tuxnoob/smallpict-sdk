# SmallPict SDK Parent Workspace

This parent workspace coordinates development, contract validation, and multi-language alignment across all official SmallPict SDK repositories under the `tuxnoob` GitHub organization.

---

## 🏛️ Architecture & Repositories

Each child directory is an **independent public Git repository** (or submodule/worktree) published to its respective ecosystem package registry:

| Directory | Target Repository | Target Package Registry | Primary Runtime Target |
| :--- | :--- | :--- | :--- |
| `smallpict-node/` | `github.com/tuxnoob/smallpict-node` | **npm** (`@smallpict/sdk` / `smallpict`) | Node.js 18+, Bun, Next.js, Cloudflare Workers |
| `smallpict-python/` | `github.com/tuxnoob/smallpict-python` | **PyPI** (`smallpict`) | Python 3.8+ (Sync & Async `httpx`, PIL Extra) |
| `smallpict-php/` | `github.com/tuxnoob/smallpict-php` | **Packagist** (`smallpict/smallpict-php`) | PHP 8.1+ (PSR-18, Laravel ServiceProvider) |
| `smallpict-go/` | `github.com/tuxnoob/smallpict-go` | **pkg.go.dev** (`github.com/tuxnoob/smallpict-go`) | Go 1.21+ (`net/http` stdlib, `io.Reader` streams) |
| `smallpict-rust/` | `github.com/tuxnoob/smallpict-rust` | **crates.io** (`smallpict`) | Rust 2021 (Async `tokio`/`reqwest`, `bytes::Bytes`) |
| `smallpict-ruby/` | `github.com/tuxnoob/smallpict-ruby` | **RubyGems** (`smallpict`) | Ruby 3.0+ (Faraday, Rails ActiveStorage) |
| `smallpict-java/` | `github.com/tuxnoob/smallpict-java` | **Maven Central** (`com.smallpict:smallpict-java`) | Java 17+ (`java.net.http.HttpClient`, Jackson) |

---

## 🔒 Unified Contract & Single Source of Truth

All SDKs implement the exact contract defined in:
👉 **[`smallPict-api/docs/openapi.yaml`](../smallPict-api/docs/openapi.yaml)** (OpenAPI 3.1.0)
👉 **[`smallPict-api/docs/api-contract.md`](../smallPict-api/docs/api-contract.md)**

### Unified Public Client Surface (4 Core Methods)
```text
client.optimize(image_source, options) -> OptimizedResult
client.get_quota()                     -> QuotaResponse
client.purge_cdn(urls_or_all)          -> PurgeResponse
client.validate_key()                  -> bool
```

### Global Client Invariants
1. **HMAC-SHA256 Signatures:** Implements `X-API-Key`, `X-Timestamp`, and `X-Signature` headers (with `Authorization: Bearer` support).
2. **Environment Key Prefixes:**
   - `sp_live_...`: Production Key (quota deduction + production edge CDN).
   - `sp_test_...`: Logical Sandbox Key (zero quota deduction + 24h temp S3 storage).
   - `sp_wp_...`: Dedicated WordPress Plugin Key.
3. **Resilience & Timeouts:** 30-second default request timeout with bounded exponential backoff & jitter on HTTP 429/5xx.
4. **Idempotency:** Automatic injection of `Idempotency-Key: <uuid>` on mutating POST requests.
5. **Secret Redaction:** Strict prohibition of logging raw API keys, secret keys, or image binary buffers.
6. **Graceful Fallback:** Support for `fallback_mode: 'throw' | 'passthrough'` on quota exhaustion.

---

## 🚦 Sequential "Vibe Coding" Execution Order

```text
Phase 0: Contract Foundation (OpenAPI 3.1 Specification) ✅ DONE
  │
  ├──► Phase 1: Web & Scripting Ecosystem (Node.js ➔ Python ➔ PHP)
  │
  ├──► Phase 2: High-Performance Systems (Go ➔ Rust)
  │
  ├──► Phase 3: Enterprise & Frameworks (Ruby ➔ Java/Kotlin)
  │
  └──► Phase 4: Documentation Hub & Package Registry Releases
```

---

## 🛠️ Workspace Scripts

- Run cross-SDK contract audit:
  ```bash
  ./scripts/check-sdk-contract.sh
  ```
