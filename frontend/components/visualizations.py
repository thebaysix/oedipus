import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any


def render_metrics_overview(results: Dict[str, Any]):
    """Render an overview of all metrics."""
    st.header("📈 Analysis Results Overview")
    
    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Extract key metrics
    info_theory = results.get("information_theory", {})
    diversity = results.get("diversity", {})
    summary = results.get("summary", {})
    
    with col1:
        st.metric(
            "Information Gain",
            f"{info_theory.get('information_gain', 0):.4f}",
            help="Mutual information between inputs and outputs"
        )
    
    with col2:
        st.metric(
            "Empowerment",
            f"{diversity.get('empowerment', 0):.4f}",
            help="Influence of model decisions on output diversity"
        )
    
    with col3:
        st.metric(
            "Total Outputs",
            summary.get('total_outputs', 0),
            help="Total number of outputs generated"
        )
    
    with col4:
        st.metric(
            "Unique Outputs",
            summary.get('unique_outputs', 0),
            help="Number of unique outputs"
        )


def render_entropy_chart(results: Dict[str, Any]):
    """Render entropy-related visualizations."""
    st.subheader("🔍 Entropy Analysis")
    
    info_theory = results.get("information_theory", {})
    
    # Create entropy comparison chart
    entropy_data = {
        "Metric": ["Input Entropy", "Response Entropy", "Information Gain"],
        "Value": [
            info_theory.get('input_entropy', 0),
            info_theory.get('response_entropy', 0),
            info_theory.get('information_gain', 0)
        ]
    }
    
    fig = px.bar(
        entropy_data,
        x="Metric",
        y="Value",
        title="Information-Theoretic Metrics",
        color="Value",
        color_continuous_scale="viridis"
    )
    
    fig.update_layout(
        xaxis_title="Metric Type",
        yaxis_title="Entropy (bits)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_length_distribution(results: Dict[str, Any]):
    """Render output length distribution charts."""
    st.subheader("📏 Output Length Analysis")
    
    char_metrics = results.get("character_metrics", {})
    token_metrics = results.get("token_metrics", {})
    
    # Create subplots for character and token distributions
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Character Count Distribution", "Token Count Distribution"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Character distribution
    char_dist = char_metrics.get("character_count_distribution", {})
    if char_dist:
        char_ranges = list(char_dist.keys())
        char_counts = list(char_dist.values())
        
        fig.add_trace(
            go.Bar(x=char_ranges, y=char_counts, name="Characters", marker_color="blue"),
            row=1, col=1
        )
    
    # Token distribution
    token_dist = token_metrics.get("token_count_distribution", {})
    if token_dist:
        token_ranges = list(token_dist.keys())
        token_counts = list(token_dist.values())
        
        fig.add_trace(
            go.Bar(x=token_ranges, y=token_counts, name="Tokens", marker_color="green"),
            row=1, col=2
        )
    
    fig.update_layout(
        title_text="Output Length Distributions",
        showlegend=False,
        height=400
    )
    
    fig.update_xaxes(title_text="Character Range", row=1, col=1)
    fig.update_xaxes(title_text="Token Range", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)


def render_diversity_metrics(results: Dict[str, Any]):
    """Render diversity-related visualizations."""
    st.subheader("🌈 Output Diversity Metrics")
    
    diversity = results.get("diversity", {})
    summary = results.get("summary", {})
    
    # Create diversity metrics chart
    diversity_data = {
        "Metric": [
            "Empowerment",
            "Unique Outputs Ratio",
            "Avg Outputs per Input",
            "Input Coverage"
        ],
        "Value": [
            diversity.get('empowerment', 0),
            diversity.get('unique_outputs_ratio', 0),
            diversity.get('average_outputs_per_input', 0) / 10,  # Scale for visualization
            summary.get('input_coverage', 0)
        ],
        "Description": [
            "Model decision influence on output diversity",
            "Ratio of unique to total outputs",
            "Average number of outputs per input (scaled)",
            "Fraction of inputs that have outputs"
        ]
    }
    
    fig = px.bar(
        diversity_data,
        x="Metric",
        y="Value",
        title="Diversity Metrics",
        color="Value",
        color_continuous_scale="plasma",
        hover_data=["Description"]
    )
    
    fig.update_layout(
        xaxis_title="Metric Type",
        yaxis_title="Normalized Value",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_summary_table(results: Dict[str, Any]):
    """Render a comprehensive summary table."""
    st.subheader("📊 Detailed Metrics Summary")
    
    # Prepare data for the table
    table_data = []
    
    # Information theory metrics
    info_theory = results.get("information_theory", {})
    for metric, value in info_theory.items():
        table_data.append({
            "Category": "Information Theory",
            "Metric": metric.replace('_', ' ').title(),
            "Value": f"{value:.4f}" if isinstance(value, (int, float)) else str(value)
        })
    
    # Diversity metrics
    diversity = results.get("diversity", {})
    for metric, value in diversity.items():
        table_data.append({
            "Category": "Diversity",
            "Metric": metric.replace('_', ' ').title(),
            "Value": f"{value:.4f}" if isinstance(value, (int, float)) else str(value)
        })
    
    # Character metrics
    char_metrics = results.get("character_metrics", {})
    for metric, value in char_metrics.items():
        if not metric.endswith('_distribution'):
            table_data.append({
                "Category": "Character Stats",
                "Metric": metric.replace('_', ' ').title(),
                "Value": f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            })
    
    # Token metrics
    token_metrics = results.get("token_metrics", {})
    for metric, value in token_metrics.items():
        if not metric.endswith('_distribution'):
            table_data.append({
                "Category": "Token Stats",
                "Metric": metric.replace('_', ' ').title(),
                "Value": f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            })
    
    # Summary metrics
    summary = results.get("summary", {})
    for metric, value in summary.items():
        table_data.append({
            "Category": "Summary",
            "Metric": metric.replace('_', ' ').title(),
            "Value": f"{value:.2f}" if isinstance(value, (int, float)) and metric != 'input_coverage' 
                    else f"{value:.2%}" if metric == 'input_coverage' 
                    else str(value)
        })
    
    # Create and display the table
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No metrics data available to display.")


def render_export_options(results: Dict[str, Any]):
    """Render export options for the results."""
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download as JSON"):
            st.download_button(
                label="Download JSON",
                data=pd.Series(results).to_json(indent=2),
                file_name="oedipus_analysis_results.json",
                mime="application/json"
            )
    
    with col2:
        # Convert results to a flat structure for CSV
        flat_results = {}
        for category, metrics in results.items():
            if isinstance(metrics, dict):
                for metric, value in metrics.items():
                    if not isinstance(value, dict):  # Skip nested dictionaries
                        flat_results[f"{category}_{metric}"] = value
        
        if flat_results:
            df = pd.DataFrame([flat_results])
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="oedipus_analysis_results.csv",
                mime="text/csv"
            )