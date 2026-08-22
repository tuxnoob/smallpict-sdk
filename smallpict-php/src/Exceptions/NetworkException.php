<?php

declare(strict_types=1);

namespace SmallPict\Exceptions;

class NetworkException extends SmallPictException
{
    /**
     * @param string $message
     * @param array<string, mixed> $details
     * @param \Throwable|null $previous
     */
    public function __construct(
        string $message = 'Network communication failed',
        array $details = [],
        ?\Throwable $previous = null
    ) {
        parent::__construct("Network communication failed: {$message}", 'NETWORK_ERROR', 0, null, $details, $previous);
    }
}
