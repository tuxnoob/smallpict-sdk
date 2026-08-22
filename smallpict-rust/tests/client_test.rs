use smallpict::{Client, ClientBuilder, FallbackMode};
use std::time::Duration;

#[tokio::test]
async fn test_client_builder_missing_api_key() {
    let res = ClientBuilder::new().api_key("").build();
    assert!(res.is_err());
    let err = res.unwrap_err();
    assert!(err.is_validation_error());
}

#[tokio::test]
async fn test_client_builder_configuration() {
    let client = Client::builder()
        .api_key("sp_live_test_1234567890")
        .secret_key("sec_test_secret_123")
        .base_url("https://custom.api.com")
        .timeout(Duration::from_secs(15))
        .max_retries(5)
        .fallback_mode(FallbackMode::Passthrough)
        .build()
        .expect("valid client");

    assert!(!client.validate_key().await); // no server at custom.api.com
}

#[cfg(feature = "blocking")]
#[test]
fn test_blocking_client_builder() {
    use smallpict::blocking::BlockingClient;

    let res = BlockingClient::builder().api_key("").build();
    assert!(res.is_err());

    let client = BlockingClient::builder()
        .api_key("sp_live_test_blocking_12345")
        .build()
        .expect("valid blocking client");

    assert!(!client.validate_key());
}
