---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.744617'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
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
    server 10.0.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
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