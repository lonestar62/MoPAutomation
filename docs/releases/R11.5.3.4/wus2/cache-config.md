---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.897057'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Cache Configuration - WUS2

## Overview

Cache configuration procedure for **westus2** region.

### Cache Context

- **Target Region**: WUS2 (westus2)
- **Cache Type**: Redis
- **Cache Size**: 2GB

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible wus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 2gb'
"

# Configure eviction policy
ansible wus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible wus2_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible wus2_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)