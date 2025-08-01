---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.484313'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: load-balancer-config.j2 - WUS2LEA
version: '1.0'
---


# Load Balancer Configuration - WUS2LEA

## Overview

Load balancer configuration procedure for **westus2euap** region.

### Load Balancer Context

- **Target Region**: WUS2LEA (westus2euap)
- **Load Balancer**: lb-wus2lea
- **Backend Pool**: backend-pool-wus2lea

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible wus2lea_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible wus2lea_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_wus2lea {
    server 10.5.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.5.1.11:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name app-wus2lea.example.com;
    
    location / {
        proxy_pass http://backend_wus2lea;
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
ansible wus2lea_lb -m blockinfile -a "
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
**Region**: WUS2LEA (westus2euap)