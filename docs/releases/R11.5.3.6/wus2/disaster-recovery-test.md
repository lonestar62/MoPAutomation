---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:27:11.917344'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: disaster-recovery-test.j2
title: disaster-recovery-test.j2 - WUS2
version: '1.0'
---


# Disaster Recovery Test - WUS2

## Overview

Disaster recovery test procedure for **westus2** region.

### DR Test Context

- **Target Region**: WUS2 (westus2)
- **DR Region**: eus2
- **Test Type**: Failover Test
- **RTO Target**: 4 hours
- **RPO Target**: 1 hour

## Pre-Test Preparation

### Backup Verification
```bash
# Verify latest backups exist
ansible wus2_db -m shell -a "
  find /backup -name 'db-*.sql.gz' -mtime -1
"

# Test backup restoration
ansible eus2_db -m shell -a "
  gunzip -c /backup/db-$(date +%Y%m%d).sql.gz | mysql test_restore_db
"
```

### DR Environment Check
```bash
# Verify DR infrastructure
ansible eus2_all -m ping

# Check DR service status
ansible eus2_web -m systemd -a "name=nginx state=started"
ansible eus2_db -m systemd -a "name=mysql state=started"
```

## Failover Test

### DNS Failover
```bash
# Update DNS to point to DR region
az network dns record-set a update \
  --resource-group rg-prod-wus2 \
  --zone-name wus2.example.com \
  --name www \
  --set aRecords[0].ipv4Address=10.0.1.10
```

### Application Failover
```bash
# Start services in DR region
ansible eus2_app -m systemd -a "name=application state=started"

# Configure load balancer for DR
ansible eus2_lb -m template -a "
  src=dr-nginx.conf.j2
  dest=/etc/nginx/sites-available/default
"
ansible eus2_lb -m systemd -a "name=nginx state=restarted"
```

### Data Synchronization
```bash
# Sync latest data to DR region
ansible wus2_db -m shell -a "
  mysqldump --all-databases | gzip > /tmp/failover-backup.sql.gz
"

ansible eus2_db -m shell -a "
  gunzip -c /tmp/failover-backup.sql.gz | mysql
"
```

## Test Validation

### Service Availability
```bash
# Test application accessibility
ansible eus2_web -m uri -a "
  url=http://localhost/health
  status_code=200
"

# Test database connectivity
ansible eus2_app -m shell -a "
  mysql -e 'SELECT 1' 2>/dev/null && echo 'DB OK' || echo 'DB FAIL'
"
```

### Performance Validation
```bash
# Run performance tests in DR region
ansible eus2_web -m shell -a "
  ab -n 100 -c 10 http://localhost/ | grep 'Requests per second'
"
```

## Failback Procedure

### DNS Restoration
```bash
# Restore DNS to primary region
az network dns record-set a update \
  --resource-group rg-prod-wus2 \
  --zone-name wus2.example.com \
  --name www \
  --set aRecords[0].ipv4Address=10.1.1.10
```

### Service Restoration
```bash
# Restore services in primary region
ansible wus2_all -m systemd -a "name=application state=started"
ansible wus2_web -m systemd -a "name=nginx state=started"
```

## Test Report

### DR Test Results
- **Test Duration**: TBD
- **RTO Achieved**: TBD
- **RPO Achieved**: TBD
- **Issues Found**: TBD
- **Recommendations**: TBD

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)