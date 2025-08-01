---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:27:11.748879'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: cache-config.j2 - WUS3
version: '1.0'
---


# Cache Configuration - WUS3

## Overview

Cache configuration procedure for **westus3** region.

### Cache Context

- **Target Region**: WUS3 (westus3)
- **Cache Type**: Redis
- **Cache Size**: 8gb

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible wus3_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 8gb'
"

# Configure eviction policy
ansible wus3_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible wus3_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible wus3_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)