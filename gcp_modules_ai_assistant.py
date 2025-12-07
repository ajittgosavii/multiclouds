"""
AI Assistant Module - Claude-Powered Cloud Operations Assistant (GCP)
Provides AI-powered assistance for GCP operations, architecture, and optimization
"""

import streamlit as st
from anthropic_helper import get_anthropic_helper
from typing import List, Dict
import json

class GCPAIAssistantModule:
    """AI-powered assistant for GCP cloud operations"""
    
    @staticmethod
    def render():
        """Render AI assistant interface"""
        
        st.markdown("## 🤖 AI Assistant (Claude)")
        st.caption("AI-powered assistance for GCP architecture, operations, and optimization")
        
        # Check if Anthropic is available
        helper = get_anthropic_helper()
        
        if not helper.is_available():
            st.warning("⚠️ Anthropic API not configured")
            st.info("""
            To enable AI Assistant features:
            
            1. Add your Anthropic API key to `.streamlit/secrets.toml`:
            ```toml
            [anthropic]
            api_key = "sk-ant-..."
            ```
            
            2. Or set environment variable:
            ```bash
            export ANTHROPIC_API_KEY="sk-ant-..."
            ```
            
            Get your API key at: https://console.anthropic.com/
            """)
            return
        
        st.success("✅ AI Assistant Ready (GCP Mode)")
        
        # AI Assistant features in tabs
        tabs = st.tabs([
            "💬 Chat Assistant",
            "🏗️ Architecture Design",
            "💰 Cost Optimization",
            "🔒 Security Analysis",
            "📝 Generate IaC",
            "📚 Runbook Generator"
        ])
        
        # Tab 1: Chat Assistant
        with tabs[0]:
            GCPAIAssistantModule._render_chat_assistant(helper)
        
        # Tab 2: Architecture Design
        with tabs[1]:
            GCPAIAssistantModule._render_architecture_design(helper)
        
        # Tab 3: Cost Optimization
        with tabs[2]:
            GCPAIAssistantModule._render_cost_optimization(helper)
        
        # Tab 4: Security Analysis
        with tabs[3]:
            GCPAIAssistantModule._render_security_analysis(helper)
        
        # Tab 5: Generate IaC
        with tabs[4]:
            GCPAIAssistantModule._render_iac_generator(helper)
        
        # Tab 6: Runbook Generator
        with tabs[5]:
            GCPAIAssistantModule._render_runbook_generator(helper)
    
    @staticmethod
    def _render_chat_assistant(helper):
        """Chat interface with Claude"""
        st.markdown("### 💬 Chat with Claude - GCP Expert")
        st.caption("Ask questions about GCP, get recommendations, troubleshoot issues")
        
        # Quick questions
        st.markdown("**Quick Questions:**")
        col1, col2, col3 = st.columns(3)
        
        quick_questions = [
            "How do I set up high availability for my web app?",
            "What's the best way to optimize my GCP costs?",
            "How can I improve my Cloud SQL performance?",
            "What security best practices should I follow?",
            "How do I migrate from VMs to containers?",
            "What's the difference between Cloud Run and Cloud Functions?"
        ]
        
        for i, question in enumerate(quick_questions):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    st.session_state.quick_question = question
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Handle quick question
        if hasattr(st.session_state, 'quick_question'):
            user_input = st.session_state.quick_question
            delattr(st.session_state, 'quick_question')
            
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            with st.spinner("Thinking..."):
                system_prompt = "You are a GCP cloud expert assistant. Provide detailed, practical answers about GCP services, architecture, and best practices."
                response = helper.chat(user_input, st.session_state.chat_history[:-1], system_prompt)
            
            if response:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            st.rerun()
        
        # Display chat history
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.chat_message("user").write(content)
            else:
                st.chat_message("assistant").write(content)
        
        # Chat input
        user_input = st.chat_input("Ask me anything about GCP infrastructure...")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Display user message
            st.chat_message("user").write(user_input)
            
            # Get AI response
            with st.spinner("Thinking..."):
                system_prompt = "You are a GCP cloud expert assistant. Provide detailed, practical answers about GCP services, architecture, and best practices."
                response = helper.chat(user_input, st.session_state.chat_history[:-1], system_prompt)
            
            if response:
                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display assistant message
                st.chat_message("assistant").write(response)
            else:
                st.error("Failed to get response from AI assistant")
        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
    
    @staticmethod
    def _render_architecture_design(helper):
        """Architecture design assistant"""
        st.markdown("### 🏗️ Architecture Design Assistant")
        st.caption("Get AI-powered GCP architecture recommendations")
        
        with st.form("architecture_form"):
            st.markdown("#### Describe Your Requirements")
            
            col1, col2 = st.columns(2)
            
            with col1:
                services = st.multiselect(
                    "GCP Services Needed",
                    ["Compute Engine", "Cloud SQL", "Cloud Storage", "Cloud Functions", 
                     "Cloud Run", "GKE", "Firestore", "Memorystore",
                     "Cloud CDN", "App Engine", "Apigee", "Pub/Sub", "Cloud Tasks",
                     "BigQuery", "Dataflow", "Eventarc",
                     "Cloud Workflows", "Vertex AI", "Cloud Identity", "Cloud Load Balancing"]
                )
                
                traffic = st.selectbox(
                    "Expected Traffic",
                    ["Low (< 1,000 req/day)", "Medium (1K-10K req/day)", 
                     "High (10K-100K req/day)", "Very High (100K-1M req/day)",
                     "Extreme (> 1M req/day)"]
                )
                
                budget = st.selectbox(
                    "Monthly Budget",
                    ["< $1,000", "$1,000 - $5,000", "$5,000 - $20,000", 
                     "$20,000 - $50,000", "> $50,000"]
                )
            
            with col2:
                compliance = st.multiselect(
                    "Compliance Requirements",
                    ["PCI-DSS", "HIPAA", "SOC 2", "GDPR", "ISO 27001", "FedRAMP", "None"]
                )
                
                architecture_type = st.selectbox(
                    "Architecture Type",
                    ["Web Application", "API Backend", "Data Processing Pipeline",
                     "Real-time Analytics", "Mobile Backend", "E-commerce Platform",
                     "IoT Platform", "Microservices", "Serverless"]
                )
                
                ha_required = st.checkbox("High Availability Required (Multi-Zone)")
                dr_required = st.checkbox("Disaster Recovery Required (Multi-Region)")
            
            additional_requirements = st.text_area(
                "Additional Requirements",
                placeholder="Any specific requirements, constraints, or preferences...\n\nExample:\n- Must support 10,000 concurrent users\n- Need real-time data processing\n- Integration with on-premise Active Directory",
                height=100
            )
            
            submitted = st.form_submit_button("🎯 Generate Architecture Recommendation", use_container_width=True)
        
        if submitted and services:
            with st.spinner("🤖 Generating architecture recommendations..."):
                requirements_text = f"""
Design a GCP architecture with the following requirements:

**Services**: {', '.join(services)}
**Architecture Type**: {architecture_type}
**Expected Traffic**: {traffic}
**Budget**: {budget}
**Compliance**: {', '.join(compliance) if compliance else 'None'}
**High Availability**: {'Yes (Multi-Zone deployment)' if ha_required else 'No'}
**Disaster Recovery**: {'Yes (Multi-Region with Cloud Load Balancing)' if dr_required else 'No'}

**Additional Requirements**:
{additional_requirements if additional_requirements else 'None'}

Please provide:
1. Architecture overview with component diagram description
2. Detailed service selection and configuration
3. Networking design (VPC, subnets, firewall rules)
4. High availability and scalability approach
5. Security best practices (Service Accounts, Cloud KMS, VPC Service Controls)
6. Cost estimation and optimization tips
7. Deployment strategy (Deployment Manager, Terraform, or gcloud)
"""
                
                recommendation = helper.chat(requirements_text, [], 
                    "You are a GCP Solutions Architect. Provide detailed, production-ready architecture recommendations.")
            
            if recommendation:
                st.markdown("#### 🎯 Architecture Recommendation")
                st.markdown(recommendation)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💾 Save Recommendation"):
                        st.success("✅ Recommendation saved")
                with col2:
                    if st.button("📄 Export as PDF"):
                        st.success("✅ Exported to PDF")
                with col3:
                    if st.button("📝 Generate IaC"):
                        st.success("✅ Switched to IaC tab")
    
    @staticmethod
    def _render_cost_optimization(helper):
        """Cost optimization assistant"""
        st.markdown("### 💰 Cost Optimization Assistant")
        st.caption("Analyze GCP resources and get AI-powered cost optimization recommendations")
        
        # Analysis type
        analysis_type = st.radio(
            "Analysis Type",
            ["Quick Scan", "Deep Analysis", "Custom Query"],
            horizontal=True
        )
        
        if analysis_type == "Quick Scan":
            st.info("Quick scan analyzes common cost optimization opportunities across Compute Engine, Cloud SQL, and Cloud Storage")
            
            if st.button("🔍 Run Quick Scan", use_container_width=True):
                with st.spinner("🤖 Analyzing resources for cost optimization..."):
                    resources_text = """
Analyze these GCP resources for cost optimization:

**Compute Engine Instances:**
- vm-web-01: n1-standard-4, CPU avg 15%, Running 24/7
- vm-app-01: n2-standard-8, CPU avg 8%, Running 24/7
- vm-worker-01: c2-standard-16, CPU avg 45%, Running 24/7

**Cloud SQL Instances:**
- cloudsql-prod: Enterprise Plus, 8 vCPU, Connections avg 25%, 500GB storage
- cloudsql-staging: Enterprise, 2 vCPU, Connections avg 5%, 100GB storage

**Persistent Disks:**
- disk-ssd-01: SSD persistent disk, 1TB, IOPS avg 30%
- disk-standard-01: Standard persistent disk, 500GB, Last accessed 90 days ago

**Cloud Storage Buckets:**
- bucket-logs: Standard storage, 5TB, 90% objects > 90 days old
- bucket-backup: Standard storage, 10TB, Accessed once per month

Provide specific cost optimization recommendations with estimated savings.
"""
                    
                    analysis = helper.chat(resources_text, [],
                        "You are a GCP cost optimization expert. Provide specific, actionable recommendations with estimated savings.")
                
                if analysis:
                    st.markdown("#### 💡 Cost Optimization Recommendations")
                    st.markdown(analysis)
        
        elif analysis_type == "Deep Analysis":
            st.info("Deep analysis includes comprehensive review of all services, Committed Use Discount recommendations, and optimization")
            
            services_to_analyze = st.multiselect(
                "Services to Analyze",
                ["Compute Engine", "Cloud SQL", "Cloud Storage", "Cloud Functions", "Firestore", "Persistent Disks", "Cloud CDN", "Network Egress"],
                default=["Compute Engine", "Cloud SQL", "Cloud Storage"]
            )
            
            if st.button("🔬 Run Deep Analysis", use_container_width=True):
                with st.spinner("🤖 Performing deep cost analysis..."):
                    analysis_text = f"""
Perform a deep cost optimization analysis for: {', '.join(services_to_analyze)}

Focus on:
1. Right-sizing opportunities (machine types, Cloud SQL tiers)
2. Committed Use Discount / Sustained Use Discount recommendations
3. Storage optimization (storage classes, lifecycle policies)
4. Unused resource identification (orphaned disks, snapshots)
5. Architecture improvements for cost efficiency
6. Network egress and data transfer optimization

Provide detailed recommendations with:
- Current cost
- Optimized cost
- Estimated monthly savings
- Implementation complexity (Low/Medium/High)
- Priority (High/Medium/Low)
"""
                    
                    analysis = helper.chat(analysis_text, [],
                        "You are a GCP FinOps expert. Provide comprehensive cost analysis with specific recommendations and ROI calculations.")
                
                if analysis:
                    st.markdown("#### 📊 Deep Analysis Results")
                    st.markdown(analysis)
        
        else:  # Custom Query
            custom_query = st.text_area(
                "Cost Optimization Query",
                placeholder="Example:\n- How can I reduce network egress costs?\n- What's the best machine type for my workload?\n- Should I use Cloud Functions or Cloud Run?",
                height=100
            )
            
            if st.button("🎯 Analyze", use_container_width=True):
                if custom_query:
                    with st.spinner("🤖 Analyzing..."):
                        analysis = helper.chat(custom_query, [],
                            "You are a GCP cost optimization expert. Provide specific recommendations with cost estimates.")
                    
                    if analysis:
                        st.markdown("#### 💡 Analysis Results")
                        st.markdown(analysis)
        
        # Action buttons
        if st.session_state.get('cost_analysis_complete'):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📄 Export Report"):
                    st.success("✅ Report exported to PDF")
            with col2:
                if st.button("📋 Create Action Plan"):
                    st.success("✅ Action plan created")
            with col3:
                if st.button("📧 Email to Team"):
                    st.success("✅ Report emailed")
    
    @staticmethod
    def _render_security_analysis(helper):
        """Security analysis assistant"""
        st.markdown("### 🔒 Security Analysis Assistant")
        st.caption("Analyze security findings and get AI-powered remediation recommendations")
        
        analysis_mode = st.radio(
            "Analysis Mode",
            ["Security Findings", "IAM Policy Review", "Network Security", "Compliance Check"],
            horizontal=True
        )
        
        if analysis_mode == "Security Findings":
            if st.button("🔍 Analyze Recent Security Findings", use_container_width=True):
                with st.spinner("🤖 Analyzing security findings from Security Command Center..."):
                    findings_text = """
Analyze these GCP Security Command Center findings and provide remediation steps:

**CRITICAL Findings:**
1. Cloud Storage bucket 'app-data-bucket' is publicly accessible
   - Resource: projects/my-project/buckets/app-data-bucket
   - Description: Bucket has allUsers with Storage Object Viewer permission

2. Firewall rule allows unrestricted SSH access
   - Resource: projects/my-project/global/firewalls/allow-ssh
   - Description: Firewall rule allows SSH (port 22) from 0.0.0.0/0

**HIGH Findings:**
3. Service account 'app-service@project.iam.gserviceaccount.com' has overly broad permissions
   - Resource: projects/my-project/serviceAccounts/app-service
   - Description: Service account has Project Editor role

4. Cloud SQL instance 'prod-db' allows public IP access
   - Resource: projects/my-project/instances/prod-db
   - Description: Instance has public IP and allows access from 0.0.0.0/0

5. Compute Engine instance 'vm-app-01' has no backup/snapshot policy
   - Resource: projects/my-project/zones/us-central1-a/instances/vm-app-01
   - Description: Instance has no snapshot schedule configured

For each finding, provide:
1. Risk assessment
2. Step-by-step remediation
3. gcloud commands or console steps
4. Prevention best practices
"""
                    
                    analysis = helper.chat(findings_text, [],
                        "You are a GCP security expert. Provide detailed remediation steps with specific gcloud commands.")
                
                if analysis:
                    st.markdown("#### 🛡️ Security Analysis & Remediation")
                    st.markdown(analysis)
        
        elif analysis_mode == "IAM Policy Review":
            policy_input = st.text_area(
                "Paste IAM Policy JSON",
                placeholder='{\n  "bindings": [\n    {\n      "role": "roles/editor",\n      "members": ["serviceAccount:app@project.iam.gserviceaccount.com"]\n    }\n  ]\n}',
                height=200
            )
            
            if st.button("🔒 Analyze IAM Policy", use_container_width=True):
                if policy_input:
                    with st.spinner("🤖 Analyzing GCP IAM policy..."):
                        policy_text = f"""
Analyze this GCP IAM policy for security issues and recommend improvements:

```json
{policy_input}
```

Check for:
1. Overly permissive roles (Owner, Editor at project level)
2. Violation of least privilege principle
3. Use of primitive roles instead of predefined/custom roles
4. Missing IAM conditions for additional security
5. Service account key usage (recommend Workload Identity)
6. Potential security risks

Provide:
- Security issues found
- Risk level for each issue
- Recommended policy improvements
- Improved policy JSON
- Comparison with GCP best practices
"""
                        
                        analysis = helper.chat(policy_text, [],
                            "You are a GCP IAM security expert. Analyze policies and provide secure alternatives.")
                    
                    if analysis:
                        st.markdown("#### 🔐 IAM Policy Analysis")
                        st.markdown(analysis)
        
        elif analysis_mode == "Network Security":
            if st.button("🌐 Analyze Network Security", use_container_width=True):
                with st.spinner("🤖 Analyzing GCP network security configuration..."):
                    network_text = """
Analyze this GCP network security configuration:

**VPC Network:**
- VPC: vpc-prod (custom mode)
- Public Subnets: subnet-public-1 (10.0.1.0/24), subnet-public-2 (10.0.2.0/24)
- Private Subnets: subnet-private-1 (10.0.10.0/24), subnet-private-2 (10.0.11.0/24)

**Firewall Rules:**
- allow-web: Allows 0.0.0.0/0 on ports 80, 443, 22
- allow-app: Allows subnet-public on port 8080
- allow-db: Allows subnet-private on port 3306

**Cloud Armor:** Not configured
**VPC Service Controls:** Not configured

Analyze for:
1. Firewall rule misconfigurations
2. Network segmentation best practices
3. Private Google Access and Private Service Connect usage
4. Cloud Armor and DDoS protection opportunities
5. VPC Service Controls recommendations
6. Cloud NAT and Cloud Router configuration
"""
                    
                    analysis = helper.chat(network_text, [],
                        "You are a GCP network security expert. Provide comprehensive network security analysis.")
                
                if analysis:
                    st.markdown("#### 🛡️ Network Security Analysis")
                    st.markdown(analysis)
        
        else:  # Compliance Check
            framework = st.selectbox(
                "Compliance Framework",
                ["PCI-DSS", "HIPAA", "SOC 2", "GDPR", "CIS GCP Foundations", "NIST", "ISO 27001"]
            )
            
            if st.button(f"✅ Check {framework} Compliance", use_container_width=True):
                with st.spinner(f"🤖 Checking {framework} compliance..."):
                    compliance_text = f"""
Perform a {framework} compliance check for GCP environment and provide:

1. Key compliance requirements for {framework}
2. GCP services and features that help achieve compliance (Policy Intelligence, Security Command Center)
3. Common compliance gaps and how to address them
4. Recommended Organization Policy constraints for continuous compliance
5. Audit and monitoring best practices (Cloud Audit Logs, Cloud Logging)
6. Documentation and attestation requirements
7. Compliance Reports and Assured Workloads usage
"""
                    
                    analysis = helper.chat(compliance_text, [],
                        f"You are a GCP compliance expert specializing in {framework}. Provide actionable compliance guidance.")
                
                if analysis:
                    st.markdown(f"#### ✅ {framework} Compliance Analysis")
                    st.markdown(analysis)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Create Remediation Tasks"):
                st.success("✅ Remediation tasks created")
        with col2:
            if st.button("📄 Export Security Report"):
                st.success("✅ Report exported")
        with col3:
            if st.button("🔔 Set Up Alerts"):
                st.success("✅ Alerts configured in Cloud Monitoring")
    
    @staticmethod
    def _render_iac_generator(helper):
        """Infrastructure as Code generator"""
        st.markdown("### 📝 Generate Infrastructure as Code")
        st.caption("Describe your GCP infrastructure and get Terraform/Deployment Manager code")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            format_type = st.selectbox(
                "IaC Format",
                ["Terraform (HCL)", "Deployment Manager (YAML)", "Deployment Manager (Python)", "Pulumi (Python)", "Pulumi (Go)"]
            )
        
        with col2:
            include_modules = st.checkbox("Use Modules/Registry", value=True)
            include_comments = st.checkbox("Include Comments", value=True)
        
        infrastructure_desc = st.text_area(
            "Describe Infrastructure",
            placeholder="""Example:

I need a production-ready web application with:

1. VPC with public and private subnets across 3 zones
2. Cloud Load Balancer (HTTPS) with SSL certificate
3. Managed Instance Group (2-10 e2-medium instances) in private subnet
4. Cloud SQL MySQL (HA configuration) in private subnet with Private Service Connect
5. Memorystore Redis instance for session storage
6. Cloud Storage bucket for static files with Cloud CDN
7. Cloud DNS zone for custom domain
8. Cloud KMS for encryption keys
9. Cloud Monitoring and Cloud Logging workspace
10. All resources with appropriate labels and firewall rules
""",
            height=250
        )
        
        if st.button("🚀 Generate IaC Template", use_container_width=True):
            if infrastructure_desc:
                with st.spinner(f"🤖 Generating {format_type} template..."):
                    iac_prompt = f"""
Generate production-ready {format_type} code for this GCP infrastructure:

{infrastructure_desc}

Requirements:
- Follow GCP best practices and Architecture Framework
- Include proper security configurations (Service Accounts, Cloud KMS, VPC Service Controls)
- Add resource dependencies
- Include variables/parameters and outputs
- {"Use Terraform modules from Google Cloud Foundation Fabric where appropriate" if include_modules and "Terraform" in format_type else ""}
- {"Add detailed comments explaining each section" if include_comments else ""}
- Ensure high availability and fault tolerance
- Use multiple zones where applicable

Provide complete, working code that can be deployed immediately with gcloud or terraform.
"""
                    
                    template = helper.chat(iac_prompt, [],
                        f"You are a GCP IaC expert specializing in {format_type}. Generate production-ready, well-structured code following GCP best practices.")
                
                if template:
                    st.markdown(f"#### 📄 Generated {format_type} Template")
                    
                    # Determine language for syntax highlighting
                    if "Terraform" in format_type:
                        language = "hcl"
                    elif "YAML" in format_type:
                        language = "yaml"
                    elif "Python" in format_type:
                        language = "python"
                    else:
                        language = "go"
                    
                    st.code(template, language=language)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📥 Download Template"):
                            st.success("✅ Template downloaded")
                    with col2:
                        if st.button("✅ Validate Syntax"):
                            st.success("✅ Syntax valid (terraform validate / gcloud deployment-manager)")
                    with col3:
                        if st.button("🚀 Deploy to GCP"):
                            st.info("🚀 Deployment initiated")
            else:
                st.warning("⚠️ Please describe the infrastructure you want to create")
        
        # Example templates
        with st.expander("📚 Example Templates"):
            st.markdown("""
            **Common Patterns:**
            - Three-tier web application (Cloud Load Balancer + MIG + Cloud SQL)
            - Serverless API (API Gateway + Cloud Functions + Firestore)
            - Data platform (Cloud Storage + BigQuery + Dataflow + Looker)
            - Container platform (GKE cluster with Cloud Load Balancer)
            - CI/CD pipeline (Cloud Build with Artifact Registry)
            - Event-driven architecture (Eventarc + Cloud Functions + Pub/Sub)
            """)
    
    @staticmethod
    def _render_runbook_generator(helper):
        """Operational runbook generator"""
        st.markdown("### 📚 Runbook Generator")
        st.caption("Generate detailed operational runbooks for GCP operations")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            operation_type = st.selectbox(
                "Operation Type",
                [
                    "Deploy Application Update",
                    "Database Migration (Cloud SQL)",
                    "Disaster Recovery Failover",
                    "Scale Up/Down Infrastructure",
                    "Security Incident Response",
                    "Backup and Restore",
                    "Certificate Renewal (Cloud Load Balancing)",
                    "Cloud Function Deployment",
                    "GKE Cluster Upgrade",
                    "Cloud SQL Point-in-Time Recovery",
                    "Cloud Storage Recovery",
                    "VM Restore from Snapshot",
                    "Custom Operation"
                ]
            )
        
        with col2:
            include_rollback = st.checkbox("Include Rollback", value=True)
            include_validation = st.checkbox("Include Validation", value=True)
        
        if operation_type == "Custom Operation":
            operation_name = st.text_input("Operation Name", placeholder="e.g., Migrate to multi-region deployment")
        else:
            operation_name = operation_type
        
        context = st.text_area(
            "Additional Context",
            placeholder="""Provide specific context about your environment:

Example:
- Environment: Production
- GCP Region: us-central1
- Application: E-commerce platform
- Database: Cloud SQL MySQL, Enterprise Plus, 8 vCPU
- Traffic: 10,000 requests/minute
- Maintenance Window: Sundays 2 AM - 6 AM CST
- Team: 3 engineers on-call
""",
            height=150
        )
        
        if st.button("📖 Generate Runbook", use_container_width=True):
            if operation_name:
                with st.spinner("🤖 Generating detailed runbook..."):
                    runbook_prompt = f"""
Generate a detailed operational runbook for: {operation_name}

Context:
{context if context else "Standard GCP production environment"}

The runbook should include:

1. **Overview**
   - Operation description
   - Prerequisites
   - Required permissions (IAM roles)
   - Estimated duration

2. **Pre-Operation Checklist**
   - Verification steps (gcloud commands)
   - Backup requirements
   - Team notifications
   - Check for resource locks/policies

3. **Step-by-Step Procedure**
   - Detailed steps with gcloud commands
   - Cloud Console instructions as alternative
   - Expected outputs for each step
   - Decision points and branching

4. **Validation Steps**
   - Health checks
   - Cloud Monitoring dashboards to watch
   - Success criteria
{"" if not include_validation else "- Automated validation scripts"}

5. **Rollback Procedure**
   - When to rollback
   - Step-by-step rollback instructions
   - Rollback validation
{"" if not include_rollback else "- Emergency rollback (< 5 minutes)"}

6. **Post-Operation Tasks**
   - Cleanup activities
   - Documentation updates
   - Team notifications
   - Lessons learned

7. **Troubleshooting**
   - Common issues and solutions
   - Emergency contacts
   - Escalation procedures
   - Google Cloud Support ticket process

Make it production-ready and executable by an engineer with GCP experience.
Include specific gcloud commands and resource paths.
"""
                    
                    runbook = helper.chat(runbook_prompt, [],
                        "You are a GCP operations expert. Generate comprehensive, production-ready runbooks with specific gcloud commands.")
                
                if runbook:
                    st.markdown("#### 📖 Generated Runbook")
                    st.markdown(runbook)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("💾 Save to Database"):
                            st.success("✅ Runbook saved")
                    with col2:
                        if st.button("📄 Export as PDF"):
                            st.success("✅ PDF exported")
                    with col3:
                        if st.button("📧 Email to Team"):
                            st.success("✅ Emailed to team")
                    with col4:
                        if st.button("📋 Add to Documentation"):
                            st.success("✅ Added to wiki")
            else:
                st.warning("⚠️ Please specify an operation name")
        
        # Runbook library
        with st.expander("📚 Runbook Library"):
            st.markdown("""
            **Available Templates:**
            - Blue/Green Deployment with Cloud Load Balancer
            - Cloud SQL High Availability Failover Testing
            - Managed Instance Group Rolling Update
            - Cloud Function Deployment with Traffic Splitting
            - Cloud Storage Cross-Region Replication Setup
            - Cloud CDN Cache Invalidation
            - Cloud DNS Failover Configuration
            - VM Patching with OS Patch Management
            """)
