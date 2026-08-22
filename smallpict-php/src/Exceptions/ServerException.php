<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class ServerException extends SmallPictException
{
    /**
     * @param string $message
     * @param int $statusCode
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Internal server error occurred',
        int $statusCode = 500,
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'INTERNAL_ERROR', $statusCode, $requestId, $details, $previous);
    }
}
