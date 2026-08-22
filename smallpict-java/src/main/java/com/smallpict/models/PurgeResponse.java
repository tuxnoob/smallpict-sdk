package com.smallpict.models;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class PurgeResponse {
    private final String message;

    @JsonCreator
    public PurgeResponse(@JsonProperty("message") String message) {
        this.message = message != null ? message : "Purge accepted";
    }

    public String getMessage() {
        return message;
    }
}
