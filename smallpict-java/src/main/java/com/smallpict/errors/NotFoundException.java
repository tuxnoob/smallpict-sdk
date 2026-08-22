package com.smallpict.errors;

import java.util.Map;

public class NotFoundException extends SmallPictException {
    public NotFoundException(String message) {
        this(message, null, null);
    }

    public NotFoundException(String message, String requestId, Map<String, Object> details) {
        super(message, "NOT_FOUND", 404, requestId, details, null);
    }
}
