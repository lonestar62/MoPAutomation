---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.494896'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---

# Agent Upgrade Procedure - EUS2LEA

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **eastus2euap** region (eus2lea).

### Environment Details

- **Region**: EUS2LEA (eastus2euap)
- **ADO Organization**: { vault_eus2lea_ado_organization }
- **Project**: { vault_eus2lea_ado_project }
- **Environment**: eus2lea-production
- **Resource Group**: rg-prod-eus2lea
- **Key Vault**: kv-prod-eus2lea
- **Early Access Region**: Yes - Preview features enabled

## Prerequisites

1. Access to { vault_eus2lea_ado_organization } Azure DevOps organization
2. Permissions to eus2lea-production environment
3. Network connectivity to eastus2euap region
4. Service principal access to rg-prod-eus2lea

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- Monitoring servers in eus2lea_monitoring group

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible eus2lea_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible eus2lea_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible eus2lea_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "eus2lea"
  environment: "eus2lea-production"
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

- **Pipeline ID**: { vault_eus2lea_pipeline_id }
- **Organization**: { vault_eus2lea_ado_organization }
- **Project**: { vault_eus2lea_ado_project }
- **Environment**: eus2lea-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible eus2lea_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible eus2lea_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible eus2lea_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible eus2lea_monitoring -m shell -a "monitoring-agent --test-connection"
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
**Region**: EUS2LEA (eastus2euap)