"""
Azure Monitor - AI-Powered Observability
Intelligent monitoring, log analysis, anomaly detection, and performance optimization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureMonitorModule:
    """AI-Enhanced Azure Monitor Intelligence"""
    
    @staticmethod
    def render():
        """Render Azure Monitor Intelligence Center"""
        
        AzureTheme.azure_header(
            "Azure Monitor Intelligence",
            "AI-Powered Observability - Analyze logs, detect anomalies, optimize performance",
            "📊"
        )
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample monitoring data", "info")
        
        tabs = st.tabs(["📊 Dashboard", "📈 Metrics", "📝 Logs", "🔔 Alerts", "🎯 APM", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            AzureMonitorModule._render_dashboard(subscriptions)
        with tabs[1]:
            AzureMonitorModule._render_metrics(subscriptions)
        with tabs[2]:
            AzureMonitorModule._render_logs(subscriptions)
        with tabs[3]:
            AzureMonitorModule._render_alerts(subscriptions)
        with tabs[4]:
            AzureMonitorModule._render_apm(subscriptions)
        with tabs[5]:
            AzureMonitorModule._render_ai_insights()
        with tabs[6]:
            AzureMonitorModule._render_reports(subscriptions)
    
    @staticmethod
    def _render_dashboard(subscriptions):
        """Monitoring dashboard"""
        
        AzureTheme.azure_section_header("📊 Monitoring Dashboard", "🎯")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Monitored Resources", "487", delta="↑ 12")
        with col2:
            st.metric("Active Alerts", "23", delta="↓ 8")
        with col3:
            st.metric("Avg Response Time", "145ms", delta="↓ 12ms")
        with col4:
            st.metric("Error Rate", "0.34%", delta="↓ 0.08%")
        with col5:
            st.metric("Availability", "99.97%", delta="↑ 0.02%")
        
        st.markdown("---")
        
        # Critical alerts
        st.markdown("### 🔔 Critical Alerts")
        
        alerts = [
            {"Alert": "High CPU Usage", "Resource": "webapp-prod-vm", "Severity": "High", "Duration": "15 min", "Status": "🔴 Active"},
            {"Alert": "Memory Pressure", "Resource": "db-server-01", "Severity": "Medium", "Duration": "8 min", "Status": "🟡 Active"},
            {"Alert": "Disk Space Low", "Resource": "storage-account", "Severity": "Medium", "Duration": "45 min", "Status": "🟡 Active"}
        ]
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Response time chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Response Time (24h)")
            times = pd.date_range(end=datetime.now(), periods=24, freq='H')
            response_times = [140 + (i % 10) + (i * 0.5) for i in range(24)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=times, y=response_times, mode='lines', fill='tonexty', line=dict(color='#0078D4')))
            fig.update_layout(yaxis_title='Response Time (ms)', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Availability SLA")
            availability_data = {"Status": ["Available", "Degraded", "Down"], "Time": [99.97, 0.02, 0.01]}
            fig = px.pie(availability_data, values='Time', names='Status', hole=0.4, color_discrete_sequence=['#34A853', '#FBBC04', '#EA4335'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_metrics(subscriptions):
        """Metrics analysis"""
        
        AzureTheme.azure_section_header("📈 Metrics & Performance", "📊")
        
        resource = st.selectbox("Select Resource", ["webapp-prod-vm", "db-server-01", "api-gateway"], key="metric_resource")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CPU Usage", "78%", delta="↑ 12%")
        with col2:
            st.metric("Memory", "6.4 GB", delta="↑ 0.8 GB")
        with col3:
            st.metric("Network In", "124 MB/s", delta="↑ 23 MB/s")
        with col4:
            st.metric("Disk IOPS", "2,847", delta="↑ 340")
        
        st.markdown("---")
        
        # CPU trend
        st.markdown("### 📊 CPU Utilization (1 Hour)")
        times = pd.date_range(end=datetime.now(), periods=60, freq='T')
        cpu_usage = [70 + (i % 20) for i in range(60)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=cpu_usage, mode='lines', name='CPU %', line=dict(color='#0078D4')))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Threshold")
        fig.update_layout(yaxis_title='CPU %', height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_logs(subscriptions):
        """Log analytics"""
        
        AzureTheme.azure_section_header("📝 Log Analytics", "🔍")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Logs", "2.4M", delta="↑ 340K")
        with col2:
            st.metric("Error Logs", "8,234", delta="↓ 1,240")
        with col3:
            st.metric("Warning Logs", "23,456", delta="↑ 2,340")
        
        st.markdown("---")
        
        # Recent errors
        st.markdown("### 🔴 Recent Error Logs")
        logs = [
            {"Time": "2 min ago", "Level": "Error", "Source": "api-gateway", "Message": "Database connection timeout", "Count": "34"},
            {"Time": "5 min ago", "Level": "Error", "Source": "web-app", "Message": "Authentication failed", "Count": "12"},
            {"Time": "12 min ago", "Level": "Warning", "Source": "worker", "Message": "High memory usage", "Count": "8"}
        ]
        st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Log query
        st.markdown("### 🔍 KQL Query")
        query = st.text_area("Enter KQL Query:", value="AzureDiagnostics | where TimeGenerated > ago(1h) | where Level == 'Error'", height=100)
        if st.button("🔍 Run Query", type="primary"):
            st.success("Query executed (Demo mode)")
    
    @staticmethod
    def _render_alerts(subscriptions):
        """Alert management"""
        
        AzureTheme.azure_section_header("🔔 Alert Management", "⚡")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rules", "87", delta="↑ 3")
        with col2:
            st.metric("Active Alerts", "23", delta="↓ 8")
        with col3:
            st.metric("Firing Rate", "12%", delta="↓ 3%")
        with col4:
            st.metric("Avg Response", "4.2 min", delta="↓ 1.1 min")
        
        st.markdown("---")
        
        # Alert rules
        st.markdown("### ⚙️ Alert Rules")
        rules = [
            {"Rule": "High CPU Alert", "Condition": "CPU > 80%", "Severity": "High", "Status": "✅ Enabled", "Fires": "12/week"},
            {"Rule": "Memory Threshold", "Condition": "Memory > 90%", "Severity": "Critical", "Status": "✅ Enabled", "Fires": "8/week"},
            {"Rule": "Disk Space Warning", "Condition": "Disk < 10%", "Severity": "Medium", "Status": "✅ Enabled", "Fires": "3/week"}
        ]
        st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_apm(subscriptions):
        """Application Performance Monitoring"""
        
        AzureTheme.azure_section_header("🎯 Application Performance", "⚡")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Response", "145ms", delta="↓ 12ms")
        with col2:
            st.metric("Requests/sec", "2,847", delta="↑ 340")
        with col3:
            st.metric("Error Rate", "0.34%", delta="↓ 0.08%")
        
        st.markdown("---")
        
        # Slow requests
        st.markdown("### 🐌 Slowest Requests")
        requests = [
            {"Endpoint": "/api/users", "Avg Time": "2,340ms", "P95": "4,560ms", "Count": "1,234", "Error Rate": "0.8%"},
            {"Endpoint": "/api/orders", "Avg Time": "1,890ms", "P95": "3,240ms", "Count": "2,456", "Error Rate": "0.3%"},
            {"Endpoint": "/api/products", "Avg Time": "980ms", "P95": "1,680ms", "Count": "8,901", "Error Rate": "0.1%"}
        ]
        st.dataframe(pd.DataFrame(requests), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_ai_insights():
        """AI-powered insights"""
        
        AzureTheme.azure_section_header("🤖 AI-Powered Monitoring Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "97%", delta="↑ 2%")
        with col2:
            st.metric("Anomalies Detected", "12", delta="↑ 3")
        with col3:
            st.metric("Recommendations", "8", delta="↑ 2")
        with col4:
            st.metric("Alert Reduction", "45%", delta="Potential")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Reduce Alert Noise", "desc": "45 alerts are firing too frequently (>10x/day). AI suggests tuning thresholds.", "impact": "Reduce alert noise by 45% (87→48 alerts)", "confidence": 98, "auto_fix": True},
            {"title": "Fix Database Connection Pool", "desc": "34 connection timeouts detected in 1 hour. DB pool exhausted during peak load.", "impact": "Eliminate 82% of timeout errors", "confidence": 96, "auto_fix": True},
            {"title": "Optimize Slow API Endpoint", "desc": "/api/users taking 2.3s avg (p95: 4.5s). 3 slow queries identified.", "impact": "Reduce response time by 80% (2.3s→450ms)", "confidence": 94, "auto_fix": False}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                if rec['auto_fix']:
                    if st.button("✅ Apply", key=f"mon_{i}"):
                        st.success("Applied! (Demo)")
                else:
                    if st.button("📋 Guide", key=f"guide_{i}"):
                        st.info("Optimization guide shown")
        
        st.markdown("---")
        st.markdown("### 🔍 Anomaly Detection")
        
        anomalies = [
            {"type": "CPU Spike", "resource": "webapp-prod-vm", "severity": "High", "details": "CPU jumped from 45% to 92% in 2 minutes"},
            {"type": "Error Rate Increase", "resource": "api-gateway", "severity": "Medium", "details": "Error rate increased 340% (baseline: 0.1%, current: 0.44%)"},
            {"type": "Memory Leak", "resource": "worker-service", "severity": "High", "details": "Memory usage growing 8% per hour, will exhaust in 6 hours"}
        ]
        
        severity_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        
        for anom in anomalies:
            st.warning(f"{severity_colors[anom['severity']]} **{anom['type']}** on {anom['resource']}: {anom['details']}")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about monitoring:", height=80, key="mon_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(AzureMonitorModule._generate_ai_response(query))
    
    @staticmethod
    def _render_reports(subscriptions):
        """Reports"""
        
        AzureTheme.azure_section_header("📤 Reports", "📊")
        
        if st.button("📥 Generate Report"):
            st.success("✅ Report generated (Demo)")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """AI response"""
        
        q = query.lower()
        
        if "error" in q or "log" in q:
            return """**🔍 Error Log Analysis:**

**Top Error:** Database connection timeout (34 occurrences)

**Root Cause:**
Connection pool size: 50  
Peak concurrent requests: 87  
Result: Pool exhaustion during peak load

**Fix:**
```yaml
# Application config
database:
  pool_size: 100  # Increase from 50
  max_overflow: 20
  timeout: 30
```

**Expected Impact:** 82% error reduction"""
        
        elif "slow" in q or "performance" in q:
            return """**⏱️ Performance Analysis:**

**Slowest Endpoint:** /api/users (2.3s avg)

**AI-Identified Issues:**
1. Query missing index (1.8s)
2. N+1 query problem (0.3s)
3. Large response payload (0.2s)

**Optimizations:**
```sql
-- Add index
CREATE INDEX idx_users_email ON users(email);
```

**Expected:** 2.3s → 450ms (80% faster)**"""
        
        elif "alert" in q:
            return """**🔔 Alert Optimization:**

**Current:** 87 alert rules, 23 active  
**Problem:** 45 alerts fire >10x per day (noise)

**AI Recommendations:**
1. Tune CPU threshold: 80% → 85%
2. Add time window: Fire after 5 min
3. Disable 12 redundant alerts

**Expected:** 87 → 48 alerts (45% reduction)
**Benefit:** Focus on critical issues**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    AzureMonitorModule.render()
