---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:26:36.902018'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: cache-config.j2 - SCUS
version: '1.0'
---


# Cache Configuration - SCUS

## Overview

Cache configuration procedure for **southcentralus** region.

### Cache Context

- **Target Region**: SCUS (southcentralus)
- **Cache Type**: Redis
- **Cache Size**: 4gb

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible scus_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 4gb'
"

# Configure eviction policy
ansible scus_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible scus_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible scus_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)