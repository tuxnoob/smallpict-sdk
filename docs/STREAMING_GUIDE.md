# SmallPict Memory-Efficient Streaming Guide

When processing high-resolution images (e.g. 50MB RAW or TIFF files), loading the entire file into memory can cause Out-Of-Memory (OOM) crashes in serverless functions and container environments.

SmallPict SDKs provide streaming primitives to pipe image payloads with constant low memory overhead.

---

## 🌊 Streaming Patterns Per Language

### 1. Node.js (ReadableStream / Buffer Streams)
```typescript
import { SmallPictClient } from '@smallpict/sdk';
import * as fs from 'node:fs';

const client = new SmallPictClient({ apiKey: process.env.SMALLPICT_API_KEY! });
const fileStream = fs.createReadStream('huge-photo.jpg');

const result = await client.optimize(fileStream, {
  filename: 'huge-photo.jpg',
  format: 'avif'
});
```

### 2. Python (Generators & IO Streams)
```python
from smallpict import SmallPictClient

client = SmallPictClient(api_key="sp_live_...")

with open("huge-photo.jpg", "rb") as f:
    result = client.optimize(f, options={"filename": "huge-photo.jpg", "format": "avif"})
```

### 3. Go (`io.Reader` Streaming)
```go
package main

import (
	"context"
	"os"
	"github.com/tuxnoob/smallpict-go"
)

func main() {
	client, _ := smallpict.NewClient(smallpict.WithAPIKey(os.Getenv("SMALLPICT_API_KEY")))
	file, _ := os.Open("huge-photo.jpg")
	defer file.Close()

	result, _ := client.OptimizeReader(context.Background(), file, &smallpict.OptimizeOptions{
		Filename: "huge-photo.jpg",
		Format:   smallpict.FormatAVIF,
	})
}
```

### 4. Java (`InputStream` Pipe)
```java
SmallPictClient client = new SmallPictClient("sp_live_...");

try (InputStream stream = new BufferedInputStream(new FileInputStream("huge-photo.jpg"))) {
    OptimizeResult result = client.optimize(stream, OptimizeOptions.builder()
            .filename("huge-photo.jpg")
            .format(ImageFormat.AVIF)
            .build());
}
```
