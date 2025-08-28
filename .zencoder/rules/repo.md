---
description: Repository Information Overview
alwaysApply: true
---

# Oedipus MVP Information

## Summary
Oedipus is an observability and analytics infrastructure for AI systems. The repository contains a fully implemented MVP focused on bulk upload analysis of AI model outputs. The system provides comprehensive information-theoretic analysis of model behavior patterns and now includes comparison capabilities for multiple model outputs.

## Structure
- **app/**: Backend FastAPI application
  - **api/**: API routes and endpoints (datasets, outputs, analysis, comparisons)
  - **core/**: Configuration and database setup
  - **models/**: SQLAlchemy database models
  - **schemas/**: Pydantic validation schemas
  - **services/**: Business logic and analysis services
  - **workers/**: Celery background tasks
- **frontend/**: Streamlit-based user interface
  - **components/**: UI components (dashboard, upload, visualizations, comparison)
  - **utils/**: Helper functions for data processing
- **scripts/**: Setup and startup scripts
- **tests/**: Test suite for API and metrics
- **alembic/**: Database migration scripts with version history

## Language & Runtime
**Language**: Python 3.13.7
**Build System**: pip
**Package Manager**: pip
**Database**: PostgreSQL 15
**Cache/Queue**: Redis 7

## Dependencies
**Main Dependencies**:
- FastAPI 0.104.1+: API framework
- SQLAlchemy 1.4.48: ORM
- Alembic 1.12.1: Database migrations
- Celery 5.3.4: Background task processing
- Streamlit 1.48.0+: Frontend UI
- Plotly 5.17.0: Data visualization
- Pandas 2.0.0+: Data manipulation
- NumPy 1.24.0+: Numerical processing
- Tiktoken 0.11.0+: Token counting
- Redis 5.0.1: Caching and message broker
- Pydantic 2.0.0+: Data validation

**Development Dependencies**:
- pytest 7.4.3: Testing framework
- pytest-asyncio 0.21.1: Async testing
- httpx 0.25.2: HTTP client for testing
- python-dotenv 1.0.0: Environment variable management

## Build & Installation
```bash
# Clone repository
git clone <repository>
cd oedipus

# Option 1: Docker setup (all services)
docker compose up --build

# Option 2: Local development setup
python scripts/setup.py
docker compose up -d  # PostgreSQL + Redis
alembic upgrade head
```

## Docker
**Dockerfile**: Uses Python 3.11-slim base image
**Services**:
- PostgreSQL 15: Primary database
- Redis 7-alpine: Caching and job queue
**Configuration**: docker-compose.yml defines services with health checks

## Testing
**Framework**: pytest with pytest-asyncio
**Test Location**: tests/ directory
**Test Files**: test_api.py, test_metrics.py
**Run Command**:
```bash
pytest tests/
```

## Usage & Operations
**Start Services**:
```bash
# Terminal 1: Backend API
python scripts/start_backend.py

# Terminal 2: Celery worker
python scripts/start_worker.py

# Terminal 3: Frontend
python scripts/start_frontend.py
```

**Access Points**:
- Frontend UI: http://localhost:8501
- API Documentation: http://localhost:8000/docs
- API Health: http://localhost:8000/health

## Features
- **Dataset Management**: Upload and version input datasets
- **Output Data Upload**: Support for multi-output relationships
- **Information-Theoretic Analysis**: Metrics like entropy, information gain
- **Visualization Dashboard**: Interactive metric visualizations
- **Background Processing**: Celery-based task queue for analysis jobs
- **Database Migrations**: Alembic for schema versioning
- **Model Comparison**: Side-by-side comparison of multiple model outputs
- **Outlier Detection**: Statistical analysis to identify anomalous outputs
- **Alignment Analysis**: Coverage statistics and matched input tracking

## API Endpoints
- **Datasets**: `/api/v1/datasets/` - Create, list, and retrieve datasets
- **Outputs**: `/api/v1/datasets/{id}/outputs` - Manage output datasets
- **Analysis**: `/api/v1/analysis/run` - Run analysis jobs
- **Comparisons**: `/api/v1/comparisons/` - Create and manage model comparisons

## Performance
- 1,000 input/output pairs: < 5 minutes
- 10,000 inputs with multiple outputs: < 15 minutes
- Complex analysis with all metrics: < 2 minutes