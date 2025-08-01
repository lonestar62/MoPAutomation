---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:26:36.732830'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - WUS2
version: '1.0'
---


# Container Deployment - WUS2

## Overview

Container deployment procedure for **westus2** region.

### Container Context

- **Target Region**: WUS2 (westus2)
- **Container Registry**: acrwus2prod.azurecr.io
- **Image Version**: 1.2.0

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus2_app -m shell -a "
  docker login acrwus2prod.azurecr.io \
  -u {{ vault_wus2_acr_username }} \
  -p {{ vault_wus2_acr_password }}
"

# Pull latest images
ansible wus2_app -m docker_image -a "
  name=acrwus2prod.azurecr.io/webapp:1.2.0
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible wus2_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible wus2_app -m docker_container -a "
  name=webapp
  image=acrwus2prod.azurecr.io/webapp:1.2.0
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_wus2_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_wus2_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible wus2_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)