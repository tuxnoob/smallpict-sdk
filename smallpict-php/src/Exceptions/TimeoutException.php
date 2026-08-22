<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class TimeoutException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Request timed out after maximum duration',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'TIMEOUT_ERROR', 408, $requestId, $details, $previous);
    }
}
