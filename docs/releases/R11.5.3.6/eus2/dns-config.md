---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:11.132205'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: dns-config.j2 - EUS2
version: '1.0'
---


# DNS Configuration - EUS2

## Overview

DNS configuration procedure for **eastus2** region.

### DNS Context

- **Target Region**: EUS2 (eastus2)
- **DNS Provider**: Azure DNS
- **Zone**: eus2.example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-eus2 \
  --zone-name eus2.example.com \
  --record-set-name www-eus2 \
  --ipv4-address 10.0.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-eus2 \
  --zone-name eus2.example.com \
  --record-set-name api-eus2 \
  --ipv4-address 10.0.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-eus2 \
  --zone-name eus2.example.com \
  --record-set-name eus2-service \
  --cname eus2.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)