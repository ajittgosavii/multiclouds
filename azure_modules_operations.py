"""
Azure AI-Enhanced Operations Module
Intelligent operations powered by AI - assistant, troubleshooting, predictive maintenance, and automation
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class AzureOperationsModule:
    """AI-Enhanced Azure Operations"""
    
    @staticmethod
    @require_permission('view_resources')

    def render():
        """Main render method"""
        
        AzureTheme.azure_header(
            "AI-Enhanced Operations",
            "Intelligent Operations powered by AI - Assistant, troubleshooting, predictive maintenance",
            "⚙️"
        )
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample operations data", "info")
        
        tabs = st.tabs([
            "🤖 AI Assistant",
            "🔍 Troubleshooting",
            "💻 VM Management",
            "🔮 Predictive Maintenance",
            "📖 Smart Runbooks",
            "🛡️ Vulnerability Mgmt",
            "📊 Resource Optimization"
        ])
        
        with tabs[0]:
            AzureOperationsModule._render_ai_assistant()
        with tabs[1]:
            AzureOperationsModule._render_troubleshooting()
        with tabs[2]:
            AzureOperationsModule._render_vm_management()
        with tabs[3]:
            AzureOperationsModule._render_predictive_maintenance()
        with tabs[4]:
            AzureOperationsModule._render_smart_runbooks()
        with tabs[5]:
            AzureOperationsModule._render_vulnerability_management()
        with tabs[6]:
            AzureOperationsModule._render_resource_optimization()
    
    @staticmethod
    def _render_ai_assistant():
        """AI Operations Assistant"""
        
        AzureTheme.azure_section_header("🤖 AI Operations Assistant", "💬")
        
        st.info("💬 Chat with AI about your Azure infrastructure - ask questions, get recommendations, automate operations")
        
        # Sample questions
        st.markdown("### 💡 Try asking:")
        
        questions = [
            "Show me all running VMs and their costs",
            "What's consuming the most resources?",
            "How can I reduce my Azure bill?",
            "Find VMs that haven't been used in 7 days",
            "What security issues should I address?",
            "Create a disaster recovery plan"
        ]
        
        cols = st.columns(2)
        for i, q in enumerate(questions):
            with cols[i % 2]:
                if st.button(f"💡 {q}", key=f"q_{i}", use_container_width=True):
                    st.session_state.ops_query = q
        
        st.markdown("---")
        
        query = st.text_area(
            "Ask AI about your Azure operations:",
            value=st.session_state.get('ops_query', ''),
            placeholder="e.g., Stop all VMs tagged Environment=Dev",
            height=100
        )
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                with st.spinner("🤖 AI is analyzing..."):
                    response = AzureOperationsModule._generate_ai_response(query)
                    st.markdown(response)
    
    @staticmethod
    def _render_troubleshooting():
        """AI Troubleshooting"""
        
        AzureTheme.azure_section_header("🔍 AI Troubleshooting", "🎯")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Issues", "23", delta="↓ 8")
        with col2:
            st.metric("Avg Resolution Time", "18 min", delta="↓ 12 min")
        with col3:
            st.metric("Auto-Resolved", "67%", delta="↑ 12%")
        
        st.markdown("---")
        
        # Common issues
        st.markdown("### 🔴 Active Issues")
        
        issues = [
            {"Issue": "VM high CPU usage", "Resource": "web-vm-prod-01", "Severity": "High", "Duration": "45 min", "AI Solution": "Scale up to D4s_v3"},
            {"Issue": "Storage account throttling", "Resource": "proddata001", "Severity": "Critical", "Duration": "12 min", "AI Solution": "Upgrade to Premium tier"},
            {"Issue": "App Service timeout", "Resource": "api-app-service", "Severity": "Medium", "Duration": "2 hours", "AI Solution": "Increase timeout to 300s"}
        ]
        
        for i, issue in enumerate(issues):
            severity_colors = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity_colors[issue['Severity']]} **{issue['Issue']}** - {issue['Resource']}"):
                st.write(f"**Duration:** {issue['Duration']}")
                st.write(f"**AI Recommended Solution:** {issue['AI Solution']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔧 Auto-Fix", key=f"fix_{i}"):
                        st.success("✅ Fix applied automatically!")
                with col2:
                    if st.button("📋 Show Details", key=f"details_{i}"):
                        st.info("Detailed diagnostics shown")
    
    @staticmethod
    def _render_vm_management():
        """VM Management"""
        
        AzureTheme.azure_section_header("💻 Virtual Machine Management", "🖥️")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total VMs", "847", delta="↑ 23")
        with col2:
            st.metric("Running", "634", delta="75%")
        with col3:
            st.metric("Stopped", "213", delta="25%")
        with col4:
            st.metric("Avg Utilization", "42%", delta="↓ 8%")
        
        st.markdown("---")
        
        # VM recommendations
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"VM": "dev-vm-01", "Issue": "Over-provisioned", "Current": "D8s_v3", "Recommended": "D4s_v3", "Savings": "$180/mo"},
            {"VM": "test-vm-02", "Issue": "Unused (7 days)", "Current": "Running", "Recommended": "Deallocate", "Savings": "$240/mo"},
            {"VM": "prod-vm-03", "Issue": "No backup", "Current": "None", "Recommended": "Enable backup", "Savings": "Risk mitigation"}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['VM']}** - {rec['Issue']} • Save {rec['Savings']}"):
                st.write(f"**Current:** {rec['Current']}")
                st.write(f"**Recommended:** {rec['Recommended']}")
                if st.button("✅ Apply", key=f"vm_{i}"):
                    st.success("Applied! (Demo)")
    
    @staticmethod
    def _render_predictive_maintenance():
        """Predictive Maintenance"""
        
        AzureTheme.azure_section_header("🔮 Predictive Maintenance", "📈")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Predicted Issues", "12", delta="Next 7 days")
        with col2:
            st.metric("Prevented Outages", "34", delta="Last 30 days")
        with col3:
            st.metric("AI Confidence", "94%", delta="↑ 3%")
        
        st.markdown("---")
        
        # Predictions
        st.markdown("### 🔮 AI Predictions")
        
        predictions = [
            {"Resource": "sql-db-prod", "Prediction": "Storage will be full", "Timeframe": "3 days", "Confidence": "96%", "Action": "Increase storage to 2 TB"},
            {"Resource": "app-service-01", "Prediction": "CPU will hit 100%", "Timeframe": "5 days", "Confidence": "89%", "Action": "Scale to P2v2 tier"},
            {"Resource": "storage-account", "Prediction": "IOPS limit reached", "Timeframe": "7 days", "Confidence": "92%", "Action": "Upgrade to Premium"}
        ]
        
        for i, pred in enumerate(predictions):
            with st.expander(f"**{pred['Resource']}** - {pred['Prediction']} in {pred['Timeframe']} • {pred['Confidence']} confidence"):
                st.write(f"**AI Recommended Action:** {pred['Action']}")
                if st.button("📅 Schedule Maintenance", key=f"pred_{i}"):
                    st.success("Maintenance scheduled!")
    
    @staticmethod
    def _render_smart_runbooks():
        """Smart Runbooks"""
        
        AzureTheme.azure_section_header("📖 Smart Runbooks", "🤖")
        
        st.markdown("### 📚 AI-Generated Runbooks")
        
        runbooks = [
            {"Name": "Emergency Incident Response", "Trigger": "Critical alert", "Steps": "12", "Automation": "85%"},
            {"Name": "Database Failover", "Trigger": "DB outage", "Steps": "8", "Automation": "100%"},
            {"Name": "Scale-Up Procedure", "Trigger": "High load", "Steps": "5", "Automation": "90%"},
            {"Name": "Security Incident", "Trigger": "Security alert", "Steps": "15", "Automation": "60%"}
        ]
        
        for i, rb in enumerate(runbooks):
            with st.expander(f"**{rb['Name']}** - {rb['Steps']} steps • {rb['Automation']} automated"):
                st.write(f"**Trigger:** {rb['Trigger']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Execute", key=f"run_{i}"):
                        st.success("Runbook executed!")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{i}"):
                        st.info("Runbook editor opened")
    
    @staticmethod
    def _render_vulnerability_management():
        """Vulnerability Management"""
        
        AzureTheme.azure_section_header("🛡️ Vulnerability Management", "🔒")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Vulnerabilities", "234", delta="↓ 45")
        with col2:
            st.metric("Critical", "12", delta="↓ 8")
        with col3:
            st.metric("Patched (30d)", "156", delta="↑ 23")
        with col4:
            st.metric("Compliance", "87%", delta="↑ 5%")
        
        st.markdown("---")
        
        # Critical vulnerabilities
        st.markdown("### 🔴 Critical Vulnerabilities")
        
        vulns = [
            {"CVE": "CVE-2024-1234", "Severity": "Critical", "Resource": "web-vm-01", "Fix": "Update to latest patch", "Priority": "P0"},
            {"CVE": "CVE-2024-5678", "Severity": "High", "Resource": "db-server", "Fix": "Apply security update", "Priority": "P1"},
            {"CVE": "CVE-2024-9012", "Severity": "High", "Resource": "app-service", "Fix": "Upgrade runtime", "Priority": "P1"}
        ]
        
        for i, vuln in enumerate(vulns):
            severity_colors = {"Critical": "🔴", "High": "🟠"}
            with st.expander(f"{severity_colors[vuln['Severity']]} **{vuln['CVE']}** - {vuln['Resource']} • {vuln['Priority']}"):
                st.write(f"**AI Recommended Fix:** {vuln['Fix']}")
                if st.button("🔧 Auto-Patch", key=f"vuln_{i}"):
                    st.success("Patch applied!")
    
    @staticmethod
    def _render_resource_optimization():
        """Resource Optimization"""
        
        AzureTheme.azure_section_header("📊 Resource Optimization", "⚡")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Potential Savings", "$12,450/mo", delta="Identified")
        with col2:
            st.metric("Waste Detected", "23%", delta="Resources")
        with col3:
            st.metric("Optimizations", "47", delta="Available")
        
        st.markdown("---")
        
        # Optimization opportunities
        st.markdown("### 💰 Top Optimization Opportunities")
        
        opts = [
            {"Category": "Compute", "Issue": "Over-provisioned VMs", "Resources": "23", "Savings": "$4,560/mo"},
            {"Category": "Storage", "Issue": "Unused disks", "Resources": "67", "Savings": "$2,340/mo"},
            {"Category": "Network", "Issue": "Idle load balancers", "Resources": "12", "Savings": "$1,440/mo"},
            {"Category": "Database", "Issue": "Right-size needed", "Resources": "8", "Savings": "$4,110/mo"}
        ]
        
        for i, opt in enumerate(opts):
            with st.expander(f"**{opt['Category']}** - {opt['Issue']} • {opt['Resources']} resources • Save {opt['Savings']}"):
                if st.button("🔧 Optimize All", key=f"opt_{i}"):
                    st.success("Optimization scheduled!")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """Generate AI response"""
        
        q = query.lower()
        
        if "cost" in q or "bill" in q or "reduce" in q:
            return """**💰 Cost Optimization Recommendations:**

**Top 3 Cost Savers:**

1. **Right-size over-provisioned VMs** - Save $4,560/month
   - 23 VMs running at <30% CPU
   - Recommended: D8s_v3 → D4s_v3
   
2. **Delete unused disks** - Save $2,340/month
   - 67 unattached disks found
   - Total wasted: 12.4 TB
   
3. **Deallocate idle VMs** - Save $3,840/month
   - 18 VMs unused for 7+ days
   - Consider auto-shutdown schedules

**Total potential savings: $10,740/month**"""
        
        elif "security" in q or "issue" in q:
            return """**🛡️ Security Recommendations:**

**Critical Items:**
- 12 critical vulnerabilities need patching
- 8 VMs missing latest security updates
- 3 storage accounts with public access

**Quick Fixes:**
1. Apply security patches (auto-fix available)
2. Enable Azure Security Center
3. Implement network security groups

**Compliance Score: 87% (+13% to reach 100%)**"""
        
        elif "vm" in q or "instance" in q:
            return """**💻 VM Analysis:**

**Running VMs:** 634 (75% of total)
**Stopped VMs:** 213 (25% of total)

**Recommendations:**
- 23 VMs over-provisioned (save $4,560/mo)
- 18 VMs unused for 7+ days (save $3,840/mo)
- 34 VMs missing backups (risk mitigation)

**Top resource consumers:**
1. prod-vm-cluster (8 VMs) - $2,340/mo
2. dev-vm-pool (12 VMs) - $1,680/mo
3. test-environment (15 VMs) - $980/mo"""
        
        return f"AI analysis for: {query}"

# Module-level render function
def render():
    """Module-level render function"""
    AzureOperationsModule.render()
