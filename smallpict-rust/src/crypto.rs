use hmac::{Hmac, Mac};
use sha2::{Digest, Sha256};

type HmacSha256 = Hmac<Sha256>;

/// SHA-256 hex digest of an empty byte slice.
pub const EMPTY_SHA256: &str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";

/// Computes the hexadecimal lowercase SHA-256 hash of a byte slice.
pub fn sha256_hex(data: &[u8]) -> String {
    if data.is_empty() {
        return EMPTY_SHA256.to_string();
    }
    let mut hasher = Sha256::new();
    hasher.update(data);
    hex::encode(hasher.finalize())
}

/// Generates an HMAC-SHA256 signature formatted as a 64-character lowercase hex string.
pub fn hmac_sha256_hex(secret_key: &str, string_to_sign: &str) -> String {
    let mut mac = HmacSha256::new_from_slice(secret_key.as_bytes())
        .expect("HMAC can take key of any size");
    mac.update(string_to_sign.as_bytes());
    hex::encode(mac.finalize().into_bytes())
}

/// Constructs the canonical string-to-sign per the OpenAPI 3.1 specification contract.
pub fn build_string_to_sign(method: &str, path: &str, timestamp: &str, body_hash: &str) -> String {
    let clean_path = if path.starts_with('/') {
        path.to_string()
    } else {
        format!("/{}", path)
    };
    format!(
        "{}\n{}\n{}\n{}",
        method.to_uppercase(),
        clean_path,
        timestamp,
        body_hash
    )
}
