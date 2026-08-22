<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class NotFoundException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Resource or job ID not found',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'NOT_FOUND', 404, $requestId, $details, $previous);
    }
}
