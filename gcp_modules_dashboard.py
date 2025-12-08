"""
GCP Module: Dashboard
Main overview for Google Cloud Platform projects and resources
"""

import streamlit as st
from gcp_theme import GCPTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class GCPDashboardModule:
    """GCP Dashboard module"""
    
    @staticmethod
    @require_permission('view_dashboard')

    def render():
        """Render GCP dashboard"""
        
        # Header
        GCPTheme.gcp_header(
            "GCP Dashboard",
            "Overview of your Google Cloud Platform projects and resources",
            "🔴"
        )
        
        # Load projects
        projects = AppConfig.load_gcp_projects()
        active_projects = [proj for proj in projects if proj.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box(
                "Demo Mode Active",
                "Displaying sample Google Cloud data for demonstration purposes. Connect your GCP account to see real data.",
                "info"
            )
        
        # Top metrics with Google's color scheme
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            GCPTheme.gcp_metric_card(
                label="Active Projects",
                value=str(len(active_projects)),
                icon="📁",
                delta="+3 this month",
                metric_type="default"
            )
        
        with col2:
            GCPTheme.gcp_metric_card(
                label="Total Resources",
                value="8,432",
                icon="📦",
                delta="+234 this week",
                metric_type="performance"
            )
        
        with col3:
            GCPTheme.gcp_metric_card(
                label="Monthly Cost",
                value="$67,845",
                icon="💰",
                delta="-$3,120 (4.4%)",
                metric_type="cost"
            )
        
        with col4:
            GCPTheme.gcp_metric_card(
                label="Security Findings",
                value="5",
                icon="🔒",
                delta="-9 resolved",
                metric_type="alert"
            )
        
        # Google's signature multi-color divider
        GCPTheme.gcp_multi_color_divider()
        
        # Project overview
        GCPTheme.gcp_section_header("Project Overview", "📋")
        
        # Display project cards with different accents
        accents = ["blue", "red", "yellow", "green"]
        for idx, proj in enumerate(active_projects):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                GCPTheme.gcp_card(
                    title=proj.project_name,
                    content=f"""
                    <strong>Project ID:</strong> {proj.project_id}<br>
                    <strong>Project Number:</strong> {proj.project_number}<br>
                    <strong>Environment:</strong> {proj.environment.title()}<br>
                    <strong>Regions:</strong> {', '.join(proj.regions[:3])} {f'(+{len(proj.regions)-3} more)' if len(proj.regions) > 3 else ''}<br>
                    <strong>Billing Account:</strong> {proj.billing_account_id[:8]}...{proj.billing_account_id[-4:]}<br>
                    <strong>Cost Center:</strong> {proj.cost_center or 'Not set'}<br>
                    <strong>Owner:</strong> {proj.owner_email or 'Not set'}
                    """,
                    icon="🔴",
                    accent=accents[idx % len(accents)]
                )
            
            with col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown(GCPTheme.gcp_status_badge(proj.status), unsafe_allow_html=True)
        
        GCPTheme.gcp_multi_color_divider()
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            GCPTheme.gcp_section_header("Cost Trend (30 Days)", "📈")
            st.line_chart({
                "Cost ($)": [62000, 64500, 63800, 66200, 67845]
            })
        
        with col2:
            GCPTheme.gcp_section_header("Resource Distribution", "🗂️")
            st.bar_chart({
                "Compute Engine": 189,
                "Cloud Storage": 234,
                "Cloud SQL": 45,
                "Cloud Functions": 156,
                "GKE": 18
            })
        
        GCPTheme.gcp_multi_color_divider()
        
        # Resource health with Google colors
        GCPTheme.gcp_section_header("Resource Health", "💚")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            GCPTheme.gcp_progress_bar(94, "Compute Health", "green")
        
        with col2:
            GCPTheme.gcp_progress_bar(89, "Storage Health", "blue")
        
        with col3:
            GCPTheme.gcp_progress_bar(96, "Network Health", "green")
        
        GCPTheme.gcp_multi_color_divider()
        
        # Recent activity
        GCPTheme.gcp_section_header("Recent Activity", "🕐")
        
        activities = [
            {"time": "1 hour ago", "action": "New VM instance created", "project": "Production Main", "status": "success"},
            {"time": "4 hours ago", "action": "Cloud Function deployed", "project": "Development", "status": "success"},
            {"time": "8 hours ago", "action": "GKE cluster updated", "project": "Production Main", "status": "success"},
            {"time": "1 day ago", "action": "Security finding addressed", "project": "Production Main", "status": "warning"}
        ]
        
        for activity in activities:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
            with col1:
                st.caption(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.caption(activity["project"])
            with col4:
                st.markdown(GCPTheme.gcp_status_badge(activity["status"]), unsafe_allow_html=True)

def render():
    """Module entry point"""
    GCPDashboardModule.render()
