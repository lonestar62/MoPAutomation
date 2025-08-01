---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.846130'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# API Gateway Configuration - WUS3

## Overview

API gateway configuration procedure for **westus3** region.

### API Gateway Context

- **Target Region**: WUS3 (westus3)
- **Gateway**: apigw-wus3
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible wus3_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible wus3_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible wus3_gateway -m blockinfile -a "
  dest=/etc/nginx/conf.d/api-routes.conf
  marker='# {mark} CORS CONFIGURATION'
  block='
    add_header Access-Control-Allow-Origin \"*\";
    add_header Access-Control-Allow-Methods \"GET, POST, PUT, DELETE, OPTIONS\";
    add_header Access-Control-Allow-Headers \"Authorization, Content-Type\";
  '
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)