---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:36.790213'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: api-gateway-config.j2 - EUS2
version: '1.0'
---


# API Gateway Configuration - EUS2

## Overview

API gateway configuration procedure for **eastus2** region.

### API Gateway Context

- **Target Region**: EUS2 (eastus2)
- **Gateway**: apigw-eus2
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible eus2_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible eus2_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible eus2_gateway -m blockinfile -a "
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
**Region**: EUS2 (eastus2)