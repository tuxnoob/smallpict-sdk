package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

public class JobStatusResult {
    @JsonProperty("job_id")
    private final String jobId;
    private final String status;
    private final String url;
    private final String format;
    @JsonProperty("bytes_saved")
    private final Long bytesSaved;
    private final Map<String, Object> error;
    @JsonProperty("created_at")
    private final String createdAt;
    @JsonProperty("updated_at")
    private final String updatedAt;

    @JsonCreator
    public JobStatusResult(
            @JsonProperty("job_id") String jobId,
            @JsonProperty("status") String status,
            @JsonProperty("url") String url,
            @JsonProperty("format") String format,
            @JsonProperty("bytes_saved") Long bytesSaved,
            @JsonProperty("error") Map<String, Object> error,
            @JsonProperty("created_at") String createdAt,
            @JsonProperty("updated_at") String updatedAt) {
        this.jobId = jobId;
        this.status = status != null ? status : "processing";
        this.url = url;
        this.format = format;
        this.bytesSaved = bytesSaved;
        this.error = error;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public String getJobId() {
        return jobId;
    }

    public String getStatus() {
        return status;
    }

    public String getUrl() {
        return url;
    }

    public String getFormat() {
        return format;
    }

    public Long getBytesSaved() {
        return bytesSaved;
    }

    public Map<String, Object> getError() {
        return error;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public String getUpdatedAt() {
        return updatedAt;
    }
}
