# Changelog

All notable changes to the `smallpict` gem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-22

### Added
- Official Ruby SDK implementation for SmallPict OpenAPI 3.1.0 API.
- Block-based global configuration (`SmallPict.configure { |c| ... }`) and standalone client instances (`SmallPict::Client.new`).
- Rails ActiveStorage Service adapter (`SmallPict::ActiveStorage::Service`).
- 4 unified core client methods: `optimize`, `get_quota`, `purge_cdn`, and `validate_key`.
- Helper `get_job_status` for polling asynchronous image conversion tasks.
- Faraday connection pooling with automatic retry and jitter on HTTP 429/5xx.
- Custom exception hierarchy with automatic secret redaction in `to_s` and `inspect`.
- Optional `:passthrough` fallback mode on quota limit exhaustion.
