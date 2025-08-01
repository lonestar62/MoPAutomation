---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:27:11.387815'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: service-discovery.j2 - WUS2
version: '1.0'
---


# Service Discovery - WUS2

## Overview

Service discovery configuration procedure for **westus2** region.

### Service Discovery Context

- **Target Region**: WUS2 (westus2)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible wus2_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible wus2_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible wus2_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible wus2_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)