---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:27:11.225855'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: load-balancer-config.j2 - WUS2
version: '1.0'
---


# Load Balancer Configuration - WUS2

## Overview

Load balancer configuration procedure for **westus2** region.

### Load Balancer Context

- **Target Region**: WUS2 (westus2)
- **Load Balancer**: lb-wus2
- **Backend Pool**: backend-pool-wus2

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible wus2_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible wus2_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_wus2 {
    server 10.1.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.1.1.11:80 max_fails=3 fail_timeout=30s;
    server 10.1.1.12:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name app-wus2.example.com;
    
    location / {
        proxy_pass http://backend_wus2;
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
ansible wus2_lb -m blockinfile -a "
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
**Region**: WUS2 (westus2)