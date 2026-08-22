<?php

declare(strict_types=1);

namespace SmallPict\Tests;

use PHPUnit\Framework\TestCase;
use SmallPict\Exceptions\AuthenticationException;
use SmallPict\Exceptions\NotFoundException;
use SmallPict\Exceptions\PermissionDeniedException;
use SmallPict\Exceptions\QuotaExceededException;
use SmallPict\Exceptions\RateLimitException;
use SmallPict\Exceptions\ServerException;
use SmallPict\Exceptions\SmallPictException;
use SmallPict\Exceptions\ValidationException;

class ExceptionsTest extends TestCase
{
    public function testSanitizeMessageMasksApiKeyAndSecret(): void
    {
        $raw = 'Failed on key sp_live_1234567890abcdef1234567890abcdef with sec_secret123456';
        $sanitized = SmallPictException::sanitizeMessage($raw);

        $this->assertStringNotContainsString('sp_live_1234567890abcdef1234567890abcdef', $sanitized);
        $this->assertStringNotContainsString('sec_secret123456', $sanitized);
        $this->assertStringContainsString('sp_live_12...cdef', $sanitized);
        $this->assertStringContainsString('***REDACTED***', $sanitized);
    }

    public function testExceptionToStringRedaction(): void
    {
        $e = new SmallPictException('Key sp_test_11223344556677889900 is revoked', 'FORBIDDEN', 403, 'req_001');
        $this->assertStringNotContainsString('sp_test_11223344556677889900', (string)$e);
        $this->assertStringContainsString('sp_test_11...9900', (string)$e);
        $this->assertStringContainsString('Request ID: req_001', (string)$e);
    }

    public function testExceptionHierarchy(): void
    {
        $this->assertInstanceOf(SmallPictException::class, new ValidationException());
        $this->assertInstanceOf(SmallPictException::class, new AuthenticationException());
        $this->assertInstanceOf(SmallPictException::class, new QuotaExceededException());
        $this->assertInstanceOf(SmallPictException::class, new PermissionDeniedException());
        $this->assertInstanceOf(SmallPictException::class, new NotFoundException());
        $this->assertInstanceOf(SmallPictException::class, new RateLimitException('Rate limited', 5));
        $this->assertInstanceOf(SmallPictException::class, new ServerException());
    }
}
