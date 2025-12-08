"""
Unified CI/CD Module for Azure - All 5 Phases Combined
Complete CI/CD Platform with Pipeline Building, Triggering, Approvals, Multi-Subscription, and AI Analytics
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from auth_azure_sso import require_permission

class AzureUnifiedCICDModule:
    """Unified Azure CI/CD Module with all 5 phases"""
    
    @staticmethod
    @require_permission('deploy_applications')

    def render():
        """Main render method"""
        
        # Custom CSS for better visibility
        st.markdown("""
        <style>
        .template-card {
            background: linear-gradient(135deg, #0078d4 0%, #0053a6 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s;
            margin-bottom: 10px;
            color: white !important;
            font-weight: bold;
        }
        .template-card:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.title("🔄 Azure CI/CD Pipeline Management")
        st.markdown("**Complete CI/CD Platform** - Build, Trigger, Approve, Deploy Multi-Subscription, and AI-Powered Analytics")
        
        # Info about Azure DevOps integration
        st.info("💡 **Azure DevOps Integration:** This module integrates with Azure DevOps, GitHub Actions, and Azure Pipelines")
        
        # Subscription selector
        subscriptions = [
            "prod-subscription-001",
            "dev-subscription-001",
            "staging-subscription-001"
        ]
        
        selected_subscription = st.selectbox(
            "Select Azure Subscription",
            options=subscriptions,
            key="azure_cicd_subscription_selector"
        )
        
        if not selected_subscription:
            st.info("Please select a subscription")
            return
        
        # Main phase tabs - ALL 5 PHASES
        phase_tabs = st.tabs([
            "🗃️ Pipeline Builder",
            "⚡ Triggering & Parameters",
            "⏸️ Approvals & Notifications",
            "🌐 Multi-Subscription",
            "🤖 AI Analytics"
        ])
        
        # Phase 1: Pipeline Builder
        with phase_tabs[0]:
            AzureUnifiedCICDModule._render_pipeline_builder(selected_subscription)
        
        # Phase 2: Triggering & Parameters
        with phase_tabs[1]:
            AzureUnifiedCICDModule._render_triggering(selected_subscription)
        
        # Phase 3: Approvals & Notifications
        with phase_tabs[2]:
            AzureUnifiedCICDModule._render_approvals(selected_subscription)
        
        # Phase 4: Multi-Subscription Management
        with phase_tabs[3]:
            AzureUnifiedCICDModule._render_multi_subscription(selected_subscription)
        
        # Phase 5: AI Analytics
        with phase_tabs[4]:
            AzureUnifiedCICDModule._render_ai_analytics(selected_subscription)
    
    # ========================================================================
    # PHASE 1: PIPELINE BUILDER
    # ========================================================================
    
    @staticmethod
    def _render_pipeline_builder(subscription):
        """Phase 1: Create and manage Azure Pipelines"""
        
        st.subheader("🗃️ Pipeline Builder & Orchestration")
        st.caption("Create and manage Azure DevOps pipelines entirely within CloudIDP")
        
        # Sub-tabs for pipeline builder
        builder_tabs = st.tabs([
            "📋 Pipeline Templates",
            "🆕 Create Pipeline",
            "📊 Existing Pipelines",
            "⚙️ Pipeline Settings"
        ])
        
        with builder_tabs[0]:
            AzureUnifiedCICDModule._render_pipeline_templates()
        
        with builder_tabs[1]:
            AzureUnifiedCICDModule._render_create_pipeline(subscription)
        
        with builder_tabs[2]:
            AzureUnifiedCICDModule._render_existing_pipelines(subscription)
        
        with builder_tabs[3]:
            AzureUnifiedCICDModule._render_pipeline_settings(subscription)
    
    @staticmethod
    def _render_pipeline_templates():
        """Show pipeline templates"""
        
        st.markdown("### 📚 Pipeline Templates")
        st.markdown("Choose from pre-built pipeline templates or create custom pipelines")
        
        templates = [
            {
                "name": "Azure App Service Deployment",
                "description": "Deploy web apps to Azure App Service with staging slots",
                "icon": "🌐",
                "stages": ["Build", "Test", "Deploy to Staging", "Approval", "Deploy to Production"],
                "estimated_time": "15-20 minutes"
            },
            {
                "name": "AKS Deployment",
                "description": "Build and deploy containerized apps to Azure Kubernetes Service",
                "icon": "🐳",
                "stages": ["Build Image", "Push to ACR", "Deploy to AKS", "Health Check"],
                "estimated_time": "20-25 minutes"
            },
            {
                "name": "Infrastructure as Code (Bicep/ARM)",
                "description": "Deploy Azure infrastructure using Bicep or ARM templates",
                "icon": "🏗️",
                "stages": ["Validate", "What-If", "Approval", "Deploy"],
                "estimated_time": "10-15 minutes"
            },
            {
                "name": "Azure Functions Deployment",
                "description": "Deploy serverless functions with automated testing",
                "icon": "⚡",
                "stages": ["Build", "Unit Tests", "Integration Tests", "Deploy"],
                "estimated_time": "10-12 minutes"
            }
        ]
        
        col1, col2 = st.columns(2)
        
        for idx, template in enumerate(templates):
            with (col1 if idx % 2 == 0 else col2):
                with st.container():
                    st.markdown(f"""
                    <div class="template-card">
                        <h3>{template['icon']} {template['name']}</h3>
                        <p>{template['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📋 Template Details"):
                        st.write(f"**Stages:** {', '.join(template['stages'])}")
                        st.write(f"**Estimated Time:** {template['estimated_time']}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("👁️ Preview", key=f"preview_{idx}"):
                                st.info(f"Previewing {template['name']} YAML...")
                        with col_b:
                            if st.button("✅ Use Template", key=f"use_{idx}", type="primary"):
                                st.success(f"✅ Template '{template['name']}' selected!")
    
    @staticmethod
    def _render_create_pipeline(subscription):
        """Create new pipeline"""
        
        st.markdown("### 🆕 Create New Pipeline")
        
        with st.form("create_azure_pipeline_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                pipeline_name = st.text_input("Pipeline Name*", placeholder="e.g., prod-app-deployment")
                pipeline_type = st.selectbox("Pipeline Type", [
                    "Azure DevOps YAML",
                    "Classic Pipeline",
                    "GitHub Actions",
                    "Multi-Stage Pipeline"
                ])
                repository = st.text_input("Repository URL", placeholder="https://github.com/org/repo")
            
            with col2:
                branch = st.selectbox("Default Branch", ["main", "develop", "master"])
                build_agent = st.selectbox("Build Agent", [
                    "ubuntu-latest",
                    "windows-latest",
                    "macOS-latest",
                    "Self-hosted"
                ])
                enable_ci = st.checkbox("Enable Continuous Integration", value=True)
            
            st.markdown("### Pipeline Stages")
            
            stages = st.multiselect(
                "Select Stages",
                ["Build", "Test", "Code Analysis", "Security Scan", "Deploy to Dev", 
                 "Deploy to Staging", "Manual Approval", "Deploy to Production", "Post-Deployment Tests"],
                default=["Build", "Test", "Deploy to Staging", "Manual Approval", "Deploy to Production"]
            )
            
            st.markdown("### Triggers")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trigger_on_commit = st.checkbox("Trigger on commit/push", value=True)
                trigger_on_pr = st.checkbox("Trigger on pull request")
            
            with col2:
                scheduled_trigger = st.checkbox("Scheduled trigger")
                if scheduled_trigger:
                    schedule = st.text_input("Cron Schedule", placeholder="0 2 * * *")
            
            st.markdown("### Notifications")
            
            notification_channels = st.multiselect(
                "Notification Channels",
                ["Email", "Microsoft Teams", "Slack", "Azure DevOps", "ServiceNow"]
            )
            
            submitted = st.form_submit_button("🚀 Create Pipeline", type="primary", use_container_width=True)
            
            if submitted:
                if pipeline_name:
                    st.success(f"✅ Pipeline '{pipeline_name}' created successfully!")
                    st.info("📊 Pipeline is now available in 'Existing Pipelines' tab")
                    st.code(f"""
# Generated Azure Pipeline YAML
trigger:
  branches:
    include:
      - {branch}

pool:
  vmImage: '{build_agent}'

stages:
{chr(10).join([f'- stage: {stage.replace(" ", "")}' for stage in stages])}
""", language="yaml")
                else:
                    st.error("❌ Please provide a pipeline name")
    
    @staticmethod
    def _render_existing_pipelines(subscription):
        """Show existing pipelines"""
        
        st.markdown("### 📊 Existing Pipelines")
        
        # Sample pipelines
        pipelines = [
            {"Name": "prod-app-deployment", "Status": "✅ Success", "Last Run": "2 hours ago", "Success Rate": "95%", "Runs": "234"},
            {"Name": "staging-api-deploy", "Status": "🔄 Running", "Last Run": "5 minutes ago", "Success Rate": "88%", "Runs": "156"},
            {"Name": "dev-infrastructure", "Status": "✅ Success", "Last Run": "1 day ago", "Success Rate": "92%", "Runs": "89"},
            {"Name": "prod-database-migration", "Status": "⏸️ Paused", "Last Run": "3 days ago", "Success Rate": "78%", "Runs": "45"},
        ]
        
        df = pd.DataFrame(pipelines)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Pipeline details
        selected_pipeline = st.selectbox("Select Pipeline for Details", [p["Name"] for p in pipelines])
        
        if selected_pipeline:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("▶️ Run Pipeline", use_container_width=True):
                    st.success(f"▶️ Pipeline '{selected_pipeline}' triggered!")
            
            with col2:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.info(f"⏸️ Pipeline '{selected_pipeline}' paused")
            
            with col3:
                if st.button("✏️ Edit", use_container_width=True):
                    st.info("Opening pipeline editor...")
            
            with col4:
                if st.button("🗑️ Delete", use_container_width=True):
                    st.warning(f"⚠️ Confirm deletion of '{selected_pipeline}'?")
    
    @staticmethod
    def _render_pipeline_settings(subscription):
        """Pipeline settings"""
        
        st.markdown("### ⚙️ Pipeline Settings & Configuration")
        
        with st.form("pipeline_settings_form"):
            st.markdown("#### General Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                retention_days = st.number_input("Pipeline Run Retention (days)", 1, 365, 90)
                max_concurrent = st.number_input("Max Concurrent Runs", 1, 10, 5)
            
            with col2:
                timeout_minutes = st.number_input("Pipeline Timeout (minutes)", 10, 480, 60)
                enable_diagnostics = st.checkbox("Enable Diagnostic Logging", value=True)
            
            st.markdown("#### Service Connections")
            
            service_connections = st.multiselect(
                "Service Connections",
                ["Azure Resource Manager", "Azure Container Registry", "GitHub", "Docker Registry", "Kubernetes"]
            )
            
            st.markdown("#### Security")
            
            col1, col2 = st.columns(2)
            
            with col1:
                require_approval = st.checkbox("Require approval for production", value=True)
                enable_secrets = st.checkbox("Enable secret variables", value=True)
            
            with col2:
                scan_code = st.checkbox("Enable security scanning", value=True)
                audit_logs = st.checkbox("Enable audit logging", value=True)
            
            submitted = st.form_submit_button("💾 Save Settings", type="primary", use_container_width=True)
            
            if submitted:
                st.success("✅ Pipeline settings saved successfully!")
    
    # ========================================================================
    # PHASE 2: TRIGGERING & PARAMETERS
    # ========================================================================
    
    @staticmethod
    def _render_triggering(subscription):
        """Phase 2: Advanced pipeline triggering"""
        
        st.subheader("⚡ Pipeline Triggering & Parameters")
        st.caption("Advanced pipeline triggering with dynamic parameters and conditions")
        
        triggering_tabs = st.tabs([
            "🎯 Manual Trigger",
            "⏰ Scheduled Triggers",
            "🔗 Webhook Triggers",
            "📊 Trigger History"
        ])
        
        with triggering_tabs[0]:
            AzureUnifiedCICDModule._render_manual_trigger()
        
        with triggering_tabs[1]:
            AzureUnifiedCICDModule._render_scheduled_triggers()
        
        with triggering_tabs[2]:
            AzureUnifiedCICDModule._render_webhook_triggers()
        
        with triggering_tabs[3]:
            AzureUnifiedCICDModule._render_trigger_history()
    
    @staticmethod
    def _render_manual_trigger():
        """Manual pipeline triggering"""
        
        st.markdown("### 🎯 Manual Pipeline Trigger")
        
        with st.form("manual_trigger_form"):
            pipeline = st.selectbox("Select Pipeline", [
                "prod-app-deployment",
                "staging-api-deploy",
                "dev-infrastructure"
            ])
            
            branch = st.selectbox("Branch", ["main", "develop", "feature/new-ui"])
            
            st.markdown("#### Pipeline Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                environment = st.selectbox("Target Environment", ["dev", "staging", "production"])
                deploy_region = st.multiselect("Deploy to Regions", [
                    "East US", "West US", "West Europe", "Southeast Asia"
                ])
            
            with col2:
                enable_tests = st.checkbox("Run tests", value=True)
                enable_rollback = st.checkbox("Enable auto-rollback", value=True)
            
            custom_params = st.text_area(
                "Custom Parameters (JSON)",
                value='{\n  "version": "1.0.0",\n  "feature_flags": ["new-ui", "api-v2"]\n}',
                height=150
            )
            
            submitted = st.form_submit_button("🚀 Trigger Pipeline", type="primary", use_container_width=True)
            
            if submitted:
                st.success(f"✅ Pipeline '{pipeline}' triggered successfully!")
                st.info(f"Pipeline ID: AzDO-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    @staticmethod
    def _render_scheduled_triggers():
        """Scheduled triggers"""
        
        st.markdown("### ⏰ Scheduled Triggers")
        
        schedules = [
            {"Name": "Nightly Build", "Schedule": "0 2 * * *", "Pipeline": "prod-app-deployment", "Status": "✅ Active"},
            {"Name": "Weekly Deploy", "Schedule": "0 0 * * 0", "Pipeline": "staging-api-deploy", "Status": "✅ Active"},
            {"Name": "Monthly Backup", "Schedule": "0 0 1 * *", "Pipeline": "dev-infrastructure", "Status": "⏸️ Paused"},
        ]
        
        df = pd.DataFrame(schedules)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        with st.expander("➕ Add New Schedule"):
            with st.form("add_schedule_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    schedule_name = st.text_input("Schedule Name", placeholder="e.g., Daily Deploy")
                    pipeline = st.selectbox("Pipeline", ["prod-app-deployment", "staging-api-deploy"])
                
                with col2:
                    cron_schedule = st.text_input("Cron Schedule", placeholder="0 2 * * *")
                    timezone = st.selectbox("Timezone", ["UTC", "PST", "EST", "CET"])
                
                submitted = st.form_submit_button("✅ Create Schedule", type="primary")
                
                if submitted:
                    st.success(f"✅ Schedule '{schedule_name}' created!")
    
    @staticmethod
    def _render_webhook_triggers():
        """Webhook triggers"""
        
        st.markdown("### 🔗 Webhook Triggers")
        
        st.info("💡 Configure webhooks to trigger pipelines from external systems")
        
        webhooks = [
            {"Name": "GitHub Push", "URL": "https://dev.azure.com/webhook/123", "Pipeline": "prod-app-deployment", "Events": "push, PR"},
            {"Name": "Docker Hub", "URL": "https://dev.azure.com/webhook/456", "Pipeline": "staging-api-deploy", "Events": "image push"},
        ]
        
        df = pd.DataFrame(webhooks)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        with st.expander("➕ Create New Webhook"):
            with st.form("create_webhook_form"):
                webhook_name = st.text_input("Webhook Name", placeholder="e.g., GitHub Integration")
                pipeline = st.selectbox("Target Pipeline", ["prod-app-deployment", "staging-api-deploy"])
                
                events = st.multiselect("Trigger Events", [
                    "push",
                    "pull_request",
                    "release",
                    "tag",
                    "issue_comment"
                ])
                
                secret = st.text_input("Webhook Secret", type="password", placeholder="Enter secret key")
                
                submitted = st.form_submit_button("🔗 Create Webhook", type="primary")
                
                if submitted:
                    webhook_url = f"https://dev.azure.com/webhook/{datetime.now().timestamp()}"
                    st.success(f"✅ Webhook created!")
                    st.code(f"Webhook URL: {webhook_url}", language="text")
    
    @staticmethod
    def _render_trigger_history():
        """Trigger history"""
        
        st.markdown("### 📊 Trigger History")
        
        history = [
            {"Time": "2 hours ago", "Pipeline": "prod-app-deployment", "Trigger": "Manual", "User": "john.doe@company.com", "Status": "✅ Success"},
            {"Time": "5 hours ago", "Pipeline": "staging-api-deploy", "Trigger": "Webhook (GitHub)", "User": "webhook", "Status": "✅ Success"},
            {"Time": "1 day ago", "Pipeline": "prod-app-deployment", "Trigger": "Scheduled", "User": "system", "Status": "✅ Success"},
            {"Time": "2 days ago", "Pipeline": "dev-infrastructure", "Trigger": "Manual", "User": "jane.smith@company.com", "Status": "❌ Failed"},
        ]
        
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # PHASE 3: APPROVALS & NOTIFICATIONS
    # ========================================================================
    
    @staticmethod
    def _render_approvals(subscription):
        """Phase 3: Approval workflows and notifications"""
        
        st.subheader("⏸️ Approvals & Notifications")
        st.caption("Manage deployment approvals and notification channels")
        
        approval_tabs = st.tabs([
            "✅ Pending Approvals",
            "📋 Approval Rules",
            "🔔 Notifications",
            "📊 Approval History"
        ])
        
        with approval_tabs[0]:
            AzureUnifiedCICDModule._render_pending_approvals()
        
        with approval_tabs[1]:
            AzureUnifiedCICDModule._render_approval_rules()
        
        with approval_tabs[2]:
            AzureUnifiedCICDModule._render_notifications()
        
        with approval_tabs[3]:
            AzureUnifiedCICDModule._render_approval_history()
    
    @staticmethod
    def _render_pending_approvals():
        """Pending approvals"""
        
        st.markdown("### ✅ Pending Approvals")
        
        approvals = [
            {
                "Pipeline": "prod-app-deployment",
                "Environment": "Production",
                "Requested By": "john.doe@company.com",
                "Requested At": "30 minutes ago",
                "Changes": "Deploy v2.0.0 to production"
            },
            {
                "Pipeline": "prod-database-migration",
                "Environment": "Production",
                "Requested By": "jane.smith@company.com",
                "Requested At": "2 hours ago",
                "Changes": "Run schema migration v5.2"
            }
        ]
        
        for approval in approvals:
            with st.container():
                st.markdown(f"### 🔴 {approval['Environment'].upper()} | {approval['Pipeline']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Requested By:** {approval['Requested By']}")
                    st.write(f"**Requested At:** {approval['Requested At']}")
                
                with col2:
                    st.write(f"**Changes:** {approval['Changes']}")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col2:
                    if st.button("✅ Approve", key=f"approve_{approval['Pipeline']}", type="primary", use_container_width=True):
                        st.success("✅ Deployment approved!")
                        st.balloons()
                
                with col3:
                    if st.button("❌ Reject", key=f"reject_{approval['Pipeline']}", use_container_width=True):
                        st.error("❌ Deployment rejected")
                
                st.markdown("---")
        
        if not approvals:
            st.success("✅ No pending approvals")
    
    @staticmethod
    def _render_approval_rules():
        """Approval rules"""
        
        st.markdown("### 📋 Approval Rules")
        
        rules = [
            {"Environment": "Production", "Approvers": "2 required", "Timeout": "4 hours", "Auto-approve": "No"},
            {"Environment": "Staging", "Approvers": "1 required", "Timeout": "2 hours", "Auto-approve": "After 24h"},
            {"Environment": "Dev", "Approvers": "None", "Timeout": "N/A", "Auto-approve": "Yes"},
        ]
        
        df = pd.DataFrame(rules)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        with st.expander("➕ Add Approval Rule"):
            with st.form("add_approval_rule"):
                environment = st.selectbox("Environment", ["Production", "Staging", "Dev", "QA"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    required_approvers = st.number_input("Required Approvers", 0, 10, 2)
                    timeout_hours = st.number_input("Timeout (hours)", 1, 48, 4)
                
                with col2:
                    auto_approve = st.checkbox("Auto-approve after timeout")
                    notify_approvers = st.checkbox("Notify approvers", value=True)
                
                approvers = st.multiselect("Approvers", [
                    "john.doe@company.com",
                    "jane.smith@company.com",
                    "admin@company.com"
                ])
                
                submitted = st.form_submit_button("✅ Create Rule", type="primary")
                
                if submitted:
                    st.success(f"✅ Approval rule for {environment} created!")
    
    @staticmethod
    def _render_notifications():
        """Notification settings"""
        
        st.markdown("### 🔔 Notification Settings")
        
        with st.form("notification_settings"):
            st.markdown("#### Notification Channels")
            
            channels = st.multiselect(
                "Active Channels",
                ["Email", "Microsoft Teams", "Slack", "Azure DevOps", "SMS", "ServiceNow"],
                default=["Email", "Microsoft Teams"]
            )
            
            st.markdown("#### Notification Events")
            
            col1, col2 = st.columns(2)
            
            with col1:
                notify_success = st.checkbox("Pipeline success", value=True)
                notify_failure = st.checkbox("Pipeline failure", value=True)
                notify_approval = st.checkbox("Approval required", value=True)
            
            with col2:
                notify_start = st.checkbox("Pipeline started")
                notify_canceled = st.checkbox("Pipeline canceled")
                notify_scheduled = st.checkbox("Scheduled run")
            
            st.markdown("#### Recipients")
            
            recipients = st.text_area(
                "Email Recipients (one per line)",
                value="john.doe@company.com\njane.smith@company.com",
                height=100
            )
            
            submitted = st.form_submit_button("💾 Save Notification Settings", type="primary", use_container_width=True)
            
            if submitted:
                st.success("✅ Notification settings saved!")
    
    @staticmethod
    def _render_approval_history():
        """Approval history"""
        
        st.markdown("### 📊 Approval History")
        
        history = [
            {"Time": "2 hours ago", "Pipeline": "prod-app-deployment", "Approver": "john.doe@company.com", "Decision": "✅ Approved", "Comment": "LGTM"},
            {"Time": "1 day ago", "Pipeline": "prod-database-migration", "Approver": "jane.smith@company.com", "Decision": "❌ Rejected", "Comment": "Need more testing"},
            {"Time": "2 days ago", "Pipeline": "prod-app-deployment", "Approver": "admin@company.com", "Decision": "✅ Approved", "Comment": "Approved"},
        ]
        
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # PHASE 4: MULTI-SUBSCRIPTION MANAGEMENT
    # ========================================================================
    
    @staticmethod
    def _render_multi_subscription(subscription):
        """Phase 4: Multi-subscription deployment management"""
        
        st.subheader("🌐 Multi-Subscription Management")
        st.caption("Deploy and manage pipelines across multiple Azure subscriptions")
        
        multi_sub_tabs = st.tabs([
            "🗺️ Subscription Overview",
            "🚀 Cross-Subscription Deploy",
            "🔄 Subscription Groups",
            "📊 Deployment Status"
        ])
        
        with multi_sub_tabs[0]:
            AzureUnifiedCICDModule._render_subscription_overview()
        
        with multi_sub_tabs[1]:
            AzureUnifiedCICDModule._render_cross_subscription_deploy()
        
        with multi_sub_tabs[2]:
            AzureUnifiedCICDModule._render_subscription_groups()
        
        with multi_sub_tabs[3]:
            AzureUnifiedCICDModule._render_deployment_status()
    
    @staticmethod
    def _render_subscription_overview():
        """Subscription overview"""
        
        st.markdown("### 🗺️ Subscription Overview")
        
        subscriptions = [
            {"Subscription": "prod-subscription-001", "Environment": "Production", "Region": "East US", "Pipelines": "12", "Last Deploy": "2 hours ago"},
            {"Subscription": "staging-subscription-001", "Environment": "Staging", "Region": "West US", "Pipelines": "8", "Last Deploy": "1 day ago"},
            {"Subscription": "dev-subscription-001", "Environment": "Development", "Region": "West Europe", "Pipelines": "15", "Last Deploy": "30 minutes ago"},
        ]
        
        df = pd.DataFrame(subscriptions)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Subscriptions", "3")
        with col2:
            st.metric("Active Pipelines", "35")
        with col3:
            st.metric("Total Deployments (24h)", "47")
    
    @staticmethod
    def _render_cross_subscription_deploy():
        """Cross-subscription deployment"""
        
        st.markdown("### 🚀 Cross-Subscription Deployment")
        
        with st.form("cross_sub_deploy_form"):
            pipeline = st.selectbox("Select Pipeline", [
                "prod-app-deployment",
                "infrastructure-deployment",
                "database-migration"
            ])
            
            st.markdown("#### Target Subscriptions")
            
            target_subs = st.multiselect(
                "Deploy to Subscriptions",
                ["prod-subscription-001", "staging-subscription-001", "dev-subscription-001"],
                default=["staging-subscription-001"]
            )
            
            deployment_strategy = st.radio(
                "Deployment Strategy",
                ["Sequential (one at a time)", "Parallel (all at once)", "Canary (gradual rollout)"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                enable_rollback = st.checkbox("Enable auto-rollback", value=True)
                health_check = st.checkbox("Run health checks", value=True)
            
            with col2:
                notify_on_complete = st.checkbox("Notify on completion", value=True)
                require_approval = st.checkbox("Require approval per subscription")
            
            submitted = st.form_submit_button("🚀 Deploy to Multiple Subscriptions", type="primary", use_container_width=True)
            
            if submitted:
                st.success(f"✅ Deployment to {len(target_subs)} subscription(s) initiated!")
                for sub in target_subs:
                    st.info(f"📊 Deploying to {sub}...")
    
    @staticmethod
    def _render_subscription_groups():
        """Subscription groups"""
        
        st.markdown("### 🔄 Subscription Groups")
        
        st.info("💡 Group subscriptions for coordinated deployments")
        
        groups = [
            {"Group": "Production", "Subscriptions": "prod-subscription-001", "Deployments": "234"},
            {"Group": "Non-Production", "Subscriptions": "staging-subscription-001, dev-subscription-001", "Deployments": "567"},
            {"Group": "DR", "Subscriptions": "dr-subscription-001", "Deployments": "45"},
        ]
        
        df = pd.DataFrame(groups)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        with st.expander("➕ Create Subscription Group"):
            with st.form("create_sub_group"):
                group_name = st.text_input("Group Name", placeholder="e.g., Production")
                
                subscriptions = st.multiselect(
                    "Subscriptions",
                    ["prod-subscription-001", "staging-subscription-001", "dev-subscription-001"]
                )
                
                description = st.text_area("Description", placeholder="Optional group description")
                
                submitted = st.form_submit_button("✅ Create Group", type="primary")
                
                if submitted:
                    st.success(f"✅ Subscription group '{group_name}' created!")
    
    @staticmethod
    def _render_deployment_status():
        """Deployment status across subscriptions"""
        
        st.markdown("### 📊 Multi-Subscription Deployment Status")
        
        deployments = [
            {"Subscription": "prod-subscription-001", "Pipeline": "prod-app-deployment", "Status": "✅ Success", "Progress": "100%", "Time": "2 hours ago"},
            {"Subscription": "staging-subscription-001", "Pipeline": "prod-app-deployment", "Status": "🔄 Running", "Progress": "65%", "Time": "5 minutes ago"},
            {"Subscription": "dev-subscription-001", "Pipeline": "prod-app-deployment", "Status": "⏳ Queued", "Progress": "0%", "Time": "Pending"},
        ]
        
        for dep in deployments:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{dep['Subscription']}**")
                    st.progress(int(dep['Progress'].replace('%', '')) / 100 if dep['Progress'] != 'Pending' else 0)
                
                with col2:
                    st.metric("Status", dep['Status'])
                
                with col3:
                    st.write(f"**{dep['Time']}**")
                
                st.markdown("---")
    
    # ========================================================================
    # PHASE 5: AI ANALYTICS
    # ========================================================================
    
    @staticmethod
    def _render_ai_analytics(subscription):
        """Phase 5: AI-powered pipeline analytics"""
        
        st.subheader("🤖 AI-Powered Pipeline Analytics")
        st.caption("Intelligent insights and recommendations for your CI/CD pipelines")
        
        ai_tabs = st.tabs([
            "📊 Performance Analytics",
            "🔮 Predictive Insights",
            "💡 Optimization Recommendations",
            "🎯 Anomaly Detection"
        ])
        
        with ai_tabs[0]:
            AzureUnifiedCICDModule._render_performance_analytics()
        
        with ai_tabs[1]:
            AzureUnifiedCICDModule._render_predictive_insights()
        
        with ai_tabs[2]:
            AzureUnifiedCICDModule._render_optimization_recommendations()
        
        with ai_tabs[3]:
            AzureUnifiedCICDModule._render_anomaly_detection()
    
    @staticmethod
    def _render_performance_analytics():
        """Performance analytics"""
        
        st.markdown("### 📊 Pipeline Performance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Build Time", "12.5 min", delta="-2.3 min")
        with col2:
            st.metric("Success Rate", "94.2%", delta="↑ 3.1%")
        with col3:
            st.metric("Deployments/Day", "23", delta="↑ 5")
        with col4:
            st.metric("MTTR", "18 min", delta="↓ 7 min")
        
        st.markdown("---")
        
        st.markdown("#### 📈 Trends (Last 30 Days)")
        
        # Sample trend data
        st.info("📊 Build time decreased by 15% month-over-month")
        st.success("✅ Success rate improved by 3.1% this month")
        st.warning("⚠️ Queue time increased by 8% - consider adding build agents")
    
    @staticmethod
    def _render_predictive_insights():
        """Predictive insights"""
        
        st.markdown("### 🔮 AI Predictive Insights")
        
        insights = [
            {
                "type": "success",
                "icon": "🎯",
                "title": "High Success Probability",
                "message": "Your next deployment to production has a 97% predicted success rate based on recent patterns",
                "confidence": "97%"
            },
            {
                "type": "warning",
                "icon": "⚠️",
                "title": "Potential Bottleneck Detected",
                "message": "Build agent capacity may be insufficient during peak hours (2-4 PM UTC)",
                "confidence": "85%"
            },
            {
                "type": "info",
                "icon": "💡",
                "title": "Optimization Opportunity",
                "message": "Parallelizing test execution could reduce build time by ~22%",
                "confidence": "92%"
            }
        ]
        
        for insight in insights:
            if insight['type'] == 'success':
                st.success(f"{insight['icon']} **{insight['title']}** (Confidence: {insight['confidence']})\n\n{insight['message']}")
            elif insight['type'] == 'warning':
                st.warning(f"{insight['icon']} **{insight['title']}** (Confidence: {insight['confidence']})\n\n{insight['message']}")
            else:
                st.info(f"{insight['icon']} **{insight['title']}** (Confidence: {insight['confidence']})\n\n{insight['message']}")
    
    @staticmethod
    def _render_optimization_recommendations():
        """AI optimization recommendations"""
        
        st.markdown("### 💡 AI Optimization Recommendations")
        
        recommendations = [
            {
                "priority": "High",
                "title": "Cache Dependencies",
                "description": "Implement dependency caching to reduce build time by ~35%",
                "impact": "Save ~4.5 minutes per build",
                "effort": "Low"
            },
            {
                "priority": "Medium",
                "title": "Optimize Test Suite",
                "description": "Parallelize unit tests across 4 agents instead of 2",
                "impact": "Reduce test time by ~40%",
                "effort": "Medium"
            },
            {
                "priority": "High",
                "title": "Upgrade Build Agents",
                "description": "Upgrade to ubuntu-latest agents for better performance",
                "impact": "15-20% faster builds",
                "effort": "Low"
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{'🔴' if rec['priority'] == 'High' else '🟡'} {rec['title']} - {rec['priority']} Priority"):
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Impact:** {rec['impact']}")
                st.write(f"**Effort:** {rec['effort']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Apply Recommendation", key=f"apply_{rec['title']}"):
                        st.success("✅ Recommendation applied!")
                with col2:
                    if st.button("📋 Learn More", key=f"learn_{rec['title']}"):
                        st.info("Opening detailed guide...")
    
    @staticmethod
    def _render_anomaly_detection():
        """Anomaly detection"""
        
        st.markdown("### 🎯 Anomaly Detection")
        
        st.info("💡 AI-powered detection of unusual patterns in your pipelines")
        
        anomalies = [
            {"Time": "2 hours ago", "Pipeline": "prod-app-deployment", "Anomaly": "Unusually long build time (18 min vs avg 12 min)", "Severity": "⚠️ Medium"},
            {"Time": "1 day ago", "Pipeline": "staging-api-deploy", "Anomaly": "High failure rate (5 failures in 2 hours)", "Severity": "🔴 High"},
            {"Time": "3 days ago", "Pipeline": "dev-infrastructure", "Anomaly": "Unexpected resource usage spike", "Severity": "🟡 Low"},
        ]
        
        df = pd.DataFrame(anomalies)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### 🔍 Anomaly Analysis")
        
        selected_anomaly = st.selectbox("Select Anomaly for Details", [a["Anomaly"] for a in anomalies])
        
        if selected_anomaly:
            st.markdown("**Root Cause Analysis:**")
            st.write("• Possible cause: Increased test suite size")
            st.write("• Contributing factor: Resource contention during peak hours")
            
            st.markdown("**Recommended Actions:**")
            st.write("1. Review recent test additions")
            st.write("2. Consider scaling build agents")
            st.write("3. Implement test result caching")


# Module-level render function
def render():
    """Module-level render function"""
    AzureUnifiedCICDModule.render()
