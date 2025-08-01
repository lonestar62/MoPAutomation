---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.777661'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - WUS2LEA
version: '1.0'
---


# Container Deployment - WUS2LEA

## Overview

Container deployment procedure for **westus2euap** region.

### Container Context

- **Target Region**: WUS2LEA (westus2euap)
- **Container Registry**: acrwus2leaprod.azurecr.io
- **Image Version**: 1.3.0-preview

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus2lea_app -m shell -a "
  docker login acrwus2leaprod.azurecr.io \
  -u {{ vault_wus2lea_acr_username }} \
  -p {{ vault_wus2lea_acr_password }}
"

# Pull latest images
ansible wus2lea_app -m docker_image -a "
  name=acrwus2leaprod.azurecr.io/webapp:1.3.0-preview
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible wus2lea_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible wus2lea_app -m docker_container -a "
  name=webapp
  image=acrwus2leaprod.azurecr.io/webapp:1.3.0-preview
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_wus2lea_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_wus2lea_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible wus2lea_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)