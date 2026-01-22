"""
Harness IO CI/CD Integration Module for Multi-Cloud IDP Platform
================================================================
Enterprise-grade CI/CD orchestration using Harness IO for multi-account AWS environments.

Features:
- Multi-account pipeline management (640+ accounts support)
- Portfolio-centric deployment strategies
- GitOps integration with Harness
- Service catalog management
- Environment promotion workflows
- Approval gates and governance
- Cost tracking per deployment
- AI-assisted pipeline optimization

Author: Ajit (Infosys)
Version: 1.0.0
"""

import streamlit as st
import json
import yaml
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import hashlib


# =============================================================================
# CONFIGURATION & ENUMS
# =============================================================================

class DeploymentStrategy(Enum):
    ROLLING = "Rolling"
    BLUE_GREEN = "Blue-Green"
    CANARY = "Canary"
    BASIC = "Basic"


class EnvironmentType(Enum):
    DEV = "Development"
    QA = "QA"
    STAGING = "Staging"
    UAT = "UAT"
    PROD = "Production"


class PipelineStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    RUNNING = "Running"
    PAUSED = "Paused"
    WAITING = "Waiting for Approval"
    QUEUED = "Queued"
    ABORTED = "Aborted"


class ApprovalStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    EXPIRED = "Expired"


@dataclass
class HarnessConfig:
    """Harness IO Configuration"""
    account_id: str = ""
    api_key: str = ""
    base_url: str = "https://app.harness.io"
    delegate_name: str = "platform-engineering-delegate"
    org_identifier: str = "default"
    
    
@dataclass
class Portfolio:
    """Portfolio/Business Unit Configuration"""
    name: str
    identifier: str
    aws_accounts: List[str]
    environments: List[str]
    approvers: List[str]
    cost_center: str
    compliance_frameworks: List[str] = field(default_factory=list)


@dataclass
class Pipeline:
    """Pipeline Definition"""
    name: str
    identifier: str
    portfolio: str
    stages: List[Dict]
    triggers: List[Dict]
    variables: Dict[str, Any]
    tags: Dict[str, str]
    

# =============================================================================
# HARNESS API CLIENT
# =============================================================================

class HarnessAPIClient:
    """
    Harness IO API Client for pipeline and deployment management
    """
    
    def __init__(self, config: HarnessConfig):
        self.config = config
        self.headers = {
            "x-api-key": config.api_key,
            "Content-Type": "application/json",
            "Harness-Account": config.account_id
        }
        self.base_url = f"{config.base_url}/gateway/pipeline/api"
        
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> Dict:
        """Make authenticated request to Harness API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def list_pipelines(self, org: str = None, project: str = None) -> List[Dict]:
        """List all pipelines in organization/project"""
        org = org or self.config.org_identifier
        endpoint = f"pipelines/list"
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project
        }
        return self._make_request("GET", endpoint, params)
    
    def get_pipeline(self, pipeline_id: str, org: str = None, project: str = None) -> Dict:
        """Get pipeline details"""
        org = org or self.config.org_identifier
        endpoint = f"pipelines/{pipeline_id}"
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project
        }
        return self._make_request("GET", endpoint, params)
    
    def execute_pipeline(self, pipeline_id: str, inputs: Dict, org: str = None, project: str = None) -> Dict:
        """Execute a pipeline with inputs"""
        org = org or self.config.org_identifier
        endpoint = f"pipeline/execute/{pipeline_id}"
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project
        }
        return self._make_request("POST", f"{endpoint}?{self._build_query(params)}", inputs)
    
    def get_execution(self, execution_id: str, org: str = None, project: str = None) -> Dict:
        """Get pipeline execution details"""
        org = org or self.config.org_identifier
        endpoint = f"pipeline/execution/{execution_id}"
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project
        }
        return self._make_request("GET", endpoint, params)
    
    def list_executions(self, pipeline_id: str = None, org: str = None, project: str = None, 
                        status: str = None, limit: int = 20) -> List[Dict]:
        """List pipeline executions"""
        org = org or self.config.org_identifier
        endpoint = "pipeline/execution/summary"
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project,
            "pipelineIdentifier": pipeline_id,
            "status": status,
            "size": limit
        }
        return self._make_request("GET", endpoint, {k: v for k, v in params.items() if v})
    
    def approve_stage(self, execution_id: str, stage_id: str, approved: bool, 
                      comments: str = "", org: str = None, project: str = None) -> Dict:
        """Approve or reject a pipeline stage"""
        org = org or self.config.org_identifier
        endpoint = f"pipeline/execution/{execution_id}/stages/{stage_id}/approval"
        data = {
            "action": "APPROVE" if approved else "REJECT",
            "comments": comments
        }
        params = {
            "accountIdentifier": self.config.account_id,
            "orgIdentifier": org,
            "projectIdentifier": project
        }
        return self._make_request("POST", f"{endpoint}?{self._build_query(params)}", data)
    
    def _build_query(self, params: Dict) -> str:
        """Build query string from params"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v])


# =============================================================================
# DEMO DATA GENERATOR
# =============================================================================

class HarnessDemoData:
    """
    Generate realistic demo data for Harness IO integration
    Simulates 640+ AWS accounts across multiple portfolios
    """
    
    PORTFOLIOS = [
        Portfolio(
            name="Digital Banking",
            identifier="digital_banking",
            aws_accounts=[f"111{i:09d}" for i in range(1, 101)],  # 100 accounts
            environments=["dev", "qa", "staging", "prod"],
            approvers=["tech-lead-banking@company.com", "release-manager@company.com"],
            cost_center="CC-BANKING-001",
            compliance_frameworks=["PCI-DSS", "SOX"]
        ),
        Portfolio(
            name="Insurance Platform",
            identifier="insurance_platform",
            aws_accounts=[f"222{i:09d}" for i in range(1, 151)],  # 150 accounts
            environments=["dev", "qa", "uat", "prod"],
            approvers=["tech-lead-insurance@company.com", "compliance@company.com"],
            cost_center="CC-INSURANCE-002",
            compliance_frameworks=["HIPAA", "SOX"]
        ),
        Portfolio(
            name="Wealth Management",
            identifier="wealth_mgmt",
            aws_accounts=[f"333{i:09d}" for i in range(1, 81)],  # 80 accounts
            environments=["dev", "staging", "prod"],
            approvers=["tech-lead-wealth@company.com"],
            cost_center="CC-WEALTH-003",
            compliance_frameworks=["SOX", "GDPR"]
        ),
        Portfolio(
            name="Core Infrastructure",
            identifier="core_infra",
            aws_accounts=[f"444{i:09d}" for i in range(1, 121)],  # 120 accounts
            environments=["dev", "staging", "prod"],
            approvers=["platform-lead@company.com", "sre-lead@company.com"],
            cost_center="CC-INFRA-004",
            compliance_frameworks=["SOC2", "ISO27001"]
        ),
        Portfolio(
            name="Data Analytics",
            identifier="data_analytics",
            aws_accounts=[f"555{i:09d}" for i in range(1, 91)],  # 90 accounts
            environments=["dev", "qa", "prod"],
            approvers=["data-lead@company.com"],
            cost_center="CC-DATA-005",
            compliance_frameworks=["GDPR", "CCPA"]
        ),
        Portfolio(
            name="Customer Experience",
            identifier="customer_exp",
            aws_accounts=[f"666{i:09d}" for i in range(1, 101)],  # 100 accounts
            environments=["dev", "qa", "staging", "prod"],
            approvers=["cx-lead@company.com", "product-owner@company.com"],
            cost_center="CC-CX-006",
            compliance_frameworks=["GDPR", "PCI-DSS"]
        ),
    ]
    
    SERVICES = [
        {"name": "api-gateway", "type": "Kubernetes", "language": "Java"},
        {"name": "payment-service", "type": "Kubernetes", "language": "Go"},
        {"name": "auth-service", "type": "Kubernetes", "language": "Python"},
        {"name": "notification-service", "type": "AWS Lambda", "language": "Node.js"},
        {"name": "data-processor", "type": "ECS", "language": "Python"},
        {"name": "web-frontend", "type": "S3/CloudFront", "language": "React"},
        {"name": "mobile-backend", "type": "Kubernetes", "language": "Kotlin"},
        {"name": "analytics-engine", "type": "EMR", "language": "Scala"},
        {"name": "ml-inference", "type": "SageMaker", "language": "Python"},
        {"name": "config-service", "type": "Kubernetes", "language": "Go"},
    ]
    
    @classmethod
    def get_portfolios(cls) -> List[Portfolio]:
        """Get all portfolios"""
        return cls.PORTFOLIOS
    
    @classmethod
    def get_total_accounts(cls) -> int:
        """Get total number of AWS accounts"""
        return sum(len(p.aws_accounts) for p in cls.PORTFOLIOS)
    
    @classmethod
    def generate_pipelines(cls, portfolio: Portfolio) -> List[Dict]:
        """Generate sample pipelines for a portfolio"""
        pipelines = []
        
        for svc in cls.SERVICES[:5]:  # 5 services per portfolio
            pipeline = {
                "identifier": f"{portfolio.identifier}_{svc['name'].replace('-', '_')}",
                "name": f"{portfolio.name} - {svc['name'].replace('-', ' ').title()}",
                "portfolio": portfolio.identifier,
                "service": svc["name"],
                "deployment_type": svc["type"],
                "language": svc["language"],
                "stages": cls._generate_stages(portfolio.environments),
                "last_execution": cls._generate_execution(),
                "executions_today": hash(svc["name"]) % 10 + 1,
                "success_rate": 85 + (hash(svc["name"]) % 15),
                "avg_duration_mins": 5 + (hash(svc["name"]) % 20),
                "tags": {
                    "portfolio": portfolio.identifier,
                    "cost_center": portfolio.cost_center,
                    "compliance": ",".join(portfolio.compliance_frameworks)
                }
            }
            pipelines.append(pipeline)
        
        return pipelines
    
    @classmethod
    def _generate_stages(cls, environments: List[str]) -> List[Dict]:
        """Generate pipeline stages based on environments"""
        stages = []
        stage_templates = {
            "dev": [
                {"name": "Build", "type": "CI", "duration": "3m"},
                {"name": "Unit Tests", "type": "CI", "duration": "5m"},
                {"name": "Deploy to Dev", "type": "CD", "duration": "4m"},
                {"name": "Integration Tests", "type": "Test", "duration": "8m"},
            ],
            "qa": [
                {"name": "Deploy to QA", "type": "CD", "duration": "4m"},
                {"name": "QA Approval", "type": "Approval", "duration": "0m"},
                {"name": "E2E Tests", "type": "Test", "duration": "15m"},
            ],
            "staging": [
                {"name": "Deploy to Staging", "type": "CD", "duration": "5m"},
                {"name": "Performance Tests", "type": "Test", "duration": "20m"},
                {"name": "Security Scan", "type": "Security", "duration": "10m"},
            ],
            "uat": [
                {"name": "UAT Approval", "type": "Approval", "duration": "0m"},
                {"name": "Deploy to UAT", "type": "CD", "duration": "5m"},
                {"name": "UAT Testing", "type": "Test", "duration": "30m"},
            ],
            "prod": [
                {"name": "Production Approval", "type": "Approval", "duration": "0m"},
                {"name": "Deploy to Production", "type": "CD", "duration": "10m"},
                {"name": "Smoke Tests", "type": "Test", "duration": "5m"},
                {"name": "Rollback Gate", "type": "Verification", "duration": "15m"},
            ]
        }
        
        for env in environments:
            if env in stage_templates:
                for stage in stage_templates[env]:
                    stages.append({
                        **stage,
                        "environment": env,
                        "status": "Success" if hash(stage["name"]) % 10 > 1 else "Running"
                    })
        
        return stages
    
    @classmethod
    def _generate_execution(cls) -> Dict:
        """Generate a sample execution record"""
        statuses = ["Success", "Success", "Success", "Running", "Failed", "Waiting for Approval"]
        status = statuses[hash(str(datetime.now())) % len(statuses)]
        
        return {
            "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12],
            "status": status,
            "started_at": (datetime.now() - timedelta(minutes=hash(str(datetime.now())) % 60)).isoformat(),
            "duration": f"{hash(str(datetime.now())) % 30 + 5}m",
            "triggered_by": "GitHub Webhook" if hash(str(datetime.now())) % 2 == 0 else "Manual",
            "commit": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:7],
            "branch": "main" if hash(str(datetime.now())) % 3 == 0 else "develop"
        }
    
    @classmethod
    def generate_executions(cls, count: int = 20) -> List[Dict]:
        """Generate sample execution history"""
        executions = []
        statuses = ["Success", "Success", "Success", "Success", "Failed", "Running"]
        triggers = ["GitHub Webhook", "Manual", "Scheduled", "API"]
        
        for i in range(count):
            started = datetime.now() - timedelta(hours=i*2 + hash(str(i)) % 5)
            duration = 10 + hash(str(i)) % 30
            
            executions.append({
                "id": hashlib.md5(f"exec_{i}".encode()).hexdigest()[:12],
                "pipeline": f"Pipeline-{(i % 5) + 1}",
                "portfolio": cls.PORTFOLIOS[i % len(cls.PORTFOLIOS)].name,
                "status": statuses[i % len(statuses)],
                "started_at": started.isoformat(),
                "ended_at": (started + timedelta(minutes=duration)).isoformat() if statuses[i % len(statuses)] != "Running" else None,
                "duration": f"{duration}m" if statuses[i % len(statuses)] != "Running" else "In Progress",
                "triggered_by": triggers[i % len(triggers)],
                "commit": hashlib.md5(f"commit_{i}".encode()).hexdigest()[:7],
                "branch": "main" if i % 3 == 0 else "develop",
                "environment": ["dev", "qa", "staging", "prod"][i % 4],
                "cost": round(0.05 + (hash(str(i)) % 100) / 100, 2)
            })
        
        return executions
    
    @classmethod
    def generate_approvals(cls, count: int = 10) -> List[Dict]:
        """Generate pending approvals"""
        approvals = []
        approval_types = ["Production Deployment", "UAT Release", "Security Exception", "Config Change"]
        
        for i in range(count):
            created = datetime.now() - timedelta(hours=hash(str(i)) % 48)
            
            approvals.append({
                "id": hashlib.md5(f"approval_{i}".encode()).hexdigest()[:12],
                "pipeline": f"Pipeline-{(i % 5) + 1}",
                "portfolio": cls.PORTFOLIOS[i % len(cls.PORTFOLIOS)].name,
                "type": approval_types[i % len(approval_types)],
                "environment": ["staging", "uat", "prod"][i % 3],
                "requested_by": f"developer{i+1}@company.com",
                "requested_at": created.isoformat(),
                "expires_at": (created + timedelta(hours=24)).isoformat(),
                "approvers": cls.PORTFOLIOS[i % len(cls.PORTFOLIOS)].approvers,
                "status": "Pending",
                "urgency": ["Normal", "High", "Critical"][i % 3],
                "changes": f"{(i+1)*3} files changed, {(i+1)*50} insertions, {(i+1)*10} deletions"
            })
        
        return approvals
    
    @classmethod
    def generate_metrics(cls) -> Dict:
        """Generate DORA and deployment metrics"""
        return {
            "dora": {
                "deployment_frequency": {
                    "value": 4.2,
                    "unit": "deploys/day",
                    "trend": "+12%",
                    "rating": "Elite"
                },
                "lead_time": {
                    "value": 2.3,
                    "unit": "hours",
                    "trend": "-18%",
                    "rating": "Elite"
                },
                "mttr": {
                    "value": 45,
                    "unit": "minutes",
                    "trend": "-25%",
                    "rating": "Elite"
                },
                "change_failure_rate": {
                    "value": 8.5,
                    "unit": "%",
                    "trend": "-3%",
                    "rating": "High"
                }
            },
            "deployments": {
                "today": 18,
                "this_week": 89,
                "this_month": 342,
                "success_rate": 94.2,
                "rollbacks": 3
            },
            "cost": {
                "today": 45.67,
                "this_week": 289.45,
                "this_month": 1234.56,
                "trend": "-5%",
                "by_portfolio": {
                    p.name: round(100 + hash(p.name) % 200, 2) 
                    for p in cls.PORTFOLIOS
                }
            }
        }


# =============================================================================
# HARNESS SERVICE TEMPLATES
# =============================================================================

class HarnessServiceTemplates:
    """
    Pre-built Harness service and pipeline templates
    """
    
    @staticmethod
    def generate_kubernetes_service(name: str, identifier: str, ecr_region: str,
                                    ecr_repo: str, connector_ref: str) -> str:
        """Generate Kubernetes service YAML"""
        return f"""
service:
  name: {name}
  identifier: {identifier}
  serviceDefinition:
    type: Kubernetes
    spec:
      manifests:
        - manifest:
            identifier: manifests
            type: K8sManifest
            spec:
              store:
                type: Git
                spec:
                  connectorRef: <+input>
                  gitFetchType: Branch
                  paths:
                    - k8s/
                  branch: main
      artifacts:
        primary:
          primaryArtifactRef: <+input>
          sources:
            - spec:
                connectorRef: {connector_ref}
                imagePath: {ecr_repo}
                tag: <+input>
                region: {ecr_region}
              identifier: ecr_artifact
              type: Ecr
"""

    @staticmethod
    def generate_lambda_service(name: str, identifier: str, s3_bucket: str,
                                function_name: str, runtime: str) -> str:
        """Generate AWS Lambda service YAML"""
        return f"""
service:
  name: {name}
  identifier: {identifier}
  serviceDefinition:
    type: ServerlessAwsLambda
    spec:
      manifests:
        - manifest:
            identifier: serverless_manifest
            type: ServerlessAwsLambda
            spec:
              store:
                type: Git
                spec:
                  connectorRef: <+input>
                  gitFetchType: Branch
                  paths:
                    - serverless.yml
                  branch: main
      artifacts:
        primary:
          primaryArtifactRef: <+input>
          sources:
            - spec:
                connectorRef: <+input>
                bucketName: {s3_bucket}
                filePath: deployments/{function_name}/<+input>.zip
                region: <+input>
              identifier: lambda_artifact
              type: AmazonS3
"""

    @staticmethod
    def generate_ecs_service(name: str, identifier: str, cluster: str,
                             ecr_repo: str, task_family: str) -> str:
        """Generate ECS service YAML"""
        return f"""
service:
  name: {name}
  identifier: {identifier}
  serviceDefinition:
    type: ECS
    spec:
      manifests:
        - manifest:
            identifier: task_definition
            type: EcsTaskDefinition
            spec:
              store:
                type: Git
                spec:
                  connectorRef: <+input>
                  gitFetchType: Branch
                  paths:
                    - ecs/task-definition.json
                  branch: main
        - manifest:
            identifier: service_definition
            type: EcsServiceDefinition
            spec:
              store:
                type: Git
                spec:
                  connectorRef: <+input>
                  gitFetchType: Branch
                  paths:
                    - ecs/service-definition.json
                  branch: main
      artifacts:
        primary:
          primaryArtifactRef: <+input>
          sources:
            - spec:
                connectorRef: <+input>
                imagePath: {ecr_repo}
                tag: <+input>
                region: <+input>
              identifier: ecr_artifact
              type: Ecr
"""

    @staticmethod
    def generate_multi_account_pipeline(name: str, identifier: str, portfolio: str,
                                        environments: List[str], strategy: str) -> str:
        """Generate multi-account deployment pipeline"""
        stages_yaml = ""
        
        for i, env in enumerate(environments):
            is_prod = env.lower() in ["prod", "production"]
            
            # Add approval stage for staging and production
            if env.lower() in ["staging", "uat", "prod", "production"]:
                stages_yaml += f"""
    - stage:
        name: {env.upper()} Approval
        identifier: {env}_approval
        type: Approval
        spec:
          execution:
            steps:
              - step:
                  name: Manual Approval
                  identifier: manual_approval
                  type: HarnessApproval
                  timeout: 24h
                  spec:
                    approvalMessage: Approve deployment to {env.upper()}
                    includePipelineExecutionHistory: true
                    approvers:
                      userGroups:
                        - {portfolio}_approvers
                      minimumCount: {"2" if is_prod else "1"}
                    approverInputs: []
"""
            
            # Deployment stage
            stages_yaml += f"""
    - stage:
        name: Deploy to {env.upper()}
        identifier: deploy_{env}
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: <+input>
          environment:
            environmentRef: {env}
            deployToAll: false
            infrastructureDefinitions:
              - identifier: {portfolio}_{env}_infra
          execution:
            steps:
              - step:
                  name: Rollout Deployment
                  identifier: rollout
                  type: K8sRollingDeploy
                  timeout: 10m
                  spec:
                    skipDryRun: false
                    pruningEnabled: false
              - step:
                  name: Verify Deployment
                  identifier: verify
                  type: Verify
                  timeout: 15m
                  spec:
                    isMultiServicesOrEnvs: false
                    type: {"Canary" if strategy == "Canary" else "Rolling"}
                    monitoredService:
                      type: Default
                      spec: {{}}
                    spec:
                      sensitivity: HIGH
                      duration: 5m
            rollbackSteps:
              - step:
                  name: Rollback
                  identifier: rollback
                  type: K8sRollingRollback
                  timeout: 10m
                  spec:
                    pruningEnabled: false
"""
        
        return f"""
pipeline:
  name: {name}
  identifier: {identifier}
  projectIdentifier: {portfolio}
  orgIdentifier: default
  tags:
    portfolio: {portfolio}
    managed_by: platform_engineering
  stages:{stages_yaml}
  properties:
    ci:
      codebase:
        connectorRef: <+input>
        repoName: <+input>
        build: <+input>
  notificationRules:
    - name: Pipeline Notifications
      identifier: pipeline_notifications
      pipelineEvents:
        - type: PipelineFailed
        - type: StageSuccess
          forStages:
            - deploy_prod
      notificationMethod:
        type: Slack
        spec:
          webhookUrl: <+input>
"""


# =============================================================================
# STREAMLIT UI MODULE
# =============================================================================

class HarnessCICDModule:
    """
    Main Streamlit UI Module for Harness IO CI/CD Integration
    Provides a reorganized, user-friendly workflow
    """
    
    @staticmethod
    def render():
        """Main render function for the module"""
        st.title("🚀 Harness IO CI/CD Platform")
        st.markdown("*Enterprise-grade CI/CD orchestration for multi-account environments*")
        
        # Initialize session state
        if "harness_mode" not in st.session_state:
            st.session_state.harness_mode = "Demo"
        if "selected_portfolio" not in st.session_state:
            st.session_state.selected_portfolio = None
        
        # Mode toggle
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mode = st.radio(
                "Mode",
                ["Demo", "Live"],
                horizontal=True,
                key="harness_mode_toggle"
            )
            st.session_state.harness_mode = mode
        
        if mode == "Live":
            st.info("🔑 Configure Harness API credentials in Settings to enable Live mode")
        
        # Main navigation tabs - REORGANIZED FOR USER-FRIENDLY WORKFLOW
        tabs = st.tabs([
            "📊 Dashboard",
            "🏢 Portfolios",
            "🔄 Pipelines",
            "▶️ Deployments",
            "✅ Approvals",
            "📦 Services",
            "🌍 Environments",
            "📈 Analytics",
            "⚙️ Settings"
        ])
        
        with tabs[0]:
            HarnessCICDModule._render_dashboard()
        with tabs[1]:
            HarnessCICDModule._render_portfolios()
        with tabs[2]:
            HarnessCICDModule._render_pipelines()
        with tabs[3]:
            HarnessCICDModule._render_deployments()
        with tabs[4]:
            HarnessCICDModule._render_approvals()
        with tabs[5]:
            HarnessCICDModule._render_services()
        with tabs[6]:
            HarnessCICDModule._render_environments()
        with tabs[7]:
            HarnessCICDModule._render_analytics()
        with tabs[8]:
            HarnessCICDModule._render_settings()
    
    @staticmethod
    def _render_dashboard():
        """Render unified dashboard with key metrics"""
        st.subheader("📊 CI/CD Command Center")
        
        metrics = HarnessDemoData.generate_metrics()
        portfolios = HarnessDemoData.get_portfolios()
        
        # Top metrics row
        cols = st.columns(6)
        with cols[0]:
            st.metric("Total AWS Accounts", HarnessDemoData.get_total_accounts())
        with cols[1]:
            st.metric("Active Portfolios", len(portfolios))
        with cols[2]:
            st.metric("Deployments Today", metrics["deployments"]["today"], "+3")
        with cols[3]:
            st.metric("Success Rate", f"{metrics['deployments']['success_rate']}%", "+2.1%")
        with cols[4]:
            st.metric("Pending Approvals", len(HarnessDemoData.generate_approvals()))
        with cols[5]:
            st.metric("Cost Today", f"${metrics['cost']['today']}", metrics['cost']['trend'])
        
        st.divider()
        
        # DORA Metrics
        st.subheader("🎯 DORA Metrics")
        dora_cols = st.columns(4)
        
        dora = metrics["dora"]
        with dora_cols[0]:
            st.metric(
                "Deployment Frequency",
                f"{dora['deployment_frequency']['value']} {dora['deployment_frequency']['unit']}",
                dora['deployment_frequency']['trend']
            )
            st.caption(f"Rating: {dora['deployment_frequency']['rating']}")
        
        with dora_cols[1]:
            st.metric(
                "Lead Time for Changes",
                f"{dora['lead_time']['value']} {dora['lead_time']['unit']}",
                dora['lead_time']['trend']
            )
            st.caption(f"Rating: {dora['lead_time']['rating']}")
        
        with dora_cols[2]:
            st.metric(
                "Mean Time to Recovery",
                f"{dora['mttr']['value']} {dora['mttr']['unit']}",
                dora['mttr']['trend']
            )
            st.caption(f"Rating: {dora['mttr']['rating']}")
        
        with dora_cols[3]:
            st.metric(
                "Change Failure Rate",
                f"{dora['change_failure_rate']['value']}{dora['change_failure_rate']['unit']}",
                dora['change_failure_rate']['trend']
            )
            st.caption(f"Rating: {dora['change_failure_rate']['rating']}")
        
        st.divider()
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔄 Recent Deployments")
            executions = HarnessDemoData.generate_executions(10)
            for exec in executions[:5]:
                status_icon = {
                    "Success": "✅",
                    "Failed": "❌",
                    "Running": "🔄",
                    "Waiting for Approval": "⏳"
                }.get(exec["status"], "❓")
                
                with st.container():
                    st.markdown(f"""
                    **{status_icon} {exec['pipeline']}** | {exec['portfolio']}
                    - Environment: `{exec['environment']}` | Branch: `{exec['branch']}`
                    - Duration: {exec['duration']} | Triggered by: {exec['triggered_by']}
                    """)
        
        with col2:
            st.subheader("⏳ Pending Approvals")
            approvals = HarnessDemoData.generate_approvals(5)
            for approval in approvals:
                urgency_color = {
                    "Critical": "🔴",
                    "High": "🟠",
                    "Normal": "🟢"
                }.get(approval["urgency"], "⚪")
                
                with st.container():
                    st.markdown(f"""
                    **{urgency_color} {approval['type']}** | {approval['portfolio']}
                    - Environment: `{approval['environment']}` | Pipeline: {approval['pipeline']}
                    - Requested by: {approval['requested_by']}
                    """)
                    if st.button(f"Review", key=f"review_{approval['id']}"):
                        st.session_state.selected_approval = approval['id']
    
    @staticmethod
    def _render_portfolios():
        """Render portfolio management view"""
        st.subheader("🏢 Portfolio Management")
        st.markdown("*Manage business unit portfolios and their AWS account associations*")
        
        portfolios = HarnessDemoData.get_portfolios()
        
        # Portfolio overview cards
        cols = st.columns(3)
        for i, portfolio in enumerate(portfolios):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {portfolio.name}")
                    st.markdown(f"**Identifier:** `{portfolio.identifier}`")
                    st.markdown(f"**AWS Accounts:** {len(portfolio.aws_accounts)}")
                    st.markdown(f"**Environments:** {', '.join(portfolio.environments)}")
                    st.markdown(f"**Cost Center:** {portfolio.cost_center}")
                    st.markdown(f"**Compliance:** {', '.join(portfolio.compliance_frameworks)}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("View Pipelines", key=f"view_pipes_{portfolio.identifier}"):
                            st.session_state.selected_portfolio = portfolio.identifier
                    with col2:
                        if st.button("Configure", key=f"config_{portfolio.identifier}"):
                            st.session_state.configure_portfolio = portfolio.identifier
        
        st.divider()
        
        # Portfolio details expander
        if st.session_state.selected_portfolio:
            selected = next((p for p in portfolios if p.identifier == st.session_state.selected_portfolio), None)
            if selected:
                st.subheader(f"📋 {selected.name} Details")
                
                tab1, tab2, tab3 = st.tabs(["AWS Accounts", "Pipelines", "Compliance"])
                
                with tab1:
                    st.markdown("**Associated AWS Accounts:**")
                    # Show first 20 accounts
                    account_cols = st.columns(5)
                    for i, account in enumerate(selected.aws_accounts[:20]):
                        with account_cols[i % 5]:
                            st.code(account)
                    if len(selected.aws_accounts) > 20:
                        st.info(f"... and {len(selected.aws_accounts) - 20} more accounts")
                
                with tab2:
                    pipelines = HarnessDemoData.generate_pipelines(selected)
                    for pipeline in pipelines:
                        with st.expander(f"🔄 {pipeline['name']}", expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Service:** {pipeline['service']}")
                                st.markdown(f"**Type:** {pipeline['deployment_type']}")
                                st.markdown(f"**Language:** {pipeline['language']}")
                            with col2:
                                st.markdown(f"**Success Rate:** {pipeline['success_rate']}%")
                                st.markdown(f"**Avg Duration:** {pipeline['avg_duration_mins']}m")
                                st.markdown(f"**Executions Today:** {pipeline['executions_today']}")
                
                with tab3:
                    st.markdown("**Compliance Frameworks:**")
                    for framework in selected.compliance_frameworks:
                        st.markdown(f"- ✅ {framework}")
                    st.markdown(f"\n**Approvers:** {', '.join(selected.approvers)}")
    
    @staticmethod
    def _render_pipelines():
        """Render pipeline management view"""
        st.subheader("🔄 Pipeline Management")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        portfolios = HarnessDemoData.get_portfolios()
        
        with col1:
            selected_portfolio = st.selectbox(
                "Filter by Portfolio",
                ["All"] + [p.name for p in portfolios]
            )
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Success", "Failed", "Running", "Waiting for Approval"]
            )
        with col3:
            search = st.text_input("Search Pipelines", placeholder="Enter pipeline name...")
        
        st.divider()
        
        # Pipeline list
        for portfolio in portfolios:
            if selected_portfolio != "All" and portfolio.name != selected_portfolio:
                continue
            
            pipelines = HarnessDemoData.generate_pipelines(portfolio)
            
            st.markdown(f"### 🏢 {portfolio.name}")
            
            for pipeline in pipelines:
                if search and search.lower() not in pipeline['name'].lower():
                    continue
                
                exec = pipeline['last_execution']
                status_icon = {
                    "Success": "✅",
                    "Failed": "❌",
                    "Running": "🔄",
                    "Waiting for Approval": "⏳"
                }.get(exec["status"], "❓")
                
                with st.expander(f"{status_icon} {pipeline['name']} | {exec['status']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Pipeline Info**")
                        st.markdown(f"- Service: {pipeline['service']}")
                        st.markdown(f"- Type: {pipeline['deployment_type']}")
                        st.markdown(f"- Language: {pipeline['language']}")
                    
                    with col2:
                        st.markdown("**Metrics**")
                        st.markdown(f"- Success Rate: {pipeline['success_rate']}%")
                        st.markdown(f"- Avg Duration: {pipeline['avg_duration_mins']}m")
                        st.markdown(f"- Today's Runs: {pipeline['executions_today']}")
                    
                    with col3:
                        st.markdown("**Last Execution**")
                        st.markdown(f"- Status: {exec['status']}")
                        st.markdown(f"- Branch: {exec['branch']}")
                        st.markdown(f"- Commit: `{exec['commit']}`")
                    
                    # Action buttons
                    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
                    with btn_col1:
                        if st.button("▶️ Run", key=f"run_{pipeline['identifier']}"):
                            st.success(f"Pipeline {pipeline['name']} triggered!")
                    with btn_col2:
                        if st.button("📋 History", key=f"history_{pipeline['identifier']}"):
                            st.session_state.view_history = pipeline['identifier']
                    with btn_col3:
                        if st.button("⚙️ Configure", key=f"configure_{pipeline['identifier']}"):
                            st.session_state.configure_pipeline = pipeline['identifier']
                    with btn_col4:
                        if st.button("📄 YAML", key=f"yaml_{pipeline['identifier']}"):
                            st.session_state.view_yaml = pipeline['identifier']
    
    @staticmethod
    def _render_deployments():
        """Render deployment execution view"""
        st.subheader("▶️ Deployment Center")
        
        subtabs = st.tabs(["Execute Pipeline", "Running Deployments", "Execution History"])
        
        with subtabs[0]:
            st.markdown("### 🚀 Execute New Deployment")
            
            portfolios = HarnessDemoData.get_portfolios()
            
            col1, col2 = st.columns(2)
            with col1:
                portfolio = st.selectbox(
                    "Select Portfolio",
                    [p.name for p in portfolios],
                    key="deploy_portfolio"
                )
                
                selected_portfolio = next((p for p in portfolios if p.name == portfolio), None)
                if selected_portfolio:
                    pipelines = HarnessDemoData.generate_pipelines(selected_portfolio)
                    pipeline = st.selectbox(
                        "Select Pipeline",
                        [p['name'] for p in pipelines],
                        key="deploy_pipeline"
                    )
            
            with col2:
                if selected_portfolio:
                    environment = st.selectbox(
                        "Target Environment",
                        selected_portfolio.environments,
                        key="deploy_env"
                    )
                    
                    strategy = st.selectbox(
                        "Deployment Strategy",
                        [s.value for s in DeploymentStrategy],
                        key="deploy_strategy"
                    )
            
            st.divider()
            
            # Deployment parameters
            with st.expander("📝 Deployment Parameters", expanded=True):
                param_col1, param_col2 = st.columns(2)
                with param_col1:
                    branch = st.text_input("Branch", value="main")
                    tag = st.text_input("Image Tag", value="latest")
                with param_col2:
                    replicas = st.number_input("Replicas", min_value=1, max_value=10, value=3)
                    notify = st.checkbox("Send Notifications", value=True)
            
            # Execute button
            if st.button("🚀 Execute Deployment", type="primary", use_container_width=True):
                with st.spinner("Triggering deployment..."):
                    time.sleep(1)
                    st.success(f"""
                    ✅ Deployment triggered successfully!
                    
                    - **Pipeline:** {pipeline}
                    - **Environment:** {environment}
                    - **Strategy:** {strategy}
                    - **Branch:** {branch}
                    - **Execution ID:** {hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]}
                    """)
        
        with subtabs[1]:
            st.markdown("### 🔄 Currently Running Deployments")
            
            executions = HarnessDemoData.generate_executions(20)
            running = [e for e in executions if e['status'] == 'Running']
            
            if running:
                for exec in running:
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        with col1:
                            st.markdown(f"**{exec['pipeline']}**")
                            st.caption(f"Portfolio: {exec['portfolio']}")
                        with col2:
                            st.markdown(f"Environment: `{exec['environment']}`")
                            st.caption(f"Branch: {exec['branch']}")
                        with col3:
                            st.markdown(f"Started: {exec['started_at'][:16]}")
                            st.progress(0.6)
                        with col4:
                            if st.button("🛑 Abort", key=f"abort_{exec['id']}"):
                                st.warning("Deployment aborted!")
            else:
                st.info("No deployments currently running")
        
        with subtabs[2]:
            st.markdown("### 📜 Execution History")
            
            executions = HarnessDemoData.generate_executions(20)
            
            # History table
            history_data = []
            for exec in executions:
                history_data.append({
                    "ID": exec['id'],
                    "Pipeline": exec['pipeline'],
                    "Portfolio": exec['portfolio'],
                    "Environment": exec['environment'],
                    "Status": exec['status'],
                    "Duration": exec['duration'],
                    "Triggered By": exec['triggered_by'],
                    "Cost": f"${exec['cost']}"
                })
            
            st.dataframe(history_data, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_approvals():
        """Render approval workflow view"""
        st.subheader("✅ Approval Workflows")
        
        approvals = HarnessDemoData.generate_approvals(10)
        pending = [a for a in approvals if a['status'] == 'Pending']
        
        st.markdown(f"### ⏳ Pending Approvals ({len(pending)})")
        
        if not pending:
            st.info("No pending approvals")
            return
        
        for approval in pending:
            urgency_color = {
                "Critical": "🔴",
                "High": "🟠",
                "Normal": "🟢"
            }.get(approval["urgency"], "⚪")
            
            with st.expander(f"{urgency_color} {approval['type']} - {approval['portfolio']} ({approval['environment'].upper()})", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Pipeline:** {approval['pipeline']}")
                    st.markdown(f"**Environment:** `{approval['environment']}`")
                    st.markdown(f"**Requested By:** {approval['requested_by']}")
                    st.markdown(f"**Changes:** {approval['changes']}")
                
                with col2:
                    st.markdown(f"**Requested At:** {approval['requested_at'][:16]}")
                    st.markdown(f"**Expires At:** {approval['expires_at'][:16]}")
                    st.markdown(f"**Approvers:** {', '.join(approval['approvers'])}")
                    st.markdown(f"**Urgency:** {approval['urgency']}")
                
                st.divider()
                
                # Approval actions
                comments = st.text_area("Comments", key=f"comments_{approval['id']}", placeholder="Add approval comments...")
                
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("✅ Approve", key=f"approve_{approval['id']}", type="primary"):
                        st.success(f"Approved: {approval['type']}")
                with btn_col2:
                    if st.button("❌ Reject", key=f"reject_{approval['id']}"):
                        st.error(f"Rejected: {approval['type']}")
                with btn_col3:
                    if st.button("🔍 View Details", key=f"details_{approval['id']}"):
                        st.info("Opening detailed view...")
    
    @staticmethod
    def _render_services():
        """Render service catalog view"""
        st.subheader("📦 Service Catalog")
        
        subtabs = st.tabs(["All Services", "Create Service", "Service Templates"])
        
        with subtabs[0]:
            services = HarnessDemoData.SERVICES
            
            st.markdown("### 📋 Registered Services")
            
            for svc in services:
                with st.expander(f"📦 {svc['name']} ({svc['type']})", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Name:** {svc['name']}")
                        st.markdown(f"**Type:** {svc['type']}")
                        st.markdown(f"**Language:** {svc['language']}")
                    with col2:
                        st.markdown("**Deployments:** 45")
                        st.markdown("**Last Deployed:** 2 hours ago")
                        st.markdown("**Health:** ✅ Healthy")
        
        with subtabs[1]:
            st.markdown("### ➕ Create New Service")
            
            service_type = st.selectbox(
                "Deployment Type",
                ["Kubernetes", "ECS", "AWS Lambda", "Serverless"]
            )
            
            with st.form("create_service"):
                svc_name = st.text_input("Service Name", placeholder="api-gateway")
                svc_identifier = st.text_input("Identifier", placeholder="api_gateway")
                svc_description = st.text_area("Description", placeholder="API Gateway microservice")
                
                st.markdown("#### Artifact Configuration")
                
                artifact_type = st.selectbox(
                    "Artifact Source",
                    ["ECR", "Docker Hub", "Artifactory", "S3"]
                )
                
                if artifact_type == "ECR":
                    ecr_region = st.selectbox("ECR Region", ["us-east-1", "us-west-2", "eu-west-1"])
                    ecr_repo = st.text_input("ECR Repository", placeholder="my-repo/api-gateway")
                    connector_ref = st.text_input("AWS Connector Reference", placeholder="aws_prod_account")
                
                if st.form_submit_button("📦 Create Service", type="primary"):
                    if svc_name and svc_identifier:
                        st.success(f"Service '{svc_name}' created successfully!")
                        
                        # Show generated YAML
                        if service_type == "Kubernetes":
                            yaml_content = HarnessServiceTemplates.generate_kubernetes_service(
                                name=svc_name,
                                identifier=svc_identifier,
                                ecr_region=ecr_region if artifact_type == "ECR" else "us-east-1",
                                ecr_repo=ecr_repo if artifact_type == "ECR" else "",
                                connector_ref=connector_ref if artifact_type == "ECR" else ""
                            )
                            st.markdown("#### Generated Service YAML")
                            st.code(yaml_content, language="yaml")
                    else:
                        st.error("Please fill in all required fields")
        
        with subtabs[2]:
            st.markdown("### 📋 Service Templates")
            
            templates = [
                {"name": "Kubernetes Microservice", "desc": "Standard K8s deployment with ECR", "type": "Kubernetes"},
                {"name": "Lambda Function", "desc": "Serverless AWS Lambda", "type": "Lambda"},
                {"name": "ECS Service", "desc": "AWS ECS Fargate deployment", "type": "ECS"},
                {"name": "Static Website", "desc": "S3 + CloudFront deployment", "type": "S3"},
            ]
            
            for tmpl in templates:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{tmpl['name']}**")
                        st.caption(tmpl['desc'])
                    with col2:
                        if st.button("Use Template", key=f"use_{tmpl['type']}"):
                            st.info(f"Loading {tmpl['name']} template...")
    
    @staticmethod
    def _render_environments():
        """Render environment management view"""
        st.subheader("🌍 Environment Management")
        
        portfolios = HarnessDemoData.get_portfolios()
        
        selected_portfolio = st.selectbox(
            "Select Portfolio",
            [p.name for p in portfolios],
            key="env_portfolio"
        )
        
        portfolio = next((p for p in portfolios if p.name == selected_portfolio), None)
        
        if portfolio:
            st.markdown(f"### Environments for {portfolio.name}")
            
            for env in portfolio.environments:
                env_type = EnvironmentType[env.upper()] if env.upper() in EnvironmentType.__members__ else EnvironmentType.DEV
                
                with st.expander(f"🌍 {env.upper()} Environment", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Type:** {env_type.value}")
                        st.markdown(f"**AWS Accounts:** {len(portfolio.aws_accounts) // len(portfolio.environments)}")
                        st.markdown(f"**Status:** ✅ Healthy")
                    
                    with col2:
                        st.markdown(f"**Last Deployment:** 3 hours ago")
                        st.markdown(f"**Active Services:** 12")
                        st.markdown(f"**Compliance:** {'✅' if env != 'dev' else '⚠️'}")
                    
                    # Infrastructure details
                    st.markdown("#### Infrastructure")
                    infra_data = {
                        "Component": ["EKS Cluster", "RDS Database", "ElastiCache", "S3 Buckets"],
                        "Status": ["✅ Running", "✅ Running", "✅ Running", "✅ Available"],
                        "Version": ["1.28", "15.4", "7.0", "N/A"],
                        "Cost/Day": ["$45.20", "$28.50", "$12.30", "$5.80"]
                    }
                    st.dataframe(infra_data, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_analytics():
        """Render analytics and reporting view"""
        st.subheader("📈 CI/CD Analytics")
        
        metrics = HarnessDemoData.generate_metrics()
        
        subtabs = st.tabs(["Overview", "Cost Analysis", "Performance", "Reports"])
        
        with subtabs[0]:
            st.markdown("### 📊 Deployment Analytics")
            
            # Summary metrics
            cols = st.columns(4)
            with cols[0]:
                st.metric("This Week", metrics["deployments"]["this_week"], "+12")
            with cols[1]:
                st.metric("This Month", metrics["deployments"]["this_month"], "+45")
            with cols[2]:
                st.metric("Success Rate", f"{metrics['deployments']['success_rate']}%", "+1.5%")
            with cols[3]:
                st.metric("Rollbacks", metrics["deployments"]["rollbacks"], "-2")
            
            # Charts placeholder
            st.markdown("#### Deployment Trend (Last 30 Days)")
            chart_data = {
                "Date": [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(30, 0, -1)],
                "Deployments": [10 + (i % 8) for i in range(30)],
                "Success": [9 + (i % 7) for i in range(30)]
            }
            st.line_chart(chart_data, x="Date", y=["Deployments", "Success"])
        
        with subtabs[1]:
            st.markdown("### 💰 CI/CD Cost Analysis")
            
            cost = metrics["cost"]
            
            cols = st.columns(3)
            with cols[0]:
                st.metric("Today", f"${cost['today']}")
            with cols[1]:
                st.metric("This Week", f"${cost['this_week']}")
            with cols[2]:
                st.metric("This Month", f"${cost['this_month']}", cost['trend'])
            
            st.markdown("#### Cost by Portfolio")
            cost_data = {
                "Portfolio": list(cost['by_portfolio'].keys()),
                "Cost ($)": list(cost['by_portfolio'].values())
            }
            st.bar_chart(cost_data, x="Portfolio", y="Cost ($)")
        
        with subtabs[2]:
            st.markdown("### ⚡ Performance Metrics")
            
            st.markdown("#### Pipeline Duration Analysis")
            perf_data = {
                "Pipeline": ["API Gateway", "Payment Service", "Auth Service", "Data Processor", "Frontend"],
                "Avg Duration (min)": [12, 18, 8, 25, 6],
                "P95 Duration (min)": [18, 28, 12, 40, 10]
            }
            st.dataframe(perf_data, use_container_width=True, hide_index=True)
        
        with subtabs[3]:
            st.markdown("### 📑 Generate Reports")
            
            report_type = st.selectbox(
                "Report Type",
                ["Weekly Deployment Summary", "Monthly Cost Report", "Compliance Audit", "DORA Metrics Report"]
            )
            
            date_range = st.date_input(
                "Date Range",
                value=(datetime.now() - timedelta(days=7), datetime.now())
            )
            
            if st.button("📊 Generate Report", type="primary"):
                with st.spinner("Generating report..."):
                    time.sleep(1)
                    st.success(f"Report generated: {report_type}")
                    st.download_button(
                        "📥 Download Report",
                        data="Report content here...",
                        file_name=f"{report_type.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
    
    @staticmethod
    def _render_settings():
        """Render settings and configuration view"""
        st.subheader("⚙️ Harness Configuration")
        
        subtabs = st.tabs(["API Configuration", "Connectors", "Delegates", "Notifications"])
        
        with subtabs[0]:
            st.markdown("### 🔑 Harness API Configuration")
            
            with st.form("harness_config"):
                account_id = st.text_input("Account ID", placeholder="Enter Harness Account ID")
                api_key = st.text_input("API Key", type="password", placeholder="Enter API Key")
                base_url = st.text_input("Base URL", value="https://app.harness.io")
                org_id = st.text_input("Organization Identifier", value="default")
                
                if st.form_submit_button("💾 Save Configuration"):
                    st.success("Configuration saved successfully!")
        
        with subtabs[1]:
            st.markdown("### 🔌 AWS Connectors")
            
            portfolios = HarnessDemoData.get_portfolios()
            
            for portfolio in portfolios:
                with st.expander(f"🏢 {portfolio.name} Connector", expanded=False):
                    st.markdown(f"**Accounts:** {len(portfolio.aws_accounts)}")
                    st.markdown(f"**Status:** ✅ Connected")
                    st.markdown(f"**IAM Role:** `arn:aws:iam::*:role/HarnessDelegate-{portfolio.identifier}`")
                    
                    if st.button(f"Test Connection", key=f"test_{portfolio.identifier}"):
                        with st.spinner("Testing..."):
                            time.sleep(1)
                            st.success("Connection successful!")
        
        with subtabs[2]:
            st.markdown("### 🤖 Harness Delegates")
            
            delegates = [
                {"name": "platform-engineering-delegate", "status": "Connected", "version": "24.01.82808", "pods": 3},
                {"name": "banking-delegate", "status": "Connected", "version": "24.01.82808", "pods": 2},
                {"name": "insurance-delegate", "status": "Connected", "version": "24.01.82808", "pods": 2},
            ]
            
            for delegate in delegates:
                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**{delegate['name']}**")
                    with col2:
                        st.markdown(f"Status: ✅ {delegate['status']}")
                        st.markdown(f"Version: {delegate['version']}")
                    with col3:
                        st.markdown(f"Pods: {delegate['pods']}")
                        if st.button("Refresh", key=f"refresh_{delegate['name']}"):
                            st.info("Refreshing delegate...")
        
        with subtabs[3]:
            st.markdown("### 🔔 Notification Settings")
            
            with st.form("notifications"):
                st.markdown("#### Slack Integration")
                slack_webhook = st.text_input("Slack Webhook URL", placeholder="https://hooks.slack.com/...")
                slack_channel = st.text_input("Default Channel", placeholder="#deployments")
                
                st.markdown("#### Email Notifications")
                email_enabled = st.checkbox("Enable Email Notifications", value=True)
                email_recipients = st.text_area("Recipients", placeholder="team@company.com, lead@company.com")
                
                st.markdown("#### Notification Events")
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox("Pipeline Started", value=False)
                    st.checkbox("Pipeline Success", value=True)
                    st.checkbox("Pipeline Failed", value=True)
                with col2:
                    st.checkbox("Approval Required", value=True)
                    st.checkbox("Deployment Completed", value=True)
                    st.checkbox("Rollback Triggered", value=True)
                
                if st.form_submit_button("💾 Save Notification Settings"):
                    st.success("Notification settings saved!")


# =============================================================================
# MODULE ENTRY POINT
# =============================================================================

def render():
    """Module-level render function for navigation compatibility"""
    HarnessCICDModule.render()


if __name__ == "__main__":
    # For standalone testing
    import streamlit as st
    render()
