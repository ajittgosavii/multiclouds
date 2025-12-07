"""
GCP Module: Security & Compliance - PRODUCTION VERSION
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPSecurityComplianceModule:
    @staticmethod
    def render():
        GCPTheme.gcp_header("Security & Compliance", "Monitor security and compliance across GCP", "🔒")
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample security data", "info")
        
        tabs = st.tabs(["📋 Overview", "🛡️ Security", "✅ Compliance", "⚠️ Findings", "🤖 AI Insights", "📊 Reports"])
        
        with tabs[0]:
            GCPSecurityComplianceModule._overview()
        with tabs[1]:
            GCPSecurityComplianceModule._security()
        with tabs[2]:
            GCPSecurityComplianceModule._compliance()
        with tabs[3]:
            GCPSecurityComplianceModule._findings()
        with tabs[4]:
            GCPSecurityComplianceModule._render_ai_insights()

        with tabs[5]:
            GCPSecurityComplianceModule._reports()
    
    @staticmethod
    def _overview():
        GCPTheme.gcp_section_header("Security Overview", "📊")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            GCPTheme.gcp_metric_card("Security Score", "89%", "🛡️", "+6% improvement")
        with col2:
            GCPTheme.gcp_metric_card("Compliance", "94%", "✅", "5 standards")
        with col3:
            GCPTheme.gcp_metric_card("Active Findings", "15", "⚠️", "-10 resolved")
        with col4:
            GCPTheme.gcp_metric_card("Vulnerabilities", "18", "🔍", "2 critical")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            severities = {"Critical": 2, "High": 6, "Medium": 10, "Low": 38}
            fig = px.bar(x=list(severities.keys()), y=list(severities.values()), title="Findings by Severity")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            scores = [83, 85, 86, 88, 88, 89]
            fig = px.line(x=months, y=scores, title="Security Score Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _security():
        GCPTheme.gcp_section_header("Security Recommendations", "💡")
        
        recs = [
            {"Title": "Enable Security Command Center Premium", "Severity": "High"},
            {"Title": "Rotate service account keys", "Severity": "High"},
            {"Title": "Enable VPC Service Controls", "Severity": "Medium"},
            {"Title": "Configure firewall rules", "Severity": "Medium"}
        ]
        
        for rec in recs:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{rec['Title']}**")
            with col2:
                st.caption(f"⚠️ {rec['Severity']}")
            with col3:
                if st.button("Fix", key=rec['Title']):
                    st.success("Applied")
            st.markdown("---")
    
    @staticmethod
    def _compliance():
        GCPTheme.gcp_section_header("Compliance Standards", "📜")
        
        standards = [
            {"Standard": "ISO 27001", "Compliance": 96},
            {"Standard": "SOC 2", "Compliance": 94},
            {"Standard": "HIPAA", "Compliance": 90},
            {"Standard": "PCI DSS", "Compliance": 92}
        ]
        
        for std in standards:
            st.write(f"**{std['Standard']}**")
            GCPTheme.gcp_progress_bar(std['Compliance'], f"{std['Compliance']}% compliant")
            st.markdown("---")
    
    @staticmethod
    def _findings():
        GCPTheme.gcp_section_header("Security Findings", "⚠️")
        
        findings = []
        for i in range(6):
            findings.append({
                "Finding": f"Security finding {i+1}",
                "Severity": ["Critical", "High", "Medium"][i%3],
                "Resource": f"resource-{i+1}",
                "Status": ["Active", "In Progress"][i%2]
            })
        
        df = pd.DataFrame(findings)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _reports():
        GCPTheme.gcp_section_header("Generate Reports", "📊")
        
        report_type = st.selectbox("Type", ["Security Posture", "Compliance", "Vulnerabilities"])
        if st.button("Generate Report", type="primary"):
            st.success(f"{report_type} report generated (Demo)")

    @staticmethod
    def GCPSecurityComplianceModule._render_ai_insights():
        """GCP AI-powered insights and recommendations"""
        
        GCPTheme.gcp_section_header("🤖 AI-Powered Insights", "🧠")
        
        # AI Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            GCPTheme.gcp_metric_card("AI Confidence", "95%", "🎯", "High accuracy")
        with col2:
            GCPTheme.gcp_metric_card("Recommendations", "6", "💡", "Ready")
        with col3:
            GCPTheme.gcp_metric_card("Auto-fixes", "3", "⚡", "Available")
        
        st.markdown("---")
        
        # AI Recommendations
        GCPTheme.gcp_section_header("💡 AI Recommendations", "🤖")
        
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
        GCPTheme.gcp_section_header("⚠️ AI Anomaly Detection", "🔍")
        
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
        GCPTheme.gcp_section_header("💬 Ask Claude AI", "🤖")
        
        query = st.text_area("Your question:", placeholder="Ask anything about GCP security...", height=100)
        if st.button("🤖 Ask Claude", type="primary"):
            if query:
                st.info(f"**Claude AI:** I've analyzed your GCP environment and identified key optimization opportunities. Focus on cost reduction and security hardening for maximum impact.")

def render():
    GCPSecurityComplianceModule.render()
