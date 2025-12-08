"""
Azure DevOps Pipelines - AI-Powered CI/CD Operations
Intelligent pipeline management, failure analysis, optimization, and troubleshooting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class AzureDevOpsPipelinesModule:
    """AI-Enhanced Azure DevOps CI/CD Intelligence"""
    
    @staticmethod
    @require_permission('deploy_applications')

    def render():
        """Render Azure DevOps Pipelines Intelligence Center"""
        
        AzureTheme.azure_header(
            "DevOps Pipelines Intelligence",
            "AI-Powered CI/CD Analytics - Predict failures, optimize builds, troubleshoot deployments",
            "🚀"
        )
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample pipeline data", "info")
        
        tabs = st.tabs(["📊 Dashboard", "🚀 Builds", "🎯 Deployments", "📈 Analytics", "🔒 Quality", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            AzureDevOpsPipelinesModule._render_dashboard(subscriptions)
        with tabs[1]:
            AzureDevOpsPipelinesModule._render_builds(subscriptions)
        with tabs[2]:
            AzureDevOpsPipelinesModule._render_deployments(subscriptions)
        with tabs[3]:
            AzureDevOpsPipelinesModule._render_analytics(subscriptions)
        with tabs[4]:
            AzureDevOpsPipelinesModule._render_quality(subscriptions)
        with tabs[5]:
            AzureDevOpsPipelinesModule._render_ai_insights()
        with tabs[6]:
            AzureDevOpsPipelinesModule._render_reports(subscriptions)
    
    @staticmethod
    def _render_dashboard(subscriptions):
        """Dashboard"""
        
        AzureTheme.azure_section_header("📊 CI/CD Operations Dashboard", "🎯")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Pipelines", "47", delta="↑ 3")
        with col2:
            st.metric("Success Rate", "94.2%", delta="↑ 2.1%")
        with col3:
            st.metric("Avg Build Time", "8m 34s", delta="↓ 1m 12s")
        with col4:
            st.metric("Failed Builds", "12", delta="↓ 5")
        with col5:
            st.metric("Deployments Today", "28", delta="↑ 4")
        
        st.markdown("---")
        
        pipelines = [
            {"Pipeline": "api-gateway-ci", "Status": "✅ Success", "Duration": "7m 23s", "Success Rate": "96%"},
            {"Pipeline": "data-pipeline", "Status": "❌ Failed", "Duration": "15m 32s", "Success Rate": "78%"}
        ]
        st.dataframe(pd.DataFrame(pipelines), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_builds(subscriptions):
        """Builds"""
        
        AzureTheme.azure_section_header("🚀 Build Management", "🔨")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Builds", "1,247")
        with col2:
            st.metric("Success", "1,175")
        with col3:
            st.metric("Failed", "72")
        
        if st.button("▶️ Run Pipeline", type="primary"):
            st.success("✅ Pipeline queued (Demo)")
    
    @staticmethod
    def _render_deployments(subscriptions):
        """Deployments"""
        
        AzureTheme.azure_section_header("🎯 Deployment Management", "🚢")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Deployments", "384")
        with col2:
            st.metric("Success Rate", "97.1%")
        with col3:
            st.metric("Rollbacks", "2")
    
    @staticmethod
    def _render_analytics(subscriptions):
        """Analytics"""
        
        AzureTheme.azure_section_header("📈 Pipeline Analytics", "📊")
        
        dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
        success_rates = [92, 91, 93, 94, 93, 95, 94.2]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=success_rates, mode='lines+markers', line=dict(color='#0078D4')))
        fig.update_layout(yaxis_title='Success Rate (%)', height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_quality(subscriptions):
        """Quality"""
        
        AzureTheme.azure_section_header("🔒 Quality & Security", "🛡️")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Code Coverage", "87.3%")
        with col2:
            st.metric("Security Scans", "Passed")
        with col3:
            st.metric("Quality Gates", "8/10")
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        AzureTheme.azure_section_header("🤖 AI-Powered CI/CD Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "94%")
        with col2:
            st.metric("Recommendations", "7")
        with col3:
            st.metric("Predicted Failures", "5")
        with col4:
            st.metric("Time Savings", "3.2 hrs/day")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Parallelize Test Execution", "impact": "Reduce build time 42% (12min→7min)", "confidence": 96, "auto_fix": True},
            {"title": "Fix Flaky Tests", "impact": "Increase success rate 94%→98%", "confidence": 98, "auto_fix": False},
            {"title": "Optimize Docker Build", "impact": "Save 2.5min per build ($280/mo)", "confidence": 92, "auto_fix": True}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                if rec['auto_fix']:
                    if st.button("✅ Apply", key=f"cicd_{i}"):
                        st.success("Applied! (Demo)")
                else:
                    if st.button("📋 Guide", key=f"guide_{i}"):
                        st.info("Fix guide shown")
        
        st.markdown("---")
        st.markdown("### 🔮 Failure Prediction")
        
        preds = [
            {"pipeline": "data-pipeline", "risk": "High", "prob": "78%", "reason": "Flaky tests"},
            {"pipeline": "frontend-deploy", "risk": "Medium", "prob": "42%", "reason": "Dependency conflicts"}
        ]
        
        for pred in preds:
            severity = {"High": "🔴", "Medium": "🟡"}
            st.warning(f"{severity[pred['risk']]} **{pred['pipeline']}** - {pred['prob']} failure probability")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about pipelines:", height=80, key="cicd_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(AzureDevOpsPipelinesModule._generate_ai_response(query))
    
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
        
        if "fail" in q:
            return """**🔍 Build Failure:**
Root cause: Test suite failure (85%)

**Fix:**
```yaml
# Update test assertions
expect(response.status).toBe(200);
```

Resolution time: 5-10 minutes"""
        
        elif "slow" in q or "time" in q:
            return """**⏱️ Build Performance:**
Current: 12min → Target: 7min (5min savings)

**Optimizations:**
1. Parallelize tests: -2.5min
2. Optimize Docker: -1.5min
3. Cache deps: -1min

**Total savings: 5 min/build (42% faster)**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    AzureDevOpsPipelinesModule.render()
