"""
Azure Module: DNS & Traffic
Azure DNS and Traffic Manager
"""

import streamlit as st
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureDNSAndTrafficModule:
    """Azure DNS & Traffic module"""
    
    @staticmethod
    def render():
        """Render Azure DNS & Traffic"""
        
        # Header
        AzureTheme.azure_header(
            "DNS & Traffic",
            "Azure DNS and Traffic Manager",
            "🌍"
        )
        
        # Load subscriptions
        subscriptions = AppConfig.load_azure_subscriptions()
        active_subs = [sub for sub in subscriptions if sub.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box(
                "Demo Mode Active",
                "Displaying sample data for DNS & Traffic. Connect your Azure account to see real data.",
                "info"
            )
        
        # Module content
        AzureTheme.azure_section_header("Overview", "🌍")
        
        st.write("""
        This module provides Azure DNS and Traffic Manager.
        
        **Features:**
        - Subscription-level management
        - Resource monitoring and control
        - Cost tracking and optimization
        - Security and compliance
        """)
        
        # Metrics
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            AzureTheme.azure_metric_card(
                label="Total Items",
                value="247",
                icon="🌍"
            )
        
        with col2:
            AzureTheme.azure_metric_card(
                label="Active",
                value="235",
                icon="✅",
                delta="+12 this week"
            )
        
        with col3:
            AzureTheme.azure_metric_card(
                label="Monthly Cost",
                value="$12.5K",
                icon="💰",
                delta="-$890 (6.6%)"
            )
        
        st.markdown("---")
        
        # Actions
        AzureTheme.azure_section_header("Actions", "⚙️")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", key="dns_traffic_refresh"):
                st.success("Data refreshed successfully!")
        
        with col2:
            if st.button("📊 Generate Report", key="dns_traffic_report"):
                st.success("Report generated successfully!")
        
        with col3:
            if st.button("⚙️ Configure", key="dns_traffic_config"):
                st.info("Configuration options coming soon!")

def render():
    """Module entry point"""
    AzureDNSAndTrafficModule.render()
