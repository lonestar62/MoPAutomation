---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.487542'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---

# Agent Upgrade Procedure - WUS2

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **westus2** region (wus2).

### Environment Details

- **Region**: WUS2 (westus2)
- **ADO Organization**: { vault_wus2_ado_organization }
- **Project**: { vault_wus2_ado_project }
- **Environment**: wus2-production
- **Resource Group**: rg-prod-wus2
- **Key Vault**: kv-prod-wus2

## Prerequisites

1. Access to { vault_wus2_ado_organization } Azure DevOps organization
2. Permissions to wus2-production environment
3. Network connectivity to westus2 region
4. Service principal access to rg-prod-wus2

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- Monitoring servers in wus2_monitoring group

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible wus2_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible wus2_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible wus2_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "wus2"
  environment: "wus2-production"
  log_level: "INFO"
  endpoints:
    primary: "monitoring-{region}.example.com"
    backup: "monitoring-backup-{region}.example.com"
  retention_days: 30
  custom_settings:
    enable_debug: False
    max_connections: 100
    timeout_seconds: 30
    buffer_size: 64MB
```

### Step 3: Azure DevOps Pipeline Execution

The upgrade process will trigger the following pipeline:

- **Pipeline ID**: { vault_wus2_pipeline_id }
- **Organization**: { vault_wus2_ado_organization }
- **Project**: { vault_wus2_ado_project }
- **Environment**: wus2-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible wus2_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible wus2_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible wus2_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible wus2_monitoring -m shell -a "monitoring-agent --test-connection"
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
**Region**: WUS2 (westus2)