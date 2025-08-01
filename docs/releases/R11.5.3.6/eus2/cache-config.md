---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:11.720898'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: cache-config.j2 - EUS2
version: '1.0'
---


# Cache Configuration - EUS2

## Overview

Cache configuration procedure for **eastus2** region.

### Cache Context

- **Target Region**: EUS2 (eastus2)
- **Cache Type**: Redis
- **Cache Size**: 4gb

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible eus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 4gb'
"

# Configure eviction policy
ansible eus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible eus2_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible eus2_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)