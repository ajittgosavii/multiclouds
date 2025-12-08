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
    from auth_azure_sso import init_authentication
    from auth_ui_components import render_login_page, render_user_profile
    from auth_database_firestore import get_database_manager
    
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
    try:
        init_authentication()
        
        # Check authentication
        user_manager = st.session_state.get('user_manager')
        if not user_manager or not user_manager.is_authenticated():
            # Show login page and stop
            render_login_page()
            st.stop()
        
        # Get current user and database manager
        current_user = user_manager.get_current_user()
        db_manager = get_database_manager()
        
        # Update user in database
        if current_user and db_manager:
            db_manager.create_or_update_user(current_user)
            
            # Load user preferences
            user_prefs = db_manager.get_user_preferences(current_user['id'])
            if 'user_preferences' not in st.session_state:
                st.session_state.user_preferences = user_prefs
            
            # Set default cloud provider from preferences
            if 'cloud_provider' not in st.session_state:
                default_cloud = user_prefs.get('default_cloud', 'AWS').upper()
                st.session_state.cloud_provider = default_cloud
    except Exception as e:
        st.error(f"⚠️ Authentication Error: {str(e)}")
        st.info("Please check your authentication configuration and ensure all auth modules are deployed.")
        st.stop()
else:
    # Authentication disabled - show warning
    st.warning("⚠️ **Authentication is disabled.** Running in legacy mode. To enable authentication, ensure these files are deployed:\n- auth_azure_sso.py\n- auth_ui_components.py\n- auth_database_firestore.py")
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

/* ===== NAVIGATION SECTION STYLING ===== */
/* White background for navigation area */
div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) {
    background: white !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    margin: 15px 0 !important;
}

/* Navigation section container - comprehensive targeting */
section[data-testid="stHorizontalBlock"] {
    background: white !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    margin: 15px 0 !important;
}

/* Navigation header styling */
h3:contains("Navigation") {
    background: transparent !important;
    padding: 15px 0px !important;
    margin-bottom: 15px !important;
    color: #2E86DE !important;
}

/* Navigation buttons - ensure good visibility */
div[data-testid="column"] button[kind="primary"] {
    background: linear-gradient(135deg, #2E86DE 0%, #0652DD 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 2px 6px rgba(46,134,222,0.4) !important;
}

div[data-testid="column"] button[kind="secondary"] {
    background-color: white !important;
    color: #2E86DE !important;
    border: 2px solid #2E86DE !important;
    font-weight: 500 !important;
}

div[data-testid="column"] button[kind="secondary"]:hover {
    background-color: #EEF5FF !important;
    border-color: #0652DD !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(6,82,221,0.2) !important;
}

/* Navigation button text visibility */
div[data-testid="column"] button * {
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END SIMPLE BLUE THEME
# ==================================================================================

# Main header - centered with WHITE text
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 12px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <h1 class="header-title" style="color: #FFFFFF !important; margin: 0; font-weight: 600; text-shadow: none;">☁️ Multi Cloud Intelligence Platform</h1>
    <p style="color: rgba(255,255,255,0.95) !important; margin: 5px 0 0 0; font-size: 18px; text-shadow: none;">Enterprise Multi-Cloud Infrastructure Development Platform</p>
</div>
""", unsafe_allow_html=True)

# ==================================================================================
# USER GREETING (IF AUTHENTICATED)
# ==================================================================================
if AUTH_ENABLED and current_user:
    st.markdown(f"### 👋 Welcome, {current_user.get('given_name', 'User')}!")
    st.caption(f"Logged in as: {current_user.get('email')}")
    st.markdown("---")

# ==================================================================================
# CLOUD PROVIDER SELECTION - ULTRA VISIBLE VERSION
# ==================================================================================

st.markdown("### 🌐 Select Cloud Provider")
st.caption("Choose your cloud platform to manage infrastructure")

# Initialize cloud provider in session state (if not already set by preferences)
if 'cloud_provider' not in st.session_state:
    st.session_state.cloud_provider = 'AWS'

# Cloud provider selection using columns
col1, col2, col3 = st.columns(3)

# ==================== AWS ====================
with col1:
    is_active = st.session_state.cloud_provider == 'AWS'
    
    if st.button("🔸 Select AWS", key="aws_btn", use_container_width=True, 
                 type="primary" if is_active else "secondary"):
        st.session_state.cloud_provider = 'AWS'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'aws'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    border = "4px solid #FF9900" if is_active else "2px solid #DDDDDD"
    bg = "#FFF5E6" if is_active else "#FFFFFF"
    shadow = "0 4px 12px rgba(255,153,0,0.3)" if is_active else "0 2px 6px rgba(0,0,0,0.1)"
    
    st.markdown(f"""
    <div style="border: {border}; background: {bg}; padding: 30px 20px; border-radius: 12px; text-align: center; box-shadow: {shadow}; margin-top: 10px;">
        <div style="font-size: 64px; color: #FF9900; font-weight: bold; margin-bottom: 12px; font-family: Arial, sans-serif;">
            AWS
        </div>
        <div style="font-size: 16px; color: #232F3E; font-weight: 600;">
            Amazon Web Services
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== AZURE ====================
with col2:
    is_active = st.session_state.cloud_provider == 'Azure'
    
    if st.button("🔹 Select Azure", key="azure_btn", use_container_width=True,
                 type="primary" if is_active else "secondary"):
        st.session_state.cloud_provider = 'Azure'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'azure'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    border = "4px solid #0078D4" if is_active else "2px solid #DDDDDD"
    bg = "#EBF5FF" if is_active else "#FFFFFF"
    shadow = "0 4px 12px rgba(0,120,212,0.3)" if is_active else "0 2px 6px rgba(0,0,0,0.1)"
    
    st.markdown(f"""
    <div style="border: {border}; background: {bg}; padding: 30px 20px; border-radius: 12px; text-align: center; box-shadow: {shadow}; margin-top: 10px;">
        <div style="margin-bottom: 12px;">
            <svg width="80" height="80" viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="azureGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#0078D4;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#00BCF2;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <path fill="url(#azureGrad)" d="M86.724 49.508 60.995 79.085H36.897L72.124 16.915h14.6L61.015 49.5zm-36.067 0L32.82 79.085H9.236l13.828-29.577h-13.6L23.309 9.236l27.348 40.272z"/>
            </svg>
        </div>
        <div style="font-size: 22px; color: #0078D4; font-weight: bold; margin-bottom: 4px; letter-spacing: 2px;">
            AZURE
        </div>
        <div style="font-size: 14px; color: #005A9E; font-weight: 600;">
            Microsoft Azure
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== GCP ====================
with col3:
    is_active = st.session_state.cloud_provider == 'GCP'
    
    if st.button("🔷 Select GCP", key="gcp_btn", use_container_width=True,
                 type="primary" if is_active else "secondary"):
        st.session_state.cloud_provider = 'GCP'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'gcp'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    border = "4px solid #4285F4" if is_active else "2px solid #DDDDDD"
    bg = "#F0F4FF" if is_active else "#FFFFFF"
    shadow = "0 4px 12px rgba(66,133,244,0.3)" if is_active else "0 2px 6px rgba(0,0,0,0.1)"
    
    st.markdown(f"""
    <div style="border: {border}; background: {bg}; padding: 30px 20px; border-radius: 12px; text-align: center; box-shadow: {shadow}; margin-top: 10px;">
        <div style="margin-bottom: 12px;">
            <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <g transform="translate(10,10)">
                    <!-- Blue hexagon top -->
                    <path d="M40 0 L60 0 L80 34.64 L60 69.28 L40 69.28 L20 34.64 Z" fill="#4285F4" opacity="0.9"/>
                    <!-- Green bottom right -->
                    <path d="M60 69.28 L80 34.64 L60 0" fill="#34A853" opacity="0.8"/>
                    <!-- Yellow bottom left -->
                    <path d="M20 34.64 L40 69.28 L60 69.28" fill="#FBBC05" opacity="0.8"/>
                    <!-- Red top -->
                    <path d="M40 0 L60 0 L80 34.64" fill="#EA4335" opacity="0.7"/>
                </g>
            </svg>
        </div>
        <div style="font-size: 22px; color: #4285F4; font-weight: bold; margin-bottom: 4px; letter-spacing: 2px;">
            GCP
        </div>
        <div style="font-size: 14px; color: #5F6368; font-weight: 600;">
            Google Cloud Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        if AUTH_ENABLED:
            render_user_profile()
            st.markdown("---")
        
        # Render global sidebar (cloud-aware)
        GlobalSidebar.render(cloud_provider)
    
    # ==================================================================================
    # MAIN NAVIGATION (CLOUD-AWARE)
    # ==================================================================================
    Navigation.render(cloud_provider)
    
    # Log page access (if authenticated)
    if AUTH_ENABLED and current_user and db_manager:
        current_page = st.session_state.get('current_page', 'Dashboard')
        db_manager.log_event(
            user_id=current_user['id'],
            event_type='page_access',
            event_data={
                'page': current_page,
                'cloud_provider': cloud_provider
            }
        )
    
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
        if AUTH_ENABLED and current_user:
            role_manager = st.session_state.get('role_manager')
            user_role = role_manager.get_user_role(current_user['id']) if role_manager else 'viewer'
            st.caption(f"👤 {user_role.title()} | CloudIDP v3.0")
        else:
            st.caption(f"🌐 Multi Cloud Intelligence Platform")

if __name__ == "__main__":
    main()