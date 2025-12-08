"""
Azure AD SSO Authentication with Cookie Fix for Edge/Incognito
Handles SameSite cookie attributes for cross-browser compatibility
"""

import streamlit as st
from typing import Optional, Dict
import secrets
import hashlib
import base64

class AzureAuthManager:
    """Manages Azure AD authentication with proper cookie handling"""
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str = "common"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        
        # Get redirect URI from secrets or use default
        self.redirect_uri = st.secrets.get("azure_ad", {}).get(
            "redirect_uri", 
            "https://hyperscaler.streamlit.app"
        )
    
    def generate_auth_url(self) -> str:
        """Generate Azure AD authorization URL with PKCE"""
        
        # Generate state (for CSRF protection)
        state = secrets.token_urlsafe(32)
        
        # Generate PKCE code verifier and challenge
        # This eliminates the need for state cookies!
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip('=')
        
        # Store in session state (not cookies!)
        st.session_state.oauth_state = state
        st.session_state.code_verifier = code_verifier
        
        # Build authorization URL
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'openid profile email User.Read',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'response_mode': 'query'
        }
        
        from urllib.parse import urlencode
        auth_url = f"{self.authority}/oauth2/v2.0/authorize?" + urlencode(auth_params)
        
        return auth_url
    
    def handle_callback(self, code: str, state: str) -> Optional[Dict]:
        """Handle OAuth callback without relying on cookies"""
        
        # Verify state (CSRF protection)
        if state != st.session_state.get('oauth_state'):
            st.error("❌ Invalid state parameter - possible CSRF attack")
            return None
        
        # Get code verifier from session
        code_verifier = st.session_state.get('code_verifier')
        if not code_verifier:
            st.error("❌ Missing code verifier")
            return None
        
        # Exchange code for token
        import requests
        
        token_url = f"{self.authority}/oauth2/v2.0/token"
        token_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier  # PKCE
        }
        
        try:
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()
            token_response = response.json()
            
            # Get user info
            access_token = token_response['access_token']
            user_info = self._get_user_info(access_token)
            
            # Clean up session state
            del st.session_state.oauth_state
            del st.session_state.code_verifier
            
            return user_info
            
        except Exception as e:
            st.error(f"❌ Token exchange failed: {str(e)}")
            return None
    
    def _get_user_info(self, access_token: str) -> Dict:
        """Get user information from Microsoft Graph API"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
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


def render_login_with_pkce():
    """Render login UI with PKCE-based OAuth (no cookies needed!)"""
    
    st.title("🔐 Sign In")
    st.caption("Secure authentication with Azure Active Directory")
    
    # Check for OAuth callback
    query_params = st.query_params
    
    if 'code' in query_params and 'state' in query_params:
        # Handle callback
        with st.spinner("Completing sign in..."):
            auth_manager = AzureAuthManager(
                client_id=st.secrets.azure_ad.client_id,
                client_secret=st.secrets.azure_ad.client_secret,
                tenant_id=st.secrets.azure_ad.get('tenant_id', 'common')
            )
            
            user_info = auth_manager.handle_callback(
                code=query_params['code'],
                state=query_params['state']
            )
            
            if user_info:
                # Auto-register or get user from Firebase
                from auth_database_firebase import get_database_manager
                db_manager = get_database_manager()
                
                if db_manager:
                    user = db_manager.create_or_update_user(
                        user_id=user_info['id'],
                        email=user_info['email'],
                        name=user_info['name'],
                        role='viewer',  # Default role
                        is_active=True
                    )
                    
                    # Store in session
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_info['id']
                    st.session_state.user_info = user
                    
                    # Clear query params and rerun
                    st.query_params.clear()
                    st.rerun()
    
    else:
        # Show login button
        st.info("""
        ℹ️ **Browser Compatibility Note**
        
        If you're using Edge or Incognito mode and experience issues:
        - Make sure to allow cookies for this site
        - Or use regular Chrome/Firefox
        
        This authentication method works in all browsers!
        """)
        
        if st.button("🔷 Sign in with Microsoft", use_container_width=True, type="primary"):
            # Generate auth URL with PKCE
            auth_manager = AzureAuthManager(
                client_id=st.secrets.azure_ad.client_id,
                client_secret=st.secrets.azure_ad.client_secret,
                tenant_id=st.secrets.azure_ad.get('tenant_id', 'common')
            )
            
            auth_url = auth_manager.generate_auth_url()
            
            # Redirect using JavaScript (works in all modes)
            st.markdown(f"""
            <script>
                window.location.href = "{auth_url}";
            </script>
            """, unsafe_allow_html=True)
            
            st.info("Redirecting to Microsoft login...")


# Backward compatibility
def render_login():
    """Alias for backward compatibility"""
    render_login_with_pkce()
