# Example Nginx Configuration for TLS 1.3

This document provides an example Nginx server block configuration that prioritizes TLS 1.3, uses strong cipher suites, and implements other security best practices for HTTPS. This configuration aims to achieve a high security rating on SSL/TLS testing services like SSL Labs.

## Nginx Server Block Configuration

```nginx
server {
    listen 443 ssl http2; # Listen on port 443 for HTTPS, enable HTTP/2
    listen [::]:443 ssl http2; # Listen on IPv6

    server_name your_domain.com www.your_domain.com; # Replace with your domain

    # SSL Certificate and Key Paths
    ssl_certificate /etc/nginx/ssl/your_domain.com.crt; # Path to your full chain certificate
    ssl_certificate_key /etc/nginx/ssl/your_domain.com.key; # Path to your private key

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/nginx/ssl/your_domain.com.crt; # Full chain certificate including root
    resolver 8.8.8.8 8.8.4.4 valid=300s; # Google Public DNS, adjust as needed
    resolver_timeout 5s;

    # TLS Protocol Configuration
    ssl_protocols TLSv1.3 TLSv1.2; # Prioritize TLS 1.3, allow TLS 1.2 for compatibility

    # Strong Cipher Suites (for TLS 1.2 and below, TLS 1.3 ciphers are negotiated separately)
    # This list is a strong recommendation, adjust based on your needs and client compatibility.
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256';
    ssl_prefer_server_ciphers on; # Server's cipher preference over client's

    # HSTS (HTTP Strict Transport Security)
    # Enforces HTTPS for a specified duration, preventing downgrade attacks.
    # max-age: how long the browser should remember to only access the site using HTTPS.
    # includeSubDomains: applies the rule to all subdomains.
    # preload: allows inclusion in browser preload lists (requires careful consideration).
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # Other Security Headers (Optional but Recommended)
    add_header X-Frame-Options "SAMEORIGIN" always; # Prevents clickjacking
    add_header X-Content-Type-Options "nosniff" always; # Prevents MIME-sniffing
    add_header X-XSS-Protection "1; mode=block" always; # Basic XSS protection
    add_header Referrer-Policy "no-referrer-when-downgrade" always; # Controls referrer information
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;" always; # Strict CSP, adjust as needed

    # SSL Session Cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1h;
    ssl_session_tickets off; # Disable session tickets for perfect forward secrecy

    # Diffie-Hellman Parameters (for perfect forward secrecy with older clients)
    # Generate with: openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    # Root for your web application
    root /var/www/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Optional: Redirect HTTP to HTTPS
    # server {
    #     listen 80;
    #     listen [::]:80;
    #     server_name your_domain.com www.your_domain.com;
    #     return 301 https://$host$request_uri;
    # }
}
```

## Key Best Practices Implemented

*   **TLS 1.3 Priority**: `ssl_protocols TLSv1.3 TLSv1.2;` ensures that TLS 1.3 is preferred when supported by the client and server.
*   **Strong Cipher Suites**: A carefully selected list of modern, secure cipher suites is used, excluding known weak or vulnerable ones.
*   **HTTP/2**: Enabled for performance benefits over HTTPS.
*   **OCSP Stapling**: Reduces overhead and improves privacy by allowing the server to provide OCSP responses directly to the client.
*   **HSTS (HTTP Strict Transport Security)**: Protects against protocol downgrade attacks and cookie hijacking by forcing browsers to interact with the server only over HTTPS.
*   **Security Headers**: Additional headers like `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`, and `Content-Security-Policy` enhance client-side security.
*   **Perfect Forward Secrecy (PFS)**: Achieved through ECDHE cipher suites and strong Diffie-Hellman parameters, ensuring that a compromise of the server's private key does not compromise past communications.
*   **SSL Session Tickets Disabled**: Improves PFS by preventing the reuse of session tickets.

## Before Deployment

1.  **Replace Placeholders**: Update `your_domain.com` and certificate paths.
2.  **Generate DH Parameters**: Create a strong `dhparam.pem` file (e.g., `openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048` or `4096`).
3.  **Obtain Valid Certificates**: Use certificates from a trusted CA (e.g., Let's Encrypt via Certbot) for production environments.
4.  **Test Configuration**: Use `nginx -t` to test the syntax of your Nginx configuration before reloading.
5.  **Audit with Tools**: Use online SSL/TLS testing tools (e.g., SSL Labs) to verify your configuration and identify any remaining weaknesses.
