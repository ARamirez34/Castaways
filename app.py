"""
Castaways Ice Cream Shop - Main Flask Application
================================================

A complete ice cream shop management system with:
- Customer homepage with ice cream showcase
- Admin dashboard with sales analytics and inventory management
- Automatic daily and monthly inventory resets
- Customer feedback system
- Secure authentication for admin access

Author: Ice Cream Shop Management System
Date: October 2025
"""

# ============================================================================
# IMPORTS AND DEPENDENCIES
# ============================================================================
from flask import Flask
from views import views
import sqlite3
import os


# ============================================================================
# DATABASE CONNECTION UTILITY
# ============================================================================
def get_db_connection():
    """
    Establishes connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection with Row factory for dict-like access
    """
    conn = sqlite3.connect("castawaysv2.db")  # Production database
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn


# ============================================================================
# FLASK APPLICATION SETUP
# ============================================================================
app = Flask(__name__)

# Security Configuration
# ----------------------
# Essential configurations for secure session management and admin authentication
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-only-change-me'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS attacks
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session timeout
app.config['SESSION_TYPE'] = 'filesystem'

# Blueprint Registration
# ----------------------
# Register all routes from views.py module
app.register_blueprint(views, url_prefix="/")


# ============================================================================
# APPLICATION STARTUP
# ============================================================================
if __name__ == '__main__':
    # Development server configuration
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=True, port=8000)