package com.smallpict;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.smallpict.models.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ModelsTest {
    private final ObjectMapper mapper = new ObjectMapper();

    @Test
    void testOptimizeOptionsBuilder() throws Exception {
        OptimizeOptions options = OptimizeOptions.builder()
                .format(ImageFormat.AVIF)
                .quality(85)
                .maxWidth(1920)
                .maxHeight(1080)
                .fit(FitMode.CONTAIN)
                .lossless(false)
                .stripMetadata(true)
                .filename("banner.png")
                .mimeType("image/png")
                .idempotencyKey("idemp_123")
                .build();

        assertEquals(ImageFormat.AVIF, options.getFormat());
        assertEquals(85, options.getQuality());
        assertEquals(1920, options.getMaxWidth());
        assertEquals(FitMode.CONTAIN, options.getFit());
        assertEquals("banner.png", options.getFilename());
        assertEquals("idemp_123", options.getIdempotencyKey());

        String json = mapper.writeValueAsString(options);
        assertTrue(json.contains("\"format\":\"avif\""));
        assertTrue(json.contains("\"quality\":85"));
        assertFalse(json.contains("idempotencyKey")); // ignored in json body
    }

    @Test
    void testOptimizeResultDeserialization() throws Exception {
        String json = """
        {
            "job_id": "job_123",
            "status": "completed",
            "url": "https://cdn.smallpict.app/opt/hero.avif",
            "format": "avif",
            "original_size": 100000,
            "compressed_size": 15000,
            "bytes_saved": 85000,
            "savings_percentage": 85.0
        }
        """;

        OptimizeResult result = mapper.readValue(json, OptimizeResult.class);
        assertEquals("job_123", result.getJobId());
        assertEquals("completed", result.getStatus());
        assertEquals("https://cdn.smallpict.app/opt/hero.avif", result.getUrl());
        assertEquals(85.0, result.getSavingsPercentage());
        assertEquals(85000, result.getBytesSaved());
    }

    @Test
    void testQuotaResponseDeserialization() throws Exception {
        String json = """
        {
            "plan": "api_velocity",
            "bytes_used": 5000000,
            "quota_limit": 10000000,
            "quota_percentage": 50.0,
            "active_keys_count": 3
        }
        """;

        QuotaResponse quota = mapper.readValue(json, QuotaResponse.class);
        assertEquals("api_velocity", quota.getPlan());
        assertEquals(5000000L, quota.getBytesUsed());
        assertEquals(10000000L, quota.getQuotaLimit());
        assertEquals(50.0, quota.getQuotaPercentage());
        assertEquals(3, quota.getActiveKeysCount());
    }
}
