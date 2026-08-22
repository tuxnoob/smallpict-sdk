# frozen_string_literal: true

module SmallPict
  class Configuration
    attr_accessor :api_key, :secret_key, :base_url, :timeout, :max_retries, :fallback_mode

    def initialize
      @api_key       = ENV["SMALLPICT_API_KEY"]
      @secret_key    = ENV["SMALLPICT_SECRET_KEY"]
      @base_url      = (ENV["SMALLPICT_BASE_URL"] || "https://api.tuxnoob.com").chomp("/")
      @timeout       = 30
      @max_retries   = 3
      @fallback_mode = :throw
    end
  end
end
