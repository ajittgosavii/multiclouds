"""
Azure AD SSO Authentication - DEBUG VERSION
Shows exact configuration being used to help diagnose issues
"""

import streamlit as st
from typing import Optional, Dict, List, Callable
from functools import wraps


# ============================================================================
# ROLE-BASED ACCESS CONTROL (Same as before)
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
# AZURE AD AUTHENTICATION - DEBUG VERSION
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
                    
                    The redirect_uri sent to Azure doesn't match what's registered.
                    
                    **Current redirect_uri:** `{redirect_uri}`
                    
                    **Steps to fix:**
                    1. Go to Azure Portal → App Registrations → Your App
                    2. Go to Authentication → Platform configurations
                    3. Add/verify this EXACT URL: `{redirect_uri}`
                    4. Make sure "ID tokens" is checked under Implicit grant
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
                
                elif 'code' in error_desc.lower() or 'expired' in error_desc.lower():
                    st.warning("""
                    **Authorization Code Invalid/Expired**
                    
                    Authorization codes expire in 10 minutes and can only be used once.
                    
                    **Solution:** Click the "Sign in with Microsoft" button below to get a new code.
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
    """Render login UI with DEBUG information"""
    
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
        tenant_id = "common"  # Use "common" for multitenant
        redirect_uri = "https://hyperscaler.streamlit.app"  # Your app URL
        ```
        
        **Important Notes:**
        - No trailing slash in redirect_uri
        - Must match EXACTLY in Azure AD App Registration
        - Use "common" for multitenant, or your tenant ID for single tenant
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
        # Show login page with DEBUG information
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
        
        # Display login page
        st.markdown("""
        <style>
        .login-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 40px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        .logo {
            font-size: 64px;
            margin-bottom: 20px;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2E86DE;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
        }
        .ms-button {
            display: inline-block;
            background-color: #0078D4;
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 18px;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,120,212,0.3);
        }
        .ms-button:hover {
            background-color: #005A9E;
            box-shadow: 0 4px 15px rgba(0,120,212,0.5);
            transform: translateY(-2px);
        }
        .debug-box {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
            text-align: left;
            font-family: monospace;
            font-size: 12px;
        }
        .debug-item {
            margin: 10px 0;
            padding: 8px;
            background: white;
            border-radius: 4px;
        }
        .debug-label {
            font-weight: bold;
            color: #495057;
        }
        .debug-value {
            color: #0078D4;
            word-break: break-all;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="login-container">
            <div class="logo">☁️</div>
            <div class="title">CloudIDP</div>
            <div class="subtitle">Multi-Cloud Infrastructure Intelligence Platform</div>
            <br>
            <a href="{auth_url}" target="_self" class="ms-button">
                🔷 Sign in with Microsoft
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # DEBUG INFORMATION - Always visible for troubleshooting
        st.markdown("---")
        st.markdown("### 🔍 DEBUG INFORMATION")
        
        st.markdown(f"""
        <div class="debug-box">
            <div class="debug-item">
                <span class="debug-label">Client ID:</span><br>
                <span class="debug-value">{client_id[:10]}...{client_id[-10:]}</span>
            </div>
            <div class="debug-item">
                <span class="debug-label">Tenant ID:</span><br>
                <span class="debug-value">{tenant_id}</span>
            </div>
            <div class="debug-item">
                <span class="debug-label">Redirect URI (from secrets):</span><br>
                <span class="debug-value">{redirect_uri_config}</span>
            </div>
            <div class="debug-item">
                <span class="debug-label">Redirect URI (cleaned, will be sent to Azure):</span><br>
                <span class="debug-value">{redirect_uri}</span>
            </div>
            <div class="debug-item">
                <span class="debug-label">Trailing slash removed?</span><br>
                <span class="debug-value">{'✅ YES' if redirect_uri != redirect_uri_config else '❌ NO (none found)'}</span>
            </div>
            <div class="debug-item">
                <span class="debug-label">URLs match exactly?</span><br>
                <span class="debug-value">{'✅ YES' if redirect_uri == redirect_uri_config.rstrip('/') else '❌ NO'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Critical configuration check
        st.markdown("### ⚠️ CRITICAL: Azure AD Configuration Required")
        
        st.error(f"""
        **In Azure Portal, your Redirect URI MUST be exactly:**
        ```
        {redirect_uri}
        ```
        
        **Steps:**
        1. Go to Azure Portal → App Registrations → Your App
        2. Click "Authentication" in left sidebar
        3. Under "Redirect URIs", ensure this EXACT URL is listed: `{redirect_uri}`
        4. Scroll down, check "ID tokens" under "Implicit grant and hybrid flows"
        5. Click Save
        6. Wait 1-2 minutes for changes to propagate
        7. Come back here and click "Sign in with Microsoft" again
        """)
        
        # Show the actual OAuth URL being used
        with st.expander("🔗 View Full OAuth URL (for advanced debugging)"):
            st.code(auth_url, language="text")
            st.caption("This is the exact URL you'll be redirected to when clicking 'Sign in with Microsoft'")
        
        # Troubleshooting guide
        with st.expander("🛠️ Common Issues & Solutions"):
            st.markdown("""
            ### Issue 1: "Refused to Connect"
            **Cause:** Redirect URI mismatch
            
            **Solution:**
            - Verify the redirect URI above matches EXACTLY in Azure AD
            - No trailing slash in either place
            - Must be HTTPS, not HTTP
            
            ### Issue 2: Page Loads but Still Fails
            **Cause:** Client secret or tenant ID issue
            
            **Solution:**
            - Check client secret is not expired in Azure AD
            - Verify tenant_id is correct ("common" for multitenant)
            
            ### Issue 3: Blank Page or Timeout
            **Cause:** Network or Azure AD service issue
            
            **Solution:**
            - Check your internet connection
            - Try a different browser
            - Clear browser cache
            - Check Azure AD service status
            
            ### Need More Help?
            1. Take a screenshot of the DEBUG INFORMATION above
            2. Take a screenshot of Azure AD → Authentication settings
            3. Compare the redirect URIs - they must match EXACTLY
            """)
        
        st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']
