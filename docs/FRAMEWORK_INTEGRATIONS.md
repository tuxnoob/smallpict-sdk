# SmallPict Framework Integration Recipes

This guide contains drop-in integration recipes for top web frameworks across the 7 SDK ecosystems.

---

## 🛠️ Framework Recipes

### 1. Next.js 14/15 App Router (TypeScript)
```typescript
// app/api/optimize/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { SmallPictClient, ImageFormat } from '@smallpict/sdk';

const client = new SmallPictClient({ apiKey: process.env.SMALLPICT_API_KEY! });

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const file = formData.get('image') as File;

  const arrayBuffer = await file.arrayBuffer();
  const result = await client.optimize(Buffer.from(arrayBuffer), {
    format: ImageFormat.AUTO,
    quality: 85,
  });

  return NextResponse.json(result);
}
```

---

### 2. FastAPI (Python)
```python
# main.py
from fastapi import FastAPI, UploadFile, File
from smallpict import AsyncSmallPictClient, ImageFormat, OptimizeOptions
import os

app = FastAPI()
client = AsyncSmallPictClient(api_key=os.environ["SMALLPICT_API_KEY"])

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    contents = await image.read()
    result = await client.optimize(
        contents,
        options=OptimizeOptions(format=ImageFormat.WEBP, quality=80)
    )
    return {"url": result.url, "savings": result.savings_percentage}
```

---

### 3. Laravel 10/11 (PHP)
```php
// config/smallpict.php
return [
    'api_key' => env('SMALLPICT_API_KEY'),
    'secret_key' => env('SMALLPICT_SECRET_KEY'),
];

// app/Http/Controllers/MediaController.php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use SmallPict\Laravel\Facades\SmallPict;
use SmallPict\Models\OptimizeOptions;
use SmallPict\Models\ImageFormat;

class MediaController extends Controller
{
    public function upload(Request $request)
    {
        $file = $request->file('image');
        $result = SmallPict::optimize(
            $file->get(),
            new OptimizeOptions(ImageFormat::AUTO, 85)
        );

        return response()->json([
            'url' => $result->getUrl(),
            'saved' => $result->getSavingsPercentage() . '%'
        ]);
    }
}
```

---

### 4. Gin Web Framework (Go)
```go
package main

import (
	"io"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/tuxnoob/smallpict-go"
)

func main() {
	r := gin.Default()
	client, _ := smallpict.NewClient(smallpict.WithAPIKey(os.Getenv("SMALLPICT_API_KEY")))

	r.POST("/upload", func(c *gin.Context) {
		fileHeader, _ := c.FormFile("image")
		file, _ := fileHeader.Open()
		defer file.Close()

		data, _ := io.ReadAll(file)
		res, err := client.Optimize(c.Request.Context(), data, &smallpict.OptimizeOptions{
			Format:  smallpict.FormatAVIF,
			Quality: 85,
		})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, res)
	})

	r.Run(":8080")
}
```

---

### 5. Ruby on Rails ActiveStorage
```ruby
# config/storage.yml
smallpict:
  service: SmallPict
  api_key: <%= Rails.application.credentials.dig(:smallpict, :api_key) %>

# config/environments/production.rb
config.active_storage.service = :smallpict
```

---

### 6. Spring Boot 3 (Java)
```java
@RestController
@RequestMapping("/api/images")
public class ImageController {
    private final SmallPictClient client;

    public ImageController(SmallPictClient client) {
        this.client = client;
    }

    @PostMapping("/upload")
    public ResponseEntity<OptimizeResult> upload(@RequestParam("file") MultipartFile file) throws IOException {
        OptimizeResult result = client.optimize(
                file.getBytes(),
                OptimizeOptions.builder()
                        .filename(file.getOriginalFilename())
                        .format(ImageFormat.AVIF)
                        .quality(85)
                        .build()
        );
        return ResponseEntity.ok(result);
    }
}
```
