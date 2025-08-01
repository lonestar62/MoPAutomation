import os
import json
import subprocess
import logging
from datetime import datetime
from renderer import MOPRenderer
from category_map import CATEGORY_TO_PLAYBOOK

class MOPExecutor:
    """Handles MOP execution using mock Ansible playbooks"""
    
    def __init__(self, playbooks_dir='playbooks', logs_dir='logs'):
        self.playbooks_dir = playbooks_dir
        self.logs_dir = logs_dir
        self.renderer = MOPRenderer()
        self.logger = logging.getLogger(__name__)
        
        # Ensure logs directory exists
        os.makedirs(logs_dir, exist_ok=True)
    
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
            
            return {
                'success': overall_success,
                'execution_id': execution_id,
                'results': execution_results,
                'log_file': f"{execution_id}.json"
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
            
            # Mock ansible-playbook execution
            # In a real environment, this would be:
            # subprocess.run(['ansible-playbook', playbook_path, '-e', json.dumps(variables)])
            
            # For now, we'll simulate the execution
            self.logger.info(f"Executing playbook {playbook_name} with variables: {variables}")
            
            # Simulate different execution scenarios based on playbook type
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
            success = random.choice([True, True, False])  # 66% success rate
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
    
    def save_execution_log(self, execution_id, log_data):
        """Save execution log to JSON file"""
        log_file = os.path.join(self.logs_dir, f"{execution_id}.json")
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
        
        self.logger.info(f"Execution log saved to {log_file}")
