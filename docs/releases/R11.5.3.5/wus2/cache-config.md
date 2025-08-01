---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:26:36.879249'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: cache-config.j2 - WUS2
version: '1.0'
---


# Cache Configuration - WUS2

## Overview

Cache configuration procedure for **westus2** region.

### Cache Context

- **Target Region**: WUS2 (westus2)
- **Cache Type**: Redis
- **Cache Size**: 4gb

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible wus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 4gb'
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