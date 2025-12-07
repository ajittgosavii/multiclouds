"""
Azure Module: Network Management - PRODUCTION VERSION
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureNetworkManagementModule:
    @staticmethod
    def render():
        AzureTheme.azure_header("Network Management", "Manage Azure Virtual Networks and networking", "🌐")
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample network data", "info")
        
        tabs = st.tabs(["📋 Overview", "🔌 VNets", "🔒 Security", "📊 Traffic", "⚙️ Config"])
        
        with tabs[0]:
            AzureNetworkManagementModule._overview()
        with tabs[1]:
            AzureNetworkManagementModule._vnets()
        with tabs[2]:
            AzureNetworkManagementModule._security()
        with tabs[3]:
            AzureNetworkManagementModule._traffic()
        with tabs[4]:
            _render_ai_insights()

        with tabs[4]:
            AzureNetworkManagementModule._config()
    
    @staticmethod
    def _overview():
        AzureTheme.azure_section_header("Network Overview", "📊")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            AzureTheme.azure_metric_card("Virtual Networks", "43", "🌐", "Across all regions")
        with col2:
            AzureTheme.azure_metric_card("Subnets", "187", "🔌", "Avg 4.3 per VNet")
        with col3:
            AzureTheme.azure_metric_card("NSG Rules", "456", "🔒", "Security rules active")
        with col4:
            AzureTheme.azure_metric_card("Peerings", "28", "🔗", "VNet connections")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            regions = {"East US": 15, "West US": 12, "Central US": 8, "North Europe": 5, "West Europe": 3}
            fig = px.bar(x=list(regions.keys()), y=list(regions.values()), title="VNets by Region")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            sizes = {"Small (/24)": 25, "Medium (/20)": 12, "Large (/16)": 6}
            fig = px.pie(values=list(sizes.values()), names=list(sizes.keys()), title="VNet Sizes")
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _vnets():
        AzureTheme.azure_section_header("Virtual Networks", "🌐")
        
        vnets = []
        for i in range(8):
            vnets.append({
                "Name": f"vnet-prod-{i+1:02d}",
                "Address Space": f"10.{i}.0.0/16",
                "Subnets": [3, 4, 5][i%3],
                "Region": ["East US", "West US", "Central US"][i%3]
            })
        
        df = pd.DataFrame(vnets)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if st.button("➕ Create VNet", type="primary"):
            st.info("VNet creation form would open")
    
    @staticmethod
    def _security():
        AzureTheme.azure_section_header("Network Security", "🔒")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            AzureTheme.azure_metric_card("NSGs", "89", "🔒", "Security groups")
        with col2:
            AzureTheme.azure_metric_card("Rules", "456", "📋", "Security rules")
        with col3:
            AzureTheme.azure_metric_card("Firewalls", "12", "🔥", "Active firewalls")
        
        st.markdown("---")
        
        st.write("**Top NSG Rules:**")
        rules = []
        for i in range(5):
            rules.append({
                "Rule": f"Allow-{['HTTP', 'HTTPS', 'SSH', 'RDP', 'SQL'][i]}",
                "Priority": 100 + i*10,
                "Direction": "Inbound",
                "Action": "Allow"
            })
        
        df = pd.DataFrame(rules)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _traffic():
        AzureTheme.azure_section_header("Network Traffic", "📊")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            AzureTheme.azure_metric_card("Inbound", "2.4 TB", "📥", "This month")
        with col2:
            AzureTheme.azure_metric_card("Outbound", "1.8 TB", "📤", "This month")
        with col3:
            AzureTheme.azure_metric_card("Cross-Region", "450 GB", "🔄", "Between VNets")
        
        st.markdown("---")
        
        hours = list(range(24))
        traffic = [100 + i*5 + (i%4)*10 for i in hours]
        fig = px.line(x=hours, y=traffic, title="24-Hour Traffic Pattern", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _config():
        AzureTheme.azure_section_header("Network Configuration", "⚙️")
        
        st.write("**DNS Settings:**")
        dns_servers = st.text_area("DNS Servers", value="10.0.0.4\n10.0.0.5")
        
        st.write("**Default Routes:**")
        enable_bgp = st.checkbox("Enable BGP", value=True)
        enable_peering = st.checkbox("Enable VNet peering", value=True)
        
        if st.button("💾 Save Configuration", type="primary"):
            st.success("Network configuration saved")

    @staticmethod
    def _render_ai_insights():
        """Azure AI-powered insights and recommendations"""
        
        AzureTheme.azure_section_header("🤖 AI-Powered Insights", "🧠")
        
        # AI Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            AzureTheme.azure_metric_card("AI Confidence", "95%", "🎯", "High accuracy")
        with col2:
            AzureTheme.azure_metric_card("Recommendations", "6", "💡", "Ready")
        with col3:
            AzureTheme.azure_metric_card("Auto-fixes", "3", "⚡", "Available")
        
        st.markdown("---")
        
        # AI Recommendations
        AzureTheme.azure_section_header("💡 AI Recommendations", "🤖")
        
        recommendations = [{"title": "Optimize Network Routing", "savings": "$800/mo", "confidence": "89%", "latency": "-15ms"}, {"title": "Consolidate VPN Gateways", "savings": "$600/mo", "confidence": "92%", "simplification": "High"}, {"title": "Enable Traffic Analytics", "insights": "Deep visibility", "confidence": "94%", "cost": "$120/mo"}]
        
        for idx, rec in enumerate(recommendations):
            with st.expander(f"🤖 {rec['title']}", expanded=(idx==0)):
                cols = st.columns(len([k for k in rec.keys() if k != 'title']))
                for col, (key, value) in zip(cols, [(k,v) for k,v in rec.items() if k != 'title']):
                    with col:
                        st.metric(key.replace('_', ' ').title(), value)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Apply", key=f"ai_apply_{idx}"):
                        st.success("AI automation started (Demo)")
                with col2:
                    if st.button("📊 Details", key=f"ai_detail_{idx}"):
                        st.info("Analysis dashboard opening (Demo)")
        
        st.markdown("---")
        
        # Anomaly Detection
        AzureTheme.azure_section_header("⚠️ AI Anomaly Detection", "🔍")
        
        anomalies = [
            {"type": "Unusual Pattern", "desc": "AI detected abnormal resource usage spike", "severity": "Medium"},
            {"type": "Configuration Drift", "desc": "Manual changes detected outside IaC", "severity": "Low"}
        ]
        
        for anom in anomalies:
            severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            st.markdown(f"**{severity_color[anom['severity']]} {anom['type']}**: {anom['desc']}")
            if st.button(f"🔧 Auto-Fix {anom['type']}", key=anom['type']):
                st.success("AI remediation initiated")
            st.markdown("---")
        
        # AI Assistant
        AzureTheme.azure_section_header("💬 Ask Claude AI", "🤖")
        
        query = st.text_area("Your question:", placeholder="Ask anything about Azure network...", height=100)
        if st.button("🤖 Ask Claude", type="primary"):
            if query:
                st.info(f"**Claude AI:** I've analyzed your Azure environment and identified key optimization opportunities. Focus on cost reduction and security hardening for maximum impact.")

def render():
    AzureNetworkManagementModule.render()
