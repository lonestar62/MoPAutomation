---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:26:36.444439'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: load-balancer-config.j2 - WUS3
version: '1.0'
---


# Load Balancer Configuration - WUS3

## Overview

Load balancer configuration procedure for **westus3** region.

### Load Balancer Context

- **Target Region**: WUS3 (westus3)
- **Load Balancer**: lb-wus3
- **Backend Pool**: backend-pool-wus3

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible wus3_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible wus3_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_wus3 {
    server 10.2.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.2.1.11:80 max_fails=3 fail_timeout=30s;
    server 10.2.1.12:80 max_fails=3 fail_timeout=30s;
    server 10.2.1.13:80 max_fails=3 fail_timeout=30s;
    server 10.2.1.14:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name app-wus3.example.com;
    
    location / {
        proxy_pass http://backend_wus3;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
  '
"
```

### Health Checks
```bash
# Configure health check endpoint
ansible wus3_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HEALTH CHECK'
  block='
    location /health {
        access_log off;
        return 200 \"healthy\";
        add_header Content-Type text/plain;
    }
  '
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)