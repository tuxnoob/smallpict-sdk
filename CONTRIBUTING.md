# Contributing to SmallPict SDKs

Thank you for contributing to the SmallPict SDK ecosystem! All official SDKs share a unified public contract, rigorous security standards, and high-performance design principles.

---

## 📜 Contract-First Development Workflow

1. **OpenAPI as Single Source of Truth:**
   Never add, modify, or remove an API endpoint, request parameter, or response field in any language SDK without first updating and verifying **`smallPict-api/docs/openapi.yaml`**.
2. **Synchronized Semantic Versioning:**
   SDK versions follow Semantic Versioning (`MAJOR.MINOR.PATCH`).
   - `PATCH`: Bug fixes, security patches, performance improvements.
   - `MINOR`: New non-breaking features, optional parameters, or new format transcoders.
   - `MAJOR`: Breaking changes to public client methods or minimum language runtime requirements.

---

## 🔒 Security & Code Quality Standards

1. **Secret & Payload Redaction:**
   - Never print API keys (`sp_live_...`, `sp_test_...`, `sp_wp_...`), secret keys, or authorization headers in log outputs, exceptions, or error details.
   - Never print raw image binary buffers in exception traces.
2. **Zero-Copy Streaming:**
   - Always leverage language-native streaming abstractions (`io.Reader` in Go, `ReadableStream` in Node.js, `bytes::Bytes` in Rust, `httpx` async streams in Python) to prevent unbounded memory allocation.
3. **Idempotency & Safe Retries:**
   - Only retry idempotent operations or requests equipped with an `Idempotency-Key` UUID header.
   - Never retry non-idempotent mutations on client error statuses (`400`, `401`, `403`, `422`).
4. **CI Testing Requirements:**
   Every SDK pull request must pass:
   - Full unit test suite with offline mock servers (no live network dependencies in CI).
   - Type checking (`tsc`, `mypy`, `phpstan`, `cargo clippy`, `go vet`).
   - Linter formatting checks.

---

## 🌿 Branching & Release Convention

- Default development branch: `main`
- Feature / Task branches: `feat/<feature-name>` or `fix/<bug-name>`
- Releases: Triggered exclusively via Git tags (`vX.Y.Z`) through keyless OIDC GitHub Actions release workflows.
