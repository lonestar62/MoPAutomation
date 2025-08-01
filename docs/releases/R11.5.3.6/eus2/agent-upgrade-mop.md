---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:10.154894'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: agent-upgrade-mop.j2
title: agent-upgrade-mop.j2 - EUS2
version: '1.0'
---

# Agent Upgrade Procedure - EUS2

## Overview

This procedure outlines the steps to upgrade monitoring agents in the **eastus2** region (eus2).

### Environment Details

- **Region**: EUS2 (eastus2)
- **ADO Organization**: { vault_eus2_ado_organization }
- **Project**: { vault_eus2_ado_project }
- **Environment**: eus2-production
- **Resource Group**: rg-prod-eus2
- **Key Vault**: kv-prod-eus2

## Prerequisites

1. Access to { vault_eus2_ado_organization } Azure DevOps organization
2. Permissions to eus2-production environment
3. Network connectivity to eastus2 region
4. Service principal access to rg-prod-eus2

## Agent Configuration

### Current Version
- **Version**: v2.1.5
- **Configuration Path**: /opt/monitoring/config
- **Log Level**: INFO

### Target Hosts
- All servers in eus2 region

## Procedure Steps

### Step 1: Pre-Upgrade Validation

```bash
# Verify current agent status
ansible eus2_monitoring -m shell -a "systemctl status monitoring-agent"

# Check agent version
ansible eus2_monitoring -m shell -a "monitoring-agent --version"

# Verify connectivity to monitoring endpoints
ansible eus2_monitoring -m shell -a "curl -f https://monitoring.example.com/health"
```

### Step 2: Configuration Update

The Ansible playbook will update the agent configuration with the following settings:

```yaml
# Configuration to be applied
agent_config:
  version: "v2.1.6"
  region: "eus2"
  environment: "eus2-production"
  log_level: "INFO"
  endpoints:
    primary: "monitoring-eus2.example.com"
    backup: "monitoring-backup-eus2.example.com"
  retention_days: 30
```

### Step 3: Azure DevOps Pipeline Execution

The upgrade process will trigger the following pipeline:

- **Pipeline ID**: { vault_eus2_pipeline_id }
- **Organization**: { vault_eus2_ado_organization }
- **Project**: { vault_eus2_ado_project }
- **Environment**: eus2-production

### Step 4: Post-Upgrade Verification

```bash
# Verify new agent version
ansible eus2_monitoring -m shell -a "monitoring-agent --version"

# Check service status
ansible eus2_monitoring -m shell -a "systemctl is-active monitoring-agent"

# Validate configuration
ansible eus2_monitoring -m shell -a "monitoring-agent --validate-config"

# Test connectivity
ansible eus2_monitoring -m shell -a "monitoring-agent --test-connection"
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
**Region**: EUS2 (eastus2)