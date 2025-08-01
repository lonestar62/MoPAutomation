---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:27:10.506048'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: patch-linux-systems.j2
title: patch-linux-systems.j2 - WUS2LEA
version: '1.0'
---


# Linux System Patching - WUS2LEA

## Overview

Security and system patching procedure for Linux servers in **westus2euap** region.

### Patching Context

- **Target Region**: WUS2LEA (westus2euap)
- **Environment**: wus2lea-production
- **Patch Category**: Security + Critical
- **Maintenance Window**: 02:00-06:00 UTC
- **ADO Organization**: { vault_wus2lea_ado_organization }

## Pre-Patching Assessment

### System Inventory
```bash
# Get list of systems requiring patches
ansible wus2lea_all -m shell -a "cat /etc/os-release | grep PRETTY_NAME"

# Check current kernel version
ansible wus2lea_all -m shell -a "uname -r"

# List available updates
ansible wus2lea_all -m shell -a "yum check-update --security" -b
```

### Backup Verification
```bash
# Verify recent backups exist
ansible wus2lea_all -m shell -a "ls -la /backup/ | head -10"

# Test system state backup
ansible wus2lea_all -m shell -a "tar -czf /tmp/system-state-$(date +%Y%m%d).tar.gz /etc /var/log"
```

## Patching Strategy

### Patch Categories
**Security + Critical Patches**
- All security vulnerabilities
- Critical system updates
- Stability improvements

### Server Groups
1. **Web Servers** (`wus2lea_web`)
   - Load balancer removal before patching
   - Rolling restart capability
   - Application health checks

2. **Database Servers** (`wus2lea_db`)
   - Database cluster awareness
   - Replication health monitoring
   - Extended maintenance window

3. **Application Servers** (`wus2lea_app`)
   - Service dependency mapping
   - Graceful service shutdown
   - Health check validation

## Execution Procedure

### Step 1: Pre-Patch Validation
```bash
# Check system health
ansible wus2lea_all -m shell -a "df -h | grep -E '(8[5-9]|9[0-9])%'" -b
ansible wus2lea_all -m shell -a "free -m | grep Mem"
ansible wus2lea_all -m shell -a "uptime"

# Verify services are running
ansible wus2lea_web -m systemd -a "name=nginx state=started" -b
ansible wus2lea_app -m systemd -a "name=application state=started" -b
ansible wus2lea_db -m systemd -a "name=mysql state=started" -b
```

### Step 2: Remove from Load Balancer
```bash
# Remove web servers from load balancer
ansible wus2lea_lb -m shell -a "nginx -s reload" -b
ansible wus2lea_lb -m shell -a "nginx -s reload" -b

# Verify traffic redirection
ansible wus2lea_lb -m shell -a "curl -I http://localhost/health"
```

### Step 3: Apply Patches
```bash
# Security patches
ansible wus2lea_all -m yum -a "name='*' state=latest security=yes" -b

# System patches (if included)
ansible wus2lea_all -m yum -a "name=kernel state=latest" -b
ansible wus2lea_all -m yum -a "name=glibc state=latest" -b
ansible wus2lea_all -m yum -a "name=openssl state=latest" -b

# Update package database
ansible wus2lea_all -m shell -a "yum clean all && yum makecache" -b
```

### Step 4: Reboot Coordination
```bash
# Check if reboot is required
ansible wus2lea_all -m shell -a "[ -f /var/run/reboot-required ] && echo 'REBOOT REQUIRED' || echo 'NO REBOOT NEEDED'"

# Coordinated reboot by group
# Reboot db servers
ansible wus2lea_db -m reboot -a "reboot_timeout=600" -b

# Wait for services to start
sleep 60
ansible wus2lea_db -m wait_for -a "port=22 timeout=300"
# Reboot app servers
ansible wus2lea_app -m reboot -a "reboot_timeout=600" -b

# Wait for services to start
sleep 60
ansible wus2lea_app -m wait_for -a "port=22 timeout=300"
# Reboot web servers
ansible wus2lea_web -m reboot -a "reboot_timeout=600" -b

# Wait for services to start
sleep 60
ansible wus2lea_web -m wait_for -a "port=22 timeout=300"
```

### Step 5: Post-Patch Validation
```bash
# Verify system status
ansible wus2lea_all -m shell -a "uptime"
ansible wus2lea_all -m shell -a "systemctl is-system-running"

# Check kernel version
ansible wus2lea_all -m shell -a "uname -r"

# Verify critical services
ansible wus2lea_web -m uri -a "url=http://localhost/health"
ansible wus2lea_app -m shell -a "systemctl is-active application"
ansible wus2lea_db -m shell -a "systemctl is-active mysql"
```

### Step 6: Return to Load Balancer
```bash
# Add servers back to load balancer
ansible wus2lea_lb -m shell -a "nginx -s reload" -b

# Verify full traffic restoration
ansible wus2lea_lb -m uri -a "url=http://localhost/health"
```

## Validation Checklist

### System Health
- [ ] All systems responsive
- [ ] Kernel versions updated
- [ ] Critical services running
- [ ] No failed systemd units
- [ ] Log files normal

### Application Health
- [ ] Web applications accessible
- [ ] Database connections functional
- [ ] API endpoints responding
- [ ] Performance within baselines
- [ ] No error rate increase

### Security Validation
```bash
# Verify security updates applied
ansible wus2lea_all -m shell -a "yum history list | head -5"

# Check for remaining vulnerabilities
ansible wus2lea_all -m shell -a "yum --security check-update"

# Validate system hardening
ansible wus2lea_all -m shell -a "auditctl -l | wc -l"
```

## Rollback Procedures

### Emergency Rollback
```bash
# Revert to previous kernel (if needed)
ansible wus2lea_all -m shell -a "grub2-set-default 1" -b
ansible wus2lea_all -m reboot -b

# Restore from backup (critical failure only)
ansible wus2lea_all -m shell -a "tar -xzf /backup/system-state-*.tar.gz -C /"
```

### Package Downgrade
```bash
# List recent package changes
ansible wus2lea_all -m shell -a "yum history list | head -10"

# Downgrade specific packages if needed
ansible wus2lea_all -m shell -a "yum downgrade package-name" -b
```

## Region-Specific Considerations

### Early Access Region
- Test patch compatibility first
- Enhanced monitoring during maintenance
- Report issues to product teams

## Monitoring and Alerts

### During Maintenance
- System resource monitoring
- Application performance tracking
- Security event monitoring
- Replication lag monitoring (if applicable)

### Post-Maintenance
- Performance baseline comparison
- Security posture assessment
- System stability monitoring
- User experience metrics

## Emergency Contacts

- **System Administrators**: sysadmin-wus2lea@example.com
- **Security Team**: security-wus2lea@example.com
- **Application Team**: appteam-wus2lea@example.com
- **On-Call Engineer**: oncall-wus2lea@example.com

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)  
**Patch Category**: Security + Critical