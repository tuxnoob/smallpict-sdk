package smallpict

import "time"

// Image formats supported for output transcoding.
const (
	FormatAuto = "auto"
	FormatAVIF = "avif"
	FormatWebP = "webp"
	FormatJPEG = "jpeg"
	FormatPNG  = "png"
)

// Resizing bounding box fit modes.
const (
	FitCover   = "cover"
	FitContain = "contain"
	FitInside  = "inside"
	FitOutside = "outside"
)

// Fallback behavior when account quota is exhausted.
const (
	FallbackThrow       = "throw"
	FallbackPassthrough = "passthrough"
)

// CDN cache invalidation scope.
const (
	PurgeTypeURL = "url"
	PurgeTypeAll = "all"
)

// OptimizeOptions contains transformation and compression parameters for an image.
type OptimizeOptions struct {
	Format         string `json:"format,omitempty"`
	Quality        int    `json:"quality,omitempty"`
	MaxWidth       int    `json:"max_width,omitempty"`
	MaxHeight      int    `json:"max_height,omitempty"`
	Fit            string `json:"fit,omitempty"`
	Lossless       bool   `json:"lossless,omitempty"`
	StripMetadata  bool   `json:"strip_metadata"`
	Filename       string `json:"filename,omitempty"`
	MIMEType       string `json:"mime_type,omitempty"`
	IdempotencyKey string `json:"-"`
}

// OptimizeResult represents the output from a successful image optimization.
type OptimizeResult struct {
	JobID             string  `json:"job_id"`
	Status            string  `json:"status"`
	URL               string  `json:"url"`
	Format            string  `json:"format"`
	OriginalSize      int64   `json:"original_size"`
	CompressedSize    int64   `json:"compressed_size"`
	BytesSaved        int64   `json:"bytes_saved"`
	SavingsPercentage float64 `json:"savings_percentage"`
	UploadURL         string  `json:"upload_url,omitempty"`
	Data              []byte  `json:"-"`
}

// QuotaResponse details the current monthly processing usage and account limits.
type QuotaResponse struct {
	Plan                string  `json:"plan"`
	BytesUsed           int64   `json:"bytes_used"`
	QuotaLimit          int64   `json:"quota_limit"`
	QuotaPercentage     float64 `json:"quota_percentage"`
	CDNEgressUsedBytes  *int64  `json:"cdn_egress_used_bytes,omitempty"`
	CDNEgressQuotaBytes *int64  `json:"cdn_egress_quota_bytes,omitempty"`
	ActiveKeysCount     *int    `json:"active_keys_count,omitempty"`
	ActiveSitesCount    *int    `json:"active_sites_count,omitempty"`
}

// PurgeResponse confirms enqueuing of a CDN cache invalidation request.
type PurgeResponse struct {
	Message string `json:"message"`
}

// JobStatusResult represents the current state of an asynchronous conversion job.
type JobStatusResult struct {
	JobID      string                 `json:"job_id"`
	Status     string                 `json:"status"`
	URL        string                 `json:"url,omitempty"`
	Format     string                 `json:"format,omitempty"`
	BytesSaved *int64                 `json:"bytes_saved,omitempty"`
	Error      map[string]interface{} `json:"error,omitempty"`
	CreatedAt  *time.Time             `json:"created_at,omitempty"`
	UpdatedAt  *time.Time             `json:"updated_at,omitempty"`
}
