# frozen_string_literal: true

module SmallPict
  module ActiveStorage
    class Service
      attr_reader :client

      def initialize(api_key: nil, secret_key: nil, base_url: nil, **options)
        @client = SmallPict::Client.new(
          api_key:    api_key,
          secret_key: secret_key,
          base_url:   base_url,
          **options
        )
      end

      def optimize(key, io, options = {})
        opts = options.merge(filename: key)
        @client.optimize(io, opts)
      end

      def url_for(key, options = {})
        opts = options.merge(filename: key)
        result = @client.optimize("", opts)
        result.url
      end
    end
  end
end
