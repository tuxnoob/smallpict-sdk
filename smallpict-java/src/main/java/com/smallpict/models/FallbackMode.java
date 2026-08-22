package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonValue;

public enum FallbackMode {
    THROW("throw"),
    PASSTHROUGH("passthrough");

    private final String value;

    FallbackMode(String value) {
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
