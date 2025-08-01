---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:35.527665'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: agent-upgrade-mop.j2 - WUS2LEA
version: '1.0'
---

# Agent Upgrade Procedure - WUS2LEA

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **westus2euap** region (wus2lea).

### Environment Details

- **Region**: WUS2LEA (westus2euap)
- **ADO Organization**: { vault_wus2lea_ado_organization }
- **Project**: { vault_wus2lea_ado_project }
- **Environment**: wus2lea-production
- **Resource Group**: rg-prod-wus2lea
- **Key Vault**: kv-prod-wus2lea
- **Early Access Region**: Yes - Preview features enabled

## Prerequisites

1. Access to { vault_wus2lea_ado_organization } Azure DevOps organization
2. Permissions to wus2lea-production environment
3. Network connectivity to westus2euap region
4. Service principal access to rg-prod-wus2lea

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- All servers in wus2lea region

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible wus2lea_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible wus2lea_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible wus2lea_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "wus2lea"
  environment: "wus2lea-production"
  log_level: "INFO"
  endpoints:
    primary: "monitoring-wus2lea.example.com"
    backup: "monitoring-backup-wus2lea.example.com"
  retention_days: 30
```

### Step 3: Azure DevOps Pipeline Execution

The upgrade process will trigger the following pipeline:

- **Pipeline ID**: { vault_wus2lea_pipeline_id }
- **Organization**: { vault_wus2lea_ado_organization }
- **Project**: { vault_wus2lea_ado_project }
- **Environment**: wus2lea-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible wus2lea_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible wus2lea_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible wus2lea_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible wus2lea_monitoring -m shell -a "monitoring-agent --test-connection"
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
**Region**: WUS2LEA (westus2euap)