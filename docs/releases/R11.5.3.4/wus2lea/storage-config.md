---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:18:32.762898'
preview_features: true
region: wus2lea
tags:
- wus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: Monitoring Agent Upgrade - WUS2LEA
version: 1.2.0
---


# Storage Configuration - WUS2LEA

## Overview

Storage configuration procedure for **westus2euap** region.

### Storage Context

- **Target Region**: WUS2LEA (westus2euap)
- **Storage Account**: storagewus2lea
- **File System**: ext4

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible wus2lea_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible wus2lea_all -m mount -a "
  path=/opt/data
  src=/dev/sdb1
  fstype=ext4
  state=mounted
"

# Update fstab for persistence
ansible wus2lea_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/sdb1 /opt/data ext4 defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible wus2lea_all -m file -a "
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
**Region**: WUS2LEA (westus2euap)