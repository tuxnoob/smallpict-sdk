package smallpict

import (
	"testing"
)

func TestCryptoUtilities(t *testing.T) {
	if EmptySHA256 != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" {
		t.Fatalf("unexpected EmptySHA256 constant: %s", EmptySHA256)
	}

	if h := SHA256Hex(nil); h != EmptySHA256 {
		t.Fatalf("expected empty SHA256, got: %s", h)
	}

	if h := SHA256Hex([]byte("hello world")); h != "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9" {
		t.Fatalf("unexpected SHA256 for 'hello world': %s", h)
	}

	stringToSign := BuildStringToSign("POST", "/v1/optimize", "1716301234", EmptySHA256)
	expectedSTS := "POST\n/v1/optimize\n1716301234\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
	if stringToSign != expectedSTS {
		t.Fatalf("unexpected string to sign: %s", stringToSign)
	}

	sig := HMACSHA256Hex("sec_test_secret_key_123", stringToSign)
	if len(sig) != 64 {
		t.Fatalf("expected 64 character signature, got len %d: %s", len(sig), sig)
	}
}

func TestSanitizeMessage(t *testing.T) {
	raw := "Failed key sp_live_1234567890abcdef1234567890abcdef with sec_secret123456"
	sanitized := SanitizeMessage(raw)

	if sanitized == raw {
		t.Fatalf("expected sanitization, got raw: %s", sanitized)
	}
	if len(sanitized) == 0 {
		t.Fatal("expected non-empty sanitized string")
	}
}
