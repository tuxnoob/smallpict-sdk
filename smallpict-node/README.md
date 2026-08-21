# SmallPict Node.js & TypeScript SDK

Official TypeScript and Node.js SDK for the [SmallPict Image Optimization API](https://smallpict.tuxnoob.com) — high-performance next-gen image transcoding (AVIF, WebP), smart compression, Edge CDN delivery, and cache purging.

[![npm version](https://img.shields.io/npm/v/@smallpict/sdk.svg)](https://www.npmjs.com/package/@smallpict/sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## ⚡ Features

- **🚀 Universal Runtime Support:** Compatible with **Node.js 18+**, **Bun**, **Next.js (App & Pages Router)**, and **Cloudflare Workers** with **zero external HTTP dependencies** (native Web Fetch & Web Crypto).
- **🛡️ HMAC-SHA256 & Bearer Auth:** Secure request signing and tamper protection.
- **✨ 4 Core Unified Methods:** `optimize()`, `getQuota()`, `purgeCdn()`, and `validateKey()`.
- **🔄 Resilience & Fault Tolerance:** Automatic `Idempotency-Key` injection, 30s request timeouts, and exponential backoff with jitter on HTTP 429/5xx.
- **🔒 Zero-Leak Privacy:** API keys and credentials are automatically redacted from error traces and logs.
- **📦 Dual ESM & CJS:** Full TypeScript definitions and source maps included.

---

## 📥 Installation

```bash
# npm
npm install @smallpict/sdk

# pnpm
pnpm add @smallpict/sdk

# yarn
yarn add @smallpict/sdk

# bun
bun add @smallpict/sdk
```

---

## 🚀 Quick Start

### 1. Minimal Example

```typescript
import { SmallPictClient } from '@smallpict/sdk';
import { readFileSync } from 'node:fs';

const client = new SmallPictClient({
  apiKey: process.env.SMALLPICT_API_KEY!, // or 'sp_live_...' / 'sp_test_...'
  secretKey: process.env.SMALLPICT_SECRET_KEY, // Optional HMAC secret key
});

const imageBuffer = readFileSync('./hero-banner.png');

const result = await client.optimize(imageBuffer, {
  format: 'avif',
  quality: 80,
  maxWidth: 1920,
});

console.log(`Optimized CDN URL: ${result.url}`);
console.log(`Original: ${result.originalSize} bytes ➔ Compressed: ${result.compressedSize} bytes`);
console.log(`Saved: ${result.savingsPercentage}% (${result.bytesSaved} bytes)`);
```

---

## 🏭 Production Examples

### Next.js Server Action / Route Handler with Fallback Mode

```typescript
import { SmallPictClient, QuotaExceededError } from '@smallpict/sdk';
import { NextResponse } from 'next/server';

const client = new SmallPictClient({
  apiKey: process.env.SMALLPICT_API_KEY!,
  secretKey: process.env.SMALLPICT_SECRET_KEY,
  // If quota is exhausted, passthrough original image without throwing
  fallbackMode: 'passthrough',
});

export async function POST(req: Request) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    const arrayBuffer = await file.arrayBuffer();
    const result = await client.optimize(arrayBuffer, {
      filename: file.name,
      mimeType: file.type,
      format: 'auto', // Intelligently selects best format (AVIF/WebP)
      quality: 85,
    });

    return NextResponse.json({
      url: result.url,
      format: result.format,
      saved: `${result.savingsPercentage}%`,
    });
  } catch (error) {
    if (error instanceof QuotaExceededError) {
      return NextResponse.json({ error: 'Monthly quota exhausted' }, { status: 402 });
    }
    return NextResponse.json({ error: 'Image optimization failed' }, { status: 500 });
  }
}
```

### Checking Account Quota & Purging CDN Cache

```typescript
import { SmallPictClient } from '@smallpict/sdk';

const client = new SmallPictClient({
  apiKey: process.env.SMALLPICT_API_KEY!,
});

// 1. Check real-time quota usage
const quota = await client.getQuota();
console.log(`Plan: ${quota.plan}`);
console.log(`Quota Used: ${quota.quotaPercentage}% (${quota.bytesUsed} / ${quota.quotaLimit} bytes)`);

// 2. Invalidate CDN cache for modified images
await client.purgeCdn([
  'https://cdn.smallpict.com/opt/hero-banner.avif',
  'https://cdn.smallpict.com/opt/logo.webp',
]);
console.log('CDN cache purged successfully!');
```

---

## 🧪 Testing

```bash
npm run test
npm run typecheck
npm run build
```

---

## 📄 License

MIT © [SmallPict Engineering](https://smallpict.tuxnoob.com)
