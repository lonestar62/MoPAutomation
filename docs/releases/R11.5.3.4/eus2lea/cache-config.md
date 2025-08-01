---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.902346'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: cache-config.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# Cache Configuration - EUS2LEA

## Overview

Cache configuration procedure for **eastus2euap** region.

### Cache Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Cache Type**: Redis
- **Cache Size**: 2GB

## Redis Configuration

### Cache Setup
```bash
# Configure Redis memory settings
ansible eus2lea_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory'
  line='maxmemory 2gb'
"

# Configure eviction policy
ansible eus2lea_cache -m lineinfile -a "
  dest=/etc/redis/redis.conf
  regexp='^maxmemory-policy'
  line='maxmemory-policy allkeys-lru'
"

# Restart Redis
ansible eus2lea_cache -m systemd -a "name=redis state=restarted"
```

### Application Cache Integration
```bash
# Update application cache configuration
ansible eus2lea_app -m template -a "
  src=cache-config.j2
  dest=/opt/app/config/cache.conf
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)