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
        
        # Clean branded login page with logo
        st.markdown("""
        <style>
        .login-container {
            max-width: 600px;
            margin: 60px auto;
            padding: 50px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
        }
        .logo-container {
            margin-bottom: 30px;
        }
        .logo {
            width: 180px;
            height: 180px;
            margin: 0 auto;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #0078D4;
            margin: 20px 0 10px 0;
        }
        .subtitle {
            font-size: 18px;
            color: #666;
            margin-bottom: 40px;
            font-weight: 500;
        }
        .info-text {
            font-size: 14px;
            color: #999;
            margin-top: 30px;
            line-height: 1.6;
        }
        </style>
        
        <div class="login-container">
            <div class="logo-container">
                <svg class="logo" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <!-- Cloud outline -->
                    <path d="M50 100 Q30 100 30 80 Q30 60 50 60 Q50 40 70 40 Q90 40 90 60 Q110 60 110 40 Q130 40 130 60 Q150 60 150 80 Q170 80 170 100 Q170 120 150 120 Q150 140 130 140 Q110 140 110 120 Q90 120 90 140 Q70 140 70 120 Q50 120 50 100 Z" 
                          fill="none" 
                          stroke="#0078D4" 
                          stroke-width="6"/>
                    
                    <!-- Left brain hemisphere (blue) -->
                    <path d="M75 75 Q75 65 85 65 Q85 75 85 85 L85 90 Q80 90 80 85 Q75 85 75 90 Q70 90 70 85 Q70 75 75 75 Z"
                          fill="#4FC3F7"/>
                    <path d="M75 85 Q75 80 80 80 L80 95 Q75 95 75 90 Z"
                          fill="#29B6F6"/>
                    <path d="M65 95 Q70 95 75 90 Q75 100 70 105 Q65 105 65 100 Z"
                          fill="#0288D1"/>
                    
                    <!-- Right brain top (green) -->
                    <path d="M115 65 Q120 65 120 70 Q125 70 125 75 Q125 85 120 90 Q115 90 115 80 Q115 70 115 65 Z"
                          fill="#66BB6A"/>
                    <path d="M115 80 Q120 80 125 85 Q125 95 120 95 Q115 95 115 85 Z"
                          fill="#4CAF50"/>
                    
                    <!-- Right brain bottom (orange) -->
                    <path d="M115 95 Q120 95 125 100 Q125 110 120 115 Q115 115 115 105 Q110 105 110 100 Q110 95 115 95 Z"
                          fill="#FFA726"/>
                    <path d="M115 105 Q120 105 120 115 Q115 120 115 115 Z"
                          fill="#FF9800"/>
                    
                    <!-- Center divider -->
                    <line x1="100" y1="60" x2="100" y2="125" 
                          stroke="#0078D4" 
                          stroke-width="4"/>
                </svg>
            </div>
            
            <div class="title">Multi Intelligence Cloud Platform</div>
            <div class="subtitle">Secure Enterprise Sign-In</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Prominent sign-in button
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Use Streamlit's link button for best compatibility
        if st.button("🔷 Sign in with Microsoft", type="primary", use_container_width=True):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
        
        # Also provide direct link
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <a href="{auth_url}" style="color: #0078D4; font-size: 16px; text-decoration: none; font-weight: 500;">
                Or click here to sign in →
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; padding: 20px; color: #999; font-size: 13px;">
            <p>✓ Supports work, school, and personal Microsoft accounts</p>
            <p>✓ Enterprise SSO • Secure • Reliable</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']
