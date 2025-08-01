import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from renderer import MOPRenderer
from executor import MOPExecutor
from category_map import CATEGORY_TO_PLAYBOOK

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize components
renderer = MOPRenderer()
executor = MOPExecutor()

# Ensure required directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('vars', exist_ok=True)
os.makedirs('playbooks', exist_ok=True)

@app.route('/')
def index():
    """Main dashboard showing system overview"""
    try:
        mops = renderer.list_mops()
        recent_executions = get_recent_executions()
        return render_template('index.html', mops=mops, recent_executions=recent_executions)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {e}")
        return render_template('index.html', mops=[], recent_executions=[], error=str(e))

@app.route('/api-demo')
def api_demo():
    """Demo page showing Next.js integration readiness"""
    return render_template('api_demo.html')

@app.route('/mops')
def list_mops():
    """List all available MOPs"""
    try:
        mops = renderer.list_mops()
        return render_template('mops.html', mops=mops)
    except Exception as e:
        app.logger.error(f"Error listing MOPs: {e}")
        return render_template('mops.html', mops=[], error=str(e))

@app.route('/mops/<mop_id>')
def mop_detail(mop_id):
    """Show MOP details and rendered content"""
    try:
        rendered_mop = renderer.render_mop(mop_id)
        if not rendered_mop:
            flash(f'MOP {mop_id} not found', 'error')
            return redirect(url_for('list_mops'))
        
        execution_history = get_mop_execution_history(mop_id)
        return render_template('mop_detail.html', mop=rendered_mop, history=execution_history)
    except Exception as e:
        app.logger.error(f"Error loading MOP {mop_id}: {e}")
        flash(f'Error loading MOP: {e}', 'error')
        return redirect(url_for('list_mops'))

@app.route('/mops/<mop_id>/execute', methods=['POST'])
def execute_mop(mop_id):
    """Execute a MOP"""
    try:
        result = executor.execute_mop(mop_id)
        
        if result['success']:
            flash(f'MOP {mop_id} executed successfully', 'success')
        else:
            flash(f'MOP {mop_id} execution failed: {result.get("error", "Unknown error")}', 'error')
        
        return redirect(url_for('mop_detail', mop_id=mop_id))
    except Exception as e:
        app.logger.error(f"Error executing MOP {mop_id}: {e}")
        flash(f'Error executing MOP: {e}', 'error')
        return redirect(url_for('mop_detail', mop_id=mop_id))

@app.route('/templates/<template_name>/edit')
def edit_template(template_name):
    """Edit MOP template"""
    try:
        template_content = renderer.get_template_content(template_name)
        return render_template('edit_template.html', 
                             template_name=template_name, 
                             content=template_content)
    except Exception as e:
        app.logger.error(f"Error loading template {template_name}: {e}")
        flash(f'Error loading template: {e}', 'error')
        return redirect(url_for('list_mops'))

@app.route('/templates/<template_name>/save', methods=['POST'])
def save_template(template_name):
    """Save MOP template"""
    try:
        content = request.form.get('content', '')
        renderer.save_template(template_name, content)
        flash(f'Template {template_name} saved successfully', 'success')
        return redirect(url_for('list_mops'))
    except Exception as e:
        app.logger.error(f"Error saving template {template_name}: {e}")
        flash(f'Error saving template: {e}', 'error')
        return redirect(url_for('edit_template', template_name=template_name))

@app.route('/vars/<mop_id>/edit')
def edit_variables(mop_id):
    """Edit MOP variables"""
    try:
        variables_content = renderer.get_variables_content(mop_id)
        return render_template('edit_variables.html', 
                             mop_id=mop_id, 
                             content=variables_content)
    except Exception as e:
        app.logger.error(f"Error loading variables for {mop_id}: {e}")
        flash(f'Error loading variables: {e}', 'error')
        return redirect(url_for('list_mops'))

@app.route('/vars/<mop_id>/save', methods=['POST'])
def save_variables(mop_id):
    """Save MOP variables"""
    try:
        content = request.form.get('content', '')
        renderer.save_variables(mop_id, content)
        flash(f'Variables for {mop_id} saved successfully', 'success')
        return redirect(url_for('mop_detail', mop_id=mop_id))
    except Exception as e:
        app.logger.error(f"Error saving variables for {mop_id}: {e}")
        flash(f'Error saving variables: {e}', 'error')
        return redirect(url_for('edit_variables', mop_id=mop_id))

# API Endpoints
@app.route('/api/mops')
def api_list_mops():
    """API endpoint to list all MOPs"""
    try:
        mops = renderer.list_mops()
        return jsonify({'success': True, 'mops': mops})
    except Exception as e:
        app.logger.error(f"API error listing MOPs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mops/<mop_id>')
def api_get_mop(mop_id):
    """API endpoint to get a specific MOP"""
    try:
        rendered_mop = renderer.render_mop(mop_id)
        if not rendered_mop:
            return jsonify({'success': False, 'error': 'MOP not found'}), 404
        
        return jsonify({'success': True, 'mop': rendered_mop})
    except Exception as e:
        app.logger.error(f"API error getting MOP {mop_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mops/<mop_id>/execute', methods=['POST'])
def api_execute_mop(mop_id):
    """API endpoint to execute a MOP"""
    try:
        result = executor.execute_mop(mop_id)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"API error executing MOP {mop_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_recent_executions(limit=10):
    """Get recent MOP executions"""
    try:
        log_files = []
        if os.path.exists('logs'):
            for filename in os.listdir('logs'):
                if filename.endswith('.json'):
                    filepath = os.path.join('logs', filename)
                    stat = os.stat(filepath)
                    log_files.append((filepath, stat.st_mtime))
        
        # Sort by modification time, most recent first
        log_files.sort(key=lambda x: x[1], reverse=True)
        
        executions = []
        for filepath, _ in log_files[:limit]:
            try:
                with open(filepath, 'r') as f:
                    execution = json.load(f)
                    executions.append(execution)
            except Exception as e:
                app.logger.warning(f"Error reading log file {filepath}: {e}")
        
        return executions
    except Exception as e:
        app.logger.error(f"Error getting recent executions: {e}")
        return []

def get_mop_execution_history(mop_id):
    """Get execution history for a specific MOP"""
    try:
        executions = []
        if os.path.exists('logs'):
            for filename in os.listdir('logs'):
                if filename.startswith(f'{mop_id}_') and filename.endswith('.json'):
                    filepath = os.path.join('logs', filename)
                    try:
                        with open(filepath, 'r') as f:
                            execution = json.load(f)
                            executions.append(execution)
                    except Exception as e:
                        app.logger.warning(f"Error reading log file {filepath}: {e}")
        
        # Sort by timestamp, most recent first
        executions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return executions
    except Exception as e:
        app.logger.error(f"Error getting execution history for {mop_id}: {e}")
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
