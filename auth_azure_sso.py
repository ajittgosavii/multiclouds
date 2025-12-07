"""
Azure AD (Entra ID) SSO Authentication Module
Provides secure multi-user authentication with Azure Active Directory
"""

import streamlit as st
import requests
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib
import json
import os

class AzureSSO:
    """Azure AD SSO Authentication Handler"""
    
    def __init__(self):
        """Initialize Azure SSO with configuration"""
        self.tenant_id = self._get_config('AZURE_TENANT_ID')
        self.client_id = self._get_config('AZURE_CLIENT_ID')
        self.client_secret = self._get_config('AZURE_CLIENT_SECRET')
        self.redirect_uri = self._get_config('AZURE_REDIRECT_URI')
        
        # Azure AD endpoints
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.authorize_endpoint = f"{self.authority}/oauth2/v2.0/authorize"
        self.token_endpoint = f"{self.authority}/oauth2/v2.0/token"
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"
        
        # Scopes
        self.scopes = ["User.Read", "openid", "profile", "email"]
    
    def _get_config(self, key: str) -> str:
        """Get configuration from Streamlit secrets or environment"""
        try:
            return st.secrets.get("azure_sso", {}).get(key.lower(), os.getenv(key, ""))
        except:
            return os.getenv(key, "")
    
    def is_configured(self) -> bool:
        """Check if Azure SSO is properly configured"""
        return all([
            self.tenant_id,
            self.client_id,
            self.client_secret,
            self.redirect_uri
        ])
    
    def get_login_url(self, state: str) -> str:
        """Generate Azure AD login URL"""
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'response_mode': 'query',
            'scope': ' '.join(self.scopes),
            'state': state
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.authorize_endpoint}?{query_string}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access token"""
        try:
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'authorization_code',
                'scope': ' '.join(self.scopes)
            }
            
            response = requests.post(self.token_endpoint, data=data)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            st.error(f"Token exchange failed: {str(e)}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get user information from Microsoft Graph API"""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(f"{self.graph_endpoint}/me", headers=headers)
            response.raise_for_status()
            
            user_data = response.json()
            
            # Get user's photo (optional)
            try:
                photo_response = requests.get(
                    f"{self.graph_endpoint}/me/photo/$value",
                    headers=headers
                )
                if photo_response.status_code == 200:
                    user_data['photo'] = photo_response.content
            except:
                pass  # Photo is optional
            
            return user_data
        except Exception as e:
            st.error(f"Failed to get user info: {str(e)}")
            return None
    
    def decode_id_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Decode ID token (JWT) from Azure AD"""
        try:
            # Note: In production, verify the signature
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            return decoded
        except Exception as e:
            st.error(f"Failed to decode ID token: {str(e)}")
            return None


class UserManager:
    """User management and session handling"""
    
    def __init__(self):
        """Initialize user manager"""
        self.session_timeout = timedelta(hours=8)  # 8 hour session
    
    def create_user_session(self, user_info: Dict[str, Any], token_data: Dict[str, Any]):
        """Create user session in Streamlit state"""
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user_info.get('id'),
            'email': user_info.get('mail') or user_info.get('userPrincipalName'),
            'name': user_info.get('displayName'),
            'given_name': user_info.get('givenName'),
            'surname': user_info.get('surname'),
            'job_title': user_info.get('jobTitle'),
            'department': user_info.get('department'),
            'office_location': user_info.get('officeLocation'),
            'photo': user_info.get('photo'),
            'access_token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'login_time': datetime.now().isoformat(),
            'expires_at': (datetime.now() + self.session_timeout).isoformat()
        }
        
        # Initialize user preferences
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = self._get_default_preferences()
        
        # Log login event
        self._log_login_event(st.session_state.user)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Check session timeout
        expires_at = st.session_state.user.get('expires_at')
        if expires_at:
            if datetime.now() > datetime.fromisoformat(expires_at):
                self.logout()
                return False
        
        return True
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        if self.is_authenticated():
            return st.session_state.user
        return None
    
    def logout(self):
        """Logout user and clear session"""
        user = st.session_state.get('user')
        if user:
            self._log_logout_event(user)
        
        # Clear session state
        for key in ['authenticated', 'user', 'user_preferences']:
            if key in st.session_state:
                del st.session_state[key]
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default user preferences"""
        return {
            'theme': 'light',
            'default_cloud': 'aws',
            'notifications_enabled': True,
            'dashboard_layout': 'default'
        }
    
    def _log_login_event(self, user: Dict[str, Any]):
        """Log user login event"""
        # In production, log to database or audit system
        event = {
            'event': 'login',
            'user_id': user.get('id'),
            'user_email': user.get('email'),
            'timestamp': datetime.now().isoformat(),
            'ip_address': self._get_client_ip()
        }
        # TODO: Store in audit log
        pass
    
    def _log_logout_event(self, user: Dict[str, Any]):
        """Log user logout event"""
        event = {
            'event': 'logout',
            'user_id': user.get('id'),
            'user_email': user.get('email'),
            'timestamp': datetime.now().isoformat()
        }
        # TODO: Store in audit log
        pass
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        # This is a placeholder - actual implementation depends on deployment
        return "unknown"


class RoleManager:
    """Role-based access control (RBAC)"""
    
    # Define roles and permissions
    ROLES = {
        'admin': {
            'name': 'Administrator',
            'description': 'Full access to all features',
            'permissions': ['*']  # All permissions
        },
        'architect': {
            'name': 'Cloud Architect',
            'description': 'Design and provision infrastructure',
            'permissions': [
                'view_dashboard',
                'design_architecture',
                'provision_resources',
                'manage_policies',
                'view_costs',
                'generate_reports'
            ]
        },
        'developer': {
            'name': 'Developer',
            'description': 'Deploy applications and view resources',
            'permissions': [
                'view_dashboard',
                'view_resources',
                'deploy_applications',
                'view_logs',
                'use_devex'
            ]
        },
        'finops': {
            'name': 'FinOps Analyst',
            'description': 'View and analyze costs',
            'permissions': [
                'view_dashboard',
                'view_costs',
                'analyze_costs',
                'generate_reports',
                'view_resources'
            ]
        },
        'security': {
            'name': 'Security Analyst',
            'description': 'View and manage security',
            'permissions': [
                'view_dashboard',
                'view_security',
                'manage_security',
                'view_compliance',
                'generate_reports'
            ]
        },
        'viewer': {
            'name': 'Viewer',
            'description': 'Read-only access',
            'permissions': [
                'view_dashboard',
                'view_resources',
                'view_costs'
            ]
        }
    }
    
    def __init__(self):
        """Initialize role manager"""
        # In production, load from database
        self.user_roles = {}
    
    def assign_role(self, user_id: str, role: str):
        """Assign role to user"""
        if role in self.ROLES:
            self.user_roles[user_id] = role
            # TODO: Store in database
        else:
            raise ValueError(f"Invalid role: {role}")
    
    def get_user_role(self, user_id: str) -> str:
        """Get user's role"""
        return self.user_roles.get(user_id, 'viewer')  # Default to viewer
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission"""
        role = self.get_user_role(user_id)
        permissions = self.ROLES.get(role, {}).get('permissions', [])
        
        # Admin has all permissions
        if '*' in permissions:
            return True
        
        return permission in permissions
    
    def get_role_info(self, role: str) -> Dict[str, Any]:
        """Get role information"""
        return self.ROLES.get(role, {})


def init_authentication():
    """Initialize authentication system"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AzureSSO()
        st.session_state.user_manager = UserManager()
        st.session_state.role_manager = RoleManager()


def require_authentication(func):
    """Decorator to require authentication for functions"""
    def wrapper(*args, **kwargs):
        user_manager = st.session_state.get('user_manager')
        if not user_manager or not user_manager.is_authenticated():
            st.warning("⚠️ Please login to access this feature")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_permission(permission: str):
    """Decorator to require specific permission"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_manager = st.session_state.get('user_manager')
            role_manager = st.session_state.get('role_manager')
            
            if not user_manager or not user_manager.is_authenticated():
                st.warning("⚠️ Please login to access this feature")
                st.stop()
            
            user = user_manager.get_current_user()
            if not role_manager.has_permission(user['id'], permission):
                st.error("❌ You don't have permission to access this feature")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
