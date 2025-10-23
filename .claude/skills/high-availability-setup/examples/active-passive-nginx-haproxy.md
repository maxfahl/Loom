# Active-Passive Setup with Nginx and HAProxy

This document outlines a conceptual active-passive high availability setup using HAProxy as a load balancer and Nginx as the web server. In this configuration, one Nginx instance is active and serves traffic, while another is passive and stands by, ready to take over in case of a failure.

## Architecture Overview

```
                               +-------------------+
                               |     HAProxy       |
                               | (Virtual IP/VIP)  |
                               +---------+---------+
                                         |
                                         |
                 +-----------------------+-----------------------+
                 |                                               |
         +-------v-------+                             +-------v-------+
         |  Nginx Server 1 (Active)  |                             |  Nginx Server 2 (Passive) |
         |   (Web Application)   |                             |   (Web Application)   |
         +-----------------------+                             +-----------------------+
```

## Components

*   **HAProxy**: Acts as the entry point for all traffic. It monitors the health of the Nginx servers and directs traffic to the active server. In case of a failure, it automatically switches traffic to the passive server.
*   **Nginx Server 1 (Active)**: The primary web server instance that actively serves client requests.
*   **Nginx Server 2 (Passive)**: The secondary web server instance that is kept in sync with the active server (e.g., through shared storage or replication of application code/data) and is ready to become active upon failover.
*   **Virtual IP (VIP)**: A floating IP address that HAProxy uses. This IP can be moved between HAProxy instances (if HAProxy itself is made highly available, e.g., with Keepalived) to ensure continuous accessibility.

## Conceptual Configuration Examples

### HAProxy Configuration (`haproxy.cfg`)

```ini
global
    log /dev/log    local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    option httpchk GET /healthz # Health check endpoint on Nginx
    server nginx1 192.168.1.101:80 check inter 2000 fall 3 rise 2
    server nginx2 192.168.1.102:80 check inter 2000 fall 3 rise 2 backup

# Explanation of backend configuration:
# - 'balance roundrobin': Distributes requests in a round-robin fashion (though for active-passive, only one will be active).
# - 'option httpchk GET /healthz': HAProxy will send a GET request to /healthz to check server health.
# - 'server nginx1 192.168.1.101:80': Defines the primary Nginx server.
# - 'check inter 2000 fall 3 rise 2': Checks every 2 seconds, marks down after 3 failures, up after 2 successes.
# - 'server nginx2 192.168.1.102:80 check inter 2000 fall 3 rise 2 backup': Defines the passive Nginx server as a backup.
#   HAProxy will only send traffic to 'nginx2' if 'nginx1' is down.
```

### Nginx Configuration (`nginx.conf` - relevant part)

Each Nginx server would have a standard configuration for serving the web application. A crucial part is the health check endpoint.

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /var/www/html;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }

    location /healthz {
        access_log off;
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
```

## Failover Mechanism

1.  HAProxy continuously monitors both Nginx servers using the `/healthz` endpoint.
2.  If Nginx Server 1 (active) fails its health checks (e.g., the Nginx process stops or the application becomes unresponsive), HAProxy detects this.
3.  HAProxy automatically stops sending traffic to Nginx Server 1.
4.  Because Nginx Server 2 is configured as `backup`, HAProxy will immediately start directing all traffic to Nginx Server 2.
5.  Once Nginx Server 1 recovers and passes its health checks, HAProxy will mark it as healthy again. Depending on the HAProxy configuration, it might switch back to Nginx Server 1 or continue using Nginx Server 2 until it fails.

## Considerations for Active-Passive

*   **Data Synchronization**: Ensure that any application data or state is synchronized between the active and passive Nginx instances. This might involve shared storage (NFS, GlusterFS), database replication, or distributed caching.
*   **Session Management**: If your application uses session state, ensure it's handled externally (e.g., in a distributed cache like Redis) or replicated to avoid session loss during failover.
*   **Deployment**: Deploying updates to an active-passive setup requires careful planning to avoid downtime. Typically, you'd update the passive server, make it active, then update the old active server.
*   **HAProxy HA**: For true high availability, HAProxy itself should be made redundant, often using tools like Keepalived to manage a floating Virtual IP (VIP) between two HAProxy instances.
