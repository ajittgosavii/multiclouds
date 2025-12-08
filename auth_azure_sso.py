"""
Azure AD SSO Authentication - ULTRA DEBUG VERSION
Maximum diagnostics to identify the exact issue
"""

import streamlit as st
from typing import Optional, Dict, List, Callable
from functools import wraps
import json


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
# AZURE AD AUTHENTICATION - ULTRA DEBUG VERSION
# ============================================================================

def test_azure_ad_connectivity(client_id: str, tenant_id: str) -> Dict:
    """Test basic connectivity to Azure AD"""
    import requests
    
    results = {
        'discovery_endpoint': False,
        'authorization_endpoint': False,
        'token_endpoint': False,
        'details': {}
    }
    
    try:
        # Test OpenID Connect discovery endpoint
        discovery_url = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
        response = requests.get(discovery_url, timeout=5)
        
        if response.status_code == 200:
            results['discovery_endpoint'] = True
            config = response.json()
            results['details']['authorization_endpoint'] = config.get('authorization_endpoint')
            results['details']['token_endpoint'] = config.get('token_endpoint')
            results['authorization_endpoint'] = True
            results['token_endpoint'] = True
        else:
            results['details']['error'] = f"Discovery failed: {response.status_code}"
    except Exception as e:
        results['details']['error'] = str(e)
    
    return results


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
            
            st.error(f"❌ Token Exchange Failed")
            
            with st.expander("🔍 View Error Details", expanded=True):
                st.code(error_desc)
                st.json(error_data)
            
            return None
        
        return response.json()
        
    except Exception as e:
        st.error(f"❌ Token exchange error: {str(e)}")
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
    """Render login UI with ULTRA DEBUG information"""
    
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
        st.code(str(e))
        st.stop()
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params:
        # User returned from Microsoft with authorization code
        with st.spinner("🔐 Completing sign-in..."):
            code = query_params['code']
            
            st.info(f"📥 Received authorization code (length: {len(code)} characters)")
            
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
                        if st.button("🔄 Try Again"):
                            st.query_params.clear()
                            st.rerun()
                else:
                    st.error("❌ Could not retrieve user information")
                    if st.button("🔄 Try Again"):
                        st.query_params.clear()
                        st.rerun()
            else:
                # Token exchange failed
                if st.button("🔄 Try Again"):
                    st.query_params.clear()
                    st.rerun()
    
    elif 'error' in query_params:
        # User cancelled or error occurred at Microsoft
        error = query_params.get('error', ['unknown'])[0]
        error_desc = query_params.get('error_description', ['No description'])[0]
        
        st.error("❌ Authentication Error from Microsoft")
        st.warning(f"**Error Code:** {error}")
        st.info(error_desc)
        
        if st.button("🔄 Try Again"):
            st.query_params.clear()
            st.rerun()
    
    else:
        # Show login page with ULTRA DEBUG
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
        
        # Test Azure AD connectivity
        st.markdown("### 🔬 Running Diagnostics...")
        with st.spinner("Testing Azure AD connectivity..."):
            connectivity = test_azure_ad_connectivity(client_id, tenant_id)
        
        # Display login page
        st.markdown("""
        <style>
        .login-container {
            max-width: 600px;
            margin: 30px auto;
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
        
        st.markdown("---")
        
        # ULTRA DEBUG SECTION
        st.markdown("## 🔍 ULTRA DEBUG DIAGNOSTICS")
        
        # Connectivity Test Results
        col1, col2, col3 = st.columns(3)
        with col1:
            if connectivity['discovery_endpoint']:
                st.success("✅ Discovery Endpoint")
            else:
                st.error("❌ Discovery Endpoint")
        
        with col2:
            if connectivity['authorization_endpoint']:
                st.success("✅ Auth Endpoint")
            else:
                st.error("❌ Auth Endpoint")
        
        with col3:
            if connectivity['token_endpoint']:
                st.success("✅ Token Endpoint")
            else:
                st.error("❌ Token Endpoint")
        
        # Configuration Details
        with st.expander("📋 Configuration Details", expanded=True):
            st.markdown("### Current Configuration")
            
            config_data = {
                "Client ID": f"{client_id[:15]}...{client_id[-15:]}",
                "Tenant ID": tenant_id,
                "Redirect URI (from secrets)": redirect_uri_config,
                "Redirect URI (cleaned)": redirect_uri,
                "Authority": authority,
                "Scopes": scopes
            }
            
            for key, value in config_data.items():
                st.text(f"{key}: {value}")
            
            st.markdown("### Validation Checks")
            checks = {
                "Has trailing slash": redirect_uri_config != redirect_uri,
                "Uses HTTPS": redirect_uri.startswith('https://'),
                "Tenant ID format": tenant_id in ['common', 'organizations', 'consumers'] or len(tenant_id) == 36,
                "Client ID format": len(client_id) == 36,
                "Redirect URI matches": redirect_uri == "https://hyperscaler.streamlit.app"
            }
            
            for check, result in checks.items():
                if result:
                    st.success(f"✅ {check}")
                else:
                    st.error(f"❌ {check}")
        
        # OAuth URL Details
        with st.expander("🔗 OAuth URL Being Used"):
            st.code(auth_url, language="text")
            
            st.markdown("### URL Components:")
            st.json({
                "authority": authority,
                "endpoint": "/oauth2/v2.0/authorize",
                "client_id": client_id[:20] + "...",
                "response_type": "code",
                "redirect_uri": redirect_uri,
                "response_mode": "query",
                "scope": scopes,
                "prompt": "select_account"
            })
        
        # Azure AD Requirements
        with st.expander("⚠️ Azure AD Configuration Requirements"):
            st.markdown(f"""
            ### Critical: Verify in Azure Portal
            
            **1. Redirect URI Must Be:**
            ```
            {redirect_uri}
            ```
            
            **2. Platform: Web**
            - Not SPA (Single Page Application)
            - Not Mobile
            - Must be "Web" platform
            
            **3. Implicit Grant:**
            - ✅ ID tokens (must be checked)
            - ✅ Access tokens (recommended)
            
            **4. API Permissions:**
            - Microsoft Graph → User.Read (Delegated)
            - openid, profile, email
            
            **5. Supported Account Types:**
            - For tenant_id="common": "Accounts in any organizational directory"
            - Must match your tenant_id setting
            
            **6. Client Secret:**
            - Must not be expired
            - Must be the VALUE, not the Secret ID
            """)
        
        # Browser Test
        with st.expander("🌐 Browser Compatibility Test"):
            st.markdown("""
            **Current Browser Information:**
            - JavaScript is enabled (Streamlit requires it)
            - Cookies are enabled (required for OAuth)
            - Can you access login.microsoftonline.com directly?
            
            **Test:** [Click here to test Microsoft login endpoint](https://login.microsoftonline.com/)
            
            If that link doesn't work, you have a network/firewall issue blocking Microsoft services.
            """)
        
        # Network Diagnostics
        if not all(connectivity.values()):
            st.error("🔴 **Network Connectivity Issue Detected**")
            st.warning("""
            Azure AD endpoints are not reachable. This could be due to:
            - Corporate firewall blocking Microsoft services
            - VPN or proxy issues
            - Network restrictions
            - ISP blocking
            
            **Try:**
            1. Disable VPN
            2. Try from a different network
            3. Check with your IT department about firewall rules
            4. Try from mobile hotspot
            """)
        
        # Common Issues Guide
        with st.expander("🆘 Common Issues & Solutions"):
            st.markdown("""
            ### Issue: "Refused to Connect"
            
            **Most Common Causes:**
            
            1. **Redirect URI Mismatch** (even though yours looks correct)
               - Azure shows: `https://hyperscaler.streamlit.app`
               - Code sends: `https://hyperscaler.streamlit.app`
               - But Azure might have multiple URIs and matching wrong one
               - **Try:** Remove ALL other redirect URIs in Azure, keep only base URL
            
            2. **Platform Type Wrong**
               - You might have "SPA" instead of "Web"
               - **Fix:** Azure AD → Authentication → Add "Web" platform
            
            3. **ID Tokens Not Enabled**
               - **Fix:** Check "ID tokens" box in Azure AD
            
            4. **Tenant ID Mismatch**
               - Multitenant app needs "common" or "organizations"
               - **Current:** {tenant_id}
            
            5. **Network/Firewall**
               - Corporate firewall blocking OAuth
               - **Test:** Try from personal device/network
            
            6. **Browser Extensions**
               - Privacy/ad blockers interfering
               - **Test:** Disable ALL extensions
            
            7. **App Permissions Not Granted**
               - Need admin consent for API permissions
               - **Fix:** Azure AD → API permissions → Grant admin consent
            """)
        
        st.stop()


__all__ = ['RoleManager', 'require_permission', 'SimpleUserManager', 'render_login']
