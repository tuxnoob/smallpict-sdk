package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class QuotaResponse {
    private final String plan;
    @JsonProperty("bytes_used")
    private final long bytesUsed;
    @JsonProperty("quota_limit")
    private final long quotaLimit;
    @JsonProperty("quota_percentage")
    private final double quotaPercentage;
    @JsonProperty("cdn_egress_used_bytes")
    private final Long cdnEgressUsedBytes;
    @JsonProperty("cdn_egress_quota_bytes")
    private final Long cdnEgressQuotaBytes;
    @JsonProperty("active_keys_count")
    private final Integer activeKeysCount;
    @JsonProperty("active_sites_count")
    private final Integer activeSitesCount;

    @JsonCreator
    public QuotaResponse(
            @JsonProperty("plan") String plan,
            @JsonProperty("bytes_used") Long bytesUsed,
            @JsonProperty("quota_limit") Long quotaLimit,
            @JsonProperty("quota_percentage") Double quotaPercentage,
            @JsonProperty("cdn_egress_used_bytes") Long cdnEgressUsedBytes,
            @JsonProperty("cdn_egress_quota_bytes") Long cdnEgressQuotaBytes,
            @JsonProperty("active_keys_count") Integer activeKeysCount,
            @JsonProperty("active_sites_count") Integer activeSitesCount) {
        this.plan = plan != null ? plan : "free";
        this.bytesUsed = bytesUsed != null ? bytesUsed : 0L;
        this.quotaLimit = quotaLimit != null ? quotaLimit : 0L;
        if (quotaPercentage != null) {
            this.quotaPercentage = Math.round(quotaPercentage * 100.0) / 100.0;
        } else if (this.quotaLimit > 0) {
            this.quotaPercentage = Math.round(((double) this.bytesUsed / this.quotaLimit * 100.0) * 100.0) / 100.0;
        } else {
            this.quotaPercentage = 0.0;
        }
        this.cdnEgressUsedBytes = cdnEgressUsedBytes;
        this.cdnEgressQuotaBytes = cdnEgressQuotaBytes;
        this.activeKeysCount = activeKeysCount;
        this.activeSitesCount = activeSitesCount;
    }

    public String getPlan() {
        return plan;
    }

    public long getBytesUsed() {
        return bytesUsed;
    }

    public long getQuotaLimit() {
        return quotaLimit;
    }

    public double getQuotaPercentage() {
        return quotaPercentage;
    }

    public Long getCdnEgressUsedBytes() {
        return cdnEgressUsedBytes;
    }

    public Long getCdnEgressQuotaBytes() {
        return cdnEgressQuotaBytes;
    }

    public Integer getActiveKeysCount() {
        return activeKeysCount;
    }

    public Integer getActiveSitesCount() {
        return activeSitesCount;
    }
}
