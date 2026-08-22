<?php

declare(strict_types=1);

namespace SmallPict\Laravel;

use SmallPict\Client;
use SmallPict\Config;

class SmallPictServiceProvider
{
    /**
     * Register SmallPict client in the Laravel service container.
     *
     * @param mixed $app
     */
    public function register($app = null): void
    {
        if (function_exists('app')) {
            app()->singleton(Client::class, static function ($app) {
                $config = function_exists('config') ? config('services.smallpict', []) : [];
                return new Client(
                    new Config(
                        $config['api_key'] ?? null,
                        $config['secret_key'] ?? null,
                        $config['base_url'] ?? null,
                        (float)($config['timeout'] ?? 30.0),
                        (int)($config['max_retries'] ?? 3),
                        (string)($config['fallback_mode'] ?? 'throw')
                    )
                );
            });

            app()->alias(Client::class, 'smallpict');
        }
    }

    public function boot(): void
    {
    }
}
