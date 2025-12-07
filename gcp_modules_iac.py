"""
Google Cloud Infrastructure as Code - AI-Powered Template Management
Intelligent template validation, drift detection, cost estimation, and security scanning
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPIaCModule:
    """AI-Enhanced GCP IaC Intelligence"""
    
    @staticmethod
    def render():
        """Render GCP IaC Intelligence Center"""
        
        GCPTheme.gcp_header(
            "Infrastructure as Code Intelligence",
            "AI-Powered IaC Management - Validate templates, detect drift, estimate costs",
            "📜"
        )
        
        projects = AppConfig.load_gcp_projects()
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample IaC data", "info")
        
        tabs = st.tabs(["📜 Templates", "🔍 Validation", "📊 Deployments", "🎯 Drift Detection", "💰 Cost Estimation", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            GCPIaCModule._render_templates(projects)
        with tabs[1]:
            GCPIaCModule._render_validation(projects)
        with tabs[2]:
            GCPIaCModule._render_deployments(projects)
        with tabs[3]:
            GCPIaCModule._render_drift(projects)
        with tabs[4]:
            GCPIaCModule._render_cost(projects)
        with tabs[5]:
            GCPIaCModule._render_ai_insights()
        with tabs[6]:
            GCPIaCModule._render_reports(projects)
    
    @staticmethod
    def _render_templates(projects):
        """Template management"""
        
        GCPTheme.gcp_section_header("📜 Deployment Manager & Terraform", "📋")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Templates", "94", delta="↑ 6")
        with col2:
            st.metric("Terraform", "68", delta="72%")
        with col3:
            st.metric("Deployment Manager", "26", delta="28%")
        with col4:
            st.metric("Active Deployments", "312", delta="↑ 18")
        with col5:
            st.metric("Validation Pass", "96.8%", delta="↑ 2.8%")
        
        st.markdown("---")
        
        # Template list
        st.markdown("### 📋 Recent Templates")
        
        templates = [
            {"Name": "gke-cluster.tf", "Type": "Terraform", "Size": "187 lines", "Status": "✅ Valid", "Last Modified": "1 hour ago", "Deployments": "8"},
            {"Name": "vpc-network.yaml", "Type": "DM", "Size": "124 lines", "Status": "✅ Valid", "Last Modified": "2 days ago", "Deployments": "23"},
            {"Name": "cloud-sql.tf", "Type": "Terraform", "Size": "245 lines", "Status": "⚠️ Warnings", "Last Modified": "4 days ago", "Deployments": "12"},
            {"Name": "compute-instance.yaml", "Type": "DM", "Size": "298 lines", "Status": "❌ Errors", "Last Modified": "6 days ago", "Deployments": "0"}
        ]
        st.dataframe(pd.DataFrame(templates), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Template editor
        st.markdown("### ✏️ Template Editor")
        
        template_code = st.text_area(
            "Edit Template:",
            value="""resource "google_storage_bucket" "main" {
  name          = "my-storage-bucket"
  location      = "US"
  force_destroy = false
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  encryption {
    default_kms_key_name = var.kms_key
  }
}""",
            height=200
        )
        
        if st.button("🔍 Validate Template", type="primary"):
            st.success("✅ Template valid (Demo mode)")
    
    @staticmethod
    def _render_validation(projects):
        """Template validation"""
        
        GCPTheme.gcp_section_header("🔍 Template Validation", "✅")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Valid Templates", "91", delta="96.8%")
        with col2:
            st.metric("Warnings", "3", delta="3.2%")
        with col3:
            st.metric("Errors", "1", delta="↓ 2")
        with col4:
            st.metric("Security Issues", "6", delta="↓ 5")
        
        st.markdown("---")
        
        # Validation results
        st.markdown("### 📊 Validation Results")
        
        results = [
            {"Template": "compute-instance.yaml", "Status": "❌ Error", "Issue": "Invalid zone format", "Severity": "High", "Line": "34"},
            {"Template": "cloud-sql.tf", "Status": "⚠️ Warning", "Issue": "Public IP enabled", "Severity": "Critical", "Line": "56"},
            {"Template": "gke-cluster.tf", "Status": "⚠️ Warning", "Issue": "Legacy metadata disabled", "Severity": "Low", "Line": "89"}
        ]
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Security scan
        st.markdown("### 🔒 Security Scan Results")
        
        security = [
            {"Finding": "Public IP on Cloud SQL", "Template": "cloud-sql.tf", "Risk": "Critical", "Recommendation": "Use private IP with VPC peering"},
            {"Finding": "No encryption key specified", "Template": "storage-bucket.yaml", "Risk": "High", "Recommendation": "Use CMEK for sensitive data"},
            {"Finding": "Default service account", "Template": "compute-instance.yaml", "Risk": "Medium", "Recommendation": "Create custom service account"}
        ]
        
        for sec in security:
            severity = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity[sec['Risk']]} **{sec['Finding']}** - {sec['Template']}"):
                st.write(f"**Risk Level:** {sec['Risk']}")
                st.write(f"**Recommendation:** {sec['Recommendation']}")
                if st.button("🔧 Auto-Fix", key=f"gcp_fix_{sec['Finding']}", use_container_width=True):
                    st.success("✅ Fixed (Demo mode)")
    
    @staticmethod
    def _render_deployments(projects):
        """Deployment tracking"""
        
        GCPTheme.gcp_section_header("📊 Deployment Tracking", "🚀")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Deployments", "312", delta="↑ 18")
        with col2:
            st.metric("Success Rate", "98.1%", delta="↑ 1.5%")
        with col3:
            st.metric("Failed", "6", delta="↓ 4")
        with col4:
            st.metric("In Progress", "2")
        
        st.markdown("---")
        
        # Recent deployments
        st.markdown("### 🚀 Recent Deployments")
        
        deployments = [
            {"Deployment": "gke-cluster-001", "Template": "gke-cluster.tf", "Status": "✅ Success", "Duration": "8m 45s", "Time": "20 min ago"},
            {"Deployment": "vpc-deploy-042", "Template": "vpc-network.yaml", "Status": "✅ Success", "Duration": "3m 23s", "Time": "2 hours ago"},
            {"Deployment": "sql-instance-012", "Template": "cloud-sql.tf", "Status": "🔄 Running", "Duration": "4m 12s", "Time": "Running..."},
            {"Deployment": "compute-vm-003", "Template": "compute-instance.yaml", "Status": "❌ Failed", "Duration": "1m 08s", "Time": "3 hours ago"}
        ]
        st.dataframe(pd.DataFrame(deployments), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_drift(projects):
        """Drift detection"""
        
        GCPTheme.gcp_section_header("🎯 Configuration Drift Detection", "🔍")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Resources Monitored", "1,247", delta="↑ 34")
        with col2:
            st.metric("Drifted Resources", "42", delta="3.4%")
        with col3:
            st.metric("Auto-Importable", "36", delta="86%")
        
        st.markdown("---")
        
        # Drift analysis
        st.markdown("### 🔍 Configuration Drift")
        
        drift = [
            {"Resource": "gke-cluster-prod", "Type": "GKE Cluster", "Drift": "Node count changed", "Current": "8 nodes", "Expected": "6 nodes"},
            {"Resource": "storage-bucket-data", "Type": "Storage Bucket", "Drift": "Public access enabled", "Current": "allUsers", "Expected": "Private"},
            {"Resource": "compute-instance-web", "Type": "Compute Instance", "Drift": "Machine type upgraded", "Current": "n2-standard-4", "Expected": "n2-standard-2"}
        ]
        
        for d in drift:
            with st.expander(f"⚠️ **{d['Resource']}** - {d['Drift']}"):
                st.write(f"**Resource Type:** {d['Type']}")
                st.write(f"**Current Value:** {d['Current']}")
                st.write(f"**Expected Value:** {d['Expected']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Revert", key=f"gcp_revert_{d['Resource']}", use_container_width=True):
                        st.success("✅ Reverted (Demo)")
                with col2:
                    if st.button("📥 Import", key=f"gcp_import_{d['Resource']}", use_container_width=True):
                        st.success("✅ Imported (Demo)")
    
    @staticmethod
    def _render_cost(projects):
        """Cost estimation"""
        
        GCPTheme.gcp_section_header("💰 Cost Estimation", "💵")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Monthly", "$15,680", delta="Current templates")
        with col2:
            st.metric("Optimized", "$10,240", delta="-$5,440/mo")
        with col3:
            st.metric("Savings", "35%", delta="Potential")
        
        st.markdown("---")
        
        # Cost breakdown
        st.markdown("### 💰 Cost Breakdown by Template")
        
        costs = [
            {"Template": "gke-cluster.tf", "Resources": "15", "Monthly Cost": "$5,680", "Optimized": "$3,420", "Savings": "$2,260"},
            {"Template": "cloud-sql.tf", "Resources": "4", "Monthly Cost": "$3,240", "Optimized": "$2,180", "Savings": "$1,060"},
            {"Template": "compute-instance.yaml", "Resources": "12", "Monthly Cost": "$4,760", "Optimized": "$3,640", "Savings": "$1,120"}
        ]
        st.dataframe(pd.DataFrame(costs), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        GCPTheme.gcp_section_header("🤖 AI-Powered IaC Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "97%", delta="↑ 3%")
        with col2:
            st.metric("Recommendations", "10", delta="↑ 3")
        with col3:
            st.metric("Security Issues", "6", delta="↓ 5")
        with col4:
            st.metric("Cost Savings", "$5,440/mo", delta="35%")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Use Preemptible VMs", "desc": "GKE node pool using regular VMs. Workload tolerates interruptions. Preemptible VMs 80% cheaper.", "impact": "Save $2,260/month (40% cost reduction)", "confidence": 98, "auto_fix": True},
            {"title": "Enable Private IP for Cloud SQL", "desc": "Cloud SQL instance has public IP. Security risk. Use VPC peering for private access.", "impact": "Eliminate public internet exposure (Critical)", "confidence": 100, "auto_fix": True},
            {"title": "Implement CMEK Encryption", "desc": "Storage buckets using Google-managed encryption. CMEK provides customer control.", "impact": "Meet compliance requirements (HIPAA, PCI-DSS)", "confidence": 96, "auto_fix": True},
            {"title": "Use Committed Use Discounts", "desc": "Compute resources eligible for CUDs. 1-year commitment provides 37% discount.", "impact": "Save $1,120/month with minimal risk", "confidence": 94, "auto_fix": False}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if rec['auto_fix']:
                        if st.button("✅ Apply", key=f"gcp_iac_{i}"):
                            st.success("Applied! (Demo)")
                    else:
                        if st.button("📋 Guide", key=f"guide_{i}"):
                            st.info("Guide shown")
                with col2:
                    if st.button("📊 Simulate", key=f"sim_{i}"):
                        st.info("Impact simulation shown")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about IaC:", height=80, key="gcp_iac_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(GCPIaCModule._generate_ai_response(query))
    
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
        
        if "cost" in q or "save" in q:
            return """**💰 GCP IaC Cost Optimization:**

**Current:** $15,680/month  
**Optimized:** $10,240/month  
**Savings:** $5,440/month (35%)

**AI-Identified Opportunities:**

1. **Preemptible VMs for GKE** ($2,260/mo)
   - Template: gke-cluster.tf
   - Current: Regular node pool
   - Recommended: Preemptible nodes
   - Discount: 80% savings
   ```hcl
   preemptible = true
   ```

2. **Committed Use Discounts** ($1,120/mo)
   - Template: compute-instance.yaml
   - Recommendation: 1-year CUD
   - Discount: 37% savings
   
3. **Rightsize Compute** ($1,060/mo)
   - Cloud SQL over-provisioned
   - Current: db-n1-standard-4
   - Recommended: db-n1-standard-2

**Quick Wins:** $3,380/mo available via auto-fix**"""
        
        elif "security" in q:
            return """**🔒 GCP IaC Security Analysis:**

**Security Issues Found:** 6

**Critical (2):**
1. Public IP on Cloud SQL (cloud-sql.tf)
   - Risk: Direct internet exposure
   - Fix: Use private IP + VPC peering

2. No CMEK encryption (storage-bucket.yaml)
   - Risk: No customer key control
   - Fix: Implement CMEK
   ```hcl
   encryption {
     default_kms_key_name = google_kms_crypto_key.key.id
   }
   ```

**High (2):**
1. Default service account (compute-instance.yaml)
2. Legacy metadata enabled (gke-cluster.tf)

**Medium (2):**
1. No VPC Service Controls
2. Missing audit logs config

**Auto-fix available for 5/6 issues**"""
        
        elif "drift" in q:
            return """**🎯 GCP Configuration Drift:**

**Drifted Resources:** 42 (3.4%)

**Top Drift Types:**
1. Console modifications (28 resources)
2. gcloud CLI changes (10 resources)
3. API updates (4 resources)

**Critical Drift:**
- gke-cluster-prod: 6 → 8 nodes
  Impact: +$920/month cost increase
  
- storage-bucket-data: Public access enabled
  Impact: Security risk (Critical)

**AI Recommendations:**
1. Revert 28 console changes via Terraform
2. Import 10 CLI changes to state
3. Use Organization Policies to prevent drift

**Terraform Import:**
```bash
terraform import google_container_cluster.main \\
  projects/PROJECT/locations/REGION/clusters/NAME
```

**Prevention:** Enable drift detection automation**"""
        
        return f"AI analysis for: {query}"
