package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonValue;

public enum ImageFormat {
    AUTO("auto"),
    AVIF("avif"),
    WEBP("webp"),
    JPEG("jpeg"),
    PNG("png");

    private final String value;

    ImageFormat(String value) {
        this.value = value;
    }

    @JsonValue
    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return value;
    }
}
