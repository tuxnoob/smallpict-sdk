<?php

declare(strict_types=1);

namespace SmallPict\Tests;

use PHPUnit\Framework\TestCase;
use SmallPict\Client;
use SmallPict\Config;
use SmallPict\Exceptions\ValidationException;
use SmallPict\Http\HttpClientInterface;
use SmallPict\Models\FallbackMode;
use SmallPict\Models\ImageFormat;
use SmallPict\Models\OptimizeOptions;

class ClientTest extends TestCase
{
    public function testMissingApiKeyThrowsValidationException(): void
    {
        $this->expectException(ValidationException::class);
        new Client('');
    }

    public function testOptimizeSuccess(): void
    {
        $mockHttp = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                TestCase::assertSame('POST', $method);
                TestCase::assertSame('https://api.smallpict.app/v1/optimize', $url);
                TestCase::assertSame('sp_live_test_1234567890', $headers['X-API-Key']);
                TestCase::assertArrayHasKey('X-Signature', $headers);
                TestCase::assertArrayHasKey('X-Timestamp', $headers);
                TestCase::assertArrayHasKey('Idempotency-Key', $headers);

                return [
                    'status' => 200,
                    'headers' => ['content-type' => 'application/json'],
                    'body' => (string)json_encode([
                        'job_id' => 'job_php_123',
                        'status' => 'completed',
                        'url' => 'https://cdn.smallpict.app/opt/photo.avif',
                        'format' => 'avif',
                        'original_size' => 100000,
                        'compressed_size' => 15000,
                        'bytes_saved' => 85000,
                        'savings_percentage' => 85.0,
                    ]),
                ];
            }
        };

        $client = new Client(
            new Config('sp_live_test_1234567890', 'sec_test_secret_123'),
            null,
            $mockHttp
        );

        $result = $client->optimize('fake image raw binary string', new OptimizeOptions(ImageFormat::AVIF, 80));

        $this->assertSame('job_php_123', $result->getJobId());
        $this->assertSame('completed', $result->getStatus());
        $this->assertSame('https://cdn.smallpict.app/opt/photo.avif', $result->getUrl());
        $this->assertSame(85.0, $result->getSavingsPercentage());
        $this->assertSame(85000, $result->getBytesSaved());
    }

    public function testGetQuota(): void
    {
        $mockHttp = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                TestCase::assertSame('GET', $method);
                TestCase::assertSame('https://api.smallpict.app/v1/quota', $url);

                return [
                    'status' => 200,
                    'headers' => ['content-type' => 'application/json'],
                    'body' => (string)json_encode([
                        'plan' => 'api_velocity',
                        'bytes_used' => 2500000,
                        'quota_limit' => 10000000,
                        'quota_percentage' => 25.0,
                        'active_keys_count' => 2,
                    ]),
                ];
            }
        };

        $client = new Client('sp_live_test', null, $mockHttp);
        $quota = $client->getQuota();

        $this->assertSame('api_velocity', $quota->getPlan());
        $this->assertSame(2500000, $quota->getBytesUsed());
        $this->assertSame(25.0, $quota->getQuotaPercentage());
        $this->assertSame(2, $quota->getActiveKeysCount());
    }

    public function testPurgeCdn(): void
    {
        $mockHttp = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                TestCase::assertSame('POST', $method);
                TestCase::assertSame('https://api.smallpict.app/v1/purge', $url);

                return [
                    'status' => 202,
                    'headers' => ['content-type' => 'application/json'],
                    'body' => (string)json_encode(['message' => 'Purge enqueued']),
                ];
            }
        };

        $client = new Client('sp_live_test', null, $mockHttp);
        $res = $client->purgeCdn(['https://cdn.smallpict.app/opt/photo.avif']);

        $this->assertSame('Purge enqueued', $res->getMessage());
    }

    public function testValidateKey(): void
    {
        $successMock = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                return [
                    'status' => 200,
                    'headers' => [],
                    'body' => (string)json_encode(['plan' => 'free', 'bytes_used' => 0, 'quota_limit' => 100, 'quota_percentage' => 0.0]),
                ];
            }
        };

        $validClient = new Client('sp_live_valid', null, $successMock);
        $this->assertTrue($validClient->validateKey());

        $failMock = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                return [
                    'status' => 401,
                    'headers' => [],
                    'body' => (string)json_encode(['error' => ['code' => 'UNAUTHORIZED', 'message' => 'Invalid key']]),
                ];
            }
        };

        $invalidClient = new Client('sp_live_invalid', null, $failMock);
        $this->assertFalse($invalidClient->validateKey());
    }

    public function testFallbackPassthroughOnQuotaExceeded(): void
    {
        $mockHttp = new class implements HttpClientInterface {
            public function send(string $method, string $url, array $headers = [], ?string $body = null, float $timeout = 30.0): array
            {
                return [
                    'status' => 402,
                    'headers' => [],
                    'body' => (string)json_encode(['error' => ['code' => 'QUOTA_EXCEEDED', 'message' => 'Quota full']]),
                ];
            }
        };

        $config = new Config('sp_live_test', null, null, 30.0, 3, FallbackMode::PASSTHROUGH);
        $client = new Client($config, null, $mockHttp);

        $result = $client->optimize('raw binary test data', new OptimizeOptions());

        $this->assertSame('fallback-passthrough', $result->getJobId());
        $this->assertSame(0.0, $result->getSavingsPercentage());
        $this->assertSame(0, $result->getBytesSaved());
    }
}
