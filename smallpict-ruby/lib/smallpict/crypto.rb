# frozen_string_literal: true

require "openssl"

module SmallPict
  module Crypto
    EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    module_function

    def sha256_hex(data)
      return EMPTY_SHA256 if data.nil? || data.empty?

      OpenSSL::Digest::SHA256.hexdigest(data)
    end

    def hmac_sha256_hex(secret_key, string_to_sign)
      OpenSSL::HMAC.hexdigest("SHA256", secret_key.to_s, string_to_sign.to_s)
    end

    def build_string_to_sign(method, path, timestamp, body_hash)
      clean_path = path.start_with?("/") ? path : "/#{path}"
      "#{method.to_s.upcase}\n#{clean_path}\n#{timestamp}\n#{body_hash}"
    end
  end
end
