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
# CLOUD PROVIDER SELECTION - PROMINENT AT TOP
# ==================================================================================

st.markdown("### 🌐 Select Cloud Provider")
st.caption("Choose your cloud platform to manage infrastructure")

# Initialize cloud provider in session state (if not already set by preferences)
if 'cloud_provider' not in st.session_state:
    st.session_state.cloud_provider = 'AWS'

# Custom CSS for cloud provider buttons
st.markdown("""
<style>
.cloud-button-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
}
.cloud-button {
    flex: 1;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid #e5e7eb;
    background: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}
.cloud-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.cloud-button.active {
    border-color: #3b82f6;
    background: #eff6ff;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}
.cloud-logo {
    font-size: 48px;
    margin-bottom: 8px;
}
.cloud-name {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# Cloud provider selection using columns and buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("", key="aws_btn", help="Amazon Web Services", use_container_width=True):
        st.session_state.cloud_provider = 'AWS'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'aws'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    # AWS logo and label
    aws_style = "border: 3px solid #FF9900; background: #FFF3E0;" if st.session_state.cloud_provider == 'AWS' else "border: 2px solid #e5e7eb;"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; {aws_style} cursor: pointer;">
        <div style="font-size: 36px; margin-bottom: 8px;">
            <svg viewBox="0 0 24 24" width="48" height="48" xmlns="http://www.w3.org/2000/svg">
                <path fill="#FF9900" d="M6.763 10.036c0 .296.032.535.088.71.064.176.144.368.256.576.04.063.056.127.056.183 0 .08-.048.16-.152.24l-.503.335c-.072.048-.144.072-.208.072-.08 0-.16-.04-.239-.112-.12-.127-.216-.263-.295-.415-.08-.152-.16-.32-.248-.512-.631.744-1.423 1.116-2.375 1.116-.68 0-1.22-.194-1.612-.583-.392-.39-.588-.91-.588-1.557 0-.688.243-1.245.735-1.663.492-.418 1.15-.627 1.97-.627.272 0 .551.024.846.064.296.04.6.104.918.176v-.583c0-.607-.127-1.031-.375-1.271-.255-.24-.686-.36-1.295-.36-.279 0-.567.032-.863.104-.295.072-.583.16-.862.272-.128.056-.224.096-.271.112-.048.016-.08.024-.104.024-.096 0-.144-.072-.144-.208v-.327c0-.104.016-.184.056-.24.04-.055.12-.104.24-.16.279-.144.614-.264 1.005-.36C4.444.272 4.87.224 5.33.224c1.023 0 1.766.231 2.246.696.471.463.711 1.167.711 2.111v2.785l-.024.001zM3.813 9.496c.264 0 .537-.048.822-.144.287-.096.543-.271.758-.504.128-.144.224-.304.279-.488.056-.184.088-.407.088-.671v-.319c-.231-.048-.479-.088-.742-.112-.263-.024-.527-.04-.79-.04-.567 0-.983.112-1.255.343-.271.23-.407.558-.407 1.006 0 .423.103.742.319.966.208.215.527.327.918.327l.01.001zm8.697 1.235c-.128 0-.215-.024-.271-.08-.056-.048-.104-.151-.144-.271l-1.612-5.303c-.04-.135-.064-.223-.064-.271 0-.104.048-.16.144-.16h.591c.135 0 .224.024.272.08.056.048.096.151.136.271l1.151 4.538 1.07-4.538c.032-.127.072-.223.128-.271.056-.048.151-.08.279-.08h.48c.135 0 .224.024.28.08.055.048.103.151.127.271l1.079 4.598 1.191-4.598c.04-.127.088-.223.144-.271.056-.048.143-.08.271-.08h.559c.104 0 .16.048.16.16 0 .04-.008.08-.016.127-.008.048-.024.112-.048.192l-1.652 5.306c-.04.127-.088.223-.144.271-.056.048-.143.08-.271.08h-.52c-.136 0-.224-.024-.28-.08-.056-.056-.103-.159-.127-.271l-1.063-4.414-1.055 4.406c-.032.127-.072.223-.128.271-.056.056-.151.08-.279.08h-.52l-.001.002zm13.742.263c-.544 0-1.087-.064-1.606-.184-.52-.12-.903-.263-1.151-.431-.127-.088-.215-.184-.247-.28-.032-.095-.048-.199-.048-.31v-.34c0-.136.048-.208.144-.208.056 0 .112.016.168.04.056.024.143.064.24.111.431.208.895.368 1.375.479.495.112.982.168 1.479.168.791 0 1.406-.136 1.838-.407.431-.271.647-.671.647-1.191 0-.36-.12-.663-.36-.911-.24-.248-.687-.471-1.343-.671l-1.926-.591c-.976-.304-1.694-.751-2.142-1.343-.447-.583-.671-1.247-.671-1.975 0-.576.12-1.086.36-1.518.239-.431.559-.799.959-1.103.399-.303.863-.535 1.382-.695.52-.16 1.07-.24 1.647-.24.232 0 .471.008.71.032.247.024.479.056.71.104.224.048.44.104.647.168.207.063.375.127.495.191.111.063.2.127.255.191.056.063.08.151.08.271v.32c0 .136-.048.208-.144.208-.064 0-.168-.048-.312-.12-.487-.231-1.031-.344-1.622-.344-.72 0-1.295.12-1.694.368-.4.247-.6.631-.6 1.15 0 .36.127.672.384.927.255.256.735.512 1.438.735l1.886.591c.96.304 1.654.727 2.078 1.271.423.543.631 1.167.631 1.87 0 .591-.12 1.119-.36 1.582-.239.464-.575.855-.999 1.175-.424.32-.935.56-1.534.727-.598.167-1.255.251-1.966.251l-.002-.001z"/>
            </svg>
        </div>
        <div style="font-weight: 600; color: #FF9900;">AWS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("", key="azure_btn", help="Microsoft Azure", use_container_width=True):
        st.session_state.cloud_provider = 'Azure'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'azure'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    # Azure logo and label
    azure_style = "border: 3px solid #0078D4; background: #E6F2FF;" if st.session_state.cloud_provider == 'Azure' else "border: 2px solid #e5e7eb;"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; {azure_style} cursor: pointer;">
        <div style="font-size: 36px; margin-bottom: 8px;">
            <svg viewBox="0 0 24 24" width="48" height="48" xmlns="http://www.w3.org/2000/svg">
                <path fill="#0078D4" d="M5.483 18.648h7.202L9.67 24H.001zm9.106-18.648-7.076 12.906L0 18.648h5.7l8.889-18.648z"/>
                <path fill="#0078D4" d="M12.326 0l8.729 15.365-6.053 3.283h8.998L12.326 0z"/>
            </svg>
        </div>
        <div style="font-weight: 600; color: #0078D4;">Azure</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("", key="gcp_btn", help="Google Cloud Platform", use_container_width=True):
        st.session_state.cloud_provider = 'GCP'
        if AUTH_ENABLED and current_user and db_manager:
            user_prefs = st.session_state.get('user_preferences', {})
            user_prefs['default_cloud'] = 'gcp'
            db_manager.save_user_preferences(current_user['id'], user_prefs)
            st.session_state.user_preferences = user_prefs
        st.rerun()
    
    # GCP logo and label
    gcp_style = "border: 3px solid #4285F4; background: #E8F0FE;" if st.session_state.cloud_provider == 'GCP' else "border: 2px solid #e5e7eb;"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; {gcp_style} cursor: pointer;">
        <div style="font-size: 36px; margin-bottom: 8px;">
            <svg viewBox="0 0 24 24" width="48" height="48" xmlns="http://www.w3.org/2000/svg">
                <path fill="#EA4335" d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/>
            </svg>
        </div>
        <div style="font-weight: 600; color: #4285F4;">GCP</div>
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