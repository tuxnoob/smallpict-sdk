import { describe, it, expect } from 'vitest';
import {
  AuthenticationError,
  createErrorFromResponse,
  NotFoundError,
  PermissionDeniedError,
  QuotaExceededError,
  RateLimitError,
  sanitizeMessage,
  ServerError,
  SmallPictError,
  ValidationError,
} from '../src/errors.js';

describe('Error Hierarchy and Redaction', () => {
  it('masks raw API keys in error strings', () => {
    const raw = 'Failed to authenticate with key sp_live_1234567890abcdef1234567890abcdef and secret sec_9988776655';
    const sanitized = sanitizeMessage(raw);

    expect(sanitized).not.toContain('sp_live_1234567890abcdef1234567890abcdef');
    expect(sanitized).not.toContain('sec_9988776655');
    expect(sanitized).toContain('sp_live_12...cdef');
    expect(sanitized).toContain('***REDACTED***');
  });

  it('redacts credentials inside SmallPictError messages', () => {
    const err = new SmallPictError(
      'Invalid key sp_test_aabbccddeeff11223344556677889900',
      'UNAUTHORIZED',
      401
    );
    expect(err.message).not.toContain('sp_test_aabbccddeeff11223344556677889900');
    expect(err.toString()).toContain('sp_test_aa...9900');
  });

  it('correctly maps 400 to ValidationError', () => {
    const err = createErrorFromResponse(400, {
      error: { code: 'VALIDATION_FAILED', message: 'Missing filesize' },
    });
    expect(err).toBeInstanceOf(ValidationError);
    expect(err.code).toBe('VALIDATION_FAILED');
    expect(err.status).toBe(400);
  });

  it('correctly maps 401 to AuthenticationError', () => {
    const err = createErrorFromResponse(401, {
      error: { code: 'UNAUTHORIZED', message: 'Invalid API Key' },
    });
    expect(err).toBeInstanceOf(AuthenticationError);
    expect(err.status).toBe(401);
  });

  it('correctly maps 402 to QuotaExceededError', () => {
    const err = createErrorFromResponse(402, {
      error: { code: 'QUOTA_EXCEEDED', message: 'Storage limit reached' },
    });
    expect(err).toBeInstanceOf(QuotaExceededError);
    expect(err.status).toBe(402);
  });

  it('correctly maps 403 to PermissionDeniedError', () => {
    const err = createErrorFromResponse(403, {
      error: { code: 'FORBIDDEN', message: 'API Key revoked' },
    });
    expect(err).toBeInstanceOf(PermissionDeniedError);
    expect(err.status).toBe(403);
  });

  it('correctly maps 404 to NotFoundError', () => {
    const err = createErrorFromResponse(404, {
      error: { code: 'NOT_FOUND', message: 'Job not found' },
    });
    expect(err).toBeInstanceOf(NotFoundError);
    expect(err.status).toBe(404);
  });

  it('correctly maps 429 to RateLimitError with retry-after', () => {
    const err = createErrorFromResponse(
      429,
      { error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many requests' } },
      'req_123',
      '5'
    );
    expect(err).toBeInstanceOf(RateLimitError);
    expect((err as RateLimitError).retryAfterSeconds).toBe(5);
    expect(err.requestId).toBe('req_123');
  });

  it('correctly maps 500 to ServerError', () => {
    const err = createErrorFromResponse(500, {
      error: { message: 'Internal transcoding panic' },
    });
    expect(err).toBeInstanceOf(ServerError);
    expect(err.status).toBe(500);
  });
});
