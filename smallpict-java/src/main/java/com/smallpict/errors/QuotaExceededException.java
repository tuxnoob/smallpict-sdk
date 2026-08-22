package com.smallpict.errors;

import java.util.Map;

public class QuotaExceededException extends SmallPictException {
    public QuotaExceededException(String message) {
        this(message, null, null);
    }

    public QuotaExceededException(String message, String requestId, Map<String, Object> details) {
        super(message, "QUOTA_EXCEEDED", 402, requestId, details, null);
    }
}
