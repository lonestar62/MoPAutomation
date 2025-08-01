---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.735081'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# DNS Configuration - EUS2LEA

## Overview

DNS configuration procedure for **eastus2euap** region.

### DNS Context

- **Target Region**: EUS2LEA (eastus2euap)
- **DNS Provider**: Azure DNS
- **Zone**: example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-eus2lea \
  --zone-name example.com \
  --record-set-name www-eus2lea \
  --ipv4-address 10.0.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-eus2lea \
  --zone-name example.com \
  --record-set-name api-eus2lea \
  --ipv4-address 10.0.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-eus2lea \
  --zone-name example.com \
  --record-set-name eus2lea-service \
  --cname eus2lea.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)