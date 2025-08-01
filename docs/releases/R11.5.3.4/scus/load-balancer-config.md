---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.745987'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: load-balancer-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Load Balancer Configuration - SCUS

## Overview

Load balancer configuration procedure for **southcentralus** region.

### Load Balancer Context

- **Target Region**: SCUS (southcentralus)
- **Load Balancer**: lb-scus
- **Backend Pool**: backend-pool-scus

## Load Balancer Rules

### HTTP/HTTPS Rules
```bash
# Configure HTTP to HTTPS redirect
ansible scus_lb -m lineinfile -a "
  dest=/etc/nginx/sites-available/default
  regexp='listen 80'
  line='    listen 80; return 301 https://\$server_name\$request_uri;'
"

# Configure HTTPS backend
ansible scus_lb -m blockinfile -a "
  dest=/etc/nginx/sites-available/default
  marker='# {mark} HTTPS BACKEND'
  block='
upstream backend_scus {
    server 10.0.1.10:80 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:80 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    location / {
        proxy_pass http://backend_scus;
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
ansible scus_lb -m blockinfile -a "
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
**Region**: SCUS (southcentralus)