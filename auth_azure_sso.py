"""
Azure AD SSO Authentication Module
Professional light blue gradient design with auto-redirect
Firebase is OPTIONAL - works without it if secrets not configured
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import secrets
import urllib.parse

# Try to import Firebase, but make it optional
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# Initialize Firebase (optional)
def init_firebase():
    """Initialize Firebase if credentials are available"""
    if not FIREBASE_AVAILABLE:
        return None
    
    # Check if Firebase secrets exist
    if "firebase" not in st.secrets:
        return None
    
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate({
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
            })
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.warning(f"Firebase initialization failed: {str(e)}")
            return None
    
    return firestore.client()

# Azure AD OAuth Configuration
def get_oauth_config():
    return {
        'client_id': st.secrets["azure_ad"]["client_id"],
        'client_secret': st.secrets["azure_ad"]["client_secret"],
        'tenant_id': st.secrets["azure_ad"]["tenant_id"],
        'redirect_uri': st.secrets["azure_ad"]["redirect_uri"]
    }

def build_auth_url():
    """Build Microsoft OAuth authorization URL"""
    config = get_oauth_config()
    
    # Generate and store state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    st.session_state.oauth_state = state
    
    params = {
        'client_id': config['client_id'],
        'response_type': 'code',
        'redirect_uri': config['redirect_uri'],
        'response_mode': 'query',
        'scope': 'openid profile email User.Read',
        'state': state
    }
    
    auth_url = f"https://login.microsoftonline.com/{config['tenant_id']}/oauth2/v2.0/authorize?"
    auth_url += urllib.parse.urlencode(params)
    
    return auth_url

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    config = get_oauth_config()
    
    token_url = f"https://login.microsoftonline.com/{config['tenant_id']}/oauth2/v2.0/token"
    
    data = {
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': code,
        'redirect_uri': config['redirect_uri'],
        'grant_type': 'authorization_code'
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Token exchange failed: {str(e)}")
        return None

def get_user_info(access_token):
    """Get user information from Microsoft Graph API"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get user info: {str(e)}")
        return None

def create_or_update_user(user_info, db=None):
    """Create or update user in Firestore (if available) or session only"""
    user_email = user_info.get('mail') or user_info.get('userPrincipalName')
    
    user_data = {
        'email': user_email,
        'display_name': user_info.get('displayName'),
        'given_name': user_info.get('givenName'),
        'surname': user_info.get('surname'),
        'job_title': user_info.get('jobTitle'),
        'office_location': user_info.get('officeLocation'),
        'last_login': datetime.utcnow(),
        'auth_provider': 'azure_ad'
    }
    
    # If Firebase is available, use it
    if db is not None:
        try:
            users_ref = db.collection('users')
            user_doc = users_ref.document(user_email).get()
            
            if not user_doc.exists:
                # New user - set default role
                user_data['role'] = 'viewer'
                user_data['created_at'] = datetime.utcnow()
                user_data['status'] = 'active'
            
            users_ref.document(user_email).set(user_data, merge=True)
            
            # Fetch complete user data
            updated_doc = users_ref.document(user_email).get()
            return updated_doc.to_dict()
        except Exception as e:
            st.warning(f"Firebase update failed, using session only: {str(e)}")
    
    # Fallback: Use session storage only (no Firebase)
    if 'role' not in user_data:
        user_data['role'] = 'viewer'
    if 'created_at' not in user_data:
        user_data['created_at'] = datetime.utcnow()
    if 'status' not in user_data:
        user_data['status'] = 'active'
    
    return user_data

def require_auth():
    """Main authentication flow with auto-redirect"""
    
    # Initialize Firebase (optional)
    db = init_firebase()
    
    # Check if user is already authenticated
    if 'user' in st.session_state and st.session_state.user:
        return True
    
    # Check for OAuth callback (code in query params)
    query_params = st.query_params
    
    if 'code' in query_params:
        # Verify state parameter
        returned_state = query_params.get('state', [''])[0] if isinstance(query_params.get('state'), list) else query_params.get('state', '')
        expected_state = st.session_state.get('oauth_state', '')
        
        if returned_state != expected_state:
            st.error("Invalid state parameter. Possible CSRF attack.")
            return False
        
        # Exchange code for token
        code = query_params['code'][0] if isinstance(query_params['code'], list) else query_params['code']
        token_response = exchange_code_for_token(code)
        
        if token_response and 'access_token' in token_response:
            # Get user info
            user_info = get_user_info(token_response['access_token'])
            
            if user_info:
                # Create/update user (with or without Firebase)
                user_data = create_or_update_user(user_info, db)
                
                # Store in session
                st.session_state.user = user_data
                st.session_state.authenticated = True
                
                # Clear query params and reload
                st.query_params.clear()
                st.rerun()
        else:
            st.error("Authentication failed. Please try again.")
            return False
    
    # Not authenticated - show login page with auto-redirect
    show_login_page()
    return False

def show_login_page():
    """Display professional login page with auto-redirect (Saturday's working approach)"""
    
    # Build OAuth URL
    auth_url = build_auth_url()
    
    # Professional light blue gradient background
    st.markdown("""
    <style>
    /* Full page gradient background */
    .stApp {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Center container */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    /* Glass-morphism card */
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 50px;
        max-width: 450px;
        width: 100%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    
    /* Title styling */
    .login-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }
    
    /* Provider logos */
    .provider-logos {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
        font-size: 48px;
    }
    
    /* Redirecting message */
    .redirect-message {
        font-size: 18px;
        color: #333;
        margin: 30px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    /* Spinner animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spinner {
        display: inline-block;
        animation: spin 1s linear infinite;
    }
    
    /* Fallback link */
    .fallback-link {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 32px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
    }
    
    .fallback-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6);
        text-decoration: none;
        color: white;
    }
    
    /* Security badge */
    .security-badge {
        margin-top: 30px;
        padding: 12px;
        background: rgba(79, 172, 254, 0.1);
        border-radius: 8px;
        color: #333;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # AUTO-REDIRECT using meta refresh (Saturday's working approach!)
    st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
    
    # Login page content (shown briefly before redirect)
    st.markdown(f"""
    <div class="login-container">
        <div class="login-card">
            <h1 class="login-title">🔐 CloudIDP Sign In</h1>
            
            <div class="provider-logos">
                <span title="AWS">🟧</span>
                <span title="Azure">🔷</span>
                <span title="GCP">🌈</span>
            </div>
            
            <div class="redirect-message">
                <span class="spinner">🔄</span>
                <span>Redirecting to Microsoft login...</span>
            </div>
            
            <a href="{auth_url}" class="fallback-link">
                🔷 If not redirected, click here
            </a>
            
            <div class="security-badge">
                🔒 Enterprise SSO Authentication • Secure & Reliable
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

def require_permission(required_role):
    """Decorator to check user permissions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user' not in st.session_state or not st.session_state.user:
                st.error("Please log in to access this feature.")
                return None
            
            user_role = st.session_state.user.get('role', 'viewer')
            role_hierarchy = {'viewer': 0, 'editor': 1, 'admin': 2}
            
            if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
                st.error(f"Insufficient permissions. Required role: {required_role}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def logout():
    """Clear session and logout"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def get_current_user():
    """Get current authenticated user"""
    return st.session_state.get('user', None)

def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    return user and user.get('role') == 'admin'

# Initialize authentication on import (but don't fail if Firebase is missing)
if __name__ != "__main__":
    try:
        require_auth()
    except Exception as e:
        # Log error but don't crash on import
        print(f"Auth initialization warning: {str(e)}")
