---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.857073'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: api-gateway-config.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# API Gateway Configuration - EUS2LEA

## Overview

API gateway configuration procedure for **eastus2euap** region.

### API Gateway Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Gateway**: apigw-eus2lea
- **Version**: v1

## Gateway Configuration

### Route Configuration
```bash
# Configure API routes
ansible eus2lea_gateway -m template -a "
  src=api-routes.conf.j2
  dest=/etc/nginx/conf.d/api-routes.conf
"

# Configure rate limiting
ansible eus2lea_gateway -m template -a "
  src=rate-limit.conf.j2
  dest=/etc/nginx/conf.d/rate-limit.conf
"
```

### Security Policies
```bash
# Configure CORS policies
ansible eus2lea_gateway -m blockinfile -a "
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
**Region**: EUS2LEA (eastus2euap)