package smallpict

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"testing"
	"time"
)

type roundTripFunc func(req *http.Request) *http.Response

func (f roundTripFunc) RoundTrip(req *http.Request) (*http.Response, error) {
	return f(req), nil
}

func newMockHTTPClient(fn roundTripFunc) *http.Client {
	return &http.Client{
		Transport: fn,
	}
}

func TestNewClientMissingKey(t *testing.T) {
	_, err := NewClient(WithAPIKey(""))
	if err == nil {
		t.Fatal("expected error on missing API key")
	}
	if !IsValidationError(err) {
		t.Fatalf("expected validation error, got: %v", err)
	}
}

func TestOptimizeSuccess(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		if r.URL.Path != "/v1/optimize" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		if r.Header.Get("X-API-Key") != "sp_live_testkey_1234567890" {
			t.Errorf("unexpected API key: %s", r.Header.Get("X-API-Key"))
		}
		if r.Header.Get("X-Signature") == "" {
			t.Error("missing X-Signature header")
		}
		if r.Header.Get("Idempotency-Key") == "" {
			t.Error("missing Idempotency-Key header")
		}

		respBody, _ := json.Marshal(map[string]interface{}{
			"job_id":             "job_go_123",
			"status":             "completed",
			"url":                "https://cdn.smallpict.com/opt/hero.avif",
			"format":             "avif",
			"original_size":      float64(100000),
			"compressed_size":    float64(15000),
			"bytes_saved":        float64(85000),
			"savings_percentage": 85.0,
		})

		return &http.Response{
			StatusCode: http.StatusOK,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, err := NewClient(
		WithAPIKey("sp_live_testkey_1234567890"),
		WithSecretKey("sec_test_secret_123"),
		WithHTTPClient(mockClient),
	)
	if err != nil {
		t.Fatalf("unexpected NewClient error: %v", err)
	}

	buf := bytes.NewBufferString("fake image payload bytes")
	res, err := client.Optimize(context.Background(), buf, &OptimizeOptions{
		Format:  FormatAVIF,
		Quality: 85,
	})
	if err != nil {
		t.Fatalf("unexpected Optimize error: %v", err)
	}

	if res.JobID != "job_go_123" {
		t.Errorf("unexpected JobID: %s", res.JobID)
	}
	if res.URL != "https://cdn.smallpict.com/opt/hero.avif" {
		t.Errorf("unexpected URL: %s", res.URL)
	}
	if res.SavingsPercentage != 85.0 {
		t.Errorf("unexpected SavingsPercentage: %f", res.SavingsPercentage)
	}
}

func TestOptimizeFile(t *testing.T) {
	tmpDir := t.TempDir()
	tmpFile := filepath.Join(tmpDir, "test.png")
	_ = os.WriteFile(tmpFile, []byte("test binary png"), 0600)

	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		respBody, _ := json.Marshal(map[string]interface{}{
			"job_id":             "job_file_1",
			"status":             "completed",
			"url":                "https://cdn.smallpict.com/opt/test.webp",
			"format":             "webp",
			"original_size":      float64(15),
			"compressed_size":    float64(5),
			"bytes_saved":        float64(10),
			"savings_percentage": 66.67,
		})
		return &http.Response{
			StatusCode: http.StatusOK,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, _ := NewClient(WithAPIKey("sp_live_test"), WithHTTPClient(mockClient))
	res, err := client.OptimizeFile(context.Background(), tmpFile, &OptimizeOptions{
		Format: FormatWebP,
	})
	if err != nil {
		t.Fatalf("unexpected OptimizeFile error: %v", err)
	}
	if res.JobID != "job_file_1" {
		t.Errorf("unexpected JobID: %s", res.JobID)
	}
}

func TestGetQuota(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		if r.URL.Path != "/v1/quota" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		respBody, _ := json.Marshal(map[string]interface{}{
			"plan":             "api_velocity",
			"bytes_used":       float64(5000000),
			"quota_limit":      float64(10000000),
			"quota_percentage": 50.0,
		})
		return &http.Response{
			StatusCode: http.StatusOK,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, err := NewClient(
		WithAPIKey("sp_live_test"),
		WithHTTPClient(mockClient),
	)
	if err != nil {
		t.Fatalf("unexpected NewClient error: %v", err)
	}

	quota, err := client.GetQuota(context.Background())
	if err != nil {
		t.Fatalf("unexpected GetQuota error: %v", err)
	}
	if quota.Plan != "api_velocity" {
		t.Errorf("unexpected Plan: %s", quota.Plan)
	}
	if quota.BytesUsed != 5000000 {
		t.Errorf("unexpected BytesUsed: %d", quota.BytesUsed)
	}
}

func TestPurgeCDN(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		if r.URL.Path != "/v1/purge" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		respBody, _ := json.Marshal(map[string]interface{}{
			"message": "Purge accepted",
		})
		return &http.Response{
			StatusCode: http.StatusAccepted,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, err := NewClient(
		WithAPIKey("sp_live_test"),
		WithHTTPClient(mockClient),
	)
	if err != nil {
		t.Fatalf("unexpected NewClient error: %v", err)
	}

	res, err := client.PurgeCDN(context.Background(), []string{"https://cdn.smallpict.com/opt/hero.avif"}, PurgeTypeURL)
	if err != nil {
		t.Fatalf("unexpected PurgeCDN error: %v", err)
	}
	if res.Message != "Purge accepted" {
		t.Errorf("unexpected Message: %s", res.Message)
	}
}

func TestGetJobStatus(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		respBody, _ := json.Marshal(map[string]interface{}{
			"job_id":      "job_async_123",
			"status":      "completed",
			"url":         "https://cdn.smallpict.com/opt/async.avif",
			"format":      "avif",
			"bytes_saved": float64(45000),
		})
		return &http.Response{
			StatusCode: http.StatusOK,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, _ := NewClient(WithAPIKey("sp_live_test"), WithHTTPClient(mockClient))
	res, err := client.GetJobStatus(context.Background(), "job_async_123")
	if err != nil {
		t.Fatalf("unexpected GetJobStatus error: %v", err)
	}
	if res.Status != "completed" {
		t.Errorf("unexpected status: %s", res.Status)
	}
	if res.URL != "https://cdn.smallpict.com/opt/async.avif" {
		t.Errorf("unexpected URL: %s", res.URL)
	}
}

func TestValidateKey(t *testing.T) {
	validMock := newMockHTTPClient(func(r *http.Request) *http.Response {
		if r.Header.Get("X-API-Key") == "sp_live_valid" {
			respBody, _ := json.Marshal(map[string]interface{}{"plan": "free"})
			return &http.Response{
				StatusCode: http.StatusOK,
				Header:     http.Header{"Content-Type": []string{"application/json"}},
				Body:       io.NopCloser(bytes.NewReader(respBody)),
			}
		}
		respBody, _ := json.Marshal(map[string]interface{}{"error": map[string]interface{}{"code": "UNAUTHORIZED"}})
		return &http.Response{
			StatusCode: http.StatusUnauthorized,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	validClient, _ := NewClient(WithAPIKey("sp_live_valid"), WithHTTPClient(validMock))
	if !validClient.ValidateKey(context.Background()) {
		t.Error("expected valid key to return true")
	}

	invalidClient, _ := NewClient(WithAPIKey("sp_live_invalid"), WithHTTPClient(validMock))
	if invalidClient.ValidateKey(context.Background()) {
		t.Error("expected invalid key to return false")
	}
}

func TestFallbackPassthrough(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		respBody, _ := json.Marshal(map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "QUOTA_EXCEEDED",
				"message": "Storage quota exhausted",
			},
		})
		return &http.Response{
			StatusCode: http.StatusPaymentRequired,
			Header:     http.Header{"Content-Type": []string{"application/json"}},
			Body:       io.NopCloser(bytes.NewReader(respBody)),
		}
	})

	client, err := NewClient(
		WithAPIKey("sp_live_test"),
		WithFallbackMode(FallbackPassthrough),
		WithHTTPClient(mockClient),
	)
	if err != nil {
		t.Fatalf("unexpected NewClient error: %v", err)
	}

	rawBytes := []byte("raw image data")
	res, err := client.OptimizeBytes(context.Background(), rawBytes, &OptimizeOptions{
		Filename: "photo.jpg",
		MIMEType: "image/jpeg",
	})
	if err != nil {
		t.Fatalf("expected passthrough, got error: %v", err)
	}
	if res.JobID != "fallback-passthrough" {
		t.Errorf("unexpected JobID: %s", res.JobID)
	}
	if res.SavingsPercentage != 0.0 {
		t.Errorf("unexpected SavingsPercentage: %f", res.SavingsPercentage)
	}
}

func TestErrorPredicates(t *testing.T) {
	validationErr := &Error{Code: "VALIDATION_FAILED", StatusCode: 400, Message: "Bad params"}
	if !IsValidationError(validationErr) {
		t.Error("expected IsValidationError true")
	}

	unauthErr := &Error{Code: "UNAUTHORIZED", StatusCode: 401, Message: "Unauthorized"}
	if !IsUnauthorized(unauthErr) {
		t.Error("expected IsUnauthorized true")
	}

	quotaErr := &Error{Code: "QUOTA_EXCEEDED", StatusCode: 402, Message: "Over quota"}
	if !IsQuotaExceeded(quotaErr) {
		t.Error("expected IsQuotaExceeded true")
	}

	forbiddenErr := &Error{Code: "FORBIDDEN", StatusCode: 403, Message: "Forbidden"}
	if !IsPermissionDenied(forbiddenErr) {
		t.Error("expected IsPermissionDenied true")
	}

	notFoundErr := &Error{Code: "NOT_FOUND", StatusCode: 404, Message: "Not found"}
	if !IsNotFound(notFoundErr) {
		t.Error("expected IsNotFound true")
	}

	rateLimitErr := &Error{Code: "RATE_LIMIT_EXCEEDED", StatusCode: 429, Message: "Slow down"}
	if !IsRateLimit(rateLimitErr) {
		t.Error("expected IsRateLimit true")
	}

	serverErr := &Error{Code: "INTERNAL_ERROR", StatusCode: 500, Message: "Crash"}
	if !IsServer(serverErr) {
		t.Error("expected IsServer true")
	}

	if fmt.Sprintf("%v", validationErr) == "" {
		t.Error("expected non-empty Error string")
	}
}

func TestContextCancellation(t *testing.T) {
	mockClient := newMockHTTPClient(func(r *http.Request) *http.Response {
		time.Sleep(50 * time.Millisecond)
		return &http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader([]byte(`{"plan":"free"}`))),
		}
	})

	client, _ := NewClient(WithAPIKey("sp_live_test"), WithHTTPClient(mockClient))

	ctx, cancel := context.WithCancel(context.Background())
	cancel() // cancel immediately

	_, err := client.GetQuota(ctx)
	if err == nil {
		t.Fatal("expected error on canceled context")
	}
}
