---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:11.301474'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: storage-config.j2 - EUS2
version: '1.0'
---


# Storage Configuration - EUS2

## Overview

Storage configuration procedure for **eastus2** region.

### Storage Context

- **Target Region**: EUS2 (eastus2)
- **Storage Account**: storageeus2
- **File System**: ext4

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible eus2_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible eus2_all -m mount -a "
  path=/opt/data
  src=/dev/sdb1
  fstype=ext4
  state=mounted
"

# Update fstab for persistence
ansible eus2_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/sdb1 /opt/data ext4 defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible eus2_all -m file -a "
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
**Region**: EUS2 (eastus2)