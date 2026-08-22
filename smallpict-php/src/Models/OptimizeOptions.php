<?php

declare(strict_types=1);

namespace SmallPict\Models;

class OptimizeOptions
{
    private string $format;
    private int $quality;
    private ?int $maxWidth;
    private ?int $maxHeight;
    private string $fit;
    private bool $lossless;
    private bool $stripMetadata;
    private ?string $filename;
    private ?string $mimeType;
    private ?string $idempotencyKey;

    public function __construct(
        string $format = ImageFormat::AUTO,
        int $quality = 80,
        ?int $maxWidth = null,
        ?int $maxHeight = null,
        string $fit = FitMode::COVER,
        bool $lossless = false,
        bool $stripMetadata = true,
        ?string $filename = null,
        ?string $mimeType = null,
        ?string $idempotencyKey = null
    ) {
        $this->format = $format;
        $this->quality = max(1, min(100, $quality));
        $this->maxWidth = $maxWidth;
        $this->maxHeight = $maxHeight;
        $this->fit = $fit;
        $this->lossless = $lossless;
        $this->stripMetadata = $stripMetadata;
        $this->filename = $filename;
        $this->mimeType = $mimeType;
        $this->idempotencyKey = $idempotencyKey;
    }

    public function getFormat(): string
    {
        return $this->format;
    }

    public function getQuality(): int
    {
        return $this->quality;
    }

    public function getMaxWidth(): ?int
    {
        return $this->maxWidth;
    }

    public function getMaxHeight(): ?int
    {
        return $this->maxHeight;
    }

    public function getFit(): string
    {
        return $this->fit;
    }

    public function isLossless(): bool
    {
        return $this->lossless;
    }

    public function shouldStripMetadata(): bool
    {
        return $this->stripMetadata;
    }

    public function getFilename(): ?string
    {
        return $this->filename;
    }

    public function getMimeType(): ?string
    {
        return $this->mimeType;
    }

    public function getIdempotencyKey(): ?string
    {
        return $this->idempotencyKey;
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return [
            'format' => $this->format,
            'quality' => $this->quality,
            'max_width' => $this->maxWidth,
            'max_height' => $this->maxHeight,
            'fit' => $this->fit,
            'lossless' => $this->lossless,
            'strip_metadata' => $this->stripMetadata,
        ];
    }
}
