package com.smallpict.errors;

public class NetworkException extends SmallPictException {
    public NetworkException(String message) {
        super(message, "NETWORK_ERROR", null, null, null, null);
    }

    public NetworkException(String message, Throwable cause) {
        super(message, "NETWORK_ERROR", null, null, null, cause);
    }
}
