document.addEventListener('DOMContentLoaded', function() {
    // Project Modal Toggle
    const projectModal = document.getElementById('project-modal');
    const addProjectBtn = document.getElementById('add-project-btn');
    const cancelProjectBtn = document.getElementById('cancel-project');
    
    if (addProjectBtn) {
        addProjectBtn.addEventListener('click', function(e) {
            e.preventDefault();
            projectModal.classList.remove('hidden');
        });
    }
    
    if (cancelProjectBtn) {
        cancelProjectBtn.addEventListener('click', function() {
            projectModal.classList.add('hidden');
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === projectModal) {
            projectModal.classList.add('hidden');
        }
    });
    
    // Task completion
    const taskCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                const taskItem = this.closest('.task-item');
                if (taskItem) {
                    taskItem.classList.add('task-complete');
                    setTimeout(() => {
                        // In a real app, we would make an API call to update the task status
                        window.location.reload();
                    }, 300);
                }
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                } else {
                    field.classList.remove('border-red-500');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        function autoResize() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        }
        
        textarea.addEventListener('input', autoResize);
        // Trigger once on load
        autoResize.call(textarea);
    });
    
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Priority indicator for task form
    const prioritySelect = document.getElementById('priority');
    if (prioritySelect) {
        const priorityIndicator = document.createElement('div');
        priorityIndicator.className = 'w-3 h-3 rounded-full ml-2';
        prioritySelect.parentNode.insertBefore(priorityIndicator, prioritySelect.nextSibling);
        
        function updatePriorityIndicator() {
            const priority = parseInt(prioritySelect.value);
            let color = 'bg-gray-300'; // Default
            
            if (priority === 1) color = 'bg-red-500';
            else if (priority === 2) color = 'bg-yellow-500';
            else if (priority === 3) color = 'bg-blue-500';
            
            priorityIndicator.className = `w-3 h-3 rounded-full ml-2 ${color}`;
        }
        
        prioritySelect.addEventListener('change', updatePriorityIndicator);
        updatePriorityIndicator(); // Initialize
    }
});

// Utility function to show loading state
function setLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = `
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            ${button.textContent}
        `;
    } else {
        button.disabled = false;
        // Restore original content if needed
    }
}
