---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:11:51.865838'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: network-security-config.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Network Security Configuration - WUS2

## Overview

Network security configuration procedure for **westus2** region.

### Security Context

- **Target Region**: WUS2 (westus2)
- **Environment**: wus2-production
- **ADO Organization**: { vault_wus2_ado_organization }
- **Resource Group**: rg-prod-wus2

## Security Components

### Network Security Groups
- **Web NSG**: nsg-web-wus2
  - HTTP/HTTPS: Allow from Internet
  - SSH: Restricted to management subnet
- **Database NSG**: nsg-db-wus2
  - SQL: Allow from web tier only
  - Management: Restricted access
- **Management NSG**: nsg-mgmt-wus2
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
az network nsg list --resource-group rg-prod-wus2 --output table

# Test connectivity
ansible wus2_web -m shell -a "curl -I http://localhost"
ansible wus2_db -m shell -a "sqlcmd -S localhost -Q 'SELECT 1'"

# Validate firewall rules
az network nsg rule list --resource-group rg-prod-wus2 --nsg-name nsg-web-wus2
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
**Region**: WUS2 (westus2)  
**Risk Level**: HIGH