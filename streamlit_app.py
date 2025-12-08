"""
Multi Cloud Infrastructure Intelligence Platform (MCIP) - Enterprise Multi-Account Cloud Management
Simple Blue Theme - Clean & Professional
WITH AZURE SSO AUTHENTICATION + FIREBASE REALTIME DATABASE
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# ==================================================================================
# AUTHENTICATION - MUST BE FIRST
# ==================================================================================
try:
    from auth_azure_sso import render_login, RoleManager  # FIXED: Use correct imports
    from auth_database_firebase import get_database_manager  # FIXED: Firebase not Firestore
    
    AUTH_ENABLED = True
except ImportError as e:
    AUTH_ENABLED = False
    print(f"Authentication modules not found: {e}")
    print("Running in legacy mode without authentication")

# ==================================================================================
# PAGE CONFIGURATION - BEFORE ANY ST COMMANDS
# ==================================================================================
st.set_page_config(
    page_title="Multi Cloud Infrastructure Intelligence Platform (MCIP)",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================================================
# INITIALIZE AUTHENTICATION (IF ENABLED)
# ==================================================================================
if AUTH_ENABLED:
    # Check if user is authenticated
    if not st.session_state.get('authenticated', False):
        # Show login page and stop
        render_login()
        st.stop()
    
    # User is authenticated - get user info
    current_user = st.session_state.get('user_info')
    
    # If authenticated but no user_info, something went wrong - show login again
    if not current_user:
        st.warning("⚠️ Session incomplete. Please login again.")
        st.session_state.authenticated = False
        render_login()
        st.stop()
    
    db_manager = get_database_manager()
    
    # Initialize role manager
    if 'role_manager' not in st.session_state:
        st.session_state.role_manager = RoleManager()
    
    # Set default cloud provider
    if 'cloud_provider' not in st.session_state:
        st.session_state.cloud_provider = 'AWS'
else:
    # No authentication - set defaults
    current_user = None
    db_manager = None

# ==================================================================================
# IMPORT APPLICATION MODULES
# ==================================================================================
from config_settings import AppConfig
from core_session_manager import SessionManager
from components_navigation import Navigation
from components_sidebar import GlobalSidebar

# ==================================================================================
# SIMPLE BLUE THEME - CLEAN & PROFESSIONAL
# ==================================================================================
st.markdown("""
<style>
/* ===== GLOBAL THEME ===== */
:root {
    --primary-color: #2E86DE;
    --secondary-color: #0652DD;
    --background-color: #FFFFFF;
    --text-color: #000000;
    --border-color: #E0E0E0;
}

/* Main app background - WHITE */
.main {
    background-color: white !important;
}

/* All text - BLACK */
body, p, span, div, label, h2, h3, h4, h5, h6 {
    color: black !important;
}

/* Main content h1 only - not header */
.main h1:not(.header-title) {
    color: black !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #F5F7FA !important;
}

[data-testid="stSidebar"] * {
    color: black !important;
}

/* ===== HEADERS ===== */
/* Header banner title - MUST BE WHITE */
.header-title {
    color: #FFFFFF !important;
    text-shadow: none !important;
}

/* Main content headers only - not the banner header */
.main h1:not(.header-title),
.main h2,
.main h3 {
    color: #2E86DE !important;
}

/* ===== BUTTONS ===== */
button {
    background-color: #2E86DE !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
}

button:hover {
    background-color: #0652DD !important;
    color: white !important;
}

/* ===== DROPDOWNS & SELECTS ===== */
/* Dropdown labels */
.stSelectbox label,
.stMultiSelect label,
.stTextInput label,
.stNumberInput label,
.stTextArea label {
    color: black !important;
    font-weight: 500 !important;
}

/* Dropdown options text - BLACK */
div[data-baseweb="select"] [role="option"],
div[data-baseweb="select"] li,
[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* Dropdown selected value - BLACK */
div[data-baseweb="select"] > div {
    color: black !important;
    background-color: white !important;
}

/* Multiselect tags */
div[data-baseweb="tag"] {
    background-color: #2E86DE !important;
}

div[data-baseweb="tag"] span {
    color: white !important;
}

/* ===== INPUT FIELDS ===== */
input, textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #E0E0E0 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: white !important;
}

.stTabs [data-baseweb="tab"] {
    color: black !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86DE !important;
    border-bottom: 2px solid #2E86DE !important;
}

/* ===== METRICS ===== */
/* Let aws_theme.py handle metric styling - don't override! */
.stMetric {
    background-color: transparent !important;
}

/* ===== INFO/WARNING/ERROR BOXES ===== */
.stAlert {
    background-color: white !important;
    border-left: 4px solid #2E86DE !important;
}

/* ===== DATAFRAMES ===== */
.stDataFrame {
    background-color: white !important;
}

table {
    background-color: white !important;
}

th {
    background-color: #2E86DE !important;
    color: white !important;
}

td {
    color: black !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background-color: #F5F7FA !important;
    color: black !important;
}

/* ===== RADIO & CHECKBOX ===== */
.stRadio label,
.stCheckbox label {
    color: black !important;
}

/* ===== CLEAN BORDERS ===== */
.stSelectbox > div,
.stMultiSelect > div,
.stTextInput > div,
.stNumberInput > div {
    border-radius: 4px !important;
}

/* ===== USER PROFILE STYLING ===== */
.user-profile {
    background-color: #F5F7FA !important;
    padding: 15px !important;
    border-radius: 8px !important;
    margin-bottom: 15px !important;
    border: 1px solid #E0E0E0 !important;
}

.user-profile h3 {
    color: #2E86DE !important;
    margin-bottom: 10px !important;
}

.user-profile p {
    color: black !important;
    margin: 5px 0 !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END SIMPLE BLUE THEME
# ==================================================================================

# Main header - centered with WHITE text
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <h1 class="header-title" style="color: #FFFFFF !important; margin: 0; font-weight: 600; text-shadow: none;">☁️ CloudIDP v3.0 Tri-Cloud Platform</h1>
    <p style="color: rgba(255,255,255,0.95) !important; margin: 5px 0 0 0; font-size: 18px; text-shadow: none;">Enterprise Multi-Cloud Infrastructure Development Platform</p>
</div>
""", unsafe_allow_html=True)

# ==================================================================================
# USER GREETING (IF AUTHENTICATED)
# ==================================================================================
if AUTH_ENABLED and current_user and isinstance(current_user, dict):
    user_name = current_user.get('given_name') or current_user.get('name') or 'User'
    user_email = current_user.get('email', '')
    st.markdown(f"### 👋 Welcome, {user_name}!")
    if user_email:
        st.caption(f"Logged in as: {user_email}")
    st.markdown("---")

# ==================================================================================
# CLOUD PROVIDER SELECTION - PROMINENT AT TOP
# ==================================================================================

st.markdown("### 🌐 Select Cloud Provider")
st.caption("Choose your cloud platform to manage infrastructure")

# Initialize cloud provider in session state (if not already set by preferences)
if 'cloud_provider' not in st.session_state:
    st.session_state.cloud_provider = 'AWS'

# Cloud provider radio buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    provider = st.radio(
        "Cloud Platform",
        options=["AWS", "Azure", "GCP"],
        horizontal=True,
        key="cloud_selector",
        index=["AWS", "Azure", "GCP"].index(st.session_state.cloud_provider),
        help="Switch between AWS, Azure, and Google Cloud Platform"
    )
    
    # Update session state and trigger rerun if changed
    if provider != st.session_state.cloud_provider:
        st.session_state.cloud_provider = provider
        
        # Save preference to database (if authenticated)
        if AUTH_ENABLED and current_user and isinstance(current_user, dict) and db_manager:
            try:
                user_prefs = st.session_state.get('user_preferences', {})
                user_prefs['default_cloud'] = provider.lower()
                db_manager.save_user_preferences(current_user['id'], user_prefs)
                st.session_state.user_preferences = user_prefs
            except Exception:
                pass  # Silently fail if preference saving doesn't work
        
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Initialize session
    SessionManager.initialize()
    
    # Get selected cloud provider
    cloud_provider = st.session_state.get('cloud_provider', 'AWS')
    
    # ==================================================================================
    # SIDEBAR - WITH USER PROFILE (IF AUTHENTICATED)
    # ==================================================================================
    with st.sidebar:
        # Show user profile at top of sidebar (if authenticated)
        if AUTH_ENABLED and current_user and isinstance(current_user, dict):
            st.markdown("## 👤 User Profile")
            st.markdown("### 👤")
            st.markdown(f"**{current_user.get('name', 'Unknown User')}**")
            st.caption(current_user.get('email', 'No email'))
            
            # Role badge
            role = current_user.get('role', 'viewer')
            role_colors = {
                'admin': '🔴',
                'architect': '🔵',
                'developer': '🟢',
                'finops': '🟡',
                'security': '🟠',
                'viewer': '⚪'
            }
            role_icon = role_colors.get(role, '⚪')
            st.markdown(f"**Role:** {role_icon} {role.title()}")
            
            # Last login
            if current_user.get('last_login'):
                try:
                    last_login = current_user['last_login'][:16]
                    st.caption(f"🟢 Logged in: {last_login.split('T')[1]}")
                except:
                    st.caption("🟢 Logged in")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                # Log logout event
                if db_manager:
                    try:
                        db_manager.log_event(
                            user_id=current_user['id'],
                            event_type='logout',
                            event_data={}
                        )
                    except:
                        pass
                
                # Clear session
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_info = None
                st.rerun()
            
            st.markdown("---")
        
        # Render global sidebar (cloud-aware)
        GlobalSidebar.render(cloud_provider)
    
    # ==================================================================================
    # MAIN NAVIGATION (CLOUD-AWARE)
    # ==================================================================================
    Navigation.render(cloud_provider)
    
    # Log page access (if authenticated)
    if AUTH_ENABLED and current_user and isinstance(current_user, dict) and db_manager:
        current_page = st.session_state.get('current_page', 'Dashboard')
        try:
            db_manager.log_event(
                user_id=current_user['id'],
                event_type='page_access',
                event_data={
                    'page': current_page,
                    'cloud_provider': cloud_provider
                }
            )
        except Exception:
            pass  # Silently fail if logging doesn't work
    
    # ==================================================================================
    # FOOTER
    # ==================================================================================
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        cloud_icon = {"AWS": "☁️", "Azure": "🔷", "GCP": "🔴"}
        st.caption(f"{cloud_icon.get(cloud_provider, '☁️')} {cloud_provider} Mode")
    
    with col3:
        if AUTH_ENABLED and current_user and isinstance(current_user, dict):
            user_role = current_user.get('role', 'viewer')
            st.caption(f"👤 {user_role.title()} | CloudIDP v3.0")
        else:
            st.caption(f"🌐 CloudIDP v3.0 Tri-Cloud Platform")

if __name__ == "__main__":
    main()