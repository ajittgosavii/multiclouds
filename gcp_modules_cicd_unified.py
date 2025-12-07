"""
Unified CI/CD Module for GCP - All 5 Phases Combined
Complete CI/CD Platform with Pipeline Building, Triggering, Approvals, Multi-Project, and AI Analytics
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class GCPUnifiedCICDModule:
    """Unified GCP CI/CD Module with all 5 phases"""
    
    @staticmethod
    def render():
        """Main render method"""
        
        # Custom CSS
        st.markdown("""
        <style>
        .template-card {
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
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
        
        st.title("🔄 GCP CI/CD Pipeline Management")
        st.markdown("**Complete CI/CD Platform** - Build, Trigger, Approve, Deploy Multi-Project, and AI-Powered Analytics")
        
        st.info("💡 **Cloud Build Integration:** This module integrates with Cloud Build, Cloud Deploy, and GitHub Actions")
        
        # Project selector
        projects = [
            "prod-project-001",
            "dev-project-001",
            "staging-project-001"
        ]
        
        selected_project = st.selectbox(
            "Select GCP Project",
            options=projects,
            key="gcp_cicd_project_selector"
        )
        
        if not selected_project:
            st.info("Please select a project")
            return
        
        # Main phase tabs - ALL 5 PHASES
        phase_tabs = st.tabs([
            "🗃️ Pipeline Builder",
            "⚡ Triggering & Parameters",
            "⏸️ Approvals & Notifications",
            "🌐 Multi-Project",
            "🤖 AI Analytics"
        ])
        
        # Phase 1: Pipeline Builder
        with phase_tabs[0]:
            GCPUnifiedCICDModule._render_pipeline_builder(selected_project)
        
        # Phase 2: Triggering & Parameters
        with phase_tabs[1]:
            GCPUnifiedCICDModule._render_triggering(selected_project)
        
        # Phase 3: Approvals & Notifications
        with phase_tabs[2]:
            GCPUnifiedCICDModule._render_approvals(selected_project)
        
        # Phase 4: Multi-Project Management
        with phase_tabs[3]:
            GCPUnifiedCICDModule._render_multi_project(selected_project)
        
        # Phase 5: AI Analytics
        with phase_tabs[4]:
            GCPUnifiedCICDModule._render_ai_analytics(selected_project)
    
    @staticmethod
    def _render_pipeline_builder(project):
        """Phase 1: Pipeline Builder"""
        st.subheader("🗃️ Cloud Build Pipeline Builder")
        st.caption("Create and manage Cloud Build pipelines entirely within CloudIDP")
        
        builder_tabs = st.tabs([
            "📋 Pipeline Templates",
            "🆕 Create Pipeline",
            "📊 Existing Pipelines",
            "⚙️ Pipeline Settings"
        ])
        
        with builder_tabs[0]:
            # Templates
            st.markdown("### 📚 Cloud Build Templates")
            templates = [
                {"name": "Cloud Run Deployment", "icon": "🚀", "desc": "Deploy to Cloud Run with Docker"},
                {"name": "GKE Deployment", "icon": "🐳", "desc": "Build and deploy to GKE cluster"},
                {"name": "Infrastructure (Terraform)", "icon": "🏗️", "desc": "Deploy with Terraform"},
                {"name": "Cloud Functions", "icon": "⚡", "desc": "Deploy serverless functions"}
            ]
            
            col1, col2 = st.columns(2)
            for idx, t in enumerate(templates):
                with (col1 if idx % 2 == 0 else col2):
                    st.markdown(f"""<div class="template-card">
                        <h3>{t['icon']} {t['name']}</h3>
                        <p>{t['desc']}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Use {t['name']}", key=f"use_{idx}"):
                        st.success(f"✅ Template '{t['name']}' selected!")
        
        with builder_tabs[1]:
            # Create Pipeline
            st.markdown("### 🆕 Create Cloud Build Pipeline")
            with st.form("create_gcp_pipeline"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Pipeline Name*", placeholder="prod-app-deploy")
                    repo = st.text_input("Repository URL", placeholder="https://github.com/org/repo")
                    branch = st.selectbox("Branch", ["main", "develop", "master"])
                with col2:
                    build_type = st.selectbox("Build Type", ["cloudbuild.yaml", "Dockerfile", "Buildpacks"])
                    region = st.selectbox("Region", ["us-central1", "us-east1", "europe-west1"])
                    trigger_type = st.selectbox("Trigger", ["On Push", "On PR", "Manual", "Scheduled"])
                
                stages = st.multiselect("Stages", 
                    ["Build", "Test", "Security Scan", "Deploy to Dev", "Deploy to Staging", 
                     "Manual Approval", "Deploy to Production"],
                    default=["Build", "Test", "Deploy to Staging", "Manual Approval", "Deploy to Production"])
                
                if st.form_submit_button("🚀 Create Pipeline", type="primary"):
                    st.success(f"✅ Pipeline '{name}' created!")
                    st.code(f"""steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/{project}/{name}', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/{project}/{name}']
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', '{name}', '--image', 'gcr.io/{project}/{name}', '--region', '{region}']""", language="yaml")
        
        with builder_tabs[2]:
            # Existing Pipelines
            st.markdown("### 📊 Existing Pipelines")
            pipelines = [
                {"Name": "prod-app-deploy", "Status": "✅ Success", "Last Run": "2h ago", "Success Rate": "96%"},
                {"Name": "staging-api", "Status": "🔄 Running", "Last Run": "5m ago", "Success Rate": "89%"},
                {"Name": "dev-infra", "Status": "✅ Success", "Last Run": "1d ago", "Success Rate": "93%"}
            ]
            st.dataframe(pd.DataFrame(pipelines), use_container_width=True, hide_index=True)
            
            sel = st.selectbox("Select for Actions", [p["Name"] for p in pipelines])
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("▶️ Run", use_container_width=True)
            with col2:
                st.button("⏸️ Pause", use_container_width=True)
            with col3:
                st.button("✏️ Edit", use_container_width=True)
            with col4:
                st.button("🗑️ Delete", use_container_width=True)
        
        with builder_tabs[3]:
            # Settings
            st.markdown("### ⚙️ Pipeline Settings")
            with st.form("pipeline_settings"):
                col1, col2 = st.columns(2)
                with col1:
                    st.number_input("Retention (days)", 1, 365, 90)
                    st.number_input("Timeout (minutes)", 10, 480, 60)
                with col2:
                    st.checkbox("Enable logs", value=True)
                    st.checkbox("Enable artifacts", value=True)
                
                if st.form_submit_button("💾 Save Settings", type="primary"):
                    st.success("✅ Settings saved!")
    
    @staticmethod
    def _render_triggering(project):
        """Phase 2: Triggering"""
        st.subheader("⚡ Pipeline Triggering & Parameters")
        
        tabs = st.tabs(["🎯 Manual Trigger", "⏰ Scheduled", "🔗 Webhooks", "📊 History"])
        
        with tabs[0]:
            st.markdown("### 🎯 Manual Trigger")
            with st.form("manual_trigger"):
                pipeline = st.selectbox("Pipeline", ["prod-app-deploy", "staging-api", "dev-infra"])
                branch = st.selectbox("Branch", ["main", "develop"])
                
                col1, col2 = st.columns(2)
                with col1:
                    env = st.selectbox("Environment", ["dev", "staging", "production"])
                    regions = st.multiselect("Regions", ["us-central1", "us-east1", "europe-west1"])
                with col2:
                    st.checkbox("Run tests", value=True)
                    st.checkbox("Auto-rollback", value=True)
                
                params = st.text_area("Parameters (YAML)", value="version: 1.0.0\nfeature_flags:\n  - new-ui\n  - api-v2")
                
                if st.form_submit_button("🚀 Trigger", type="primary"):
                    st.success(f"✅ Pipeline '{pipeline}' triggered!")
                    st.info(f"Build ID: {datetime.now().strftime('%Y%m%d-%H%M%S')}")
        
        with tabs[1]:
            st.markdown("### ⏰ Scheduled Triggers")
            schedules = [
                {"Name": "Nightly Build", "Schedule": "0 2 * * *", "Pipeline": "prod-app-deploy", "Status": "✅ Active"},
                {"Name": "Weekly Deploy", "Schedule": "0 0 * * 0", "Pipeline": "staging-api", "Status": "✅ Active"}
            ]
            st.dataframe(pd.DataFrame(schedules), use_container_width=True, hide_index=True)
        
        with tabs[2]:
            st.markdown("### 🔗 Webhooks")
            webhooks = [
                {"Name": "GitHub Push", "URL": "https://cloudbuild.googleapis.com/...", "Events": "push, PR"},
                {"Name": "Docker Hub", "URL": "https://cloudbuild.googleapis.com/...", "Events": "image push"}
            ]
            st.dataframe(pd.DataFrame(webhooks), use_container_width=True, hide_index=True)
        
        with tabs[3]:
            st.markdown("### 📊 History")
            history = [
                {"Time": "2h ago", "Pipeline": "prod-app-deploy", "Trigger": "Manual", "User": "john@company.com", "Status": "✅"},
                {"Time": "5h ago", "Pipeline": "staging-api", "Trigger": "Webhook", "User": "github", "Status": "✅"}
            ]
            st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_approvals(project):
        """Phase 3: Approvals"""
        st.subheader("⏸️ Approvals & Notifications")
        
        tabs = st.tabs(["✅ Pending", "📋 Rules", "🔔 Notifications", "📊 History"])
        
        with tabs[0]:
            st.markdown("### ✅ Pending Approvals")
            approvals = [
                {"Pipeline": "prod-app-deploy", "Env": "Production", "By": "john@company.com", "At": "30m ago"},
                {"Pipeline": "prod-db-migration", "Env": "Production", "By": "jane@company.com", "At": "2h ago"}
            ]
            
            for a in approvals:
                st.markdown(f"### 🔴 {a['Env'].upper()} | {a['Pipeline']}")
                st.write(f"**By:** {a['By']} | **At:** {a['At']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve", key=f"app_{a['Pipeline']}", type="primary"):
                        st.success("✅ Approved!")
                        st.balloons()
                with col2:
                    if st.button("❌ Reject", key=f"rej_{a['Pipeline']}"):
                        st.error("❌ Rejected")
                st.markdown("---")
        
        with tabs[1]:
            st.markdown("### 📋 Approval Rules")
            rules = [
                {"Environment": "Production", "Approvers": "2", "Timeout": "4h", "Auto-approve": "No"},
                {"Environment": "Staging", "Approvers": "1", "Timeout": "2h", "Auto-approve": "After 24h"}
            ]
            st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
        
        with tabs[2]:
            st.markdown("### 🔔 Notifications")
            with st.form("notifications"):
                channels = st.multiselect("Channels", ["Email", "Chat", "Pub/Sub", "SMS"], default=["Email"])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox("Success", value=True)
                    st.checkbox("Failure", value=True)
                with col2:
                    st.checkbox("Approval needed", value=True)
                    st.checkbox("Canceled")
                
                if st.form_submit_button("💾 Save", type="primary"):
                    st.success("✅ Saved!")
        
        with tabs[3]:
            st.markdown("### 📊 History")
            history = [
                {"Time": "2h ago", "Pipeline": "prod-app-deploy", "Approver": "john@company.com", "Decision": "✅ Approved"},
                {"Time": "1d ago", "Pipeline": "prod-db-migration", "Approver": "jane@company.com", "Decision": "❌ Rejected"}
            ]
            st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_multi_project(project):
        """Phase 4: Multi-Project"""
        st.subheader("🌐 Multi-Project Management")
        
        tabs = st.tabs(["🗺️ Overview", "🚀 Cross-Project Deploy", "🔄 Groups", "📊 Status"])
        
        with tabs[0]:
            st.markdown("### 🗺️ Project Overview")
            projects = [
                {"Project": "prod-project-001", "Env": "Production", "Region": "us-central1", "Pipelines": "12"},
                {"Project": "staging-project-001", "Env": "Staging", "Region": "us-east1", "Pipelines": "8"},
                {"Project": "dev-project-001", "Env": "Dev", "Region": "europe-west1", "Pipelines": "15"}
            ]
            st.dataframe(pd.DataFrame(projects), use_container_width=True, hide_index=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Projects", "3")
            with col2:
                st.metric("Pipelines", "35")
            with col3:
                st.metric("Deployments (24h)", "52")
        
        with tabs[1]:
            st.markdown("### 🚀 Cross-Project Deploy")
            with st.form("cross_project"):
                pipeline = st.selectbox("Pipeline", ["prod-app-deploy", "infra-deploy"])
                targets = st.multiselect("Target Projects", 
                    ["prod-project-001", "staging-project-001", "dev-project-001"])
                strategy = st.radio("Strategy", ["Sequential", "Parallel", "Canary"])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox("Auto-rollback", value=True)
                    st.checkbox("Health checks", value=True)
                with col2:
                    st.checkbox("Notify on complete", value=True)
                    st.checkbox("Approval per project")
                
                if st.form_submit_button("🚀 Deploy", type="primary"):
                    st.success(f"✅ Deploying to {len(targets)} projects!")
        
        with tabs[2]:
            st.markdown("### 🔄 Project Groups")
            groups = [
                {"Group": "Production", "Projects": "prod-project-001", "Deploys": "234"},
                {"Group": "Non-Prod", "Projects": "staging, dev", "Deploys": "567"}
            ]
            st.dataframe(pd.DataFrame(groups), use_container_width=True, hide_index=True)
        
        with tabs[3]:
            st.markdown("### 📊 Status")
            status = [
                {"Project": "prod-project-001", "Status": "✅ Success", "Progress": "100%"},
                {"Project": "staging-project-001", "Status": "🔄 Running", "Progress": "65%"},
                {"Project": "dev-project-001", "Status": "⏳ Queued", "Progress": "0%"}
            ]
            for s in status:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{s['Project']}**")
                    st.progress(int(s['Progress'].replace('%', '')) / 100 if s['Progress'] != 'Pending' else 0)
                with col2:
                    st.metric("Status", s['Status'])
                st.markdown("---")
    
    @staticmethod
    def _render_ai_analytics(project):
        """Phase 5: AI Analytics"""
        st.subheader("🤖 AI-Powered Analytics")
        
        tabs = st.tabs(["📊 Performance", "🔮 Predictions", "💡 Recommendations", "🎯 Anomalies"])
        
        with tabs[0]:
            st.markdown("### 📊 Performance")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Build", "11.2 min", "-1.8 min")
            with col2:
                st.metric("Success Rate", "95.8%", "↑ 2.3%")
            with col3:
                st.metric("Deploys/Day", "28", "↑ 6")
            with col4:
                st.metric("MTTR", "15 min", "↓ 5 min")
            
            st.info("📊 Build time decreased 12% month-over-month")
            st.success("✅ Success rate improved 2.3% this month")
        
        with tabs[1]:
            st.markdown("### 🔮 AI Predictions")
            st.success("🎯 **High Success Probability** (98%)\n\nNext production deploy has 98% predicted success")
            st.warning("⚠️ **Capacity Warning** (87%)\n\nBuild capacity may be insufficient 2-4 PM UTC")
            st.info("💡 **Optimization Opportunity** (94%)\n\nParallel testing could save ~25% build time")
        
        with tabs[2]:
            st.markdown("### 💡 Recommendations")
            recs = [
                {"Priority": "High", "Title": "Cache Dependencies", "Impact": "Save ~3.8 min/build"},
                {"Priority": "Medium", "Title": "Parallel Tests", "Impact": "Reduce time 35%"},
                {"Priority": "High", "Title": "Use Kaniko", "Impact": "15-20% faster builds"}
            ]
            for r in recs:
                with st.expander(f"{'🔴' if r['Priority']=='High' else '🟡'} {r['Title']}"):
                    st.write(f"**Impact:** {r['Impact']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("✅ Apply", key=f"app_{r['Title']}")
                    with col2:
                        st.button("📋 Learn More", key=f"learn_{r['Title']}")
        
        with tabs[3]:
            st.markdown("### 🎯 Anomalies")
            anomalies = [
                {"Time": "2h ago", "Pipeline": "prod-app-deploy", "Anomaly": "Long build (16m vs avg 11m)", "Severity": "⚠️ Medium"},
                {"Time": "1d ago", "Pipeline": "staging-api", "Anomaly": "High failures (5 in 2h)", "Severity": "🔴 High"}
            ]
            st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)
            
            st.markdown("**Root Cause:** Increased test suite size")
            st.markdown("**Actions:** 1) Review tests 2) Scale builders 3) Cache results")

def render():
    """Module-level render function"""
    GCPUnifiedCICDModule.render()
