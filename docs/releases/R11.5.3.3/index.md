---
title: Release R11.5.3.3 Documentation
description: Q1 2025 Release: Security patches, agent upgrades, and infrastructure updates
version: R11.5.3.3
created_at: 2025-08-01T08:11:51.817202
created_by: release_engineer
total_mops: 5
layout: release_index
---

# Release R11.5.3.3 Documentation

**Description**: Q1 2025 Release: Security patches, agent upgrades, and infrastructure updates
**Created**: 2025-08-01T08:11:51.817202
**Created By**: release_engineer
**Total MOPs**: 5

## Execution Order

MOPs will be executed in the following regional order:
1. **EUS2** - East US 2 (Primary, Documentation Hub)
2. **WUS2** - West US 2 (Primary West)
3. **WUS3** - West US 3 (Modern Infrastructure)
4. **SCUS** - South Central US (Hub)
5. **EUS2LEA** - East US 2 LEA (Early Access)
6. **WUS2LEA** - West US 2 LEA (Early Access)

## MOPs in this Release

### Agent-Upgrade MOPs

#### Agent Upgrade Mop (`agent-upgrade-mop`)
- **Description**: MOP procedure: agent-upgrade-mop
- **Risk Level**: medium
- **Duration**: ~30 minutes
- **Playbooks**: edit_yaml.yml, commit_to_git.yml, run_manual_pipeline.yml
- **Regional Documentation**:
  - [EUS2](eus2/agent-upgrade-mop.md)
  - [WUS2](wus2/agent-upgrade-mop.md)
  - [WUS3](wus3/agent-upgrade-mop.md)
  - [SCUS](scus/agent-upgrade-mop.md)
  - [EUS2LEA](eus2lea/agent-upgrade-mop.md)
  - [WUS2LEA](wus2lea/agent-upgrade-mop.md)

### Infrastructure MOPs

#### Infrastructure Deployment (`infrastructure-deployment`)
- **Description**: MOP procedure: infrastructure-deployment
- **Risk Level**: medium
- **Duration**: ~30 minutes
- **Playbooks**: edit_yaml.yml, commit_to_git.yml, run_manual_pipeline.yml
- **Regional Documentation**:
  - [EUS2](eus2/infrastructure-deployment.md)
  - [WUS2](wus2/infrastructure-deployment.md)
  - [WUS3](wus3/infrastructure-deployment.md)
  - [SCUS](scus/infrastructure-deployment.md)
  - [EUS2LEA](eus2lea/infrastructure-deployment.md)
  - [WUS2LEA](wus2lea/infrastructure-deployment.md)

### Network MOPs

#### Network Security Configuration (`network-security-config`)
- **Description**: Configure network security groups and firewall rules
- **Risk Level**: high
- **Duration**: ~45 minutes
- **Playbooks**: edit_yaml.yml, commit_to_git.yml, run_manual_pipeline.yml
- **Regional Documentation**:
  - [EUS2](eus2/network-security-config.md)
  - [WUS2](wus2/network-security-config.md)
  - [WUS3](wus3/network-security-config.md)
  - [SCUS](scus/network-security-config.md)
  - [EUS2LEA](eus2lea/network-security-config.md)
  - [WUS2LEA](wus2lea/network-security-config.md)

### Backup MOPs

#### Database Maintenance (`database-maintenance`)
- **Description**: Perform routine database maintenance and optimization
- **Risk Level**: medium
- **Duration**: ~60 minutes
- **Playbooks**: edit_yaml.yml, commit_to_git.yml, run_manual_pipeline.yml
- **Regional Documentation**:
  - [EUS2](eus2/database-maintenance.md)
  - [WUS2](wus2/database-maintenance.md)
  - [WUS3](wus3/database-maintenance.md)
  - [SCUS](scus/database-maintenance.md)
  - [EUS2LEA](eus2lea/database-maintenance.md)
  - [WUS2LEA](wus2lea/database-maintenance.md)

### Patch-Linux MOPs

#### Linux System Patching (`patch-linux-systems`)
- **Description**: Apply security and system patches to Linux servers
- **Risk Level**: high
- **Duration**: ~90 minutes
- **Playbooks**: patch_linux.yml
- **Regional Documentation**:
  - [EUS2](eus2/patch-linux-systems.md)
  - [WUS2](wus2/patch-linux-systems.md)
  - [WUS3](wus3/patch-linux-systems.md)
  - [SCUS](scus/patch-linux-systems.md)
  - [EUS2LEA](eus2lea/patch-linux-systems.md)
  - [WUS2LEA](wus2lea/patch-linux-systems.md)
