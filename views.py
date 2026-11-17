"""
Castaways Ice Cream Shop - View Controllers and Route Handlers
===========================================================

This module contains all the route handlers and business logic for the
Castaways Ice Cream Shop web application, including:

- Customer homepage and ice cream display
- Admin authentication and session management
- Sales analytics and chart data generation
- Inventory management and automatic resets
- Customer feedback system
- API endpoints for dynamic data

Author: Ice Cream Shop Management System
Date: October 2025
"""

# ============================================================================
# IMPORTS AND DEPENDENCIES  
# ============================================================================
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime, timedelta
import sqlite3
import os
import calendar
from functools import wraps

# ============================================================================
# BLUEPRINT CONFIGURATION
# ============================================================================
views = Blueprint("views", __name__)

# ============================================================================
# AUTHENTICATION AND SECURITY UTILITIES
# ============================================================================

def login_required(f):
    """
    Decorator to require admin login for protected routes.
    
    Redirects to login page if user is not authenticated in session.
    Used to protect admin dashboard, charts, tables, and other sensitive areas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# DATABASE UTILITY FUNCTIONS
# ============================================================================

def check_and_reset_monthly_data():
    """
    Monthly Reset System - Automatically resets sales data at start of new month.
    
    Checks if any inventory records are from a previous month and resets their
    amountSold counters to 0. This provides clean monthly sales reporting.
    
    Returns:
        str: Current month in YYYY-MM format
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    current_month_start = f"{current_month}-01"
    
    # Check if any record was last updated in a different month
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT last_updated FROM AddOns 
            UNION ALL 
            SELECT last_updated FROM Supplies 
            UNION ALL 
            SELECT last_updated FROM IceCreamInventory
        ) WHERE strftime('%Y-%m', last_updated) != ?
    """, (current_month,))
    
    records_from_old_month = cursor.fetchone()[0]
    
    if records_from_old_month > 0:
        # Reset all amountSold to 0 and update timestamps
        cursor.execute('UPDATE AddOns SET amountSold = 0, last_updated = ?', (current_month_start,))
        cursor.execute('UPDATE Supplies SET amountSold = 0, last_updated = ?', (current_month_start,))
        cursor.execute('UPDATE IceCreamInventory SET amountSold = 0, last_updated = ?', (current_month_start,))
        conn.commit()
    
    conn.close()
    return current_month


def auto_update_ice_cream_availability():
    """
    Automatic Availability Management - Updates ice cream availability status.
    
    Updates availability labels based on current stock levels:
    - Full: 5+ containers
    - Half: 2-4 containers  
    - Low: 1 container
    - Empty: 0 containers
    
    This ensures customers see accurate availability on the homepage.
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Define stock thresholds
    cursor.execute("""
        UPDATE IceCreamInventory 
        SET availability = CASE 
            WHEN currentStockAmount >= 5 THEN 'Full'
            WHEN currentStockAmount >= 2 THEN 'Half'
            WHEN currentStockAmount >= 1 THEN 'Low'
            ELSE 'Empty'
        END,
        last_updated = ?
    """, (datetime.now().strftime('%Y-%m-%d'),))
    
    conn.commit()
    conn.close()


def check_and_reset_daily_sales():
    """
    Daily Reset System - Automatically resets daily sales counters at midnight.
    
    Checks if it's a new day and resets the soldToday counter for all ice cream
    flavors. This enables accurate daily sales tracking for analytics.
    
    Returns:
        str: Current date in YYYY-MM-DD format
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Check if any record needs daily reset (different day than lastDailyReset)
    cursor.execute("""
        SELECT COUNT(*) FROM IceCreamInventory 
        WHERE lastDailyReset != ? OR lastDailyReset IS NULL
    """, (current_date,))
    
    records_need_reset = cursor.fetchone()[0]
    
    if records_need_reset > 0:
        print(f"🌙 Daily reset triggered for {records_need_reset} ice cream flavors")
        
        # Reset soldToday to 0 for all flavors and update lastDailyReset
        cursor.execute("""
            UPDATE IceCreamInventory 
            SET soldToday = 0, lastDailyReset = ?
        """, (current_date,))
        
        conn.commit()
        print(f"✅ Daily sales reset completed for {current_date}")
    
    conn.close()
    return current_date


# ============================================================================
# ADMIN UTILITY ROUTES
# ============================================================================
# These routes provide access to the various admin dashboard pages
@views.route("/buttons")
def buttons():
    return render_template("buttons.html")
 
@views.route("/cards")
def cards():
    return render_template("cards.html")

@views.route("/utilities-color.html")
def utilities_color():
    return render_template("utilities-color.html")

@views.route("/utilities-border.html")
def utilities_border():
    return render_template("utilities-border.html")

@views.route("/utilities-animation.html")
def utilities_animation():
    return render_template("utilities-animation.html")

@views.route("/utilities-other.html")
def utilities_other():
    return render_template("utilities-other.html")


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@views.route("/login", methods=["GET", "POST"])
def login():
    """
    Admin Login System with Security Features
    
    Provides secure authentication for admin access with:
    - Username/password validation (set via ADMIN_USERNAME / ADMIN_PASSWORD env vars)
    - Failed attempt tracking (max 5 attempts)
    - Temporary lockout (15 minutes after 5 failed attempts)
    - Session management and timeout
    """
    error = None
    attempts_remaining = 5
    locked_out = False
    lockout_time = 0
    
    # Use timezone-naive datetime consistently
    current_time = datetime.now()
    
    # Check if user is already logged in
    if 'user_logged_in' in session:
        return redirect(url_for('views.charts'))
    
    # Check if user is locked out
    if 'lockout_until' in session:
        lockout_until = session['lockout_until']
        
        # Convert string back to datetime if needed
        if isinstance(lockout_until, str):
            try:
                lockout_until = datetime.fromisoformat(lockout_until)
            except:
                # If parsing fails, clear the lockout
                session.pop('lockout_until', None)
                session.pop('login_attempts', None)
        
        # Ensure both datetimes are timezone-naive for comparison
        if hasattr(lockout_until, 'replace'):
            lockout_until = lockout_until.replace(tzinfo=None)
        
        if current_time < lockout_until:
            minutes_remaining = int((lockout_until - current_time).total_seconds() / 60) + 1
            return render_template('login.html', 
                                  locked_out=True, 
                                  lockout_time=minutes_remaining)
        else:
            # Lockout expired, reset attempts
            session.pop('lockout_until', None)
            session.pop('login_attempts', None)
    
    if 'login_attempts' not in session:
        session['login_attempts'] = 0
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"🔐 Login attempt received:")
        print(f"   Username: '{username}'")
        print(f"   Password length: {len(password) if password else 0}")
        
        # Authentication check
        if username == os.environ.get('ADMIN_USERNAME', 'admin') and password == os.environ.get('ADMIN_PASSWORD', 'demo'):
            # Successful login
            session.pop('login_attempts', None)
            session.pop('lockout_until', None)
            session['user_logged_in'] = True
            session['username'] = username
            session.permanent = True
            
            print(f"✅ Successful login for user: {username}")
            return redirect(url_for('views.charts'))
        else:
            # Failed login
            session['login_attempts'] = session.get('login_attempts', 0) + 1
            attempts_remaining = 5 - session['login_attempts']
            
            print(f"❌ Failed login attempt {session['login_attempts']}/5 for username: {username}")
            
            if session['login_attempts'] >= 5:
                # Store lockout time as ISO string to avoid timezone issues
                lockout_until = current_time + timedelta(minutes=15)
                session['lockout_until'] = lockout_until.isoformat()
                locked_out = True
                lockout_time = 15
                error = "🔒 Too many failed login attempts. Account temporarily locked for 15 minutes."
                print(f"🔒 Account locked until: {lockout_until}")
            else:
                error = f"❌ Invalid username or password. {attempts_remaining} attempts remaining."
    
    return render_template('login.html', 
                          error=error, 
                          attempts_remaining=attempts_remaining,
                          locked_out=locked_out,
                          lockout_time=lockout_time)

# Redirect /login.html to /login for consistency
@views.route('/login.html', methods=["GET", "POST"])
def login_html_redirect():
    return redirect(url_for('views.login'))

@views.route('/logout')
def logout():
    session.clear()
    print("👋 User logged out")
    return redirect(url_for('views.login'))

@views.route('/clear_session')
def clear_session():
    """Debug route to clear session data"""
    session.clear()
    print("🧹 Session cleared for debugging")
    return redirect(url_for('views.login'))

@views.route("/register.html")
def register():
    return render_template("register.html")

@views.route("/forgot-password.html")
def forgot_password():
    return render_template("forgot-password.html")

@views.route("/404.html")
def page_not_found():
    return render_template("404.html")

@views.route("/blank.html")
def blank():
    return render_template("blank.html")


# ============================================================================
# ANALYTICS AND DASHBOARD ROUTES
# ============================================================================

@views.route("/charts")
@login_required
def charts():
    """
    Admin Analytics Dashboard - Sales Charts and Performance Metrics
    
    Displays comprehensive sales analytics including:
    - Monthly sales data with automatic resets
    - Inventory levels by category (Ice Cream, AddOns, Supplies)
    - Top selling items across all categories
    - Ice cream availability status distribution
    - Current month sales performance
    """
    # Check and reset data if we're in a new month
    current_month = check_and_reset_monthly_data()
    # Auto-update ice cream availability based on stock levels
    auto_update_ice_cream_availability()
    current_month_display = datetime.now().strftime('%B %Y')  # e.g., "September 2025"
    
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Get sales data for charts (current month only)
    charts_data = {}
    
    # Total inventory by category (using current stock levels)
    categories = {}
    
    # AddOns and Supplies use boxCount
    for table in ['AddOns', 'Supplies']:
        cur = conn.execute(f"SELECT SUM(boxCount) as total FROM {table}")
        result = cur.fetchone()
        categories[table] = result['total'] if result['total'] else 0
    
    # IceCreamInventory uses currentStockAmount
    cur = conn.execute("SELECT SUM(currentStockAmount) as total FROM IceCreamInventory")
    result = cur.fetchone()
    categories['IceCreamInventory'] = result['total'] if result['total'] else 0
    
    # Top selling items across all categories (current month)
    top_items = []
    
    # Get top AddOns for current month
    cur = conn.execute(f"SELECT name, amountSold FROM AddOns WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['name'], 'sold': row['amountSold'], 'category': 'AddOns'})
    
    # Get top Supplies for current month
    cur = conn.execute(f"SELECT item, amountSold FROM Supplies WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['item'], 'sold': row['amountSold'], 'category': 'Supplies'})
    
    # Get top Ice Cream for current month
    cur = conn.execute(f"SELECT flavor, amountSold FROM IceCreamInventory WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['flavor'], 'sold': row['amountSold'], 'category': 'IceCreamInventory'})
    
    # Sort top items by sales
    top_items.sort(key=lambda x: x['sold'], reverse=True)
    top_items = top_items[:10]  # Top 10 items
    
    # Count of flavors by availability status (Ice Cream only)
    cur = conn.execute("SELECT availability, COUNT(*) as count FROM IceCreamInventory GROUP BY availability")
    availability_sales = {}
    for row in cur.fetchall():
        availability_sales[row['availability']] = row['count'] if row['count'] else 0
    
    # Individual table data for detailed charts (current month)
    individual_data = {}
    
    # AddOns detailed data
    cur = conn.execute(f"SELECT name, amountSold FROM AddOns ORDER BY amountSold DESC")
    individual_data['addons'] = [{'name': row['name'], 'sold': row['amountSold']} for row in cur.fetchall()]
    
    # Supplies detailed data
    cur = conn.execute(f"SELECT item, size, amountSold FROM Supplies ORDER BY amountSold DESC")
    supplies_items = []
    for row in cur.fetchall():
        name = row['item'] + (f" ({row['size']})" if row['size'] else "")
        supplies_items.append({'name': name, 'sold': row['amountSold']})
    individual_data['supplies'] = supplies_items
    
    # Ice Cream detailed data
    cur = conn.execute(f"SELECT flavor, amountSold FROM IceCreamInventory ORDER BY amountSold DESC")
    individual_data['icecream'] = [{'name': row['flavor'], 'sold': row['amountSold']} for row in cur.fetchall()]
    
    charts_data = {
        'categories': categories,
        'top_items': top_items,
        'availability_sales': availability_sales,
        'individual_data': individual_data,
        'current_month': current_month,
        'current_month_display': current_month_display
    }
    
    conn.close()
    return render_template("charts.html", charts_data=charts_data)


# ============================================================================
# API ENDPOINTS FOR DYNAMIC DATA
# ============================================================================

@views.route("/api/chart_data")
def chart_data():
    """
    Chart Data API - Returns current inventory and sales data as JSON
    
    Provides real-time data for dashboard charts including:
    - Current inventory levels by category
    - Top selling items
    - Ice cream availability distribution
    
    Used for dynamic chart updates without page refresh.
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Get inventory data for charts (same logic as charts route)
    categories = {}
    
    # AddOns and Supplies use boxCount
    for table in ['AddOns', 'Supplies']:
        cur = conn.execute(f"SELECT SUM(boxCount) as total FROM {table}")
        result = cur.fetchone()
        categories[table] = result['total'] if result['total'] else 0
    
    # IceCreamInventory uses currentStockAmount
    cur = conn.execute("SELECT SUM(currentStockAmount) as total FROM IceCreamInventory")
    result = cur.fetchone()
    categories['IceCreamInventory'] = result['total'] if result['total'] else 0
    
    # Top selling items across all categories
    top_items = []
    
    # Get top AddOns
    cur = conn.execute("SELECT name, amountSold FROM AddOns WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['name'], 'sold': row['amountSold'], 'category': 'AddOns'})
    
    # Get top Supplies
    cur = conn.execute("SELECT item, amountSold FROM Supplies WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['item'], 'sold': row['amountSold'], 'category': 'Supplies'})
    
    # Get top Ice Cream
    cur = conn.execute("SELECT flavor, amountSold FROM IceCreamInventory WHERE amountSold > 0 ORDER BY amountSold DESC LIMIT 5")
    for row in cur.fetchall():
        top_items.append({'name': row['flavor'], 'sold': row['amountSold'], 'category': 'IceCreamInventory'})
    
    # Sort top items by sales
    top_items.sort(key=lambda x: x['sold'], reverse=True)
    top_items = top_items[:10]  # Top 10 items
    
    # Count of flavors by availability status (Ice Cream only)
    cur = conn.execute("SELECT availability, COUNT(*) as count FROM IceCreamInventory GROUP BY availability")
    availability_sales = {}
    for row in cur.fetchall():
        availability_sales[row['availability']] = row['count'] if row['count'] else 0
    
    charts_data = {
        'categories': categories,
        'top_items': top_items,
        'availability_sales': availability_sales
    }
    
    conn.close()
    return jsonify(charts_data)

@views.route("/api/historical_chart_data")
def historical_chart_data():
    """API endpoint to get historical chart data (September 2025 simulation)"""
    # Since we don't have actual historical data, we'll simulate September 2025 data
    # In a real application, this would query historical tables or archived data
    
    # Simulated historical data for September 2025
    historical_data = {
        'categories': {
            'AddOns': 45,      # Slightly different from current
            'Supplies': 38,
            'IceCreamInventory': 156
        },
        'top_items': [
            {'name': 'Coconut', 'sold': 28, 'category': 'IceCreamInventory'},
            {'name': 'Vanilla', 'sold': 22, 'category': 'IceCreamInventory'},
            {'name': 'Chocolate Chip Cookies', 'sold': 21, 'category': 'IceCreamInventory'},
            {'name': 'Cereal', 'sold': 19, 'category': 'AddOns'},
            {'name': 'Mango', 'sold': 18, 'category': 'IceCreamInventory'},
            {'name': 'Cup (Large)', 'sold': 15, 'category': 'Supplies'},
            {'name': 'Sprinkles', 'sold': 14, 'category': 'AddOns'},
            {'name': 'Bowl', 'sold': 13, 'category': 'Supplies'},
            {'name': 'Pandan w/ Coconut', 'sold': 12, 'category': 'IceCreamInventory'},
            {'name': 'Hot Fudge', 'sold': 10, 'category': 'AddOns'}
        ],
        'availability_sales': {
            'Full': 85,
            'Half': 45,
            'Low': 26
        },
        'individual_data': {
            'addons': [
                {'name': 'Cereal', 'sold': 19},
                {'name': 'Sprinkles', 'sold': 14},
                {'name': 'Hot Fudge', 'sold': 10},
                {'name': 'Chocolate Sprinkles', 'sold': 2},
                {'name': 'Caramel', 'sold': 0}
            ],
            'supplies': [
                {'name': 'Cup (Large)', 'sold': 15},
                {'name': 'Bowl', 'sold': 13},
                {'name': 'Cup (Small)', 'sold': 8},
                {'name': 'Cup (Keiki)', 'sold': 2},
                {'name': 'Cone', 'sold': 0}
            ],
            'icecream': [
                {'name': 'Coconut', 'sold': 28},
                {'name': 'Vanilla', 'sold': 22},
                {'name': 'Chocolate Chip Cookies', 'sold': 21},
                {'name': 'Mango', 'sold': 18},
                {'name': 'Pandan w/ Coconut', 'sold': 12},
                {'name': 'Vanilla Bean', 'sold': 11},
                {'name': 'Biscoff Butter Cookies', 'sold': 9},
                {'name': 'Strawberry', 'sold': 8},
                {'name': 'Cherry w/ Chocolate Chip', 'sold': 7},
                {'name': 'Cookies Galore', 'sold': 0}
            ]
        },
        'current_month': 'September',
        'current_month_display': 'September 2025'
    }
    
    return jsonify(historical_data)

@views.route("/api/ice_cream_availability")
def ice_cream_availability():
    """API endpoint to get real-time ice cream availability for customers"""
    # Check for daily reset (at midnight) before updating availability
    check_and_reset_daily_sales()
    # Auto-update availability before returning data
    auto_update_ice_cream_availability()
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Get only available ice cream flavors (exclude Empty ones) - now with soldToday
    cur = conn.execute("""
        SELECT flavor, availability, currentStockAmount, amountSold, soldToday 
        FROM IceCreamInventory 
        WHERE availability != 'Empty' AND currentStockAmount > 0
        ORDER BY soldToday DESC, flavor ASC
    """)
    
    flavors = []
    for row in cur.fetchall():
        # Determine status based on availability (no need to check for Empty since we filtered it out)
        if row['availability'] == 'Full':
            status = 'available'
            status_text = 'In Stock'
            badge_class = 'success'
        elif row['availability'] == 'Half':
            status = 'limited'
            status_text = 'Limited'
            badge_class = 'warning'
        elif row['availability'] == 'Low':
            status = 'low'
            status_text = 'Running Low'
            badge_class = 'danger'
        else:
            # Fallback (shouldn't happen due to filtering)
            continue
        
        # Determine if it's trending (has daily sales today)
        is_trending = (row['soldToday'] or 0) > 0
        
        flavors.append({
            'name': row['flavor'],
            'availability': row['availability'],
            'stock': row['currentStockAmount'],
            'sold_today': row['soldToday'] or 0,  # Use daily sales for display
            'monthly_sold': row['amountSold'] or 0,  # Keep monthly for analytics
            'status': status,
            'status_text': status_text,
            'badge_class': badge_class,
            'is_trending': is_trending
        })
    
    conn.close()
    
    # Separate trending and regular flavors
    trending_flavors = [f for f in flavors if f['is_trending']]
    regular_flavors = [f for f in flavors if not f['is_trending']]
    
    return jsonify({
        'trending_flavors': trending_flavors[:6],  # Top 6 trending
        'all_flavors': flavors,
        'total_flavors': len(flavors),
        'available_count': len([f for f in flavors if f['status'] == 'available']),
        'limited_count': len([f for f in flavors if f['status'] == 'limited']),
        'low_count': len([f for f in flavors if f['status'] == 'low']),
        'out_of_stock_count': len([f for f in flavors if f['status'] == 'unavailable'])
    })

@views.route("/tables")
@login_required
def tables():
    """
    Admin Data Tables - View and manage all database records
    
    Displays comprehensive inventory and employee data in sortable tables.
    Provides admin interface for viewing all database contents.
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Specify the desired order
    table_order = ["AddOns", "Supplies", "IceCreamInventory", "Employees"]
    tables_data = {}
    for table in table_order:
        # Include ROWID so we can still identify rows for editing/deleting
        cur = conn.execute(f"SELECT ROWID, * FROM {table}")
        tables_data[table] = cur.fetchall()
    conn.close()
    # Pass the order as well for template rendering
    return render_template("tables.html", tables=tables_data, table_order=table_order)


# ============================================================================
# CUSTOMER-FACING ROUTES
# ============================================================================

@views.route("/")
def home():
    """
    Customer Homepage - Ice Cream Showcase and Availability
    
    Displays the main customer-facing page with:
    - Trending ice cream flavors (based on daily sales)
    - Real-time availability status
    - Automatic daily reset functionality
    - Live stock level indicators
    """
    # Check for daily reset first (at midnight)
    check_and_reset_daily_sales()
    # Auto-update availability before displaying
    auto_update_ice_cream_availability()
    # Get ice cream data for display
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Get trending flavors (ones with daily sales AND still available)
    cur = conn.execute("""
        SELECT flavor, availability, currentStockAmount, amountSold, soldToday 
        FROM IceCreamInventory 
        WHERE soldToday > 0 AND availability != 'Empty' AND currentStockAmount > 0
        ORDER BY soldToday DESC 
        LIMIT 6
    """)
    
    trending_flavors = []
    for row in cur.fetchall():
        status_info = get_availability_status(row['availability'])
        trending_flavors.append({
            'name': row['flavor'],
            'sold_today': row['soldToday'],  # Use daily sales for trending display
            'availability': row['availability'],
            'status_text': status_info['text'],
            'badge_class': status_info['badge']
        })
    
    # Get all available flavors count (exclude Empty and Out of Stock)
    cur = conn.execute("SELECT COUNT(*) as count FROM IceCreamInventory WHERE availability NOT IN ('Empty', 'Out') AND currentStockAmount > 0")
    available_count = cur.fetchone()['count']
    
    conn.close()
    
    return render_template("index.html", 
                         trending_flavors=trending_flavors,
                         available_count=available_count)

def get_availability_status(availability):
    """Helper function to get status info"""
    if availability == 'Full':
        return {'text': 'In Stock', 'badge': 'success'}
    elif availability == 'Half':
        return {'text': 'Limited', 'badge': 'warning'}
    elif availability == 'Low':
        return {'text': 'Running Low', 'badge': 'danger'}
    elif availability == 'Empty':
        return {'text': 'Out of Stock', 'badge': 'secondary'}
    else:
        return {'text': 'Out of Stock', 'badge': 'secondary'}

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Route to serve ADMIN.html when /ADMIN is accessed
# ============================================================================
# ADMIN DASHBOARD ROUTES  
# ============================================================================

@views.route("/ADMIN")
def admin():
    # Load latest feedback entries and compute unread count if feedback table exists.
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    feedback = []
    unread_count = 0
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
            if cur.fetchone():
                # Try to fetch recent messages and compute unread_count using common column names
                cur.execute("PRAGMA table_info(feedback)")
                cols = [r[1] for r in cur.fetchall()]
                # Prefer an 'unread' column if present
                if 'unread' in cols:
                    cur.execute("SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10")
                    rows = cur.fetchall()
                    feedback = rows
                    unread_count = sum(1 for r in rows if r['unread'])
                elif 'is_read' in cols or 'read' in cols or 'read_flag' in cols:
                    # treat truthy 'is_read'/'read' as 1 = read, so unread where is_read = 0
                    read_col = 'is_read' if 'is_read' in cols else ('read' if 'read' in cols else 'read_flag')
                    cur.execute(f"SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10")
                    rows = cur.fetchall()
                    feedback = rows
                    unread_count = sum(1 for r in rows if not r[read_col])
                else:
                    # No explicit read-flag, just fetch recent items and count them as unread
                    cur.execute("SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10")
                    rows = cur.fetchall()
                    feedback = rows
                    unread_count = len(rows)
            conn.close()
        except Exception:
            # On any DB error, fall back to safe defaults
            feedback = []
            unread_count = 0

    return render_template("ADMIN.html", unread_count=unread_count, feedback=feedback)


# ============================================================================
# CUSTOMER FEEDBACK SYSTEM
# ============================================================================

@views.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """
    Customer Feedback Submission Handler
    
    Processes feedback form data and saves to database with comprehensive
    error handling and validation.
    """
    # Accept form fields and persist into castawaysv2.db
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Debug logging
    print(f"📝 Feedback submission received:")
    print(f"   Name: '{name}'")
    print(f"   Email: '{email}'")
    print(f"   Message: '{message}'")
    
    # Validate required fields
    if not name or not email or not message:
        print(f"❌ Missing required fields - Name: {bool(name)}, Email: {bool(email)}, Message: {bool(message)}")
        return redirect(url_for('views.home') + '?error=1')

    # Simplified error handling - let's see what the real issue is
    try:
        # Test database connection first
        db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
        print(f"🔍 Attempting to connect to database at: {db_path}")
        
        conn = sqlite3.connect(db_path, timeout=30)  # Add timeout
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Insert the feedback (note: phone field not in database, so we skip it)
        print(f"📝 Inserting feedback into database...")
        cur.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
                    (name, email, message))
        conn.commit()
        print(f"✅ Database commit successful")
        conn.close()
        
        print(f"✅ Feedback saved successfully for {name}")
        
        # Redirect to home with success message
        return redirect(url_for('views.home') + '?success=1')
        
    except sqlite3.DatabaseError as db_err:
        print(f"❌ SQLite Database error: {db_err}")
        return redirect(url_for('views.home') + '?error=1')
    except Exception as e:
        print(f"❌ General error saving feedback: {e}")
        print(f"   Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('views.home') + '?error=1')


@views.route('/test_feedback', methods=['POST'])
def test_feedback():
    """Temporary debug route to see what form data is being sent"""
    print("🔍 DEBUG - Raw form data received:")
    for key, value in request.form.items():
        print(f"   {key}: '{value}'")
    print(f"   Content-Type: {request.content_type}")
    print(f"   Method: {request.method}")
    return f"Form data received: {dict(request.form)}"


# Endpoint used by ADMIN page to mark a feedback row as read.
# The ADMIN template expects url_for('views.mark_feedback_read') to exist.
@views.route('/mark_feedback_read', methods=['POST'])
def mark_feedback_read():
    """Mark a feedback entry as read.

    Accepts JSON body or form data with an `id` (or `feedback_id`).
    Tries to update a sensible boolean/flag column if the `feedback` table
    exists and contains a known column (e.g. 'read', 'is_read', 'seen').
    Returns 204 on success or if there's nothing to update, 400 for bad input,
    and 500 for unexpected errors.
    """
    try:
        data = request.get_json(silent=True) or request.form
        fid = None
        if isinstance(data, dict):
            fid = data.get('id') or data.get('feedback_id')
        else:
            # werkzeug ImmutableMultiDict -> behave like mapping
            fid = data.get('id') or data.get('feedback_id')

        if not fid:
            return (jsonify({'error': 'missing id'}), 400)

        db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
        if not os.path.exists(db_path):
            # Nothing to update - but return success so the frontend doesn't fail.
            return ('', 204)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Ensure table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
        if not cur.fetchone():
            conn.close()
            return ('', 204)

        # Inspect columns to find a plausible read flag
        cur.execute("PRAGMA table_info(feedback)")
        cols = [r[1] for r in cur.fetchall()]
        flag_col = None
        for candidate in ('read', 'is_read', 'seen', 'unread', 'read_flag'):
            if candidate in cols:
                flag_col = candidate
                break

        if flag_col:
            # If the column looks like 'unread' invert semantics: set to 0 to mark read
            if flag_col == 'unread':
                cur.execute(f"UPDATE feedback SET {flag_col}=0 WHERE id = ?", (fid,))
            else:
                cur.execute(f"UPDATE feedback SET {flag_col}=1 WHERE id = ?", (fid,))
            conn.commit()

        conn.close()
        return ('', 204)
    except Exception as e:
        # Return error to aid debugging in dev; in production you'd log and hide details
        return (jsonify({'error': str(e)}), 500)


@views.route('/all_feedback')
def all_feedback():
    """Admin listing of all feedback entries. Renders templates/all_feedback.html.

    If the feedback table or DB don't exist, the template will be rendered with an
    empty list.
    """
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    feedback = []
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
            if cur.fetchone():
                cur.execute("SELECT id, name, email, message, created_at, is_read FROM feedback ORDER BY created_at DESC")
                feedback = cur.fetchall()
            conn.close()
        except Exception:
            feedback = []

    return render_template('all_feedback.html', feedback=feedback)


@views.route('/mark_all_feedback_read', methods=['POST'])
def mark_all_feedback_read():
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    try:
        if not os.path.exists(db_path):
            return ('', 204)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
        if not cur.fetchone():
            conn.close()
            return ('', 204)
        # Update all feedback rows to mark them read
        cur.execute("UPDATE feedback SET unread = 0 WHERE unread != 0")
        conn.commit()
        conn.close()
        return ('', 204)
    except Exception:
        return ('', 500)


@views.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete a specific feedback entry by ID"""
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    try:
        if not os.path.exists(db_path):
            return redirect(url_for('views.all_feedback'))
            
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Delete the specific feedback entry
        cur.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('views.all_feedback'))
    except Exception:
        return redirect(url_for('views.all_feedback'))


# CRUD routes for Tables management (Updated for tables without ID columns)
@views.route('/add_table_entry/<table_name>', methods=['POST'])
def add_table_entry(table_name):
    """Add a new entry to the specified table"""
    if table_name not in ["AddOns", "Supplies", "IceCreamInventory", "Employees"]:
        return redirect(url_for('views.tables'))
    
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        if table_name == "AddOns":
            name = request.form.get('name')
            boxCount = request.form.get('boxCount')
            amountSold = request.form.get('amountSold')
            cur.execute("INSERT INTO AddOns (name, boxCount, amountSold) VALUES (?, ?, ?)", (name, boxCount, amountSold))
            
        elif table_name == "Supplies":
            item = request.form.get('item')
            size = request.form.get('size') or ''
            type_val = request.form.get('type')
            boxCount = request.form.get('boxCount')
            amountSold = request.form.get('amountSold')
            cur.execute("INSERT INTO Supplies (item, size, type, boxCount, amountSold) VALUES (?, ?, ?, ?, ?)", 
                       (item, size, type_val, boxCount, amountSold))
            
        elif table_name == "IceCreamInventory":
            flavor = request.form.get('flavor')
            currentStockAmount_str = request.form.get('currentStockAmount')
            amountSold_str = request.form.get('amountSold')
            
            # Convert strings to integers with validation
            try:
                currentStockAmount = int(currentStockAmount_str) if currentStockAmount_str else 0
                amountSold = int(amountSold_str) if amountSold_str else 0
            except ValueError as e:
                print(f"❌ Error converting numeric values: {e}")
                raise
            
            # Set temporary availability (will be auto-updated immediately)
            availability = 'Empty'  # Temporary value
            
            cur.execute("INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold) VALUES (?, ?, ?, ?)",
                       (flavor, availability, currentStockAmount, amountSold))
            
            # Auto-update availability for ALL flavors using same connection
            print("🔄 Running auto-update availability after insert...")
            cur.execute("""
                UPDATE IceCreamInventory 
                SET availability = CASE 
                    WHEN currentStockAmount >= 5 THEN 'Full'
                    WHEN currentStockAmount >= 2 THEN 'Half'
                    WHEN currentStockAmount >= 1 THEN 'Low'
                    ELSE 'Empty'
                END
            """)
            print(f"Auto-update affected {cur.rowcount} rows")
            
        elif table_name == "Employees":
            name = request.form.get('name')
            phone = request.form.get('phone') or ''
            email = request.form.get('email') or ''
            role = request.form.get('role')
            cur.execute("INSERT INTO Employees (name, phone, email, role) VALUES (?, ?, ?, ?)",
                       (name, phone, email, role))
        
        conn.commit()
        conn.close()
        print(f"✅ Successfully added new {table_name} entry")
    except Exception as e:
        print(f"❌ Error adding {table_name} entry: {e}")
        if 'conn' in locals():
            conn.close()
    
    return redirect(url_for('views.tables'))


@views.route('/edit_table_entry/<table_name>/<int:row_id>', methods=['POST'])
def edit_table_entry(table_name, row_id):
    """Edit an existing entry using ROWID (SQLite's internal row identifier)"""
    if table_name not in ["AddOns", "Supplies", "IceCreamInventory", "Employees"]:
        return redirect(url_for('views.tables'))
    
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Get current timestamp for last_updated
        current_timestamp = datetime.now().strftime('%Y-%m-%d')
        
        if table_name == "AddOns":
            name = request.form.get('name')
            boxCount_str = request.form.get('boxCount')
            amountSold_str = request.form.get('amountSold')
            
            # Convert to integers with validation
            try:
                boxCount = int(boxCount_str) if boxCount_str else 0
                amountSold = int(amountSold_str) if amountSold_str else 0
            except ValueError as e:
                print(f"❌ Error converting AddOns numeric values: {e}")
                raise
                
            cur.execute("UPDATE AddOns SET name = ?, boxCount = ?, amountSold = ?, last_updated = ? WHERE ROWID = ?", 
                       (name, boxCount, amountSold, current_timestamp, row_id))
            
        elif table_name == "Supplies":
            item = request.form.get('item')
            size = request.form.get('size') or ''
            type_val = request.form.get('type')
            boxCount_str = request.form.get('boxCount')
            amountSold_str = request.form.get('amountSold')
            
            # Convert to integers with validation
            try:
                boxCount = int(boxCount_str) if boxCount_str else 0
                amountSold = int(amountSold_str) if amountSold_str else 0
            except ValueError as e:
                print(f"❌ Error converting Supplies numeric values: {e}")
                raise
                
            cur.execute("UPDATE Supplies SET item = ?, size = ?, type = ?, boxCount = ?, amountSold = ?, last_updated = ? WHERE ROWID = ?", 
                       (item, size, type_val, boxCount, amountSold, current_timestamp, row_id))
            
        elif table_name == "IceCreamInventory":
            flavor = request.form.get('flavor')
            currentStockAmount_str = request.form.get('currentStockAmount')
            amountSold_str = request.form.get('amountSold')
            
            # Debug logging
            print(f"🔍 Form data received for {table_name} ROWID {row_id}:")
            print(f"  flavor: {flavor}")
            print(f"  currentStockAmount: {currentStockAmount_str}")
            print(f"  amountSold: {amountSold_str}")
            
            # Convert strings to integers with validation
            try:
                currentStockAmount = int(currentStockAmount_str) if currentStockAmount_str else 0
                new_amountSold = int(amountSold_str) if amountSold_str else 0
            except ValueError as e:
                print(f"❌ Error converting numeric values: {e}")
                raise
            
            # Get current values to calculate the difference for daily tracking
            cur.execute("SELECT amountSold, soldToday FROM IceCreamInventory WHERE ROWID = ?", (row_id,))
            current_data = cur.fetchone()
            old_amountSold = current_data[0] if current_data and current_data[0] else 0
            current_soldToday = current_data[1] if current_data and current_data[1] else 0
            
            # Calculate the difference (how much was actually sold since last update)
            sales_difference = new_amountSold - old_amountSold
            
            # Add the difference to soldToday (represents new sales today)
            new_soldToday = max(0, current_soldToday + sales_difference)
            
            print(f"📈 Sales update for {flavor}:")
            print(f"  Monthly: {old_amountSold} → {new_amountSold} (+{sales_difference})")
            print(f"  Daily: {current_soldToday} → {new_soldToday}")
            
            # Update with both monthly and daily sales tracking
            cur.execute("""
                UPDATE IceCreamInventory 
                SET flavor = ?, currentStockAmount = ?, amountSold = ?, soldToday = ?, last_updated = ? 
                WHERE ROWID = ?
            """, (flavor, currentStockAmount, new_amountSold, new_soldToday, current_timestamp, row_id))
            
            # Auto-update availability for ALL flavors using same connection
            print("🔄 Running auto-update availability on same connection...")
            cur.execute("""
                UPDATE IceCreamInventory 
                SET availability = CASE 
                    WHEN currentStockAmount >= 5 THEN 'Full'
                    WHEN currentStockAmount >= 2 THEN 'Half'
                    WHEN currentStockAmount >= 1 THEN 'Low'
                    ELSE 'Empty'
                END
            """)
            print(f"Auto-update affected {cur.rowcount} rows")
            
        elif table_name == "Employees":
            name = request.form.get('name')
            phone = request.form.get('phone') or ''
            email = request.form.get('email') or ''
            role = request.form.get('role')
            cur.execute("UPDATE Employees SET name = ?, phone = ?, email = ?, role = ? WHERE ROWID = ?",
                       (name, phone, email, role, row_id))
        
        conn.commit()
        conn.close()
        print(f"✅ Successfully updated {table_name} entry with ROWID {row_id}")
    except Exception as e:
        print(f"❌ Error updating {table_name} entry with ROWID {row_id}: {e}")
        if 'conn' in locals():
            conn.close()
    
    return redirect(url_for('views.tables'))


@views.route('/delete_table_entry/<table_name>/<int:row_id>', methods=['POST'])
def delete_table_entry(table_name, row_id):
    """Delete an entry using ROWID (SQLite's internal row identifier)"""
    if table_name not in ["AddOns", "Supplies", "IceCreamInventory", "Employees"]:
        return redirect(url_for('views.tables'))
    
    db_path = os.path.join(os.path.dirname(__file__), 'castawaysv2.db')
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name} WHERE ROWID = ?", (row_id,))
        conn.commit()
        conn.close()
        print(f"✅ Successfully deleted {table_name} entry with ROWID {row_id}")
    except Exception as e:
        print(f"❌ Error deleting {table_name} entry with ROWID {row_id}: {e}")
        if 'conn' in locals():
            conn.close()
    
    return redirect(url_for('views.tables'))



