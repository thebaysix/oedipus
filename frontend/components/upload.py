import streamlit as st
import requests
import json
from typing import Dict, Any, Optional
from utils.data_processing import validate_input_json, validate_output_json, create_sample_data

API_BASE_URL = "http://localhost:8000"


def render_dataset_upload() -> Optional[str]:
    """Render the dataset upload component."""
    st.header("📊 Upload Input Dataset")
    
    # Option to use sample data
    if st.button("Use Sample Data", key="sample_input"):
        sample_inputs, _ = create_sample_data()
        st.session_state.sample_input_json = json.dumps(sample_inputs, indent=2)
    
    # Dataset name input
    dataset_name = st.text_input(
        "Dataset Name",
        placeholder="Enter a name for your dataset",
        key="dataset_name"
    )
    
    # JSON input
    json_input = st.text_area(
        "Input Data (JSON)",
        placeholder='{"input_1": "What is AI?", "input_2": "Explain ML"}',
        height=200,
        value=st.session_state.get('sample_input_json', ''),
        key="input_json"
    )
    
    # Validation and upload
    if st.button("Upload Dataset", key="upload_dataset"):
        if not dataset_name.strip():
            st.error("Please enter a dataset name")
            return None
        
        if not json_input.strip():
            st.error("Please enter JSON data")
            return None
        
        # Validate JSON
        is_valid, message, data = validate_input_json(json_input)
        
        if not is_valid:
            st.error(f"Invalid JSON: {message}")
            return None
        
        # Upload to API
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/datasets/",
                json={
                    "name": dataset_name,
                    "inputs": data,
                    "metadata": {"uploaded_via": "streamlit"}
                }
            )
            
            if response.status_code == 201:
                dataset_info = response.json()
                st.success(f"Dataset '{dataset_name}' uploaded successfully!")
                st.json({"dataset_id": dataset_info["id"], "total_inputs": len(data)})
                return dataset_info["id"]
            else:
                st.error(f"Upload failed: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API. Make sure the backend is running on http://localhost:8000")
            return None
        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return None
    
    return None


def render_output_upload(dataset_id: str) -> Optional[str]:
    """Render the output dataset upload component."""
    st.header("🎯 Upload Output Dataset")
    
    # Get dataset info
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/datasets/{dataset_id}")
        if response.status_code == 200:
            dataset_info = response.json()
            st.info(f"Uploading outputs for dataset: **{dataset_info['name']}**")
            
            # Show input keys for reference
            input_keys = list(dataset_info['inputs'].keys())
            st.write(f"Available input IDs: {', '.join(input_keys[:10])}" + 
                    (f" ... and {len(input_keys)-10} more" if len(input_keys) > 10 else ""))
            
        else:
            st.error("Could not fetch dataset information")
            return None
            
    except Exception as e:
        st.error(f"Error fetching dataset: {str(e)}")
        return None
    
    # Option to use sample data
    if st.button("Use Sample Data", key="sample_output"):
        _, sample_outputs = create_sample_data()
        st.session_state.sample_output_json = json.dumps(sample_outputs, indent=2)
    
    # Output dataset name
    output_name = st.text_input(
        "Output Dataset Name",
        placeholder="Enter a name for your output dataset",
        key="output_name"
    )
    
    # JSON input for outputs
    output_json = st.text_area(
        "Output Data (JSON)",
        placeholder='{"input_1": ["Response 1", "Response 2"], "input_2": ["Another response"]}',
        height=200,
        value=st.session_state.get('sample_output_json', ''),
        key="output_json"
    )
    
    # Upload button
    if st.button("Upload Outputs", key="upload_outputs"):
        if not output_name.strip():
            st.error("Please enter an output dataset name")
            return None
        
        if not output_json.strip():
            st.error("Please enter JSON data")
            return None
        
        # Validate JSON
        is_valid, message, data = validate_output_json(output_json, input_keys)
        
        if not is_valid:
            st.error(f"Invalid JSON: {message}")
            return None
        
        # Upload to API
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/datasets/{dataset_id}/outputs",
                json={
                    "name": output_name,
                    "outputs": data,
                    "metadata": {"uploaded_via": "streamlit"}
                }
            )
            
            if response.status_code == 201:
                output_info = response.json()
                st.success(f"Output dataset '{output_name}' uploaded successfully!")
                
                total_outputs = sum(len(outputs) for outputs in data.values())
                st.json({
                    "output_dataset_id": output_info["id"],
                    "total_outputs": total_outputs,
                    "inputs_covered": len(data)
                })
                return output_info["id"]
            else:
                st.error(f"Upload failed: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return None
    
    return None


def render_dataset_selector() -> Optional[str]:
    """Render a dataset selector component."""
    st.header("📋 Select Dataset")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/datasets/")
        if response.status_code == 200:
            datasets = response.json()
            
            if not datasets:
                st.info("No datasets found. Please upload a dataset first.")
                return None
            
            # Create selection options
            dataset_options = {
                f"{ds['name']} ({ds['id'][:8]}...)": ds['id'] 
                for ds in datasets
            }
            
            selected_name = st.selectbox(
                "Choose a dataset:",
                options=list(dataset_options.keys()),
                key="dataset_selector"
            )
            
            if selected_name:
                return dataset_options[selected_name]
        else:
            st.error("Could not fetch datasets")
            return None
            
    except Exception as e:
        st.error(f"Error fetching datasets: {str(e)}")
        return None