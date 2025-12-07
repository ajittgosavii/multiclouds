"""
Google Cloud Database Operations - AI-Powered Database Management
Intelligent query optimization, performance tuning, scaling, and cost management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gcp_theme import GCPTheme
from config_settings import AppConfig

class GCPDatabaseModule:
    """AI-Enhanced GCP Database Intelligence"""
    
    @staticmethod
    def render():
        """Render GCP Database Intelligence Center"""
        
        GCPTheme.gcp_header(
            "Cloud Database Operations",
            "AI-Powered Database Management - Optimize queries, tune performance, scale resources",
            "💾"
        )
        
        projects = AppConfig.load_gcp_projects()
        
        if st.session_state.get('mode') == 'Demo':
            GCPTheme.gcp_info_box("Demo Mode", "Using sample database data", "info")
        
        tabs = st.tabs(["💾 Databases", "📊 Performance", "🔍 Query Optimization", "📈 Scaling", "💰 Cost Management", "🤖 AI Insights", "📤 Reports"])
        
        with tabs[0]:
            GCPDatabaseModule._render_databases(projects)
        with tabs[1]:
            GCPDatabaseModule._render_performance(projects)
        with tabs[2]:
            GCPDatabaseModule._render_queries(projects)
        with tabs[3]:
            GCPDatabaseModule._render_scaling(projects)
        with tabs[4]:
            GCPDatabaseModule._render_cost(projects)
        with tabs[5]:
            GCPDatabaseModule._render_ai_insights()
        with tabs[6]:
            GCPDatabaseModule._render_reports(projects)
    
    @staticmethod
    def _render_databases(projects):
        """Database overview"""
        
        GCPTheme.gcp_section_header("💾 Database Overview", "🗄️")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Databases", "52", delta="↑ 4")
        with col2:
            st.metric("Cloud SQL", "34", delta="65%")
        with col3:
            st.metric("Firestore", "11", delta="21%")
        with col4:
            st.metric("Spanner", "7", delta="14%")
        with col5:
            st.metric("Health Score", "89/100", delta="↑ 6")
        
        st.markdown("---")
        
        # Database list
        st.markdown("### 🗄️ Database Inventory")
        
        databases = [
            {"Database": "prod-sql-mysql", "Type": "Cloud SQL", "Size": "1.8 TB", "Tier": "db-n1-highmem-4", "Status": "✅ Online", "Cost/mo": "$2,840"},
            {"Database": "orders-firestore", "Type": "Firestore", "Size": "624 GB", "Mode": "Native", "Status": "✅ Online", "Cost/mo": "$1,240"},
            {"Database": "analytics-postgres", "Type": "Cloud SQL", "Size": "3.2 TB", "Tier": "db-n1-highmem-8", "Status": "✅ Online", "Cost/mo": "$4,680"},
            {"Database": "test-mysql-01", "Type": "Cloud SQL", "Size": "180 GB", "Tier": "db-n1-standard-1", "Status": "⚠️ Slow", "Cost/mo": "$340"}
        ]
        st.dataframe(pd.DataFrame(databases), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Database Distribution")
            db_types = {"Type": ["Cloud SQL", "Firestore", "Spanner"], "Count": [34, 11, 7]}
            fig = px.pie(db_types, values='Count', names='Type', hole=0.4, color_discrete_sequence=['#4285F4', '#34A853', '#FBBC04'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 Cost by Type")
            costs = {"Type": ["Cloud SQL", "Firestore", "Spanner"], "Cost": [18420, 5680, 9240]}
            fig = px.bar(costs, x='Type', y='Cost', title='Monthly Cost ($)')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_performance(projects):
        """Performance monitoring"""
        
        GCPTheme.gcp_section_header("📊 Performance Monitoring", "⚡")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Query Time", "187ms", delta="↓ 38ms")
        with col2:
            st.metric("CPU Usage", "62%", delta="↑ 7%")
        with col3:
            st.metric("Storage Used", "71%", delta="↑ 4%")
        with col4:
            st.metric("Active Connections", "1,247", delta="↑ 89")
        
        st.markdown("---")
        
        # Performance issues
        st.markdown("### ⚠️ Performance Issues")
        
        issues = [
            {"Database": "prod-sql-mysql", "Issue": "High CPU usage", "Impact": "Query latency", "Severity": "High", "Duration": "38 min"},
            {"Database": "orders-firestore", "Issue": "Index missing", "Impact": "Full collection scans", "Severity": "Critical", "Duration": "2 days"},
            {"Database": "analytics-postgres", "Issue": "Slow SELECT", "Impact": "Report delays", "Severity": "Medium", "Duration": "5 hours"}
        ]
        
        for issue in issues:
            severity_colors = {"Critical": "🔴", "High": "🟠", "Medium": "🟡"}
            with st.expander(f"{severity_colors[issue['Severity']]} **{issue['Database']}** - {issue['Issue']}"):
                st.write(f"**Impact:** {issue['Impact']}")
                st.write(f"**Duration:** {issue['Duration']}")
                if st.button("🔧 Optimize", key=f"gcp_perf_{issue['Database']}", use_container_width=True):
                    st.success("✅ Optimization applied (Demo)")
        
        st.markdown("---")
        
        # CPU trend
        st.markdown("### 📈 CPU Usage Trend (24h)")
        times = pd.date_range(end=datetime.now(), periods=24, freq='H')
        cpu = [55 + (i % 12) for i in range(24)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=cpu, mode='lines', fill='tonexty', line=dict(color='#4285F4')))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Threshold")
        fig.update_layout(yaxis_title='CPU %', height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_queries(projects):
        """Query optimization"""
        
        GCPTheme.gcp_section_header("🔍 Query Optimization", "🎯")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Queries", "3.8M/day", delta="↑ 240K")
        with col2:
            st.metric("Slow Queries", "1,247", delta="↓ 340")
        with col3:
            st.metric("Avg Duration", "187ms", delta="↓ 38ms")
        
        st.markdown("---")
        
        # Slow queries
        st.markdown("### 🐌 Slowest Queries")
        
        queries = [
            {"Query": "SELECT * FROM orders WHERE status = ?", "Avg Time": "5,840ms", "Executions": "18,450", "Database": "prod-sql-mysql", "Fix": "Add index on status"},
            {"Query": "SELECT o.*, c.* FROM orders o JOIN customers c...", "Avg Time": "3,240ms", "Executions": "12,340", "Database": "prod-sql-mysql", "Fix": "Optimize JOIN"},
            {"Query": "firestore: collection('orders').where('status', '==', ...)", "Avg Time": "2,180ms", "Executions": "34,670", "Database": "orders-firestore", "Fix": "Create composite index"}
        ]
        
        for i, q in enumerate(queries):
            with st.expander(f"**Query #{i+1}** - {q['Avg Time']} avg • {q['Executions']} executions"):
                st.code(q['Query'], language='sql' if 'SELECT' in q['Query'] else 'javascript')
                st.write(f"**Database:** {q['Database']}")
                st.write(f"**AI Recommendation:** {q['Fix']}")
                if st.button("🔧 Apply Fix", key=f"gcp_query_{i}", use_container_width=True):
                    st.success("✅ Fix applied (Demo)")
    
    @staticmethod
    def _render_scaling(projects):
        """Scaling recommendations"""
        
        GCPTheme.gcp_section_header("📈 Scaling Recommendations", "🚀")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Auto-Scale Enabled", "31", delta="60%")
        with col2:
            st.metric("Manual Scale Events", "18", delta="Last 30d")
        with col3:
            st.metric("Potential Savings", "$3,120/mo", delta="Right-sizing")
        
        st.markdown("---")
        
        # Scaling opportunities
        st.markdown("### 📊 Scaling Opportunities")
        
        opportunities = [
            {"Database": "prod-sql-mysql", "Current": "db-n1-highmem-4", "Recommended": "db-n1-highmem-2", "Reason": "Avg CPU 52%", "Savings": "$1,120/mo"},
            {"Database": "analytics-postgres", "Current": "db-n1-highmem-8", "Recommended": "db-n1-standard-8", "Reason": "Memory underutilized", "Savings": "$890/mo"},
            {"Database": "test-mysql-01", "Current": "db-n1-standard-1", "Recommended": "db-f1-micro", "Reason": "Test environment", "Savings": "$180/mo"}
        ]
        st.dataframe(pd.DataFrame(opportunities), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_cost(projects):
        """Cost management"""
        
        GCPTheme.gcp_section_header("💰 Cost Management", "💵")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Monthly", "$33,340", delta="All databases")
        with col2:
            st.metric("Optimized", "$28,760", delta="-$4,580/mo")
        with col3:
            st.metric("Savings", "14%", delta="Potential")
        
        st.markdown("---")
        
        # Cost breakdown
        st.markdown("### 💰 Cost Breakdown")
        
        costs = [
            {"Database": "prod-sql-mysql", "Type": "Cloud SQL", "Current": "$2,840", "Optimized": "$1,720", "Savings": "$1,120"},
            {"Database": "analytics-postgres", "Type": "Cloud SQL", "Current": "$4,680", "Optimized": "$3,790", "Savings": "$890"},
            {"Database": "orders-firestore", "Type": "Firestore", "Current": "$1,240", "Optimized": "$920", "Savings": "$320"}
        ]
        st.dataframe(pd.DataFrame(costs), use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_ai_insights():
        """AI insights"""
        
        GCPTheme.gcp_section_header("🤖 AI-Powered Database Insights", "🧠")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Confidence", "98%", delta="↑ 2%")
        with col2:
            st.metric("Recommendations", "11", delta="↑ 3")
        with col3:
            st.metric("Query Optimizations", "15", delta="↑ 5")
        with col4:
            st.metric("Cost Savings", "$4,580/mo", delta="14%")
        
        st.markdown("---")
        st.markdown("### 💡 AI Recommendations")
        
        recs = [
            {"title": "Add Composite Index", "desc": "Firestore query scanning entire collection (34K docs). Composite index on status + timestamp needed.", "impact": "Query time: 2.18s → 45ms (95% faster)", "confidence": 100, "auto_fix": True},
            {"title": "Right-Size Machine Type", "desc": "prod-sql-mysql using avg 52% CPU. db-n1-highmem-2 sufficient based on 30-day analysis.", "impact": "Save $1,120/month (39% cost reduction)", "confidence": 98, "auto_fix": True},
            {"title": "Enable Query Insights", "desc": "Analytics database missing Query Insights. AI-powered recommendations available.", "impact": "Automatic query optimization suggestions", "confidence": 96, "auto_fix": True},
            {"title": "Implement Read Replicas", "desc": "70% of queries are SELECT. Read replica in us-west1 reduces latency 3x.", "impact": "Reduce read latency from 187ms to 62ms", "confidence": 94, "auto_fix": False}
        ]
        
        for i, rec in enumerate(recs):
            with st.expander(f"**{rec['title']}** - {rec['impact']} • {rec['confidence']}%"):
                st.write(f"**Analysis:** {rec['desc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if rec['auto_fix']:
                        if st.button("✅ Apply", key=f"gcp_db_{i}"):
                            st.success("Applied! (Demo)")
                    else:
                        if st.button("📋 Guide", key=f"guide_{i}"):
                            st.info("Implementation guide shown")
                with col2:
                    if st.button("📊 Simulate", key=f"sim_{i}"):
                        st.info("Impact simulation shown")
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        
        query = st.text_area("Ask about database operations:", height=80, key="gcp_db_query")
        
        if st.button("🤖 Ask AI", type="primary"):
            if query:
                st.markdown(GCPDatabaseModule._generate_ai_response(query))
    
    @staticmethod
    def _render_reports(projects):
        """Reports"""
        
        GCPTheme.gcp_section_header("📤 Reports", "📊")
        
        if st.button("📥 Generate Report"):
            st.success("✅ Report generated (Demo)")
    
    @staticmethod
    def _generate_ai_response(query: str):
        """AI response"""
        
        q = query.lower()
        
        if "slow" in q or "performance" in q or "query" in q:
            return """**🔍 Query Performance Analysis:**

**Slowest Query:** SELECT * FROM orders WHERE status = ?  
**Avg Time:** 5.84 seconds  
**Executions:** 18,450/day

**AI Root Cause:**
- Full table scan: 1.8M rows
- No index on status column
- Missing query optimization

**Fix:**
```sql
-- Add index
CREATE INDEX idx_orders_status 
ON orders(status);

-- Optional: Add covering index
CREATE INDEX idx_orders_status_date 
ON orders(status, order_date) 
INCLUDE (id, total);
```

**Firestore Alternative:**
```javascript
// Create composite index
firestore.collection('orders')
  .createIndex({
    fields: [
      {fieldPath: 'status', order: 'ASCENDING'},
      {fieldPath: 'timestamp', order: 'DESCENDING'}
    ]
  });
```

**Expected Impact:**
- Query time: 5.84s → 45ms (99% faster)
- Rows scanned: 1.8M → 1,234 (99.93% reduction)
- CPU savings: 31% reduction**"""
        
        elif "cost" in q or "save" in q:
            return """**💰 Database Cost Optimization:**

**Current:** $33,340/month  
**Optimized:** $28,760/month  
**Savings:** $4,580/month (14%)

**AI-Identified Opportunities:**

1. **Right-Size Machine Type** ($1,120/mo)
   - Database: prod-sql-mysql
   - Current: db-n1-highmem-4
   - Recommended: db-n1-highmem-2
   - Avg CPU: 52%, Memory: 48%

2. **Optimize Memory Tier** ($890/mo)
   - Database: analytics-postgres
   - Current: db-n1-highmem-8
   - Recommended: db-n1-standard-8
   - Memory utilization: 34%

3. **Firestore Optimization** ($320/mo)
   - Database: orders-firestore
   - Recommendation: Add indexes to reduce reads
   - Current: 34K document scans
   - Optimized: 1.2K indexed reads

**GCP-Specific:**
- Committed use discounts available
- Consider Spanner for global distribution
- Use Cloud SQL Insights for ongoing optimization

**Quick Wins:** All 3 optimizations auto-fixable**"""
        
        elif "firestore" in q or "index" in q:
            return """**🔥 Firestore Optimization:**

**Issue:** Collection scans on orders collection

**Current Performance:**
- Query: where('status', '==', 'pending')
- Avg time: 2.18 seconds
- Documents scanned: 34,670

**AI Recommendation: Composite Index**

```javascript
// Create in Firebase Console or via CLI
{
  collectionGroup: "orders",
  queryScope: "COLLECTION",
  fields: [
    { fieldPath: "status", order: "ASCENDING" },
    { fieldPath: "timestamp", order: "DESCENDING" }
  ]
}
```

**Alternative: Single Field Index**
```bash
gcloud firestore indexes composite create \\
  --collection-group=orders \\
  --field-config field-path=status,order=ascending \\
  --field-config field-path=timestamp,order=descending
```

**Expected Results:**
- Query time: 2.18s → 45ms (95% faster)
- Reads: 34,670 → 1,234 (96% reduction)
- Cost: $320/month savings**"""
        
        return f"AI analysis for: {query}"

# Module-level render function for navigation compatibility
def render():
    """Module-level render function"""
    GCPDatabaseModule.render()
