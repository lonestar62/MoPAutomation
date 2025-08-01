---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.770075'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# Service Discovery - WUS3

## Overview

Service discovery configuration procedure for **westus3** region.

### Service Discovery Context

- **Target Region**: WUS3 (westus3)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible wus3_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible wus3_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible wus3_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible wus3_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)