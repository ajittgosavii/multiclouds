"""
Google Cloud IAM - AI-Powered Identity & Access Management
Intelligent user management, RBAC optimization, privilege analysis, and security recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPIAMModule:
    """AI-Enhanced Google Cloud IAM Intelligence"""
    
    @staticmethod
    def render():
        """Render GCP IAM Intelligence Center"""
        
        GCPTheme.gcp_header(
            "Cloud IAM Intelligence",
            "AI-Powered Identity & Access - Optimize RBAC, analyze privileges, enforce security",
            "🔐"
        )
        
        projects = AppConfig.load_gcp_projects()
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample identity data", "info")
        
        tabs = st.tabs(["👥 Users & Groups", "🔑 Roles & Permissions", "📋 Policies", "🛡️ Security", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            GCPIAMModule._render_users(projects)
        with tabs[1]:
            GCPIAMModule._render_roles(projects)
        with tabs[2]:
            GCPIAMModule._render_policies(projects)
        with tabs[3]:
            GCPIAMModule._render_security(projects)
        with tabs[4]:
            GCPIAMModule._render_ai_insights()
        with tabs[5]:
            GCPIAMModule._render_reports(projects)
    
    @staticmethod
    def _render_users(projects):
        """User management"""
        
        GCPTheme.gcp_section_header("👥 Users & Service Accounts", "🔐")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Members", "1,384", delta="↑ 28")
        with col2:
            st.metric("Active Users", "1,298", delta="93.8%")
        with col3:
            st.metric("Service Accounts", "456", delta="↑ 18")
        with col4:
            st.metric("Groups", "127", delta="↑ 3")
        with col5:
            st.metric("2FA Enabled", "89.2%", delta="↑ 3.1%")
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### 📊 Recent Member Activity")
        
        users = [
            {"Member": "user@company.com", "Type": "User", "Last Activity": "1 hour ago", "2FA": "✅ Yes", "Roles": "4", "Risk": "Low"},
            {"Member": "admin@company.com", "Type": "User", "Last Activity": "3 days ago", "2FA": "❌ No", "Roles": "15", "Risk": "Critical"},
            {"Member": "sa-prod@project.iam", "Type": "Service Account", "Last Activity": "5 min ago", "2FA": "N/A", "Roles": "3", "Risk": "Medium"},
            {"Member": "group-dev@company.com", "Type": "Group", "Last Activity": "N/A", "2FA": "Mixed", "Roles": "2", "Risk": "Low"}
        ]
        st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Member Growth (30 Days)")
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            counts = [1350 + i for i in range(30)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines', fill='tonexty', line=dict(color='#4285F4')))
            fig.update_layout(yaxis_title='Total Members', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🔐 2FA Status")
            tfa_data = {"Status": ["Enabled", "Disabled"], "Count": [1234, 150]}
            fig = px.pie(tfa_data, values='Count', names='Status', hole=0.4, color_discrete_sequence=['#34A853', '#EA4335'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_roles(projects):
        """Role management"""
        
        GCPTheme.gcp_section_header("🔑 Roles & Permissions", "⚡")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Roles", "3,456", delta="Built-in")
        with col2:
            st.metric("Custom Roles", "34", delta="↑ 3")
        with col3:
            st.metric("Bindings", "8,234", delta="↑ 234")
        with col4:
            st.metric("Highly Privileged", "28", delta="2.0%")
        
        st.markdown("---")
        
        # Top role bindings
        st.markdown("### 🔑 Top Role Bindings")
        
        roles = [
            {"Role": "roles/owner", "Type": "Primitive", "Bindings": "8", "Risk": "🔴 Critical", "Scope": "Project"},
            {"Role": "roles/editor", "Type": "Primitive", "Bindings": "67", "Risk": "🟠 High", "Scope": "Project"},
            {"Role": "roles/viewer", "Type": "Primitive", "Bindings": "892", "Risk": "🟢 Low", "Scope": "Project"},
            {"Role": "roles/compute.admin", "Type": "Predefined", "Bindings": "23", "Risk": "🟡 Medium", "Scope": "Project"}
        ]
        st.dataframe(pd.DataFrame(roles), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Role Distribution")
            role_dist = {"Type": ["Primitive", "Predefined", "Custom"], "Count": [975, 7025, 234]}
            fig = px.bar(role_dist, x='Type', y='Count', title='IAM Bindings by Role Type')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🔍 Privilege Analysis**")
            st.metric("Primitive Roles Used", "975", delta="High risk")
            st.metric("Service Accounts with Owner", "4", delta="Critical")
            st.metric("Unused Roles", "12", delta="90+ days")
    
    @staticmethod
    def _render_policies(projects):
        """Policy management"""
        
        GCPTheme.gcp_section_header("📋 Organization Policies", "📜")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Policies", "34", delta="↑ 2")
        with col2:
            st.metric("Compliance", "94.1%", delta="↑ 2.3%")
        with col3:
            st.metric("Violations", "8", delta="↓ 3")
        
        st.markdown("---")
        
        # Organization policies
        st.markdown("### 🔐 Organization Policies")
        
        policies = [
            {"Policy": "Require OS Login", "Status": "✅ Enforced", "Scope": "Organization", "Compliance": "100%"},
            {"Policy": "Disable Service Account Key Creation", "Status": "✅ Enforced", "Scope": "Organization", "Compliance": "98.7%"},
            {"Policy": "Restrict VPC Peering", "Status": "⚠️ Monitoring", "Scope": "Folder", "Compliance": "87.3%"},
            {"Policy": "Require Shielded VMs", "Status": "✅ Enforced", "Scope": "Project", "Compliance": "95.2%"}
        ]
        st.dataframe(pd.DataFrame(policies), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_security(projects):
        """Security analysis"""
        
        GCPTheme.gcp_section_header("🛡️ Security & Risk Analysis", "🔒")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Security Score", "82/100", delta="↑ 6")
        with col2:
            st.metric("High-Risk Members", "12", delta="↓ 4")
        with col3:
            st.metric("Service Account Keys", "234", delta="↓ 23")
        with col4:
            st.metric("External Members", "8", delta="Need review")
        
        st.markdown("---")
        
        # Security findings
        st.markdown("### 🔴 Security Findings")
        
        findings = [
            {"Finding": "Service accounts with owner role", "Count": "4 accounts", "Risk": "Critical", "Action": "Apply least privilege"},
            {"Finding": "Users with primitive roles", "Count": "67 bindings", "Risk": "High", "Action": "Migrate to predefined roles"},
            {"Finding": "Long-lived SA keys", "Count": "89 keys >90 days", "Risk": "Medium", "Action": "Rotate or use Workload Identity"}
        ]
        
        for finding in findings:
            severity = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity[finding['Risk']]} **{finding['Finding']}** - {finding['Count']}"):
                st.write(f"**Risk Level:** {finding['Risk']}")
                st.write(f"**Recommended Action:** {finding['Action']}")
                if st.button("🔧 Remediate", key=f"gcp_rem_{finding['Finding']}", use_container_width=True):
                    st.success("✅ Remediation applied (Demo mode)")
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        GCPTheme.gcp_section_header("🤖 AI-Powered IAM Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "96%", delta="↑ 3%")
        with col2:
            st.metric("Recommendations", "8", delta="↑ 2")
        with col3:
            st.metric("Security Issues", "28", delta="↓ 12")
        with col4:
            st.metric("Primitive Roles", "975", delta="High risk")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Eliminate Primitive Roles", "desc": "67 members use primitive roles (owner/editor). AI recommends migration to least-privilege predefined roles.", "impact": "Reduce blast radius by 78%", "confidence": 98, "auto_fix": False},
            {"title": "Migrate to Workload Identity", "desc": "234 service account keys detected. Workload Identity eliminates key management.", "impact": "Remove 234 long-lived credentials", "confidence": 100, "auto_fix": True},
            {"title": "Remove Service Account Owner", "desc": "4 service accounts have owner role. AI analysis shows they only need compute.admin.", "impact": "Reduce attack surface by 45%", "confidence": 96, "auto_fix": True},
            {"title": "Enable Context-Aware Access", "desc": "12.6% of access from unmanaged devices. BeyondCorp recommended.", "impact": "Block 95% of unauthorized access attempts", "confidence": 94, "auto_fix": True}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if rec['auto_fix']:
                        if st.button("✅ Apply", key=f"gcp_iam_{i}"):
                            st.success("Applied! (Demo)")
                    else:
                        if st.button("📋 Guide", key=f"guide_{i}"):
                            st.info("Migration guide shown")
                with col2:
                    if st.button("📊 Simulate", key=f"sim_{i}"):
                        st.info("Impact simulation shown")
        
        st.markdown("---")
        st.markdown("### 🔍 Privilege Analysis")
        
        st.markdown("**🔴 Over-Privileged Members:**")
        over_privs = [
            {"Member": "user@company.com", "Current": "roles/owner", "Recommended": "roles/compute.admin", "Last Used Owner": "Never"},
            {"Member": "sa-app@project.iam", "Current": "roles/owner", "Recommended": "roles/storage.admin", "Last Used Owner": "Never"}
        ]
        st.dataframe(pd.DataFrame(over_privs), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about Cloud IAM:", height=80, key="gcp_iam_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(GCPIAMModule._generate_ai_response(query))
    
    @staticmethod
    def _render_reports(projects):
        """Reports"""
        
        GCPTheme.gcp_section_header("📤 Reports", "📊")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👥 Access Report**")
            if st.button("📥 Generate", key="access_report", use_container_width=True):
                st.success("✅ Report generated (Demo)")
        with col2:
            st.markdown("**🔒 Security Audit**")
            if st.button("📥 Generate", key="audit_report", use_container_width=True):
                st.success("✅ Report generated (Demo)")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """AI response"""
        
        q = query.lower()
        
        if "primitive" in q or "owner" in q or "editor" in q:
            return """**🔍 Primitive Role Analysis:**

**Current:** 975 primitive role bindings  
**Problem:** Overly broad permissions

**Breakdown:**
- roles/owner: 8 bindings (critical risk)
- roles/editor: 67 bindings (high risk)  
- roles/viewer: 900 bindings (low risk)

**AI Recommendations:**
```
Owner → Specific admin roles:
  user@company.com: roles/owner → roles/compute.admin
  
Editor → Least privilege:
  dev@company.com: roles/editor → roles/storage.objectAdmin
```

**Impact:** Reduce blast radius by 78%  
**GCP Best Practice:** Use predefined roles**"""
        
        elif "service account" in q or "workload" in q:
            return """**🔐 Service Account Security:**

**Current:** 234 service account keys  
**Risk:** Long-lived credentials (89 keys >90 days)

**Problems:**
1. Key rotation overhead
2. Potential credential leakage
3. No automatic expiration

**AI Recommendation: Workload Identity**

**Migration:**
```bash
# Enable Workload Identity
gcloud container clusters update CLUSTER \\
  --workload-pool=PROJECT.svc.id.goog

# Bind SA to KSA
gcloud iam service-accounts add-iam-policy-binding SA \\
  --role roles/iam.workloadIdentityUser \\
  --member "serviceAccount:PROJECT.svc.id.goog[NS/KSA]"
```

**Impact:** Eliminate 234 long-lived credentials**"""
        
        elif "security" in q or "risk" in q:
            return """**🛡️ IAM Security Analysis:**

**High-Risk Issues:**
1. 4 service accounts with owner (critical)
2. 67 primitive role bindings (high)
3. 89 SA keys >90 days old (medium)
4. 8 external members (review needed)

**AI Recommendations:**
1. Downgrade SA owners to specific roles
2. Migrate primitive → predefined roles
3. Enable Workload Identity
4. Review external access

**Expected Results:**
- Security score: 82 → 95 (+13 points)
- Attack surface: -78% reduction
- Key management: -234 credentials**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    GCPIAMModule.render()
