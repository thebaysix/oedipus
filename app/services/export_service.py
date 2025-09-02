from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Tuple
import uuid
import json
import csv
import io
from datetime import datetime
from ..models.comparison import Comparison
from ..models.dataset import Dataset
from ..models.completion import CompletionDataset
from ..schemas.export import ExportRequest

# PDF generation imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class ExportService:
    def __init__(self, db: Session):
        self.db = db

    def export_comparison(self, request: ExportRequest) -> Tuple[bytes, str, str]:
        """
        Export comparison data in the requested format.
        Returns: (content_bytes, filename, content_type)
        """
        # Get the comparison
        comparison = self.db.query(Comparison).filter(
            Comparison.id == request.comparison_id
        ).first()
        
        if not comparison:
            raise ValueError(f"Comparison {request.comparison_id} not found")
        
        # Get related data
        dataset_id = uuid.UUID(comparison.datasets[0])
        completion_dataset_ids = [uuid.UUID(id_str) for id_str in comparison.datasets[1:]]
        
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        completions = (
            self.db.query(CompletionDataset)
            .filter(CompletionDataset.id.in_(completion_dataset_ids))
            .all()
        )
        
        # Prepare data based on format
        if request.format == 'json':
            return self._export_json(comparison, dataset, completions, request)
        elif request.format == 'csv':
            return self._export_csv(comparison, dataset, completions, request)
        elif request.format == 'summary':
            return self._export_summary(comparison, dataset, completions, request)
        elif request.format == 'pdf':
            return self._export_pdf(comparison, dataset, completions, request)
        else:
            raise ValueError(f"Unsupported export format: {request.format}")

    def _export_json(self, comparison: Comparison, dataset: Dataset, completions: List[CompletionDataset], request: ExportRequest) -> tuple[bytes, str, str]:
        """Export as JSON format."""
        data = {
            "comparison": {
                "id": str(comparison.id),
                "name": comparison.name,
                "created_at": comparison.created_at.isoformat(),
                "status": comparison.status,
                "alignment_key": comparison.alignment_key
            },
            "dataset": {
                "id": str(dataset.id),
                "name": dataset.name,
                "created_at": dataset.created_at.isoformat()
            },
            "completion_datasets": [
                {
                    "id": str(comp.id),
                    "name": comp.name,
                    "created_at": comp.created_at.isoformat()
                }
                for comp in completions
            ]
        }
        
        if request.include_raw_data:
            # Include alignment data
            alignment_result = comparison.statistical_results.get("alignment", {})
            data["raw_data"] = {
                "prompts": dataset.prompts,
                "completions": [comp.completions for comp in completions],
                "alignment": alignment_result
            }
        
        if request.include_statistics:
            data["statistics"] = comparison.statistical_results
        
        if request.include_insights:
            data["insights"] = comparison.automated_insights
        
        content = json.dumps(data, indent=2, default=str)
        filename = f"oedipus-comparison-{comparison.id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return content.encode('utf-8'), filename, "application/json"

    def _export_csv(self, comparison: Comparison, dataset: Dataset, completions: List[CompletionDataset], request: ExportRequest) -> tuple[bytes, str, str]:
        """Export as CSV format."""
        output = io.StringIO()
        
        # Get alignment data
        alignment_result = comparison.statistical_results.get("alignment", {})
        aligned_rows = alignment_result.get("alignedRows", [])
        
        if not aligned_rows:
            # Fallback: create basic alignment
            aligned_rows = []
            for prompt_id, prompt_text in dataset.prompts.items():
                row = {"prompt_id": prompt_id, "prompt_text": prompt_text}
                for i, comp in enumerate(completions):
                    completion_text = comp.completions.get(prompt_id, "")
                    row[f"completion_{i+1}"] = completion_text
                    row[f"completion_{i+1}_name"] = comp.name
                aligned_rows.append(row)
        
        if aligned_rows:
            writer = csv.DictWriter(output, fieldnames=aligned_rows[0].keys())
            writer.writeheader()
            writer.writerows(aligned_rows)
        
        # Add statistics if requested
        if request.include_statistics and comparison.statistical_results:
            output.write("\n\n# Statistical Results\n")
            stats = comparison.statistical_results
            for key, value in stats.items():
                if key != "alignment":  # Skip alignment data as it's already included
                    output.write(f"# {key}: {value}\n")
        
        # Add insights if requested
        if request.include_insights and comparison.automated_insights:
            output.write("\n\n# Automated Insights\n")
            for insight in comparison.automated_insights:
                output.write(f"# {insight}\n")
        
        content = output.getvalue()
        filename = f"oedipus-comparison-{comparison.id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return content.encode('utf-8'), filename, "text/csv"

    def _export_summary(self, comparison: Comparison, dataset: Dataset, completions: List[CompletionDataset], request: ExportRequest) -> tuple[bytes, str, str]:
        """Export as executive summary (text format for now, could be enhanced to PDF)."""
        lines = []
        lines.append(f"OEDIPUS COMPARISON REPORT")
        lines.append("=" * 50)
        lines.append(f"Comparison: {comparison.name}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Status: {comparison.status}")
        lines.append("")
        
        lines.append("DATASETS")
        lines.append("-" * 20)
        lines.append(f"Base Dataset: {dataset.name}")
        lines.append(f"Prompt Count: {len(dataset.prompts)}")
        lines.append("")
        
        lines.append("Completion Datasets:")
        for i, comp in enumerate(completions, 1):
            lines.append(f"  {i}. {comp.name} ({len(comp.completions)} completions)")
        lines.append("")
        
        if request.include_statistics and comparison.statistical_results:
            lines.append("STATISTICAL ANALYSIS")
            lines.append("-" * 30)
            
            # Alignment summary
            alignment = comparison.statistical_results.get("alignment", {})
            if alignment:
                lines.append(f"Alignment Coverage: {alignment.get('coverage_percentage', 'N/A')}%")
                lines.append(f"Matched Prompts: {alignment.get('matched_prompts', 'N/A')}")
                lines.append(f"Total Prompts: {alignment.get('total_prompts', 'N/A')}")
                lines.append("")
            
            # Other statistics
            for key, value in comparison.statistical_results.items():
                if key not in ["alignment", "progress"]:
                    lines.append(f"{key.replace('_', ' ').title()}: {value}")
            lines.append("")
        
        if request.include_insights and comparison.automated_insights:
            lines.append("KEY INSIGHTS")
            lines.append("-" * 20)
            for i, insight in enumerate(comparison.automated_insights, 1):
                lines.append(f"{i}. {insight}")
            lines.append("")
        
        lines.append("METHODOLOGY")
        lines.append("-" * 20)
        lines.append("This report was generated using Oedipus, an observability and")
        lines.append("analytics infrastructure for AI systems. The analysis includes")
        lines.append("comparative evaluation of model completions using information-")
        lines.append("theoretic metrics and statistical testing.")
        
        content = "\n".join(lines)
        filename = f"oedipus-summary-{comparison.id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        return content.encode('utf-8'), filename, "text/plain"

    def _export_pdf(self, comparison: Comparison, dataset: Dataset, completions: List[CompletionDataset], request: ExportRequest) -> Tuple[bytes, str, str]:
        """Export as PDF format using reportlab."""
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2563eb')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#1f2937')
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#374151')
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("OEDIPUS COMPARISON REPORT", title_style))
        story.append(Spacer(1, 12))
        
        # Basic info
        story.append(Paragraph("Report Details", heading_style))
        info_data = [
            ["Comparison Name:", comparison.name],
            ["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Status:", comparison.status],
            ["Comparison ID:", str(comparison.id)]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Datasets section
        story.append(Paragraph("Datasets", heading_style))
        story.append(Paragraph(f"<b>Prompt Dataset:</b> {dataset.name}", body_style))
        story.append(Paragraph(f"<b>Total Prompts:</b> {len(dataset.prompts) if dataset.prompts else 0}", body_style))
        story.append(Paragraph(f"<b>Created:</b> {dataset.created_at.strftime('%Y-%m-%d %H:%M:%S') if dataset.created_at else 'Unknown'}", body_style))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Completion Datasets:", subheading_style))
        for i, completion_dataset in enumerate(completions, 1):
            story.append(Paragraph(f"{i}. <b>{completion_dataset.name}</b>", body_style))
            story.append(Paragraph(f"   Total Completions: {len(completion_dataset.completions) if completion_dataset.completions else 0}", body_style))
            story.append(Paragraph(f"   Created: {completion_dataset.created_at.strftime('%Y-%m-%d %H:%M:%S') if completion_dataset.created_at else 'Unknown'}", body_style))
        
        story.append(Spacer(1, 20))
        
        # Statistics section
        if request.include_statistics and comparison.statistical_results:
            story.append(Paragraph("Statistical Analysis", heading_style))
            
            # Alignment stats
            if "alignment" in comparison.statistical_results:
                alignment = comparison.statistical_results["alignment"]
                story.append(Paragraph("Data Alignment", subheading_style))
                
                if "coverageStats" in alignment:
                    coverage = alignment["coverageStats"]
                    story.append(Paragraph(f"<b>Coverage:</b> {coverage.get('coveragePercentage', 0):.1f}%", body_style))
                    story.append(Paragraph(f"<b>Matched Prompts:</b> {coverage.get('matchedInputs', 0)}", body_style))
                    story.append(Paragraph(f"<b>Total Prompts:</b> {coverage.get('totalInputs', 0)}", body_style))
                
                story.append(Spacer(1, 12))
            
            # Other statistical metrics
            metrics_data = []
            for key, value in comparison.statistical_results.items():
                if key not in ["alignment", "progress"] and isinstance(value, (int, float, str)):
                    metrics_data.append([key.replace('_', ' ').title(), str(value)])
            
            if metrics_data:
                story.append(Paragraph("Key Metrics", subheading_style))
                metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
                metrics_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ]))
                story.append(metrics_table)
                story.append(Spacer(1, 20))
        
        # Insights section
        if request.include_insights and comparison.automated_insights:
            story.append(Paragraph("Key Insights", heading_style))
            for i, insight in enumerate(comparison.automated_insights, 1):
                story.append(Paragraph(f"{i}. {insight}", body_style))
            story.append(Spacer(1, 20))
        
        # Raw data section (sample)
        if request.include_raw_data and dataset.prompts and completions:
            story.append(Paragraph("Sample Data", heading_style))
            story.append(Paragraph("First 5 prompt-completion pairs:", subheading_style))
            
            # Create aligned data (same logic as CSV export)
            alignment_result = comparison.statistical_results.get("alignment", {})
            aligned_rows = alignment_result.get("alignedRows", [])
            
            if not aligned_rows:
                # Fallback: create basic alignment
                aligned_rows = []
                for prompt_id, prompt_text in dataset.prompts.items():
                    row = {"prompt_id": prompt_id, "prompt_text": prompt_text}
                    for i, comp in enumerate(completions):
                        completion_text = comp.completions.get(prompt_id, "")
                        row[f"completion_{i+1}"] = completion_text
                        row[f"completion_{i+1}_name"] = comp.name
                    aligned_rows.append(row)
            
            # Show first 5 items
            sample_data = aligned_rows[:5]
            
            for i, item in enumerate(sample_data, 1):
                story.append(Paragraph(f"<b>Sample {i}:</b>", body_style))
                prompt_text = item.get('prompt_text', '')
                story.append(Paragraph(f"<b>Prompt:</b> {prompt_text[:200]}{'...' if len(prompt_text) > 200 else ''}", body_style))
                
                # Show completions
                for key, value in item.items():
                    if key.startswith('completion_') and not key.endswith('_name'):
                        name_key = f"{key}_name"
                        dataset_name = item.get(name_key, f"Dataset {key.split('_')[1]}")
                        completion_text = str(value)
                        story.append(Paragraph(f"<b>{dataset_name}:</b> {completion_text[:200]}{'...' if len(completion_text) > 200 else ''}", body_style))
                
                story.append(Spacer(1, 8))
        
        # Methodology section
        story.append(PageBreak())
        story.append(Paragraph("Methodology", heading_style))
        methodology_text = """
        This report was generated using Oedipus, an observability and analytics infrastructure for AI systems. 
        The analysis includes comparative evaluation of model completions using information-theoretic metrics 
        and statistical testing.
        
        The comparison process involves:
        • Data alignment between prompt and completion datasets
        • Statistical analysis of completion characteristics
        • Information-theoretic metrics calculation
        • Automated insight generation based on statistical patterns
        
        All metrics are calculated using established statistical methods and are designed to provide 
        meaningful insights into model behavior and performance differences.
        """
        story.append(Paragraph(methodology_text, body_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f"oedipus-report-{comparison.id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return pdf_content, filename, "application/pdf"