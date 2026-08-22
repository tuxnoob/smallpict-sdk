<?php

declare(strict_types=1);

namespace SmallPict\Models;

final class FallbackMode
{
    public const THROW = 'throw';
    public const PASSTHROUGH = 'passthrough';

    private function __construct()
    {
    }
}
