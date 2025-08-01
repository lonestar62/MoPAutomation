---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:26:36.801870'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: api-gateway-config.j2 - WUS2
version: '1.0'
---


# API Gateway Configuration - WUS2

## Overview

API gateway configuration procedure for **westus2** region.

### API Gateway Context

- **Target Region**: WUS2 (westus2)
- **Gateway**: apigw-wus2
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible wus2_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible wus2_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible wus2_gateway -m blockinfile -a "
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
**Region**: WUS2 (westus2)