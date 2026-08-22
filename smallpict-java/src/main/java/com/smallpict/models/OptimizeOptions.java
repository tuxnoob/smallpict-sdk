package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class OptimizeOptions {
    private final ImageFormat format;
    private final Integer quality;
    @JsonProperty("max_width")
    private final Integer maxWidth;
    @JsonProperty("max_height")
    private final Integer maxHeight;
    private final FitMode fit;
    private final Boolean lossless;
    @JsonProperty("strip_metadata")
    private final boolean stripMetadata;
    private final String filename;
    @JsonProperty("mime_type")
    private final String mimeType;
    @JsonIgnore
    private final String idempotencyKey;

    private OptimizeOptions(Builder builder) {
        this.format = builder.format;
        this.quality = builder.quality;
        this.maxWidth = builder.maxWidth;
        this.maxHeight = builder.maxHeight;
        this.fit = builder.fit;
        this.lossless = builder.lossless;
        this.stripMetadata = builder.stripMetadata;
        this.filename = builder.filename;
        this.mimeType = builder.mimeType;
        this.idempotencyKey = builder.idempotencyKey;
    }

    public static Builder builder() {
        return new Builder();
    }

    public ImageFormat getFormat() {
        return format;
    }

    public Integer getQuality() {
        return quality;
    }

    public Integer getMaxWidth() {
        return maxWidth;
    }

    public Integer getMaxHeight() {
        return maxHeight;
    }

    public FitMode getFit() {
        return fit;
    }

    public Boolean getLossless() {
        return lossless;
    }

    public boolean isStripMetadata() {
        return stripMetadata;
    }

    public String getFilename() {
        return filename;
    }

    public String getMimeType() {
        return mimeType;
    }

    public String getIdempotencyKey() {
        return idempotencyKey;
    }

    public static class Builder {
        private ImageFormat format = ImageFormat.AUTO;
        private Integer quality = 80;
        private Integer maxWidth;
        private Integer maxHeight;
        private FitMode fit = FitMode.COVER;
        private Boolean lossless = false;
        private boolean stripMetadata = true;
        private String filename;
        private String mimeType;
        private String idempotencyKey;

        public Builder format(ImageFormat format) {
            this.format = format;
            return this;
        }

        public Builder quality(int quality) {
            this.quality = Math.max(1, Math.min(100, quality));
            return this;
        }

        public Builder maxWidth(int maxWidth) {
            this.maxWidth = maxWidth;
            return this;
        }

        public Builder maxHeight(int maxHeight) {
            this.maxHeight = maxHeight;
            return this;
        }

        public Builder fit(FitMode fit) {
            this.fit = fit;
            return this;
        }

        public Builder lossless(boolean lossless) {
            this.lossless = lossless;
            return this;
        }

        public Builder stripMetadata(boolean stripMetadata) {
            this.stripMetadata = stripMetadata;
            return this;
        }

        public Builder filename(String filename) {
            this.filename = filename;
            return this;
        }

        public Builder mimeType(String mimeType) {
            this.mimeType = mimeType;
            return this;
        }

        public Builder idempotencyKey(String idempotencyKey) {
            this.idempotencyKey = idempotencyKey;
            return this;
        }

        public OptimizeOptions build() {
            return new OptimizeOptions(this);
        }
    }
}
