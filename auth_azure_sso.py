"""
Azure AD SSO Authentication - FIXED BUTTON VERSION
Works with personal Microsoft accounts
"""

import streamlit as st
from typing import Optional, Dict, List, Callable
from functools import wraps


# ============================================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================================

class RoleManager:
    """Manages role-based permissions"""
    
    ROLES = {
        'admin': {
            'description': 'Full system access',
            'permissions': ['*']
        },
        'architect': {
            'description': 'Design and provision infrastructure',
            'permissions': [
                'view_dashboard', 'view_resources', 'provision_resources',
                'design_architecture', 'use_devex', 'view_costs', 'manage_policies'
            ]
        },
        'developer': {
            'description': 'Deploy and manage applications',
            'permissions': ['view_dashboard', 'view_resources', 'deploy_applications', 'use_devex']
        },
        'finops': {
            'description': 'Financial operations and cost management',
            'permissions': ['view_dashboard', 'view_costs']
        },
        'security': {
            'description': 'Security and compliance management',
            'permissions': ['view_dashboard', 'view_security']
        },
        'viewer': {
            'description': 'Read-only access',
            'permissions': ['view_dashboard', 'view_resources', 'view_costs']
        }
    }
    
    @staticmethod
    def has_permission(user_role: str, required_permission: str) -> bool:
        if not user_role or user_role not in RoleManager.ROLES:
            return False
        role_permissions = RoleManager.ROLES[user_role]['permissions']
        if '*' in role_permissions:
            return True
        return required_permission in role_permissions
    
    @staticmethod
    def get_user_permissions(user_role: str) -> List[str]:
        if not user_role or user_role not in RoleManager.ROLES:
            return []
        permissions = RoleManager.ROLES[user_role]['permissions']
        if '*' in permissions:
            all_permissions = set()
            for role_data in RoleManager.ROLES.values():
                all_permissions.update(role_data['permissions'])
            all_permissions.discard('*')
            return list(all_permissions)
        return permissions


def require_permission(permission: str) -> Callable:
    """Decorator to require specific permission for a function"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_manager = st.session_state.get('user_manager')
            if not user_manager:
                st.error("❌ Authentication required")
                return
            
            current_user = user_manager.get_current_user()
            if not current_user or not isinstance(current_user, dict):
                st.error("❌ User session not found")
                st.info("Please logout and login again")
                return
            
            user_role = current_user.get('role', 'viewer')
            
            if not RoleManager.has_permission(user_role, permission):
                st.error("❌ You don't have permission to access this feature")
                st.info(f"**Required:** `{permission}` | **Your role:** `{user_role}`")
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


class SimpleUserManager:
    """Simple user manager for session"""
    
    def get_current_user(self):
        return st.session_state.get('user_info')
    
    def is_authenticated(self):
        return st.session_state.get('authenticated', False)


# ============================================================================
# AZURE AD AUTHENTICATION - FIXED BUTTON VERSION
# ============================================================================

def exchange_code_for_token(code: str, client_id: str, client_secret: str, 
                           redirect_uri: str, tenant_id: str = "common") -> Optional[Dict]:
    """Exchange authorization code for access token"""
    import requests
    
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'scope': 'openid profile email https://graph.microsoft.com/User.Read'
    }
    
    try:
        response = requests.post(token_url, data=token_data, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            error_desc = error_data.get('error_description', f'HTTP {response.status_code}')
            
            st.error(f"❌ Authentication Failed")
            
            with st.expander("🔍 View Error Details", expanded=True):
                st.code(error_desc)
                
                # Provide specific fixes based on error type
                if 'redirect_uri' in error_desc.lower():
                    st.warning(f"""
                    **Redirect URI Mismatch**
                    
                    The redirect_uri must match EXACTLY in Azure AD.
                    
                    Current redirect_uri: `{redirect_uri}`
                    """)
                
                elif 'unauthorized_client' in error_desc.lower():
                    st.warning("""
                    **Unauthorized Client**
                    
                    This usually means:
                    1. Personal Microsoft accounts not enabled in Azure AD
                    2. Or the app is not configured for the account type being used
                    
                    **Fix:**
                    - Go to Azure Portal → App registrations → Your App
                    - Change "Supported account types" to include personal Microsoft accounts
                    """)
                
                elif 'client_secret' in error_desc.lower() or 'invalid_client' in error_desc.lower():
                    st.warning("""
                    **Invalid Client Secret**
                    
                    **Steps to fix:**
                    1. Go to Azure Portal → App Registrations → Your App
                    2. Go to Certificates & secrets
                    3. Create a new client secret
                    4. Update the secret in Streamlit secrets
                    """)
            
            return None
        
        return response.json()
        
    except requests.exceptions.Timeout:
        st.error("❌ Connection timeout - please try again")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Network connection error - please check your internet connection")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None


def get_user_info(access_token: str) -> Optional[Dict]:
    """Get user information from Microsoft Graph"""
    import requests
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get('https://graph.microsoft.com/v1.0/me', 
                              headers=headers, 
                              timeout=10)
        response.raise_for_status()
        
        user_data = response.json()
        
        return {
            'id': user_data.get('id'),
            'email': user_data.get('mail') or user_data.get('userPrincipalName'),
            'name': user_data.get('displayName'),
            'given_name': user_data.get('givenName'),
            'family_name': user_data.get('surname')
        }
    except Exception as e:
        st.error(f"❌ Failed to get user info: {str(e)}")
        return None


def render_login():
    """Render login UI with WORKING button"""
    
    # Get Azure AD config
    try:
        client_id = st.secrets.azure_ad.client_id
        client_secret = st.secrets.azure_ad.client_secret
        tenant_id = st.secrets.azure_ad.get('tenant_id', 'common')
        
        # Get redirect URI and clean it
        redirect_uri_config = st.secrets.azure_ad.get('redirect_uri', '')
        
        # Clean the redirect_uri
        redirect_uri = redirect_uri_config.rstrip('/')
        
        # Validate configuration
        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError("Missing required configuration")
            
    except Exception as e:
        st.error("❌ Azure AD Configuration Error")
        st.info("""
        **Required Streamlit Secrets:**
        
        ```toml
        [azure_ad]
        client_id = "your-client-id-from-azure"
        client_secret = "your-client-secret-from-azure"
        tenant_id = "common"  # For both work and personal accounts
        redirect_uri = "https://hyperscaler.streamlit.app"
        ```
        """)
        st.stop()
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params:
        # User returned from Microsoft with authorization code
        with st.spinner("🔐 Completing sign-in..."):
            code = query_params['code']
            
            # Exchange code for token
            token_response = exchange_code_for_token(
                code=code,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                tenant_id=tenant_id
            )
            
            if token_response and 'access_token' in token_response:
                # Get user info from Microsoft Graph
                user_info = get_user_info(token_response['access_token'])
                
                if user_info:
                    # Register/update user in Firebase
                    try:
                        from auth_database_firebase import get_database_manager
                        db_manager = get_database_manager()
                        
                        if db_manager:
                            user_id = user_info['id']
                            
                            # Check if user exists
                            try:
                                existing_user = db_manager.get_user(user_id)
                                is_new_user = not (existing_user and isinstance(existing_user, dict))
                            except:
                                is_new_user = True
                            
                            if is_new_user:
                                # New user - set defaults
                                user_info['role'] = 'viewer'
                                user_info['is_active'] = True
                                db_manager.create_or_update_user(user_info)
                                final_user_info = user_info
                            else:
                                # Existing user - update info but preserve role
                                update_data = {
                                    'id': user_info['id'],
                                    'email': user_info['email'],
                                    'name': user_info.get('name', ''),
                                    'given_name': user_info.get('given_name', ''),
                                    'family_name': user_info.get('family_name', '')
                                }
                                db_manager.create_or_update_user(update_data)
                                
                                # Load from Firebase to get actual role
                                try:
                                    final_user_info = db_manager.get_user(user_id)
                                    if not final_user_info:
                                        final_user_info = user_info
                                except:
                                    final_user_info = user_info
                            
                            # Set session state
                            st.session_state.authenticated = True
                            st.session_state.user_id = final_user_info['id']
                            st.session_state.user_info = final_user_info
                            st.session_state.user_manager = SimpleUserManager()
                            
                            # Clear query params and redirect to app
                            st.query_params.clear()
                            st.success("✅ Login successful!")
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                        st.info("Please try logging in again")
                        if st.button("🔄 Try Again"):
                            st.query_params.clear()
                            st.rerun()
                else:
                    st.error("❌ Could not retrieve user information")
                    if st.button("🔄 Try Again"):
                        st.query_params.clear()
                        st.rerun()
            else:
                # Token exchange failed - error already displayed
                if st.button("🔄 Try Again"):
                    st.query_params.clear()
                    st.rerun()
    
    elif 'error' in query_params:
        # User cancelled or error occurred at Microsoft
        error = query_params.get('error', ['unknown'])[0]
        error_desc = query_params.get('error_description', ['No description'])[0]
        
        st.error("❌ Authentication Error")
        st.warning(f"**Error:** {error}")
        st.info(error_desc)
        
        if st.button("🔄 Try Again"):
            st.query_params.clear()
            st.rerun()
    
    else:
        # Auto-redirect to Microsoft login - NO login page shown
        from urllib.parse import quote
        
        # Build OAuth authorization URL
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        
        # Define scopes
        scopes = "openid profile email https://graph.microsoft.com/User.Read"
        
        # Build complete OAuth URL
        auth_url = (
            f"{authority}/oauth2/v2.0/authorize?"
            f"client_id={client_id}&"
            f"response_type=code&"
            f"redirect_uri={quote(redirect_uri, safe='')}&"
            f"response_mode=query&"
            f"scope={quote(scopes)}&"
            f"prompt=select_account"
        )
        
        # Show branded redirect page with logo
        # Using custom logo and meta refresh for reliable redirect
        st.markdown(f"""
        <meta http-equiv="refresh" content="0;url={auth_url}">
        <style>
        .redirect-container {{
            max-width: 600px;
            margin: 80px auto;
            padding: 50px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .logo-container {{
            margin-bottom: 30px;
        }}
        .logo {{
            width: 200px;
            height: 200px;
            margin: 0 auto;
            animation: pulse 1.5s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.05); opacity: 0.8; }}
        }}
        .title {{
            font-size: 28px;
            font-weight: bold;
            color: #0078D4;
            margin: 20px 0 10px 0;
        }}
        .subtitle {{
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
        }}
        .loading-dots {{
            font-size: 24px;
            color: #0078D4;
            letter-spacing: 4px;
            animation: blink 1.4s infinite;
        }}
        @keyframes blink {{
            0%, 20% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        .fallback-link {{
            margin-top: 30px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
        }}
        .fallback-link a {{
            color: #0078D4;
            font-weight: bold;
            text-decoration: none;
            font-size: 16px;
        }}
        .fallback-link a:hover {{
            text-decoration: underline;
        }}
        </style>
        
        <div class="redirect-container">
            <div class="logo-container">
                <svg class="logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <!-- Cloud brain logo -->
                    <!-- Outer cloud shape -->
                    <path d="M50 100 Q30 100 30 80 Q30 60 50 60 Q50 40 70 40 Q90 40 90 60 Q110 60 110 40 Q130 40 130 60 Q150 60 150 80 Q170 80 170 100 Q170 120 150 120 Q150 140 130 140 Q110 140 110 120 Q90 120 90 140 Q70 140 70 120 Q50 120 50 100 Z" 
                          fill="none" 
                          stroke="#0078D4" 
                          stroke-width="6"/>
                    
                    <!-- Left brain (blue) -->
                    <path d="M75 80 Q75 70 85 70 Q85 80 85 90 L85 95 Q80 95 80 90 Q75 90 75 95 Q70 95 70 90 Q70 80 75 80 Z"
                          fill="#4FC3F7"/>
                    <path d="M65 100 Q70 100 75 95 Q75 105 70 105 Q65 105 65 100 Z"
                          fill="#29B6F6"/>
                    
                    <!-- Right brain top (green) -->
                    <path d="M115 70 Q120 70 120 75 Q125 75 125 80 Q125 90 120 90 Q115 90 115 85 Q115 75 115 70 Z"
                          fill="#66BB6A"/>
                    <path d="M115 85 Q120 85 120 95 Q115 95 115 90 Z"
                          fill="#4CAF50"/>
                    
                    <!-- Right brain bottom (orange/yellow) -->
                    <path d="M115 100 Q120 100 125 105 Q125 115 120 115 Q115 115 115 110 Q110 110 110 105 Q110 100 115 100 Z"
                          fill="#FFA726"/>
                    <path d="M115 110 Q120 110 120 120 Q115 120 115 115 Z"
                          fill="#FF9800"/>
                    
                    <!-- Dividing line -->
                    <line x1="100" y1="65" x2="100" y2="125" 
                          stroke="#0078D4" 
                          stroke-width="4"/>
                </svg>
            </div>
            
            <div class="title">Redirecting to Microsoft Login</div>
            <div class="subtitle">Multi Intelligence Cloud Platform</div>
            <div class="loading-dots">• • •</div>
            
            <div class="fallback-link">
                <p style="font-size: 14px; color: #666; margin-bottom: 10px;">
                    If you are not redirected automatically
                </p>
                <a href="{auth_url}">click here to continue</a>
            </div>
        </div>
        
        <script>
            // Fallback JavaScript redirect
            setTimeout(function() {{
                window.location.href = "{auth_url}";
            }}, 100);
        </script>
        """, unsafe_allow_html=True)
        
        st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']
