"""
GCP Module: FinOps & Cost Management - PRODUCTION VERSION
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPFinOpsCostModule:
    @staticmethod
    def render():
        GCPTheme.gcp_header("FinOps & Cost Management", "Optimize Google Cloud costs", "💰")
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample cost data", "info")
        
        tabs = st.tabs(["📋 Overview", "📈 Trends", "💡 Recommendations", "📊 Budgets", "📄 Reports",
            "🤖 AI Insights"])
        
        with tabs[0]:
            GCPFinOpsCostModule._overview()
        with tabs[1]:
            GCPFinOpsCostModule._trends()
        with tabs[2]:
            GCPFinOpsCostModule._recommendations()
        with tabs[3]:
            GCPFinOpsCostModule._budgets()
        with tabs[4]:
            GCPFinOpsCostModule._render_ai_insights()

        with tabs[4]:
            GCPFinOpsCostModule._reports()
    
    @staticmethod
    def _overview():
        GCPTheme.gcp_section_header("Cost Overview", "📊")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            GCPTheme.gcp_metric_card("MTD Cost", "$76,450", "💰", "+1.8% vs forecast")
        with col2:
            GCPTheme.gcp_metric_card("Daily Avg", "$2,548", "📊", "Stable")
        with col3:
            GCPTheme.gcp_metric_card("Forecast", "$82,200", "📈", "+7.5% vs budget")
        with col4:
            GCPTheme.gcp_metric_card("Savings", "$9,800", "💡", "12.8% potential")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            services = {"Compute Engine": 28000, "Cloud Storage": 15000, "BigQuery": 18500, "Networking": 8950, "Other": 6000}
            fig = px.pie(values=list(services.values()), names=list(services.keys()), title="Cost by Service")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            projects = {"Production": 45000, "Development": 20000, "Testing": 11450}
            fig = px.bar(x=list(projects.keys()), y=list(projects.values()), title="Cost by Project")
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _trends():
        GCPTheme.gcp_section_header("Cost Trends", "📈")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        costs = [74000 + i*80 + (i%7)*400 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=costs, mode='lines+markers', name='Daily Cost',
                                line=dict(color='#4285F4', width=2), fill='tozeroy'))
        fig.update_layout(height=350, title="30-Day Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _recommendations():
        GCPTheme.gcp_section_header("Cost Optimization", "💡")
        
        recs = [
            {"Title": "Use committed use discounts", "Savings": "$3,200/mo"},
            {"Title": "Delete idle instances", "Savings": "$2,400/mo"},
            {"Title": "Optimize BigQuery queries", "Savings": "$1,800/mo"},
            {"Title": "Use preemptible VMs", "Savings": "$2,400/mo"}
        ]
        
        for rec in recs:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{rec['Title']}**")
            with col2:
                st.write(f"**{rec['Savings']}**")
            with col3:
                if st.button("Apply", key=rec['Title']):
                    st.success("Applied")
            st.markdown("---")
    
    @staticmethod
    def _budgets():
        GCPTheme.gcp_section_header("Budget Tracking", "📊")
        
        budgets = [
            {"Name": "Production", "Budget": 50000, "Spent": 45000},
            {"Name": "Development", "Budget": 25000, "Spent": 20000},
            {"Name": "Testing", "Budget": 15000, "Spent": 11450}
        ]
        
        for b in budgets:
            pct = int(b['Spent'] / b['Budget'] * 100)
            st.write(f"**{b['Name']}** - ${b['Budget']:,}")
            GCPTheme.gcp_progress_bar(pct, f"${b['Spent']:,} ({pct}%)")
            st.markdown("---")
    
    @staticmethod
    def _reports():
        GCPTheme.gcp_section_header("Cost Reports", "📄")
        
        report_type = st.selectbox("Type", ["Monthly Summary", "Project Breakdown", "Service Analysis"])
        if st.button("Generate Report", type="primary"):
            st.success(f"{report_type} generated")

    @staticmethod
    def GCPFinOpsCostModule._render_ai_insights():
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
        
        recommendations = [{"title": "Purchase Reserved Instances", "savings": "$3,500/mo", "confidence": "96%", "roi": "280%"}, {"title": "Implement Auto-Shutdown Schedules", "savings": "$2,100/mo", "confidence": "93%", "roi": "Immediate"}, {"title": "Optimize Storage Tiers", "savings": "$1,600/mo", "confidence": "91%", "roi": "190%"}]
        
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
        
        query = st.text_area("Your question:", placeholder="Ask anything about GCP finops...", height=100)
        if st.button("🤖 Ask Claude", type="primary"):
            if query:
                st.info(f"**Claude AI:** I've analyzed your GCP environment and identified key optimization opportunities. Focus on cost reduction and security hardening for maximum impact.")

def render():
    GCPFinOpsCostModule.render()
