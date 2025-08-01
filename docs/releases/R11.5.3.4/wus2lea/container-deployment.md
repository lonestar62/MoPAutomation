---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:18:32.835991'
preview_features: true
region: wus2lea
tags:
- wus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - WUS2LEA
version: 1.2.0
---


# Container Deployment - WUS2LEA

## Overview

Container deployment procedure for **westus2euap** region.

### Container Context

- **Target Region**: WUS2LEA (westus2euap)
- **Container Registry**: acrwus2lea.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus2lea_app -m shell -a "
  docker login acrwus2lea.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible wus2lea_app -m docker_image -a "
  name=acrwus2lea.azurecr.io/webapp:latest
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
  image=acrwus2lea.azurecr.io/webapp:latest
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=
    API_KEY=
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