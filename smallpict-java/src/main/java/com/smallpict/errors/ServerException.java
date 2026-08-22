package com.smallpict.errors;

import java.util.Map;

public class ServerException extends SmallPictException {
    public ServerException(String message, int statusCode, String requestId, Map<String, Object> details) {
        super(message, "INTERNAL_ERROR", statusCode, requestId, details, null);
    }
}
