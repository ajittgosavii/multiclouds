"""
Azure-Specific Anthropic Helper
AI assistance tailored for Azure services, architecture, and best practices
"""

from typing import Any, Dict, List, Optional
import streamlit as st
import json

class AzureAnthropicHelper:
    """Azure-specific AI helper with Claude integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Azure AI helper"""
        self.api_key = api_key or self._get_api_key()
        self.client = None
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                st.warning("⚠️ Anthropic library not installed. Run: pip install anthropic")
            except Exception as e:
                st.warning(f"⚠️ Could not initialize Anthropic client: {str(e)}")
    
    @staticmethod
    def _get_api_key() -> Optional[str]:
        """Get API key from secrets or environment"""
        if hasattr(st, 'secrets'):
            try:
                if 'anthropic' in st.secrets and 'api_key' in st.secrets['anthropic']:
                    return st.secrets['anthropic']['api_key']
                elif 'ANTHROPIC_API_KEY' in st.secrets:
                    return st.secrets['ANTHROPIC_API_KEY']
            except Exception:
                pass
        
        import os
        return os.getenv('ANTHROPIC_API_KEY')
    
    def chat(self, prompt: str, context: Optional[Any] = None, system_prompt: Optional[str] = None) -> str:
        """Azure-focused chat with Claude"""
        if not self.client:
            return "⚠️ AI features not available. Please configure ANTHROPIC_API_KEY."
        
        # Default Azure-specific system prompt
        if not system_prompt:
            system_prompt = """You are an Azure Solutions Architect Expert with deep knowledge of:
- Azure Well-Architected Framework (all 5 pillars)
- Azure service catalog and best practices
- Infrastructure as Code (ARM templates, Bicep, Terraform)
- Azure security and compliance (Azure AD, Key Vault, Security Center)
- Cost optimization with Azure Advisor and Cost Management
- High availability with Availability Zones and Azure Site Recovery
- Azure CLI, PowerShell, and Azure SDKs
- Azure DevOps and GitHub Actions integration

Provide practical, production-ready guidance specific to Azure services and patterns."""

        try:
            # Build context
            if context:
                if isinstance(context, str):
                    full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
                elif isinstance(context, list):
                    context_str = "\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in context])
                    full_prompt = f"Previous conversation:\n{context_str}\n\nUser: {prompt}"
                elif isinstance(context, dict):
                    context_str = json.dumps(context, indent=2)
                    full_prompt = f"Context:\n{context_str}\n\nQuestion: {prompt}"
                else:
                    full_prompt = prompt
            else:
                full_prompt = prompt
            
            # Call Claude API with Azure-specific system prompt
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            response_text = ""
            for content_block in message.content:
                if hasattr(content_block, 'text'):
                    response_text += content_block.text
            
            return response_text
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate_architecture_recommendation(self, requirements: Dict) -> str:
        """Generate Azure-specific architecture recommendation"""
        if not self.client:
            return "⚠️ AI features not available."
        
        prompt = f"""As an Azure Solutions Architect, design a production-ready architecture using Azure services:

**Requirements:**
- Services needed: {', '.join(requirements.get('services', []))}
- Traffic: {requirements.get('traffic', 'Unknown')}
- Compliance: {', '.join(requirements.get('compliance', []))}
- Budget: {requirements.get('budget', 'Unknown')}
- High Availability: {'Yes' if requirements.get('ha_required') else 'No'}
- Additional: {requirements.get('additional', 'None')}

**Provide:**
1. Azure service selection with justification
2. Architecture diagram description (using Azure services)
3. Availability Zones and region pairs design
4. Security architecture (Azure AD, RBAC, Key Vault, NSGs)
5. Cost breakdown using Azure Pricing Calculator
6. Scalability strategy (VMSS, App Service scaling, AKS)
7. Monitoring (Azure Monitor, Log Analytics, Application Insights)
8. Disaster recovery with Azure Site Recovery
9. Implementation roadmap with ARM/Bicep templates
10. Azure Well-Architected Framework alignment
"""
        
        return self.chat(prompt)
    
    def analyze_cost_optimization(self, resources: List[Dict]) -> str:
        """Analyze Azure resources for cost optimization"""
        if not self.client:
            return "⚠️ AI features not available."
        
        resources_str = json.dumps(resources, indent=2)
        prompt = f"""As an Azure cost optimization expert, analyze these resources:

{resources_str}

**For each resource provide:**
1. Current Azure pricing estimate
2. Utilization metrics from Azure Monitor
3. Right-sizing recommendations (VM sizes, SQL tiers)
4. Azure pricing model optimization (Reserved Instances, Spot VMs)
5. Alternative Azure services (VMs → Container Instances, Azure Functions)
6. Storage optimization (Hot/Cool/Archive tiers, managed disks)
7. Monthly savings potential in USD
8. Implementation steps (Azure CLI/PowerShell/Portal)
9. Risk assessment and downtime requirements
10. Azure Advisor and Cost Management insights
"""
        
        return self.chat(prompt)
    
    def analyze_security_findings(self, findings: List[Dict]) -> str:
        """Analyze Azure security findings"""
        if not self.client:
            return "⚠️ AI features not available."
        
        findings_str = json.dumps(findings, indent=2)
        prompt = f"""As an Azure security expert, analyze these findings:

{findings_str}

**For each finding provide:**
1. Azure security impact assessment
2. Related Azure services and configurations
3. Step-by-step remediation (Azure CLI/PowerShell/Portal)
4. Azure AD and RBAC recommendations
5. Network Security Group and firewall fixes
6. Azure Policy definitions to prevent recurrence
7. Compliance mapping (ISO 27001, GDPR, HIPAA)
8. Azure Security Center/Defender integration
9. Azure Activity Log and diagnostic settings
10. Cost impact of remediation
"""
        
        return self.chat(prompt)
    
    def generate_iac_template(self, infrastructure: Dict, format_type: str) -> str:
        """Generate Azure IaC template (ARM, Bicep, Terraform)"""
        if not self.client:
            return "⚠️ AI features not available."
        
        desc = infrastructure.get('description', '')
        
        # Map format types to Azure-specific
        format_mapping = {
            'arm': 'Azure Resource Manager (ARM) JSON',
            'bicep': 'Azure Bicep',
            'terraform': 'Terraform for Azure',
            'powershell': 'Azure PowerShell script'
        }
        
        format_name = format_mapping.get(format_type.lower(), format_type)
        
        prompt = f"""Generate production-ready {format_name} code:

{desc}

**Requirements:**
1. Use Azure best practices and naming conventions
2. Include all necessary Azure resources
3. Implement Azure security best practices
4. Add comprehensive tagging strategy
5. Include Parameters for flexibility
6. Add Outputs for resource references
7. Use Azure managed identities where appropriate
8. Include Azure Monitor diagnostic settings
9. Add comments explaining Azure-specific configurations
10. Make it ready for Azure deployment

Generate ONLY the code, no explanations."""
        
        return self.chat(prompt)
    
    def generate_runbook(self, operation: str, context: Dict) -> str:
        """Generate Azure-specific operational runbook"""
        if not self.client:
            return "⚠️ AI features not available."
        
        context_str = context.get('context', 'Standard Azure environment')
        prompt = f"""Generate a detailed Azure operational runbook for: {operation}

Context: {context_str}

**Include:**
1. **Overview** - Purpose and Azure services involved
2. **Prerequisites** - Azure RBAC permissions, CLI/PowerShell setup
3. **Pre-flight Checks** - Azure service health, subscription limits
4. **Step-by-Step Procedures** - Azure Portal, CLI, and PowerShell commands
5. **Validation** - Azure Monitor metrics, Log Analytics queries
6. **Rollback** - Azure-specific rollback procedures
7. **Troubleshooting** - Common Azure issues and solutions
8. **Communication** - Event Grid and Logic Apps notifications
9. **Post-operation** - Activity Log review, cost impact
10. **Automation** - Azure Automation, Logic Apps, or Functions

Use Azure CLI, PowerShell, and Azure Portal navigation steps.
"""
        
        return self.chat(prompt)
    
    def is_available(self) -> bool:
        """Check if AI features are available"""
        return self.client is not None


@st.cache_resource
def get_azure_anthropic_helper() -> AzureAnthropicHelper:
    """Get cached Azure AI helper instance"""
    return AzureAnthropicHelper()
