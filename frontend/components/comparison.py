import streamlit as st
import requests
from typing import Optional, Dict, Any, List

API_BASE_URL = "http://localhost:8000"


def _list_datasets() -> List[Dict[str, Any]]:
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/datasets/")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch datasets: {e}")
        return []


def _list_outputs(dataset_id: str) -> List[Dict[str, Any]]:
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/datasets/{dataset_id}/outputs")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch output datasets: {e}")
        return []


def render_comparison_creator() -> Optional[str]:
    """
    Render a comparison creation UI:
    - Select base input dataset
    - Select 2+ output datasets belonging to it
    - Enter a name and create the comparison
    Shows alignment stats after creation.
    """
    st.header("🆚 Create Comparison")

    # Step 1: Choose base dataset
    datasets = _list_datasets()
    if not datasets:
        st.info("No datasets available. Upload inputs and outputs first.")
        return None

    ds_options = {f"{d['name']} ({d['id'][:8]}...)": d for d in datasets}
    ds_label = st.selectbox("Base Input Dataset", options=list(ds_options.keys()))
    selected_dataset = ds_options[ds_label]

    # Step 2: Choose output datasets for comparison
    outputs = _list_outputs(selected_dataset['id'])
    if not outputs:
        st.info("This dataset has no output datasets yet.")
        return None

    out_options = {f"{o['name']} ({o['id'][:8]}...)": o for o in outputs}
    chosen_labels = st.multiselect(
        "Select at least two output datasets to compare",
        options=list(out_options.keys()),
    )

    comp_name = st.text_input("Comparison Name", placeholder="e.g., GPT-4 vs Claude 3 vs Llama 3")

    col1, col2 = st.columns(2)
    with col1:
        create_clicked = st.button("Create Comparison", type="primary")
    with col2:
        st.caption("Tip: Ensure the selected outputs belong to the chosen input dataset.")

    if create_clicked:
        if not comp_name.strip():
            st.error("Please enter a comparison name.")
            return None
        if len(chosen_labels) < 2:
            st.error("Select at least two output datasets.")
            return None

        chosen_outputs = [out_options[lbl]['id'] for lbl in chosen_labels]
        payload = {
            "name": comp_name,
            "dataset_id": selected_dataset['id'],
            "output_dataset_ids": chosen_outputs,
            "alignment_key": "input_id",
            "comparison_config": {"min_aligned": 10},
        }
        try:
            resp = requests.post(f"{API_BASE_URL}/api/v1/comparisons/create", json=payload)
            if resp.status_code == 201:
                data = resp.json()
                st.success("Comparison created!")
                st.json({"comparison_id": data["id"], "status": data.get("status", "created")})

                # Alignment stats summary
                stats = data.get("alignment_stats", {}) or {}
                if stats:
                    st.subheader("Alignment Summary")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Total Inputs", stats.get("total_inputs", 0))
                    col_b.metric("Datasets", stats.get("datasets_included", 0))
                    col_c.metric("Matched Inputs", stats.get("matched_inputs", 0))
                    col_d.metric("Coverage %", stats.get("coverage_percentage", 0.0))

                    with st.expander("Details: Unmatched Inputs by Dataset"):
                        st.json(stats.get("unmatched_inputs", {}))
                return data["id"]
            else:
                try:
                    err = resp.json()
                except Exception:
                    err = resp.text
                st.error(f"Failed to create comparison: {err}")
                return None
        except Exception as e:
            st.error(f"Request failed: {e}")
            return None

    return None