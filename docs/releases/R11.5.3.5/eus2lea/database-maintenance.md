---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:26:35.735029'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: database-maintenance.j2
title: database-maintenance.j2 - EUS2LEA
version: '1.0'
---


# Database Maintenance - EUS2LEA

## Overview

Database maintenance procedure for **eastus2euap** region.

### Database Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Environment**: eus2lea-production
- **Database Server**: sqldb-prod-eus2lea.database.windows.net
- **Resource Group**: rg-prod-eus2lea

## Maintenance Tasks

### Index Optimization
```sql
-- Rebuild fragmented indexes
USE [ProductionDB]
GO

-- Check index fragmentation
SELECT 
    OBJECT_NAME(OBJECT_ID) AS TableName,
    s.name AS IndexName,
    avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, NULL) AS s
INNER JOIN sys.indexes AS i ON s.object_id = i.object_id
WHERE s.avg_fragmentation_in_percent > 10
ORDER BY avg_fragmentation_in_percent DESC;

-- Rebuild high fragmentation indexes
ALTER INDEX ALL ON [Users] REBUILD;
ALTER INDEX ALL ON [Orders] REBUILD;
ALTER INDEX ALL ON [Products] REBUILD;
ALTER INDEX ALL ON [Transactions] REBUILD;
ALTER INDEX ALL ON [AuditLog] REBUILD;
ALTER INDEX ALL ON [Sessions] REBUILD;
ALTER INDEX ALL ON [PreviewFeatures] REBUILD;
ALTER INDEX ALL ON [EarlyAccessLogs] REBUILD;
```

### Statistics Update
```sql
-- Update database statistics
UPDATE STATISTICS ProductionDB;

-- Update specific table statistics
UPDATE STATISTICS [Users] WITH FULLSCAN;
UPDATE STATISTICS [Orders] WITH FULLSCAN;
UPDATE STATISTICS [Products] WITH FULLSCAN;
UPDATE STATISTICS [Transactions] WITH FULLSCAN;
UPDATE STATISTICS [AuditLog] WITH FULLSCAN;
UPDATE STATISTICS [Sessions] WITH FULLSCAN;
UPDATE STATISTICS [PreviewFeatures] WITH FULLSCAN;
UPDATE STATISTICS [EarlyAccessLogs] WITH FULLSCAN;
```

### Cleanup Operations
```sql
-- Cleanup old data (retention: 180 days)

-- Shrink log file if necessary
```

## Pre-Maintenance Checklist

### Backup Verification
- [ ] Recent backup verified (< 24 hours)
- [ ] Backup restoration tested
- [ ] Transaction log backup current
- [ ] Point-in-time recovery available

### Performance Baseline
```bash
# Capture performance metrics
ansible eus2lea_db -m shell -a "sqlcmd -S sqldb-prod-eus2lea.database.windows.net -Q \"
SELECT 
    cntr_value as [Buffer Cache Hit Ratio]
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Buffer cache hit ratio'
\""

# Check active connections
ansible eus2lea_db -m shell -a "sqlcmd -Q \"
SELECT 
    DB_NAME(dbid) as DatabaseName,
    COUNT(dbid) as NumberOfConnections
FROM sys.sysprocesses 
WHERE dbid > 0 
GROUP BY dbid, DB_NAME(dbid)
\""
```

## Execution Steps

### Step 1: Preparation
```bash
# Set database to restricted mode during maintenance
ansible eus2lea_db -m shell -a "sqlcmd -Q \"
ALTER DATABASE [ProductionDB] 
SET RESTRICTED_USER WITH ROLLBACK IMMEDIATE
\""
```

### Step 2: Maintenance Tasks
- Index rebuilding (estimated 30 minutes)
- Statistics update (estimated 15 minutes)
- Cleanup operations (estimated 10 minutes)

### Step 3: Validation
```bash
# Verify database integrity
ansible eus2lea_db -m shell -a "sqlcmd -Q \"DBCC CHECKDB('ProductionDB') WITH NO_INFOMSGS\""

# Check performance improvements
ansible eus2lea_db -m shell -a "sqlcmd -Q \"
SELECT 
    OBJECT_NAME(object_id) AS TableName,
    avg_fragmentation_in_percent 
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, NULL)
WHERE avg_fragmentation_in_percent > 5
\""
```

### Step 4: Restore Access
```bash
# Return database to normal access
ansible eus2lea_db -m shell -a "sqlcmd -Q \"
ALTER DATABASE [ProductionDB] 
SET MULTI_USER
\""
```

## Post-Maintenance Validation

### Performance Verification
- [ ] Query response times improved
- [ ] Index fragmentation reduced
- [ ] Statistics updated successfully
- [ ] Database integrity verified

### Application Testing
- [ ] Application connectivity verified
- [ ] Critical functions tested
- [ ] Performance monitoring resumed
- [ ] Error logs reviewed

## Region-Specific Notes

### Early Access Region
- Test new maintenance procedures first
- Enhanced monitoring during maintenance
- Shorter maintenance window for validation

## Emergency Procedures

### Rollback Plan
1. Restore from pre-maintenance backup
2. Verify data consistency
3. Resume application services
4. Notify incident response team

### Emergency Contacts
- **DBA Team**: dba-eus2lea@example.com
- **DevOps**: devops-eus2lea@example.com
- **Application Team**: appteam-eus2lea@example.com

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)  
**Database**: ProductionDB