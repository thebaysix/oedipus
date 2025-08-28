import streamlit as st
import requests
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Tuple

API_BASE_URL = "http://localhost:8000"


# ------------ API helpers ------------

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


def _list_comparisons() -> List[Dict[str, Any]]:
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/comparisons/")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch comparisons: {e}")
        return []


def _get_comparison(comp_id: str) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(f"{API_BASE_URL}/api/v1/comparisons/{comp_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch comparison {comp_id}: {e}")
        return None


# ------------ Alignment transform ------------

def _extract_alignment(comp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # Support both legacy alignment_stats and new statistical_results["alignment"]
    if comp.get("statistical_results") and isinstance(comp["statistical_results"], dict):
        aln = comp["statistical_results"].get("alignment")
        if aln:
            return aln
    # legacy
    if comp.get("alignment_stats"):
        stats = comp["alignment_stats"]
        # Build a minimal alignment result from legacy stats if available
        return {
            "alignedRows": [],
            "unmatchedInputs": list({k for v in (stats.get("unmatched_inputs") or {}).values() for k in v}),
            "coverageStats": {
                "totalInputs": stats.get("total_inputs", 0),
                "matchedInputs": stats.get("matched_inputs", 0),
                "coveragePercentage": stats.get("coverage_percentage", 0.0),
            },
        }
    return None


def _alignment_to_dataframe(alignment: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
    rows = alignment.get("alignedRows", []) or []
    if not rows:
        return pd.DataFrame(columns=["inputId", "inputText"]), []

    # Determine dataset display names from first row
    first_outputs = rows[0].get("outputs", {})
    dataset_names = list(first_outputs.keys())

    # Build table
    table: List[Dict[str, Any]] = []
    for r in rows:
        entry: Dict[str, Any] = {
            "inputId": r.get("inputId"),
            "inputText": r.get("inputText", ""),
        }
        outputs = r.get("outputs", {}) or {}
        for ds in dataset_names:
            values = outputs.get(ds)
            # Show first output text for overview; keep counts and lengths for metrics
            first_text = (values[0] if isinstance(values, list) and values else None)
            entry[f"{ds}__text"] = first_text
            entry[f"{ds}__n"] = len(values) if isinstance(values, list) else 0
            entry[f"{ds}__len"] = len(first_text) if isinstance(first_text, str) else np.nan
        table.append(entry)

    df = pd.DataFrame(table)
    return df, dataset_names


# ------------ UI: Creation ------------

def render_comparison_creator() -> Optional[str]:
    st.header("🆚 Create Comparison")

    datasets = _list_datasets()
    if not datasets:
        st.info("No datasets available. Upload inputs and outputs first.")
        return None

    ds_options = {f"{d['name']} ({d['id'][:8]}...)": d for d in datasets}
    ds_label = st.selectbox("Base Input Dataset", options=list(ds_options.keys()))
    selected_dataset = ds_options[ds_label]

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
                st.session_state["last_comparison_id"] = data["id"]
                st.json({"comparison_id": data["id"], "status": data.get("status", "pending")})
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


# ------------ UI: Explorer ------------

def _compute_outliers(df: pd.DataFrame, dataset_names: List[str], z_thresh: float, char_diff: int) -> pd.DataFrame:
    df = df.copy()
    # Compute per-dataset z-scores on length columns
    for ds in dataset_names:
        col = f"{ds}__len"
        if col in df:
            lengths = df[col].astype(float)
            mu = np.nanmean(lengths)
            sigma = np.nanstd(lengths) or 1.0
            z = (lengths - mu) / sigma
            df[f"{ds}__z"] = z
            df[f"{ds}__is_outlier"] = z.abs() >= z_thresh
    # Pairwise absolute differences between first two datasets (if available)
    if len(dataset_names) >= 2:
        a, b = dataset_names[0], dataset_names[1]
        da = df.get(f"{a}__len")
        db = df.get(f"{b}__len")
        if da is not None and db is not None:
            diff = (da - db).abs()
            df["abs_len_diff"] = diff
            df["diff_exceeds_threshold"] = diff >= char_diff
    return df


def _filter_df(df: pd.DataFrame, dataset_names: List[str], 
               show_only_outliers: bool, text_query: str) -> pd.DataFrame:
    filtered = df
    if text_query:
        q = text_query.lower()
        filtered = filtered[filtered["inputText"].str.lower().str.contains(q, na=False)]
    if show_only_outliers:
        outlier_flags = [f"{ds}__is_outlier" for ds in dataset_names if f"{ds}__is_outlier" in filtered]
        if outlier_flags:
            mask = np.zeros(len(filtered), dtype=bool)
            for col in outlier_flags:
                mask |= filtered[col].fillna(False).to_numpy()
            filtered = filtered[mask]
    return filtered


def render_comparison_explorer():
    st.subheader("🔎 Explore Comparisons")

    comparisons = _list_comparisons()
    if not comparisons:
        st.info("No comparisons found. Create one above.")
        return

    label_map = {f"{c['name']} ({c['id'][:8]}...)": c for c in comparisons}
    default_label = None
    last_id = st.session_state.get("last_comparison_id")
    if last_id:
        for lbl, obj in label_map.items():
            if obj["id"] == last_id:
                default_label = lbl
                break
    comp_label = st.selectbox("Select comparison", options=list(label_map.keys()), index=(list(label_map.keys()).index(default_label) if default_label in label_map else 0))
    comp = label_map[comp_label]

    alignment = _extract_alignment(comp)
    if not alignment:
        datasets = comp.get("datasets") or []
        stats = comp.get("statistical_results") or {}
        if len(datasets) < 2:
            reason = "It references fewer than two datasets."
        elif not stats:
            reason = "It was likely created before the latest update, so no results were stored."
        elif "alignment" not in stats:
            reason = "Its stored results are missing the alignment section."
        else:
            reason = "Alignment payload is empty."
        st.warning(f"No alignment data available for this comparison. {reason} Create a new comparison or re-upload outputs to populate alignment.")
        return

    # Summary metrics
    cov = alignment.get("coverageStats", {})
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Inputs", cov.get("totalInputs", 0))
    c2.metric("Matched Inputs", cov.get("matchedInputs", 0))
    c3.metric("Coverage %", cov.get("coveragePercentage", 0.0))

    df, dataset_names = _alignment_to_dataframe(alignment)
    if df.empty:
        st.info("No aligned rows to display.")
        return

    # Controls
    st.markdown("### Controls")
    colA, colB, colC, colD = st.columns([2, 2, 2, 2])

    with colA:
        ds_to_show = st.multiselect("Datasets to show", options=dataset_names, default=dataset_names)
    with colB:
        sig_level = st.selectbox("Significance level", options=[0.05, 0.01, 0.001], index=0)
        z_map = {0.05: 1.96, 0.01: 2.58, 0.001: 3.29}
        z_thresh = z_map[sig_level]
    with colC:
        char_diff = st.slider("Min char difference (A vs B)", min_value=0, max_value=500, value=50, step=10)
        view_mode = st.radio("View", options=["Text", "Lengths"], horizontal=True)
    with colD:
        only_outliers = st.checkbox("Show only outliers", value=False)
        text_query = st.text_input("Filter text")

    # Compute outliers and filters
    df_calc = _compute_outliers(df, dataset_names, z_thresh=z_thresh, char_diff=char_diff)
    df_filtered = _filter_df(df_calc, dataset_names, show_only_outliers=only_outliers, text_query=text_query)

    # Build display frame with selected datasets
    cols = ["inputId", "inputText"]
    for ds in ds_to_show:
        if view_mode == "Text":
            cols.append(f"{ds}__text")
        else:
            cols.extend([f"{ds}__len", f"{ds}__n", f"{ds}__z"])  # show z for understanding
    if "abs_len_diff" in df_filtered.columns and len(ds_to_show) >= 2:
        cols.append("abs_len_diff")
        if "diff_exceeds_threshold" in df_filtered:
            cols.append("diff_exceeds_threshold")

    display_df = df_filtered[cols]

    # Interactive table (virtualized + sortable)
    st.markdown("### Side-by-Side Table")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    # Outliers navigation
    st.markdown("### Outliers & Edge Cases")
    outlier_rows = []
    for ds in dataset_names:
        flag_col = f"{ds}__is_outlier"
        if flag_col in df_filtered:
            idxs = df_filtered.index[df_filtered[flag_col] == True].tolist()
            outlier_rows.extend(idxs)
    outlier_rows = sorted(set(outlier_rows))

    if outlier_rows:
        sel = st.selectbox("Jump to outlier row", options=[str(i) for i in outlier_rows])
        if sel:
            i = int(sel)
            st.write("Selected Outlier Row Detail:")
            st.json(df_filtered.loc[i].to_dict())
    else:
        st.caption("No outliers under current settings.")

    # Export
    st.markdown("### Export")
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV (current view)", data=csv, file_name="comparison_view.csv", mime="text/csv")


# ------------ Entry point for page ------------

def render_comparison_page():
    created_id = render_comparison_creator()
    if created_id:
        st.success("Scroll down to explore your comparison.")
    st.divider()
    render_comparison_explorer()