---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:26:36.387743'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: dns-config.j2 - EUS2LEA
version: '1.0'
---


# DNS Configuration - EUS2LEA

## Overview

DNS configuration procedure for **eastus2euap** region.

### DNS Context

- **Target Region**: EUS2LEA (eastus2euap)
- **DNS Provider**: Azure DNS
- **Zone**: eus2lea.example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-eus2lea \
  --zone-name eus2lea.example.com \
  --record-set-name www-eus2lea \
  --ipv4-address 10.4.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-eus2lea \
  --zone-name eus2lea.example.com \
  --record-set-name api-eus2lea \
  --ipv4-address 10.4.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-eus2lea \
  --zone-name eus2lea.example.com \
  --record-set-name eus2lea-service \
  --cname eus2lea.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)