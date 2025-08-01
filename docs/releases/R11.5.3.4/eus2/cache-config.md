---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: eus2-production
generated_at: '2025-08-01T08:18:32.894571'
region: eus2
tags:
- eus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: Monitoring Agent Upgrade - EUS2
version: 1.2.0
---


# Cache Configuration - EUS2

## Overview

Cache configuration procedure for **eastus2** region.

### Cache Context

- **Target Region**: EUS2 (eastus2)
- **Cache Type**: Redis
- **Cache Size**: 2GB

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible eus2_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 2gb'
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