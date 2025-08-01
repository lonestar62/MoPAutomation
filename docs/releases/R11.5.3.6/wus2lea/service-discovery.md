---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:27:11.444624'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: service-discovery.j2 - WUS2LEA
version: '1.0'
---


# Service Discovery - WUS2LEA

## Overview

Service discovery configuration procedure for **westus2euap** region.

### Service Discovery Context

- **Target Region**: WUS2LEA (westus2euap)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible wus2lea_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible wus2lea_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible wus2lea_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible wus2lea_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)