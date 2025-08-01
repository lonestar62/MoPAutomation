---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.830524'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Container Deployment - WUS2

## Overview

Container deployment procedure for **westus2** region.

### Container Context

- **Target Region**: WUS2 (westus2)
- **Container Registry**: acrwus2.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus2_app -m shell -a "
  docker login acrwus2.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible wus2_app -m docker_image -a "
  name=acrwus2.azurecr.io/webapp:latest
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
  image=acrwus2.azurecr.io/webapp:latest
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