---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:10.300867'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: network-security-config.j2
title: network-security-config.j2 - EUS2
version: '1.0'
---


# Network Security Configuration - EUS2

## Overview

Network security configuration procedure for **eastus2** region.

### Security Context

- **Target Region**: EUS2 (eastus2)
- **Environment**: eus2-production
- **ADO Organization**: { vault_eus2_ado_organization }
- **Resource Group**: rg-prod-eus2

## Security Components

### Network Security Groups
- **Web NSG**: nsg-web-eus2
  - HTTP/HTTPS: Allow from Internet
  - SSH: Restricted to management subnet
- **Database NSG**: nsg-db-eus2
  - SQL: Allow from web tier only
  - Management: Restricted access
- **Management NSG**: nsg-mgmt-eus2
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
      source: "10.0.1.0/24"
      action: allow
  management:
    - port: 22
      protocol: TCP
      source: "10.0.200.0/24"
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
az network nsg list --resource-group rg-prod-eus2 --output table

# Test connectivity
ansible eus2_web -m shell -a "curl -I http://localhost"
ansible eus2_db -m shell -a "sqlcmd -S localhost -Q 'SELECT 1'"

# Validate firewall rules
az network nsg rule list --resource-group rg-prod-eus2 --nsg-name nsg-web-eus2
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
**Region**: EUS2 (eastus2)  
**Risk Level**: HIGH