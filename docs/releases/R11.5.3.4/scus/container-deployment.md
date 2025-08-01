---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.833129'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Container Deployment - SCUS

## Overview

Container deployment procedure for **southcentralus** region.

### Container Context

- **Target Region**: SCUS (southcentralus)
- **Container Registry**: acrscus.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible scus_app -m shell -a "
  docker login acrscus.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible scus_app -m docker_image -a "
  name=acrscus.azurecr.io/webapp:latest
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible scus_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible scus_app -m docker_container -a "
  name=webapp
  image=acrscus.azurecr.io/webapp:latest
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
ansible scus_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)