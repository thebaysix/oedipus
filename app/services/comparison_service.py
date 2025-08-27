from sqlalchemy.orm import Session
from typing import List, Dict, Any, Tuple
import uuid
from ..models.dataset import Dataset
from ..models.output import OutputDataset
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

        # Validate output datasets
        outputs: List[OutputDataset] = (
            self.db.query(OutputDataset)
            .filter(OutputDataset.id.in_(payload.output_dataset_ids))
            .all()
        )
        if len(outputs) != len(set(payload.output_dataset_ids)):
            found_ids = {str(o.id) for o in outputs}
            missing = [str(i) for i in payload.output_dataset_ids if str(i) not in found_ids]
            raise ValueError(f"Output datasets not found: {missing}")

        # Ensure all outputs belong to the same input dataset
        for o in outputs:
            if o.dataset_id != payload.dataset_id:
                raise ValueError("All output datasets must belong to the specified dataset")

        # Basic alignment + validation
        alignment_stats = self._compute_alignment_stats(dataset.inputs, outputs)

        comp = Comparison(
            name=payload.name,
            dataset_id=payload.dataset_id,
            output_dataset_ids=[str(i) for i in payload.output_dataset_ids],
            alignment_key=payload.alignment_key,
            comparison_config=payload.comparison_config or {},
            alignment_stats=alignment_stats,
            status="created",
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

    def _compute_alignment_stats(self, inputs: Dict[str, str], outputs: List[OutputDataset]) -> Dict[str, Any]:
        input_keys = set(inputs.keys())
        matched_by_dataset: Dict[str, int] = {}
        unmatched_inputs: Dict[str, List[str]] = {}
        matched_intersection = input_keys.copy()

        for o in outputs:
            keys = set((o.outputs or {}).keys())
            matched = keys & input_keys
            matched_by_dataset[str(o.id)] = len(matched)
            unmatched_inputs[str(o.id)] = sorted(list(input_keys - keys))
            matched_intersection &= matched

        total_inputs = len(input_keys)
        matched_inputs = len(matched_intersection)
        coverage = (matched_inputs / total_inputs * 100.0) if total_inputs else 0.0

        return {
            "total_inputs": total_inputs,
            "datasets_included": len(outputs),
            "matched_inputs": matched_inputs,
            "coverage_percentage": round(coverage, 2),
            "matched_by_dataset": matched_by_dataset,
            "unmatched_inputs": unmatched_inputs,
        }