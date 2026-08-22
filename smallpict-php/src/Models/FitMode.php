<?php

declare(strict_types=1);

namespace SmallPict\Models;

final class FitMode
{
    public const COVER = 'cover';
    public const CONTAIN = 'contain';
    public const INSIDE = 'inside';
    public const OUTSIDE = 'outside';

    private function __construct()
    {
    }
}
