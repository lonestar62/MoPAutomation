---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.542634'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: network-security-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# Network Security Configuration - WUS3

## Overview

Network security configuration procedure for **westus3** region.

### Security Context

- **Target Region**: WUS3 (westus3)
- **Environment**: wus3-production
- **ADO Organization**: { vault_wus3_ado_organization }
- **Resource Group**: rg-prod-wus3

## Security Components

### Network Security Groups
- **Web NSG**: nsg-web-wus3
  - HTTP/HTTPS: Allow from Internet
  - SSH: Restricted to management subnet
- **Database NSG**: nsg-db-wus3
  - SQL: Allow from web tier only
  - Management: Restricted access
- **Management NSG**: nsg-mgmt-wus3
  - RDP/SSH: VPN access only
  - Monitoring: Internal access

### Firewall Rules
```yaml
firewall_rules:
  web_tier:
    - port: 80
      protocol: TCP
      source: "0.0.0.0/0"
      action: allow
    - port: 443
      protocol: TCP
      source: "0.0.0.0/0"
      action: allow
  database_tier:
    - port: 1433
      protocol: TCP
      source: ""
      action: allow
  management:
    - port: 22
      protocol: TCP
      source: "10.0.100.0/24"
      action: allow
```

## Security Validation

### Pre-Configuration Checks
- [ ] Current security groups documented
- [ ] Firewall rules backed up
- [ ] Network topology verified
- [ ] Change approval obtained

### Post-Configuration Verification
```bash
# Verify NSG associations
az network nsg list --resource-group rg-prod-wus3 --output table

# Test connectivity
ansible wus3_web -m shell -a "curl -I http://localhost"
ansible wus3_db -m shell -a "sqlcmd -S localhost -Q 'SELECT 1'"

# Validate firewall rules
az network nsg rule list --resource-group rg-prod-wus3 --nsg-name nsg-web-wus3
```

## Security Compliance

### Required Validations
- Network segmentation verified
- Access controls properly configured
- Logging and monitoring enabled
- Compliance scan passed

### Risk Mitigation
- Backup connectivity maintained
- Rollback procedures verified
- Emergency access preserved
- Security team notified

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)  
**Risk Level**: HIGH