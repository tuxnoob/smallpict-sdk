# SmallPict SDK Quickstart Comparison Matrix

This guide provides a side-by-side comparison of getting started with the official SmallPict SDK in **7 programming languages**.

---

## 📦 Package Matrix

| Language | Official Package | Package Registry | Minimum Runtime | Default Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Node.js / TS** | `@smallpict/sdk` | [npm](https://npmjs.com/package/@smallpict/sdk) | Node 18+ / Bun / Deno | Native `fetch` + Web Crypto |
| **Python** | `smallpict` | [PyPI](https://pypi.org/project/smallpict) | Python 3.9+ | `httpx` (Sync & Async) |
| **PHP** | `smallpict/smallpict-php` | [Packagist](https://packagist.org/packages/smallpict/smallpict-php) | PHP 7.4 - 8.4+ | Native cURL / PSR-18 |
| **Go** | `github.com/tuxnoob/smallpict-go` | [pkg.go.dev](https://pkg.go.dev/github.com/tuxnoob/smallpict-go) | Go 1.21+ | Go `net/http` Standard Lib |
| **Rust** | `smallpict` | [crates.io](https://crates.io/crates/smallpict) | Rust 1.75+ (MSRV) | `reqwest` + `rustls-tls` |
| **Ruby** | `smallpict` | [RubyGems](https://rubygems.org/gems/smallpict) | Ruby 3.0+ | `Faraday` + OpenSSL |
| **Java / Kotlin** | `com.smallpict:smallpict-java` | [Maven Central](https://search.maven.org) | Java 17+ | Java `HttpClient` + Jackson |

---

## ⚡ Hello World: Image Optimization

````carousel
```typescript
// Node.js / TypeScript
import { SmallPictClient, ImageFormat } from '@smallpict/sdk';
import * as fs from 'node:fs/promises';

const client = new SmallPictClient({
  apiKey: process.env.SMALLPICT_API_KEY!,
  secretKey: process.env.SMALLPICT_SECRET_KEY, // Optional HMAC Secret
});

const imageBuffer = await fs.readFile('hero-banner.png');
const result = await client.optimize(imageBuffer, {
  format: ImageFormat.AVIF,
  quality: 80,
  maxWidth: 1920,
});

console.log(`Optimized URL: ${result.url}`);
console.log(`Saved: ${result.savingsPercentage}% (${result.bytesSaved} bytes)`);
```
<!-- slide -->
```python
# Python
import os
from smallpict import SmallPictClient, ImageFormat, OptimizeOptions

client = SmallPictClient(
    api_key=os.environ["SMALLPICT_API_KEY"],
    secret_key=os.environ.get("SMALLPICT_SECRET_KEY"), # Optional HMAC Secret
)

with open("hero-banner.png", "rb") as f:
    image_bytes = f.read()

result = client.optimize(
    image_bytes,
    options=OptimizeOptions(format=ImageFormat.AVIF, quality=80, max_width=1920),
)

print(f"Optimized URL: {result.url}")
print(f"Saved: {result.savings_percentage}% ({result.bytes_saved} bytes)")
```
<!-- slide -->
```php
<?php
// PHP
require_once __DIR__ . '/vendor/autoload.php';

use SmallPict\Client;
use SmallPict\Models\OptimizeOptions;
use SmallPict\Models\ImageFormat;

$client = new Client(
    getenv('SMALLPICT_API_KEY'),
    getenv('SMALLPICT_SECRET_KEY') // Optional HMAC Secret
);

$imageContent = file_get_contents('hero-banner.png');
$result = $client->optimize(
    $imageContent,
    new OptimizeOptions(ImageFormat::AVIF, 80, 1920)
);

echo "Optimized URL: " . $result->getUrl() . "\n";
echo "Saved: " . $result->getSavingsPercentage() . "% (" . $result->getBytesSaved() . " bytes)\n";
```
<!-- slide -->
```go
// Go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/tuxnoob/smallpict-go"
)

func main() {
	client, err := smallpict.NewClient(
		smallpict.WithAPIKey(os.Getenv("SMALLPICT_API_KEY")),
		smallpict.WithSecretKey(os.Getenv("SMALLPICT_SECRET_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}

	result, err := client.OptimizeFile(context.Background(), "hero-banner.png", &smallpict.OptimizeOptions{
		Format:   smallpict.FormatAVIF,
		Quality:  80,
		MaxWidth: 1920,
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Optimized URL: %s\n", result.URL)
	fmt.Printf("Saved: %.2f%% (%d bytes)\n", result.SavingsPercentage, result.BytesSaved)
}
```
<!-- slide -->
```rust
// Rust
use smallpict::{Client, ImageFormat, OptimizeOptions};
use std::fs;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::builder()
        .api_key(std::env::var("SMALLPICT_API_KEY")?)
        .secret_key(std::env::var("SMALLPICT_SECRET_KEY").ok())
        .build()?;

    let image_bytes = fs::read("hero-banner.png")?;
    let options = OptimizeOptions::builder()
        .format(ImageFormat::Avif)
        .quality(80)
        .max_width(1920)
        .build();

    let result = client.optimize(&image_bytes, Some(options)).await?;
    println!("Optimized URL: {}", result.url);
    println!("Saved: {:.2}% ({} bytes)", result.savings_percentage, result.bytes_saved);
    Ok(())
}
```
<!-- slide -->
```ruby
# Ruby
require "smallpict"

SmallPict.configure do |config|
  config.api_key    = ENV["SMALLPICT_API_KEY"]
  config.secret_key = ENV["SMALLPICT_SECRET_KEY"]
end

image_data = File.binread("hero-banner.png")
result = SmallPict.optimize(
  image_data,
  format: "avif",
  quality: 80,
  max_width: 1920
)

puts "Optimized URL: #{result.url}"
puts "Saved: #{result.savings_percentage}% (#{result.bytes_saved} bytes)"
```
<!-- slide -->
```java
// Java
import com.smallpict.SmallPictClient;
import com.smallpict.models.ImageFormat;
import com.smallpict.models.OptimizeOptions;
import com.smallpict.models.OptimizeResult;
import java.io.File;

public class Main {
    public static void main(String[] args) {
        SmallPictClient client = SmallPictClient.builder()
                .apiKey(System.getenv("SMALLPICT_API_KEY"))
                .secretKey(System.getenv("SMALLPICT_SECRET_KEY"))
                .build();

        OptimizeResult result = client.optimize(
                new File("hero-banner.png"),
                OptimizeOptions.builder()
                        .format(ImageFormat.AVIF)
                        .quality(80)
                        .maxWidth(1920)
                        .build()
        );

        System.out.println("Optimized URL: " + result.getUrl());
        System.out.println("Saved: " + result.getSavingsPercentage() + "% (" + result.getBytesSaved() + " bytes)");
    }
}
```
````

---

## 📊 Account Quota & CDN Purge Comparison

| Method | Node.js | Python | PHP | Go | Rust | Ruby | Java |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Get Quota** | `client.getQuota()` | `client.get_quota()` | `$client->getQuota()` | `client.GetQuota(ctx)` | `client.get_quota().await` | `SmallPict.get_quota` | `client.getQuota()` |
| **Purge CDN** | `client.purgeCdn(urls)` | `client.purge_cdn(urls)` | `$client->purgeCdn($urls)` | `client.PurgeCDN(ctx, urls, type)` | `client.purge_cdn(&urls, type).await` | `SmallPict.purge_cdn(urls)` | `client.purgeCdn(urls, type)` |
| **Validate Key** | `client.validateKey()` | `client.validate_key()` | `$client->validateKey()` | `client.ValidateKey(ctx)` | `client.validate_key().await` | `SmallPict.validate_key` | `client.validateKey()` |
| **Job Status** | `client.getJobStatus(id)` | `client.get_job_status(id)` | `$client->getJobStatus($id)` | `client.GetJobStatus(ctx, id)` | `client.get_job_status(id).await` | `SmallPict.get_job_status(id)` | `client.getJobStatus(id)` |
