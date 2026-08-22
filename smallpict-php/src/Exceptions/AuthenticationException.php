<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class AuthenticationException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Authentication failed',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'UNAUTHORIZED', 401, $requestId, $details, $previous);
    }
}
