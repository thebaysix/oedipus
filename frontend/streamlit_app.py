import sys
from pathlib import Path

# Add project root to sys.path so 'app' and 'components' are importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import requests
from app.core.config import settings
from components.upload import render_dataset_upload, render_output_upload, render_dataset_selector
from components.dashboard import render_analysis_dashboard
from app.workers.analysis_worker import celery_app, run_analysis_task

# Page configuration
st.set_page_config(
    page_title="Oedipus MVP",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 3rem;
    }
    
    .workflow-step {
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🔬 Oedipus MVP</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Observability & Analytics Infrastructure for AI Systems</p>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["🏠 Home", "📊 Upload Data", "🔬 Analysis", "📈 Dashboard"]
)

# Sidebar: local mode toggle (optional)
use_local_mode = st.sidebar.checkbox("Use Local Mode", value=(settings.OEDIPUS_ENV=="local"))

# API health check
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Display API status
api_healthy = check_api_health()
if api_healthy:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Disconnected")
    st.sidebar.info("Make sure the backend is running:\n`uvicorn app.api.main:app --reload`")

# Helper to submit analysis respecting local mode
def submit_analysis(data):
    if use_local_mode or celery_app is None:
        # Run synchronously for local development
        return run_analysis_task(data)
    else:
        # Queue task with Celery
        return celery_app.send_task("app.workers.analysis_worker.run_analysis_task", args=[data])

# Page routing
if page == "🏠 Home":
    st.header("Welcome to Oedipus MVP")
    
    st.markdown("""
    **Oedipus** is an observability and analytics platform for AI systems. This MVP focuses on 
    bulk upload analysis of AI model outputs, providing comprehensive information-theoretic 
    analysis to understand model behavior patterns.
    """)
    
    # Workflow overview
    st.subheader("📋 Analysis Workflow")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="workflow-step">
            <h4>1. 📊 Upload Input Dataset</h4>
            <p>Upload your input prompts as JSON mapping input IDs to prompt strings.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="workflow-step">
            <h4>2. 🎯 Upload Output Dataset</h4>
            <p>Upload corresponding model outputs as JSON mapping input IDs to output arrays.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="workflow-step">
            <h4>3. 🔬 Run Analysis</h4>
            <p>Get comprehensive information-theoretic metrics and visualizations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features overview
    st.subheader("🚀 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Information-Theoretic Analysis:**
        - Input Entropy
        - Response Entropy  
        - Information Gain
        - Empowerment Metrics
        
        **Basic Statistics:**
        - Character count distributions
        - Token count analysis
        - Output length variance
        """)
    
    with col2:
        st.markdown("""
        **Interactive Visualizations:**
        - Entropy comparison charts
        - Length distribution plots
        - Diversity metrics dashboard
        - Export capabilities (JSON/CSV)
        
        **Easy Upload Process:**
        - JSON validation
        - Sample data provided
        - Real-time progress tracking
        """)

    # Sample data format
    st.subheader("📝 Data Format Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Input Dataset Format:**")
        st.code('''
{
    "input_1": "What is the capital of France?",
    "input_2": "Explain quantum computing",
    "input_3": "Write a haiku about spring"
}
        ''', language="json")
    
    with col2:
        st.markdown("**Output Dataset Format:**")
        st.code('''
{
    "input_1": [
        "The capital of France is Paris.",
        "Paris is the capital city of France."
    ],
    "input_2": [
        "Quantum computing uses quantum mechanics...",
        "It's a type of computation that harnesses..."
    ]
}
        ''', language="json")
    
    # Getting started
    st.subheader("🎯 Getting Started")
    st.info("👈 Use the sidebar navigation to start uploading your data and running analysis!")

elif page == "📊 Upload Data":
    # Initialize session state
    if 'current_dataset_id' not in st.session_state:
        st.session_state.current_dataset_id = None
    if 'current_output_id' not in st.session_state:
        st.session_state.current_output_id = None
    
    # Step 1: Upload or select dataset
    st.markdown("## Step 1: Input Dataset")
    
    tab1, tab2 = st.tabs(["📤 Upload New Dataset", "📋 Select Existing Dataset"])
    
    with tab1:
        dataset_id = render_dataset_upload()
        if dataset_id:
            st.session_state.current_dataset_id = dataset_id
    
    with tab2:
        selected_id = render_dataset_selector()
        if selected_id:
            st.session_state.current_dataset_id = selected_id
            st.success(f"Selected dataset: {selected_id}")
    
    # Step 2: Upload outputs (only if dataset is selected)
    if st.session_state.current_dataset_id:
        st.markdown("## Step 2: Output Dataset")
        output_id = render_output_upload(st.session_state.current_dataset_id)
        if output_id:
            st.session_state.current_output_id = output_id
            st.success("✅ Ready for analysis! Go to the Analysis page.")
    else:
        st.info("👆 Please upload or select an input dataset first.")

elif page == "🔬 Analysis":
    if 'current_output_id' not in st.session_state or not st.session_state.current_output_id:
        st.warning("⚠️ No output dataset selected. Please upload data first.")
        st.info("Go to the 'Upload Data' page to upload your datasets.")
    else:
        # Run analysis either locally or via Celery
        output_id = st.session_state.current_output_id
        with st.spinner("Running analysis..."):
            results = submit_analysis(output_id)
            st.session_state.analysis_results = results
        render_analysis_dashboard(results)

elif page == "📈 Dashboard":
    st.header("📈 Analysis Dashboard")
    
    if 'analysis_results' in st.session_state:
        from components.dashboard import display_analysis_results
        display_analysis_results(st.session_state.analysis_results)
    else:
        st.info("No analysis results available. Please run an analysis first.")
        
        # Show recent datasets
        if api_healthy:
            try:
                response = requests.get("http://localhost:8000/api/v1/datasets/")
                if response.status_code == 200:
                    datasets = response.json()
                    if datasets:
                        st.subheader("Recent Datasets")
                        for ds in datasets[-3:]:  # Show last 3 datasets
                            with st.expander(f"📊 {ds['name']} ({ds['id'][:8]}...)"):
                                st.write(f"**Created:** {ds['created_at']}")
                                st.write(f"**Inputs:** {len(ds['inputs'])}")
                                st.json(ds['metadata'])
            except:
                pass

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Oedipus MVP - Phase 1 | Built with FastAPI + Streamlit</p>
    <p>🔗 API Documentation: <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></p>
</div>
""", unsafe_allow_html=True)
