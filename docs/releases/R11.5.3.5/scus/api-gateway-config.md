---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:26:36.824411'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: api-gateway-config.j2 - SCUS
version: '1.0'
---


# API Gateway Configuration - SCUS

## Overview

API gateway configuration procedure for **southcentralus** region.

### API Gateway Context

- **Target Region**: SCUS (southcentralus)
- **Gateway**: apigw-scus
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible scus_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible scus_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible scus_gateway -m blockinfile -a "
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
**Region**: SCUS (southcentralus)