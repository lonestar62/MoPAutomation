# Ansible Logging Integration

## Overview

Our MOP Automation Platform integrates comprehensively with Ansible's logging capabilities to capture all execution data, performance metrics, and operational insights.

## Ansible Log Types

### 1. Standard Output (STDOUT)
- **Content**: Play-by-play execution output
- **Format**: Human-readable text
- **Location**: Captured in execution logs
- **Use**: Real-time monitoring, debugging

Example:
```
PLAY [Edit YAML Configuration] ************************************************

TASK [Backup existing configuration] *****************************************
changed: [localhost]

TASK [Update YAML values] *****************************************************
changed: [localhost]

PLAY RECAP ********************************************************************
localhost : ok=3    changed=2    unreachable=0    failed=0
```

### 2. Standard Error (STDERR)
- **Content**: Warning messages and errors
- **Format**: Error text and stack traces
- **Location**: Captured separately in logs
- **Use**: Error analysis, troubleshooting

### 3. Ansible Log File
- **Content**: Detailed execution logs with timestamps
- **Format**: Structured log entries
- **Location**: `logs/ansible/` directory
- **Configuration**: `--log-file` parameter or `ANSIBLE_LOG_PATH`

### 4. JSON Callback Output
- **Content**: Structured execution data
- **Format**: JSON objects per task/play
- **Configuration**: `ANSIBLE_STDOUT_CALLBACK=json`
- **Use**: Programmatic analysis, metrics

Example JSON structure:
```json
{
  "play": {
    "name": "Edit YAML Configuration",
    "id": "uuid"
  },
  "task": {
    "name": "Update YAML values",
    "id": "uuid"
  },
  "host": "localhost",
  "status": "changed",
  "start": "2025-08-01T06:50:46.928586",
  "end": "2025-08-01T06:50:47.456341",
  "duration": 0.527755,
  "results": {...}
}
```

### 5. Performance Callback
- **Content**: Task timing and performance metrics
- **Configuration**: `ANSIBLE_CALLBACKS_ENABLED=profile_tasks`
- **Location**: Embedded in standard output
- **Use**: Performance optimization

## Integration Architecture

### Log Collection Flow
```
Ansible Playbook Execution
├── STDOUT → execution_logs
├── STDERR → error_logs  
├── Log File → ansible_logs/
├── JSON Callback → structured_data/
└── Performance → metrics/
```

### Directory Structure
```
logs/
├── system.log                    # System-wide logging
├── processes/                    # Process tracking
├── executions/                   # MOP execution logs
└── ansible/                      # Ansible-specific logs
    ├── playbook_name_timestamp.json
    ├── performance_data.json
    └── structured_callbacks.json
```

## Log Storage Strategy

### Execution Logs (`logs/executions/`)
- **Format**: JSON with MOP metadata + Ansible output
- **Retention**: 90 days
- **Indexing**: By MOP ID, timestamp, success status

### Ansible Logs (`logs/ansible/`)
- **Format**: Comprehensive JSON with all Ansible data
- **Content**: 
  - Raw stdout/stderr
  - JSON callback data
  - Performance metrics
  - Variable data
  - Host information
- **Retention**: 30 days for detailed logs
- **Indexing**: By playbook name, timestamp

### System Logs (`logs/system.log`)
- **Format**: Standard logging format
- **Content**: Process start/stop, errors, warnings
- **Retention**: 7 days
- **Rotation**: Daily

## API Integration

### Endpoints for Ansible Logs

#### Get Execution Logs
```
GET /api/logs/executions?mop_id=<id>&limit=50
```
Returns MOP execution logs including Ansible output.

#### Get Ansible-Specific Logs
```
GET /api/logs/ansible?playbook_name=<name>&limit=50
```
Returns detailed Ansible execution data.

#### Search All Logs
```
GET /api/logs/search?query=<term>&type=ansible
```
Search across all Ansible logs.

## Configuration Options

### Environment Variables
```bash
# Ansible logging configuration
ANSIBLE_LOG_PATH=/app/logs/ansible.log
ANSIBLE_STDOUT_CALLBACK=json
ANSIBLE_CALLBACKS_ENABLED=profile_tasks
ANSIBLE_DEBUG=1                    # For debug logging
ANSIBLE_KEEP_REMOTE_FILES=1        # Keep temp files for debugging
```

### Playbook Execution Parameters
```bash
ansible-playbook playbook.yml \
  --log-file logs/ansible/execution.log \
  -v \                             # Verbose output
  --diff \                         # Show file differences
  --check \                        # Dry run mode
  -e "@vars/variables.yml"         # Variable files
```

## Performance Monitoring

### Metrics Captured
- **Task Duration**: Individual task execution times
- **Play Duration**: Complete play execution time
- **Connection Time**: Host connection establishment
- **Template Rendering**: Jinja2 template processing time
- **File Transfer**: Copy/fetch operation timing

### Slow Task Identification
Tasks exceeding thresholds are flagged:
- **Warning**: > 30 seconds
- **Critical**: > 2 minutes

### Resource Usage
- Memory consumption during execution
- CPU utilization per task
- Network bandwidth for remote operations

## Error Handling and Analysis

### Error Categories
1. **Connection Errors**: SSH, WinRM failures
2. **Authentication Errors**: Key/password issues  
3. **Task Failures**: Command/module execution failures
4. **Template Errors**: Jinja2 syntax/variable issues
5. **Timeout Errors**: Long-running task timeouts

### Error Log Structure
```json
{
  "error_type": "connection_failure",
  "host": "server1.example.com", 
  "task": "Update configuration",
  "message": "SSH connection timeout",
  "timestamp": "2025-08-01T06:50:46Z",
  "playbook": "update_config.yml",
  "line_number": 45
}
```

## Log Analysis and Dashboards

### Web Dashboard Features
- **Real-time Execution Monitoring**: Live playbook progress
- **Historical Analysis**: Execution trends and patterns
- **Error Dashboards**: Failure analysis and resolution tracking
- **Performance Metrics**: Task timing and optimization insights
- **Search and Filter**: Query across all log types

### Integration Points
- **Frontend Dashboard**: `templates/logs_dashboard.html`
- **API Endpoints**: RESTful log access
- **Search Functionality**: Full-text and structured search
- **Export Capabilities**: JSON, CSV export options

## Best Practices

### Log Rotation
- Implement automated log rotation to manage disk space
- Archive old logs to long-term storage
- Compress historical logs

### Security
- Sanitize sensitive data from logs (passwords, keys)
- Implement log access controls
- Encrypt logs in transit and at rest

### Monitoring
- Set up alerts for execution failures
- Monitor log file sizes and growth
- Track execution duration trends

### Debugging
- Use verbose logging for troubleshooting
- Preserve failed execution logs
- Maintain correlation between MOP and Ansible logs

## Example Integration

See `executor.py:execute_ansible_playbook()` for the complete implementation of Ansible log integration with our MOP system.