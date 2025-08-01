---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:11:51.869526'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: network-security-config.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# Network Security Configuration - EUS2LEA

## Overview

Network security configuration procedure for **eastus2euap** region.

### Security Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Environment**: eus2lea-production
- **ADO Organization**: { vault_eus2lea_ado_organization }
- **Resource Group**: rg-prod-eus2lea
- **Early Access Features**: Enhanced security policies enabled

## Security Components

### Network Security Groups
- **Web NSG**: nsg-web-eus2lea
  - HTTP/HTTPS: Allow from Internet
  - SSH: Restricted to management subnet
- **Database NSG**: nsg-db-eus2lea
  - SQL: Allow from web tier only
  - Management: Restricted access
- **Management NSG**: nsg-mgmt-eus2lea
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
az network nsg list --resource-group rg-prod-eus2lea --output table

# Test connectivity
ansible eus2lea_web -m shell -a "curl -I http://localhost"
ansible eus2lea_db -m shell -a "sqlcmd -S localhost -Q 'SELECT 1'"

# Validate firewall rules
az network nsg rule list --resource-group rg-prod-eus2lea --nsg-name nsg-web-eus2lea
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
**Region**: EUS2LEA (eastus2euap)  
**Risk Level**: HIGH