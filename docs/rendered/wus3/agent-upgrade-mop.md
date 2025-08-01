---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: infrastructure
description: Deploy core infrastructure components across Azure regions
environment: wus3-production
generated_at: '2025-08-01T07:59:23.883013'
region: wus3
tags:
- wus3
- infrastructure
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: Azure Infrastructure Deployment - WUS3
version: 2.0.0
---

# Agent Upgrade Procedure - WUS3

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **westus3** region (wus3).

### Environment Details

- **Region**: WUS3 (westus3)
- **ADO Organization**: { vault_wus3_ado_organization }
- **Project**: { vault_wus3_ado_project }
- **Environment**: wus3-production
- **Resource Group**: rg-prod-wus3
- **Key Vault**: kv-prod-wus3

## Prerequisites

1. Access to { vault_wus3_ado_organization } Azure DevOps organization
2. Permissions to wus3-production environment
3. Network connectivity to westus3 region
4. Service principal access to rg-prod-wus3

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- All servers in wus3 region

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible wus3_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible wus3_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible wus3_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "wus3"
  environment: "wus3-production"
  log_level: "INFO"
  endpoints:
    primary: "monitoring-wus3.example.com"
    backup: "monitoring-backup-wus3.example.com"
  retention_days: 30
```

### Step 3: Azure DevOps Pipeline Execution

The upgrade process will trigger the following pipeline:

- **Pipeline ID**: { vault_wus3_pipeline_id }
- **Organization**: { vault_wus3_ado_organization }
- **Project**: { vault_wus3_ado_project }
- **Environment**: wus3-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible wus3_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible wus3_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible wus3_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible wus3_monitoring -m shell -a "monitoring-agent --test-connection"
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
**Region**: WUS3 (westus3)