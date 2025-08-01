---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:10.409105'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: database-maintenance.j2
title: database-maintenance.j2 - SCUS
version: '1.0'
---


# Database Maintenance - SCUS

## Overview

Database maintenance procedure for **southcentralus** region.

### Database Context

- **Target Region**: SCUS (southcentralus)
- **Environment**: scus-production
- **Database Server**: sqldb-prod-scus.database.windows.net
- **Resource Group**: rg-prod-scus

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
ALTER INDEX ALL ON [CrossRegionSync] REBUILD;
ALTER INDEX ALL ON [HubCoordination] REBUILD;
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
UPDATE STATISTICS [CrossRegionSync] WITH FULLSCAN;
UPDATE STATISTICS [HubCoordination] WITH FULLSCAN;
```

### Cleanup Operations
```sql
-- Cleanup old data (retention: 365 days)
DELETE FROM AuditLog 
WHERE LogDate < DATEADD(day, -365, GETDATE());

DELETE FROM SessionData 
WHERE LastAccess < DATEADD(day, -30, GETDATE());

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
ansible scus_db -m shell -a "sqlcmd -S sqldb-prod-scus.database.windows.net -Q \"
SELECT 
    cntr_value as [Buffer Cache Hit Ratio]
FROM sys.dm_os_performance_counters 
WHERE counter_name = 'Buffer cache hit ratio'
\""

# Check active connections
ansible scus_db -m shell -a "sqlcmd -Q \"
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
ansible scus_db -m shell -a "sqlcmd -Q \"
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
ansible scus_db -m shell -a "sqlcmd -Q \"DBCC CHECKDB('ProductionDB') WITH NO_INFOMSGS\""

# Check performance improvements
ansible scus_db -m shell -a "sqlcmd -Q \"
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
ansible scus_db -m shell -a "sqlcmd -Q \"
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


## Emergency Procedures

### Rollback Plan
1. Restore from pre-maintenance backup
2. Verify data consistency
3. Resume application services
4. Notify incident response team

### Emergency Contacts
- **DBA Team**: dba-scus@example.com
- **DevOps**: devops-scus@example.com
- **Application Team**: appteam-scus@example.com

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)  
**Database**: ProductionDB