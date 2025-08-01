import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional
from functools import wraps

class MOPLogger:
    """Comprehensive logging system for MOP operations"""
    
    def __init__(self, logs_dir='logs'):
        self.logs_dir = logs_dir
        self.system_log_file = os.path.join(logs_dir, 'system.log')
        self.process_logs_dir = os.path.join(logs_dir, 'processes')
        self.execution_logs_dir = os.path.join(logs_dir, 'executions')
        
        # Ensure directories exist
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(self.process_logs_dir, exist_ok=True)
        os.makedirs(self.execution_logs_dir, exist_ok=True)
        
        # Configure system logger
        self.system_logger = self._setup_system_logger()
        
    def _setup_system_logger(self):
        """Setup system-wide logger"""
        logger = logging.getLogger('mop_system')
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(self.system_log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_process_start(self, process_type: str, process_id: str, metadata: Dict[str, Any]) -> str:
        """Log the start of a process"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': 'process_start',
            'process_type': process_type,
            'process_id': process_id,
            'metadata': metadata,
            'status': 'started'
        }
        
        # Log to system logger
        self.system_logger.info(f"Process started: {process_type} - {process_id}")
        
        # Save detailed log
        log_file = os.path.join(self.process_logs_dir, f"{process_id}_{timestamp.replace(':', '-')}.json")
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2, default=str)
        
        return log_file
    
    def log_process_step(self, process_id: str, step_name: str, step_data: Dict[str, Any], status: str = 'success'):
        """Log a step within a process"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': 'process_step',
            'process_id': process_id,
            'step_name': step_name,
            'step_data': step_data,
            'status': status
        }
        
        self.system_logger.info(f"Process step {status}: {process_id} - {step_name}")
        
        # Append to process log
        self._append_to_process_log(process_id, log_entry)
    
    def log_process_end(self, process_id: str, result: Dict[str, Any], status: str = 'completed'):
        """Log the end of a process"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': 'process_end',
            'process_id': process_id,
            'result': result,
            'status': status
        }
        
        self.system_logger.info(f"Process {status}: {process_id}")
        
        # Append to process log
        self._append_to_process_log(process_id, log_entry)
    
    def log_error(self, process_id: str, error: Exception, context: Dict[str, Any] = None):
        """Log an error with full context"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event_type': 'error',
            'process_id': process_id,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        self.system_logger.error(f"Error in process {process_id}: {error}")
        
        # Append to process log
        self._append_to_process_log(process_id, log_entry)
        
        # Also save as separate error log
        error_file = os.path.join(self.logs_dir, f"error_{process_id}_{timestamp.replace(':', '-')}.json")
        with open(error_file, 'w') as f:
            json.dump(log_entry, f, indent=2, default=str)
    
    def _append_to_process_log(self, process_id: str, log_entry: Dict[str, Any]):
        """Append log entry to process log file"""
        # Find the latest log file for this process
        process_files = [f for f in os.listdir(self.process_logs_dir) if f.startswith(process_id)]
        if process_files:
            latest_file = sorted(process_files)[-1]
            log_file = os.path.join(self.process_logs_dir, latest_file)
            
            # Read existing data
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                
                # Ensure events list exists
                if 'events' not in data:
                    data['events'] = []
                
                # Add new event
                data['events'].append(log_entry)
                
                # Update status
                data['last_updated'] = log_entry['timestamp']
                if log_entry.get('status') in ['completed', 'failed', 'error']:
                    data['status'] = log_entry['status']
                
                # Write back
                with open(log_file, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                    
            except Exception as e:
                self.system_logger.error(f"Error updating process log: {e}")
    
    def get_process_logs(self, process_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get process logs, optionally filtered by process_id"""
        logs = []
        
        try:
            for filename in os.listdir(self.process_logs_dir):
                if process_id and not filename.startswith(process_id):
                    continue
                
                filepath = os.path.join(self.process_logs_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        log_data = json.load(f)
                        logs.append(log_data)
                except Exception as e:
                    self.system_logger.warning(f"Error reading log file {filename}: {e}")
            
            # Sort by timestamp (newest first)
            logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return logs[:limit]
            
        except Exception as e:
            self.system_logger.error(f"Error getting process logs: {e}")
            return []
    
    def get_system_logs(self, lines: int = 100) -> List[str]:
        """Get recent system log lines"""
        try:
            with open(self.system_log_file, 'r') as f:
                log_lines = f.readlines()
            
            # Return last N lines
            return log_lines[-lines:] if lines else log_lines
            
        except Exception as e:
            self.system_logger.error(f"Error reading system logs: {e}")
            return []
    
    def get_execution_logs(self, mop_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get MOP execution logs"""
        logs = []
        
        try:
            # Check both main logs directory and executions subdirectory
            log_dirs = [self.logs_dir, self.execution_logs_dir]
            
            for log_dir in log_dirs:
                if not os.path.exists(log_dir):
                    continue
                    
                for filename in os.listdir(log_dir):
                    if not filename.endswith('.json'):
                        continue
                    
                    if mop_id and not filename.startswith(mop_id):
                        continue
                    
                    filepath = os.path.join(log_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            log_data = json.load(f)
                            
                        # Ensure it's an execution log
                        if 'execution_id' in log_data or 'mop_id' in log_data:
                            logs.append(log_data)
                            
                    except Exception as e:
                        self.system_logger.warning(f"Error reading execution log {filename}: {e}")
            
            # Sort by timestamp (newest first)
            logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return logs[:limit]
            
        except Exception as e:
            self.system_logger.error(f"Error getting execution logs: {e}")
            return []
    
    def search_logs(self, query: str, log_type: str = 'all', limit: int = 100) -> List[Dict[str, Any]]:
        """Search logs for specific content"""
        results = []
        query_lower = query.lower()
        
        try:
            if log_type in ['all', 'process']:
                process_logs = self.get_process_logs(limit=limit)
                for log in process_logs:
                    log_str = json.dumps(log, default=str).lower()
                    if query_lower in log_str:
                        log['log_type'] = 'process'
                        results.append(log)
            
            if log_type in ['all', 'execution']:
                execution_logs = self.get_execution_logs(limit=limit)
                for log in execution_logs:
                    log_str = json.dumps(log, default=str).lower()
                    if query_lower in log_str:
                        log['log_type'] = 'execution'
                        results.append(log)
            
            # Sort by timestamp (newest first)
            results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            self.system_logger.error(f"Error searching logs: {e}")
            return []

# Decorator for logging function calls
def log_process(process_type: str, logger_instance: MOPLogger = None):
    """Decorator to automatically log process execution"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use global logger if none provided
            logger = logger_instance or MOPLogger()
            
            # Generate process ID
            process_id = f"{process_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Prepare metadata
            metadata = {
                'function_name': func.__name__,
                'args': str(args)[:200],  # Truncate for log size
                'kwargs': str(kwargs)[:200]
            }
            
            # Log process start
            logger.log_process_start(process_type, process_id, metadata)
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Log successful completion
                logger.log_process_end(process_id, {'result': str(result)[:500]}, 'completed')
                
                return result
                
            except Exception as e:
                # Log error
                logger.log_error(process_id, e, metadata)
                raise
        
        return wrapper
    return decorator

# Global logger instance
mop_logger = MOPLogger()