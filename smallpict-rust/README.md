# SmallPict Rust SDK

Official asynchronous Rust client for the [SmallPict Image Optimization API](https://smallpict.tuxnoob.com).

> ⚠️ **Development Scaffold (Phase 0):** This crate is currently being scaffolded under Phase 0. Full implementation begins in **Phase 2.2**.

## Target Features
- Async-first design with `tokio` and `reqwest`.
- `bytes::Bytes` zero-copy stream processing.
- Typed `serde` models and `thiserror` error enums.
- Configurable TLS backends (`default-tls` vs `rustls-tls`).

## License
MIT
