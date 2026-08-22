package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonValue;

public enum FitMode {
    COVER("cover"),
    CONTAIN("contain"),
    INSIDE("inside"),
    OUTSIDE("outside");

    private final String value;

    FitMode(String value) {
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
