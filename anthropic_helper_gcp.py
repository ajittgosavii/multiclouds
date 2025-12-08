"""
GCP-Specific Anthropic Helper
AI assistance tailored for Google Cloud Platform services, architecture, and best practices
"""

from typing import Any, Dict, List, Optional
import streamlit as st
import json

class GCPAnthropicHelper:
    """GCP-specific AI helper with Claude integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize GCP AI helper"""
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
        """GCP-focused chat with Claude"""
        if not self.client:
            return "⚠️ AI features not available. Please configure ANTHROPIC_API_KEY."
        
        # Default GCP-specific system prompt
        if not system_prompt:
            system_prompt = """You are a Google Cloud Platform (GCP) Solutions Architect Expert with deep knowledge of:
- Google Cloud Architecture Framework
- GCP service catalog and best practices
- Infrastructure as Code (Deployment Manager, Terraform)
- GCP security (Cloud IAM, Cloud KMS, Security Command Center)
- Cost optimization with Cloud Billing and Recommender
- High availability with zones, regions, and load balancing
- gcloud CLI, Cloud SDK, and client libraries
- Cloud Build, Cloud Deploy, and CI/CD integration

Provide practical, production-ready guidance specific to GCP services and patterns."""

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
            
            # Call Claude API with GCP-specific system prompt
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
        """Generate GCP-specific architecture recommendation"""
        if not self.client:
            return "⚠️ AI features not available."
        
        prompt = f"""As a GCP Solutions Architect, design a production-ready architecture using Google Cloud services:

**Requirements:**
- Services needed: {', '.join(requirements.get('services', []))}
- Traffic: {requirements.get('traffic', 'Unknown')}
- Compliance: {', '.join(requirements.get('compliance', []))}
- Budget: {requirements.get('budget', 'Unknown')}
- High Availability: {'Yes' if requirements.get('ha_required') else 'No'}
- Additional: {requirements.get('additional', 'None')}

**Provide:**
1. GCP service selection with justification
2. Architecture diagram description (using GCP services)
3. Multi-zone and multi-region design
4. Security architecture (Cloud IAM, VPC, Cloud Armor, KMS)
5. Cost breakdown using GCP Pricing Calculator
6. Scalability strategy (Managed Instance Groups, GKE autoscaling)
7. Monitoring (Cloud Monitoring, Cloud Logging, Cloud Trace)
8. Disaster recovery and backup strategies
9. Implementation roadmap with Deployment Manager/Terraform
10. Google Cloud Architecture Framework alignment
"""
        
        return self.chat(prompt)
    
    def analyze_cost_optimization(self, resources: List[Dict]) -> str:
        """Analyze GCP resources for cost optimization"""
        if not self.client:
            return "⚠️ AI features not available."
        
        resources_str = json.dumps(resources, indent=2)
        prompt = f"""As a GCP cost optimization expert, analyze these resources:

{resources_str}

**For each resource provide:**
1. Current GCP pricing estimate
2. Utilization metrics from Cloud Monitoring
3. Right-sizing recommendations (machine types, Cloud SQL tiers)
4. GCP pricing model optimization (Committed Use Discounts, Preemptible VMs)
5. Alternative GCP services (Compute Engine → Cloud Run, Cloud Functions)
6. Storage optimization (Nearline, Coldline, Archive classes)
7. Monthly savings potential in USD
8. Implementation steps (gcloud CLI/Console)
9. Risk assessment and downtime requirements
10. Active Assist and Recommender insights
"""
        
        return self.chat(prompt)
    
    def analyze_security_findings(self, findings: List[Dict]) -> str:
        """Analyze GCP security findings"""
        if not self.client:
            return "⚠️ AI features not available."
        
        findings_str = json.dumps(findings, indent=2)
        prompt = f"""As a GCP security expert, analyze these findings:

{findings_str}

**For each finding provide:**
1. GCP security impact assessment
2. Related GCP services and configurations
3. Step-by-step remediation (gcloud CLI/Console)
4. Cloud IAM policy recommendations
5. VPC firewall rules and Cloud Armor fixes
6. Organization Policy constraints to prevent recurrence
7. Compliance mapping (ISO 27001, PCI DSS, HIPAA)
8. Security Command Center integration
9. Cloud Audit Logs and logging recommendations
10. Cost impact of remediation
"""
        
        return self.chat(prompt)
    
    def generate_iac_template(self, infrastructure: Dict, format_type: str) -> str:
        """Generate GCP IaC template (Deployment Manager, Terraform)"""
        if not self.client:
            return "⚠️ AI features not available."
        
        desc = infrastructure.get('description', '')
        
        # Map format types to GCP-specific
        format_mapping = {
            'deployment_manager': 'Google Cloud Deployment Manager YAML',
            'terraform': 'Terraform for GCP',
            'gcloud': 'gcloud CLI script',
            'python': 'GCP Client Libraries (Python)'
        }
        
        format_name = format_mapping.get(format_type.lower(), format_type)
        
        prompt = f"""Generate production-ready {format_name} code:

{desc}

**Requirements:**
1. Use GCP best practices and naming conventions
2. Include all necessary GCP resources
3. Implement GCP security best practices
4. Add comprehensive labeling strategy
5. Include properties/variables for flexibility
6. Add outputs for resource references
7. Use service accounts with minimal permissions
8. Include Cloud Monitoring and Logging
9. Add comments explaining GCP-specific configurations
10. Make it ready for GCP deployment

Generate ONLY the code, no explanations."""
        
        return self.chat(prompt)
    
    def generate_runbook(self, operation: str, context: Dict) -> str:
        """Generate GCP-specific operational runbook"""
        if not self.client:
            return "⚠️ AI features not available."
        
        context_str = context.get('context', 'Standard GCP environment')
        prompt = f"""Generate a detailed GCP operational runbook for: {operation}

Context: {context_str}

**Include:**
1. **Overview** - Purpose and GCP services involved
2. **Prerequisites** - Cloud IAM roles, gcloud SDK setup
3. **Pre-flight Checks** - GCP service status, quota limits
4. **Step-by-Step Procedures** - Cloud Console and gcloud commands
5. **Validation** - Cloud Monitoring metrics, Log Explorer queries
6. **Rollback** - GCP-specific rollback procedures
7. **Troubleshooting** - Common GCP issues and solutions
8. **Communication** - Pub/Sub and Cloud Functions notifications
9. **Post-operation** - Audit Logs review, cost impact
10. **Automation** - Cloud Functions, Cloud Scheduler, Workflows

Use gcloud commands and GCP Console navigation steps.
"""
        
        return self.chat(prompt)
    
    def is_available(self) -> bool:
        """Check if AI features are available"""
        return self.client is not None


@st.cache_resource
def get_gcp_anthropic_helper() -> GCPAnthropicHelper:
    """Get cached GCP AI helper instance"""
    return GCPAnthropicHelper()
