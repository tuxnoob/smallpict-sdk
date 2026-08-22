package com.smallpict.errors;

public class TimeoutException extends SmallPictException {
    public TimeoutException(String message) {
        super(message, "TIMEOUT_ERROR", 408, null, null, null);
    }

    public TimeoutException(String message, Throwable cause) {
        super(message, "TIMEOUT_ERROR", 408, null, null, cause);
    }
}
