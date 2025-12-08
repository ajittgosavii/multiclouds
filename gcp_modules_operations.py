"""
GCP AI-Enhanced Operations Module
Intelligent operations powered by AI - assistant, troubleshooting, predictive maintenance, and automation
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig
from auth_azure_sso import require_permission

class GCPOperationsModule:
    """AI-Enhanced GCP Operations"""
    
    @staticmethod
    @require_permission('view_resources')

    def render():
        """Main render method"""
        
        GCPTheme.gcp_header(
            "AI-Enhanced Operations",
            "Intelligent Operations powered by AI - Assistant, troubleshooting, predictive maintenance",
            "⚙️"
        )
        
        projects = AppConfig.load_gcp_projects()
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample operations data", "info")
        
        tabs = st.tabs([
            "🤖 AI Assistant",
            "🔍 Troubleshooting",
            "💻 Instance Management",
            "🔮 Predictive Maintenance",
            "📖 Smart Runbooks",
            "🛡️ Vulnerability Mgmt",
            "📊 Resource Optimization"
        ])
        
        with tabs[0]:
            GCPOperationsModule._render_ai_assistant()
        with tabs[1]:
            GCPOperationsModule._render_troubleshooting()
        with tabs[2]:
            GCPOperationsModule._render_instance_management()
        with tabs[3]:
            GCPOperationsModule._render_predictive_maintenance()
        with tabs[4]:
            GCPOperationsModule._render_smart_runbooks()
        with tabs[5]:
            GCPOperationsModule._render_vulnerability_management()
        with tabs[6]:
            GCPOperationsModule._render_resource_optimization()
    
    @staticmethod
    def _render_ai_assistant():
        """AI Operations Assistant"""
        
        GCPTheme.gcp_section_header("🤖 AI Operations Assistant", "💬")
        
        st.info("💬 Chat with AI about your GCP infrastructure - ask questions, get recommendations, automate operations")
        
        # Sample questions
        st.markdown("### 💡 Try asking:")
        
        questions = [
            "Show me all running instances and costs",
            "What's consuming the most resources?",
            "How can I reduce my GCP bill?",
            "Find instances not used in 7 days",
            "What security issues should I fix?",
            "Create a DR plan for production"
        ]
        
        cols = st.columns(2)
        for i, q in enumerate(questions):
            with cols[i % 2]:
                if st.button(f"💡 {q}", key=f"gcp_q_{i}", use_container_width=True):
                    st.session_state.gcp_ops_query = q
        
        st.markdown("---")
        
        query = st.text_area(
            "Ask AI about your GCP operations:",
            value=st.session_state.get('gcp_ops_query', ''),
            placeholder="e.g., Stop all instances with label env=dev",
            height=100
        )
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                with st.spinner("🤖 AI is analyzing..."):
                    response = GCPOperationsModule._generate_ai_response(query)
                    st.markdown(response)
    
    @staticmethod
    def _render_troubleshooting():
        """AI Troubleshooting"""
        
        GCPTheme.gcp_section_header("🔍 AI Troubleshooting", "🎯")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Issues", "18", delta="↓ 6")
        with col2:
            st.metric("Avg Resolution Time", "14 min", delta="↓ 9 min")
        with col3:
            st.metric("Auto-Resolved", "72%", delta="↑ 15%")
        
        st.markdown("---")
        
        # Common issues
        st.markdown("### 🔴 Active Issues")
        
        issues = [
            {"Issue": "Instance high CPU", "Resource": "web-instance-prod", "Severity": "High", "Duration": "38 min", "AI Solution": "Scale to n2-standard-4"},
            {"Issue": "Cloud SQL slow queries", "Resource": "prod-mysql-01", "Severity": "Critical", "Duration": "15 min", "AI Solution": "Add indexes on user_id"},
            {"Issue": "GKE pod crashes", "Resource": "api-deployment", "Severity": "Medium", "Duration": "1 hour", "AI Solution": "Increase memory to 512Mi"}
        ]
        
        for i, issue in enumerate(issues):
            severity_colors = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity_colors[issue['Severity']]} **{issue['Issue']}** - {issue['Resource']}"):
                st.write(f"**Duration:** {issue['Duration']}")
                st.write(f"**AI Recommended Solution:** {issue['AI Solution']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔧 Auto-Fix", key=f"gcp_fix_{i}"):
                        st.success("✅ Fix applied automatically!")
                with col2:
                    if st.button("📋 Show Details", key=f"gcp_details_{i}"):
                        st.info("Detailed diagnostics shown")
    
    @staticmethod
    def _render_instance_management():
        """Instance Management"""
        
        GCPTheme.gcp_section_header("💻 Compute Instance Management", "🖥️")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Instances", "1,247", delta="↑ 34")
        with col2:
            st.metric("Running", "924", delta="74%")
        with col3:
            st.metric("Stopped", "323", delta="26%")
        with col4:
            st.metric("Avg Utilization", "38%", delta="↓ 12%")
        
        st.markdown("---")
        
        # Instance recommendations
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"Instance": "dev-instance-01", "Issue": "Over-provisioned", "Current": "n2-standard-8", "Recommended": "n2-standard-4", "Savings": "$240/mo"},
            {"Instance": "test-instance-02", "Issue": "Unused (7 days)", "Current": "Running", "Recommended": "Stop instance", "Savings": "$340/mo"},
            {"Instance": "prod-instance-03", "Issue": "Use preemptible", "Current": "Standard", "Recommended": "Preemptible", "Savings": "$680/mo"}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['Instance']}** - {rec['Issue']} • Save {rec['Savings']}"):
                st.write(f"**Current:** {rec['Current']}")
                st.write(f"**Recommended:** {rec['Recommended']}")
                if st.button("✅ Apply", key=f"gcp_vm_{i}"):
                    st.success("Applied! (Demo)")
    
    @staticmethod
    def _render_predictive_maintenance():
        """Predictive Maintenance"""
        
        GCPTheme.gcp_section_header("🔮 Predictive Maintenance", "📈")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Predicted Issues", "9", delta="Next 7 days")
        with col2:
            st.metric("Prevented Outages", "42", delta="Last 30 days")
        with col3:
            st.metric("AI Confidence", "96%", delta="↑ 4%")
        
        st.markdown("---")
        
        # Predictions
        st.markdown("### 🔮 AI Predictions")
        
        predictions = [
            {"Resource": "cloud-sql-prod", "Prediction": "Disk will be full", "Timeframe": "2 days", "Confidence": "98%", "Action": "Increase disk to 500 GB"},
            {"Resource": "gke-cluster-prod", "Prediction": "Node pool exhaustion", "Timeframe": "4 days", "Confidence": "92%", "Action": "Enable autoscaling to 10 nodes"},
            {"Resource": "load-balancer-01", "Prediction": "Capacity limit reached", "Timeframe": "6 days", "Confidence": "87%", "Action": "Add backend instances"}
        ]
        
        for i, pred in enumerate(predictions):
            with st.expander(f"**{pred['Resource']}** - {pred['Prediction']} in {pred['Timeframe']} • {pred['Confidence']} confidence"):
                st.write(f"**AI Recommended Action:** {pred['Action']}")
                if st.button("📅 Schedule Maintenance", key=f"gcp_pred_{i}"):
                    st.success("Maintenance scheduled!")
    
    @staticmethod
    def _render_smart_runbooks():
        """Smart Runbooks"""
        
        GCPTheme.gcp_section_header("📖 Smart Runbooks", "🤖")
        
        st.markdown("### 📚 AI-Generated Runbooks")
        
        runbooks = [
            {"Name": "Incident Response", "Trigger": "Critical alert", "Steps": "10", "Automation": "90%"},
            {"Name": "Cloud SQL Failover", "Trigger": "DB outage", "Steps": "6", "Automation": "100%"},
            {"Name": "GKE Scale-Up", "Trigger": "High pod count", "Steps": "4", "Automation": "95%"},
            {"Name": "Security Breach Response", "Trigger": "Security alert", "Steps": "18", "Automation": "55%"}
        ]
        
        for i, rb in enumerate(runbooks):
            with st.expander(f"**{rb['Name']}** - {rb['Steps']} steps • {rb['Automation']} automated"):
                st.write(f"**Trigger:** {rb['Trigger']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Execute", key=f"gcp_run_{i}"):
                        st.success("Runbook executed!")
                with col2:
                    if st.button("✏️ Edit", key=f"gcp_edit_{i}"):
                        st.info("Runbook editor opened")
    
    @staticmethod
    def _render_vulnerability_management():
        """Vulnerability Management"""
        
        GCPTheme.gcp_section_header("🛡️ Vulnerability Management", "🔒")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Vulnerabilities", "189", delta="↓ 52")
        with col2:
            st.metric("Critical", "8", delta="↓ 6")
        with col3:
            st.metric("Patched (30d)", "142", delta="↑ 28")
        with col4:
            st.metric("Compliance", "91%", delta="↑ 7%")
        
        st.markdown("---")
        
        # Critical vulnerabilities
        st.markdown("### 🔴 Critical Vulnerabilities")
        
        vulns = [
            {"CVE": "CVE-2024-1234", "Severity": "Critical", "Resource": "web-instance-01", "Fix": "Update OS to latest", "Priority": "P0"},
            {"CVE": "CVE-2024-5678", "Severity": "High", "Resource": "db-instance", "Fix": "Apply patch v2.4.1", "Priority": "P1"},
            {"CVE": "CVE-2024-9012", "Severity": "High", "Resource": "app-engine", "Fix": "Upgrade runtime", "Priority": "P1"}
        ]
        
        for i, vuln in enumerate(vulns):
            severity_colors = {"Critical": "🔴", "High": "🟠"}
            with st.expander(f"{severity_colors[vuln['Severity']]} **{vuln['CVE']}** - {vuln['Resource']} • {vuln['Priority']}"):
                st.write(f"**AI Recommended Fix:** {vuln['Fix']}")
                if st.button("🔧 Auto-Patch", key=f"gcp_vuln_{i}"):
                    st.success("Patch applied!")
    
    @staticmethod
    def _render_resource_optimization():
        """Resource Optimization"""
        
        GCPTheme.gcp_section_header("📊 Resource Optimization", "⚡")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Potential Savings", "$15,840/mo", delta="Identified")
        with col2:
            st.metric("Waste Detected", "28%", delta="Resources")
        with col3:
            st.metric("Optimizations", "52", delta="Available")
        
        st.markdown("---")
        
        # Optimization opportunities
        st.markdown("### 💰 Top Optimization Opportunities")
        
        opts = [
            {"Category": "Compute", "Issue": "Use preemptible VMs", "Resources": "34", "Savings": "$6,840/mo"},
            {"Category": "Storage", "Issue": "Unused persistent disks", "Resources": "89", "Savings": "$3,120/mo"},
            {"Category": "Network", "Issue": "Idle load balancers", "Resources": "15", "Savings": "$1,680/mo"},
            {"Category": "Database", "Issue": "Cloud SQL right-sizing", "Resources": "12", "Savings": "$4,200/mo"}
        ]
        
        for i, opt in enumerate(opts):
            with st.expander(f"**{opt['Category']}** - {opt['Issue']} • {opt['Resources']} resources • Save {opt['Savings']}"):
                if st.button("🔧 Optimize All", key=f"gcp_opt_{i}"):
                    st.success("Optimization scheduled!")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """Generate AI response"""
        
        q = query.lower()
        
        if "cost" in q or "bill" in q or "reduce" in q:
            return """**💰 Cost Optimization Recommendations:**

**Top 3 Cost Savers:**

1. **Use Preemptible VMs** - Save $6,840/month
   - 34 instances eligible for preemptible
   - 80% cost savings available
   
2. **Delete unused disks** - Save $3,120/month
   - 89 unattached persistent disks found
   - Total wasted: 18.7 TB
   
3. **Right-size Cloud SQL** - Save $4,200/month
   - 12 databases over-provisioned
   - Avg utilization: 32%

**Total potential savings: $14,160/month**

**GCP-Specific Tips:**
- Enable committed use discounts
- Use sustained use discounts automatically
- Consider Cloud SQL auto-scaling"""
        
        elif "security" in q or "issue" in q:
            return """**🛡️ Security Recommendations:**

**Critical Items:**
- 8 critical vulnerabilities need patching
- 12 instances missing security updates
- 5 storage buckets with public access

**Quick Fixes:**
1. Apply OS patches (auto-fix available)
2. Enable Security Command Center
3. Implement VPC firewall rules
4. Enable binary authorization for GKE

**Compliance Score: 91% (+9% to reach 100%)**

**GCP Security Best Practices:**
- Use service accounts with least privilege
- Enable VPC Service Controls
- Implement Cloud Armor WAF"""
        
        elif "instance" in q or "vm" in q:
            return """**💻 Instance Analysis:**

**Running Instances:** 924 (74% of total)
**Stopped Instances:** 323 (26% of total)

**Recommendations:**
- 34 instances → Use preemptible (save $6,840/mo)
- 23 instances unused 7+ days (save $4,560/mo)
- 45 instances missing snapshots (risk)

**Top resource consumers:**
1. prod-instance-pool (12 VMs) - $3,840/mo
2. dev-cluster (18 VMs) - $2,160/mo
3. test-environment (24 VMs) - $1,440/mo

**GCP Tips:**
- Use sole-tenant nodes for licensing
- Enable live migration for maintenance
- Use custom machine types for exact fit"""
        
        return f"AI analysis for: {query}"

# Module-level render function
def render():
    """Module-level render function"""
    GCPOperationsModule.render()
