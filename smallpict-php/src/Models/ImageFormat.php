<?php

declare(strict_types=1);

namespace SmallPict\Models;

final class ImageFormat
{
    public const AUTO = 'auto';
    public const AVIF = 'avif';
    public const WEBP = 'webp';
    public const JPEG = 'jpeg';
    public const PNG = 'png';

    private function __construct()
    {
    }
}
