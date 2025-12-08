"""
Google Cloud Monitoring - AI-Powered Observability
Intelligent monitoring, log analysis, anomaly detection, and performance optimization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class GCPMonitoringModule:
    """AI-Enhanced Cloud Monitoring Intelligence"""
    
    @staticmethod
    @require_permission('view_resources')

    def render():
        """Render Cloud Monitoring Intelligence Center"""
        
        GCPTheme.gcp_header(
            "Cloud Monitoring Intelligence",
            "AI-Powered Observability - Analyze logs, detect anomalies, optimize performance",
            "📊"
        )
        
        projects = AppConfig.load_gcp_projects()
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample monitoring data", "info")
        
        tabs = st.tabs(["📊 Dashboard", "📈 Metrics", "📝 Logs", "🔔 Alerts", "🎯 APM", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            GCPMonitoringModule._render_dashboard(projects)
        with tabs[1]:
            GCPMonitoringModule._render_metrics(projects)
        with tabs[2]:
            GCPMonitoringModule._render_logs(projects)
        with tabs[3]:
            GCPMonitoringModule._render_alerts(projects)
        with tabs[4]:
            GCPMonitoringModule._render_apm(projects)
        with tabs[5]:
            GCPMonitoringModule._render_ai_insights()
        with tabs[6]:
            GCPMonitoringModule._render_reports(projects)
    
    @staticmethod
    def _render_dashboard(projects):
        """Monitoring dashboard"""
        
        GCPTheme.gcp_section_header("📊 Monitoring Dashboard", "🎯")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Monitored Resources", "542", delta="↑ 18")
        with col2:
            st.metric("Active Alerts", "18", delta="↓ 6")
        with col3:
            st.metric("Avg Latency", "132ms", delta="↓ 8ms")
        with col4:
            st.metric("Error Rate", "0.28%", delta="↓ 0.12%")
        with col5:
            st.metric("Uptime", "99.98%", delta="↑ 0.01%")
        
        st.markdown("---")
        
        # Critical alerts
        st.markdown("### 🔔 Active Alerts")
        
        alerts = [
            {"Alert": "High Memory", "Resource": "gke-cluster-1", "Severity": "High", "Duration": "12 min", "Status": "🔴 Firing"},
            {"Alert": "Slow Queries", "Resource": "cloud-sql-prod", "Severity": "Medium", "Duration": "25 min", "Status": "🟡 Firing"},
            {"Alert": "Request Spike", "Resource": "api-service", "Severity": "Low", "Duration": "5 min", "Status": "🟢 Info"}
        ]
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Latency Trend (24h)")
            times = pd.date_range(end=datetime.now(), periods=24, freq='H')
            latency = [130 + (i % 8) + (i * 0.3) for i in range(24)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=times, y=latency, mode='lines', fill='tonexty', line=dict(color='#4285F4')))
            fig.update_layout(yaxis_title='Latency (ms)', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 SLO Compliance")
            slo_data = {"Status": ["Met", "Nearly Met", "Violated"], "Percentage": [94.8, 4.2, 1.0]}
            fig = px.pie(slo_data, values='Percentage', names='Status', hole=0.4, color_discrete_sequence=['#34A853', '#FBBC04', '#EA4335'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_metrics(projects):
        """Metrics analysis"""
        
        GCPTheme.gcp_section_header("📈 Metrics & Performance", "📊")
        
        resource = st.selectbox("Select Resource", ["gke-cluster-1", "cloud-sql-prod", "api-service"], key="metric_resource")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CPU Usage", "72%", delta="↑ 8%")
        with col2:
            st.metric("Memory", "5.8 GB", delta="↑ 0.6 GB")
        with col3:
            st.metric("Network", "98 MB/s", delta="↑ 18 MB/s")
        with col4:
            st.metric("Requests/s", "3,240", delta="↑ 420")
        
        st.markdown("---")
        
        st.markdown("### 📊 CPU Utilization (1 Hour)")
        times = pd.date_range(end=datetime.now(), periods=60, freq='T')
        cpu = [65 + (i % 15) for i in range(60)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=cpu, mode='lines', line=dict(color='#4285F4')))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Alert Threshold")
        fig.update_layout(yaxis_title='CPU %', height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_logs(projects):
        """Log analysis"""
        
        GCPTheme.gcp_section_header("📝 Cloud Logging", "🔍")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Logs", "3.2M", delta="↑ 420K")
        with col2:
            st.metric("Error Logs", "6,842", delta="↓ 1,120")
        with col3:
            st.metric("Warning Logs", "18,234", delta="↑ 1,840")
        
        st.markdown("---")
        
        st.markdown("### 🔴 Recent Errors")
        logs = [
            {"Time": "1 min ago", "Severity": "ERROR", "Resource": "api-service", "Message": "Connection pool exhausted", "Count": "42"},
            {"Time": "4 min ago", "Severity": "ERROR", "Resource": "cloud-function", "Message": "Timeout after 60s", "Count": "18"},
            {"Time": "8 min ago", "Severity": "WARNING", "Resource": "gke-node", "Message": "Memory pressure", "Count": "12"}
        ]
        st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("### 🔍 Log Query")
        query = st.text_area("Enter Log Query:", value='resource.type="gce_instance"\nseverity="ERROR"', height=100)
        if st.button("🔍 Run Query", type="primary"):
            st.success("Query executed (Demo mode)")
    
    @staticmethod
    def _render_alerts(projects):
        """Alert management"""
        
        GCPTheme.gcp_section_header("🔔 Alert Policies", "⚡")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Policies", "94", delta="↑ 4")
        with col2:
            st.metric("Active Alerts", "18", delta="↓ 6")
        with col3:
            st.metric("Notification Channels", "12")
        with col4:
            st.metric("Avg Response", "3.8 min", delta="↓ 0.9 min")
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Alert Policies")
        policies = [
            {"Policy": "High CPU Alert", "Condition": "CPU > 80%", "Severity": "Critical", "Status": "✅ Enabled", "Triggers": "8/week"},
            {"Policy": "Memory Threshold", "Condition": "Memory > 85%", "Severity": "High", "Status": "✅ Enabled", "Triggers": "12/week"},
            {"Policy": "Error Rate Spike", "Condition": "Errors > 1%", "Severity": "Medium", "Status": "✅ Enabled", "Triggers": "5/week"}
        ]
        st.dataframe(pd.DataFrame(policies), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_apm(projects):
        """Application Performance"""
        
        GCPTheme.gcp_section_header("🎯 Application Performance", "⚡")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Latency", "132ms", delta="↓ 8ms")
        with col2:
            st.metric("Requests/sec", "3,240", delta="↑ 420")
        with col3:
            st.metric("Error Rate", "0.28%", delta="↓ 0.12%")
        
        st.markdown("---")
        
        st.markdown("### 🐌 Slow Requests")
        requests = [
            {"Endpoint": "/api/search", "P50": "1,840ms", "P95": "3,920ms", "Count": "2,340", "Errors": "1.2%"},
            {"Endpoint": "/api/checkout", "P50": "1,240ms", "P95": "2,680ms", "Count": "1,890", "Errors": "0.6%"},
            {"Endpoint": "/api/catalog", "P50": "680ms", "P95": "1,340ms", "Count": "12,450", "Errors": "0.2%"}
        ]
        st.dataframe(pd.DataFrame(requests), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        GCPTheme.gcp_section_header("🤖 AI-Powered Monitoring Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "96%", delta="↑ 3%")
        with col2:
            st.metric("Anomalies", "9", delta="↑ 2")
        with col3:
            st.metric("Recommendations", "7", delta="↑ 1")
        with col4:
            st.metric("Alert Reduction", "38%", delta="Potential")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Optimize Cloud SQL Queries", "desc": "5 slow queries causing 78% of latency. Add missing indexes.", "impact": "Reduce query time by 84% (1.8s→280ms)", "confidence": 98, "auto_fix": False},
            {"title": "Scale Cloud Function Memory", "desc": "Function timing out after 60s. Memory-constrained.", "impact": "Eliminate 95% of timeout errors", "confidence": 96, "auto_fix": True},
            {"title": "Tune Alert Thresholds", "desc": "38 policies firing too frequently (>15x/day).", "impact": "Reduce alert noise by 38% (94→58 policies)", "confidence": 94, "auto_fix": True}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                if rec['auto_fix']:
                    if st.button("✅ Apply", key=f"gcp_mon_{i}"):
                        st.success("Applied! (Demo)")
                else:
                    if st.button("📋 Guide", key=f"guide_{i}"):
                        st.info("Optimization guide shown")
        
        st.markdown("---")
        st.markdown("### 🔍 Anomaly Detection")
        
        anomalies = [
            {"type": "Memory Spike", "resource": "gke-cluster-1", "severity": "High", "details": "Memory jumped 68% in 5 minutes"},
            {"type": "Latency Increase", "resource": "api-service", "severity": "Medium", "details": "P95 latency increased 240% (baseline: 1.2s, current: 2.9s)"},
            {"type": "Error Burst", "resource": "cloud-function", "severity": "High", "details": "Error rate spiked from 0.1% to 2.8% (28x increase)"}
        ]
        
        severity_colors = {"High": "🔴", "Medium": "🟡"}
        
        for anom in anomalies:
            st.warning(f"{severity_colors[anom['severity']]} **{anom['type']}** on {anom['resource']}: {anom['details']}")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about monitoring:", height=80, key="gcp_mon_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(GCPMonitoringModule._generate_ai_response(query))
    
    @staticmethod
    def _render_reports(projects):
        """Reports"""
        
        GCPTheme.gcp_section_header("📤 Reports", "📊")
        
        if st.button("📥 Generate Report"):
            st.success("✅ Report generated (Demo)")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """AI response"""
        
        q = query.lower()
        
        if "error" in q or "log" in q:
            return """**🔍 Error Log Analysis:**

**Top Error:** Connection pool exhausted (42 occurrences)

**Root Cause:**
Cloud SQL connection pool: 60  
Peak concurrent: 128  
Result: Pool exhaustion

**GCP-Specific Fix:**
```yaml
# Cloud SQL connection pool
max_connections: 150  # Increase from 60
connection_timeout: 30s
pool_recycle: 3600
```

**Expected:** 92% error reduction"""
        
        elif "slow" in q or "performance" in q:
            return """**⏱️ Performance Analysis:**

**Slowest Endpoint:** /api/search (1.84s)

**AI-Identified Issues:**
1. Missing Cloud SQL index (1.2s)
2. Inefficient query (0.4s)
3. Large response (0.24s)

**Cloud SQL Optimization:**
```sql
CREATE INDEX idx_products_search 
ON products USING GIN(to_tsvector('english', name));
```

**Expected:** 1.84s → 340ms (82% faster)**"""
        
        elif "alert" in q:
            return """**🔔 Alert Optimization:**

**Current:** 94 alert policies, 18 firing  
**Problem:** 38 policies fire >15x/day

**AI Recommendations:**
1. Increase threshold: 80% → 85%
2. Add duration: Fire after 10 min
3. Consolidate 15 redundant policies

**Expected:** 94 → 58 policies (38% reduction)
**Benefit:** Focus on critical alerts**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    GCPMonitoringModule.render()
