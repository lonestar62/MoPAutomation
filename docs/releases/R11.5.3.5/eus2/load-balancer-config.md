---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:36.418076'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: load-balancer-config.j2 - EUS2
version: '1.0'
---


# Load Balancer Configuration - EUS2

## Overview

Load balancer configuration procedure for **eastus2** region.

### Load Balancer Context

- **Target Region**: EUS2 (eastus2)
- **Load Balancer**: lb-eus2
- **Backend Pool**: backend-pool-eus2

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible eus2_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible eus2_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_eus2 {
    server 10.0.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:80 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name app-eus2.example.com;
    
    location / {
        proxy_pass http://backend_eus2;
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
ansible eus2_lb -m blockinfile -a "
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
**Region**: EUS2 (eastus2)