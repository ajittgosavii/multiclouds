"""
GCP Organization & Project Management
Enterprise-grade project organization, policies, and governance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPOrganizationManagement:
    """Enterprise GCP Organization & Project Management"""
    
    @staticmethod
    def render():
        """Main render function"""
        
        st.title("🏢 GCP Organization & Project Management")
        
        st.info("📌 This module requires organization admin credentials")
        
        # Organization selection
        st.markdown("**Select Organization**")
        st.selectbox("", ["POC ORGANIZATION", "vanguard-infosys.com", "enterprise.com"], label_visibility="collapsed")
        
        st.markdown("---")
        
        # 6 comprehensive tabs matching AWS
        tabs = st.tabs([
            "🏢 Organization",
            "📁 Folders",
            "📋 Projects",
            "📜 Policies",
            "➕ Create Project",
            "🏷️ Labels"
        ])
        
        with tabs[0]:
            GCPOrganizationManagement._render_organization()
        with tabs[1]:
            GCPOrganizationManagement._render_folders()
        with tabs[2]:
            GCPOrganizationManagement._render_projects()
        with tabs[3]:
            GCPOrganizationManagement._render_policies()
        with tabs[4]:
            GCPOrganizationManagement._render_create_project()
        with tabs[5]:
            GCPOrganizationManagement._render_labels()
    
    @staticmethod
    def _render_organization():
        """Organization Overview tab"""
        
        st.markdown("## 🏢 Organization Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Organization ID")
            st.markdown("**o-gcp9g6fr6ky**")
            
            st.markdown("### Organization Name")
            st.markdown("**vanguard-infosys.com**")
        
        with col2:
            st.markdown("### Feature Set")
            st.markdown("**ALL**")
            
            st.markdown("### Admin Email")
            st.markdown("**admin@vanguard-infosys.com**")
        
        st.markdown("---")
        
        # Organization Hierarchy
        st.markdown("### Organization Hierarchy")
        
        hierarchy = """
```
vanguard-infosys.com (Organization)
├── Production (Folder)
│   ├── prod-web-app-001 (Project)
│   ├── prod-api-services-001 (Project)
│   └── prod-data-platform-001 (Project)
├── Development (Folder)
│   ├── dev-testing-001 (Project)
│   ├── dev-sandbox-001 (Project)
│   └── dev-experiments-001 (Project)
├── Staging (Folder)
│   └── staging-preview-001 (Project)
└── Shared-Services (Folder)
    ├── network-hub-001 (Project)
    └── security-center-001 (Project)
```
"""
        st.code(hierarchy, language="")
        
        st.markdown("---")
        
        # Organization Statistics
        st.markdown("### Organization Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", "34", delta="Active")
        with col2:
            st.metric("Total Folders", "4", delta="Top-level")
        with col3:
            st.metric("Organization Policies", "28", delta="Enforced")
        with col4:
            st.metric("Total Spend", "$428,950/mo", delta="↑ $18,340")
        
        st.markdown("---")
        
        # Available Policy Types
        st.markdown("### Available Policy Types")
        
        policy_types = [
            {"Type": "ORGANIZATION_POLICY", "Status": "ENABLED"},
            {"Type": "IAM_POLICY", "Status": "ENABLED"},
            {"Type": "RESOURCE_MANAGER_POLICY", "Status": "ENABLED"},
        ]
        st.dataframe(pd.DataFrame(policy_types), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_folders():
        """Folders tab"""
        
        st.markdown("## 📁 Folder Management")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Folders", "12", delta="↑ 1")
        with col2:
            st.metric("Top-Level", "4", delta="33.3%")
        with col3:
            st.metric("Nested Folders", "8", delta="66.7%")
        with col4:
            st.metric("Projects", "34", delta="Total")
        
        st.markdown("---")
        
        # Folder list
        st.markdown("### Folder List")
        
        folders = [
            {"Name": "Production", "ID": "folders/123456789", "Parent": "Organization", "Projects": "12", "Policies": "18"},
            {"Name": "Development", "ID": "folders/234567890", "Parent": "Organization", "Projects": "15", "Policies": "12"},
            {"Name": "Staging", "ID": "folders/345678901", "Parent": "Organization", "Projects": "4", "Policies": "14"},
            {"Name": "Shared-Services", "ID": "folders/456789012", "Parent": "Organization", "Projects": "3", "Policies": "20"},
        ]
        st.dataframe(pd.DataFrame(folders), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Selected folder details
        st.markdown("### Folder Details")
        
        selected_folder = st.selectbox("Select Folder", ["Production", "Development", "Staging"])
        
        if selected_folder:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Folder Name:** Production")
                st.write("**Folder ID:** folders/123456789")
                st.write("**Parent:** organizations/o-gcp9g6fr6ky")
            with col2:
                st.write("**Projects:** 12")
                st.write("**Organization Policies:** 18")
                st.write("**Created:** 2023-01-15")
            
            st.markdown("**Projects in this folder:**")
            st.write("• prod-web-app-001")
            st.write("• prod-api-services-001")
            st.write("• prod-data-platform-001")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Create Folder", use_container_width=True):
                st.info("Folder creation form would open")
        with col2:
            if st.button("🔄 Refresh Hierarchy", use_container_width=True):
                st.success("✅ Hierarchy refreshed")
    
    @staticmethod
    def _render_projects():
        """Projects tab"""
        
        st.markdown("## 📋 GCP Projects")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", "34", delta="Active")
        with col2:
            st.metric("Production", "12", delta="35.3%")
        with col3:
            st.metric("Development", "15", delta="44.1%")
        with col4:
            st.metric("Total Spend", "$428,950/mo", delta="↑ $18,340")
        
        st.markdown("---")
        
        # Project list
        st.markdown("### Project List")
        
        projects = [
            {"Name": "prod-web-app-001", "ID": "proj-12345", "Number": "123456789012", "State": "✅ ACTIVE", "Folder": "Production", "Spend/mo": "$58,920", "Resources": "3,456"},
            {"Name": "prod-api-services-001", "ID": "proj-23456", "Number": "234567890123", "State": "✅ ACTIVE", "Folder": "Production", "Spend/mo": "$45,680", "Resources": "2,134"},
            {"Name": "dev-testing-001", "ID": "proj-34567", "Number": "345678901234", "State": "✅ ACTIVE", "Folder": "Development", "Spend/mo": "$15,670", "Resources": "1,023"},
            {"Name": "staging-preview-001", "ID": "proj-45678", "Number": "456789012345", "State": "⚠️ SUSPENDED", "Folder": "Staging", "Spend/mo": "$12,340", "Resources": "567"},
        ]
        st.dataframe(pd.DataFrame(projects), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Selected project details
        st.markdown("### Project Details")
        
        selected_project = st.selectbox("Select Project", ["prod-web-app-001", "prod-api-services-001"])
        
        if selected_project:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Project Name:** prod-web-app-001")
                st.write("**Project ID:** proj-12345")
                st.write("**Project Number:** 123456789012")
                st.write("**State:** ACTIVE")
            with col2:
                st.write("**Monthly Spend:** $58,920")
                st.write("**Resources:** 3,456")
                st.write("**Folder:** Production")
                st.write("**Created:** 2023-02-20")
            
            st.markdown("**Labels:**")
            st.write("environment: production")
            st.write("cost-center: engineering")
            st.write("owner: platform-team@company.com")
    
    @staticmethod
    def _render_policies():
        """Organization Policies tab"""
        
        st.markdown("## 📜 Organization Policy Management")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Policies", "189", delta="Active")
        with col2:
            st.metric("Enforced", "156", delta="82.5%")
        with col3:
            st.metric("Audit Only", "33", delta="17.5%")
        with col4:
            st.metric("Non-Compliant", "287", delta="Resources")
        
        st.markdown("---")
        
        # Policy Categories
        st.markdown("### Policy Constraints")
        
        categories = [
            {"Constraint": "constraints/compute.vmExternalIpAccess", "Type": "List", "Status": "✅ Enforced", "Scope": "Organization"},
            {"Constraint": "constraints/iam.allowedPolicyMemberDomains", "Type": "List", "Status": "✅ Enforced", "Scope": "Organization"},
            {"Constraint": "constraints/storage.uniformBucketLevelAccess", "Type": "Boolean", "Status": "✅ Enforced", "Scope": "Organization"},
            {"Constraint": "constraints/compute.requireShieldedVm", "Type": "Boolean", "Status": "✅ Enforced", "Scope": "Production Folder"},
            {"Constraint": "constraints/sql.restrictPublicIp", "Type": "Boolean", "Status": "✅ Enforced", "Scope": "Production Folder"},
        ]
        st.dataframe(pd.DataFrame(categories), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Policy Details
        st.markdown("### Active Organization Policies")
        
        policies = [
            {"Policy": "Restrict VM external IPs", "Constraint": "compute.vmExternalIpAccess", "Scope": "Organization", "Compliant": "3,169", "Non-Compliant": "287"},
            {"Policy": "Require uniform bucket access", "Constraint": "storage.uniformBucketLevelAccess", "Scope": "Organization", "Compliant": "5,678", "Non-Compliant": "0"},
            {"Policy": "Allowed IAM domains", "Constraint": "iam.allowedPolicyMemberDomains", "Scope": "Organization", "Compliant": "All", "Non-Compliant": "0"},
        ]
        st.dataframe(pd.DataFrame(policies), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Create Policy", use_container_width=True):
                st.info("Policy creation form would open")
        with col2:
            if st.button("📊 Compliance Report", use_container_width=True):
                st.success("✅ Generating compliance report...")
    
    @staticmethod
    def _render_create_project():
        """Create Project tab"""
        
        st.markdown("## ➕ Create GCP Project")
        
        st.info("💡 Create a new GCP project in your organization")
        
        with st.form("create_project_form"):
            st.markdown("### Project Configuration")
            
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("Project Name", placeholder="e.g., prod-web-app-002")
                project_id = st.text_input("Project ID", placeholder="unique-project-id-123")
                folder = st.selectbox("Parent Folder", ["Production", "Development", "Staging", "Shared-Services"])
            
            with col2:
                billing_account = st.selectbox("Billing Account", ["Billing Account 1 (012345-6789AB)", "Billing Account 2 (ABCDEF-123456)"])
                owner_email = st.text_input("Owner Email", placeholder="owner@company.com")
                auto_create_network = st.checkbox("Auto-create default network", value=False)
            
            st.markdown("### Labels")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("environment", value="production")
                st.text_input("cost-center", value="engineering")
            with col2:
                st.text_input("owner", value="")
                st.text_input("managed-by", value="terraform")
            
            st.markdown("### Organization Policies to Apply")
            st.multiselect(
                "Select policies",
                [
                    "Restrict VM external IPs",
                    "Require uniform bucket access",
                    "Require Shielded VMs",
                    "Restrict SQL public IPs",
                    "Allowed IAM domains"
                ],
                default=["Restrict VM external IPs", "Require uniform bucket access"]
            )
            
            st.markdown("### APIs to Enable")
            st.multiselect(
                "Select APIs",
                [
                    "Compute Engine API",
                    "Cloud Storage API",
                    "Cloud SQL API",
                    "Cloud Functions API",
                    "Cloud Run API"
                ],
                default=["Compute Engine API", "Cloud Storage API"]
            )
            
            submitted = st.form_submit_button("🚀 Create Project", type="primary", use_container_width=True)
            if submitted:
                st.success(f"✅ Project '{project_name}' (ID: {project_id}) created successfully!")
                st.info("⏳ Project initialization may take 30-60 seconds...")
    
    @staticmethod
    def _render_labels():
        """Labels tab"""
        
        st.markdown("## 🏷️ Label Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Labeled Resources", "91%", delta="↑ 6%")
        with col2:
            st.metric("Required Labels", "5", delta="Enforced")
        with col3:
            st.metric("Missing Labels", "1,456", delta="Resources")
        
        st.markdown("---")
        
        # Label Compliance
        st.markdown("### Label Compliance")
        
        label_compliance = [
            {"Label": "environment", "Required": "✅ Yes", "Coverage": "95%", "Missing": "623 resources"},
            {"Label": "cost-center", "Required": "✅ Yes", "Coverage": "89%", "Missing": "1,456 resources"},
            {"Label": "owner", "Required": "✅ Yes", "Coverage": "93%", "Missing": "892 resources"},
            {"Label": "team", "Required": "✅ Yes", "Coverage": "81%", "Missing": "2,345 resources"},
            {"Label": "application", "Required": "❌ No", "Coverage": "52%", "Missing": "5,678 resources"},
        ]
        st.dataframe(pd.DataFrame(label_compliance), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Label Values
        st.markdown("### Common Label Values")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**environment:**")
            st.write("• production (42%)")
            st.write("• development (38%)")
            st.write("• staging (15%)")
            st.write("• testing (5%)")
        
        with col2:
            st.markdown("**cost-center:**")
            st.write("• engineering (54%)")
            st.write("• operations (21%)")
            st.write("• security (14%)")
            st.write("• finance (11%)")
        
        st.markdown("---")
        
        # Label Key Management
        st.markdown("### Label Key Management")
        
        st.info("💡 GCP supports both project labels and resource labels")
        
        label_keys = [
            {"Key": "environment", "Type": "Standard", "Usage": "12,456 resources"},
            {"Key": "cost-center", "Type": "Standard", "Usage": "11,234 resources"},
            {"Key": "owner", "Type": "Standard", "Usage": "10,987 resources"},
            {"Key": "managed-by", "Type": "Automation", "Usage": "9,876 resources"},
        ]
        st.dataframe(pd.DataFrame(label_keys), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔧 Bulk Label Resources", use_container_width=True):
                st.info("Bulk labeling wizard would open")
        with col2:
            if st.button("📊 Label Report", use_container_width=True):
                st.success("✅ Generating label compliance report...")

# Module-level render function
def render():
    """Module-level render function"""
    GCPOrganizationManagement.render()
