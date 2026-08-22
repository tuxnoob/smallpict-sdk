package com.smallpict.errors;

import java.util.Map;

public class PermissionDeniedException extends SmallPictException {
    public PermissionDeniedException(String message) {
        this(message, null, null);
    }

    public PermissionDeniedException(String message, String requestId, Map<String, Object> details) {
        super(message, "FORBIDDEN", 403, requestId, details, null);
    }
}
