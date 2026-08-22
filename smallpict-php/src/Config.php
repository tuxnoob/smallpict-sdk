<?php

declare(strict_types=1);

namespace SmallPict;

use SmallPict\Exceptions\ValidationException;
use SmallPict\Models\FallbackMode;

class Config
{
    private string $apiKey;
    private ?string $secretKey;
    private string $baseUrl;
    private float $timeout;
    private int $maxRetries;
    private string $fallbackMode;

    public function __construct(
        ?string $apiKey = null,
        ?string $secretKey = null,
        ?string $baseUrl = null,
        float $timeout = 30.0,
        int $maxRetries = 3,
        string $fallbackMode = FallbackMode::THROW
    ) {
        $resolvedApiKey = $apiKey ?? (string)getenv('SMALLPICT_API_KEY');
        if ($resolvedApiKey === '') {
            throw new ValidationException(
                'Missing required SmallPict API Key. Provide `apiKey` in Config or set SMALLPICT_API_KEY environment variable.'
            );
        }

        $this->apiKey = $resolvedApiKey;
        $this->secretKey = $secretKey ?? (getenv('SMALLPICT_SECRET_KEY') ?: null);
        $this->baseUrl = rtrim($baseUrl ?? (getenv('SMALLPICT_BASE_URL') ?: 'https://api.tuxnoob.com'), '/');
        $this->timeout = $timeout;
        $this->maxRetries = $maxRetries;
        $this->fallbackMode = $fallbackMode;
    }

    public function getApiKey(): string
    {
        return $this->apiKey;
    }

    public function getSecretKey(): ?string
    {
        return $this->secretKey;
    }

    public function getBaseUrl(): string
    {
        return $this->baseUrl;
    }

    public function getTimeout(): float
    {
        return $this->timeout;
    }

    public function getMaxRetries(): int
    {
        return $this->maxRetries;
    }

    public function getFallbackMode(): string
    {
        return $this->fallbackMode;
    }
}
