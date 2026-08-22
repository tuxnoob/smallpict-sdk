<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class QuotaExceededException extends SmallPictException
{
    /**
     * @param string $message
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Storage or processing quota exceeded',
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'QUOTA_EXCEEDED', 402, $requestId, $details, $previous);
    }
}
