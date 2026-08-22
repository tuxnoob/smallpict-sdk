# frozen_string_literal: true

require "spec_helper"

RSpec.describe SmallPict::Error do
  describe ".sanitize" do
    it "masks api keys and secrets" do
      raw = "Invalid key sp_live_1234567890abcdef1234567890abcdef with sec_secret123456"
      sanitized = described_class.sanitize(raw)
      expect(sanitized).not_to include("sp_live_1234567890abcdef1234567890abcdef")
      expect(sanitized).not_to include("sec_secret123456")
      expect(sanitized).to include("sp_live_12...cdef")
      expect(sanitized).to include("***REDACTED***")
    end
  end

  describe "#to_s" do
    it "formats error with code, status, and request id" do
      err = SmallPict::AuthenticationError.new("Access denied with key sp_test_11223344556677889900", request_id: "req_001")
      str = err.to_s
      expect(str).not_to include("sp_test_11223344556677889900")
      expect(str).to include("[UNAUTHORIZED HTTP 401]")
      expect(str).to include("Request ID: req_001")
    end
  end

  describe "subclasses" do
    it "provides proper status codes and error codes" do
      expect(SmallPict::ValidationError.new.status_code).to eq(400)
      expect(SmallPict::AuthenticationError.new.status_code).to eq(401)
      expect(SmallPict::QuotaExceededError.new.status_code).to eq(402)
      expect(SmallPict::PermissionDeniedError.new.status_code).to eq(403)
      expect(SmallPict::NotFoundError.new.status_code).to eq(404)
      expect(SmallPict::RateLimitError.new.status_code).to eq(429)
      expect(SmallPict::ServerError.new.status_code).to eq(500)
      expect(SmallPict::TimeoutError.new.status_code).to eq(408)
    end
  end
end
