<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class PermissionDeniedException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Permission denied for this endpoint scope',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'FORBIDDEN', 403, $requestId, $details, $previous);
    }
}
