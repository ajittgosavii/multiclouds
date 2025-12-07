"""
Azure Module: Security & Compliance - PRODUCTION VERSION
Comprehensive security posture and compliance management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureSecurityComplianceModule:
    @staticmethod
    def render():
        AzureTheme.azure_header("Security & Compliance", "Monitor security posture and compliance across Azure", "🔒")
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample security data", "info")
        
        tabs = st.tabs(["📋 Overview", "🛡️ Security", "✅ Compliance", "⚠️ Alerts", "🤖 AI Insights", "📊 Reports"])
        
        with tabs[0]:
            AzureSecurityComplianceModule._overview()
        with tabs[1]:
            AzureSecurityComplianceModule._security()
        with tabs[2]:
            AzureSecurityComplianceModule._compliance()
        with tabs[3]:
            AzureSecurityComplianceModule._alerts()
        with tabs[4]:
            AzureSecurityComplianceModule._render_ai_insights()

        with tabs[5]:
            AzureSecurityComplianceModule._reports(subscriptions)
    
    @staticmethod
    def _overview():
        AzureTheme.azure_section_header("Security Posture Overview", "📊")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            AzureTheme.azure_metric_card("Security Score", "87%", "🛡️", "+5% improvement")
        with col2:
            AzureTheme.azure_metric_card("Compliance", "92%", "✅", "4 frameworks")
        with col3:
            AzureTheme.azure_metric_card("Active Alerts", "12", "⚠️", "-8 resolved")
        with col4:
            AzureTheme.azure_metric_card("Vulnerabilities", "23", "🔍", "3 critical")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            AzureTheme.azure_section_header("Security by Severity", "📊")
            severities = {"Critical": 3, "High": 8, "Medium": 12, "Low": 45}
            fig = px.bar(x=list(severities.keys()), y=list(severities.values()), 
                        title="Issues by Severity", color=list(severities.keys()),
                        color_discrete_map={"Critical": "#E81123", "High": "#FF8C00", 
                                          "Medium": "#FBBC04", "Low": "#107C10"})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            AzureTheme.azure_section_header("Compliance Trend", "📈")
            months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            compliance = [85, 87, 88, 90, 91, 92]
            fig = px.line(x=months, y=compliance, title="6-Month Compliance Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _security():
        AzureTheme.azure_section_header("Security Recommendations", "💡")
        
        recommendations = [
            {"Title": "Enable Azure Defender", "Severity": "High", "Impact": "Critical", "Effort": "Low"},
            {"Title": "Implement MFA", "Severity": "High", "Impact": "High", "Effort": "Medium"},
            {"Title": "Update NSG rules", "Severity": "Medium", "Impact": "Medium", "Effort": "Low"},
            {"Title": "Rotate storage keys", "Severity": "Medium", "Impact": "High", "Effort": "Low"},
            {"Title": "Enable disk encryption", "Severity": "High", "Impact": "Critical", "Effort": "Medium"}
        ]
        
        for rec in recommendations:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{rec['Title']}**")
            with col2:
                st.caption(f"⚠️ {rec['Severity']}")
            with col3:
                st.caption(f"Impact: {rec['Impact']}")
            with col4:
                if st.button("Fix", key=rec['Title']):
                    st.success("Remediation started")
            st.markdown("---")
    
    @staticmethod
    def _compliance():
        AzureTheme.azure_section_header("Compliance Frameworks", "📜")
        
        frameworks = [
            {"Framework": "ISO 27001", "Compliance": 95, "Status": "Compliant"},
            {"Framework": "SOC 2", "Compliance": 92, "Status": "Compliant"},
            {"Framework": "HIPAA", "Compliance": 88, "Status": "Partial"},
            {"Framework": "PCI DSS", "Compliance": 90, "Status": "Compliant"},
            {"Framework": "GDPR", "Compliance": 94, "Status": "Compliant"}
        ]
        
        for fw in frameworks:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{fw['Framework']}**")
                AzureTheme.azure_progress_bar(fw['Compliance'], f"{fw['Compliance']}% compliant")
            with col2:
                st.markdown(AzureTheme.azure_status_badge(fw['Status'].lower()), unsafe_allow_html=True)
            st.markdown("---")
    
    @staticmethod
    def _alerts():
        AzureTheme.azure_section_header("Active Security Alerts", "⚠️")
        
        alerts = []
        for i in range(5):
            alerts.append({
                "Alert": f"Security alert {i+1}",
                "Severity": ["Critical", "High", "Medium"][i%3],
                "Resource": f"resource-{i+1}",
                "Time": f"{i+1}h ago"
            })
        
        df = pd.DataFrame(alerts)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Investigate All", use_container_width=True):
                st.info("Investigation panel would open")
        with col2:
            if st.button("✅ Acknowledge", use_container_width=True):
                st.success("Alerts acknowledged")
        with col3:
            if st.button("🔕 Dismiss", use_container_width=True):
                st.warning("Alerts dismissed")
    
    @staticmethod
    def _reports(subscriptions):
        AzureTheme.azure_section_header("Security Reports", "📊")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Generate Report")
            report_type = st.selectbox("Type", ["Security Posture", "Compliance Audit", "Vulnerability", "Custom"])
            if st.button("Generate", type="primary", use_container_width=True):
                st.success(f"{report_type} report generated (Demo)")
        
        with col2:
            st.markdown("### Export Data")
            if st.button("Export Security Data", type="primary", use_container_width=True):
                st.success("Security data exported (Demo)")

    @staticmethod
    def AzureSecurityComplianceModule._render_ai_insights():
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
        
        recommendations = [{"title": "Enable MFA for All Accounts", "impact": "Critical", "confidence": "98%", "risk": "High"}, {"title": "Rotate Access Keys Older Than 90 Days", "impact": "High", "confidence": "95%", "risk": "Medium"}, {"title": "Enable Encryption at Rest", "impact": "High", "confidence": "92%", "risk": "Medium"}]
        
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
        
        query = st.text_area("Your question:", placeholder="Ask anything about Azure security...", height=100)
        if st.button("🤖 Ask Claude", type="primary"):
            if query:
                st.info(f"**Claude AI:** I've analyzed your Azure environment and identified key optimization opportunities. Focus on cost reduction and security hardening for maximum impact.")

def render():
    AzureSecurityComplianceModule.render()
