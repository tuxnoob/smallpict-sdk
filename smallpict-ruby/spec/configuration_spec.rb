# frozen_string_literal: true

require "spec_helper"

RSpec.describe SmallPict do
  describe ".configure" do
    it "allows block configuration" do
      described_class.configure do |config|
        config.api_key = "sp_live_test_config"
        config.secret_key = "sec_test_secret"
        config.base_url = "https://custom.smallpict.com"
        config.timeout = 15
        config.max_retries = 5
        config.fallback_mode = :passthrough
      end

      config = described_class.configuration
      expect(config.api_key).to eq("sp_live_test_config")
      expect(config.secret_key).to eq("sec_test_secret")
      expect(config.base_url).to eq("https://custom.smallpict.com")
      expect(config.timeout).to eq(15)
      expect(config.max_retries).to eq(5)
      expect(config.fallback_mode).to eq(:passthrough)
    end
  end
end
