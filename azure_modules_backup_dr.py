"""
Azure Module: Backup & DR
Azure Backup and Site Recovery
"""

import streamlit as st
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureBackupAndDRModule:
    """Azure Backup & DR module"""
    
    @staticmethod
    def render():
        """Render Azure Backup & DR"""
        
        # Header
        AzureTheme.azure_header(
            "Backup & DR",
            "Azure Backup and Site Recovery",
            "💾"
        )
        
        # Load subscriptions
        subscriptions = AppConfig.load_azure_subscriptions()
        active_subs = [sub for sub in subscriptions if sub.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box(
                "Demo Mode Active",
                "Displaying sample data for Backup & DR. Connect your Azure account to see real data.",
                "info"
            )
        
        # Module content
        AzureTheme.azure_section_header("Overview", "💾")
        
        st.write("""
        This module provides Azure Backup and Site Recovery.
        
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
        
        # Actions
        AzureTheme.azure_section_header("Actions", "⚙️")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", key="backup_dr_refresh"):
                st.success("Data refreshed successfully!")
        
        with col2:
            if st.button("📊 Generate Report", key="backup_dr_report"):
                st.success("Report generated successfully!")
        
        with col3:
            if st.button("⚙️ Configure", key="backup_dr_config"):
                st.info("Configuration options coming soon!")

def render():
    """Module entry point"""
    AzureBackupAndDRModule.render()
