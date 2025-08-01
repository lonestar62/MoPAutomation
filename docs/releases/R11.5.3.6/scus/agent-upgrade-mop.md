---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:10.186396'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: agent-upgrade-mop.j2 - SCUS
version: '1.0'
---

# Agent Upgrade Procedure - SCUS

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **southcentralus** region (scus).

### Environment Details

- **Region**: SCUS (southcentralus)
- **ADO Organization**: { vault_scus_ado_organization }
- **Project**: { vault_scus_ado_project }
- **Environment**: scus-production
- **Resource Group**: rg-prod-scus
- **Key Vault**: kv-prod-scus

## Prerequisites

1. Access to { vault_scus_ado_organization } Azure DevOps organization
2. Permissions to scus-production environment
3. Network connectivity to southcentralus region
4. Service principal access to rg-prod-scus

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- All servers in scus region

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible scus_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible scus_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible scus_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "scus"
  environment: "scus-production"
  log_level: "INFO"
  endpoints:
    primary: "monitoring-scus.example.com"
    backup: "monitoring-backup-scus.example.com"
  retention_days: 30
```

### Step 3: Azure DevOps Pipeline Execution

The upgrade process will trigger the following pipeline:

- **Pipeline ID**: { vault_scus_pipeline_id }
- **Organization**: { vault_scus_ado_organization }
- **Project**: { vault_scus_ado_project }
- **Environment**: scus-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible scus_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible scus_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible scus_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible scus_monitoring -m shell -a "monitoring-agent --test-connection"
```

## Success Criteria

The upgrade is considered successful when:

- [ ] All agents report new version: v2.1.6
- [ ] All agents are in active/running state
- [ ] Configuration validation passes on all hosts
- [ ] Connectivity tests pass to all endpoints
- [ ] No error alerts in monitoring dashboard
- [ ] Azure DevOps pipeline completes successfully

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)