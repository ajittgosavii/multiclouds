"""
GCP Developer Experience (DevEx) - Your Coding Assistant
Practical tools, ready-to-use code, and AI help for GCP developers
"""

import streamlit as st
import json
import uuid

class GCPDevExModule:
    """GCP Developer Experience - Practical Coding Helper"""
    
    @staticmethod
    @require_permission('use_devex')

    def render():
        """Render GCP DevEx module"""
        
        if 'gcp_devex_session_id' not in st.session_state:
            st.session_state.gcp_devex_session_id = str(uuid.uuid4())[:8]
        
        st.title("👨‍💻 GCP Developer Experience")
        st.markdown("**Your coding assistant** - Copy-paste code, generate commands, get instant help")
        
        ai_available = True
        
        if ai_available:
            st.success("🤖 **AI Assistant: READY** | Ask coding questions | Generate GCP code | Debug issues")
        
        tabs = st.tabs([
            "🏠 Dev Portal",
            "📚 Quick Reference",
            "💻 Code Generator",
            "🔧 gcloud Commands",
            "🚀 Getting Started",
            "🎯 Try It Now",
            "🤖 AI Helper",
            "🐛 Debug Assistant"
        ])
        
        with tabs[0]:
            GCPDevExModule._render_developer_portal()
        with tabs[1]:
            GCPDevExModule._render_quick_reference()
        with tabs[2]:
            GCPDevExModule._render_code_generator()
        with tabs[3]:
            GCPDevExModule._render_gcloud_commands()
        with tabs[4]:
            GCPDevExModule._render_getting_started()
        with tabs[5]:
            GCPDevExModule._render_try_it_now()
        with tabs[6]:
            GCPDevExModule._render_ai_helper(ai_available)
        with tabs[7]:
            GCPDevExModule._render_debug_assistant(ai_available)
    
    @staticmethod
    def _render_developer_portal():
        """Developer portal hub"""
        st.markdown("## 🏠 GCP Developer Portal")
        st.caption("Your one-stop shop for GCP development")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🚀 Quick Actions")
            if st.button("📋 Generate gcloud command", use_container_width=True):
                st.info("Jump to gcloud Commands tab →")
            if st.button("💻 Get code snippet", use_container_width=True):
                st.info("Jump to Code Generator tab →")
            if st.button("🐛 Debug my issue", use_container_width=True):
                st.info("Jump to Debug Assistant tab →")
            if st.button("🤖 Ask AI", use_container_width=True):
                st.info("Jump to AI Helper tab →")
        
        with col2:
            st.markdown("### 📚 Popular Resources")
            st.markdown("""
            - [Google Cloud Python SDK](https://cloud.google.com/python/docs/reference)
            - [Google Cloud Java SDK](https://cloud.google.com/java/docs/reference)
            - [Google Cloud Go SDK](https://pkg.go.dev/cloud.google.com/go)
            - [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
            - [Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
            - [REST API Reference](https://cloud.google.com/apis/docs/overview)
            """)
        
        with col3:
            st.markdown("### 💡 Common Tasks")
            st.markdown("""
            **Storage:**
            - Upload to Cloud Storage
            - List bucket contents
            - Generate signed URLs
            
            **Compute:**
            - Create VM instance
            - Deploy Cloud Run service
            - Manage GKE cluster
            
            **Database:**
            - Connect to Cloud SQL
            - Query Firestore
            - Use BigQuery
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 Today's Tips")
        
        tips = [
            "💡 **Tip:** Use Application Default Credentials (ADC) for seamless authentication",
            "💡 **Tip:** Add `--format=json` or `--format=table` to gcloud commands for better output",
            "💡 **Tip:** Use Workload Identity instead of service account keys in GKE",
            "💡 **Tip:** Enable Cloud Trace and Cloud Profiler for automatic performance insights"
        ]
        
        for tip in tips:
            st.info(tip)
    
    @staticmethod
    def _render_quick_reference():
        """Quick reference guide"""
        st.markdown("## 📚 GCP Quick Reference")
        st.caption("Common patterns and examples you can copy-paste")
        
        category = st.selectbox("Select Category", [
            "Storage (Cloud Storage, Filestore)",
            "Compute (Compute Engine, Cloud Run)",
            "Database (Cloud SQL, Firestore, BigQuery)",
            "Messaging (Pub/Sub)",
            "Identity (IAM, Workload Identity)",
            "Monitoring (Cloud Logging, Trace)"
        ])
        
        if "Storage" in category:
            st.markdown("### 📦 Cloud Storage - Python")
            st.code('''
from google.cloud import storage

# Using Application Default Credentials (recommended)
client = storage.Client()

# Upload file
bucket = client.bucket('my-bucket')
blob = bucket.blob('myfile.txt')
blob.upload_from_filename('local_file.txt')
print(f'File uploaded to gs://my-bucket/myfile.txt')

# Download file
blob.download_to_filename('downloaded.txt')

# List blobs
for blob in client.list_blobs('my-bucket'):
    print(blob.name)

# Generate signed URL (1 hour expiry)
from datetime import timedelta
url = blob.generate_signed_url(expiration=timedelta(hours=1))
print(f'Signed URL: {url}')
            ''', language='python')
            
            st.markdown("### 📦 Cloud Storage - Go")
            st.code('''
package main

import (
    "context"
    "cloud.google.com/go/storage"
    "io"
    "os"
)

func uploadFile(bucketName, objectName, filename string) error {
    ctx := context.Background()
    client, _ := storage.NewClient(ctx)
    defer client.Close()
    
    // Upload
    f, _ := os.Open(filename)
    defer f.Close()
    
    wc := client.Bucket(bucketName).Object(objectName).NewWriter(ctx)
    if _, err := io.Copy(wc, f); err != nil {
        return err
    }
    return wc.Close()
}
            ''', language='go')
        
        elif "Compute" in category:
            st.markdown("### 🚀 Cloud Run - Python Flask")
            st.code('''
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    name = os.environ.get('NAME', 'World')
    return f'Hello {name} from Cloud Run!'

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# requirements.txt
# Flask==2.3.0
# gunicorn==21.2.0

# Dockerfile
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY app.py .
# CMD exec gunicorn --bind :$PORT app:app

# Deploy:
# gcloud run deploy myapp --source . --region us-central1 --allow-unauthenticated
            ''', language='python')
        
        elif "Database" in category:
            st.markdown("### 🗄️ Cloud SQL Connection - Python")
            st.code('''
import sqlalchemy
from google.cloud.sql.connector import Connector

# Using Cloud SQL Python Connector (recommended)
connector = Connector()

def getconn():
    return connector.connect(
        "project:region:instance",
        "pymysql",
        user="myuser",
        password="mypassword",
        db="mydb"
    )

# Create SQLAlchemy engine
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Query
with engine.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT * FROM users"))
    for row in result:
        print(row)

# Clean up
connector.close()
            ''', language='python')
            
            st.markdown("### 📊 BigQuery - Python")
            st.code('''
from google.cloud import bigquery

client = bigquery.Client()

# Query
query = """
    SELECT name, COUNT(*) as count
    FROM `project.dataset.table`
    WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    GROUP BY name
    ORDER BY count DESC
    LIMIT 10
"""

results = client.query(query)
for row in results:
    print(f"{row.name}: {row.count}")

# Insert data
rows_to_insert = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
table_id = "project.dataset.table"
errors = client.insert_rows_json(table_id, rows_to_insert)
if errors:
    print(f"Errors: {errors}")
            ''', language='python')
        
        elif "Messaging" in category:
            st.markdown("### 📬 Pub/Sub - Publish Message")
            st.code('''
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project', 'my-topic')

# Publish message
data = {"user_id": 123, "action": "login"}
message_bytes = json.dumps(data).encode('utf-8')
future = publisher.publish(topic_path, message_bytes, origin='python-app')
print(f'Published message ID: {future.result()}')

# Subscribe to messages
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('my-project', 'my-subscription')

def callback(message):
    print(f'Received: {message.data.decode("utf-8")}')
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print('Listening for messages...')

# Keep listening (blocks)
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
            ''', language='python')
        
        st.markdown("---")
        st.info("💡 **Pro Tip:** Use Application Default Credentials (ADC) - no need to manage service account keys!")
    
    @staticmethod
    def _render_code_generator():
        """Interactive code generator"""
        st.markdown("## 💻 GCP Code Generator")
        st.caption("Generate ready-to-use code for common tasks")
        
        task = st.selectbox("What do you want to do?", [
            "Upload file to Cloud Storage",
            "Query BigQuery",
            "Publish to Pub/Sub",
            "Connect to Cloud SQL",
            "Deploy Cloud Run service",
            "Create VM instance",
            "Use Secret Manager"
        ])
        
        language = st.selectbox("Programming Language", ["Python", "Go", "Java", "Node.js", "gcloud CLI"])
        
        if task == "Upload file to Cloud Storage":
            bucket = st.text_input("Bucket Name", "my-bucket")
            
            if language == "Python":
                code = f'''
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('{bucket}')
blob = bucket.blob('myfile.txt')

# Upload from file
blob.upload_from_filename('local_file.txt')
print(f'Uploaded to gs://{bucket}/myfile.txt')

# Upload from string
blob.upload_from_string('Hello GCP!', content_type='text/plain')

# Make public (optional)
blob.make_public()
print(f'Public URL: {{blob.public_url}}')
'''
            elif language == "gcloud CLI":
                code = f'''
# Upload single file
gsutil cp local_file.txt gs://{bucket}/

# Upload directory
gsutil -m cp -r ./local_directory gs://{bucket}/

# Set public access
gsutil acl ch -u AllUsers:R gs://{bucket}/myfile.txt

# List files
gsutil ls gs://{bucket}/
'''
            else:
                code = "# Code generation for this language coming soon!"
            
            st.code(code, language='python' if language == "Python" else 'bash')
            st.button("📋 Copy to Clipboard")
        
        elif task == "Deploy Cloud Run service":
            service_name = st.text_input("Service Name", "myapp")
            region = st.selectbox("Region", ["us-central1", "us-east1", "europe-west1", "asia-southeast1"])
            
            code = f'''
# Build and deploy from source
gcloud run deploy {service_name} \\
    --source . \\
    --region {region} \\
    --allow-unauthenticated

# Deploy from container image
gcloud run deploy {service_name} \\
    --image gcr.io/my-project/myapp:latest \\
    --region {region} \\
    --platform managed \\
    --memory 512Mi \\
    --cpu 1 \\
    --max-instances 10 \\
    --allow-unauthenticated

# Get service URL
gcloud run services describe {service_name} \\
    --region {region} \\
    --format 'value(status.url)'
'''
            st.code(code, language='bash')
            st.success("✅ Generated! Run this in Cloud Shell or your terminal")
    
    @staticmethod
    def _render_gcloud_commands():
        """gcloud CLI command helper"""
        st.markdown("## 🔧 gcloud Command Helper")
        st.caption("Build gcloud commands interactively")
        
        service = st.selectbox("GCP Service", [
            "Cloud Storage",
            "Compute Engine",
            "Cloud Run",
            "Cloud SQL",
            "GKE (Kubernetes)",
            "BigQuery"
        ])
        
        operation = st.selectbox("Operation", ["Create", "List", "Describe", "Delete", "Update"])
        
        if service == "Cloud Storage" and operation == "Create":
            st.markdown("### Configure Bucket Creation")
            bucket_name = st.text_input("Bucket Name", "my-bucket-12345")
            location = st.selectbox("Location", ["us-central1", "us-east1", "europe-west1", "asia-southeast1", "multi-region-us"])
            storage_class = st.selectbox("Storage Class", ["STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"])
            
            cmd = f'''gsutil mb -c {storage_class} -l {location} gs://{bucket_name}/'''
            
            st.code(cmd, language='bash')
            st.info("💡 Run this command in Cloud Shell or your terminal")
        
        elif service == "Compute Engine" and operation == "Create":
            instance_name = st.text_input("Instance Name", "my-instance")
            zone = st.selectbox("Zone", ["us-central1-a", "us-east1-b", "europe-west1-b"])
            machine_type = st.selectbox("Machine Type", ["e2-micro", "e2-small", "e2-medium", "n2-standard-2"])
            image = st.selectbox("Image Family", ["debian-11", "ubuntu-2204-lts", "centos-stream-9"])
            
            cmd = f'''gcloud compute instances create {instance_name} \\
    --zone={zone} \\
    --machine-type={machine_type} \\
    --image-family={image} \\
    --image-project=debian-cloud \\
    --boot-disk-size=10GB \\
    --tags=http-server,https-server

# Get external IP
gcloud compute instances describe {instance_name} \\
    --zone={zone} \\
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
'''
            st.code(cmd, language='bash')
    
    @staticmethod
    def _render_getting_started():
        """Getting started guide"""
        st.markdown("## 🚀 Getting Started with GCP Development")
        
        st.markdown("### 1️⃣ Install Google Cloud SDK")
        st.code('''
# macOS
brew install google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Windows
# Download from: https://cloud.google.com/sdk/docs/install

# Verify installation
gcloud --version
        ''', language='bash')
        
        st.markdown("### 2️⃣ Initialize gcloud")
        st.code('''
# Initialize and login
gcloud init

# Or login separately
gcloud auth login

# Set default project
gcloud config set project my-project-id

# Set default region
gcloud config set compute/region us-central1

# Enable Application Default Credentials
gcloud auth application-default login
        ''', language='bash')
        
        st.markdown("### 3️⃣ Install Python Client Libraries")
        st.code('''
# Install Google Cloud Storage
pip install google-cloud-storage

# Install BigQuery
pip install google-cloud-bigquery

# Install Pub/Sub
pip install google-cloud-pubsub

# Install Cloud SQL connector
pip install cloud-sql-python-connector

# Or install multiple at once
pip install google-cloud-storage google-cloud-bigquery google-cloud-pubsub
        ''', language='bash')
        
        st.markdown("### 4️⃣ Your First GCP Python App")
        st.code('''
from google.cloud import storage

# Application Default Credentials automatically used
client = storage.Client()

# Create bucket
bucket = client.bucket('my-unique-bucket-name')
if not bucket.exists():
    bucket = client.create_bucket('my-unique-bucket-name', location='us-central1')
    print('✅ Bucket created!')

# Upload file
blob = bucket.blob('hello.txt')
blob.upload_from_string('Hello Google Cloud!', content_type='text/plain')
print('✅ File uploaded!')

# List files
print('Files in bucket:')
for blob in client.list_blobs('my-unique-bucket-name'):
    print(f'  - {blob.name}')
        ''', language='python')
        
        st.success("🎉 You're ready to build on Google Cloud!")
    
    @staticmethod
    def _render_try_it_now():
        """Interactive sandbox"""
        st.markdown("## 🎯 Try GCP Commands Now")
        st.caption("Interactive environment to test gcloud commands")
        
        st.info("🚀 **Cloud Shell:** Open [Google Cloud Shell](https://shell.cloud.google.com) in a new tab to try these commands!")
        
        st.markdown("### 📝 Common Commands to Try")
        
        with st.expander("🔍 List Resources"):
            st.code('''
# List projects
gcloud projects list

# List compute instances
gcloud compute instances list

# List Cloud Storage buckets
gsutil ls

# List Cloud Run services
gcloud run services list

# List BigQuery datasets
bq ls
            ''', language='bash')
        
        with st.expander("📦 Cloud Storage Operations"):
            st.code('''
# Create bucket
gsutil mb -l us-central1 gs://my-bucket-name/

# Upload file
echo "Hello GCP!" > hello.txt
gsutil cp hello.txt gs://my-bucket-name/

# List bucket contents
gsutil ls gs://my-bucket-name/

# Download file
gsutil cp gs://my-bucket-name/hello.txt downloaded.txt

# Make file public
gsutil acl ch -u AllUsers:R gs://my-bucket-name/hello.txt

# Get public URL
echo "https://storage.googleapis.com/my-bucket-name/hello.txt"
            ''', language='bash')
        
        with st.expander("🖥️ Compute Engine Operations"):
            st.code('''
# Create VM
gcloud compute instances create my-instance \\
    --zone=us-central1-a \\
    --machine-type=e2-micro \\
    --image-family=debian-11 \\
    --image-project=debian-cloud

# Start instance
gcloud compute instances start my-instance --zone=us-central1-a

# Stop instance
gcloud compute instances stop my-instance --zone=us-central1-a

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# Delete instance
gcloud compute instances delete my-instance --zone=us-central1-a
            ''', language='bash')
        
        with st.expander("🚀 Cloud Run Operations"):
            st.code('''
# Deploy from source
gcloud run deploy myapp \\
    --source . \\
    --region us-central1 \\
    --allow-unauthenticated

# Deploy from container
gcloud run deploy myapp \\
    --image gcr.io/cloudrun/hello \\
    --region us-central1 \\
    --allow-unauthenticated

# Get service URL
gcloud run services describe myapp \\
    --region us-central1 \\
    --format 'value(status.url)'

# View logs
gcloud run services logs read myapp --region us-central1
            ''', language='bash')
    
    @staticmethod
    def _render_ai_helper(ai_available):
        """AI coding assistant"""
        st.markdown("## 🤖 AI GCP Coding Helper")
        st.caption("Ask me anything about GCP development!")
        
        if not ai_available:
            st.warning("⚠️ AI features require configuration")
            return
        
        st.markdown("### 💡 Quick Questions")
        questions = [
            "How do I authenticate to GCP from Python?",
            "What's the best way to store secrets in GCP?",
            "How do I deploy a containerized app?",
            "Show me how to use Pub/Sub",
            "How do I use Application Default Credentials?",
            "What's the difference between Cloud Storage classes?"
        ]
        
        col1, col2 = st.columns(2)
        for i, q in enumerate(questions):
            with col1 if i % 2 == 0 else col2:
                if st.button(f"💬 {q}", key=f"q_{i}", use_container_width=True):
                    st.info(f"🤖 Let me help with: {q}")
        
        st.markdown("---")
        user_question = st.text_area(
            "Ask your GCP coding question:",
            placeholder="e.g., How do I stream large files from Cloud Storage?",
            height=100
        )
        
        if st.button("🚀 Get AI Answer", type="primary", use_container_width=True):
            if user_question:
                st.success(f'''
**AI Response:**

To stream large files from Cloud Storage efficiently:

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('large-file.bin')

# Stream download (doesn't load entire file into memory)
with blob.open('rb') as f:
    # Process in chunks
    chunk_size = 1024 * 1024  # 1MB chunks
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        process_chunk(chunk)  # Your processing logic

# Or download to file with streaming
blob.download_to_filename('local-file.bin', chunk_size=chunk_size)
```

**Key points:**
- Use `blob.open()` for streaming reads
- Process data in chunks to avoid memory issues
- Set appropriate `chunk_size` (1-10MB typically)
- For uploads, use `blob.open('wb')` for streaming writes
                ''')
    
    @staticmethod
    def _render_debug_assistant(ai_available):
        """Debug helper"""
        st.markdown("## 🐛 GCP Debug Assistant")
        st.caption("Get help fixing common GCP issues")
        
        st.markdown("### 🔍 Common Issues & Solutions")
        
        with st.expander("❌ Permission Denied / 403 Forbidden"):
            st.markdown('''
**Problem:** Getting permission errors when accessing GCP resources

**Solutions:**
1. **Check IAM permissions:**
```bash
# List your roles
gcloud projects get-iam-policy my-project \\
    --flatten="bindings[].members" \\
    --filter="bindings.members:user:youremail@example.com" \\
    --format="table(bindings.role)"

# Grant Storage Admin role
gcloud projects add-iam-policy-binding my-project \\
    --member="user:youremail@example.com" \\
    --role="roles/storage.admin"
```

2. **Use Application Default Credentials:**
```bash
# Login with your user account
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

3. **Check if API is enabled:**
```bash
# Enable Cloud Storage API
gcloud services enable storage.googleapis.com

# List enabled APIs
gcloud services list --enabled
```
            ''')
        
        with st.expander("❌ Bucket/Resource Not Found"):
            st.markdown('''
**Problem:** Resource doesn't exist or can't be found

**Solutions:**
1. **Verify bucket exists:**
```bash
# List all buckets
gsutil ls

# Check specific bucket
gsutil ls gs://my-bucket-name/
```

2. **Check project:**
```bash
# View current project
gcloud config get-value project

# List all projects
gcloud projects list

# Switch project
gcloud config set project my-project-id
```

3. **Verify region/location:**
- Buckets must be accessed from correct project
- Some resources are region-specific
            ''')
        
        with st.expander("❌ Service Account Key Issues"):
            st.markdown('''
**Problem:** Issues with service account authentication

**Best Practice: Use Application Default Credentials**

❌ **DON'T** (Service Account Key File):
```python
from google.cloud import storage
client = storage.Client.from_service_account_json('key.json')
```

✅ **DO** (Application Default Credentials):
```python
from google.cloud import storage
client = storage.Client()  # Automatically uses ADC
```

**Setup ADC:**
```bash
# For development
gcloud auth application-default login

# For production (use Workload Identity in GKE)
# No keys needed - automatic!
```

**Why ADC?**
- No key files to manage
- No secrets in code
- Works locally and in GCP
- Automatic in Cloud Run, GKE, Cloud Functions
            ''')
        
        with st.expander("❌ Slow BigQuery Queries"):
            st.markdown('''
**Problem:** BigQuery queries running slowly

**Solutions:**
1. **Use partitioning:**
```sql
CREATE TABLE dataset.table
PARTITION BY DATE(timestamp)
AS SELECT * FROM source_table;

-- Query with partition filter
SELECT * FROM dataset.table
WHERE DATE(timestamp) = '2024-12-01';
```

2. **Use clustering:**
```sql
CREATE TABLE dataset.table
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, region
AS SELECT * FROM source_table;
```

3. **Avoid SELECT *:**
```sql
-- ❌ Don't do this
SELECT * FROM large_table;

-- ✅ Do this
SELECT id, name, timestamp FROM large_table;
```

4. **Use query caching:**
```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(use_query_cache=True)
results = client.query(query, job_config=job_config)
```
            ''')
        
        if ai_available:
            st.markdown("---")
            st.markdown("### 🤖 AI Debug Helper")
            error_msg = st.text_area(
                "Paste your error message:",
                placeholder="google.api_core.exceptions.NotFound: 404 Bucket my-bucket not found",
                height=100
            )
            
            if st.button("🔍 Analyze Error", type="primary"):
                if error_msg:
                    st.success('''
**AI Analysis:**

This error means the Cloud Storage bucket doesn't exist. Here's how to fix it:

```bash
# Create the bucket
gsutil mb -l us-central1 gs://my-bucket/

# Or check if it exists with different name
gsutil ls

# Verify you're in the right project
gcloud config get-value project
```

In Python, create bucket if it doesn't exist:
```python
from google.cloud import storage
from auth_azure_sso import require_permission

client = storage.Client()
bucket_name = 'my-bucket'

bucket = client.bucket(bucket_name)
if not bucket.exists():
    bucket = client.create_bucket(bucket_name, location='us-central1')
    print(f'Created bucket {bucket_name}')
```
                    ''')

def render():
    """Module-level render"""
    GCPDevExModule.render()
