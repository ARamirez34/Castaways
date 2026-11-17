"""
Castaways Ice Cream Shop - Production Flask Application
======================================================

Production-ready configuration with proper security and deployment settings.
"""

import os
from flask import Flask
from views import views


def create_app():
    """Application factory for production deployment"""
    app = Flask(__name__)
    
    # ============================================================================
    # PRODUCTION SECURITY CONFIGURATION
    # ============================================================================
    
    # SECRET KEY - Must be set via environment variable in production
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        raise ValueError("SECRET_KEY environment variable must be set for production")
    
    # Session Security Configuration
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
    
    # ============================================================================
    # BLUEPRINT REGISTRATION
    # ============================================================================
    app.register_blueprint(views, url_prefix="/")
    
    return app


# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Development server - only for local testing
    # In production, this should be run via Gunicorn/WSGI server
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=port
    )