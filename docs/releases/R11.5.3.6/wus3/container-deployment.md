---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:27:11.576026'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - WUS3
version: '1.0'
---


# Container Deployment - WUS3

## Overview

Container deployment procedure for **westus3** region.

### Container Context

- **Target Region**: WUS3 (westus3)
- **Container Registry**: acrwus3prod.azurecr.io
- **Image Version**: 1.2.0

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus3_app -m shell -a "
  docker login acrwus3prod.azurecr.io \
  -u {{ vault_wus3_acr_username }} \
  -p {{ vault_wus3_acr_password }}
"

# Pull latest images
ansible wus3_app -m docker_image -a "
  name=acrwus3prod.azurecr.io/webapp:1.2.0
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible wus3_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible wus3_app -m docker_container -a "
  name=webapp
  image=acrwus3prod.azurecr.io/webapp:1.2.0
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_wus3_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_wus3_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible wus3_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)