// Show flash messages
function showFlashMessage(message, category = 'success') {
    const flashContainer = document.createElement('div');
    flashContainer.className = `alert alert-${category} alert-dismissible fade show`;
    flashContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(flashContainer, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(flashContainer);
        alert.close();
    }, 5000);
}

// Format date to YYYY-MM-DD
function formatDate(date) {
    if (!date) return '';
    
    try {
        // Если date строка - преобразуем в объект Date
        if (typeof date === 'string') {
            const dateObj = new Date(date);
            if (isNaN(dateObj.getTime())) {
                console.warn('Invalid date string:', date);
                return '';
            }
            return dateObj.toISOString().split('T')[0];
        } 
        // Если date уже объект Date
        else if (date instanceof Date) {
            return date.toISOString().split('T')[0];
        }
        
        return '';
    } catch (error) {
        console.error('Date formatting error:', error);
        return '';
    }
}

// Safe date formatter for any type of input
function safeFormatDate(dateInput) {
    if (!dateInput) return 'Не указана';
    
    try {
        // Если входные данные - строка
        if (typeof dateInput === 'string') {
            const date = new Date(dateInput);
            if (isNaN(date.getTime())) {
                console.warn('Некорректная дата:', dateInput);
                return 'Некорректная дата';
            }
            
            return date.toLocaleString('ru-RU', {
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } 
        // Если входные данные - объект Date
        else if (dateInput instanceof Date) {
            if (isNaN(dateInput.getTime())) {
                return 'Некорректная дата';
            }
            
            return dateInput.toLocaleString('ru-RU', {
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        return 'Неизвестный формат';
    } catch (error) {
        console.error('Ошибка при форматировании даты:', error, dateInput);
        return 'Ошибка даты';
    }
}

// Format number with 2 decimal places
function formatNumber(number) {
    return Number(number).toFixed(2);
}

// Handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    showFlashMessage('An error occurred. Please try again.', 'danger');
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Update active navigation link
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Initialize all tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize all popovers
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}); 