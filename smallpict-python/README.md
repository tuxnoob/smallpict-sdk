# SmallPict Python SDK

Official Python client for the [SmallPict Image Optimization API](https://smallpict.tuxnoob.com) — high-performance next-gen image transcoding (AVIF, WebP), smart compression, Edge CDN delivery, and cache purging.

[![PyPI version](https://img.shields.io/pypi/v/smallpict.svg)](https://pypi.org/project/smallpict/)
[![Python versions](https://img.shields.io/pypi/pyversions/smallpict.svg)](https://pypi.org/project/smallpict/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## ⚡ Features

- **🚀 Synchronous & Asynchronous:** First-class sync (`SmallPictClient`) and async (`AsyncSmallPictClient`) clients powered by `httpx`.
- **🖼️ Optional Pillow / PIL Support:** Optimize `PIL.Image` instances directly via `pip install smallpict[pil]`.
- **🛡️ Secure HMAC-SHA256 & Bearer Auth:** Tamper-proof payload verification.
- **✨ 4 Core Unified Methods:** `optimize()`, `get_quota()`, `purge_cdn()`, and `validate_key()`.
- **🔄 Resilience & Fault Tolerance:** Automatic `Idempotency-Key` UUID injection, 30s timeouts, and exponential backoff with jitter on HTTP 429/5xx.
- **🔒 Zero-Leak Privacy:** API keys and credentials are automatically redacted from error traces and logs.
- **🏷️ Fully Typed:** Complete type annotations (PEP 561 `py.typed`) and strict `mypy` compatibility.

---

## 📥 Installation

```bash
# Standard installation
pip install smallpict

# With optional Pillow / PIL integration
pip install "smallpict[pil]"

# With poetry
poetry add smallpict
```

---

## 🚀 Quick Start

### 1. Synchronous Example

```python
import os
from smallpict import SmallPictClient

client = SmallPictClient(
    api_key=os.environ["SMALLPICT_API_KEY"],
    secret_key=os.environ.get("SMALLPICT_SECRET_KEY"),
)

with open("hero-banner.png", "rb") as f:
    image_bytes = f.read()

result = client.optimize(
    image_bytes,
    filename="hero-banner.png",
    format="avif",
    quality=80,
    max_width=1920,
)

print(f"Optimized CDN URL: {result.url}")
print(f"Original: {result.original_size}B ➔ Compressed: {result.compressed_size}B")
print(f"Saved: {result.savings_percentage}% ({result.bytes_saved} bytes)")
```

### 2. Asynchronous Example (FastAPI / Starlette)

```python
import os
from fastapi import FastAPI, UploadFile, File
from smallpict import AsyncSmallPictClient

app = FastAPI()
client = AsyncSmallPictClient(api_key=os.environ["SMALLPICT_API_KEY"])


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    result = await client.optimize(
        contents,
        filename=file.filename,
        format="auto", # Intelligently selects best format (AVIF/WebP)
        quality=85,
    )
    
    return {
        "url": result.url,
        "format": result.format,
        "saved_percentage": f"{result.savings_percentage}%",
    }
```

### 3. Celery Background Worker Task

```python
import os
from celery import Celery
from smallpict import SmallPictClient

app = Celery("tasks", broker="redis://localhost:6379/0")
client = SmallPictClient(api_key=os.environ["SMALLPICT_API_KEY"])


@app.task
def process_user_avatar(file_path: str):
    result = client.optimize(
        file_path,
        format="webp",
        quality=80,
        max_width=400,
        max_height=400,
    )
    return {"cdn_url": result.url, "bytes_saved": result.bytes_saved}
```

### 4. Optional Pillow / PIL Integration

```python
from PIL import Image
from smallpict import SmallPictClient

img = Image.open("photo.jpg")
# Crop or transform with Pillow
img_cropped = img.crop((0, 0, 800, 600))

client = SmallPictClient(api_key="sp_live_...")
result = client.optimize(img_cropped, format="avif", quality=85)
print(f"Delivered via CDN: {result.url}")
```

---

## 📊 Checking Quota & Invalidating CDN Cache

```python
from smallpict import SmallPictClient

client = SmallPictClient(api_key="sp_live_...")

# 1. Real-time quota metrics
quota = client.get_quota()
print(f"Plan: {quota.plan}, Used: {quota.quota_percentage}%")

# 2. Invalidate CDN cache
client.purge_cdn(["https://cdn.smallpict.com/opt/hero-banner.avif"])
print("CDN edge cache invalidated successfully.")
```

---

## 🧪 Testing

```bash
pytest
mypy smallpict
ruff check .
```

---

## 📄 License

MIT © [SmallPict Engineering](https://smallpict.tuxnoob.com)
