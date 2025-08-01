---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.521249'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: infrastructure-deployment.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---

# Infrastructure Deployment - WUS2

## Deployment Overview

Infrastructure deployment procedure for **westus2** region using Azure DevOps pipelines.

### Deployment Context

- **Target Region**: WUS2 (westus2)
- **Environment**: wus2-production
- **Deployment Type**: rolling
- **ADO Organization**: { vault_wus2_ado_organization }
- **Resource Group**: rg-prod-wus2

## Infrastructure Components

### Core Infrastructure
- Virtual Networks and Subnets
- Load Balancers and Application Gateways  
- Storage Accounts and Databases
- Monitoring and Logging Infrastructure

### Network Configuration
- **VNet**: vnet-prod-wus2
- **Address Space**: 10.0.0.0/16
- **Subnets**:
  - Web Tier: 10.0.1.0/24
  - DB Tier: 10.0.2.0/24
  - Monitoring: 10.0.3.0/24

## Pre-Deployment Checklist

### Azure Resources
- [ ] Subscription access validated for westus2
- [ ] Resource group rg-prod-wus2 exists
- [ ] Network Security Groups configured
- [ ] Key Vault kv-prod-wus2 accessible
- [ ] Service Principal permissions verified

### Azure DevOps Pipeline
- [ ] Pipeline { vault_wus2_pipeline_id } exists in { vault_wus2_ado_organization }
- [ ] Environment wus2-production configured
- [ ] Variable groups populated
- [ ] Service connections validated
- [ ] Agent pools available

## Deployment Steps

### Step 1: Environment Preparation

```bash
# Validate Azure connectivity
az account show --subscription { vault_wus2_subscription_id }

# Verify resource group
az group show --name rg-prod-wus2 --subscription { vault_wus2_subscription_id }

# Check key vault access
az keyvault secret list --vault-name kv-prod-wus2
```

### Step 2: Pipeline Configuration

The deployment pipeline will be configured with:

```yaml
# Pipeline variables
variables:
  region: wus2
  resourceGroup: rg-prod-wus2
  subscriptionId: { vault_wus2_subscription_id }
  environment: wus2-production
  deploymentType: rolling
  notification_webhook: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
  approval_required: True
  rollback_enabled: True
```

### Step 3: Infrastructure Deployment

Pipeline stages:
1. **Validation**: ARM template validation and what-if analysis
2. **Security**: Security scanning and compliance checks
3. **Deployment**: Resource deployment with rollback capability
4. **Verification**: Post-deployment testing and validation

### Step 4: Post-Deployment Validation

```bash
# Verify core resources
az resource list --resource-group rg-prod-wus2 --output table

# Test network connectivity
az network vnet show --name vnet-prod-wus2 --resource-group rg-prod-wus2

# Validate monitoring setup
az monitor activity-log list --resource-group rg-prod-wus2 --max-events 5
```

## Monitoring and Alerting

### Health Checks
- Application Gateway health probe
- Database connectivity check  
- Storage account accessibility
- Key Vault operations test

### Alert Configuration
- Infrastructure health alerts
- Performance threshold monitoring
- Security and compliance notifications
- Cost management alerts

## Region-Specific Considerations

### West US 2 (Primary West)
- Disaster recovery target for eus2
- High-availability configuration
- Cross-region replication setup

## Rollback Procedures

### Automatic Rollback Triggers
- Deployment failure with exit code > 0
- Health check failures post-deployment
- Security scan failures
- Performance degradation alerts

### Manual Rollback Steps
1. **Stop Pipeline**: Cancel current deployment
2. **Assess Impact**: Determine affected resources
3. **Execute Rollback**: Deploy previous known-good state
4. **Validate Recovery**: Confirm system functionality

## Success Criteria

Deployment is successful when:
- [ ] All ARM templates deploy without errors
- [ ] Health checks pass for all components
- [ ] Network connectivity verified between tiers
- [ ] Monitoring and alerting operational
- [ ] Security scans pass with no critical issues
- [ ] Performance baselines established

## Emergency Contacts

### Escalation Path
- **Level 1**: Operations Team
- **Level 2**: Infrastructure Team  
- **Level 3**: Architecture Team

### Region Team
- **Regional Lead**: TBD
- **DevOps Engineer**: TBD
- **Site Reliability**: TBD

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)  
**Deployment Type**: rolling