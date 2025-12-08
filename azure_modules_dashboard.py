"""
Azure Module: Dashboard
Main overview for Azure subscriptions and resources
"""

import streamlit as st
from azure_theme import AzureTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class AzureDashboardModule:
    """Azure Dashboard module"""
    
    @staticmethod
    @require_permission('view_dashboard')

    def render():
        """Render Azure dashboard"""
        
        # Header
        AzureTheme.azure_header(
            "Azure Dashboard",
            "Overview of your Azure subscriptions and resources",
            "🔷"
        )
        
        # Load subscriptions
        subscriptions = AppConfig.load_azure_subscriptions()
        active_subs = [sub for sub in subscriptions if sub.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box(
                "Demo Mode Active",
                "Displaying sample Azure data for demonstration purposes. Connect your Azure account to see real data.",
                "info"
            )
        
        # Top metrics
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            AzureTheme.azure_metric_card(
                label="Active Subscriptions",
                value=str(len(active_subs)),
                icon="📁",
                delta="+2 this month"
            )
        
        with col2:
            AzureTheme.azure_metric_card(
                label="Total Resources",
                value="12,847",
                icon="📦",
                delta="+458 this week"
            )
        
        with col3:
            AzureTheme.azure_metric_card(
                label="Monthly Cost",
                value="$98,325",
                icon="💰",
                delta="-$5,120 (4.9%)"
            )
        
        with col4:
            AzureTheme.azure_metric_card(
                label="Security Alerts",
                value="8",
                icon="🔒",
                delta="-12 resolved"
            )
        
        st.markdown("---")
        
        # Subscription overview
        AzureTheme.azure_section_header("Subscription Overview", "📋")
        
        # Display subscription cards
        for sub in active_subs:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                AzureTheme.azure_card(
                    title=sub.subscription_name,
                    content=f"""
                    <strong>Subscription ID:</strong> {sub.subscription_id[:8]}...{sub.subscription_id[-4:]}<br>
                    <strong>Environment:</strong> {sub.environment.title()}<br>
                    <strong>Regions:</strong> {', '.join(sub.regions[:3])} {f'(+{len(sub.regions)-3} more)' if len(sub.regions) > 3 else ''}<br>
                    <strong>Cost Center:</strong> {sub.cost_center or 'Not set'}<br>
                    <strong>Owner:</strong> {sub.owner_email or 'Not set'}
                    """,
                    icon="🔷"
                )
            
            with col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown(AzureTheme.azure_status_badge(sub.status), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            AzureTheme.azure_section_header("Cost Trend (30 Days)", "📈")
            st.line_chart({
                "Cost ($)": [92000, 94500, 93200, 95800, 98325]
            })
        
        with col2:
            AzureTheme.azure_section_header("Resource Distribution", "🗂️")
            st.bar_chart({
                "VMs": 245,
                "Storage": 189,
                "SQL DB": 67,
                "Functions": 134,
                "AKS": 23
            })
        
        st.markdown("---")
        
        # Resource health
        AzureTheme.azure_section_header("Resource Health", "💚")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            AzureTheme.azure_progress_bar(92, "Compute Health")
        
        with col2:
            AzureTheme.azure_progress_bar(88, "Storage Health")
        
        with col3:
            AzureTheme.azure_progress_bar(95, "Network Health")
        
        st.markdown("---")
        
        # Recent activity
        AzureTheme.azure_section_header("Recent Activity", "🕐")
        
        activities = [
            {"time": "2 hours ago", "action": "New VM deployed", "subscription": "Production-Main", "status": "success"},
            {"time": "5 hours ago", "action": "Storage account created", "subscription": "Development", "status": "success"},
            {"time": "1 day ago", "action": "AKS cluster scaled", "subscription": "Production-Main", "status": "success"},
            {"time": "2 days ago", "action": "Security alert resolved", "subscription": "Production-Main", "status": "warning"}
        ]
        
        for activity in activities:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
            with col1:
                st.caption(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.caption(activity["subscription"])
            with col4:
                st.markdown(AzureTheme.azure_status_badge(activity["status"]), unsafe_allow_html=True)

def render():
    """Module entry point"""
    AzureDashboardModule.render()
