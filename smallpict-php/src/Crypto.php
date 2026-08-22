<?php

declare(strict_types=1);

namespace SmallPict;

final class Crypto
{
    public const EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';

    public static function sha256Hex(string $data): string
    {
        if ($data === '') {
            return self::EMPTY_SHA256;
        }
        return hash('sha256', $data);
    }

    public static function hmacSha256Hex(string $secretKey, string $stringToSign): string
    {
        return hash_hmac('sha256', $stringToSign, $secretKey);
    }

    public static function buildStringToSign(
        string $method,
        string $path,
        string $timestamp,
        string $bodyHash
    ): string {
        $cleanPath = strpos($path, '/') === 0 ? $path : '/' . $path;
        return strtoupper($method) . "\n" . $cleanPath . "\n" . $timestamp . "\n" . $bodyHash;
    }

    private function __construct()
    {
    }
}
