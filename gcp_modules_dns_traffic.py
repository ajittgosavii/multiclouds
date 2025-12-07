"""
GCP Module: DNS & Traffic
Cloud DNS and load balancing
"""

import streamlit as st
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPDNSAndTrafficModule:
    """GCP DNS & Traffic module"""
    
    @staticmethod
    def render():
        """Render GCP DNS & Traffic"""
        
        # Header
        GCPTheme.gcp_header(
            "DNS & Traffic",
            "Cloud DNS and load balancing",
            "🌍"
        )
        
        # Load projects
        projects = AppConfig.load_gcp_projects()
        active_projects = [proj for proj in projects if proj.status == 'active']
        
        # Demo mode indicator
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box(
                "Demo Mode Active",
                "Displaying sample data for DNS & Traffic. Connect your GCP account to see real data.",
                "info"
            )
        
        # Module content
        GCPTheme.gcp_section_header("Overview", "🌍")
        
        st.write("""
        This module provides Cloud DNS and load balancing.
        
        **Features:**
        - Project-level management
        - Resource monitoring and control
        - Cost tracking and optimization
        - Security and compliance
        """)
        
        # Metrics with Google colors
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            GCPTheme.gcp_metric_card(
                label="Total Items",
                value="189",
                icon="🌍",
                metric_type="default"
            )
        
        with col2:
            GCPTheme.gcp_metric_card(
                label="Active",
                value="178",
                icon="✅",
                delta="+9 this week",
                metric_type="performance"
            )
        
        with col3:
            GCPTheme.gcp_metric_card(
                label="Monthly Cost",
                value="$8.7K",
                icon="💰",
                delta="-$620 (6.7%)",
                metric_type="cost"
            )
        
        GCPTheme.gcp_multi_color_divider()
        
        # Project breakdown
        GCPTheme.gcp_section_header("Project Breakdown", "📋")
        
        accents = ["blue", "red", "yellow", "green"]
        for idx, proj in enumerate(active_projects):
            with st.expander(f"{icon} {{proj.project_name}}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Project ID:** {{proj.project_id}}")
                    st.write(f"**Environment:** {{proj.environment.title()}}")
                    st.write(f"**Regions:** {{', '.join(proj.regions[:2])}}")
                
                with col2:
                    st.write(f"**Cost Center:** {{proj.cost_center or 'Not set'}}")
                    st.write(f"**Owner:** {{proj.owner_email or 'Not set'}}")
                    st.markdown(GCPTheme.gcp_status_badge(proj.status), unsafe_allow_html=True)
        
        GCPTheme.gcp_multi_color_divider()
        
        # Actions
        GCPTheme.gcp_section_header("Actions", "⚙️")
        
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
    GCPDNSAndTrafficModule.render()
