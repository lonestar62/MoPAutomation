/**
 * MOP Ansible Renderer - Frontend JavaScript
 * Provides interactive functionality for the web interface
 */

// Global application state
const MOPApp = {
    editors: {},
    config: {
        debounceDelay: 500,
        autoSaveEnabled: true
    }
};

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Main application initialization
 */
function initializeApp() {
    console.log('Initializing MOP Ansible Renderer...');
    
    // Initialize components based on current page
    initializeCodeEditors();
    initializeFormHandlers();
    initializeTooltips();
    initializeAlerts();
    initializeModalHandlers();
    
    // Page-specific initializations
    if (document.querySelector('.CodeMirror')) {
        initializeEditorEnhancements();
    }
    
    console.log('MOP Ansible Renderer initialized successfully');
}

/**
 * Initialize CodeMirror editors for YAML and template editing
 */
function initializeCodeEditors() {
    // YAML Editor initialization
    const yamlTextarea = document.getElementById('content');
    if (yamlTextarea && yamlTextarea.getAttribute('data-mode') !== 'initialized') {
        const isYaml = window.location.pathname.includes('/vars/') || 
                      yamlTextarea.name === 'variables';
        const isTemplate = window.location.pathname.includes('/templates/');
        
        let mode = 'yaml';
        if (isTemplate) {
            mode = 'markdown';
        }
        
        const editor = CodeMirror.fromTextArea(yamlTextarea, {
            mode: mode,
            theme: 'monokai',
            lineNumbers: true,
            lineWrapping: true,
            indentUnit: 2,
            tabSize: 2,
            autoCloseBrackets: true,
            matchBrackets: true,
            foldGutter: true,
            gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
            extraKeys: {
                'Ctrl-Space': 'autocomplete',
                'Ctrl-S': function(cm) {
                    saveContent();
                },
                'F11': function(cm) {
                    toggleFullscreen(cm);
                },
                'Esc': function(cm) {
                    exitFullscreen(cm);
                }
            }
        });
        
        // Set editor height
        editor.setSize(null, isTemplate ? 600 : 500);
        
        // Store editor reference
        MOPApp.editors.main = editor;
        
        // Add real-time validation for YAML
        if (isYaml) {
            editor.on('change', debounce(function() {
                validateYAML(editor);
            }, MOPApp.config.debounceDelay));
        }
        
        // Add template syntax highlighting for Jinja2
        if (isTemplate) {
            addTemplateFeatures(editor);
        }
        
        yamlTextarea.setAttribute('data-mode', 'initialized');
    }
}

/**
 * Add Jinja2 template-specific features
 */
function addTemplateFeatures(editor) {
    // Highlight Jinja2 syntax
    editor.on('change', function() {
        // Add custom styling for Jinja2 syntax
        const content = editor.getValue();
        if (content.includes('{{') || content.includes('{%')) {
            // Template detected
            addTemplateHelpers(editor);
        }
    });
}

/**
 * Add template helper functions
 */
function addTemplateHelpers(editor) {
    // Add autocomplete for common Jinja2 patterns
    CodeMirror.registerHelper('hint', 'jinja2', function(editor) {
        const cursor = editor.getCursor();
        const token = editor.getTokenAt(cursor);
        const start = token.start;
        const end = cursor.ch;
        const line = cursor.line;
        const currentWord = token.string;
        
        const suggestions = [
            '{{ variable }}',
            '{% for item in items %}',
            '{% endfor %}',
            '{% if condition %}',
            '{% endif %}',
            '{{ item.property }}',
            '{{ variable | default("default_value") }}',
            '{% set variable = value %}',
            '{{ variable | length }}',
            '{{ variable | first }}',
            '{{ variable | last }}'
        ];
        
        return {
            list: suggestions.filter(s => s.toLowerCase().includes(currentWord.toLowerCase())),
            from: CodeMirror.Pos(line, start),
            to: CodeMirror.Pos(line, end)
        };
    });
}

/**
 * Validate YAML content in real-time
 */
function validateYAML(editor) {
    const content = editor.getValue().trim();
    if (!content) return;
    
    try {
        // Basic YAML validation using simple checks
        const lines = content.split('\n');
        let indentLevel = 0;
        let hasError = false;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (line.trim() === '' || line.trim().startsWith('#')) continue;
            
            // Check for basic YAML syntax
            if (line.includes(':')) {
                const parts = line.split(':');
                if (parts.length >= 2) {
                    // Valid key-value pair
                    continue;
                }
            } else if (line.trim().startsWith('-')) {
                // Valid list item
                continue;
            } else if (line.trim().length > 0) {
                // Potential syntax error
                hasError = true;
                break;
            }
        }
        
        // Update editor styling based on validation
        updateValidationStatus(editor, !hasError);
        
    } catch (error) {
        updateValidationStatus(editor, false, error.message);
    }
}

/**
 * Update validation status visual feedback
 */
function updateValidationStatus(editor, isValid, errorMessage) {
    const wrapper = editor.getWrapperElement();
    
    // Remove existing validation classes
    wrapper.classList.remove('yaml-valid', 'yaml-invalid');
    
    // Add appropriate class
    wrapper.classList.add(isValid ? 'yaml-valid' : 'yaml-invalid');
    
    // Update or create validation message
    let statusElement = wrapper.parentNode.querySelector('.validation-status');
    if (!statusElement) {
        statusElement = document.createElement('div');
        statusElement.className = 'validation-status mt-2';
        wrapper.parentNode.appendChild(statusElement);
    }
    
    if (isValid) {
        statusElement.innerHTML = '<small class="text-success"><i class="fas fa-check-circle"></i> Valid YAML</small>';
    } else {
        statusElement.innerHTML = `<small class="text-danger"><i class="fas fa-exclamation-circle"></i> YAML Syntax Error${errorMessage ? ': ' + errorMessage : ''}</small>`;
    }
}

/**
 * Toggle fullscreen mode for editor
 */
function toggleFullscreen(editor) {
    const wrapper = editor.getWrapperElement();
    if (wrapper.classList.contains('CodeMirror-fullscreen')) {
        exitFullscreen(editor);
    } else {
        wrapper.classList.add('CodeMirror-fullscreen');
        editor.setSize(null, '100vh');
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Exit fullscreen mode
 */
function exitFullscreen(editor) {
    const wrapper = editor.getWrapperElement();
    wrapper.classList.remove('CodeMirror-fullscreen');
    editor.setSize(null, 500);
    document.body.style.overflow = '';
}

/**
 * Initialize form handlers
 */
function initializeFormHandlers() {
    // Handle MOP execution forms
    const executeButtons = document.querySelectorAll('form[action*="/execute"] button[type="submit"]');
    executeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form) {
                handleMOPExecution(e, form);
            }
        });
    });
    
    // Handle save forms with validation
    const saveForms = document.querySelectorAll('form[action*="/save"]');
    saveForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            handleSaveForm(e, this);
        });
    });
    
    // Handle file upload if present
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileUpload);
    });
}

/**
 * Handle MOP execution with confirmation and feedback
 */
function handleMOPExecution(event, form) {
    const mopId = form.action.match(/mops\/([^\/]+)\/execute/);
    const mopName = mopId ? mopId[1] : 'Unknown MOP';
    
    // Add loading state
    const button = event.target;
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="loading me-2"></span>Executing...';
    
    // Simulate execution delay for better UX
    setTimeout(() => {
        // In a real scenario, this would be handled by the form submission
        // For now, we'll let the form submit normally
        form.submit();
    }, 500);
}

/**
 * Handle save form validation
 */
function handleSaveForm(event, form) {
    // Validate content before saving
    const contentTextarea = form.querySelector('textarea[name="content"]');
    if (contentTextarea && MOPApp.editors.main) {
        const content = MOPApp.editors.main.getValue();
        
        // Update textarea value
        contentTextarea.value = content;
        
        // Validate if it's YAML
        if (form.action.includes('/vars/')) {
            if (!validateYAMLContent(content)) {
                event.preventDefault();
                showAlert('Please fix YAML syntax errors before saving.', 'danger');
                return false;
            }
        }
    }
    
    // Add loading state to save button
    const saveButton = form.querySelector('button[type="submit"]');
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.innerHTML = '<span class="loading me-2"></span>Saving...';
    }
    
    return true;
}

/**
 * Validate YAML content
 */
function validateYAMLContent(content) {
    if (!content.trim()) return true;
    
    try {
        // Basic YAML structure validation
        const lines = content.split('\n');
        let braceCount = 0;
        let bracketCount = 0;
        
        for (const line of lines) {
            if (line.trim().startsWith('#')) continue;
            
            braceCount += (line.match(/\{/g) || []).length;
            braceCount -= (line.match(/\}/g) || []).length;
            bracketCount += (line.match(/\[/g) || []).length;
            bracketCount -= (line.match(/\]/g) || []).length;
        }
        
        return braceCount === 0 && bracketCount === 0;
    } catch (error) {
        return false;
    }
}

/**
 * Handle file upload
 */
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['.yml', '.yaml', '.md', '.j2'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showAlert(`Invalid file type. Allowed types: ${allowedTypes.join(', ')}`, 'danger');
        event.target.value = '';
        return;
    }
    
    // Read file content
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        
        // Update editor if present
        if (MOPApp.editors.main) {
            MOPApp.editors.main.setValue(content);
        }
        
        showAlert(`File "${file.name}" loaded successfully.`, 'success');
    };
    
    reader.readAsText(file);
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize alert handling
 */
function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        if (!alert.querySelector('.btn-close')) {
            setTimeout(() => {
                fadeOut(alert);
            }, 5000);
        }
    });
}

/**
 * Initialize modal handlers
 */
function initializeModalHandlers() {
    // Handle execution details modal
    const modal = document.getElementById('executionDetailsModal');
    if (modal) {
        modal.addEventListener('show.bs.modal', function(event) {
            // Modal content is handled by the showExecutionDetails function
            // in the template, but we can add additional functionality here
        });
    }
}

/**
 * Initialize editor enhancements
 */
function initializeEditorEnhancements() {
    // Add keyboard shortcuts info
    addKeyboardShortcutsHelp();
    
    // Add editor toolbar if needed
    addEditorToolbar();
}

/**
 * Add keyboard shortcuts help
 */
function addKeyboardShortcutsHelp() {
    const editorContainer = document.querySelector('.CodeMirror');
    if (!editorContainer) return;
    
    const helpButton = document.createElement('button');
    helpButton.className = 'btn btn-sm btn-outline-secondary position-absolute';
    helpButton.style.top = '10px';
    helpButton.style.right = '10px';
    helpButton.style.zIndex = '1000';
    helpButton.innerHTML = '<i class="fas fa-keyboard"></i>';
    helpButton.title = 'Keyboard Shortcuts';
    
    helpButton.addEventListener('click', showKeyboardShortcuts);
    
    editorContainer.parentNode.style.position = 'relative';
    editorContainer.parentNode.appendChild(helpButton);
}

/**
 * Show keyboard shortcuts modal
 */
function showKeyboardShortcuts() {
    const shortcuts = [
        { key: 'Ctrl+S', action: 'Save content' },
        { key: 'F11', action: 'Toggle fullscreen' },
        { key: 'Esc', action: 'Exit fullscreen' },
        { key: 'Ctrl+Space', action: 'Autocomplete' },
        { key: 'Ctrl+F', action: 'Find' },
        { key: 'Ctrl+H', action: 'Find and replace' },
        { key: 'Ctrl+G', action: 'Go to line' }
    ];
    
    let content = '<h6>Keyboard Shortcuts</h6><table class="table table-sm">';
    shortcuts.forEach(shortcut => {
        content += `<tr><td><kbd>${shortcut.key}</kbd></td><td>${shortcut.action}</td></tr>`;
    });
    content += '</table>';
    
    showModal('Keyboard Shortcuts', content);
}

/**
 * Add editor toolbar
 */
function addEditorToolbar() {
    const editorContainer = document.querySelector('.CodeMirror');
    if (!editorContainer || editorContainer.dataset.toolbarAdded) return;
    
    const toolbar = document.createElement('div');
    toolbar.className = 'editor-toolbar btn-group btn-group-sm mb-2';
    toolbar.innerHTML = `
        <button type="button" class="btn btn-outline-secondary" onclick="formatYAML()" title="Format YAML">
            <i class="fas fa-indent"></i>
        </button>
        <button type="button" class="btn btn-outline-secondary" onclick="validateCurrentContent()" title="Validate">
            <i class="fas fa-check-circle"></i>
        </button>
        <button type="button" class="btn btn-outline-secondary" onclick="toggleLineNumbers()" title="Toggle Line Numbers">
            <i class="fas fa-list-ol"></i>
        </button>
    `;
    
    editorContainer.parentNode.insertBefore(toolbar, editorContainer);
    editorContainer.dataset.toolbarAdded = 'true';
}

/**
 * Format YAML content
 */
function formatYAML() {
    if (!MOPApp.editors.main) return;
    
    const content = MOPApp.editors.main.getValue();
    try {
        // Basic YAML formatting - add proper indentation
        const lines = content.split('\n');
        const formatted = lines.map(line => {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('#')) return line;
            
            // Basic indentation for nested items
            const indentLevel = (line.match(/^  */)[0].length / 2);
            return '  '.repeat(indentLevel) + trimmed;
        }).join('\n');
        
        MOPApp.editors.main.setValue(formatted);
        showAlert('YAML formatted successfully.', 'success');
    } catch (error) {
        showAlert('Failed to format YAML: ' + error.message, 'danger');
    }
}

/**
 * Validate current content
 */
function validateCurrentContent() {
    if (!MOPApp.editors.main) return;
    
    const content = MOPApp.editors.main.getValue();
    const isValid = validateYAMLContent(content);
    
    if (isValid) {
        showAlert('Content is valid!', 'success');
    } else {
        showAlert('Content has validation errors.', 'danger');
    }
}

/**
 * Toggle line numbers
 */
function toggleLineNumbers() {
    if (!MOPApp.editors.main) return;
    
    const current = MOPApp.editors.main.getOption('lineNumbers');
    MOPApp.editors.main.setOption('lineNumbers', !current);
}

/**
 * Utility function to show alerts
 */
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto dismiss
    if (duration > 0) {
        setTimeout(() => {
            if (alert.parentNode) {
                fadeOut(alert);
            }
        }, duration);
    }
}

/**
 * Utility function to show modals
 */
function showModal(title, content, size = '') {
    const modalId = 'dynamicModal';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = modalId;
        modal.innerHTML = `
            <div class="modal-dialog ${size}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"></h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body"></div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    modal.querySelector('.modal-title').textContent = title;
    modal.querySelector('.modal-body').innerHTML = content;
    
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

/**
 * Utility function for fade out animation
 */
function fadeOut(element) {
    element.style.transition = 'opacity 0.5s';
    element.style.opacity = '0';
    setTimeout(() => {
        if (element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }, 500);
}

/**
 * Debounce function to limit rapid function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Save content function (can be called from keyboard shortcut)
 */
function saveContent() {
    const saveButton = document.querySelector('button[type="submit"]');
    if (saveButton) {
        saveButton.click();
    }
}

/**
 * Add CSS for editor enhancements
 */
function addEditorStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .CodeMirror-fullscreen {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            z-index: 9999 !important;
            background: var(--bs-body-bg) !important;
        }
        
        .yaml-valid .CodeMirror {
            border-color: var(--bs-success) !important;
        }
        
        .yaml-invalid .CodeMirror {
            border-color: var(--bs-danger) !important;
        }
        
        .editor-toolbar {
            margin-bottom: 0.5rem;
        }
        
        .validation-status {
            font-size: 0.875rem;
        }
    `;
    document.head.appendChild(style);
}

// Add editor styles when the script loads
addEditorStyles();

// Export for global access
window.MOPApp = MOPApp;
