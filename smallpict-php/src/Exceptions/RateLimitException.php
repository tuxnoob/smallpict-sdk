<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class RateLimitException extends SmallPictException
{
    private ?int $retryAfterSeconds;

    /**
     * @param string $message
     * @param int|null $retryAfterSeconds
     * @param string|null $requestId
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Rate limit exceeded',
        ?int $retryAfterSeconds = null,
        ?string $requestId = null,
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, 'RATE_LIMIT_EXCEEDED', 429, $requestId, $details, $previous);
        $this->retryAfterSeconds = $retryAfterSeconds;
    }

    public function getRetryAfterSeconds(): ?int
    {
        return $this->retryAfterSeconds;
    }
}
