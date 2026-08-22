package com.smallpict.errors;

import java.util.Map;

public class ValidationException extends SmallPictException {
    public ValidationException(String message) {
        this(message, null, null);
    }

    public ValidationException(String message, String requestId, Map<String, Object> details) {
        super(message, "VALIDATION_FAILED", 400, requestId, details, null);
    }
}
