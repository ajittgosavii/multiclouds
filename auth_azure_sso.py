"""
Azure AD SSO Authentication - DEBUG VERSION
Shows detailed error messages for troubleshooting
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
            if not current_user:
                st.error("❌ User session not found")
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

def exchange_code_for_token_debug(code: str, client_id: str, client_secret: str, 
                                  redirect_uri: str, tenant_id: str = "common") -> Optional[Dict]:
    """Exchange authorization code for access token - WITH DEBUGGING"""
    import requests
    
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'scope': 'openid profile email User.Read'
    }
    
    # Debug output
    st.write("🔍 **Debug Info:**")
    st.write(f"- Token URL: `{token_url}`")
    st.write(f"- Client ID: `{client_id[:10]}...{client_id[-10:]}`")
    st.write(f"- Redirect URI: `{redirect_uri}`")
    st.write(f"- Code: `{code[:20]}...` (length: {len(code)})")
    
    try:
        response = requests.post(token_url, data=token_data)
        
        # Show response status
        st.write(f"- Response Status: `{response.status_code}`")
        
        if response.status_code != 200:
            # Show detailed error
            try:
                error_data = response.json()
                st.error("❌ **Token Exchange Failed!**")
                st.json(error_data)
                
                # Common error messages and fixes
                error_code = error_data.get('error')
                error_desc = error_data.get('error_description', '')
                
                if 'redirect_uri' in error_desc.lower():
                    st.warning("""
                    **🔧 Redirect URI Mismatch!**
                    
                    The redirect_uri in your token request doesn't match what was used in the authorization request.
                    
                    **Fix:**
                    1. Check your Azure AD App Registration → Authentication
                    2. Make sure this EXACT URL is listed:
                       `""" + redirect_uri + """`
                    3. No trailing slash, exact match required
                    """)
                
                elif 'client_secret' in error_desc.lower() or 'credentials' in error_desc.lower():
                    st.warning("""
                    **🔧 Invalid Client Secret!**
                    
                    The client_secret is incorrect or expired.
                    
                    **Fix:**
                    1. Go to Azure Portal → App Registration → Certificates & secrets
                    2. Generate a new client secret
                    3. Copy the VALUE (not the Secret ID)
                    4. Update in Streamlit Secrets
                    """)
                
                elif 'code' in error_desc.lower():
                    st.warning("""
                    **🔧 Invalid or Expired Code!**
                    
                    The authorization code is invalid, expired, or already used.
                    
                    **Fix:**
                    1. Authorization codes can only be used once
                    2. They expire after 10 minutes
                    3. Try logging in again (click "Sign in with Microsoft")
                    """)
                
            except:
                st.error(f"Response: {response.text}")
            
            return None
        
        token_response = response.json()
        st.success("✅ Token exchange successful!")
        return token_response
        
    except Exception as e:
        st.error(f"❌ Exception during token exchange: {str(e)}")
        st.exception(e)
        return None


def get_user_info(access_token: str) -> Optional[Dict]:
    """Get user information from Microsoft Graph"""
    import requests
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
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
    """Render login UI with debugging"""
    
    st.title("🔐 Sign In - DEBUG MODE")
    st.caption("Showing detailed debug information")
    
    # Get Azure AD config
    try:
        client_id = st.secrets.azure_ad.client_id
        client_secret = st.secrets.azure_ad.client_secret
        tenant_id = st.secrets.azure_ad.get('tenant_id', 'common')
        redirect_uri = st.secrets.azure_ad.get('redirect_uri', '')
        
        # Show config (partially masked)
        with st.expander("📋 Azure AD Configuration"):
            st.write(f"- Client ID: `{client_id[:10]}...{client_id[-10:]}`")
            st.write(f"- Client Secret: `{'*' * 20}`")
            st.write(f"- Tenant ID: `{tenant_id}`")
            st.write(f"- Redirect URI: `{redirect_uri}`")
        
    except Exception as e:
        st.error(f"❌ Azure AD configuration missing: {str(e)}")
        st.info("""
        **Add these to Streamlit Secrets:**
        ```toml
        [azure_ad]
        client_id = "your-client-id"
        client_secret = "your-client-secret"
        tenant_id = "common"
        redirect_uri = "https://hyperscaler.streamlit.app"
        ```
        """)
        return
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params:
        st.info("🔄 Processing OAuth callback...")
        
        # Show query params
        with st.expander("📋 Query Parameters"):
            for key, value in query_params.items():
                if key == 'code':
                    st.write(f"- {key}: `{value[:20]}...` (length: {len(value)})")
                else:
                    st.write(f"- {key}: `{value}`")
        
        code = query_params['code']
        
        # Exchange code for token (with debugging)
        token_response = exchange_code_for_token_debug(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            tenant_id=tenant_id
        )
        
        if token_response and 'access_token' in token_response:
            st.success("✅ Got access token!")
            
            # Get user info
            user_info = get_user_info(token_response['access_token'])
            
            if user_info:
                st.success(f"✅ Got user info: {user_info.get('name')}")
                
                # Auto-register or update user in Firebase
                try:
                    from auth_database_firebase import get_database_manager
                    db_manager = get_database_manager()
                    
                    if db_manager:
                        user = db_manager.create_or_update_user(
                            user_id=user_info['id'],
                            email=user_info['email'],
                            name=user_info['name'],
                            role='viewer',
                            is_active=True
                        )
                        
                        # Store in session
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_info['id']
                        st.session_state.user_info = user
                        st.session_state.user_manager = SimpleUserManager()
                        
                        st.success("✅ User registered in Firebase!")
                        st.success("✅ Login successful! Redirecting...")
                        
                        # Clear query params and rerun
                        st.query_params.clear()
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to register user in Firebase: {str(e)}")
                    st.exception(e)
        else:
            st.error("❌ Token exchange failed. See details above.")
            
            if st.button("🔄 Try Again"):
                st.query_params.clear()
                st.rerun()
    
    else:
        # Show login button
        st.info("Click below to sign in with Microsoft")
        
        if st.button("🔷 Sign in with Microsoft", use_container_width=True, type="primary"):
            from urllib.parse import urlencode
            
            authority = f"https://login.microsoftonline.com/{tenant_id}"
            
            auth_params = {
                'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': 'openid profile email User.Read',
                'response_mode': 'query'
            }
            
            auth_url = f"{authority}/oauth2/v2.0/authorize?" + urlencode(auth_params)
            
            # Show auth URL
            with st.expander("🔗 Authorization URL"):
                st.code(auth_url)
            
            # Redirect
            st.markdown(f"""
            <meta http-equiv="refresh" content="0;url={auth_url}">
            <p>Redirecting to Microsoft login...</p>
            <p>If you are not redirected, <a href="{auth_url}" target="_self">click here</a>.</p>
            """, unsafe_allow_html=True)
            
            st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']