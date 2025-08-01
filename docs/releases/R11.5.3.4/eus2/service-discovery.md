---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: eus2-production
generated_at: '2025-08-01T08:18:32.767488'
region: eus2
tags:
- eus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: service-discovery.j2
title: Monitoring Agent Upgrade - EUS2
version: 1.2.0
---


# Service Discovery - EUS2

## Overview

Service discovery configuration procedure for **eastus2** region.

### Service Discovery Context

- **Target Region**: EUS2 (eastus2)
- **Discovery Service**: Consul
- **Registration Method**: Automatic

## Service Registration

### Application Services
```bash
# Register web services
ansible eus2_web -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/web-service.json
"

# Register database services
ansible eus2_db -m template -a "
  src=consul-service.json.j2
  dest=/etc/consul.d/db-service.json
"

# Reload consul configuration
ansible eus2_all -m systemd -a "name=consul state=reloaded"
```

### Health Check Registration
```bash
# Configure health checks
ansible eus2_all -m template -a "
  src=health-check.json.j2
  dest=/etc/consul.d/health-check.json
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)