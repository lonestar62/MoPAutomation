---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:27:11.349135'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: storage-config.j2 - EUS2LEA
version: '1.0'
---


# Storage Configuration - EUS2LEA

## Overview

Storage configuration procedure for **eastus2euap** region.

### Storage Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Storage Account**: storageeus2lea
- **File System**: ext4

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible eus2lea_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible eus2lea_all -m mount -a "
  path=/opt/data
  src=/dev/sdb1
  fstype=ext4
  state=mounted
"

# Update fstab for persistence
ansible eus2lea_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/sdb1 /opt/data ext4 defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible eus2lea_all -m file -a "
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
**Region**: EUS2LEA (eastus2euap)