---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.848669'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: api-gateway-config.j2 - WUS2LEA
version: '1.0'
---


# API Gateway Configuration - WUS2LEA

## Overview

API gateway configuration procedure for **westus2euap** region.

### API Gateway Context

- **Target Region**: WUS2LEA (westus2euap)
- **Gateway**: apigw-wus2lea
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible wus2lea_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible wus2lea_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible wus2lea_gateway -m blockinfile -a "
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
**Region**: WUS2LEA (westus2euap)