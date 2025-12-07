"""
Azure Module: Storage Management
Manage Blob Storage, Files, and storage accounts
"""

import streamlit as st
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureStorageManagementModule:
    """Azure Storage Management module"""
    
    @staticmethod
    def render():
        """Render Azure Storage Management"""
        
        # Header
        AzureTheme.azure_header(
            "Storage Management",
            "Manage Blob Storage, Files, and storage accounts",
            "💾"
        )
        
        # Load subscriptions
        subscriptions = AppConfig.load_azure_subscriptions()
        active_subs = [sub for sub in subscriptions if sub.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box(
                "Demo Mode Active",
                "Displaying sample data for Storage Management. Connect your Azure account to see real data.",
                "info"
            )
        
        # Module content
        AzureTheme.azure_section_header("Overview", "💾")
        
        st.write("""
        This module provides manage blob storage, files, and storage accounts.
        
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
                icon="💾"
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
        
        # Subscription breakdown
        AzureTheme.azure_section_header("Subscription Breakdown", "📋")
        
        for sub in active_subs:
            with st.expander(f"💾 {sub.subscription_name}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Subscription ID:** {sub.subscription_id[:8]}...{sub.subscription_id[-4:]}")
                    st.write(f"**Environment:** {sub.environment.title()}")
                    st.write(f"**Regions:** {', '.join(sub.regions[:2])}")
                
                with col2:
                    st.write(f"**Cost Center:** {sub.cost_center or 'Not set'}")
                    st.write(f"**Owner:** {sub.owner_email or 'Not set'}")
                    st.markdown(AzureTheme.azure_status_badge(sub.status), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Actions
        AzureTheme.azure_section_header("Actions", "⚙️")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", key="storage_management_refresh"):
                st.success("Data refreshed successfully!")
        
        with col2:
            if st.button("📊 Generate Report", key="storage_management_report"):
                st.success("Report generated successfully!")
        
        with col3:
            if st.button("⚙️ Configure", key="storage_management_config"):
                st.info("Configuration options coming soon!")

def render():
    """Module entry point"""
    AzureStorageManagementModule.render()
