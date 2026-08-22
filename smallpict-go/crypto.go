package smallpict

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strings"
)

// EmptySHA256 is the standard SHA-256 hash of an empty byte slice.
const EmptySHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

// SHA256Hex computes the lowercase hexadecimal SHA-256 digest of data.
func SHA256Hex(data []byte) string {
	if len(data) == 0 {
		return EmptySHA256
	}
	h := sha256.Sum256(data)
	return hex.EncodeToString(h[:])
}

// HMACSHA256Hex computes the hexadecimal HMAC-SHA256 signature for a string using secretKey.
func HMACSHA256Hex(secretKey, stringToSign string) string {
	mac := hmac.New(sha256.New, []byte(secretKey))
	mac.Write([]byte(stringToSign))
	return hex.EncodeToString(mac.Sum(nil))
}

// BuildStringToSign formats the canonical string-to-sign per the OpenAPI 3.1 contract.
func BuildStringToSign(method, path, timestamp, bodyHash string) string {
	cleanPath := path
	if !strings.HasPrefix(cleanPath, "/") {
		cleanPath = "/" + cleanPath
	}
	return fmt.Sprintf("%s\n%s\n%s\n%s", strings.ToUpper(method), cleanPath, timestamp, bodyHash)
}
