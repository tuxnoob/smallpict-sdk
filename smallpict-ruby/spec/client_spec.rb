# frozen_string_literal: true

require "spec_helper"

RSpec.describe SmallPict::Client do
  let(:api_key) { "sp_live_test_1234567890" }
  let(:secret_key) { "sec_test_secret_123" }
  let(:base_url) { "https://api.smallpict.app" }
  let(:client) { described_class.new(api_key: api_key, secret_key: secret_key, base_url: base_url) }

  describe "#initialize" do
    it "raises ValidationError when api_key is missing" do
      expect { described_class.new(api_key: "") }.to raise_error(SmallPict::ValidationError)
    end
  end

  describe "#optimize" do
    it "sends optimization request and returns OptimizeResult" do
      stub_request(:post, "#{base_url}/v1/optimize")
        .with(
          headers: {
            "Accept"          => "application/json",
            "Content-Type"    => "application/json",
            "X-Api-Key"       => api_key
          }
        )
        .to_return(
          status: 200,
          headers: { "Content-Type" => "application/json" },
          body: JSON.generate({
            job_id:             "job_rb_123",
            status:             "completed",
            url:                "https://cdn.smallpict.app/opt/photo.avif",
            format:             "avif",
            original_size:      100_000,
            compressed_size:    15_000,
            bytes_saved:        85_000,
            savings_percentage: 85.0
          })
        )

      result = client.optimize("fake image data", format: "avif", quality: 85)

      expect(result.job_id).to eq("job_rb_123")
      expect(result.status).to eq("completed")
      expect(result.url).to eq("https://cdn.smallpict.app/opt/photo.avif")
      expect(result.savings_percentage).to eq(85.0)
    end

    it "handles fallback passthrough on 402 quota exceeded" do
      stub_request(:post, "#{base_url}/v1/optimize")
        .to_return(
          status: 402,
          headers: { "Content-Type" => "application/json" },
          body: JSON.generate({
            error: { code: "QUOTA_EXCEEDED", message: "Monthly quota full" }
          })
        )

      passthrough_client = described_class.new(
        api_key:       api_key,
        base_url:      base_url,
        fallback_mode: :passthrough
      )

      res = passthrough_client.optimize("raw binary test data", filename: "photo.jpg", mime_type: "image/jpeg")

      expect(res.job_id).to eq("fallback-passthrough")
      expect(res.status).to eq("completed")
      expect(res.savings_percentage).to eq(0.0)
    end
  end

  describe "#get_quota" do
    it "retrieves quota metrics" do
      stub_request(:get, "#{base_url}/v1/quota")
        .to_return(
          status: 200,
          headers: { "Content-Type" => "application/json" },
          body: JSON.generate({
            plan:             "api_velocity",
            bytes_used:       2_500_000,
            quota_limit:      10_000_000,
            quota_percentage: 25.0
          })
        )

      quota = client.get_quota
      expect(quota.plan).to eq("api_velocity")
      expect(quota.bytes_used).to eq(2_500_000)
      expect(quota.quota_percentage).to eq(25.0)
    end
  end

  describe "#purge_cdn" do
    it "enqueues CDN cache invalidation" do
      stub_request(:post, "#{base_url}/v1/purge")
        .to_return(
          status: 202,
          headers: { "Content-Type" => "application/json" },
          body: JSON.generate({ message: "Purge accepted" })
        )

      res = client.purge_cdn(["https://cdn.smallpict.app/opt/photo.avif"])
      expect(res.message).to eq("Purge accepted")
    end
  end

  describe "#validate_key" do
    it "returns true on valid credentials and false on unauthorized" do
      stub_request(:get, "#{base_url}/v1/quota")
        .to_return(status: 200, body: JSON.generate({ plan: "free" }))

      expect(client.validate_key).to be true

      stub_request(:get, "#{base_url}/v1/quota")
        .to_return(status: 401, body: JSON.generate({ error: "Unauthorized" }))

      expect(client.validate_key).to be false
    end
  end
end
