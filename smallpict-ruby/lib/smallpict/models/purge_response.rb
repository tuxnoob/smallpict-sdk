# frozen_string_literal: true

module SmallPict
  module Models
    class PurgeResponse
      attr_reader :message

      def initialize(attributes = {})
        @message = attributes[:message] || attributes["message"] || "Purge accepted"
      end
    end
  end
end
