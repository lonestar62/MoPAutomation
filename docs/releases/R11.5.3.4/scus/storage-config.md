---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.760362'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Storage Configuration - SCUS

## Overview

Storage configuration procedure for **southcentralus** region.

### Storage Context

- **Target Region**: SCUS (southcentralus)
- **Storage Account**: storagescus
- **File System**: ext4

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible scus_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible scus_all -m mount -a "
  path=/opt/data
  src=/dev/sdb1
  fstype=ext4
  state=mounted
"

# Update fstab for persistence
ansible scus_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/sdb1 /opt/data ext4 defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible scus_all -m file -a "
  path=/opt/data
  owner=appuser
  group=appgroup
  mode=0755
  recurse=yes
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)