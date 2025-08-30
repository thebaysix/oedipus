from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
from datetime import datetime
from ..models.analysis import AnalysisJob
from ..models.completion import CompletionDataset
from ..schemas.analysis import AnalysisJobCreate
from .metrics.entropy import calculate_input_entropy, calculate_response_entropy
from .metrics.information_gain import calculate_mutual_information
from .metrics.empowerment import calculate_output_diversity_metrics
from .metrics.basic_metrics import calculate_character_metrics, calculate_token_metrics


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_analysis_job(self, job_data: AnalysisJobCreate) -> AnalysisJob:
        """Create a new analysis job."""
        # Verify the completion dataset exists
        completion_dataset = self.db.query(CompletionDataset).filter(
            CompletionDataset.id == job_data.completion_dataset_id
        ).first()
        
        if not completion_dataset:
            raise ValueError(f"Completion dataset {job_data.completion_dataset_id} not found")
        
        db_job = AnalysisJob(
            completion_dataset_id=job_data.completion_dataset_id,
            status="pending"
        )
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job
    
    def get_analysis_job(self, job_id: uuid.UUID) -> AnalysisJob:
        """Get an analysis job by ID."""
        return self.db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    
    def update_job_status(self, job_id: uuid.UUID, status: str, results: Dict[str, Any] = None):
        """Update analysis job status and results."""
        job = self.get_analysis_job(job_id)
        if job:
            job.status = status
            if results:
                job.results = results
            if status in ["completed", "failed"]:
                job.completed_at = datetime.utcnow()
            self.db.commit()
    
    def run_analysis(self, job_id: uuid.UUID) -> Dict[str, Any]:
        """Run the complete analysis for a job."""
        job = self.get_analysis_job(job_id)
        if not job:
            raise ValueError(f"Analysis job {job_id} not found")
        
        # Update status to running
        self.update_job_status(job_id, "running")
        
        try:
            # Get the completion dataset and related prompt dataset
            completion_dataset = job.completion_dataset
            prompt_dataset = completion_dataset.dataset
            
            # Run all analyses
            results = self.compute_all_metrics(
                prompt_dataset.prompts,
                completion_dataset.completions
            )
            
            # Update job with results
            self.update_job_status(job_id, "completed", results)
            return results
            
        except Exception as e:
            # Update job status to failed
            error_results = {"error": str(e)}
            self.update_job_status(job_id, "failed", error_results)
            raise
    
    def compute_all_metrics(self, prompts: Dict[str, str], completions: Dict[str, list]) -> Dict[str, Any]:
        """Compute all available metrics for the given prompts and completions."""
        results = {}
        
        # Information-theoretic metrics
        results["information_theory"] = calculate_mutual_information(prompts, completions)
        
        # Output diversity metrics
        results["diversity"] = calculate_output_diversity_metrics(prompts, completions)
        
        # Basic metrics
        results["character_metrics"] = calculate_character_metrics(completions)
        results["token_metrics"] = calculate_token_metrics(completions)
        
        # Summary statistics
        results["summary"] = self._compute_summary_stats(prompts, completions)
        
        return results
    
    def _compute_summary_stats(self, prompts: Dict[str, str], completions: Dict[str, list]) -> Dict[str, Any]:
        """Compute summary statistics."""
        total_inputs = len(prompts)
        total_outputs = sum(len(output_list) for output_list in completions.values())
        unique_inputs = len(set(prompts.values()))
        
        all_outputs = []
        for output_list in completions.values():
            all_outputs.extend(output_list)
        unique_outputs = len(set(all_outputs))
        
        return {
            "total_inputs": total_inputs,
            "total_outputs": total_outputs,
            "unique_inputs": unique_inputs,
            "unique_outputs": unique_outputs,
            "avg_outputs_per_input": total_outputs / total_inputs if total_inputs > 0 else 0,
            "input_coverage": len(completions) / total_inputs if total_inputs > 0 else 0
        }