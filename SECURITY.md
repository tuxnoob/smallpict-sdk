# Security Policy & Secret Management

The SmallPict team takes security and data integrity very seriously across all SDK implementations and cloud services.

---

## 🛡️ Reporting a Vulnerability

If you discover a security vulnerability in any SmallPict SDK or backend API, please **DO NOT open a public GitHub issue**.

Please report the vulnerability privately:
- **Email:** [security@smallpict.app](mailto:security@smallpict.app)
- **Response SLA:** Initial acknowledgment within **24 hours**, with triage and patch timeline within **72 hours**.

---

## 🔒 Secret Handling & Least Privilege

1. **Client-Side Secret Masking:**
   SDKs must redact API keys and HMAC signatures from all runtime error messages, HTTP loggers, and stack traces.
   
   Example safe error structure:
   ```json
   {
     "error": {
       "code": "UNAUTHORIZED",
       "message": "Invalid API Key signature. Key prefix: sp_live_a8f9...",
       "request_id": "req_01HPX7YZ8N9Q"
     }
   }
   ```

2. **Supply Chain & Registry Security:**
   - **Keyless OIDC Publishing:** PyPI and npm releases are authenticated via GitHub Actions OpenID Connect (OIDC) with Sigstore Provenance (`--provenance`). No static registry passwords or API tokens are stored in repository secrets.
   - **Automated Dependency Auditing:** All SDK repositories run Dependabot, CodeQL, and Semgrep security scanning on every push.

3. **Privacy & EXIF Data Sanitization:**
   - By default, all image optimization calls apply `strip_metadata: true` to strip private EXIF tags (GPS geolocation, camera hardware serials) before transmission, ensuring compliance with global privacy regulations (GDPR, UU PDP).
