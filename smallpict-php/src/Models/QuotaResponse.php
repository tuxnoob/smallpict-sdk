<?php

declare(strict_types=1);

namespace SmallPict\Models;

class QuotaResponse
{
    private string $plan;
    private int $bytesUsed;
    private int $quotaLimit;
    private float $quotaPercentage;
    private ?int $cdnEgressUsedBytes;
    private ?int $cdnEgressQuotaBytes;
    private ?int $activeKeysCount;
    private ?int $activeSitesCount;

    public function __construct(
        string $plan,
        int $bytesUsed,
        int $quotaLimit,
        float $quotaPercentage,
        ?int $cdnEgressUsedBytes = null,
        ?int $cdnEgressQuotaBytes = null,
        ?int $activeKeysCount = null,
        ?int $activeSitesCount = null
    ) {
        $this->plan = $plan;
        $this->bytesUsed = $bytesUsed;
        $this->quotaLimit = $quotaLimit;
        $this->quotaPercentage = $quotaPercentage;
        $this->cdnEgressUsedBytes = $cdnEgressUsedBytes;
        $this->cdnEgressQuotaBytes = $cdnEgressQuotaBytes;
        $this->activeKeysCount = $activeKeysCount;
        $this->activeSitesCount = $activeSitesCount;
    }

    public function getPlan(): string
    {
        return $this->plan;
    }

    public function getBytesUsed(): int
    {
        return $this->bytesUsed;
    }

    public function getQuotaLimit(): int
    {
        return $this->quotaLimit;
    }

    public function getQuotaPercentage(): float
    {
        return $this->quotaPercentage;
    }

    public function getCdnEgressUsedBytes(): ?int
    {
        return $this->cdnEgressUsedBytes;
    }

    public function getCdnEgressQuotaBytes(): ?int
    {
        return $this->cdnEgressQuotaBytes;
    }

    public function getActiveKeysCount(): ?int
    {
        return $this->activeKeysCount;
    }

    public function getActiveSitesCount(): ?int
    {
        return $this->activeSitesCount;
    }
}
