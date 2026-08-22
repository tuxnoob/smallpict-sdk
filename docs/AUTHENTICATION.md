# SmallPict Authentication & Cryptographic Signing Guide

SmallPict supports two authentication schemes:
1. **Bearer Token Authentication** (Standard & Quick).
2. **HMAC-SHA256 Request Signing** (Enterprise, Tamper-Proof, & Replay-Protected).

---

## 🔐 1. Bearer Token Authentication

When initialized with only an `apiKey`, the SDK includes an `Authorization: Bearer <API_KEY>` or `X-API-Key: <API_KEY>` header with each request.

```http
POST /v1/optimize HTTP/1.1
Host: api.tuxnoob.com
Authorization: Bearer sp_live_1234567890abcdef1234567890abcdef
Content-Type: application/json
```

---

## 🛡️ 2. HMAC-SHA256 Request Signing

When initialized with both `apiKey` and `secretKey`, the SDK automatically generates a cryptographic HMAC signature for each request, protecting against data tampering and replay attacks.

### Canonical String to Sign
The SDK constructs a 4-line newline-separated canonical string:

```text
HTTP_METHOD
CANONICAL_URI_PATH
TIMESTAMP_IN_SECONDS
HEX_ENCODED_SHA256_OF_REQUEST_BODY
```

> [!NOTE]
> For requests with an empty body (e.g. `GET /v1/quota`), the empty body SHA-256 constant is used:
> `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

### Headers Sent
```http
POST /v1/optimize HTTP/1.1
Host: api.tuxnoob.com
X-API-Key: sp_live_1234567890abcdef1234567890abcdef
X-Timestamp: 1716301234
X-Signature: a1b2c3d4e5f67890... (64 hex characters)
Content-Type: application/json
```

---

## 🧪 Signing Examples Across Languages

````carousel
```typescript
// Node.js (Web Crypto)
const bodyHash = body ? await sha256Hex(body) : EMPTY_SHA256;
const stringToSign = `${method.toUpperCase()}\n${path}\n${timestamp}\n${bodyHash}`;
const signature = await hmacSha256Hex(secretKey, stringToSign);
```
<!-- slide -->
```python
# Python (hashlib & hmac)
import hashlib, hmac
body_hash = hashlib.sha256(body_bytes).hexdigest() if body_bytes else EMPTY_SHA256
string_to_sign = f"{method.upper()}\n{path}\n{timestamp}\n{body_hash}"
signature = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).hexdigest()
```
<!-- slide -->
```php
<?php
// PHP (hash_hmac & hash)
$bodyHash = !empty($body) ? hash('sha256', $body) : Crypto::EMPTY_SHA256;
$stringToSign = strtoupper($method) . "\n" . $path . "\n" . $timestamp . "\n" . $bodyHash;
$signature = hash_hmac('sha256', $stringToSign, $secretKey);
```
<!-- slide -->
```go
// Go (crypto/hmac & crypto/sha256)
bodyHash := sha256Hex(bodyBytes)
stringToSign := fmt.Sprintf("%s\n%s\n%s\n%s", strings.ToUpper(method), path, timestamp, bodyHash)
mac := hmac.New(sha256.New, []byte(secretKey))
mac.Write([]byte(stringToSign))
signature := hex.EncodeToString(mac.Sum(nil))
```
<!-- slide -->
```rust
// Rust (hmac & sha2)
let body_hash = sha256_hex(&body_bytes);
let string_to_sign = format!("{}\n{}\n{}\n{}", method.as_str().to_uppercase(), path, timestamp, body_hash);
let mut mac = HmacSha256::new_from_slice(secret_key.as_bytes())?;
mac.update(string_to_sign.as_bytes());
let signature = hex::encode(mac.finalize().into_bytes());
```
<!-- slide -->
```ruby
# Ruby (OpenSSL::HMAC & Digest::SHA256)
body_hash = body.nil? || body.empty? ? EMPTY_SHA256 : Digest::SHA256.hexdigest(body)
string_to_sign = "#{method.upcase}\n#{path}\n#{timestamp}\n#{body_hash}"
signature = OpenSSL::HMAC.hexdigest("SHA256", secret_key, string_to_sign)
```
<!-- slide -->
```java
// Java (javax.crypto.Mac & MessageDigest)
String bodyHash = bodyBytes != null && bodyBytes.length > 0 ? sha256Hex(bodyBytes) : EMPTY_SHA256;
String stringToSign = method.toUpperCase() + "\n" + path + "\n" + timestamp + "\n" + bodyHash;
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(secretKey.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
String signature = bytesToHex(mac.doFinal(stringToSign.getBytes(StandardCharsets.UTF_8)));
```
````
