// ===== ADMIN PANEL JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Admin Panel JavaScript yuklandi!');
    
    // Initialize admin functions
    initAdminTables();
    initAdminForms();
    initAdminCharts();
    initAdminNotifications();
    initBulkActions();
    initQuickSearch();
    initRealTimeUpdates();
});

// ===== ADMIN TABLES =====
function initAdminTables() {
    // Table row hover effects
    const tableRows = document.querySelectorAll('.admin-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Table sorting
    const sortableHeaders = document.querySelectorAll('.admin-table th[data-sort]');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            const currentUrl = new URL(window.location);
            const currentSort = currentUrl.searchParams.get('sort');
            
            if (currentSort === sortField) {
                currentUrl.searchParams.set('sort', `-${sortField}`);
            } else {
                currentUrl.searchParams.set('sort', sortField);
            }
            
            window.location.href = currentUrl.toString();
        });
    });
    
    // Row selection
    const selectAllCheckbox = document.getElementById('selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            rowCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActions();
        });
    }
    
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActions);
    });
}

// ===== ADMIN FORMS =====
function initAdminForms() {
    // Form validation
    const adminForms = document.querySelectorAll('.admin-form');
    adminForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAdminNotification('Iltimos, barcha majburiy maydonlarni to\'ldiring!', 'error');
            }
        });
    });
    
    // Auto-save drafts
    const autoSaveFields = document.querySelectorAll('[data-autosave]');
    autoSaveFields.forEach(field => {
        field.addEventListener('input', debounce(function() {
            const key = `autosave_${field.name}`;
            localStorage.setItem(key, field.value);
            showAdminNotification('Qoralama saqlandi', 'info', 2000);
        }, 1000));
        
        // Load saved draft
        const savedValue = localStorage.getItem(`autosave_${field.name}`);
        if (savedValue && !field.value) {
            field.value = savedValue;
        }
    });
    
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.getElementById(`${input.id}-preview`);
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = `${input.id}-preview`;
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        preview.style.maxHeight = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// ===== ADMIN CHARTS =====
function initAdminCharts() {
    // Simple chart implementation using Chart.js if available
    if (typeof Chart !== 'undefined') {
        // Sales chart
        const salesChartCanvas = document.getElementById('salesChart');
        if (salesChartCanvas) {
            new Chart(salesChartCanvas, {
                type: 'line',
                data: {
                    labels: ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun'],
                    datasets: [{
                        label: 'Sotuvlar',
                        data: [12, 19, 3, 5, 2, 3],
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
        
        // Users chart
        const usersChartCanvas = document.getElementById('usersChart');
        if (usersChartCanvas) {
            new Chart(usersChartCanvas, {
                type: 'doughnut',
                data: {
                    labels: ['Faol', 'Nofaol'],
                    datasets: [{
                        data: [75, 25],
                        backgroundColor: [
                            'rgb(67, 233, 123)',
                            'rgb(245, 87, 108)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }
}

// ===== ADMIN NOTIFICATIONS =====
function initAdminNotifications() {
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

function showAdminNotification(message, type = 'info', duration = 5000) {
    const container = document.querySelector('.admin-content') || document.body;
    const notification = document.createElement('div');
    
    const colors = {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
    };
    
    notification.className = `alert ${colors[type]} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, duration);
}

// ===== BULK ACTIONS =====
function initBulkActions() {
    const bulkActionSelect = document.getElementById('bulkAction');
    const bulkActionBtn = document.getElementById('bulkActionBtn');
    
    if (bulkActionSelect && bulkActionBtn) {
        bulkActionBtn.addEventListener('click', function() {
            const selectedAction = bulkActionSelect.value;
            const selectedRows = document.querySelectorAll('.row-checkbox:checked');
            
            if (!selectedAction) {
                showAdminNotification('Iltimos, amalni tanlang!', 'warning');
                return;
            }
            
            if (selectedRows.length === 0) {
                showAdminNotification('Iltimos, kamida bitta elementni tanlang!', 'warning');
                return;
            }
            
            if (confirm(`${selectedRows.length} ta element uchun "${selectedAction}" amalini bajarmoqchimisiz?`)) {
                // Perform bulk action
                const ids = Array.from(selectedRows).map(checkbox => checkbox.value);
                performBulkAction(selectedAction, ids);
            }
        });
    }
}

function updateBulkActions() {
    const selectedRows = document.querySelectorAll('.row-checkbox:checked');
    const bulkActionsContainer = document.getElementById('bulkActions');
    
    if (bulkActionsContainer) {
        if (selectedRows.length > 0) {
            bulkActionsContainer.style.display = 'block';
            bulkActionsContainer.querySelector('.selected-count').textContent = selectedRows.length;
        } else {
            bulkActionsContainer.style.display = 'none';
        }
    }
}

function performBulkAction(action, ids) {
    // This would typically make an AJAX request to perform the bulk action
    console.log(`Performing ${action} on items:`, ids);
    
    // Show loading state
    const bulkActionBtn = document.getElementById('bulkActionBtn');
    const originalText = bulkActionBtn.innerHTML;
    bulkActionBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Bajarilmoqda...';
    bulkActionBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        bulkActionBtn.innerHTML = originalText;
        bulkActionBtn.disabled = false;
        showAdminNotification(`${action} muvaffaqiyatli bajarildi!`, 'success');
        
        // Refresh page or update UI
        window.location.reload();
    }, 2000);
}

// ===== UTILITY FUNCTIONS =====

// Debounce function
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

// Format numbers
function formatNumber(num) {
    return new Intl.NumberFormat('uz-UZ').format(num);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('uz-UZ', {
        style: 'currency',
        currency: 'UZS'
    }).format(amount);
}

// Export data
function exportData(format, data) {
    if (format === 'csv') {
        exportToCSV(data);
    } else if (format === 'excel') {
        // Placeholder for exportToExcel function
        console.log('Excel export functionality is not implemented.');
    }
}

function exportToCSV(data) {
    const csv = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Search functionality
function initQuickSearch() {
    const searchInput = document.getElementById('quickSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('.admin-table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }, 300));
    }
}

// ===== REAL-TIME UPDATES =====
function initRealTimeUpdates() {
    // Check for updates every 30 seconds
    setInterval(() => {
        updateDashboardStats();
    }, 30000);
}

function updateDashboardStats() {
    // This would typically fetch updated stats from the server
    console.log('Updating dashboard stats...');
}

// Initialize real-time updates if on dashboard
if (window.location.pathname.includes('/admin/dashboard/')) {
    initRealTimeUpdates();
}

console.log('✅ Admin Panel JavaScript yuklandi!');

// Export functions for global use
window.AdminPanel = {
    showNotification: showAdminNotification,
    exportData,
    formatNumber,
    formatCurrency
};

// Placeholder for bootstrap variable declaration
const bootstrap = {
    Modal: {
        getInstance: function(modal) {
            // Placeholder for bootstrap Modal instance
            return {
                hide: function() {
                    modal.style.display = 'none';
                }
            };
        }
    }
};