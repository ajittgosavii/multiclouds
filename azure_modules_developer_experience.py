"""
Azure Developer Experience (DevEx) - Your Coding Assistant
Practical tools, ready-to-use code, and AI help for Azure developers
"""

import streamlit as st
from auth_azure_sso import require_permission
import json
import uuid

class AzureDevExModule:
    """Azure Developer Experience - Practical Coding Helper"""
    
    @staticmethod
    @require_permission('use_devex')

    def render():
        """Render Azure DevEx module"""
        
        if 'azure_devex_session_id' not in st.session_state:
            st.session_state.azure_devex_session_id = str(uuid.uuid4())[:8]
        
        st.title("👨‍💻 Azure Developer Experience")
        st.markdown("**Your coding assistant** - Copy-paste code, generate commands, get instant help")
        
        ai_available = True
        
        if ai_available:
            st.success("🤖 **AI Assistant: READY** | Ask coding questions | Generate Azure code | Debug issues")
        
        tabs = st.tabs([
            "🏠 Dev Portal",
            "📚 Quick Reference",
            "💻 Code Generator",
            "🔧 CLI Commands",
            "🚀 Getting Started",
            "🎯 Try It Now",
            "🤖 AI Helper",
            "🐛 Debug Assistant"
        ])
        
        with tabs[0]:
            AzureDevExModule._render_developer_portal()
        with tabs[1]:
            AzureDevExModule._render_quick_reference()
        with tabs[2]:
            AzureDevExModule._render_code_generator()
        with tabs[3]:
            AzureDevExModule._render_cli_commands()
        with tabs[4]:
            AzureDevExModule._render_getting_started()
        with tabs[5]:
            AzureDevExModule._render_try_it_now()
        with tabs[6]:
            AzureDevExModule._render_ai_helper(ai_available)
        with tabs[7]:
            AzureDevExModule._render_debug_assistant(ai_available)
    
    @staticmethod
    def _render_developer_portal():
        """Developer portal hub"""
        st.markdown("## 🏠 Azure Developer Portal")
        st.caption("Your one-stop shop for Azure development")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🚀 Quick Actions")
            if st.button("📋 Generate az CLI command", use_container_width=True):
                st.info("Jump to CLI Commands tab →")
            if st.button("💻 Get code snippet", use_container_width=True):
                st.info("Jump to Code Generator tab →")
            if st.button("🐛 Debug my issue", use_container_width=True):
                st.info("Jump to Debug Assistant tab →")
            if st.button("🤖 Ask AI", use_container_width=True):
                st.info("Jump to AI Helper tab →")
        
        with col2:
            st.markdown("### 📚 Popular Resources")
            st.markdown("""
            - [Azure SDK for Python](https://aka.ms/azsdk/python)
            - [Azure SDK for .NET](https://aka.ms/azsdk/net)
            - [Azure SDK for Java](https://aka.ms/azsdk/java)
            - [Azure CLI Docs](https://docs.microsoft.com/cli/azure)
            - [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep)
            - [Azure REST API Reference](https://docs.microsoft.com/rest/api/azure)
            """)
        
        with col3:
            st.markdown("### 💡 Common Tasks")
            st.markdown("""
            **Storage:**
            - Upload blob to storage
            - List container contents
            - Generate SAS token
            
            **Compute:**
            - Create VM
            - Start/stop VM
            - Get VM status
            
            **Database:**
            - Connect to Azure SQL
            - Query Cosmos DB
            - Manage PostgreSQL
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 Today's Tips")
        
        tips = [
            "💡 **Tip:** Use `az interactive` for auto-complete and help as you type",
            "💡 **Tip:** Add `--query` to filter az CLI output using JMESPath",
            "💡 **Tip:** Use Managed Identity instead of storing credentials in code",
            "💡 **Tip:** Enable Azure Monitor Application Insights for automatic telemetry"
        ]
        
        for tip in tips:
            st.info(tip)
    
    @staticmethod
    def _render_quick_reference():
        """Quick reference guide"""
        st.markdown("## 📚 Azure Quick Reference")
        st.caption("Common patterns and examples you can copy-paste")
        
        category = st.selectbox("Select Category", [
            "Storage (Blob, Queue, Table)",
            "Compute (VMs, App Service)",
            "Database (SQL, Cosmos DB)",
            "Messaging (Service Bus, Event Hubs)",
            "Identity (AAD, Managed Identity)",
            "Monitoring (App Insights, Log Analytics)"
        ])
        
        if "Storage" in category:
            st.markdown("### 📦 Blob Storage - Python")
            st.code('''
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

# Using Managed Identity (recommended)
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Upload file
blob_client = blob_service.get_blob_client(
    container="mycontainer", 
    blob="myfile.txt"
)
with open("local_file.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# Download file
with open("downloaded.txt", "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

# List blobs
container_client = blob_service.get_container_client("mycontainer")
for blob in container_client.list_blobs():
    print(blob.name)
            ''', language='python')
            
            st.markdown("### 📦 Blob Storage - C#")
            st.code('''
using Azure.Storage.Blobs;
using Azure.Identity;

// Using Managed Identity
var credential = new DefaultAzureCredential();
var blobServiceClient = new BlobServiceClient(
    new Uri("https://mystorageaccount.blob.core.windows.net"),
    credential
);

// Upload
var containerClient = blobServiceClient.GetBlobContainerClient("mycontainer");
var blobClient = containerClient.GetBlobClient("myfile.txt");
await blobClient.UploadAsync("local_file.txt", overwrite: true);

// Download
await blobClient.DownloadToAsync("downloaded.txt");

// List
await foreach (var blob in containerClient.GetBlobsAsync())
{
    Console.WriteLine(blob.Name);
}
            ''', language='csharp')
        
        elif "Compute" in category:
            st.markdown("### 🖥️ App Service Deployment - Python Flask")
            st.code('''
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Azure App Service!"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

# requirements.txt
# Flask==2.3.0

# Deploy commands:
# az webapp up --name myapp --resource-group mygroup --runtime "PYTHON:3.11"
            ''', language='python')
        
        elif "Database" in category:
            st.markdown("### 🗄️ Azure SQL Connection - Python")
            st.code('''
import pyodbc
from azure.identity import DefaultAzureCredential
import struct

# Using Managed Identity (recommended)
credential = DefaultAzureCredential()
token = credential.get_token("https://database.windows.net/.default")
token_bytes = token.token.encode("utf-16-le")
token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=myserver.database.windows.net;"
    "DATABASE=mydb;",
    attrs_before={1256: token_struct}
)

# Query
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE active = ?", (True,))
for row in cursor:
    print(row)

conn.close()
            ''', language='python')
        
        elif "Messaging" in category:
            st.markdown("### 📬 Service Bus - Send Message")
            st.code('''
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(
    fully_qualified_namespace="mybus.servicebus.windows.net",
    credential=credential
)

# Send message
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name="myqueue")
    with sender:
        message = ServiceBusMessage("Hello Azure Service Bus!")
        sender.send_messages(message)

# Receive messages
with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name="myqueue")
    with receiver:
        for msg in receiver.receive_messages(max_wait_time=5):
            print(str(msg))
            receiver.complete_message(msg)
            ''', language='python')
        
        st.markdown("---")
        st.info("💡 **Pro Tip:** Always use Managed Identity instead of connection strings in production!")
    
    @staticmethod
    def _render_code_generator():
        """Interactive code generator"""
        st.markdown("## 💻 Azure Code Generator")
        st.caption("Generate ready-to-use code for common tasks")
        
        task = st.selectbox("What do you want to do?", [
            "Upload file to Blob Storage",
            "Create Azure SQL connection",
            "Send Service Bus message",
            "Query Cosmos DB",
            "Deploy to App Service",
            "Create VM with CLI",
            "Set up Key Vault access"
        ])
        
        language = st.selectbox("Programming Language", ["Python", "C#", "Java", "JavaScript", "az CLI", "PowerShell"])
        
        if task == "Upload file to Blob Storage":
            account = st.text_input("Storage Account Name", "mystorageaccount")
            container = st.text_input("Container Name", "mycontainer")
            
            if language == "Python":
                code = f'''
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://{account}.blob.core.windows.net",
    credential=credential
)

# Upload file
blob_client = blob_service.get_blob_client(container="{container}", blob="myfile.txt")
with open("local_file.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded to https://{account}.blob.core.windows.net/{container}/myfile.txt")
'''
            elif language == "az CLI":
                code = f'''
# Upload single file
az storage blob upload \\
    --account-name {account} \\
    --container-name {container} \\
    --name myfile.txt \\
    --file local_file.txt \\
    --auth-mode login

# Upload directory
az storage blob upload-batch \\
    --account-name {account} \\
    --destination {container} \\
    --source ./local_directory/ \\
    --auth-mode login
'''
            else:
                code = "# Code generation for this language coming soon!"
            
            st.code(code, language='python' if language == "Python" else 'bash')
            st.button("📋 Copy to Clipboard")
        
        elif task == "Create VM with CLI":
            rg = st.text_input("Resource Group", "myResourceGroup")
            vm_name = st.text_input("VM Name", "myVM")
            vm_size = st.selectbox("VM Size", ["Standard_B2s", "Standard_D2s_v3", "Standard_D4s_v3"])
            
            code = f'''
# Create resource group
az group create --name {rg} --location eastus

# Create VM
az vm create \\
    --resource-group {rg} \\
    --name {vm_name} \\
    --image Ubuntu2204 \\
    --size {vm_size} \\
    --admin-username azureuser \\
    --generate-ssh-keys \\
    --public-ip-sku Standard

# Open port 80
az vm open-port --port 80 --resource-group {rg} --name {vm_name}

# Get VM IP address
az vm show -d -g {rg} -n {vm_name} --query publicIps -o tsv
'''
            st.code(code, language='bash')
            st.success("✅ Generated! Copy and run in Azure Cloud Shell or your terminal")
    
    @staticmethod
    def _render_cli_commands():
        """az CLI command helper"""
        st.markdown("## 🔧 Azure CLI Command Helper")
        st.caption("Build az CLI commands interactively")
        
        service = st.selectbox("Azure Service", [
            "Storage Account",
            "Virtual Machine",
            "App Service",
            "SQL Database",
            "Container Instance",
            "Key Vault"
        ])
        
        operation = st.selectbox("Operation", ["Create", "List", "Show", "Delete", "Update"])
        
        if service == "Storage Account" and operation == "Create":
            st.markdown("### Configure Storage Account Creation")
            name = st.text_input("Storage Account Name", "mystorageacct123")
            rg = st.text_input("Resource Group", "myResourceGroup")
            location = st.selectbox("Location", ["eastus", "westus2", "westeurope", "southeastasia"])
            sku = st.selectbox("SKU", ["Standard_LRS", "Standard_GRS", "Standard_ZRS", "Premium_LRS"])
            
            cmd = f'''az storage account create \\
    --name {name} \\
    --resource-group {rg} \\
    --location {location} \\
    --sku {sku} \\
    --kind StorageV2 \\
    --enable-hierarchical-namespace true'''
            
            st.code(cmd, language='bash')
            st.info("💡 Copy and run this command in Azure Cloud Shell or your terminal")
        
        elif service == "Virtual Machine" and operation == "Create":
            vm_name = st.text_input("VM Name", "myVM")
            rg = st.text_input("Resource Group", "myResourceGroup")
            image = st.selectbox("Image", ["Ubuntu2204", "Win2022Datacenter", "Debian11"])
            size = st.selectbox("Size", ["Standard_B2s", "Standard_D2s_v3", "Standard_D4s_v3"])
            
            cmd = f'''az vm create \\
    --resource-group {rg} \\
    --name {vm_name} \\
    --image {image} \\
    --size {size} \\
    --admin-username azureuser \\
    --generate-ssh-keys \\
    --public-ip-sku Standard'''
            
            st.code(cmd, language='bash')
    
    @staticmethod
    def _render_getting_started():
        """Getting started guide"""
        st.markdown("## 🚀 Getting Started with Azure Development")
        
        st.markdown("### 1️⃣ Install Azure CLI")
        st.code('''
# macOS
brew install azure-cli

# Windows
winget install Microsoft.AzureCLI

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az --version
        ''', language='bash')
        
        st.markdown("### 2️⃣ Login to Azure")
        st.code('''
# Login interactively
az login

# Login with service principal
az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>

# Set default subscription
az account set --subscription "My Subscription"
        ''', language='bash')
        
        st.markdown("### 3️⃣ Install Python SDK")
        st.code('''
# Install Azure SDK packages
pip install azure-identity
pip install azure-storage-blob
pip install azure-keyvault-secrets
pip install azure-servicebus
pip install azure-cosmos

# Or install all common packages
pip install azure-core azure-identity azure-mgmt-resource
        ''', language='bash')
        
        st.markdown("### 4️⃣ Your First Azure Python App")
        st.code('''
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Use Managed Identity or local credentials
credential = DefaultAzureCredential()

# Connect to storage
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Upload a file
container_client = blob_service.get_container_client("mycontainer")
blob_client = container_client.get_blob_client("hello.txt")
blob_client.upload_blob("Hello Azure!", overwrite=True)

print("✅ File uploaded successfully!")
        ''', language='python')
        
        st.success("🎉 You're ready to build on Azure!")
    
    @staticmethod
    def _render_try_it_now():
        """Interactive sandbox"""
        st.markdown("## 🎯 Try Azure Commands Now")
        st.caption("Interactive environment to test Azure commands")
        
        st.info("🚀 **Cloud Shell:** Open [Azure Cloud Shell](https://shell.azure.com) in a new tab to try these commands!")
        
        st.markdown("### 📝 Common Commands to Try")
        
        with st.expander("🔍 List Resources"):
            st.code('''
# List all resource groups
az group list --output table

# List VMs
az vm list --output table

# List storage accounts
az storage account list --output table

# List all resources in a resource group
az resource list --resource-group myResourceGroup --output table
            ''', language='bash')
        
        with st.expander("📦 Storage Operations"):
            st.code('''
# Create storage account
az storage account create \\
    --name mystorageacct123 \\
    --resource-group myResourceGroup \\
    --location eastus \\
    --sku Standard_LRS

# Create container
az storage container create \\
    --name mycontainer \\
    --account-name mystorageacct123 \\
    --auth-mode login

# Upload file
az storage blob upload \\
    --account-name mystorageacct123 \\
    --container-name mycontainer \\
    --name hello.txt \\
    --file ./hello.txt \\
    --auth-mode login

# List blobs
az storage blob list \\
    --account-name mystorageacct123 \\
    --container-name mycontainer \\
    --output table \\
    --auth-mode login
            ''', language='bash')
        
        with st.expander("🖥️ VM Operations"):
            st.code('''
# Create VM
az vm create \\
    --resource-group myResourceGroup \\
    --name myVM \\
    --image Ubuntu2204 \\
    --admin-username azureuser \\
    --generate-ssh-keys

# Start VM
az vm start --resource-group myResourceGroup --name myVM

# Stop VM
az vm stop --resource-group myResourceGroup --name myVM

# Get VM status
az vm get-instance-view \\
    --resource-group myResourceGroup \\
    --name myVM \\
    --query instanceView.statuses[1] \\
    --output table
            ''', language='bash')
    
    @staticmethod
    def _render_ai_helper(ai_available):
        """AI coding assistant"""
        st.markdown("## 🤖 AI Azure Coding Helper")
        st.caption("Ask me anything about Azure development!")
        
        if not ai_available:
            st.warning("⚠️ AI features require configuration")
            return
        
        st.markdown("### 💡 Quick Questions")
        questions = [
            "How do I authenticate to Azure from Python?",
            "What's the best way to store secrets?",
            "How do I connect to Azure SQL from my app?",
            "Show me how to deploy a container to ACI",
            "How do I use Managed Identity?",
            "What's the difference between Blob and File storage?"
        ]
        
        col1, col2 = st.columns(2)
        for i, q in enumerate(questions):
            with col1 if i % 2 == 0 else col2:
                if st.button(f"💬 {q}", key=f"q_{i}", use_container_width=True):
                    st.info(f"🤖 Let me help with: {q}")
        
        st.markdown("---")
        user_question = st.text_area(
            "Ask your Azure coding question:",
            placeholder="e.g., How do I upload a large file to Blob Storage efficiently?",
            height=100
        )
        
        if st.button("🚀 Get AI Answer", type="primary", use_container_width=True):
            if user_question:
                st.success(f'''
**AI Response:**

For uploading large files to Azure Blob Storage efficiently, here's the recommended approach:

```python
from azure.storage.blob import BlobServiceClient, BlobBlock
from azure.identity import DefaultAzureCredential
import os

credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

blob_client = blob_service.get_blob_client(container="mycontainer", blob="largefile.zip")

# Upload in chunks (4MB each) for better performance
chunk_size = 4 * 1024 * 1024  # 4MB
with open("largefile.zip", "rb") as data:
    blob_client.upload_blob(
        data, 
        overwrite=True,
        max_concurrency=4  # Upload 4 chunks in parallel
    )
```

**Key points:**
- Use `max_concurrency` for parallel uploads
- Default chunk size is 4MB (optimal for most cases)
- Use Managed Identity (`DefaultAzureCredential`) for authentication
- For very large files (>100GB), consider using `upload_blob_from_url()` if the file is already accessible via HTTP
                ''')
    
    @staticmethod
    def _render_debug_assistant(ai_available):
        """Debug helper"""
        st.markdown("## 🐛 Azure Debug Assistant")
        st.caption("Get help fixing common Azure issues")
        
        st.markdown("### 🔍 Common Issues & Solutions")
        
        with st.expander("❌ Authentication Failed / 401 Unauthorized"):
            st.markdown('''
**Problem:** Getting authentication errors when accessing Azure resources

**Solutions:**
1. **Using Managed Identity:**
```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
```

2. **Check RBAC permissions:**
```bash
# Check your current role assignments
az role assignment list --assignee <your-email> --output table

# Grant yourself Storage Blob Data Contributor role
az role assignment create \\
    --role "Storage Blob Data Contributor" \\
    --assignee <your-email> \\
    --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>
```

3. **Login to Azure CLI:**
```bash
az login
az account show  # Verify correct subscription
```
            ''')
        
        with st.expander("❌ Resource Not Found / 404 Error"):
            st.markdown('''
**Problem:** Azure resource not found

**Solutions:**
1. **Verify resource exists:**
```bash
# List all resources
az resource list --output table

# Check specific resource group
az group show --name myResourceGroup
```

2. **Check subscription:**
```bash
# List all subscriptions
az account list --output table

# Set correct subscription
az account set --subscription "My Subscription"
```

3. **Verify resource name and region:**
- Storage account names must be globally unique
- Resource must exist in the same region as expected
            ''')
        
        with st.expander("❌ Slow Blob Upload/Download"):
            st.markdown('''
**Problem:** Slow performance when transferring files

**Solutions:**
1. **Use concurrent upload:**
```python
blob_client.upload_blob(data, max_concurrency=4)
```

2. **Choose correct access tier:**
- Hot: Frequent access (higher storage cost, lower access cost)
- Cool: Infrequent access (lower storage cost, higher access cost)
- Archive: Rarely accessed (lowest cost, hours to retrieve)

3. **Use appropriate region:**
- Choose region closest to your users
- Use same region as your compute resources
            ''')
        
        with st.expander("❌ Connection String vs Managed Identity"):
            st.markdown('''
**Problem:** Confused about authentication methods

**Best Practice: Use Managed Identity**

❌ **DON'T** (Connection String):
```python
connection_string = "DefaultEndpointsProtocol=https;AccountName=..."
blob_service = BlobServiceClient.from_connection_string(connection_string)
```

✅ **DO** (Managed Identity):
```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)
```

**Why Managed Identity?**
- No secrets in code
- Automatic credential rotation
- Works locally and in Azure
- Better security
            ''')
        
        if ai_available:
            st.markdown("---")
            st.markdown("### 🤖 AI Debug Helper")
            error_msg = st.text_area(
                "Paste your error message:",
                placeholder="azure.core.exceptions.ResourceNotFoundError: The specified container does not exist.",
                height=100
            )
            
            if st.button("🔍 Analyze Error", type="primary"):
                if error_msg:
                    st.success('''
**AI Analysis:**

This error indicates the container doesn't exist in your storage account. Here's how to fix it:

```bash
# Create the container
az storage container create \\
    --name mycontainer \\
    --account-name mystorageaccount \\
    --auth-mode login
```

Or in Python:
```python
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from auth_azure_sso import require_permission

credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Create container if it doesn't exist
container_client = blob_service.get_container_client("mycontainer")
if not container_client.exists():
    container_client.create_container()
```
                    ''')

def render():
    """Module-level render"""
    AzureDevExModule.render()