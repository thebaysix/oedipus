import streamlit as st
import requests
import time
from typing import Dict, Any, Optional
from .visualizations import (
    render_metrics_overview,
    render_entropy_chart,
    render_length_distribution,
    render_diversity_metrics,
    render_summary_table,
    render_export_options
)

API_BASE_URL = "http://localhost:8000"


def render_analysis_dashboard(output_dataset_id: str):
    """Render the main analysis dashboard."""
    st.header("🔬 Analysis Dashboard")
    
    # Analysis controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"Output Dataset ID: {output_dataset_id}")
    
    with col2:
        if st.button("🚀 Run Analysis", key="run_analysis"):
            run_analysis_job(output_dataset_id)
    
    # Check for existing analysis results
    check_analysis_status(output_dataset_id)


def run_analysis_job(output_dataset_id: str):
    """Start an analysis job."""
    try:
        # Start analysis job
        response = requests.post(
            f"{API_BASE_URL}/api/v1/analysis/run",
            json={"output_dataset_id": output_dataset_id}
        )
        
        if response.status_code == 201:
            job_info = response.json()
            job_id = job_info["id"]
            
            st.success(f"Analysis job started! Job ID: {job_id}")
            st.session_state.current_job_id = job_id
            st.session_state.job_status = "pending"
            
            # Start monitoring the job
            monitor_job_progress(job_id)
            
        else:
            st.error(f"Failed to start analysis: {response.text}")
            
    except Exception as e:
        st.error(f"Error starting analysis: {str(e)}")


def monitor_job_progress(job_id: str):
    """Monitor job progress with real-time updates."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    max_attempts = 60  # 5 minutes with 5-second intervals
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/analysis/{job_id}/status")
            
            if response.status_code == 200:
                job_info = response.json()
                status = job_info["status"]
                
                if status == "pending":
                    progress_bar.progress(10)
                    status_text.text("⏳ Analysis job is pending...")
                elif status == "running":
                    progress_bar.progress(50)
                    status_text.text("🔄 Analysis is running...")
                elif status == "completed":
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis completed!")
                    st.session_state.job_status = "completed"
                    st.session_state.current_job_id = job_id
                    
                    # Fetch and display results
                    fetch_and_display_results(job_id)
                    break
                elif status == "failed":
                    progress_bar.progress(0)
                    status_text.text("❌ Analysis failed!")
                    st.error("Analysis job failed. Please try again.")
                    break
                
                time.sleep(5)
                attempt += 1
            else:
                st.error(f"Error checking job status: {response.text}")
                break
                
        except Exception as e:
            st.error(f"Error monitoring job: {str(e)}")
            break
    
    if attempt >= max_attempts:
        st.warning("Analysis is taking longer than expected. Please check back later.")


def fetch_and_display_results(job_id: str):
    """Fetch and display analysis results."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/analysis/{job_id}/results")
        
        if response.status_code == 200:
            result_data = response.json()
            results = result_data["results"]
            
            # Store results in session state
            st.session_state.analysis_results = results
            
            # Display results
            display_analysis_results(results)
            
        else:
            st.error(f"Failed to fetch results: {response.text}")
            
    except Exception as e:
        st.error(f"Error fetching results: {str(e)}")


def display_analysis_results(results: Dict[str, Any]):
    """Display comprehensive analysis results."""
    st.success("🎉 Analysis completed successfully!")
    
    # Render all visualization components
    render_metrics_overview(results)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🔍 Entropy", 
        "📏 Length Analysis", 
        "🌈 Diversity", 
        "📋 Detailed Table"
    ])
    
    with tab1:
        render_entropy_chart(results, key="entropy_overview")
        render_diversity_metrics(results, key="diversity_overview")
    
    with tab2:
        render_entropy_chart(results, key="entropy_details")
        
        # Additional entropy insights
        st.subheader("Entropy Insights")
        info_theory = results.get("information_theory", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Input Entropy",
                f"{info_theory.get('input_entropy', 0):.4f}",
                help="Measures the diversity of input prompts"
            )
            st.metric(
                "Response Entropy",
                f"{info_theory.get('response_entropy', 0):.4f}",
                help="Measures the diversity of outputs given inputs"
            )
        
        with col2:
            st.metric(
                "Information Gain",
                f"{info_theory.get('information_gain', 0):.4f}",
                help="How much information outputs provide about inputs"
            )
            st.metric(
                "Normalized Info Gain",
                f"{info_theory.get('normalized_information_gain', 0):.4f}",
                help="Information gain normalized by input entropy"
            )
    
    with tab3:
        render_length_distribution(results, key="length_distribution")
        
        # Additional length statistics
        char_metrics = results.get("character_metrics", {})
        token_metrics = results.get("token_metrics", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Character Statistics")
            st.write(f"**Mean Length:** {char_metrics.get('character_count_mean', 0):.2f}")
            st.write(f"**Std Deviation:** {char_metrics.get('character_count_std', 0):.2f}")
            st.write(f"**Range:** {char_metrics.get('character_count_min', 0)} - {char_metrics.get('character_count_max', 0)}")
        
        with col2:
            st.subheader("Token Statistics")
            st.write(f"**Mean Tokens:** {token_metrics.get('token_count_mean', 0):.2f}")
            st.write(f"**Std Deviation:** {token_metrics.get('token_count_std', 0):.2f}")
            st.write(f"**Range:** {token_metrics.get('token_count_min', 0)} - {token_metrics.get('token_count_max', 0)}")
    
    with tab4:
        render_diversity_metrics(results)
        
        # Additional diversity insights
        st.subheader("Diversity Insights")
        diversity = results.get("diversity", {})
        summary = results.get("summary", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Empowerment Score",
                f"{diversity.get('empowerment', 0):.4f}",
                help="How much model choices affect output diversity"
            )
            st.metric(
                "Unique Output Ratio",
                f"{diversity.get('unique_outputs_ratio', 0):.2%}",
                help="Percentage of outputs that are unique"
            )
        
        with col2:
            st.metric(
                "Coverage Rate",
                f"{summary.get('input_coverage', 0):.2%}",
                help="Percentage of inputs that have outputs"
            )
            st.metric(
                "Avg Outputs/Input",
                f"{diversity.get('average_outputs_per_input', 0):.2f}",
                help="Average number of outputs per input"
            )
    
    with tab5:
        render_summary_table(results)
    
    # Export options
    st.divider()
    render_export_options(results)


def check_analysis_status(output_dataset_id: str):
    """Check if there are any existing analysis results."""
    if "analysis_results" in st.session_state:
        st.info("📊 Previous analysis results found!")
        if st.button("Show Previous Results"):
            display_analysis_results(st.session_state.analysis_results)
    
    if "current_job_id" in st.session_state and "job_status" in st.session_state:
        job_id = st.session_state.current_job_id
        status = st.session_state.job_status
        
        if status == "completed":
            st.success(f"✅ Analysis job {job_id[:8]}... completed!")
            if st.button("Show Results"):
                fetch_and_display_results(job_id)
        elif status in ["pending", "running"]:
            st.info(f"🔄 Analysis job {job_id[:8]}... is {status}")
            if st.button("Check Status"):
                monitor_job_progress(job_id)