// InsightMatch2 Configuration

window.IM_CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:8000/api',
    BACKEND_URL: 'http://localhost:8000',
    
    // Feature Flags
    FEATURES: {
        AI_ANALYSIS: true,
        CONSULTANT_MATCHING: true,
        PDF_GENERATION: false, // Coming soon
        EMAIL_NOTIFICATIONS: false // Coming soon
    },
    
    // UI Configuration
    UI: {
        THEME: 'light',
        LANGUAGE: 'ko',
        ANIMATIONS: true
    },
    
    // Analysis Configuration
    ANALYSIS: {
        MAX_RISKS: 10,
        MAX_CERTIFICATIONS: 10,
        MAX_NEWS_ITEMS: 10,
        MAX_DART_ITEMS: 10
    },
    
    // Consultant Configuration
    CONSULTANTS: {
        ITEMS_PER_PAGE: 12,
        DEFAULT_FILTERS: {
            industry: '',
            certification: '',
            region: ''
        }
    }
};

// Environment-specific configuration
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Development environment
    window.IM_CONFIG.API_BASE_URL = 'http://localhost:8000/api';
    window.IM_CONFIG.BACKEND_URL = 'http://localhost:8000';
} else {
    // Production environment (Railway)
    window.IM_CONFIG.API_BASE_URL = 'https://your-railway-app.railway.app/api';
    window.IM_CONFIG.BACKEND_URL = 'https://your-railway-app.railway.app';
}
