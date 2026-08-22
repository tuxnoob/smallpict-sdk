package com.smallpict.errors;

import java.util.Map;

public class AuthenticationException extends SmallPictException {
    public AuthenticationException(String message) {
        this(message, null, null);
    }

    public AuthenticationException(String message, String requestId, Map<String, Object> details) {
        super(message, "UNAUTHORIZED", 401, requestId, details, null);
    }
}
