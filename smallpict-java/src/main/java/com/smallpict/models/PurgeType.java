package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonValue;

public enum PurgeType {
    URL("url"),
    ALL("all");

    private final String value;

    PurgeType(String value) {
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
