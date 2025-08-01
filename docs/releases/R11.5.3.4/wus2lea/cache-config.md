---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:18:32.903822'
preview_features: true
region: wus2lea
tags:
- wus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: Monitoring Agent Upgrade - WUS2LEA
version: 1.2.0
---


# Cache Configuration - WUS2LEA

## Overview

Cache configuration procedure for **westus2euap** region.

### Cache Context

- **Target Region**: WUS2LEA (westus2euap)
- **Cache Type**: Redis
- **Cache Size**: 2GB

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible wus2lea_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 2gb'
"

# Configure eviction policy
ansible wus2lea_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible wus2lea_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible wus2lea_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)