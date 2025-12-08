"""
Azure AD SSO Authentication - Streamlit Compatible
Uses query parameter state management to work with Streamlit redirects
"""

import streamlit as st
from typing import Optional, Dict, List, Callable
from functools import wraps
import secrets
import hashlib


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
                'view_dashboard',
                'view_resources',
                'provision_resources',
                'design_architecture',
                'use_devex',
                'view_costs',
                'manage_policies'
            ]
        },
        'developer': {
            'description': 'Deploy and manage applications',
            'permissions': [
                'view_dashboard',
                'view_resources',
                'deploy_applications',
                'use_devex'
            ]
        },
        'finops': {
            'description': 'Financial operations and cost management',
            'permissions': [
                'view_dashboard',
                'view_costs'
            ]
        },
        'security': {
            'description': 'Security and compliance management',
            'permissions': [
                'view_dashboard',
                'view_security'
            ]
        },
        'viewer': {
            'description': 'Read-only access',
            'permissions': [
                'view_dashboard',
                'view_resources',
                'view_costs'
            ]
        }
    }
    
    @staticmethod
    def has_permission(user_role: str, required_permission: str) -> bool:
        """Check if a role has a specific permission"""
        
        if not user_role or user_role not in RoleManager.ROLES:
            return False
        
        role_permissions = RoleManager.ROLES[user_role]['permissions']
        
        if '*' in role_permissions:
            return True
        
        return required_permission in role_permissions
    
    @staticmethod
    def get_user_permissions(user_role: str) -> List[str]:
        """Get all permissions for a role"""
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
                st.info("Please login to access this feature")
                return
            
            current_user = user_manager.get_current_user()
            if not current_user:
                st.error("❌ User session not found")
                st.info("Please logout and login again")
                return
            
            user_role = current_user.get('role', 'viewer')
            
            if not RoleManager.has_permission(user_role, permission):
                st.error("❌ You don't have permission to access this feature")
                st.info(f"""
                **Required permission:** `{permission}`  
                **Your role:** `{user_role}`  
                
                Contact your administrator to request access.
                """)
                
                try:
                    from auth_database_firebase import get_database_manager
                    db_manager = get_database_manager()
                    if db_manager:
                        db_manager.log_event(
                            user_id=current_user['id'],
                            event_type='permission_denied',
                            event_data={
                                'permission': permission,
                                'role': user_role,
                                'module': func.__name__
                            }
                        )
                except:
                    pass
                
                return
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# ============================================================================
# SIMPLE USER MANAGER
# ============================================================================

class SimpleUserManager:
    """Simple user manager for session"""
    
    def __init__(self):
        pass
    
    def get_current_user(self):
        """Get current user from session"""
        return st.session_state.get('user_info')
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)


# ============================================================================
# AZURE AD AUTHENTICATION - SIMPLE VERSION
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
        'grant_type': 'authorization_code'
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Token exchange failed: {str(e)}")
        return None


def get_user_info(access_token: str) -> Optional[Dict]:
    """Get user information from Microsoft Graph"""
    import requests
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers=headers
        )
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
    """Render login UI - Simple version that works with Streamlit"""
    
    st.title("🔐 Sign In")
    st.caption("Secure authentication with Azure Active Directory")
    
    # Get Azure AD config
    try:
        client_id = st.secrets.azure_ad.client_id
        client_secret = st.secrets.azure_ad.client_secret
        tenant_id = st.secrets.azure_ad.get('tenant_id', 'common')
        redirect_uri = st.secrets.azure_ad.get('redirect_uri', st.secrets.azure_ad.get('redirect_url', ''))
    except Exception as e:
        st.error(f"❌ Azure AD configuration missing: {str(e)}")
        st.info("""
        Please add Azure AD secrets to Streamlit Cloud:
        
        ```toml
        [azure_ad]
        client_id = "your-client-id"
        client_secret = "your-client-secret"
        tenant_id = "common"
        redirect_uri = "https://your-app.streamlit.app"
        ```
        """)
        return
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params:
        # Handle callback
        with st.spinner("Completing sign in..."):
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
                # Get user info
                user_info = get_user_info(token_response['access_token'])
                
                if user_info:
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
                            
                            # Clear query params and rerun
                            st.query_params.clear()
                            st.success("✅ Login successful!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Failed to register user: {str(e)}")
                        st.stop()
    
    else:
        # Show login button
        st.info("""
        ℹ️ **Secure Authentication**
        
        Sign in with your Microsoft account to access CloudIDP.
        
        - Enterprise Azure AD accounts
        - Personal Microsoft accounts
        - Office 365 accounts
        """)
        
        if st.button("🔷 Sign in with Microsoft", use_container_width=True, type="primary"):
            # Build authorization URL
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
            
            # Redirect using meta refresh (most compatible)
            st.markdown(f"""
            <meta http-equiv="refresh" content="0;url={auth_url}">
            <p>Redirecting to Microsoft login...</p>
            <p>If you are not redirected, <a href="{auth_url}" target="_self">click here</a>.</p>
            """, unsafe_allow_html=True)
            
            st.stop()


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'RoleManager',
    'require_permission',
    'SimpleUserManager',
    'render_login'
]