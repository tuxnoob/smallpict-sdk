# frozen_string_literal: true

module SmallPict
  module Models
    class JobStatusResult
      attr_reader :job_id, :status, :url, :format, :bytes_saved,
                  :error, :created_at, :updated_at

      def initialize(attributes = {})
        @job_id      = attributes[:job_id] || attributes["job_id"]
        @status      = attributes[:status] || attributes["status"] || "processing"
        @url         = attributes[:url] || attributes["url"]
        @format      = attributes[:format] || attributes["format"]
        @bytes_saved = attributes[:bytes_saved] || attributes["bytes_saved"]
        @error       = attributes[:error] || attributes["error"]
        @created_at  = attributes[:created_at] || attributes["created_at"]
        @updated_at  = attributes[:updated_at] || attributes["updated_at"]
      end
    end
  end
end
