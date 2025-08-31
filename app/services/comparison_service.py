from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
import asyncio
import time
from datetime import datetime
from ..models.dataset import Dataset
from ..models.completion import CompletionDataset
from ..models.comparison import Comparison
from ..schemas.comparison import ComparisonCreate
from .metrics.statistical_tests import run_statistical_tests, calculate_summary_statistics
from .metrics.basic_metrics import calculate_character_metrics, calculate_token_metrics


class ComparisonService:
    def __init__(self, db: Session):
        self.db = db

    def create_comparison(self, payload: ComparisonCreate) -> Comparison:
        # Validate base dataset
        dataset: Dataset | None = self.db.query(Dataset).filter(Dataset.id == payload.dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {payload.dataset_id} not found")

        # Validate completion datasets
        completions: List[CompletionDataset] = (
            self.db.query(CompletionDataset)
            .filter(CompletionDataset.id.in_(payload.completion_dataset_ids))
            .all()
        )
        if len(completions) != len(set(payload.completion_dataset_ids)):
            found_ids = {str(o.id) for o in completions}
            missing = [str(i) for i in payload.completion_dataset_ids if str(i) not in found_ids]
            raise ValueError(f"Completion datasets not found: {missing}")

        # Ensure all completions belong to the same prompt dataset
        for o in completions:
            if o.dataset_id != payload.dataset_id:
                raise ValueError("All completion datasets must belong to the specified dataset")

        # Alignment result per Feature 1 spec
        alignment_result = self._compute_alignment_result(dataset.prompts, completions)

        comp = Comparison(
            name=payload.name,
            datasets=[str(payload.dataset_id)] + [str(i) for i in payload.completion_dataset_ids],
            alignment_key=payload.alignment_key,
            comparison_config=payload.comparison_config or {},
            statistical_results={"alignment": alignment_result},
            automated_insights=[],
            status="pending",
        )
        self.db.add(comp)
        self.db.commit()
        self.db.refresh(comp)
        return comp

    def run_comparison_analysis(self, comparison_id: uuid.UUID) -> Comparison:
        """Run the statistical analysis for a comparison."""
        comp = self.get_comparison(comparison_id)
        if not comp:
            raise ValueError(f"Comparison {comparison_id} not found")
        
        if comp.status != "pending":
            return comp
        
        # Update status to running
        comp.status = "running"
        updated_results = dict(comp.statistical_results)
        updated_results["progress"] = {"step": "statistical_analysis", "message": "Computing statistical metrics..."}
        comp.statistical_results = updated_results
        self.db.commit()
        
        try:
            # Get the datasets
            dataset_id = uuid.UUID(comp.datasets[0])
            completion_dataset_ids = [uuid.UUID(id_str) for id_str in comp.datasets[1:]]
            
            dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
            completions = (
                self.db.query(CompletionDataset)
                .filter(CompletionDataset.id.in_(completion_dataset_ids))
                .all()
            )
            
            # Simulate realistic analysis timing with progress updates
            time.sleep(1)
            
            # Update progress: insights generation
            updated_results = dict(comp.statistical_results)
            updated_results["progress"] = {"step": "insights", "message": "Generating automated insights..."}
            comp.statistical_results = updated_results
            self.db.commit()
            
            time.sleep(1)
            
            # Update progress: visualization prep
            updated_results = dict(comp.statistical_results)
            updated_results["progress"] = {"step": "visualization", "message": "Preparing visualizations..."}
            comp.statistical_results = updated_results
            self.db.commit()
            
            time.sleep(1)
            
            # Run statistical analysis
            alignment_result = comp.statistical_results.get("alignment", {})
            statistical_results = self._run_comparison_analysis(dataset, completions, alignment_result)
            
            # Create a new dict to ensure SQLAlchemy detects the change
            updated_results = dict(comp.statistical_results)
            updated_results.update(statistical_results)
            comp.statistical_results = updated_results
            comp.automated_insights = statistical_results.get("insights", [])
            comp.status = "completed"
            self.db.commit()
            
        except Exception as e:
            comp.status = "failed"
            # Create a new dict to ensure SQLAlchemy detects the change
            updated_results = dict(comp.statistical_results)
            updated_results["error"] = str(e)
            comp.statistical_results = updated_results
            self.db.commit()
            raise
        
        return comp

    def list_comparisons(self, skip: int = 0, limit: int = 100) -> List[Comparison]:
        return (
            self.db.query(Comparison)
            .order_by(Comparison.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_comparison(self, comparison_id: uuid.UUID) -> Comparison | None:
        return self.db.query(Comparison).filter(Comparison.id == comparison_id).first()

    def delete_comparison(self, comparison_id: uuid.UUID) -> bool:
        comp = self.get_comparison(comparison_id)
        if not comp:
            return False
        self.db.delete(comp)
        self.db.commit()
        return True

    def _compute_alignment_result(self, prompts: Dict[str, str], completions: List[CompletionDataset]) -> Dict[str, Any]:
        input_keys = set(prompts.keys())
        matched_intersection = input_keys.copy()

        # Build quick maps for completions by dataset
        outputs_by_dataset: Dict[str, Dict[str, List[str]]] = {}
        dataset_name_by_id: Dict[str, str] = {}
        for o in completions:
            ds_id = str(o.id)
            outputs_by_dataset[ds_id] = o.completions or {}
            dataset_name_by_id[ds_id] = o.name
            matched_intersection &= set((o.completions or {}).keys())

        total_inputs = len(input_keys)
        matched_inputs = len(matched_intersection)
        coverage = (matched_inputs / total_inputs * 100.0) if total_inputs else 0.0

        # Unmatched prompts: those missing in any selected dataset (union of differences)
        unmatched_union = set()
        for o in completions:
            keys = set((o.completions or {}).keys())
            unmatched_union |= (input_keys - keys)

        # Construct aligned rows for matched intersection (cap to 200 rows to keep payload small)
        aligned_rows = []
        for prompt_id in list(matched_intersection)[:200]:
            row_outputs: Dict[str, Any] = {}
            row_meta: Dict[str, Any] = {}
            for ds_id, ds_outputs in outputs_by_dataset.items():
                name = dataset_name_by_id.get(ds_id, ds_id)
                row_outputs[name] = ds_outputs.get(prompt_id, None)
                row_meta[name] = {}
            aligned_rows.append({
                "inputId": prompt_id,
                "inputText": prompts.get(prompt_id, ""),
                "completions": row_outputs,
                "metadata": row_meta,
            })

        return {
            "alignedRows": aligned_rows,
            "unmatchedInputs": sorted(list(unmatched_union)),
            "coverageStats": {
                "totalInputs": total_inputs,
                "matchedInputs": matched_inputs,
                "coveragePercentage": round(coverage, 2),
            },
        }
    
    def _run_comparison_analysis(self, dataset: Dataset, completions: List[CompletionDataset], alignment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Run statistical analysis comparing multiple completion datasets."""
        # Prepare data for statistical analysis
        completions_by_dataset = {}
        for completion_dataset in completions:
            completions_by_dataset[completion_dataset.name] = completion_dataset.completions or {}
        
        # Run statistical tests
        metrics = run_statistical_tests(completions_by_dataset)
        
        # Generate automated insights
        insights = self._generate_insights(metrics, completions_by_dataset)
        
        return {
            "metrics": metrics,
            "summary_statistics": calculate_summary_statistics(completions_by_dataset),
            "insights": insights
        }
    
    def _generate_insights(self, metrics: List[Dict[str, Any]], completions_by_dataset: Dict[str, Dict[str, List[str]]]) -> List[str]:
        """Generate automated insights from statistical analysis."""
        insights = []
        
        # Find significant differences
        significant_metrics = [m for m in metrics if m.get("statistical_significance", 1.0) < 0.05]
        if significant_metrics:
            insights.append(f"Found {len(significant_metrics)} statistically significant differences between datasets.")
            
            # Highlight the most significant
            most_significant = min(significant_metrics, key=lambda x: x.get("statistical_significance", 1.0))
            insights.append(f"Most significant difference: {most_significant['name']} (p={most_significant['statistical_significance']:.4f})")
        
        # Dataset size comparison
        dataset_sizes = {name: sum(len(completions) for completions in dataset.values()) 
                        for name, dataset in completions_by_dataset.items()}
        if dataset_sizes:
            largest_dataset = max(dataset_sizes.items(), key=lambda x: x[1])
            smallest_dataset = min(dataset_sizes.items(), key=lambda x: x[1])
            insights.append(f"Dataset sizes range from {smallest_dataset[1]} ({smallest_dataset[0]}) to {largest_dataset[1]} ({largest_dataset[0]}) completions.")
        
        # Effect size insights
        large_effects = [m for m in metrics if abs(m.get("effect_size", 0)) > 0.8]
        if large_effects:
            insights.append(f"Found {len(large_effects)} metrics with large effect sizes (>0.8), indicating substantial practical differences.")
        
        return insights