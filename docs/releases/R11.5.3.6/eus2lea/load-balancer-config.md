---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:27:11.274194'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: load-balancer-config.j2 - EUS2LEA
version: '1.0'
---


# Load Balancer Configuration - EUS2LEA

## Overview

Load balancer configuration procedure for **eastus2euap** region.

### Load Balancer Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Load Balancer**: lb-eus2lea
- **Backend Pool**: backend-pool-eus2lea

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible eus2lea_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible eus2lea_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_eus2lea {
    server 10.4.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.4.1.11:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name app-eus2lea.example.com;
    
    location / {
        proxy_pass http://backend_eus2lea;
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
ansible eus2lea_lb -m blockinfile -a "
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
**Region**: EUS2LEA (eastus2euap)