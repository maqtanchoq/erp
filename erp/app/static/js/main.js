// ===== MAIN JAVASCRIPT FILE =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Sanjarbek Online Do\'kon yuklandi!');
    
    // Initialize all functions
    initScrollEffects();
    initAnimations();
    initNotifications();
    initSearchEnhancements();
    initCartFunctionality();
    initProductInteractions();
    initFormEnhancements();
    initLoadingStates();
});

// ===== SCROLL EFFECTS =====
function initScrollEffects() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        }
    });
    
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Reveal animations on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .category-card, .stats-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// ===== ANIMATIONS =====
function initAnimations() {
    // Add floating animation to icons
    document.querySelectorAll('.category-icon, .stats-icon').forEach(icon => {
        icon.classList.add('float-animation');
    });
    
    // Stagger animation for product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fadeInUp');
    });
    
    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// ===== NOTIFICATIONS =====
function initNotifications() {
    // Create notification container
    if (!document.querySelector('.notification-container')) {
        const container = document.createElement('div');
        container.className = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }
    
    // Enhanced Django messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Add enhanced styling
        alert.style.borderRadius = '15px';
        alert.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
        alert.style.border = 'none';
        alert.style.backdropFilter = 'blur(10px)';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(400px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Show custom notification
function showNotification(message, type = 'success') {
    const container = document.querySelector('.notification-container');
    const notification = document.createElement('div');
    
    const colors = {
        success: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        error: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        warning: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        info: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };
    
    notification.style.cssText = `
        background: ${colors[type]};
        color: white;
        padding: 15px 25px;
        border-radius: 15px;
        margin-bottom: 10px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        transform: translateX(400px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: auto;
        font-weight: 600;
    `;
    
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        ${message}
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: white; float: right; font-size: 18px; cursor: pointer;">×</button>
    `;
    
    container.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-hide
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ===== SEARCH ENHANCEMENTS =====
function initSearchEnhancements() {
    const searchInputs = document.querySelectorAll('input[type="text"][name="q"]');
    
    searchInputs.forEach(input => {
        // Add search icon
        const container = document.createElement('div');
        container.className = 'search-container position-relative';
        input.parentNode.insertBefore(container, input);
        container.appendChild(input);
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-search search-icon';
        container.appendChild(icon);
        
        input.classList.add('search-input');
        input.placeholder = 'Mahsulotlarni qidiring...';
        
        // Add search suggestions (mock data)
        const suggestions = ['Telefon', 'Laptop', 'Kiyim', 'Kitob', 'Sport'];
        
        input.addEventListener('focus', function() {
            // You can add search suggestions dropdown here
            this.style.borderColor = '#667eea';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '#e9ecef';
        });
    });
}

// ===== CART FUNCTIONALITY =====
function initCartFunctionality() {
    // Add to cart animation
    const addToCartBtns = document.querySelectorAll('a[href*="add-to-cart"]');
    
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading-spinner"></span> Qo\'shilmoqda...';
            this.style.pointerEvents = 'none';
            
            // Simulate loading (remove this in production)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = 'auto';
                showNotification('Mahsulot savatchaga qo\'shildi!', 'success');
            }, 1000);
        });
    });
    
    // Cart item animations
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fadeInUp');
    });
}

// ===== PRODUCT INTERACTIONS =====
function initProductInteractions() {
    // Product card hover effects
    const productCards = document.querySelectorAll('.card');
    
    productCards.forEach(card => {
        const img = card.querySelector('.card-img-top');
        
        card.addEventListener('mouseenter', function() {
            if (img) {
                img.style.transform = 'scale(1.1)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (img) {
                img.style.transform = 'scale(1)';
            }
        });
    });
    
    // Product quick view (placeholder)
    const viewBtns = document.querySelectorAll('a[href*="product/"]');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Add loading effect
            this.innerHTML = '<span class="loading-spinner"></span> Yuklanmoqda...';
        });
    });
}

// ===== FORM ENHANCEMENTS =====
function initFormEnhancements() {
    // Add floating labels effect
    const formGroups = document.querySelectorAll('.mb-3');
    
    formGroups.forEach(group => {
        const input = group.querySelector('input, textarea, select');
        const label = group.querySelector('label');
        
        if (input && label) {
            input.addEventListener('focus', function() {
                label.style.color = '#667eea';
                label.style.transform = 'scale(0.9)';
            });
            
            input.addEventListener('blur', function() {
                label.style.color = '#6c757d';
                label.style.transform = 'scale(1)';
            });
        }
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading-spinner"></span> Yuborilmoqda...';
                submitBtn.disabled = true;
                
                // Re-enable after 3 seconds (adjust as needed)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });
}

// ===== LOADING STATES =====
function initLoadingStates() {
    // Page loading animation
    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    });
    
    // Link loading states
    const links = document.querySelectorAll('a:not([href^="#"]):not([href^="mailto"]):not([href^="tel"])');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.target !== '_blank') {
                // Add loading cursor
                document.body.style.cursor = 'wait';
                
                setTimeout(() => {
                    document.body.style.cursor = 'default';
                }, 2000);
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Format price with animation
function animatePrice(element, newPrice) {
    element.style.transform = 'scale(1.1)';
    element.style.color = '#43e97b';
    
    setTimeout(() => {
        element.textContent = newPrice;
        element.style.transform = 'scale(1)';
        element.style.color = '';
    }, 200);
}

// Copy to clipboard with notification
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Nusxalandi!', 'success');
    });
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl + K for search
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Esc to close modals/dropdowns
    if (e.key === 'Escape') {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }
});

// ===== PERFORMANCE OPTIMIZATIONS =====

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Debounce function for search
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

// ===== EXPORT FUNCTIONS FOR GLOBAL USE =====
window.SanjarbekShop = {
    showNotification,
    scrollToElement,
    animatePrice,
    copyToClipboard
};

console.log('✅ Sanjarbek Online Do\'kon JavaScript yuklandi!');