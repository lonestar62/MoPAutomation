---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:26:36.616771'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: service-discovery.j2 - EUS2LEA
version: '1.0'
---


# Service Discovery - EUS2LEA

## Overview

Service discovery configuration procedure for **eastus2euap** region.

### Service Discovery Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible eus2lea_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible eus2lea_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible eus2lea_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible eus2lea_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)