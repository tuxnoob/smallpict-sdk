# SmallPict Go SDK

Official idiomatic Go SDK for the [SmallPict Image Optimization API](https://smallpict.tuxnoob.com).

> ⚠️ **Development Scaffold (Phase 0):** This package is currently being scaffolded under Phase 0. Full implementation begins in **Phase 2.1**.

## Target Features
- Zero external runtime dependencies (Standard `net/http` library only).
- `context.Context` propagation and cancellation on all network operations.
- `io.Reader` and `io.Writer` zero-copy stream uploads and downloads.
- Table-driven unit tests with `net/http/httptest`.

## License
MIT
