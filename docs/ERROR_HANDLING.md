# SmallPict Unified Error Handling Taxonomy

SmallPict uses structured HTTP error codes and JSON error envelopes. Every SDK maps server errors to a language-idiomatic exception hierarchy.

---

## 🛑 Error Taxonomy Matrix

| HTTP Status | Error Code | Exception Class (Node/TS/PHP/Ruby) | Exception Class (Python) | Exception Class (Go) | Exception Class (Rust) | Exception Class (Java) | Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **400** | `VALIDATION_FAILED` | `ValidationError` | `ValidationError` | `ErrValidation` / `IsValidationError()` | `SmallPictError::Validation` | `ValidationException` | Invalid options or corrupted payload. |
| **401** | `UNAUTHORIZED` | `AuthenticationError` | `AuthenticationError` | `ErrAuthentication` / `IsAuthError()` | `SmallPictError::Authentication` | `AuthenticationException` | Invalid, expired, or missing API Key. |
| **402** | `QUOTA_EXCEEDED` | `QuotaExceededError` | `QuotaExceededError` | `ErrQuotaExceeded` / `IsQuotaError()` | `SmallPictError::QuotaExceeded` | `QuotaExceededException` | Account monthly processing quota full. |
| **403** | `FORBIDDEN` | `PermissionDeniedError` | `PermissionDeniedError`| `ErrPermissionDenied` | `SmallPictError::PermissionDenied` | `PermissionDeniedException` | Missing required permissions or domain restricted. |
| **404** | `NOT_FOUND` | `NotFoundError` | `NotFoundError` | `ErrNotFound` | `SmallPictError::NotFound` | `NotFoundException` | Job ID or resource was not found. |
| **429** | `RATE_LIMIT_EXCEEDED`| `RateLimitError` | `RateLimitError` | `ErrRateLimit` | `SmallPictError::RateLimit` | `RateLimitException` | Request throughput throttle exceeded. |
| **500-504**| `INTERNAL_ERROR` | `ServerError` | `ServerError` | `ErrServer` | `SmallPictError::Server` | `ServerException` | Transient server error on Edge worker. |
| **408 / -**| `TIMEOUT_ERROR` | `TimeoutError` | `TimeoutError` | `ErrTimeout` | `SmallPictError::Timeout` | `TimeoutException` | Network connection or read timeout. |
| **-** | `NETWORK_ERROR` | `NetworkError` | `NetworkError` | `ErrNetwork` | `SmallPictError::Network` | `NetworkException` | DNS, socket, or connection failure. |

---

## 💻 Catching Errors in Code

````carousel
```typescript
// Node.js / TypeScript
import { SmallPictClient, QuotaExceededError, RateLimitError } from '@smallpict/sdk';

try {
  const result = await client.optimize(buffer);
} catch (error) {
  if (error instanceof QuotaExceededError) {
    console.warn("Storage quota full, prompt upgrade.");
  } else if (error instanceof RateLimitError) {
    console.warn(`Throttled. Retry after ${error.retryAfter}s`);
  }
}
```
<!-- slide -->
```python
# Python
from smallpict import SmallPictClient
from smallpict.errors import QuotaExceededError, RateLimitError

try:
    result = client.optimize(image_bytes)
except QuotaExceededError:
    print("Monthly quota exhausted.")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds.")
```
<!-- slide -->
```php
<?php
// PHP
use SmallPict\Exceptions\QuotaExceededException;
use SmallPict\Exceptions\RateLimitException;

try {
    $result = $client->optimize($imageBytes);
} catch (QuotaExceededException $e) {
    echo "Quota exceeded. Upgrade your tier.\n";
} catch (RateLimitException $e) {
    echo "Rate limit reached. Retry in " . $e->getRetryAfter() . " seconds.\n";
}
```
<!-- slide -->
```go
// Go
package main

import (
	"context"
	"fmt"
	"github.com/tuxnoob/smallpict-go"
)

result, err := client.Optimize(ctx, data, options)
if err != nil {
	if smallpict.IsQuotaError(err) {
		fmt.Println("Quota exceeded!")
	} else if smallpict.IsRateLimitError(err) {
		fmt.Printf("Throttled: %v\n", err)
	}
}
```
<!-- slide -->
```rust
// Rust
use smallpict::SmallPictError;

match client.optimize(&image_bytes, None).await {
    Ok(result) => println!("Success: {}", result.url),
    Err(SmallPictError::QuotaExceeded { message, .. }) => println!("Quota full: {}", message),
    Err(SmallPictError::RateLimit { retry_after, .. }) => println!("Rate limited. Retry after: {:?}", retry_after),
    Err(err) => eprintln!("Error: {}", err),
}
```
<!-- slide -->
```ruby
# Ruby
begin
  result = SmallPict.optimize(image_data)
rescue SmallPict::QuotaExceededError
  puts "Account quota reached."
rescue SmallPict::RateLimitError => e
  puts "Rate limited, retry after #{e.retry_after} seconds"
end
```
<!-- slide -->
```java
// Java
import com.smallpict.errors.QuotaExceededException;
import com.smallpict.errors.RateLimitException;

try {
    OptimizeResult result = client.optimize(file, options);
} catch (QuotaExceededException e) {
    System.out.println("Plan quota exceeded!");
} catch (RateLimitException e) {
    System.out.printf("Rate limit reached. Retry after %d seconds\n", e.getRetryAfterSeconds());
}
```
````
