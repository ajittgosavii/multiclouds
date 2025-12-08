"""
GCP Provisioning & Deployment Module - Infrastructure Deployment WITH CI/CD INTEGRATION
Automated deployment workflows using Deployment Manager/Terraform, multi-region, rollback
Enhanced with CI/CD pipeline monitoring and approval workflows
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from auth_azure_sso import require_permission

# ============================================================================
# CI/CD INTEGRATION (DEMO MODE - Shows sample data)
# ============================================================================

class CICDDeployment:
    """Represents a CI/CD pipeline deployment"""
    def __init__(self, pipeline_id, pipeline_name, status, environment, deployment_name,
                 commit_hash, commit_message, author, triggered_at, completed_at=None,
                 approval_required=False, pipeline_url=None):
        self.pipeline_id = pipeline_id
        self.pipeline_name = pipeline_name
        self.status = status
        self.environment = environment
        self.deployment_name = deployment_name
        self.commit_hash = commit_hash
        self.commit_message = commit_message
        self.author = author
        self.triggered_at = triggered_at
        self.completed_at = completed_at
        self.approval_required = approval_required
        self.pipeline_url = pipeline_url

class CICDIntegrationManager:
    """Manages CI/CD pipeline integrations - Demo Mode"""
    
    def __init__(self):
        """Initialize with demo data"""
        self.demo_mode = True
    
    def get_recent_deployments(self, limit=10):
        """Get demo deployment data"""
        now = datetime.now()
        
        return [
            CICDDeployment(
                pipeline_id="CB-1234",
                pipeline_name="Deploy Infrastructure",
                status="success",
                environment="production",
                deployment_name="prod-vpc-deployment",
                commit_hash="abc1234",
                commit_message="Add production VPC with 3 subnets",
                author="John Doe",
                triggered_at=now - timedelta(hours=2),
                completed_at=now - timedelta(hours=1, minutes=45),
                pipeline_url="#"
            ),
            CICDDeployment(
                pipeline_id="CB-1235",
                pipeline_name="Deploy Infrastructure",
                status="pending_approval",
                environment="production",
                deployment_name="prod-sql-deployment",
                commit_hash="def5678",
                commit_message="Add production Cloud SQL with read replicas",
                author="Jane Smith",
                triggered_at=now - timedelta(minutes=30),
                completed_at=None,
                approval_required=True,
                pipeline_url="#"
            ),
            CICDDeployment(
                pipeline_id="CB-1233",
                pipeline_name="Deploy Infrastructure",
                status="success",
                environment="staging",
                deployment_name="staging-app-deployment",
                commit_hash="def5678",
                commit_message="Deploy staging Cloud Run service",
                author="Jane Smith",
                triggered_at=now - timedelta(minutes=45),
                completed_at=now - timedelta(minutes=35),
                pipeline_url="#"
            ),
            CICDDeployment(
                pipeline_id="CB-1230",
                pipeline_name="Deploy Infrastructure",
                status="running",
                environment="staging",
                deployment_name="staging-update-deployment",
                commit_hash="jkl3456",
                commit_message="Update Cloud Functions",
                author="Alice Johnson",
                triggered_at=now - timedelta(minutes=10),
                completed_at=None,
                pipeline_url="#"
            ),
        ]
    
    def approve_deployment(self, pipeline_id):
        """Approve a deployment (demo)"""
        return {"success": True, "message": f"Deployment {pipeline_id} approved"}
    
    def reject_deployment(self, pipeline_id, reason):
        """Reject a deployment (demo)"""
        return {"success": True, "message": f"Deployment {pipeline_id} rejected: {reason}"}
    
    def trigger_pipeline(self, pipeline_name, environment, deployment_name, parameters):
        """Trigger a pipeline deployment (demo)"""
        return {"success": True, "pipeline_id": f"CB-{datetime.now().strftime('%Y%m%d%H%M')}"}

# ============================================================================
# MAIN MODULE
# ============================================================================

class GCPProvisioningModule:
    """GCP Infrastructure Provisioning & Deployment"""
    
    @staticmethod
    @require_permission('provision_resources')

    def render():
        """Main render function"""
        
        st.title("🚀 Provisioning & Deployment")
        st.caption("Infrastructure deployment with Cloud Build/Deployment Manager/Terraform integration")
        
        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()
        
        # Initialize managers
        cicd_mgr = CICDIntegrationManager()
        
        st.info("💡 **Demo Mode:** Showing sample deployment data. Configure Cloud Build integration to see real pipeline data.")
        
        # 9 tabs matching AWS
        tabs = st.tabs([
            "📊 CI/CD Deployments",
            "⏸️ Pending Approvals",
            "🎯 Trigger Pipeline",
            "📚 Template Library",
            "🚀 Deploy Template",
            "🔄 Active Deployments",
            "📝 Preview Changes",
            "🌍 Multi-Region",
            "⏮️ Rollback"
        ])
        
        with tabs[0]:
            GCPProvisioningModule._render_cicd_deployments(cicd_mgr)
        with tabs[1]:
            GCPProvisioningModule._render_pending_approvals(cicd_mgr)
        with tabs[2]:
            GCPProvisioningModule._render_trigger_pipeline(cicd_mgr)
        with tabs[3]:
            GCPProvisioningModule._render_template_library()
        with tabs[4]:
            GCPProvisioningModule._render_deploy_template()
        with tabs[5]:
            GCPProvisioningModule._render_active_deployments()
        with tabs[6]:
            GCPProvisioningModule._render_preview_changes()
        with tabs[7]:
            GCPProvisioningModule._render_multi_region()
        with tabs[8]:
            GCPProvisioningModule._render_rollback()
    
    @staticmethod
    def _render_cicd_deployments(cicd_mgr):
        """Tab 1: Monitor CI/CD pipeline deployments"""
        st.subheader("📊 CI/CD Pipeline Deployments")
        st.caption("Monitor automated deployments from Cloud Build pipelines")
        
        with st.expander("📖 How to Enable Real CI/CD Integration"):
            st.markdown("""
            ### Setup Instructions
            
            **For Cloud Build:**
            1. Add to `.streamlit/secrets.toml`:
               ```toml
               GCP_PROJECT_ID = "your-project-id"
               GCP_SERVICE_ACCOUNT_KEY = "base64_encoded_key"
               ```
            2. Enable Cloud Build API in your project
            
            **For GitHub Actions:**
            1. Add to `.streamlit/secrets.toml`:
               ```toml
               GITHUB_TOKEN = "ghp_your_token"
               GITHUB_ORG = "your-org"
               GITHUB_REPO = "infrastructure"
               ```
            
            **Benefits:**
            - Real-time pipeline status
            - Actual Git commit information
            - Live approval workflows
            - Complete audit trail
            """)
        
        # Get deployments
        deployments = cicd_mgr.get_recent_deployments(limit=20)
        
        if not deployments:
            st.info("No recent CI/CD deployments found")
            return
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Deployments", len(deployments))
        with col2:
            pending = sum(1 for d in deployments if d.status == "pending_approval")
            st.metric("Pending Approval", pending)
        with col3:
            running = sum(1 for d in deployments if d.status == "running")
            st.metric("Running", running)
        with col4:
            failed = sum(1 for d in deployments if d.status == "failed")
            st.metric("Failed", failed)
        
        st.markdown("---")
        
        # Display deployments
        for deployment in deployments:
            # Status icon
            status_icons = {
                "success": "✅",
                "failed": "❌",
                "running": "🔄",
                "pending_approval": "⏸️"
            }
            status_icon = status_icons.get(deployment.status, "⚪")
            
            # Environment badge
            env_colors = {"production": "🔴", "staging": "🟡", "dev": "🟢"}
            env_badge = env_colors.get(deployment.environment, "⚪")
            
            with st.expander(
                f"{status_icon} {env_badge} **{deployment.environment.upper()}** | "
                f"{deployment.deployment_name} | {deployment.status.upper()}",
                expanded=deployment.approval_required
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Pipeline:** {deployment.pipeline_name}")
                    st.markdown(f"**Pipeline ID:** {deployment.pipeline_id}")
                    st.markdown(f"**Deployment:** {deployment.deployment_name}")
                    st.markdown(f"**Environment:** {deployment.environment}")
                
                with col2:
                    st.markdown(f"**Commit:** `{deployment.commit_hash}`")
                    st.markdown(f"**Message:** {deployment.commit_message}")
                    st.markdown(f"**Author:** {deployment.author}")
                    st.markdown(f"**Triggered:** {deployment.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if deployment.completed_at:
                        duration = (deployment.completed_at - deployment.triggered_at).total_seconds() / 60
                        st.markdown(f"**Duration:** {duration:.1f} minutes")
                
                # Approval UI
                if deployment.approval_required and deployment.status == "pending_approval":
                    st.markdown("---")
                    st.warning("⏸️ **This deployment requires approval!**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Approve", key=f"approve_{deployment.pipeline_id}", type="primary"):
                            result = cicd_mgr.approve_deployment(deployment.pipeline_id)
                            if result.get("success"):
                                st.success("Deployment approved!")
                                st.balloons()
                    
                    with col2:
                        if st.button("❌ Reject", key=f"reject_{deployment.pipeline_id}"):
                            st.session_state[f"show_reject_{deployment.pipeline_id}"] = True
                    
                    if st.session_state.get(f"show_reject_{deployment.pipeline_id}"):
                        reason = st.text_area(
                            "Rejection Reason",
                            key=f"reason_{deployment.pipeline_id}",
                            placeholder="Explain why this deployment is being rejected..."
                        )
                        if st.button("Confirm Rejection", key=f"confirm_{deployment.pipeline_id}"):
                            if reason.strip():
                                cicd_mgr.reject_deployment(deployment.pipeline_id, reason)
                                st.error(f"Deployment rejected: {reason}")
    
    @staticmethod
    def _render_pending_approvals(cicd_mgr):
        """Tab 2: Show deployments pending approval"""
        st.subheader("⏸️ Pending Approvals")
        st.caption("Review and approve production deployments")
        
        deployments = cicd_mgr.get_recent_deployments(limit=20)
        pending = [d for d in deployments if d.status == "pending_approval"]
        
        if not pending:
            st.success("✅ No deployments pending approval")
            return
        
        st.warning(f"⚠️ **{len(pending)} deployment(s) require your approval**")
        
        for deployment in pending:
            with st.container():
                st.markdown(f"### 🔴 {deployment.environment.upper()} | {deployment.deployment_name}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Commit:** `{deployment.commit_hash}`")
                    st.markdown(f"**Message:** {deployment.commit_message}")
                    st.markdown(f"**Author:** {deployment.author}")
                
                with col2:
                    st.markdown(f"**Pipeline:** {deployment.pipeline_name}")
                    st.markdown(f"**Triggered:** {deployment.triggered_at.strftime('%Y-%m-%d %H:%M')}")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col2:
                    if st.button("✅ Approve", key=f"app2_{deployment.pipeline_id}", type="primary", use_container_width=True):
                        cicd_mgr.approve_deployment(deployment.pipeline_id)
                        st.success("Approved!")
                        st.balloons()
                
                with col3:
                    if st.button("❌ Reject", key=f"rej2_{deployment.pipeline_id}", use_container_width=True):
                        st.error("Rejected")
                
                st.markdown("---")
    
    @staticmethod
    def _render_trigger_pipeline(cicd_mgr):
        """Tab 3: Trigger new pipeline deployment"""
        st.subheader("🎯 Trigger Pipeline Deployment")
        st.caption("Manually trigger infrastructure deployment pipeline")
        
        with st.form("trigger_pipeline_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                pipeline_name = st.selectbox("Pipeline", [
                    "Deploy Infrastructure",
                    "Deploy Network",
                    "Deploy Compute",
                    "Deploy Database"
                ])
                
                environment = st.selectbox("Environment", [
                    "dev",
                    "staging",
                    "production"
                ])
            
            with col2:
                deployment_name = st.text_input("Deployment Name", placeholder="e.g., vpc-deployment")
                
                branch = st.selectbox("Branch", ["main", "develop", "release"])
            
            st.markdown("### Parameters (YAML)")
            parameters = st.text_area(
                "Deployment Parameters",
                height=150,
                value="""project: my-project-id
region: us-central1
network:
  name: vpc-prod
  cidr: 10.0.0.0/16""",
                placeholder='key: value'
            )
            
            require_approval = st.checkbox("Require approval before deployment", value=True)
            
            submitted = st.form_submit_button("🚀 Trigger Pipeline", type="primary", use_container_width=True)
            
            if submitted:
                result = cicd_mgr.trigger_pipeline(pipeline_name, environment, deployment_name, {})
                
                if result.get("success"):
                    st.success(f"✅ Pipeline triggered successfully!")
                    st.info(f"Pipeline ID: {result['pipeline_id']}")
                    if require_approval:
                        st.warning("⏸️ Deployment will wait for approval")
    
    @staticmethod
    def _render_template_library():
        """Tab 4: Deployment Manager / Terraform library"""
        st.subheader("📚 Deployment Template Library")
        st.caption("Pre-built infrastructure templates")
        
        # Filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox("Category", ["All", "Network", "Compute", "Database", "Storage", "Security"])
        with col2:
            template_type = st.selectbox("Type", ["All", "Deployment Manager", "Terraform"])
        with col3:
            complexity = st.selectbox("Complexity", ["All", "Simple", "Moderate", "Complex"])
        
        st.markdown("---")
        
        # Templates
        templates = [
            {
                "Name": "Production VPC",
                "Description": "VPC with 3 subnets (app, data, gateway)",
                "Type": "Deployment Manager",
                "Category": "Network",
                "Resources": "VPC, Subnets, Firewall Rules, Cloud Router",
                "Complexity": "Moderate"
            },
            {
                "Name": "Cloud Run + SQL",
                "Description": "Serverless app with Cloud SQL database",
                "Type": "Terraform",
                "Category": "Compute",
                "Resources": "Cloud Run, Cloud SQL, VPC Connector",
                "Complexity": "Moderate"
            },
            {
                "Name": "GKE Cluster",
                "Description": "Kubernetes cluster with node pools",
                "Type": "Terraform",
                "Category": "Compute",
                "Resources": "GKE, Node Pools, Workload Identity, VPC",
                "Complexity": "Complex"
            },
            {
                "Name": "Cloud Storage",
                "Description": "Storage bucket with lifecycle policies",
                "Type": "Deployment Manager",
                "Category": "Storage",
                "Resources": "Storage Bucket, Lifecycle Policy, IAM",
                "Complexity": "Simple"
            }
        ]
        
        for template in templates:
            with st.expander(f"📄 {template['Name']} ({template['Type']})"):
                st.write(f"**Description:** {template['Description']}")
                st.write(f"**Category:** {template['Category']} | **Complexity:** {template['Complexity']}")
                st.write(f"**Resources:** {template['Resources']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"👁️ View", key=f"view_{template['Name']}")
                with col2:
                    st.button(f"📥 Download", key=f"download_{template['Name']}")
                with col3:
                    st.button(f"🚀 Deploy", key=f"deploy_{template['Name']}", type="primary")
    
    @staticmethod
    def _render_deploy_template():
        """Tab 5: Deploy template"""
        st.subheader("🚀 Deploy Infrastructure Template")
        st.caption("Deploy infrastructure using Deployment Manager or Terraform")
        
        with st.form("deploy_template_form"):
            st.markdown("### Deployment Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                deployment_name = st.text_input("Deployment Name*", placeholder="e.g., prod-vpc-deployment")
                
                project = st.selectbox("GCP Project", [
                    "prod-project-001",
                    "dev-project-001",
                    "staging-project-001"
                ])
                
                region = st.selectbox("Region", [
                    "us-central1", "us-east1", "us-west1",
                    "europe-west1", "asia-east1"
                ])
            
            with col2:
                template_source = st.radio("Template Source", [
                    "Template Library",
                    "Upload File",
                    "Git Repository"
                ])
                
                if template_source == "Template Library":
                    template = st.selectbox("Select Template", [
                        "Production VPC",
                        "Cloud Run + SQL",
                        "GKE Cluster"
                    ])
                elif template_source == "Upload File":
                    uploaded_file = st.file_uploader("Upload Template", type=["yaml", "jinja", "tf"])
                else:
                    repo_url = st.text_input("Repository URL")
                    template_path = st.text_input("Template Path", placeholder="templates/main.yaml")
            
            st.markdown("### Configuration")
            
            config = st.text_area(
                "Deployment Configuration (YAML)",
                height=200,
                value="""project: my-project-id
region: us-central1
resources:
  - name: vpc-prod
    type: compute.v1.network
    properties:
      autoCreateSubnetworks: false
  - name: subnet-app
    type: compute.v1.subnetwork
    properties:
      ipCidrRange: 10.0.1.0/24
      network: $(ref.vpc-prod.selfLink)"""
            )
            
            st.markdown("### Deployment Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                preview_only = st.checkbox("Preview only (don't deploy)")
                create_policy = st.checkbox("Create with default policy")
            
            with col2:
                enable_monitoring = st.checkbox("Enable deployment monitoring", value=True)
                auto_approve = st.checkbox("Auto-approve (skip manual approval)")
            
            submitted = st.form_submit_button("🚀 Deploy Template", type="primary", use_container_width=True)
            
            if submitted:
                if not deployment_name or not project:
                    st.error("❌ Please fill in required fields")
                else:
                    with st.spinner("Deploying template..."):
                        st.success(f"✅ Deployment '{deployment_name}' started successfully!")
                        st.info("📊 View progress in the 'Active Deployments' tab")
    
    @staticmethod
    def _render_active_deployments():
        """Tab 6: Monitor active deployments"""
        st.subheader("🔄 Active Deployments")
        st.caption("Monitor ongoing infrastructure deployments")
        
        # Sample active deployments
        deployments = [
            {
                "Name": "prod-vpc-deployment",
                "Status": "🔄 Running",
                "Progress": 65,
                "Project": "prod-project-001",
                "Started": "2025-12-07 14:30",
                "Duration": "3m 15s",
                "Resources": "Creating Subnet (2/3)"
            },
            {
                "Name": "staging-app-deployment",
                "Status": "✅ Succeeded",
                "Progress": 100,
                "Project": "staging-project-001",
                "Started": "2025-12-07 14:15",
                "Duration": "8m 42s",
                "Resources": "Completed (5/5)"
            },
            {
                "Name": "dev-sql-deployment",
                "Status": "⏸️ Waiting",
                "Progress": 0,
                "Project": "dev-project-001",
                "Started": "2025-12-07 14:45",
                "Duration": "0m 30s",
                "Resources": "Waiting for approval"
            }
        ]
        
        for dep in deployments:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {dep['Name']}")
                    st.progress(dep['Progress'] / 100)
                    st.caption(f"{dep['Resources']}")
                
                with col2:
                    st.metric("Status", dep['Status'])
                    st.caption(f"Duration: {dep['Duration']}")
                
                with col3:
                    st.button("👁️ Details", key=f"details_{dep['Name']}")
                    if dep['Status'] == "🔄 Running":
                        st.button("⏸️ Cancel", key=f"cancel_{dep['Name']}")
                
                st.markdown("---")
    
    @staticmethod
    def _render_preview_changes():
        """Tab 7: Preview changes"""
        st.subheader("📝 Preview Deployment Changes")
        st.caption("Preview changes before deploying")
        
        st.info("💡 Preview shows you what changes will be made without actually deploying")
        
        with st.form("preview_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project = st.text_input("GCP Project", placeholder="prod-project-001")
                template = st.selectbox("Template", [
                    "Production VPC",
                    "Cloud Run + SQL",
                    "GKE Cluster"
                ])
            
            with col2:
                deployment_name = st.text_input("Deployment Name", placeholder="vpc-deployment")
            
            config = st.text_area(
                "Configuration (YAML)",
                height=150,
                value='network:\n  name: vpc-prod\n  cidr: 10.0.0.0/16'
            )
            
            submitted = st.form_submit_button("🔍 Preview Changes", type="primary", use_container_width=True)
            
            if submitted:
                with st.spinner("Generating preview..."):
                    st.markdown("### 📋 Predicted Changes")
                    
                    st.success("**✅ Resources to be created (3)**")
                    st.write("• Network: vpc-prod")
                    st.write("• Subnetwork: subnet-app (us-central1)")
                    st.write("• Firewall Rule: allow-internal")
                    
                    st.info("**🔄 Resources to be modified (1)**")
                    st.write("• Route: default-route (next hop will be updated)")
                    
                    st.error("**⚠️ Resources to be deleted (0)**")
                    
                    st.markdown("---")
                    
                    if st.button("✅ Proceed with Deployment", type="primary"):
                        st.success("Deployment initiated!")
    
    @staticmethod
    def _render_multi_region():
        """Tab 8: Multi-region deployment"""
        st.subheader("🌍 Multi-Region Deployment")
        st.caption("Deploy infrastructure across multiple GCP regions")
        
        with st.form("multi_region_form"):
            st.markdown("### Deployment Configuration")
            
            deployment_name = st.text_input("Deployment Name", placeholder="global-infrastructure")
            template = st.selectbox("Template", [
                "Global VPC",
                "Multi-Region Cloud Run",
                "Geo-Replicated Storage"
            ])
            
            st.markdown("### Select Regions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Primary Region**")
                primary_region = st.selectbox("Primary", ["us-central1", "europe-west1", "asia-east1"])
                primary_project = st.text_input("Primary Project", placeholder="prod-project-001")
            
            with col2:
                st.markdown("**Secondary Regions**")
                secondary_regions = st.multiselect("Secondary", [
                    "us-east1", "us-west1", "europe-west2", "asia-northeast1"
                ])
            
            st.markdown("### Deployment Strategy")
            
            strategy = st.radio("Strategy", [
                "Sequential (one region at a time)",
                "Parallel (all regions simultaneously)",
                "Blue-Green (deploy to secondary, then swap)"
            ])
            
            enable_monitoring = st.checkbox("Enable cross-region monitoring", value=True)
            
            submitted = st.form_submit_button("🚀 Deploy Multi-Region", type="primary", use_container_width=True)
            
            if submitted:
                st.success(f"✅ Multi-region deployment '{deployment_name}' initiated!")
                st.info(f"Deploying to {len(secondary_regions) + 1} regions...")
                
                for region in [primary_region] + secondary_regions:
                    st.write(f"• {region}: Queued")
    
    @staticmethod
    def _render_rollback():
        """Tab 9: Rollback deployments"""
        st.subheader("⏮️ Rollback Deployment")
        st.caption("Rollback failed or problematic deployments")
        
        st.warning("⚠️ Rolling back a deployment will delete resources created by that deployment")
        
        # Recent deployments
        st.markdown("### Recent Deployments")
        
        deployments = [
            {"Name": "prod-vpc-deployment", "Status": "✅ Succeeded", "Time": "2 hours ago", "Can Rollback": True},
            {"Name": "staging-app-deployment", "Status": "❌ Failed", "Time": "1 hour ago", "Can Rollback": True},
            {"Name": "dev-sql-deployment", "Status": "✅ Succeeded", "Time": "30 minutes ago", "Can Rollback": True},
        ]
        
        for dep in deployments:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{dep['Name']}**")
                    st.caption(f"{dep['Time']}")
                
                with col2:
                    st.markdown(dep['Status'])
                
                with col3:
                    if dep['Can Rollback']:
                        if st.button("⏮️ Rollback", key=f"rollback_{dep['Name']}"):
                            st.session_state[f"confirm_rollback_{dep['Name']}"] = True
                
                if st.session_state.get(f"confirm_rollback_{dep['Name']}"):
                    st.error(f"⚠️ Confirm rollback of '{dep['Name']}'?")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Yes, Rollback", key=f"yes_{dep['Name']}", type="primary"):
                            st.success(f"✅ Rollback initiated for {dep['Name']}")
                            del st.session_state[f"confirm_rollback_{dep['Name']}"]
                    
                    with col2:
                        if st.button("❌ Cancel", key=f"no_{dep['Name']}"):
                            del st.session_state[f"confirm_rollback_{dep['Name']}"]
                
                st.markdown("---")

# Module-level render function
def render():
    """Module-level render function"""
    GCPProvisioningModule.render()
