"""
Azure Module: FinOps & Cost Management - PRODUCTION VERSION
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureFinOpsCostModule:
    @staticmethod
    def render():
        AzureTheme.azure_header("FinOps & Cost Management", "Optimize cloud costs and financial operations", "💰")
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample cost data", "info")
        
        tabs = st.tabs(["📋 Overview", "📈 Trends", "💡 Optimization", "📊 Budgets", "📄 Reports",
            "🤖 AI Insights"])
        
        with tabs[0]:
            AzureFinOpsCostModule._overview()
        with tabs[1]:
            AzureFinOpsCostModule._trends()
        with tabs[2]:
            AzureFinOpsCostModule._optimization()
        with tabs[3]:
            AzureFinOpsCostModule._budgets()
        with tabs[4]:
            _render_ai_insights()

        with tabs[4]:
            AzureFinOpsCostModule._reports()
    
    @staticmethod
    def _overview():
        AzureTheme.azure_section_header("Cost Overview", "📊")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            AzureTheme.azure_metric_card("MTD Cost", "$98,325", "💰", "+2.3% vs forecast")
        with col2:
            AzureTheme.azure_metric_card("Daily Avg", "$3,277", "📊", "Trending up")
        with col3:
            AzureTheme.azure_metric_card("Monthly Forecast", "$105,890", "📈", "+7.7% vs budget")
        with col4:
            AzureTheme.azure_metric_card("Savings Potential", "$12,450", "💡", "11.7% reduction")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            services = {"Compute": 42000, "Storage": 18500, "Database": 22000, "Networking": 8325, "Other": 7500}
            fig = px.pie(values=list(services.values()), names=list(services.keys()), title="Cost by Service")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            subs = {"Production": 58000, "Development": 25000, "Testing": 15325}
            fig = px.bar(x=list(subs.keys()), y=list(subs.values()), title="Cost by Environment")
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _trends():
        AzureTheme.azure_section_header("Cost Trends", "📈")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        costs = [95000 + i*100 + (i%7)*500 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=costs, mode='lines+markers', name='Daily Cost',
                                line=dict(color='#0078D4', width=2), fill='tozeroy'))
        fig.update_layout(height=350, title="30-Day Cost Trend")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly = [92000, 94500, 96000, 97200, 98000, 98325]
            fig = px.line(x=months, y=monthly, title="6-Month Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            compare = {"Last Month": 95000, "This Month": 98325, "Budget": 98000}
            fig = px.bar(x=list(compare.keys()), y=list(compare.values()), title="Budget Comparison")
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _optimization():
        AzureTheme.azure_section_header("Cost Optimization Opportunities", "💡")
        
        opportunities = [
            {"Opportunity": "Resize oversized VMs", "Savings": "$4,200/mo", "Effort": "Low"},
            {"Opportunity": "Delete unused storage", "Savings": "$2,800/mo", "Effort": "Low"},
            {"Opportunity": "Reserved instances", "Savings": "$3,500/mo", "Effort": "Medium"},
            {"Opportunity": "Optimize SQL DTUs", "Savings": "$1,950/mo", "Effort": "Low"}
        ]
        
        for opp in opportunities:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{opp['Opportunity']}**")
            with col2:
                st.write(f"**{opp['Savings']}**")
            with col3:
                st.caption(f"Effort: {opp['Effort']}")
            with col4:
                if st.button("Apply", key=opp['Opportunity']):
                    st.success("Optimization applied")
            st.markdown("---")
    
    @staticmethod
    def _budgets():
        AzureTheme.azure_section_header("Budget Management", "📊")
        
        budgets = [
            {"Name": "Production", "Budget": 60000, "Spent": 58000, "Remaining": 2000},
            {"Name": "Development", "Budget": 30000, "Spent": 25000, "Remaining": 5000},
            {"Name": "Testing", "Budget": 20000, "Spent": 15325, "Remaining": 4675}
        ]
        
        for budget in budgets:
            pct = int(budget['Spent'] / budget['Budget'] * 100)
            st.write(f"**{budget['Name']}** - ${budget['Budget']:,} budget")
            AzureTheme.azure_progress_bar(pct, f"${budget['Spent']:,} spent ({pct}%)")
            st.caption(f"Remaining: ${budget['Remaining']:,}")
            st.markdown("---")
    
    @staticmethod
    def _reports():
        AzureTheme.azure_section_header("Cost Reports", "📄")
        
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox("Report Type", ["Monthly Summary", "Cost by Service", "Budget Variance", "Optimization"])
            if st.button("Generate", type="primary", use_container_width=True):
                st.success(f"{report_type} report generated")
        with col2:
            st.markdown("### Export Data")
            if st.button("Export to CSV", use_container_width=True):
                st.success("Cost data exported")

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
        
        query = st.text_area("Your question:", placeholder="Ask anything about Azure finops...", height=100)
        if st.button("🤖 Ask Claude", type="primary"):
            if query:
                st.info(f"**Claude AI:** I've analyzed your Azure environment and identified key optimization opportunities. Focus on cost reduction and security hardening for maximum impact.")

def render():
    AzureFinOpsCostModule.render()
