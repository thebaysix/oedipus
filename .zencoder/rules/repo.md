---
description: Repository Information Overview
alwaysApply: true
---

# Oedipus MVP Information

## Summary
Oedipus is a planned observability and analytics infrastructure for AI systems. The repository currently contains the architectural design and specifications for Phase 1 MVP, which focuses on bulk upload analysis of AI model outputs. The system aims to provide comprehensive information-theoretic analysis of model behavior patterns without requiring custom evaluation scripts.

## Structure
The repository currently contains only design documentation. The planned implementation structure as described in the documentation includes:
- **app/**: Backend FastAPI application with routes, models, services, and workers
- **frontend/**: Streamlit-based user interface components
- **docker/**: Containerization configuration

## Specification & Tools

**Type**: Architecture specification and design document
**Planned Technology Stack**:
- **Backend**: FastAPI, PostgreSQL, Redis, Celery
- **Frontend**: Streamlit, Plotly, Pandas
- **Deployment**: Docker, Railway/Fly.io

## Key Resources

**Main Files**:
- `oedipus_mvp_readme.md`: Comprehensive architecture specification document

**Planned Data Models**:
- Dataset: For storing input data
- OutputDataset: For storing model outputs
- AnalysisJob: For tracking analysis tasks

## Usage & Operations

**Planned Development Workflow**:
```bash
# Setup
git clone repo
docker-compose up -d  # postgres, redis
pip install -r requirements.txt

# Run backend
uvicorn app.api.main:app --reload

# Run frontend
streamlit run frontend/streamlit_app.py

# Run workers
celery -A app.workers.analysis_worker worker --loglevel=info
```

**Core Features**:
- Dataset Management: Upload and version input datasets
- Output Data Upload: Support for multi-output relationships
- Information-Theoretic Analysis: Metrics like entropy, information gain
- Visualization Dashboard: Interactive metric visualizations

## Validation

**Planned Success Metrics**:
- Upload→Analysis→Results cycle < 5 minutes for 1000 input/output pairs
- Support datasets up to 10,000 inputs with multiple outputs
- 99% uptime for analysis processing