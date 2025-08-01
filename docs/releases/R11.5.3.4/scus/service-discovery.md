---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.771264'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Service Discovery - SCUS

## Overview

Service discovery configuration procedure for **southcentralus** region.

### Service Discovery Context

- **Target Region**: SCUS (southcentralus)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible scus_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible scus_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible scus_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible scus_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)