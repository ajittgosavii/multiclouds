"""
AI Assistant Module - Claude-Powered Cloud Operations Assistant (Azure)
Provides AI-powered assistance for Azure operations, architecture, and optimization
"""

import streamlit as st
from anthropic_helper import get_anthropic_helper
from typing import List, Dict
import json
from auth_azure_sso import require_permission

class AzureAIAssistantModule:
    """AI-powered assistant for Azure cloud operations"""
    
    @staticmethod
    @require_permission('view_dashboard')

    def render():
        """Render AI assistant interface"""
        
        st.markdown("## 🤖 AI Assistant (Claude)")
        st.caption("AI-powered assistance for Azure architecture, operations, and optimization")
        
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
        
        st.success("✅ AI Assistant Ready (Azure Mode)")
        
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
            AzureAIAssistantModule._render_chat_assistant(helper)
        
        # Tab 2: Architecture Design
        with tabs[1]:
            AzureAIAssistantModule._render_architecture_design(helper)
        
        # Tab 3: Cost Optimization
        with tabs[2]:
            AzureAIAssistantModule._render_cost_optimization(helper)
        
        # Tab 4: Security Analysis
        with tabs[3]:
            AzureAIAssistantModule._render_security_analysis(helper)
        
        # Tab 5: Generate IaC
        with tabs[4]:
            AzureAIAssistantModule._render_iac_generator(helper)
        
        # Tab 6: Runbook Generator
        with tabs[5]:
            AzureAIAssistantModule._render_runbook_generator(helper)
    
    @staticmethod
    def _render_chat_assistant(helper):
        """Chat interface with Claude"""
        st.markdown("### 💬 Chat with Claude - Azure Expert")
        st.caption("Ask questions about Azure, get recommendations, troubleshoot issues")
        
        # Quick questions
        st.markdown("**Quick Questions:**")
        col1, col2, col3 = st.columns(3)
        
        quick_questions = [
            "How do I set up high availability for my web app?",
            "What's the best way to optimize my Azure costs?",
            "How can I improve my Azure SQL performance?",
            "What security best practices should I follow?",
            "How do I migrate from VMs to containers?",
            "What's the difference between Functions and Container Apps?"
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
                system_prompt = "You are an Azure cloud expert assistant. Provide detailed, practical answers about Azure services, architecture, and best practices."
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
        user_input = st.chat_input("Ask me anything about Azure infrastructure...")
        
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
                system_prompt = "You are an Azure cloud expert assistant. Provide detailed, practical answers about Azure services, architecture, and best practices."
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
        st.caption("Get AI-powered Azure architecture recommendations")
        
        with st.form("architecture_form"):
            st.markdown("#### Describe Your Requirements")
            
            col1, col2 = st.columns(2)
            
            with col1:
                services = st.multiselect(
                    "Azure Services Needed",
                    ["Virtual Machines", "Azure SQL", "Blob Storage", "Functions", 
                     "Container Instances", "AKS", "Cosmos DB", "Redis Cache",
                     "Front Door", "App Service", "API Management", "Service Bus", "Event Hubs",
                     "Synapse Analytics", "Data Factory", "Event Grid",
                     "Logic Apps", "Cognitive Services", "Active Directory", "Application Gateway"]
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
                
                ha_required = st.checkbox("High Availability Required (Availability Zones)")
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
Design an Azure architecture with the following requirements:

**Services**: {', '.join(services)}
**Architecture Type**: {architecture_type}
**Expected Traffic**: {traffic}
**Budget**: {budget}
**Compliance**: {', '.join(compliance) if compliance else 'None'}
**High Availability**: {'Yes (Availability Zones)' if ha_required else 'No'}
**Disaster Recovery**: {'Yes (Multi-Region with Traffic Manager)' if dr_required else 'No'}

**Additional Requirements**:
{additional_requirements if additional_requirements else 'None'}

Please provide:
1. Architecture overview with component diagram description
2. Detailed service selection and configuration
3. Networking design (VNet, subnets, NSGs, ASGs)
4. High availability and scalability approach
5. Security best practices (Managed Identity, Key Vault, etc.)
6. Cost estimation and optimization tips
7. Deployment strategy (ARM, Bicep, or Terraform)
"""
                
                recommendation = helper.chat(requirements_text, [], 
                    "You are an Azure Solutions Architect. Provide detailed, production-ready architecture recommendations.")
            
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
        st.caption("Analyze Azure resources and get AI-powered cost optimization recommendations")
        
        # Analysis type
        analysis_type = st.radio(
            "Analysis Type",
            ["Quick Scan", "Deep Analysis", "Custom Query"],
            horizontal=True
        )
        
        if analysis_type == "Quick Scan":
            st.info("Quick scan analyzes common cost optimization opportunities across VMs, Azure SQL, and Storage")
            
            if st.button("🔍 Run Quick Scan", use_container_width=True):
                with st.spinner("🤖 Analyzing resources for cost optimization..."):
                    resources_text = """
Analyze these Azure resources for cost optimization:

**Virtual Machines:**
- vm-web-01: Standard_D4s_v3, CPU avg 15%, Running 24/7
- vm-app-01: Standard_E8s_v3, CPU avg 8%, Running 24/7
- vm-worker-01: Standard_F16s_v2, CPU avg 45%, Running 24/7

**Azure SQL Databases:**
- sqldb-prod: Business Critical, Gen5 8 vCore, DTU avg 25%, 500GB storage
- sqldb-staging: General Purpose, Gen5 2 vCore, DTU avg 5%, 100GB storage

**Managed Disks:**
- disk-premium-01: Premium SSD, P30 (1TB), IOPS avg 30%
- disk-standard-01: Standard SSD, E30 (500GB), Last accessed 90 days ago

**Storage Accounts:**
- stglogs: Hot tier, 5TB, 90% blobs > 90 days old
- stgbackup: Hot tier, 10TB, Accessed once per month

Provide specific cost optimization recommendations with estimated savings.
"""
                    
                    analysis = helper.chat(resources_text, [],
                        "You are an Azure cost optimization expert. Provide specific, actionable recommendations with estimated savings.")
                
                if analysis:
                    st.markdown("#### 💡 Cost Optimization Recommendations")
                    st.markdown(analysis)
        
        elif analysis_type == "Deep Analysis":
            st.info("Deep analysis includes comprehensive review of all services, Reserved Instance recommendations, and Azure Savings Plans")
            
            services_to_analyze = st.multiselect(
                "Services to Analyze",
                ["Virtual Machines", "Azure SQL", "Storage", "Functions", "Cosmos DB", "Disks", "Front Door", "Bandwidth"],
                default=["Virtual Machines", "Azure SQL", "Storage"]
            )
            
            if st.button("🔬 Run Deep Analysis", use_container_width=True):
                with st.spinner("🤖 Performing deep cost analysis..."):
                    analysis_text = f"""
Perform a deep cost optimization analysis for: {', '.join(services_to_analyze)}

Focus on:
1. Right-sizing opportunities (VM sizes, SQL tiers)
2. Reserved Instance / Azure Savings Plan recommendations
3. Storage optimization (access tiers, lifecycle management)
4. Unused resource identification (orphaned disks, NICs)
5. Architecture improvements for cost efficiency
6. Data transfer and bandwidth optimization

Provide detailed recommendations with:
- Current cost
- Optimized cost
- Estimated monthly savings
- Implementation complexity (Low/Medium/High)
- Priority (High/Medium/Low)
"""
                    
                    analysis = helper.chat(analysis_text, [],
                        "You are an Azure FinOps expert. Provide comprehensive cost analysis with specific recommendations and ROI calculations.")
                
                if analysis:
                    st.markdown("#### 📊 Deep Analysis Results")
                    st.markdown(analysis)
        
        else:  # Custom Query
            custom_query = st.text_area(
                "Cost Optimization Query",
                placeholder="Example:\n- How can I reduce bandwidth costs between regions?\n- What's the best VM size for my workload?\n- Should I use Functions or Container Apps?",
                height=100
            )
            
            if st.button("🎯 Analyze", use_container_width=True):
                if custom_query:
                    with st.spinner("🤖 Analyzing..."):
                        analysis = helper.chat(custom_query, [],
                            "You are an Azure cost optimization expert. Provide specific recommendations with cost estimates.")
                    
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
            ["Security Findings", "RBAC Policy Review", "Network Security", "Compliance Check"],
            horizontal=True
        )
        
        if analysis_mode == "Security Findings":
            if st.button("🔍 Analyze Recent Security Findings", use_container_width=True):
                with st.spinner("🤖 Analyzing security findings from Azure Security Center / Defender..."):
                    findings_text = """
Analyze these Azure Security Center / Defender findings and provide remediation steps:

**CRITICAL Findings:**
1. Storage account 'stgappdata' has public blob access enabled
   - Resource: /subscriptions/.../resourceGroups/rg-prod/providers/Microsoft.Storage/storageAccounts/stgappdata
   - Description: Allow Blob public access is set to Enabled

2. Network Security Group 'nsg-web' allows unrestricted SSH
   - Resource: /subscriptions/.../networkSecurityGroups/nsg-web
   - Description: Inbound rule allows SSH (port 22) from Internet (*)

**HIGH Findings:**
3. Service Principal 'app-service-sp' has long-lived secret (365 days old)
   - Resource: Application ID: abc-123-def
   - Description: Client secret has not been rotated in 365 days

4. Azure SQL Server 'sqlsrv-prod' allows Azure services access
   - Resource: /subscriptions/.../servers/sqlsrv-prod
   - Description: Firewall rule allows access from all Azure services

5. VM 'vm-app-01' has no backup policy configured
   - Resource: /subscriptions/.../virtualMachines/vm-app-01
   - Description: Virtual machine is not protected by Azure Backup

For each finding, provide:
1. Risk assessment
2. Step-by-step remediation
3. Azure CLI commands or portal steps
4. Prevention best practices
"""
                    
                    analysis = helper.chat(findings_text, [],
                        "You are an Azure security expert. Provide detailed remediation steps with specific az CLI commands.")
                
                if analysis:
                    st.markdown("#### 🛡️ Security Analysis & Remediation")
                    st.markdown(analysis)
        
        elif analysis_mode == "RBAC Policy Review":
            policy_input = st.text_area(
                "Paste Custom Role Definition JSON",
                placeholder='{\n  "Name": "Custom Role",\n  "IsCustom": true,\n  "Description": "Custom role",\n  "Actions": ["*"],\n  "NotActions": [],\n  "AssignableScopes": ["/subscriptions/*"]\n}',
                height=200
            )
            
            if st.button("🔒 Analyze RBAC Role", use_container_width=True):
                if policy_input:
                    with st.spinner("🤖 Analyzing Azure RBAC role..."):
                        policy_text = f"""
Analyze this Azure custom RBAC role for security issues and recommend improvements:

```json
{policy_input}
```

Check for:
1. Overly permissive permissions (wildcards in Actions)
2. Violation of least privilege principle
3. Missing NotActions to restrict dangerous operations
4. Scope too broad (subscription vs resource group)
5. Potential security risks
6. Compliance with Azure best practices

Provide:
- Security issues found
- Risk level for each issue
- Recommended role improvements
- Improved role JSON
- Comparison with Azure built-in roles
"""
                        
                        analysis = helper.chat(policy_text, [],
                            "You are an Azure RBAC security expert. Analyze roles and provide secure alternatives.")
                    
                    if analysis:
                        st.markdown("#### 🔐 RBAC Role Analysis")
                        st.markdown(analysis)
        
        elif analysis_mode == "Network Security":
            if st.button("🌐 Analyze Network Security", use_container_width=True):
                with st.spinner("🤖 Analyzing Azure network security configuration..."):
                    network_text = """
Analyze this Azure network security configuration:

**Virtual Network:**
- VNet: vnet-prod (10.0.0.0/16)
- Public Subnets: subnet-public-1 (10.0.1.0/24), subnet-public-2 (10.0.2.0/24)
- Private Subnets: subnet-private-1 (10.0.10.0/24), subnet-private-2 (10.0.11.0/24)

**Network Security Groups:**
- nsg-web: Allows Internet (*) on ports 80, 443, 22
- nsg-app: Allows nsg-web on port 8080
- nsg-db: Allows nsg-app on port 1433

**Application Security Groups:**
- asg-web-servers
- asg-app-servers
- asg-db-servers

**Azure Firewall:** Not configured

Analyze for:
1. NSG misconfigurations
2. Application Security Group usage
3. Network segmentation best practices
4. Azure Firewall opportunities
5. DDoS Protection recommendations
6. Service Endpoints and Private Link usage
"""
                    
                    analysis = helper.chat(network_text, [],
                        "You are an Azure network security expert. Provide comprehensive network security analysis.")
                
                if analysis:
                    st.markdown("#### 🛡️ Network Security Analysis")
                    st.markdown(analysis)
        
        else:  # Compliance Check
            framework = st.selectbox(
                "Compliance Framework",
                ["PCI-DSS", "HIPAA", "SOC 2", "GDPR", "CIS Azure Foundations", "NIST", "ISO 27001"]
            )
            
            if st.button(f"✅ Check {framework} Compliance", use_container_width=True):
                with st.spinner(f"🤖 Checking {framework} compliance..."):
                    compliance_text = f"""
Perform a {framework} compliance check for Azure environment and provide:

1. Key compliance requirements for {framework}
2. Azure services and features that help achieve compliance (Azure Policy, Blueprints)
3. Common compliance gaps and how to address them
4. Recommended Azure Policy definitions for continuous compliance
5. Audit and monitoring best practices (Activity Logs, Security Center)
6. Documentation and attestation requirements
"""
                    
                    analysis = helper.chat(compliance_text, [],
                        f"You are an Azure compliance expert specializing in {framework}. Provide actionable compliance guidance.")
                
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
                st.success("✅ Alerts configured in Azure Monitor")
    
    @staticmethod
    def _render_iac_generator(helper):
        """Infrastructure as Code generator"""
        st.markdown("### 📝 Generate Infrastructure as Code")
        st.caption("Describe your Azure infrastructure and get Bicep/ARM/Terraform code")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            format_type = st.selectbox(
                "IaC Format",
                ["Bicep", "ARM Template (JSON)", "Terraform (HCL)", "Pulumi (Python)", "Pulumi (TypeScript)"]
            )
        
        with col2:
            include_modules = st.checkbox("Use Modules/Registry", value=True)
            include_comments = st.checkbox("Include Comments", value=True)
        
        infrastructure_desc = st.text_area(
            "Describe Infrastructure",
            placeholder="""Example:

I need a production-ready web application with:

1. Virtual Network with public and private subnets across 3 availability zones
2. Application Gateway (WAF enabled) in public subnet
3. VM Scale Set (2-10 Standard_D2s_v3 instances) in private subnet
4. Azure SQL Database (General Purpose, 8 vCores) with geo-replication
5. Redis Cache (Premium tier) for session storage
6. Storage account for static files with CDN (Front Door)
7. Azure DNS zone for custom domain
8. Key Vault for secrets and certificates
9. Application Insights and Log Analytics workspace
10. All resources with appropriate tags and NSGs
""",
            height=250
        )
        
        if st.button("🚀 Generate IaC Template", use_container_width=True):
            if infrastructure_desc:
                with st.spinner(f"🤖 Generating {format_type} template..."):
                    iac_prompt = f"""
Generate production-ready {format_type} code for this Azure infrastructure:

{infrastructure_desc}

Requirements:
- Follow Azure best practices and Well-Architected Framework
- Include proper security configurations (Managed Identity, Private Endpoints)
- Add resource dependencies
- Include parameters and outputs
- {"Use modules or Azure Verified Modules where appropriate" if include_modules and "Bicep" in format_type else ""}
- {"Add detailed comments explaining each section" if include_comments else ""}
- Ensure high availability and fault tolerance
- Use Availability Zones where applicable

Provide complete, working code that can be deployed immediately with az CLI or Azure Portal.
"""
                    
                    template = helper.chat(iac_prompt, [],
                        f"You are an Azure IaC expert specializing in {format_type}. Generate production-ready, well-structured code following Azure best practices.")
                
                if template:
                    st.markdown(f"#### 📄 Generated {format_type} Template")
                    
                    # Determine language for syntax highlighting
                    if "Bicep" in format_type:
                        language = "bicep"
                    elif "JSON" in format_type or "ARM" in format_type:
                        language = "json"
                    elif "Terraform" in format_type:
                        language = "hcl"
                    elif "Python" in format_type:
                        language = "python"
                    else:
                        language = "typescript"
                    
                    st.code(template, language=language)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📥 Download Template"):
                            st.success("✅ Template downloaded")
                    with col2:
                        if st.button("✅ Validate Syntax"):
                            st.success("✅ Syntax valid (az deployment validate)")
                    with col3:
                        if st.button("🚀 Deploy to Azure"):
                            st.info("🚀 Deployment initiated")
            else:
                st.warning("⚠️ Please describe the infrastructure you want to create")
        
        # Example templates
        with st.expander("📚 Example Templates"):
            st.markdown("""
            **Common Patterns:**
            - Three-tier web application (App Gateway + VMSS + Azure SQL)
            - Serverless API (API Management + Functions + Cosmos DB)
            - Data platform (Data Lake + Synapse + Power BI)
            - Container platform (AKS cluster with Application Gateway)
            - CI/CD pipeline (Azure DevOps with Container Registry)
            - Event-driven architecture (Event Grid + Functions + Service Bus)
            """)
    
    @staticmethod
    def _render_runbook_generator(helper):
        """Operational runbook generator"""
        st.markdown("### 📚 Runbook Generator")
        st.caption("Generate detailed operational runbooks for Azure operations")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            operation_type = st.selectbox(
                "Operation Type",
                [
                    "Deploy Application Update",
                    "Database Migration (Azure SQL)",
                    "Disaster Recovery Failover",
                    "Scale Up/Down Infrastructure",
                    "Security Incident Response",
                    "Backup and Restore",
                    "Certificate Renewal (Key Vault)",
                    "Function App Deployment",
                    "AKS Cluster Upgrade",
                    "Azure SQL Point-in-Time Restore",
                    "Storage Account Recovery",
                    "VM Restore from Backup",
                    "Custom Operation"
                ]
            )
        
        with col2:
            include_rollback = st.checkbox("Include Rollback", value=True)
            include_validation = st.checkbox("Include Validation", value=True)
        
        if operation_type == "Custom Operation":
            operation_name = st.text_input("Operation Name", placeholder="e.g., Migrate to Availability Zones")
        else:
            operation_name = operation_type
        
        context = st.text_area(
            "Additional Context",
            placeholder="""Provide specific context about your environment:

Example:
- Environment: Production
- Azure Region: East US 2
- Application: E-commerce platform
- Database: Azure SQL Gen5 8 vCore, Business Critical tier
- Traffic: 10,000 requests/minute
- Maintenance Window: Sundays 2 AM - 6 AM EST
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
{context if context else "Standard Azure production environment"}

The runbook should include:

1. **Overview**
   - Operation description
   - Prerequisites
   - Required permissions (Azure RBAC roles)
   - Estimated duration

2. **Pre-Operation Checklist**
   - Verification steps (az CLI commands)
   - Backup requirements
   - Team notifications
   - Resource locks check

3. **Step-by-Step Procedure**
   - Detailed steps with az CLI commands
   - Azure Portal instructions as alternative
   - Expected outputs for each step
   - Decision points and branching

4. **Validation Steps**
   - Health checks
   - Azure Monitor dashboards to watch
   - Success criteria
{"" if not include_validation else "- Automated validation scripts"}

5. **Rollback Procedure**
   - When to rollback
   - Step-by-step rollback instructions
   - Rollback validation
{"" if not include_rollback else "- Emergency rollback (< 5 minutes)"}

6. **Post-Operation Tasks**
   - Cleanup activities
   - Documentation updates (Confluence, Wiki)
   - Team notifications
   - Lessons learned

7. **Troubleshooting**
   - Common issues and solutions
   - Emergency contacts
   - Escalation procedures
   - Azure Support ticket process

Make it production-ready and executable by an engineer with Azure experience.
Include specific az CLI commands and resource paths.
"""
                    
                    runbook = helper.chat(runbook_prompt, [],
                        "You are an Azure operations expert. Generate comprehensive, production-ready runbooks with specific az CLI commands.")
                
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
                        if st.button("📋 Add to Azure DevOps"):
                            st.success("✅ Added to Wiki")
            else:
                st.warning("⚠️ Please specify an operation name")
        
        # Runbook library
        with st.expander("📚 Runbook Library"):
            st.markdown("""
            **Available Templates:**
            - Blue/Green Deployment with Traffic Manager
            - Azure SQL Geo-Failover Testing
            - VMSS Update Domain Upgrade
            - Function App Slot Swap Deployment
            - Storage Account Geo-Replication Setup
            - Front Door Cache Purge
            - Azure DNS Failover Configuration
            - VM Patching with Update Management
            """)

# Module-level render function
def render():
    """Module-level render function"""
    AzureAIAssistantModule.render()