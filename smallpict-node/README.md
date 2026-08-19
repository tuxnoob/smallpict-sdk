# SmallPict Node.js & TypeScript SDK

Official TypeScript and Node.js SDK for the [SmallPict Image Optimization API](https://smallpict.tuxnoob.com).

> ⚠️ **Development Scaffold (Phase 0):** This package is currently being scaffolded under Phase 0. Full implementation begins in **Phase 1.1**.

## Target Features
- Full TypeScript strict mode & generated declaration files.
- Zero external HTTP runtime dependencies (Fetch-native for Node.js 18+, Bun, Next.js, Cloudflare Workers).
- Native support for `Buffer`, `Blob`, `File`, `ReadableStream`.
- Bounded retry with exponential backoff and jitter on HTTP 429 / 5xx.
- Idempotency key injection on mutating calls.

## License
MIT
