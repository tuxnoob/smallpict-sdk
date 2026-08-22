<?php

declare(strict_types=1);

namespace SmallPict\Laravel\Facades;

use SmallPict\Client;

/**
 * @method static \SmallPict\Models\OptimizeResult optimize(string|resource $source, ?\SmallPict\Models\OptimizeOptions $options = null)
 * @method static \SmallPict\Models\QuotaResponse getQuota()
 * @method static \SmallPict\Models\PurgeResponse purgeCdn(array|string $urls = [], string $purgeType = 'url')
 * @method static bool validateKey()
 * @method static \SmallPict\Models\JobStatusResult getJobStatus(string $jobId)
 *
 * @see \SmallPict\Client
 */
class SmallPict
{
    /**
     * @param string $method
     * @param array<mixed> $args
     * @return mixed
     */
    public static function __callStatic(string $method, array $args)
    {
        if (function_exists('app')) {
            $instance = app(Client::class);
            return $instance->$method(...$args);
        }
        throw new \RuntimeException('Laravel container is not available');
    }
}
