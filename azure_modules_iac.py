"""
Azure Infrastructure as Code - AI-Powered Template Management
Intelligent template validation, drift detection, cost estimation, and security scanning
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure_theme import AzureTheme
from config_settings import AppConfig

class AzureIaCModule:
    """AI-Enhanced Azure IaC Intelligence"""
    
    @staticmethod
    def render():
        """Render Azure IaC Intelligence Center"""
        
        AzureTheme.azure_header(
            "Infrastructure as Code Intelligence",
            "AI-Powered IaC Management - Validate templates, detect drift, estimate costs",
            "📜"
        )
        
        subscriptions = AppConfig.load_azure_subscriptions()
        
        if st.session_state.get('mode') == 'Demo':
            AzureTheme.azure_info_box("Demo Mode", "Using sample IaC data", "info")
        
        tabs = st.tabs(["📜 Templates", "🔍 Validation", "📊 Deployments", "🎯 Drift Detection", "💰 Cost Estimation", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            AzureIaCModule._render_templates(subscriptions)
        with tabs[1]:
            AzureIaCModule._render_validation(subscriptions)
        with tabs[2]:
            AzureIaCModule._render_deployments(subscriptions)
        with tabs[3]:
            AzureIaCModule._render_drift(subscriptions)
        with tabs[4]:
            AzureIaCModule._render_cost(subscriptions)
        with tabs[5]:
            AzureIaCModule._render_ai_insights()
        with tabs[6]:
            AzureIaCModule._render_reports(subscriptions)
    
    @staticmethod
    def _render_templates(subscriptions):
        """Template management"""
        
        AzureTheme.azure_section_header("📜 ARM Templates & Bicep", "📋")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Templates", "87", delta="↑ 5")
        with col2:
            st.metric("ARM Templates", "45", delta="52%")
        with col3:
            st.metric("Bicep Files", "42", delta="48%")
        with col4:
            st.metric("Active Deployments", "234", delta="↑ 12")
        with col5:
            st.metric("Validation Pass", "94.2%", delta="↑ 2.1%")
        
        st.markdown("---")
        
        # Template list
        st.markdown("### 📋 Recent Templates")
        
        templates = [
            {"Name": "vm-deployment.bicep", "Type": "Bicep", "Size": "234 lines", "Status": "✅ Valid", "Last Modified": "2 hours ago", "Deployments": "12"},
            {"Name": "storage-account.json", "Type": "ARM", "Size": "156 lines", "Status": "✅ Valid", "Last Modified": "1 day ago", "Deployments": "45"},
            {"Name": "vnet-config.bicep", "Type": "Bicep", "Size": "189 lines", "Status": "⚠️ Warnings", "Last Modified": "3 days ago", "Deployments": "23"},
            {"Name": "app-service.json", "Type": "ARM", "Size": "412 lines", "Status": "❌ Errors", "Last Modified": "5 days ago", "Deployments": "0"}
        ]
        st.dataframe(pd.DataFrame(templates), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Template editor
        st.markdown("### ✏️ Template Editor")
        
        template_code = st.text_area(
            "Edit Template:",
            value="""resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageaccount'
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}""",
            height=200
        )
        
        if st.button("🔍 Validate Template", type="primary"):
            st.success("✅ Template valid (Demo mode)")
    
    @staticmethod
    def _render_validation(subscriptions):
        """Template validation"""
        
        AzureTheme.azure_section_header("🔍 Template Validation", "✅")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valid Templates", "82", delta="94.2%")
        with col2:
            st.metric("Warnings", "5", delta="5.8%")
        with col3:
            st.metric("Errors", "2", delta="↓ 3")
        with col4:
            st.metric("Security Issues", "8", delta="↓ 4")
        
        st.markdown("---")
        
        # Validation results
        st.markdown("### 📊 Validation Results")
        
        results = [
            {"Template": "app-service.json", "Status": "❌ Error", "Issue": "Invalid API version", "Severity": "High", "Line": "42"},
            {"Template": "vnet-config.bicep", "Status": "⚠️ Warning", "Issue": "Missing tags", "Severity": "Low", "Line": "23"},
            {"Template": "vm-deployment.bicep", "Status": "⚠️ Warning", "Issue": "Hardcoded password", "Severity": "Critical", "Line": "67"}
        ]
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Security scan
        st.markdown("### 🔒 Security Scan Results")
        
        security = [
            {"Finding": "Public access enabled", "Template": "storage-account.json", "Risk": "High", "Recommendation": "Set publicNetworkAccess to Disabled"},
            {"Finding": "No encryption at rest", "Template": "sql-database.json", "Risk": "Critical", "Recommendation": "Enable Transparent Data Encryption"},
            {"Finding": "Weak TLS version", "Template": "app-service.json", "Risk": "Medium", "Recommendation": "Set minTlsVersion to TLS1_3"}
        ]
        
        for sec in security:
            severity = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity[sec['Risk']]} **{sec['Finding']}** - {sec['Template']}"):
                st.write(f"**Risk Level:** {sec['Risk']}")
                st.write(f"**Recommendation:** {sec['Recommendation']}")
                if st.button("🔧 Auto-Fix", key=f"fix_{sec['Finding']}", use_container_width=True):
                    st.success("✅ Fixed (Demo mode)")
    
    @staticmethod
    def _render_deployments(subscriptions):
        """Deployment tracking"""
        
        AzureTheme.azure_section_header("📊 Deployment Tracking", "🚀")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Deployments", "234", delta="↑ 12")
        with col2:
            st.metric("Success Rate", "96.8%", delta="↑ 1.2%")
        with col3:
            st.metric("Failed", "8", delta="↓ 3")
        with col4:
            st.metric("In Progress", "3")
        
        st.markdown("---")
        
        # Recent deployments
        st.markdown("### 🚀 Recent Deployments")
        
        deployments = [
            {"Deployment": "vm-deployment-001", "Template": "vm-deployment.bicep", "Status": "✅ Succeeded", "Duration": "4m 23s", "Time": "15 min ago"},
            {"Deployment": "storage-deploy-042", "Template": "storage-account.json", "Status": "✅ Succeeded", "Duration": "2m 12s", "Time": "1 hour ago"},
            {"Deployment": "vnet-config-012", "Template": "vnet-config.bicep", "Status": "🔄 Running", "Duration": "1m 45s", "Time": "Running..."},
            {"Deployment": "app-service-003", "Template": "app-service.json", "Status": "❌ Failed", "Duration": "0m 34s", "Time": "2 hours ago"}
        ]
        st.dataframe(pd.DataFrame(deployments), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_drift(subscriptions):
        """Drift detection"""
        
        AzureTheme.azure_section_header("🎯 Configuration Drift Detection", "🔍")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Resources Monitored", "847", delta="↑ 23")
        with col2:
            st.metric("Drifted Resources", "34", delta="4.0%")
        with col3:
            st.metric("Auto-Importable", "28", delta="82%")
        
        st.markdown("---")
        
        # Drift analysis
        st.markdown("### 🔍 Configuration Drift")
        
        drift = [
            {"Resource": "myvm-prod-01", "Type": "Virtual Machine", "Drift": "VM size changed", "Current": "Standard_D4s_v3", "Expected": "Standard_D2s_v3"},
            {"Resource": "mystorageacct", "Type": "Storage Account", "Drift": "Public access enabled", "Current": "Enabled", "Expected": "Disabled"},
            {"Resource": "myapp-service", "Type": "App Service", "Drift": "Tags modified", "Current": "env=test", "Expected": "env=prod"}
        ]
        
        for d in drift:
            with st.expander(f"⚠️ **{d['Resource']}** - {d['Drift']}"):
                st.write(f"**Resource Type:** {d['Type']}")
                st.write(f"**Current Value:** {d['Current']}")
                st.write(f"**Expected Value:** {d['Expected']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Revert to Template", key=f"revert_{d['Resource']}", use_container_width=True):
                        st.success("✅ Reverted (Demo)")
                with col2:
                    if st.button("📥 Import to Template", key=f"import_{d['Resource']}", use_container_width=True):
                        st.success("✅ Imported (Demo)")
    
    @staticmethod
    def _render_cost(subscriptions):
        """Cost estimation"""
        
        AzureTheme.azure_section_header("💰 Cost Estimation", "💵")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Monthly", "$12,450", delta="Current templates")
        with col2:
            st.metric("Optimized", "$8,320", delta="-$4,130/mo")
        with col3:
            st.metric("Savings", "33%", delta="Potential")
        
        st.markdown("---")
        
        # Cost breakdown
        st.markdown("### 💰 Cost Breakdown by Template")
        
        costs = [
            {"Template": "vm-deployment.bicep", "Resources": "12", "Monthly Cost": "$4,240", "Optimized": "$2,680", "Savings": "$1,560"},
            {"Template": "storage-account.json", "Resources": "8", "Monthly Cost": "$2,340", "Optimized": "$1,890", "Savings": "$450"},
            {"Template": "vnet-config.bicep", "Resources": "15", "Monthly Cost": "$3,870", "Optimized": "$2,750", "Savings": "$1,120"}
        ]
        st.dataframe(pd.DataFrame(costs), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        AzureTheme.azure_section_header("🤖 AI-Powered IaC Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "96%", delta="↑ 2%")
        with col2:
            st.metric("Recommendations", "12", delta="↑ 4")
        with col3:
            st.metric("Security Issues", "8", delta="↓ 4")
        with col4:
            st.metric("Cost Savings", "$4,130/mo", delta="33%")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Optimize VM Sizing", "desc": "VM template uses Standard_D4s_v3 but AI analysis shows avg CPU 23%. Standard_D2s_v3 sufficient.", "impact": "Save $1,560/month (37% cost reduction)", "confidence": 98, "auto_fix": True},
            {"title": "Enable Encryption at Rest", "desc": "Storage account template missing encryption. Critical security issue for compliance.", "impact": "Meet compliance requirements (SOC2, PCI-DSS)", "confidence": 100, "auto_fix": True},
            {"title": "Use Managed Identities", "desc": "App service using connection strings. Managed identities eliminate credential management.", "impact": "Remove 12 stored credentials, improve security", "confidence": 96, "auto_fix": True},
            {"title": "Implement Tags Strategy", "desc": "5 templates missing required tags (CostCenter, Environment, Owner).", "impact": "Enable cost allocation and governance", "confidence": 94, "auto_fix": True}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if rec['auto_fix']:
                        if st.button("✅ Apply", key=f"iac_{i}"):
                            st.success("Applied! (Demo)")
                with col2:
                    if st.button("📊 Simulate", key=f"sim_{i}"):
                        st.info("Cost impact simulation shown")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about IaC:", height=80, key="iac_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(AzureIaCModule._generate_ai_response(query))
    
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
        
        if "cost" in q or "save" in q or "optimize" in q:
            return """**💰 IaC Cost Optimization:**

**Current:** $12,450/month  
**Optimized:** $8,320/month  
**Savings:** $4,130/month (33%)

**AI-Identified Opportunities:**

1. **VM Right-Sizing** ($1,560/mo)
   - Template: vm-deployment.bicep
   - Current: Standard_D4s_v3
   - Recommended: Standard_D2s_v3
   - Reason: Avg CPU 23%, memory 34%

2. **Storage Tier Optimization** ($450/mo)
   - Template: storage-account.json
   - Current: Premium SSD
   - Recommended: Standard SSD
   - Reason: IOPS requirements met by Standard

3. **Reserved Instances** ($1,120/mo)
   - Template: vnet-config.bicep
   - Recommendation: 1-year RI commitment
   - Discount: 29% savings

**Quick Wins:** Apply all 3 recommendations via auto-fix**"""
        
        elif "security" in q or "validate" in q:
            return """**🔒 Template Security Analysis:**

**Security Issues Found:** 8

**Critical (3):**
1. Public access enabled (storage-account.json)
2. No encryption at rest (sql-database.json)
3. Hardcoded credentials (app-service.json)

**High (2):**
1. Weak TLS version (app-service.json)
2. Missing network isolation (vm-deployment.bicep)

**Medium (3):**
1. Missing tags (vnet-config.bicep)
2. No diagnostic logs (storage-account.json)
3. Public IP assigned (vm-deployment.bicep)

**AI Recommendations:**
```bicep
// Fix 1: Disable public access
publicNetworkAccess: 'Disabled'

// Fix 2: Enable encryption
transparentDataEncryption: {
  status: 'Enabled'
}

// Fix 3: Use managed identity
identity: {
  type: 'SystemAssigned'
}
```

**Auto-fix available for all 8 issues**"""
        
        elif "drift" in q:
            return """**🎯 Configuration Drift Analysis:**

**Drifted Resources:** 34 (4.0% of total)

**Top Drift Categories:**
1. Manual changes (23 resources)
2. Console modifications (8 resources)
3. Script updates (3 resources)

**Critical Drift:**
- myvm-prod-01: VM size changed manually
  Current: Standard_D4s_v3
  Template: Standard_D2s_v3
  Impact: +$120/month cost increase

**AI Recommendations:**
1. Revert 23 manual changes to template
2. Import 8 console changes to IaC
3. Update templates for 3 script changes

**Automation:**
- 28 resources auto-importable (82%)
- 6 resources require manual review

**Prevention:** Enable Azure Policy to block manual changes**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    AzureIaCModule.render()
