use serde::{Deserialize, Serialize};
use std::fmt;

/// Output format for image transcoding.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum ImageFormat {
    #[default]
    Auto,
    Avif,
    Webp,
    Jpeg,
    Png,
}

impl fmt::Display for ImageFormat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Auto => write!(f, "auto"),
            Self::Avif => write!(f, "avif"),
            Self::Webp => write!(f, "webp"),
            Self::Jpeg => write!(f, "jpeg"),
            Self::Png => write!(f, "png"),
        }
    }
}

/// Bounding box resizing strategy.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum FitMode {
    #[default]
    Cover,
    Contain,
    Inside,
    Outside,
}

impl fmt::Display for FitMode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Cover => write!(f, "cover"),
            Self::Contain => write!(f, "contain"),
            Self::Inside => write!(f, "inside"),
            Self::Outside => write!(f, "outside"),
        }
    }
}

/// Action to take if storage or processing quota limit is reached.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum FallbackMode {
    #[default]
    Throw,
    Passthrough,
}

/// CDN cache invalidation scope.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum PurgeType {
    #[default]
    Url,
    All,
}

impl fmt::Display for PurgeType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Url => write!(f, "url"),
            Self::All => write!(f, "all"),
        }
    }
}

/// Image optimization options payload.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OptimizeOptions {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format: Option<ImageFormat>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub quality: Option<u8>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub max_width: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub max_height: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub fit: Option<FitMode>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub lossless: Option<bool>,
    pub strip_metadata: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filename: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub mime_type: Option<String>,
    #[serde(skip)]
    pub idempotency_key: Option<String>,
}

impl Default for OptimizeOptions {
    fn default() -> Self {
        Self {
            format: Some(ImageFormat::Auto),
            quality: Some(80),
            max_width: None,
            max_height: None,
            fit: Some(FitMode::Cover),
            lossless: Some(false),
            strip_metadata: true,
            filename: None,
            mime_type: None,
            idempotency_key: None,
        }
    }
}

impl OptimizeOptions {
    pub fn builder() -> OptimizeOptionsBuilder {
        OptimizeOptionsBuilder::default()
    }
}

/// Builder for constructing [`OptimizeOptions`].
#[derive(Debug, Default, Clone)]
pub struct OptimizeOptionsBuilder {
    options: OptimizeOptions,
}

impl OptimizeOptionsBuilder {
    pub fn format(mut self, format: ImageFormat) -> Self {
        self.options.format = Some(format);
        self
    }

    pub fn quality(mut self, quality: u8) -> Self {
        self.options.quality = Some(quality.clamp(1, 100));
        self
    }

    pub fn max_width(mut self, width: u32) -> Self {
        self.options.max_width = Some(width);
        self
    }

    pub fn max_height(mut self, height: u32) -> Self {
        self.options.max_height = Some(height);
        self
    }

    pub fn fit(mut self, fit: FitMode) -> Self {
        self.options.fit = Some(fit);
        self
    }

    pub fn lossless(mut self, lossless: bool) -> Self {
        self.options.lossless = Some(lossless);
        self
    }

    pub fn strip_metadata(mut self, strip: bool) -> Self {
        self.options.strip_metadata = strip;
        self
    }

    pub fn filename(mut self, name: impl Into<String>) -> Self {
        self.options.filename = Some(name.into());
        self
    }

    pub fn mime_type(mut self, mime: impl Into<String>) -> Self {
        self.options.mime_type = Some(mime.into());
        self
    }

    pub fn idempotency_key(mut self, key: impl Into<String>) -> Self {
        self.options.idempotency_key = Some(key.into());
        self
    }

    pub fn build(self) -> OptimizeOptions {
        self.options
    }
}

/// Result of an image optimization operation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OptimizeResult {
    pub job_id: String,
    pub status: String,
    pub url: String,
    pub format: String,
    pub original_size: u64,
    pub compressed_size: u64,
    pub bytes_saved: u64,
    pub savings_percentage: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub upload_url: Option<String>,
    #[serde(skip)]
    pub data: Option<Vec<u8>>,
}

/// Real-time quota and usage metrics.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuotaResponse {
    pub plan: String,
    pub bytes_used: u64,
    pub quota_limit: u64,
    pub quota_percentage: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cdn_egress_used_bytes: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cdn_egress_quota_bytes: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub active_keys_count: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub active_sites_count: Option<u32>,
}

/// CDN cache purge response.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PurgeResponse {
    pub message: String,
}

/// Progress status of an asynchronous image conversion task.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JobStatusResult {
    pub job_id: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub url: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub bytes_saved: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub created_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}
