---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.900566'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Cache Configuration - SCUS

## Overview

Cache configuration procedure for **southcentralus** region.

### Cache Context

- **Target Region**: SCUS (southcentralus)
- **Cache Type**: Redis
- **Cache Size**: 2GB

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible scus_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 2gb'
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