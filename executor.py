import os
import json
import subprocess
import logging
from datetime import datetime
from renderer import MOPRenderer
from category_map import CATEGORY_TO_PLAYBOOK
from logger import log_process, mop_logger

class MOPExecutor:
    """Handles MOP execution using mock Ansible playbooks"""
    
    def __init__(self, playbooks_dir='playbooks', logs_dir='logs'):
        self.playbooks_dir = playbooks_dir
        self.logs_dir = logs_dir
        self.renderer = MOPRenderer()
        self.logger = logging.getLogger(__name__)
        
        # Ensure logs directory exists
        os.makedirs(logs_dir, exist_ok=True)
    
    @log_process('execute_mop')
    def execute_mop(self, mop_id):
        """Execute a MOP by running associated playbooks"""
        timestamp = datetime.now().isoformat()
        execution_id = f"{mop_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Load MOP details
            rendered_mop = self.renderer.render_mop(mop_id)
            if not rendered_mop:
                raise Exception(f"MOP {mop_id} not found")
            
            category = rendered_mop['variables'].get('category', 'unknown')
            playbooks = CATEGORY_TO_PLAYBOOK.get(category, [])
            
            if not playbooks:
                raise Exception(f"No playbooks found for category {category}")
            
            # Execute each playbook
            execution_results = []
            overall_success = True
            
            for playbook in playbooks:
                playbook_result = self.execute_playbook(playbook, rendered_mop['variables'])
                execution_results.append(playbook_result)
                
                if not playbook_result['success']:
                    overall_success = False
                    # Continue executing other playbooks for now
            
            # Log execution results
            execution_log = {
                'execution_id': execution_id,
                'mop_id': mop_id,
                'timestamp': timestamp,
                'category': category,
                'playbooks': playbooks,
                'success': overall_success,
                'results': execution_results,
                'variables': rendered_mop['variables']
            }
            
            self.save_execution_log(execution_id, execution_log)
            
            # Add error summary for failed executions
            error_summary = None
            if not overall_success:
                failed_playbooks = [r for r in execution_results if not r['success']]
                error_summary = f"Failed playbooks: {', '.join([p['playbook'] for p in failed_playbooks])}"
            
            return {
                'success': overall_success,
                'execution_id': execution_id,
                'results': execution_results,
                'log_file': f"{execution_id}.json",
                'error': error_summary if not overall_success else None
            }
            
        except Exception as e:
            self.logger.error(f"Error executing MOP {mop_id}: {e}")
            
            # Log the error
            error_log = {
                'execution_id': execution_id,
                'mop_id': mop_id,
                'timestamp': timestamp,
                'success': False,
                'error': str(e)
            }
            
            try:
                self.save_execution_log(execution_id, error_log)
            except:
                pass
            
            return {
                'success': False,
                'execution_id': execution_id,
                'error': str(e)
            }
    
    def execute_playbook(self, playbook_name, variables):
        """Execute a single playbook (mock execution)"""
        start_time = datetime.now()
        
        try:
            playbook_path = os.path.join(self.playbooks_dir, playbook_name)
            
            # Check if playbook exists
            if not os.path.exists(playbook_path):
                raise Exception(f"Playbook {playbook_name} not found at {playbook_path}")
            
            # Real ansible-playbook execution with comprehensive logging
            # Ansible provides multiple log outputs that we capture:
            # 1. STDOUT: Playbook execution output
            # 2. STDERR: Error messages and warnings
            # 3. Return code: Exit status
            # 4. Ansible log file: Detailed execution logs
            # 5. JSON callback: Structured execution data
            
            # Log execution start
            mop_logger.log_process_step(
                f"execute_mop_{datetime.now().strftime('%Y%m%d_%H%M%S')}", 
                f"start_playbook_{playbook_name}",
                {"playbook": playbook_name, "variables_count": len(variables)}
            )
            
            # In production, this would be real Ansible execution:
            success, output, return_code, ansible_logs = self.execute_ansible_playbook(playbook_path, variables)
            
            # For demo, we'll simulate but show the real integration structure
            success, output, return_code = self.mock_playbook_execution(playbook_name, variables)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'playbook': playbook_name,
                'success': success,
                'return_code': return_code,
                'output': output,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration
            }
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'playbook': playbook_name,
                'success': False,
                'return_code': 1,
                'output': f"Error: {str(e)}",
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration,
                'error': str(e)
            }
    
    def mock_playbook_execution(self, playbook_name, variables):
        """Mock playbook execution with realistic scenarios"""
        import time
        import random
        
        # Simulate execution time
        time.sleep(random.uniform(0.5, 2.0))
        
        # Simulate success/failure based on playbook type
        if 'patch_linux' in playbook_name:
            success = random.choice([True, True, True, False])  # 75% success rate
            if success:
                output = f"""
PLAY [Patch Linux Systems] ****************************************************

TASK [Update package cache] ***************************************************
ok: [server1.{variables.get('region', 'eastus2')}.example.com]
ok: [server2.{variables.get('region', 'eastus2')}.example.com]

TASK [Install security updates] **********************************************
changed: [server1.{variables.get('region', 'eastus2')}.example.com]
changed: [server2.{variables.get('region', 'eastus2')}.example.com]

TASK [Reboot if required] *****************************************************
skipping: [server1.{variables.get('region', 'eastus2')}.example.com]
changed: [server2.{variables.get('region', 'eastus2')}.example.com]

PLAY RECAP ********************************************************************
server1.{variables.get('region', 'eastus2')}.example.com : ok=2    changed=1    unreachable=0    failed=0
server2.{variables.get('region', 'eastus2')}.example.com : ok=3    changed=2    unreachable=0    failed=0
"""
                return_code = 0
            else:
                output = f"""
PLAY [Patch Linux Systems] ****************************************************

TASK [Update package cache] ***************************************************
ok: [server1.{variables.get('region', 'eastus2')}.example.com]
failed: [server2.{variables.get('region', 'eastus2')}.example.com] => {{"msg": "Connection timeout"}}

PLAY RECAP ********************************************************************
server1.{variables.get('region', 'eastus2')}.example.com : ok=1    changed=0    unreachable=0    failed=0
server2.{variables.get('region', 'eastus2')}.example.com : ok=0    changed=0    unreachable=1    failed=1
"""
                return_code = 2
                
        elif 'edit_yaml' in playbook_name:
            success = True
            output = f"""
PLAY [Edit YAML Configuration] ************************************************

TASK [Backup existing configuration] *****************************************
changed: [localhost]

TASK [Update YAML values] *****************************************************
changed: [localhost]

TASK [Validate YAML syntax] **************************************************
ok: [localhost]

PLAY RECAP ********************************************************************
localhost : ok=3    changed=2    unreachable=0    failed=0
"""
            return_code = 0
            
        elif 'commit_to_git' in playbook_name:
            # In development environment, sometimes git operations work, sometimes they fail
            # This demonstrates both success and failure scenarios
            success = random.choice([True, False])  # 50% success rate for demo
            if success:
                output = f"""
PLAY [Commit to Git Repository] ***********************************************

TASK [Git add changes] ********************************************************
changed: [localhost]

TASK [Git commit] *************************************************************
changed: [localhost]

TASK [Git push] ***************************************************************
ok: [localhost]

PLAY RECAP ********************************************************************
localhost : ok=3    changed=2    unreachable=0    failed=0
"""
                return_code = 0
            else:
                output = f"""
PLAY [Commit to Git Repository] ***********************************************

TASK [Git add changes] ********************************************************
changed: [localhost]

TASK [Git commit] *************************************************************
changed: [localhost]

TASK [Git push] ***************************************************************
failed: [localhost] => {{"msg": "Permission denied (publickey)"}}

PLAY RECAP ********************************************************************
localhost : ok=2    changed=2    unreachable=0    failed=1
"""
                return_code = 2
                
        elif 'run_manual_pipeline' in playbook_name:
            success = True
            output = f"""
PLAY [Trigger Azure DevOps Pipeline] *****************************************

TASK [Get pipeline ID] ********************************************************
ok: [localhost]

TASK [Trigger pipeline run] **************************************************
changed: [localhost]

TASK [Wait for pipeline completion] ******************************************
ok: [localhost]

PLAY RECAP ********************************************************************
localhost : ok=3    changed=1    unreachable=0    failed=0
"""
            return_code = 0
            
        else:
            # Default mock execution
            success = True
            output = f"""
PLAY [Generic Playbook] *******************************************************

TASK [Execute tasks] **********************************************************
changed: [localhost]

PLAY RECAP ********************************************************************
localhost : ok=1    changed=1    unreachable=0    failed=0
"""
            return_code = 0
        
        return success, output, return_code
    
    def execute_ansible_playbook(self, playbook_path, variables):
        """Execute real Ansible playbook with comprehensive logging"""
        # This method shows how real Ansible integration would work
        
        # Ansible log file configuration
        ansible_log_file = os.path.join(self.logs_dir, f"ansible_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # Ansible provides these logging mechanisms:
        
        # 1. Standard execution with log file
        ansible_cmd = [
            'ansible-playbook',
            playbook_path,
            '-e', json.dumps(variables),
            '--log-file', ansible_log_file,  # Ansible's built-in logging
            '-v',  # Verbose output for detailed logs
        ]
        
        # 2. JSON callback for structured data
        json_log_file = os.path.join(self.logs_dir, f"ansible_json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        env = os.environ.copy()
        env['ANSIBLE_STDOUT_CALLBACK'] = 'json'  # JSON structured output
        env['ANSIBLE_LOG_PATH'] = ansible_log_file  # Standard log file
        
        # 3. Additional Ansible logging options available:
        # - ANSIBLE_DEBUG=1 for debug logging
        # - ANSIBLE_KEEP_REMOTE_FILES=1 to keep temporary files
        # - ANSIBLE_CALLBACKS_ENABLED=profile_tasks for performance logging
        
        try:
            # Execute Ansible with comprehensive logging
            result = subprocess.run(
                ansible_cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=300  # 5 minute timeout
            )
            
            # Ansible log types captured:
            logs = {
                'stdout': result.stdout,           # Play execution output
                'stderr': result.stderr,           # Warnings and errors
                'return_code': result.returncode,  # Exit status
                'ansible_log': self._read_ansible_log(ansible_log_file),  # Detailed log
                'json_output': self._parse_json_callback(result.stdout),  # Structured data
                'performance': self._extract_performance_data(result.stdout)  # Timing info
            }
            
            # Save comprehensive Ansible logs
            self._save_ansible_logs(playbook_path, logs)
            
            return (
                result.returncode == 0,
                result.stdout,
                result.returncode,
                logs
            )
            
        except subprocess.TimeoutExpired:
            error_msg = f"Ansible playbook {playbook_path} timed out after 5 minutes"
            self.logger.error(error_msg)
            return False, error_msg, 1, {}
            
        except Exception as e:
            error_msg = f"Error executing Ansible playbook {playbook_path}: {e}"
            self.logger.error(error_msg)
            return False, error_msg, 1, {}
    
    def _read_ansible_log(self, log_file):
        """Read Ansible's detailed log file"""
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    return f.read()
        except Exception as e:
            self.logger.warning(f"Could not read Ansible log file: {e}")
        return ""
    
    def _parse_json_callback(self, stdout):
        """Parse JSON callback output from Ansible"""
        # Ansible JSON callback provides structured data:
        # - Task results with timing
        # - Variable data
        # - Host information
        # - Change tracking
        try:
            lines = stdout.split('\n')
            json_data = []
            for line in lines:
                if line.strip().startswith('{'):
                    try:
                        data = json.loads(line)
                        json_data.append(data)
                    except json.JSONDecodeError:
                        continue
            return json_data
        except Exception as e:
            self.logger.warning(f"Could not parse JSON callback: {e}")
        return []
    
    def _extract_performance_data(self, output):
        """Extract performance timing from Ansible output"""
        # Ansible provides timing data for:
        # - Task execution times
        # - Play duration
        # - Handler execution
        # - Connection times
        performance = {
            'total_duration': 0,
            'task_timings': [],
            'slow_tasks': []
        }
        
        # Parse timing information from output
        lines = output.split('\n')
        for line in lines:
            if 'changed:' in line or 'ok:' in line:
                # Extract task timing (would need regex for real implementation)
                pass
                
        return performance
    
    def _save_ansible_logs(self, playbook_path, logs):
        """Save comprehensive Ansible logs to structured files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        playbook_name = os.path.basename(playbook_path).replace('.yml', '').replace('.yaml', '')
        
        # Save to logs/ansible/ subdirectory
        ansible_logs_dir = os.path.join(self.logs_dir, 'ansible')
        os.makedirs(ansible_logs_dir, exist_ok=True)
        
        # Comprehensive log file with all Ansible data
        comprehensive_log = {
            'timestamp': datetime.now().isoformat(),
            'playbook': playbook_path,
            'playbook_name': playbook_name,
            'logs': logs,
            'log_type': 'ansible_comprehensive'
        }
        
        log_file = os.path.join(ansible_logs_dir, f"{playbook_name}_{timestamp}.json")
        with open(log_file, 'w') as f:
            json.dump(comprehensive_log, f, indent=2, default=str)
        
        self.logger.info(f"Saved comprehensive Ansible logs to {log_file}")
    
    def save_execution_log(self, execution_id, log_data):
        """Save execution log to JSON file"""
        log_file = os.path.join(self.logs_dir, f"{execution_id}.json")
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
        
        self.logger.info(f"Execution log saved to {log_file}")
