<?php

declare(strict_types=1);

namespace SmallPict\Http;

interface HttpClientInterface
{
    /**
     * Send an HTTP request and return the response array.
     *
     * @param string $method HTTP Method (GET, POST, DELETE, etc.)
     * @param string $url Target full URL
     * @param array<string, string> $headers Request headers
     * @param string|null $body Serialized body payload
     * @param float $timeout Timeout in seconds
     * @return array{status: int, headers: array<string, string>, body: string}
     * @throws \SmallPict\Exceptions\SmallPictException
     */
    public function send(
        string $method,
        string $url,
        array $headers = [],
        ?string $body = null,
        float $timeout = 30.0
    ): array;
}
