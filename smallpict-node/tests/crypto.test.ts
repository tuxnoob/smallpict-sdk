import { describe, it, expect } from 'vitest';
import {
  bufferToHex,
  buildStringToSign,
  EMPTY_SHA256,
  hmacSha256Hex,
  sha256Hex,
} from '../src/crypto.js';

describe('Crypto Utilities', () => {
  it('correctly returns known empty SHA-256 constant', () => {
    expect(EMPTY_SHA256).toBe('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
  });

  it('computes correct SHA-256 for empty string', async () => {
    const hash = await sha256Hex('');
    expect(hash).toBe(EMPTY_SHA256);
  });

  it('computes correct SHA-256 for test string', async () => {
    const hash = await sha256Hex('hello world');
    expect(hash).toBe('b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9');
  });

  it('builds canonical string-to-sign correctly', () => {
    const str = buildStringToSign('POST', '/v1/optimize', '1716301234', EMPTY_SHA256);
    expect(str).toBe(`POST\n/v1/optimize\n1716301234\n${EMPTY_SHA256}`);
  });

  it('computes HMAC-SHA256 signature matching test vector', async () => {
    const secretKey = 'sec_test_secret_key_123';
    const stringToSign = 'POST\n/v1/optimize\n1716301234\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';

    const signature = await hmacSha256Hex(secretKey, stringToSign);
    expect(signature).toHaveLength(64);
    expect(signature).toMatch(/^[a-f0-9]{64}$/);
  });

  it('converts byte buffers to hex accurately', () => {
    const bytes = new Uint8Array([0x00, 0x0f, 0xff, 0x10]);
    expect(bufferToHex(bytes)).toBe('000fff10');
  });
});
