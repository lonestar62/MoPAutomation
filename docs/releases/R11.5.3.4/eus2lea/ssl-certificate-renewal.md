---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.642612'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: ssl-certificate-renewal.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# SSL Certificate Renewal - EUS2LEA

## Overview

SSL certificate renewal procedure for **eastus2euap** region.

### Certificate Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Environment**: eus2lea-production
- **Certificate Authority**: Let's Encrypt / Azure Key Vault
- **Domains**: *.example.com, api.example.com

## Certificate Management

### Certificate Renewal
```bash
# Renew certificates using certbot
ansible eus2lea_web -m shell -a "certbot renew --dry-run"
ansible eus2lea_web -m shell -a "certbot renew --force-renewal"

# Deploy certificates to load balancers
ansible eus2lea_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/fullchain.pem
  dest=/etc/nginx/ssl/
"
ansible eus2lea_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/privkey.pem
  dest=/etc/nginx/ssl/
"
```

### Service Restart
```bash
# Restart web services to pick up new certificates
ansible eus2lea_web -m systemd -a "name=nginx state=restarted"
ansible eus2lea_lb -m systemd -a "name=haproxy state=restarted"
```

### Certificate Validation
```bash
# Verify certificate validity
ansible eus2lea_web -m uri -a "
  url=https://
  validate_certs=yes
  return_content=no
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)