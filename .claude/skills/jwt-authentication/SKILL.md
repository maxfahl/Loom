# SKILL.md - JWT Authentication

## Metadata Section

- Name: jwt-authentication
- Version: 1.0.0
- Category: Security / Authentication
- Tags: JWT, Authentication, Authorization, Security, Token, Web Security, TypeScript
- Description: Guides Claude on implementing secure JSON Web Token (JWT) authentication in modern applications, focusing on TypeScript best practices.

## Skill Purpose

This skill enables Claude to design, implement, and review robust JWT-based authentication systems. It covers token generation, secure storage, validation, and common pitfalls, ensuring applications are secure, scalable, and maintainable.

## When to Activate This Skill

Activate this skill when the task involves:
- Designing a new authentication system for a web or mobile application.
- Implementing user login, registration, or session management.
- Securing API endpoints with token-based authorization.
- Refactoring an existing authentication mechanism to use JWTs.
- Reviewing code related to JWT handling, token validation, or user sessions.
- Addressing security vulnerabilities related to authentication.
- Setting up refresh token mechanisms or token revocation.
- Discussing stateless authentication or microservices security.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for JWT authentication:

1.  **JWT Structure:**
    *   **Header:** `alg` (algorithm, e.g., HS256, RS256), `typ` (type, always JWT).
    *   **Payload (Claims):**
        *   **Registered Claims:** `iss` (issuer), `sub` (subject), `aud` (audience), `exp` (expiration time), `nbf` (not before), `iat` (issued at), `jti` (JWT ID).
        *   **Public Claims:** Custom claims defined by users, but publicly registered.
        *   **Private Claims:** Custom claims agreed upon by parties, not publicly registered.
    *   **Signature:** Used to verify the sender of the JWT and ensure the message hasn't been changed.

2.  **Token Types:**
    *   **Access Token:** Short-lived, used for authenticating API requests.
    *   **Refresh Token:** Long-lived, used to obtain new access tokens without re-authentication. Stored securely (e.g., HTTP-only cookie).

3.  **Algorithms:**
    *   **Symmetric (HMAC):** e.g., HS256. Uses a single secret key for signing and verification.
    *   **Asymmetric (RSA/ECDSA):** e.g., RS256, ES256. Uses a private key for signing and a public key for verification.

4.  **Key Concepts:**
    *   **Statelessness:** JWTs contain all necessary information, reducing server-side session storage.
    *   **Authentication vs. Authorization:** JWTs primarily handle authentication (who you are) and can carry authorization data (what you can do).
    *   **Token Revocation:** Mechanisms to invalidate tokens before their natural expiry (e.g., blacklisting, short-lived tokens with refresh tokens).
    *   **Token Storage:** Secure client-side storage strategies (HTTP-only cookies, memory).
    *   **HTTPS:** Essential for protecting tokens in transit.

5.  **TypeScript Libraries (Node.js/Browser):**
    *   `jsonwebtoken` (Node.js): For signing and verifying JWTs.
    *   `jose` (Node.js/Browser): Modern, comprehensive library for JWT, JWS, JWE, JWA, JWK.
    *   `@types/jsonwebtoken`: TypeScript type definitions.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Use short-lived access tokens and long-lived refresh tokens.** Access tokens should expire quickly (e.g., 15-60 minutes) to minimize the impact of compromise. Refresh tokens, stored securely, can be used to obtain new access tokens.
- ✅ **Store refresh tokens in HTTP-only, Secure, SameSite cookies.** This protects against XSS and CSRF attacks.
- ✅ **Store access tokens in memory or session storage.** Avoid `localStorage` for access tokens due to XSS vulnerability.
- ✅ **Always validate JWTs on the server-side.** Verify signature, expiration (`exp`), "not before" (`nbf`), issuer (`iss`), and audience (`aud`) claims.
- ✅ **Use strong, randomly generated secret keys/private keys.** Store them securely (environment variables, secret management services), never hardcode or commit to VCS.
- ✅ **Enforce HTTPS for all communication.** Protects tokens from Man-in-the-Middle (MITM) attacks.
- ✅ **Implement token revocation for refresh tokens.** Allow users to log out or invalidate compromised tokens immediately.
- ✅ **Explicitly whitelist allowed signing algorithms.** Reject tokens using the "none" algorithm to prevent critical vulnerabilities.
- ✅ **Keep JWT payloads minimal and non-sensitive.** JWTs are encoded, not encrypted by default. Sensitive data should not be stored directly in the payload.
- ✅ **Implement robust error handling** for token validation failures, providing generic error messages to clients.
- ✅ **Use TypeScript interfaces for JWT payloads** to ensure type safety and improve maintainability.
- ✅ **Consider using Key IDs (kid)** in JWT headers for smoother key rotation, especially in distributed systems.

### Never Recommend (❌ anti-patterns)

- ❌ **Storing JWTs (especially access tokens) in `localStorage`.** Highly vulnerable to XSS attacks.
- ❌ **Using long-lived access tokens without a revocation mechanism.** Increases the window of vulnerability if a token is compromised.
- ❌ **Not validating the JWT signature or claims on the server.** Allows attackers to forge or tamper with tokens.
- ❌ **Accepting the "none" algorithm for JWTs.** A critical security flaw that allows bypassing signature verification.
- ❌ **Hardcoding secret keys or committing them to version control.** Leads to easy compromise.
- ❌ **Sending JWTs over HTTP (non-HTTPS) connections.** Exposes tokens to interception.
- ❌ **Storing sensitive user data (e.g., passwords, PII) directly in the JWT payload.** JWTs are easily decoded.
- ❌ **Over-stuffing the JWT payload with excessive or frequently changing data.** Leads to token bloat and stale data.
- ❌ **Using JWTs as primary session storage for server-side state.** Defeats the purpose of statelessness and complicates revocation.
- ❌ **Ignoring `exp`, `nbf`, `iss`, or `aud` claims during validation.** Weakens security posture.

### Common Questions & Responses (FAQ format)

**Q: Where should I store JWTs on the client-side?**
A: Access tokens (short-lived) should be stored in memory or session storage. Refresh tokens (long-lived) should be stored in HTTP-only, Secure, SameSite cookies. Avoid `localStorage` for any tokens.

**Q: How do I handle token expiration and renewal?**
A: Use short-lived access tokens. When an access token expires, the client should use a refresh token (sent from an HTTP-only cookie) to request a new access token from the server. The server should validate the refresh token and issue a new access/refresh token pair.

**Q: What's the difference between HS256 and RS256? When should I use each?**
A: HS256 (HMAC-SHA256) is a symmetric algorithm, using the same secret key for signing and verification. It's simpler but requires the secret to be shared. RS256 (RSA-SHA256) is an asymmetric algorithm, using a private key for signing and a public key for verification. RS256 is preferred in distributed systems or when the issuer and verifier are different entities, as only the public key needs to be shared.

**Q: How can I revoke a JWT before its expiration?**
A: Since JWTs are stateless, direct revocation is not built-in. For access tokens, rely on their short lifespan. For refresh tokens, implement a server-side blacklist/denylist or a database to track revoked tokens. When a user logs out or a token is compromised, add the refresh token's `jti` (JWT ID) to the blacklist.

**Q: Is it safe to put user roles/permissions in the JWT payload?**
A: Yes, for authorization purposes, but keep it minimal. Only include static, non-sensitive roles or permissions that don't change frequently. For dynamic or sensitive permissions, store a user ID in the JWT and fetch permissions from a database or authorization service on each request.

## Anti-Patterns to Flag

### Anti-Pattern 1: Storing Tokens in `localStorage`

**BAD (Vulnerable to XSS):**
```typescript
// client-side code
localStorage.setItem('accessToken', jwtToken);

// Malicious script can easily steal:
// const stolenToken = localStorage.getItem('accessToken');
```

**GOOD (More secure for refresh tokens, access tokens in memory):**
```typescript
// Server-side setting HTTP-only cookie for refresh token
// Example in Node.js with Express:
res.cookie('refreshToken', refreshToken, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production', // Use secure in production
  sameSite: 'strict', // Protects against CSRF
  expires: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
});

// Client-side storing short-lived access token in memory
let accessToken: string | null = null;

function setAccessToken(token: string) {
  accessToken = token;
}

function getAccessToken(): string | null {
  return accessToken;
}

// On page refresh, access token is lost, requiring refresh token flow.
```

### Anti-Pattern 2: Not Validating All Claims / Accepting "none" Algorithm

**BAD (Allows forged tokens):**
```typescript
import jwt from 'jsonwebtoken';

// Server-side verification (missing algorithm check, not validating all claims)
try {
  // If an attacker changes 'alg' to 'none' and removes signature, this might pass!
  const decoded = jwt.verify(token, process.env.JWT_SECRET as string);
  console.log('Decoded (potentially insecure):', decoded);
} catch (error) {
  console.error('Token verification failed:', error.message);
}
```

**GOOD (Robust validation):**
```typescript
import jwt from 'jsonwebtoken';

interface JwtPayloadWithCustomClaims extends jwt.JwtPayload {
  userId: string;
  roles: string[];
}

// Server-side verification with explicit algorithm and claim validation
const JWT_SECRET = process.env.JWT_SECRET as string;
const JWT_ALGORITHM = 'HS256'; // Whitelist allowed algorithm
const JWT_ISSUER = 'my-auth-service';
const JWT_AUDIENCE = 'my-web-app';

try {
  const decoded = jwt.verify(token, JWT_SECRET, {
    algorithms: [JWT_ALGORITHM], // Explicitly allow only HS256
    issuer: JWT_ISSUER,
    audience: JWT_AUDIENCE,
    // 'ignoreExpiration' and 'ignoreNotBefore' should generally be false
  }) as JwtPayloadWithCustomClaims;

  // Further custom claim validation
  if (!decoded.userId || !decoded.roles || !Array.isArray(decoded.roles)) {
    throw new Error('Invalid JWT payload structure');
  }

  console.log('Decoded (secure):', decoded);
} catch (error) {
  if (error instanceof jwt.TokenExpiredError) {
    console.error('Token expired:', error.message);
  } else if (error instanceof jwt.JsonWebTokenError) {
    console.error('Invalid token:', error.message);
  } else {
    console.error('Token verification failed:', error.message);
  }
}
```

### Anti-Pattern 3: Storing Sensitive Data in Payload

**BAD (Sensitive data exposed):**
```typescript
// Server-side token generation
const user = {
  id: 'user123',
  email: 'user@example.com',
  passwordHash: 'hashedpassword123', // NEVER store this!
  creditCardInfo: '**** **** **** 1234', // NEVER store this!
};
const token = jwt.sign(user, process.env.JWT_SECRET as string);

// Anyone can decode the token and see sensitive info!
// jwt.decode(token) => { id: 'user123', email: 'user@example.com', passwordHash: '...', creditCardInfo: '...' }
```

**GOOD (Minimal, non-sensitive payload):**
```typescript
// Server-side token generation
const userPayload = {
  userId: 'user123',
  roles: ['admin', 'editor'],
  // Only essential, non-sensitive data
};
const token = jwt.sign(userPayload, process.env.JWT_SECRET as string, {
  expiresIn: '15m',
  issuer: 'my-auth-service',
  audience: 'my-web-app',
});
```

## Code Review Checklist

- [ ] Are access tokens short-lived (e.g., 15-60 minutes)?
- [ ] Are refresh tokens used, and are they stored in HTTP-only, Secure, SameSite cookies?
- [ ] Are access tokens stored in memory or session storage on the client-side?
- [ ] Is `localStorage` explicitly avoided for storing any JWTs?
- [ ] Is server-side validation performed for every incoming JWT?
- [ ] Does validation include signature, `exp`, `nbf`, `iss`, and `aud` claims?
- [ ] Is the "none" algorithm explicitly disallowed during verification?
- [ ] Are secret keys/private keys strong, randomly generated, and stored securely (not hardcoded or in VCS)?
- [ ] Is HTTPS enforced for all API communication?
- [ ] Is there a mechanism for refresh token revocation (e.g., blacklist)?
- [ ] Is the JWT payload minimal and free of sensitive information?
- [ ] Are TypeScript interfaces used for JWT payloads?
- [ ] Is error handling robust for token-related issues, providing generic messages to clients?
- [ ] If asymmetric algorithms (RS256) are used, are public/private keys managed securely?
- [ ] Is there a strategy for key rotation?

## Related Skills

- `secrets-management`: For securely storing JWT secret keys and other sensitive configuration.
- `api-security`: General API security principles that complement JWT authentication.
- `typescript-strict-mode`: Ensures type safety and code quality in TypeScript implementations.
- `rest-api-design`: For designing secure and efficient API endpoints that consume JWTs.

## Examples Directory Structure

```
examples/
├── server/
│   ├── src/
│   │   ├── auth/
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── jwt.strategy.ts
│   │   │   └── auth.middleware.ts
│   │   ├── users/
│   │   │   └── users.service.ts
│   │   ├── app.ts
│   │   └── types.ts
│   ├── .env.example
│   └── package.json
├── client/
│   ├── src/
│   │   ├── components/
│   │   │   └── AuthForm.tsx
│   │   ├── services/
│   │   │   └── auth.api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── .env.example
│   └── package.json
└── README.md
```

## Custom Scripts Section

Here are 3 automation scripts designed to streamline common tasks related to JWT authentication:

1.  **`generate_jwt.py` (Python): JWT Token Generator**
    *   **Purpose:** Automates the creation of JWT tokens for development and testing purposes. It allows specifying payload data, secret key, algorithm, and expiration time, saving developers from manually encoding tokens or using online tools.
    *   **Pain Point Solved:** Manually crafting JWTs for testing different scenarios (e.g., expired tokens, specific roles) is tedious and error-prone.
    *   **Usage:** `python scripts/generate_jwt.py --payload '{"userId": "test", "role": "user"}' --secret "mysecret" --expires-in 1h`

2.  **`validate_jwt.sh` (Shell): JWT Validator & Inspector**
    *   **Purpose:** Provides a quick command-line utility to decode a JWT, display its header and payload, and perform basic checks like expiration. It helps developers quickly inspect tokens received from APIs or generated during development.
    *   **Pain Point Solved:** Debugging JWT issues often involves copying tokens to online decoders. This script offers a local, quick, and scriptable alternative.
    *   **Usage:** `bash scripts/validate_jwt.sh <your_jwt_token>`

3.  **`rotate_jwt_secret.py` (Python): JWT Secret Key Rotator**
    *   **Purpose:** Generates a cryptographically secure random string suitable for a JWT secret key and can optionally update a `.env` file. It also provides crucial guidance on the key rotation process, which is a critical security practice.
    *   **Pain Point Solved:** Securely generating and managing secret keys, especially during rotation, can be complex and lead to insecure practices if not handled correctly.
    *   **Usage:** `python scripts/rotate_jwt_secret.py --output-env .env --key-name JWT_SECRET`
