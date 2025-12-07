"""
Azure AD / Entra ID - AI-Powered Identity & Access Management
Intelligent user management, RBAC optimization, privilege analysis, and security recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureADModule:
    """AI-Enhanced Azure AD / Entra ID Intelligence"""
    
    @staticmethod
    def render():
        """Render Azure AD Intelligence Center"""
        
        AzureTheme.azure_header(
            "Azure AD / Entra ID Intelligence",
            "AI-Powered Identity & Access - Optimize RBAC, analyze privileges, enforce security",
            "🔐"
        )
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample identity data", "info")
        
        tabs = st.tabs(["👥 Users & Groups", "🔑 Roles & Permissions", "📋 Policies", "🛡️ Security", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            AzureADModule._render_users(subscriptions)
        with tabs[1]:
            AzureADModule._render_roles(subscriptions)
        with tabs[2]:
            AzureADModule._render_policies(subscriptions)
        with tabs[3]:
            AzureADModule._render_security(subscriptions)
        with tabs[4]:
            AzureADModule._render_ai_insights()
        with tabs[5]:
            AzureADModule._render_reports(subscriptions)
    
    @staticmethod
    def _render_users(subscriptions):
        """User management"""
        
        AzureTheme.azure_section_header("👥 User & Group Management", "🔐")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Users", "1,247", delta="↑ 23")
        with col2:
            st.metric("Active Users", "1,189", delta="95.3%")
        with col3:
            st.metric("Groups", "184", delta="↑ 4")
        with col4:
            st.metric("Service Principals", "342", delta="↑ 12")
        with col5:
            st.metric("MFA Enabled", "87.4%", delta="↑ 2.3%")
        
        st.markdown("---")
        
        # Recent user activity
        st.markdown("### 📊 Recent User Activity")
        
        users = [
            {"User": "john.doe@company.com", "Status": "✅ Active", "Last Login": "2 hours ago", "MFA": "✅ Enabled", "Risk": "Low", "Roles": "3"},
            {"User": "jane.smith@company.com", "Status": "✅ Active", "Last Login": "15 min ago", "MFA": "✅ Enabled", "Risk": "Low", "Roles": "5"},
            {"User": "admin@company.com", "Status": "✅ Active", "Last Login": "1 day ago", "MFA": "❌ Disabled", "Risk": "High", "Roles": "12"},
            {"User": "service.account@company.com", "Status": "🔐 Service", "Last Login": "5 min ago", "MFA": "N/A", "Risk": "Medium", "Roles": "2"}
        ]
        st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 User Growth (30 Days)")
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            user_counts = [1200 + i for i in range(30)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=user_counts, mode='lines', fill='tonexty', line=dict(color='#0078D4')))
            fig.update_layout(yaxis_title='Total Users', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🔐 MFA Adoption")
            mfa_data = {"Status": ["Enabled", "Disabled"], "Count": [1090, 157]}
            fig = px.pie(mfa_data, values='Count', names='Status', hole=0.4, color_discrete_sequence=['#34A853', '#EA4335'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_roles(subscriptions):
        """Role management"""
        
        AzureTheme.azure_section_header("🔑 Roles & Permissions", "⚡")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Roles", "87", delta="↑ 3")
        with col2:
            st.metric("Custom Roles", "23", delta="↑ 2")
        with col3:
            st.metric("Role Assignments", "2,847", delta="↑ 67")
        with col4:
            st.metric("Privileged Users", "34", delta="2.7%")
        
        st.markdown("---")
        
        # Role assignments
        st.markdown("### 🔑 Top Role Assignments")
        
        roles = [
            {"Role": "Owner", "Type": "Built-in", "Assignments": "12", "Risk": "🔴 Critical", "Scope": "Subscription"},
            {"Role": "Contributor", "Type": "Built-in", "Assignments": "89", "Risk": "🟠 High", "Scope": "Resource Group"},
            {"Role": "Reader", "Type": "Built-in", "Assignments": "342", "Risk": "🟢 Low", "Scope": "All"},
            {"Role": "Custom-DevOps", "Type": "Custom", "Assignments": "45", "Risk": "🟡 Medium", "Scope": "Resource Group"}
        ]
        st.dataframe(pd.DataFrame(roles), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Permission analysis
        st.markdown("### 📊 Permission Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            permissions = {"Level": ["Owner", "Contributor", "Reader", "Custom"], "Users": [12, 89, 342, 68]}
            fig = px.bar(permissions, x='Level', y='Users', title='Users by Permission Level')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🔍 Privilege Analysis**")
            st.metric("Over-Privileged Users", "23", delta="Need review")
            st.metric("Unused Roles", "8", delta="Can be removed")
            st.metric("Stale Assignments", "34", delta=">90 days")
    
    @staticmethod
    def _render_policies(subscriptions):
        """Policy management"""
        
        AzureTheme.azure_section_header("📋 Policies & Compliance", "📜")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Policies", "47", delta="↑ 2")
        with col2:
            st.metric("Compliance", "92.3%", delta="↑ 1.8%")
        with col3:
            st.metric("Violations", "12", delta="↓ 5")
        
        st.markdown("---")
        
        # Conditional access policies
        st.markdown("### 🔐 Conditional Access Policies")
        
        policies = [
            {"Policy": "Require MFA for Admins", "Status": "✅ Enabled", "Users": "34", "Compliance": "100%"},
            {"Policy": "Block Legacy Auth", "Status": "✅ Enabled", "Users": "All", "Compliance": "97.8%"},
            {"Policy": "Require Managed Device", "Status": "⚠️ Report-only", "Users": "All", "Compliance": "84.2%"},
            {"Policy": "Block High-Risk Sign-ins", "Status": "✅ Enabled", "Users": "All", "Compliance": "100%"}
        ]
        st.dataframe(pd.DataFrame(policies), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_security(subscriptions):
        """Security analysis"""
        
        AzureTheme.azure_section_header("🛡️ Security & Risk Analysis", "🔒")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Security Score", "78/100", delta="↑ 5")
        with col2:
            st.metric("High-Risk Users", "8", delta="↓ 3")
        with col3:
            st.metric("Failed Logins", "234", delta="↓ 67")
        with col4:
            st.metric("Risky Sign-ins", "12", delta="↓ 4")
        
        st.markdown("---")
        
        # Security findings
        st.markdown("### 🔴 Security Findings")
        
        findings = [
            {"Finding": "Admin without MFA", "Users": "admin@company.com", "Risk": "Critical", "Action": "Enable MFA immediately"},
            {"Finding": "Inactive admin accounts", "Users": "3 accounts", "Risk": "High", "Action": "Disable or remove"},
            {"Finding": "Over-privileged service principals", "Users": "12 service accounts", "Risk": "Medium", "Action": "Apply least privilege"}
        ]
        
        for finding in findings:
            severity = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity[finding['Risk']]} **{finding['Finding']}** - {finding['Users']}"):
                st.write(f"**Risk Level:** {finding['Risk']}")
                st.write(f"**Recommended Action:** {finding['Action']}")
                if st.button("🔧 Remediate", key=f"remediate_{finding['Finding']}", use_container_width=True):
                    st.success("✅ Remediation applied (Demo mode)")
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        AzureTheme.azure_section_header("🤖 AI-Powered IAM Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "97%", delta="↑ 2%")
        with col2:
            st.metric("Recommendations", "9", delta="↑ 3")
        with col3:
            st.metric("Security Issues", "23", delta="↓ 8")
        with col4:
            st.metric("Over-Privileged", "23 users", delta="Need review")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Reduce Admin Privileges", "desc": "12 users have Owner role but only use Contributor permissions. AI analysis shows 0 Owner actions in 90 days.", "impact": "Reduce attack surface by 35%", "confidence": 98, "auto_fix": True},
            {"title": "Enforce MFA for All Users", "desc": "157 users (12.6%) without MFA. 8 high-risk users identified.", "impact": "Block 99.9% of account compromise attempts", "confidence": 100, "auto_fix": True},
            {"title": "Remove Stale Service Principals", "desc": "34 service principals unused for 90+ days. Still have active credentials.", "impact": "Eliminate 34 potential attack vectors", "confidence": 96, "auto_fix": True},
            {"title": "Optimize Custom Roles", "desc": "8 custom roles have duplicate permissions with built-in roles.", "impact": "Simplify RBAC, reduce management overhead", "confidence": 94, "auto_fix": False}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if rec['auto_fix']:
                        if st.button("✅ Apply", key=f"iam_{i}"):
                            st.success("Applied! (Demo)")
                    else:
                        if st.button("📋 Guide", key=f"guide_{i}"):
                            st.info("Optimization guide shown")
                with col2:
                    if st.button("📊 Simulate", key=f"sim_{i}"):
                        st.info("Impact simulation shown")
        
        st.markdown("---")
        st.markdown("### 🔍 Privilege Analysis")
        
        st.markdown("**🔴 Over-Privileged Users (23):**")
        over_privs = [
            {"User": "john.doe@company.com", "Current": "Owner", "Required": "Contributor", "Unused Days": "90+"},
            {"User": "jane.smith@company.com", "Current": "Owner", "Required": "Reader", "Unused Days": "120+"}
        ]
        st.dataframe(pd.DataFrame(over_privs), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about identity & access:", height=80, key="iam_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(AzureADModule._generate_ai_response(query))
    
    @staticmethod
    def _render_reports(subscriptions):
        """Reports"""
        
        AzureTheme.azure_section_header("📤 Reports", "📊")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👥 User Access Report**")
            if st.button("📥 Generate", key="user_report", use_container_width=True):
                st.success("✅ Report generated (Demo)")
        with col2:
            st.markdown("**🔒 Security Audit Report**")
            if st.button("📥 Generate", key="security_report", use_container_width=True):
                st.success("✅ Report generated (Demo)")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """AI response"""
        
        q = query.lower()
        
        if "privilege" in q or "admin" in q:
            return """**🔍 Privilege Analysis:**

**Over-Privileged Users:** 23 identified

**Top Issues:**
1. 12 users with Owner role (use 0 Owner actions)
2. 8 admins without MFA (critical risk)
3. 34 service principals unused 90+ days

**AI Recommendations:**
```
Downgrade 12 users: Owner → Contributor
Enable MFA: 8 high-risk admins
Remove: 34 stale service principals
```

**Impact:** 
- Reduce attack surface by 35%
- Block 99.9% of account compromise
- Eliminate 34 attack vectors"""
        
        elif "mfa" in q or "security" in q:
            return """**🔐 MFA & Security Analysis:**

**Current:** 87.4% MFA adoption  
**Target:** 100%  
**Gap:** 157 users without MFA

**High-Risk Users (8):**
- admin@company.com (Owner, no MFA)
- 7 other privileged accounts

**AI Recommendation:**
1. Enable MFA for all users (Conditional Access)
2. Block sign-in without MFA for admins
3. Require MFA for sensitive operations

**Impact:** Block 99.9% of account compromise attempts**"""
        
        elif "role" in q or "rbac" in q:
            return """**🔑 RBAC Optimization:**

**Current:** 87 roles, 2,847 assignments  
**Issues:**
- 12 users: Owner (over-privileged)
- 8 custom roles: Duplicate built-in roles
- 34 stale assignments: >90 days unused

**AI Recommendations:**
1. Downgrade 12 users to least privilege
2. Consolidate 8 custom roles
3. Remove 34 stale assignments

**Expected:**
- Simplified RBAC structure
- 26% reduction in assignments
- Lower management overhead**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    AzureADModule.render()
