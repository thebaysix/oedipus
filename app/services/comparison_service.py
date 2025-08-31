from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
from ..models.dataset import Dataset
from ..models.completion import CompletionDataset
from ..models.comparison import Comparison
from ..schemas.comparison import ComparisonCreate


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
        for input_id in list(matched_intersection)[:200]:
            row_outputs: Dict[str, Any] = {}
            row_meta: Dict[str, Any] = {}
            for ds_id, ds_outputs in outputs_by_dataset.items():
                name = dataset_name_by_id.get(ds_id, ds_id)
                row_outputs[name] = ds_outputs.get(input_id, None)
                row_meta[name] = {}
            aligned_rows.append({
                "inputId": input_id,
                "inputText": prompts.get(input_id, ""),
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