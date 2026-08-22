<?php

declare(strict_types=1);

namespace SmallPict\Http;

use SmallPict\Exceptions\NetworkException;
use SmallPict\Exceptions\TimeoutException;

class CurlHttpClient implements HttpClientInterface
{
    public function send(
        string $method,
        string $url,
        array $headers = [],
        ?string $body = null,
        float $timeout = 30.0
    ): array {
        $ch = curl_init($url);
        if ($ch === false) {
            throw new NetworkException('Failed to initialize cURL handle');
        }

        $formattedHeaders = [];
        foreach ($headers as $k => $v) {
            $formattedHeaders[] = "{$k}: {$v}";
        }

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $formattedHeaders);
        curl_setopt($ch, CURLOPT_TIMEOUT, (int)ceil($timeout));
        curl_setopt($ch, CURLOPT_HEADER, true);

        if ($body !== null && $body !== '') {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }

        $rawResponse = curl_exec($ch);
        $statusCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $headerSize = (int)curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $errno = curl_errno($ch);
        $error = curl_error($ch);

        curl_close($ch);

        if ($errno !== 0) {
            if ($errno === CURLE_OPERATION_TIMEDOUT) {
                throw new TimeoutException("Request to {$url} timed out after {$timeout}s");
            }
            throw new NetworkException("cURL error ({$errno}): {$error}");
        }

        $rawHeaders = substr((string)$rawResponse, 0, $headerSize);
        $responseBody = substr((string)$rawResponse, $headerSize);

        $parsedHeaders = [];
        foreach (explode("\r\n", $rawHeaders) as $line) {
            $parts = explode(':', $line, 2);
            if (count($parts) === 2) {
                $parsedHeaders[strtolower(trim($parts[0]))] = trim($parts[1]);
            }
        }

        return [
            'status' => $statusCode,
            'headers' => $parsedHeaders,
            'body' => (string)$responseBody,
        ];
    }
}
