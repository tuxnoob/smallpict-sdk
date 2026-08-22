<?php

declare(strict_types=1);

namespace SmallPict\Tests;

use PHPUnit\Framework\TestCase;
use SmallPict\Crypto;

class CryptoTest extends TestCase
{
    public function testEmptySha256Constant(): void
    {
        $this->assertSame('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', Crypto::EMPTY_SHA256);
    }

    public function testSha256HexEmpty(): void
    {
        $this->assertSame(Crypto::EMPTY_SHA256, Crypto::sha256Hex(''));
    }

    public function testSha256HexString(): void
    {
        $this->assertSame('b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9', Crypto::sha256Hex('hello world'));
    }

    public function testBuildStringToSign(): void
    {
        $res = Crypto::buildStringToSign('POST', '/v1/optimize', '1716301234', Crypto::EMPTY_SHA256);
        $this->assertSame("POST\n/v1/optimize\n1716301234\n" . Crypto::EMPTY_SHA256, $res);
    }

    public function testHmacSha256Hex(): void
    {
        $secretKey = 'sec_test_secret_key_123';
        $stringToSign = "POST\n/v1/optimize\n1716301234\n" . Crypto::EMPTY_SHA256;
        $sig = Crypto::hmacSha256Hex($secretKey, $stringToSign);

        $this->assertSame(64, strlen($sig));
        $this->assertTrue(ctype_xdigit($sig));
    }
}
