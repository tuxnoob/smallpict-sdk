/**
 * SHA-256 hash of an empty string (standard RFC 6234).
 */
export const EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';

/**
 * Convert an ArrayBuffer or Uint8Array to a lowercase hex string.
 */
export function bufferToHex(buffer: ArrayBuffer | Uint8Array): string {
  const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  let hex = '';
  for (let i = 0; i < bytes.length; i++) {
    const b = bytes[i]!;
    hex += b < 16 ? '0' + b.toString(16) : b.toString(16);
  }
  return hex;
}

/**
 * Universal SHA-256 hashing supporting Web Crypto API and Node.js runtime.
 */
export async function sha256Hex(input: string | Uint8Array): Promise<string> {
  const encoder = new TextEncoder();
  const data = typeof input === 'string' ? encoder.encode(input) : input;

  // 1. Try global Web Crypto API (Node 18+, Bun, Next.js, Cloudflare Workers, Browser)
  if (typeof globalThis !== 'undefined' && globalThis.crypto?.subtle) {
    const hashBuffer = await globalThis.crypto.subtle.digest('SHA-256', data as BufferSource);
    return bufferToHex(hashBuffer);
  }

  // 2. Fallback to Node.js built-in crypto module
  try {
    const nodeCrypto = await import('node:crypto');
    return nodeCrypto.createHash('sha256').update(data).digest('hex');
  } catch {
    throw new Error('No compatible cryptographic provider found for SHA-256 calculation');
  }
}

/**
 * Universal HMAC-SHA256 signature generator.
 */
export async function hmacSha256Hex(secretKey: string, stringToSign: string): Promise<string> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secretKey);
  const messageData = encoder.encode(stringToSign);

  // 1. Try Web Crypto API
  if (typeof globalThis !== 'undefined' && globalThis.crypto?.subtle) {
    const cryptoKey = await globalThis.crypto.subtle.importKey(
      'raw',
      keyData as BufferSource,
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    );
    const signatureBuffer = await globalThis.crypto.subtle.sign('HMAC', cryptoKey, messageData as BufferSource);
    return bufferToHex(signatureBuffer);
  }

  // 2. Fallback to Node.js crypto module
  try {
    const nodeCrypto = await import('node:crypto');
    return nodeCrypto.createHmac('sha256', secretKey).update(stringToSign, 'utf8').digest('hex');
  } catch {
    throw new Error('No compatible cryptographic provider found for HMAC-SHA256 calculation');
  }
}

/**
 * Constructs the canonical string to sign matching SmallPict OpenAPI 3.1 specification.
 */
export function buildStringToSign(
  method: string,
  path: string,
  timestamp: string,
  bodyHash: string
): string {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${method.toUpperCase()}\n${cleanPath}\n${timestamp}\n${bodyHash}`;
}
