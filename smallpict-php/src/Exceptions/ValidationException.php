<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class ValidationException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Validation failed',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'VALIDATION_FAILED', 400, $requestId, $details, $previous);
    }
}
