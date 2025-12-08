"""
Azure AD SSO Authentication - Simple Auto-Redirect Version
Simplified for maximum Streamlit compatibility
"""

import streamlit as st
from typing import Optional, Dict, List, Callable
from functools import wraps
import streamlit.components.v1 as components


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
# AZURE AD AUTHENTICATION
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
            st.error(f"❌ Authentication Failed: {error_desc}")
            return None
        
        return response.json()
        
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
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
    """Render login with auto-redirect to Microsoft"""
    
    # Get Azure AD config
    try:
        client_id = st.secrets.azure_ad.client_id
        client_secret = st.secrets.azure_ad.client_secret
        tenant_id = st.secrets.azure_ad.get('tenant_id', 'common')
        redirect_uri = st.secrets.azure_ad.get('redirect_uri', '').rstrip('/')
        
        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError("Missing required configuration")
            
    except Exception as e:
        st.error("❌ Azure AD Configuration Error")
        st.stop()
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params:
        # Handle OAuth callback
        with st.spinner("🔐 Completing sign-in..."):
            code = query_params['code']
            
            token_response = exchange_code_for_token(
                code=code,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                tenant_id=tenant_id
            )
            
            if token_response and 'access_token' in token_response:
                user_info = get_user_info(token_response['access_token'])
                
                if user_info:
                    try:
                        from auth_database_firebase import get_database_manager
                        db_manager = get_database_manager()
                        
                        if db_manager:
                            user_id = user_info['id']
                            
                            try:
                                existing_user = db_manager.get_user(user_id)
                                is_new_user = not (existing_user and isinstance(existing_user, dict))
                            except:
                                is_new_user = True
                            
                            if is_new_user:
                                user_info['role'] = 'viewer'
                                user_info['is_active'] = True
                                db_manager.create_or_update_user(user_info)
                                final_user_info = user_info
                            else:
                                update_data = {
                                    'id': user_info['id'],
                                    'email': user_info['email'],
                                    'name': user_info.get('name', ''),
                                    'given_name': user_info.get('given_name', ''),
                                    'family_name': user_info.get('family_name', '')
                                }
                                db_manager.create_or_update_user(update_data)
                                
                                try:
                                    final_user_info = db_manager.get_user(user_id)
                                    if not final_user_info:
                                        final_user_info = user_info
                                except:
                                    final_user_info = user_info
                            
                            st.session_state.authenticated = True
                            st.session_state.user_id = final_user_info['id']
                            st.session_state.user_info = final_user_info
                            st.session_state.user_manager = SimpleUserManager()
                            
                            st.query_params.clear()
                            st.success("✅ Login successful!")
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                        if st.button("🔄 Try Again"):
                            st.query_params.clear()
                            st.rerun()
            else:
                if st.button("🔄 Try Again"):
                    st.query_params.clear()
                    st.rerun()
    
    elif 'error' in query_params:
        error = query_params.get('error', ['unknown'])[0]
        error_desc = query_params.get('error_description', ['No description'])[0]
        
        st.error("❌ Authentication Error")
        st.warning(f"**Error:** {error}")
        st.info(error_desc)
        
        if st.button("🔄 Try Again"):
            st.query_params.clear()
            st.rerun()
    
    else:
        # Build OAuth URL and auto-redirect
        from urllib.parse import quote
        
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scopes = "openid profile email https://graph.microsoft.com/User.Read"
        
        auth_url = (
            f"{authority}/oauth2/v2.0/authorize?"
            f"client_id={client_id}&"
            f"response_type=code&"
            f"redirect_uri={quote(redirect_uri, safe='')}&"
            f"response_mode=query&"
            f"scope={quote(scopes)}&"
            f"prompt=select_account"
        )
        
        # Simple redirect page
        st.markdown("# 🔄 Redirecting to Microsoft...")
        st.info("Please wait while we redirect you to sign in.")
        
        # Use Streamlit components for reliable redirect
        redirect_html = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url={auth_url}">
        </head>
        <body>
            <script>
                window.location.replace("{auth_url}");
            </script>
            <p>Redirecting... <a href="{auth_url}">Click here</a> if not redirected automatically.</p>
        </body>
        </html>
        """
        
        components.html(redirect_html, height=100)
        
        st.markdown(f"[Click here if not redirected automatically]({auth_url})")
        
        st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']
