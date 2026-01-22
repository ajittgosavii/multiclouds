# ☁️ Multi Cloud Infrastructure Intelligence Platform (MCIP)

## Enterprise Multi-Account Cloud Management with Harness CI/CD Integration

A comprehensive Streamlit-based platform for managing multi-cloud infrastructure across AWS, Azure, and GCP with enterprise-grade Harness IO CI/CD orchestration.

---

## 🌟 Key Features

### Multi-Cloud Support
- **AWS** - Full support for 640+ accounts across multiple portfolios
- **Azure** - Subscription and resource management
- **GCP** - Project and organization management

### Core Modules
| Module | Description |
|--------|-------------|
| 🏠 **Dashboard** | Command center with key metrics and alerts |
| 👥 **Account/Subscription Management** | Multi-account organization |
| 📦 **Resource Inventory** | Cross-cloud resource tracking |
| 🌐 **Network Management** | VPC, VNet, VPC Network management |
| 🏢 **Organizations** | AWS Orgs, Azure Management Groups, GCP Org |
| 📐 **Design & Planning** | Architecture planning tools |
| 🚀 **Provisioning** | Infrastructure deployment |
| 📄 **CI/CD** | Native cloud CI/CD pipelines |
| 🔷 **Harness CI/CD** | Enterprise Harness IO integration (NEW) |
| ⚙️ **Operations** | Day-to-day operational tasks |
| ⚡ **Advanced Operations** | Advanced automation |
| 🤖 **Security & AI** | Security compliance with AI assistance |
| 📌 **EKS/AKS/GKE** | Kubernetes cluster management |
| 💰 **FinOps** | Cost optimization and tracking |
| 📄 **Account Lifecycle** | Account provisioning workflows |
| 👨‍💻 **Developer Experience** | Self-service developer tools |
| 🤖 **AI Assistant** | Claude AI-powered assistance |
| 👨‍💼 **Admin Panel** | Platform administration |

---

## 🚀 Harness CI/CD Integration

### New in This Release
The platform now includes full Harness IO integration for enterprise-grade CI/CD orchestration:

- **Multi-Account Pipeline Management** - Orchestrate deployments across 640+ AWS accounts
- **Portfolio-Centric Deployments** - Organize pipelines by business unit
- **Deployment Strategies** - Rolling, Blue-Green, Canary support
- **Approval Workflows** - Multi-level approval gates with urgency classification
- **DORA Metrics** - Real-time deployment frequency, lead time, MTTR, CFR
- **Cost Tracking** - Per-deployment and per-portfolio cost analysis
- **Service Catalog** - Kubernetes, ECS, Lambda service templates

### Portfolio Structure
```
Enterprise Organization
├── Digital Banking (100 AWS accounts)
├── Insurance Platform (150 AWS accounts)
├── Wealth Management (80 AWS accounts)
├── Core Infrastructure (120 AWS accounts)
├── Data Analytics (90 AWS accounts)
└── Customer Experience (100 AWS accounts)
```

---

## 📥 Installation

### Prerequisites
- Python 3.9+
- Streamlit Cloud account (for deployment)
- GitHub account

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/multiclouds.git
cd multiclouds

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `streamlit_app.py` as the main file
5. Add secrets in Streamlit Cloud settings:
   - `ANTHROPIC_API_KEY` (for AI features)
   - Firebase credentials (for authentication)

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file or configure in Streamlit Cloud secrets:

```env
# AI Integration
ANTHROPIC_API_KEY=your_anthropic_api_key

# Firebase Authentication
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email

# Harness IO (optional - demo mode available)
HARNESS_ACCOUNT_ID=your_harness_account_id
HARNESS_API_KEY=your_harness_api_key
```

### Streamlit Secrets (`secrets.toml`)
```toml
[anthropic]
api_key = "your_api_key"

[firebase]
project_id = "your_project"
# ... other firebase config
```

---

## 📁 Project Structure

```
multiclouds/
├── streamlit_app.py              # Main application entry
├── requirements.txt              # Python dependencies
├── config_settings.py            # Application configuration
├── components_navigation.py      # Module navigation
├── components_sidebar.py         # Sidebar components
├── core_session_manager.py       # Session management
├── core_account_manager.py       # Account management
│
├── # AWS Modules
├── modules_dashboard.py
├── modules_account_management.py
├── modules_resource_inventory.py
├── modules_cicd_unified.py
├── harness_cicd_module.py        # NEW: Harness integration
├── modules_*.py                  # Other AWS modules
│
├── # Azure Modules
├── azure_modules_*.py
│
├── # GCP Modules
├── gcp_modules_*.py
│
├── # Authentication
├── auth_azure_sso.py
├── auth_database_firebase.py
├── auth_ui_components.py
│
├── # Documentation
├── DEPLOYMENT_GUIDE.md
├── STREAMLIT_CLOUD_DEPLOYMENT.md
├── EKS_GUIDE.md
└── GITHUB_WEB_UPLOAD_GUIDE.md
```

---

## 🔷 Using Harness CI/CD Module

### Accessing the Module
1. Select any cloud provider (AWS, Azure, or GCP)
2. Click the **🔷 Harness** button in the navigation bar

### Available Features

#### Dashboard
- Active pipelines count
- Success rate metrics
- Pending approvals
- DORA metrics summary

#### Pipelines
- View all pipelines by portfolio
- Filter by status and environment
- Execute deployments

#### Deployments
- Configure deployment parameters
- Select deployment strategy (Rolling/Blue-Green/Canary)
- Monitor execution progress

#### Approvals
- View pending approval requests
- Approve/reject with comments
- Track approval history

#### Analytics
- Deployment trends
- Cost analysis by portfolio
- Performance metrics
- Generate reports

---

## 🔒 Authentication

The platform supports Azure SSO authentication with Firebase backend:

- **Admin** - Full platform access
- **Architect** - Design and planning access
- **Developer** - CI/CD and deployment access
- **FinOps** - Cost management access
- **Security** - Security and compliance access
- **Viewer** - Read-only access

---

## 📊 Demo Mode

All modules include demo mode with simulated data for testing without cloud credentials:

- Realistic multi-account data
- Sample pipelines and deployments
- Mock approval workflows
- Simulated metrics

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Module not loading | Check import paths and requirements |
| Authentication failing | Verify Firebase credentials |
| Harness API errors | Check API key and account ID |
| Streamlit timeout | Optimize heavy queries |

### Logs
- **Local**: Check terminal output
- **Streamlit Cloud**: Manage App → Logs

---

## 📄 License

Developed for enterprise cloud operations.

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-22 | Added Harness CI/CD integration |
| 2.0.0 | 2025-12-08 | Multi-cloud support (AWS, Azure, GCP) |
| 1.0.0 | 2025-10-01 | Initial AWS-focused release |

---

## 👨‍💻 Author

**Ajit** - Senior Project Manager, Infosys  
Enterprise Cloud Operations & Platform Engineering

---

## 🙏 Acknowledgments

- Anthropic Claude AI for development assistance
- Harness IO platform documentation
- Streamlit team for the amazing framework
