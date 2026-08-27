# SmallPict Rust SDK

Official Rust SDK for the [SmallPict Image Optimization API](https://smallpict.app) — high-performance next-gen image transcoding (AVIF, WebP), smart compression, Edge CDN delivery, and cache purging.

[![Crates.io](https://img.shields.io/crates/v/smallpict.svg)](https://crates.io/crates/smallpict)
[![Documentation](https://docs.rs/smallpict/badge.svg)](https://docs.rs/smallpict)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ⚡ Features

- **🦀 Pure Rust TLS Stack:** Uses `rustls-tls` by default to avoid OpenSSL C-runtime issues.
- **⚡ Dual Asynchronous & Blocking Modes:** High-concurrency `tokio` async client and optional sync `BlockingClient`.
- **🛡️ Secure HMAC-SHA256 & Bearer Auth:** Tamper-proof payload verification.
- **✨ 4 Core Unified Methods:** `optimize()`, `get_quota()`, `purge_cdn()`, and `validate_key()`.
- **🔄 Resilience & Fault Tolerance:** Automatic `Idempotency-Key` UUID injection, 30s timeouts, and exponential backoff with jitter on HTTP 429/5xx.
- **🔒 Zero-Leak Privacy:** API keys and credentials are automatically wrapped in `SecretRedacted` and masked in `Display`, `Debug`, and error logs.

---

## 📥 Installation

In your `Cargo.toml`:

```toml
[dependencies]
smallpict = "1.0"
```

To enable synchronous / blocking mode:

```toml
[dependencies]
smallpict = { version = "1.0", features = ["blocking"] }
```

---

## 🚀 Quick Start

### 1. Asynchronous Example (Tokio)

```rust
use smallpict::{Client, ImageFormat, OptimizeOptions};
use std::fs;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::builder()
        .api_key(std::env::var("SMALLPICT_API_KEY")?)
        .secret_key(std::env::var("SMALLPICT_SECRET_KEY").ok()) // Optional HMAC Secret
        .build()?;

    let image_bytes = fs::read("hero-banner.png")?;

    let options = OptimizeOptions::builder()
        .format(ImageFormat::Avif)
        .quality(80)
        .max_width(1920)
        .build();

    let result = client.optimize(&image_bytes, Some(options)).await?;

    println!("Optimized CDN URL: {}", result.url);
    println!("Saved: {:.2}% ({} bytes)", result.savings_percentage, result.bytes_saved);

    Ok(())
}
```

### 2. Synchronous / Blocking Example

```rust
use smallpict::blocking::BlockingClient;
use smallpict::models::{ImageFormat, OptimizeOptions};
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = BlockingClient::new("sp_live_your_api_key")?;
    let image_bytes = fs::read("hero-banner.png")?;

    let result = client.optimize(&image_bytes, None)?;
    println!("CDN URL: {}", result.url);

    Ok(())
}
```

---

## 📊 Account Quota & Edge CDN Purge

```rust
// 1. Check real-time quota usage
let quota = client.get_quota().await?;
println!("Plan: {}, Quota Used: {:.2}%", quota.plan, quota.quota_percentage);

// 2. Invalidate Edge CDN cache
let purge = client.purge_cdn(&["https://cdn.smallpict.app/opt/hero-banner.avif"], smallpict::PurgeType::Url).await?;
println!("{}", purge.message);
```

---

## 🧪 Testing

```bash
cargo test --all-features
cargo clippy --all-targets --all-features -- -D warnings
```

---

## 📄 License

MIT © [SmallPict Engineering](https://smallpict.app)
