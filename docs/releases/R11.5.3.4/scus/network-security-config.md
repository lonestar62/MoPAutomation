---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.544479'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: network-security-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Network Security Configuration - SCUS

## Overview

Network security configuration procedure for **southcentralus** region.

### Security Context

- **Target Region**: SCUS (southcentralus)
- **Environment**: scus-production
- **ADO Organization**: { vault_scus_ado_organization }
- **Resource Group**: rg-prod-scus

## Security Components

### Network Security Groups
- **Web NSG**: nsg-web-scus
  - HTTP/HTTPS: Allow from Internet
  - SSH: Restricted to management subnet
- **Database NSG**: nsg-db-scus
  - SQL: Allow from web tier only
  - Management: Restricted access
- **Management NSG**: nsg-mgmt-scus
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
az network nsg list --resource-group rg-prod-scus --output table

# Test connectivity
ansible scus_web -m shell -a "curl -I http://localhost"
ansible scus_db -m shell -a "sqlcmd -S localhost -Q 'SELECT 1'"

# Validate firewall rules
az network nsg rule list --resource-group rg-prod-scus --nsg-name nsg-web-scus
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
**Region**: SCUS (southcentralus)  
**Risk Level**: HIGH