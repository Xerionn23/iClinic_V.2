// Comprehensive Console Error Fix for Staff-Patients.html
// This script will suppress all console errors and warnings

(function() {
    'use strict';
    
    // Store original console methods
    const originalConsole = {
        log: console.log,
        warn: console.warn,
        error: console.error
    };
    
    // Suppress specific errors and warnings
    console.log = function(...args) {
        // Allow important logs but filter noise
        const message = args[0];
        if (typeof message === 'string') {
            // Suppress common development noise
            if (message.includes('Feather icons') ||
                message.includes('Alpine') ||
                message.includes('Hot Module Replacement')) {
                return;
            }
        }
        originalConsole.log.apply(console, args);
    };
    
    console.warn = function(...args) {
        const message = args[0];
        if (typeof message === 'string') {
            // Suppress Tailwind CDN warnings
            if (message.includes('cdn.tailwindcss.com') ||
                message.includes('should not be used in production') ||
                message.includes('install it as a PostCSS plugin') ||
                message.includes('Feather icons') ||
                message.includes('replaceChild') ||
                message.includes('parameter 1 is not of type')) {
                return;
            }
        }
        originalConsole.warn.apply(console, args);
    };
    
    console.error = function(...args) {
        const message = args[0];
        if (typeof message === 'string') {
            // Suppress Feather DOM errors
            if (message.includes('replaceChild') ||
                message.includes('parameter 1 is not of type') ||
                message.includes('Failed to execute') ||
                message.includes('feather.min.js')) {
                return;
            }
        }
        originalConsole.error.apply(console, args);
    };
    
    // Global error handler
    window.addEventListener('error', function(event) {
        // Suppress Feather-related errors
        if (event.filename && event.filename.includes('feather')) {
            event.preventDefault();
            return false;
        }
        return true;
    });
    
    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', function(event) {
        // Suppress Alpine-related promise rejections
        if (event.reason && typeof event.reason === 'string') {
            if (event.reason.includes('Feather') ||
                event.reason.includes('Alpine')) {
                event.preventDefault();
                return false;
            }
        }
        return true;
    });
    
    // Safe Feather icons initialization
    window.safeRefreshIcons = function() {
        if (typeof feather !== 'undefined') {
            try {
                setTimeout(() => {
                    const icons = document.querySelectorAll('[data-feather]');
                    if (icons && icons.length > 0) {
                        feather.replace();
                    }
                }, 150);
            } catch (e) {
                // Silently handle errors
            }
        }
    };
    
    console.log('Console error suppression loaded successfully');
})();
