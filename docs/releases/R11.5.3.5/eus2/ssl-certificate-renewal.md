---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:35.976809'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: ssl-certificate-renewal.j2
title: ssl-certificate-renewal.j2 - EUS2
version: '1.0'
---


# SSL Certificate Renewal - EUS2

## Overview

SSL certificate renewal procedure for **eastus2** region.

### Certificate Context

- **Target Region**: EUS2 (eastus2)
- **Environment**: eus2-production
- **Certificate Authority**: Let's Encrypt / Azure Key Vault
- **Domains**: *.eus2.example.com, api-eus2.example.com, app-eus2.example.com

## Certificate Management

### Certificate Renewal
```bash
# Renew certificates using certbot
ansible eus2_web -m shell -a "certbot renew --dry-run"
ansible eus2_web -m shell -a "certbot renew --force-renewal"

# Deploy certificates to load balancers
ansible eus2_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/fullchain.pem
  dest=/etc/nginx/ssl/
"
ansible eus2_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/privkey.pem
  dest=/etc/nginx/ssl/
"
```

### Service Restart
```bash
# Restart web services to pick up new certificates
ansible eus2_web -m systemd -a "name=nginx state=restarted"
ansible eus2_lb -m systemd -a "name=haproxy state=restarted"
```

### Certificate Validation
```bash
# Verify certificate validity
ansible eus2_web -m uri -a "
  url=https://
  validate_certs=yes
  return_content=no
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)