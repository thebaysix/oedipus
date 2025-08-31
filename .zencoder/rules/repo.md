---
description: Repository Information Overview
alwaysApply: true
---

# Oedipus MVP Information

## Summary
Oedipus is an observability and analytics infrastructure for AI systems. The repository contains a fully implemented MVP with a primary focus on comparative analysis of AI model completions. The system provides comprehensive information-theoretic analysis of model behavior patterns and features a new React-based frontend optimized for side-by-side comparison of multiple model completions.

## Structure
- **app/**: Backend FastAPI application
  - **api/**: API routes and endpoints (datasets, completions, analysis, comparisons)
  - **core/**: Configuration and database setup
  - **models/**: SQLAlchemy database models
  - **schemas/**: Pydantic validation schemas
  - **services/**: Business logic and analysis services
  - **workers/**: Celery background tasks
- **react-frontend/**: New React-based user interface
  - **src/components/**: UI components (ComparisonTable, DatasetUpload, MetricsComparison)
  - **src/hooks/**: Custom React hooks for API integration
  - **src/utils/**: Helper functions for data processing
- **frontend/**: Legacy Streamlit-based user interface
- **scripts/**: Setup and startup scripts
- **tests/**: Test suite for API and metrics
- **alembic/**: Database migration scripts with version history

## Language & Runtime
**Language**: Python 3.13.7 (Backend), TypeScript/JavaScript (Frontend)
**Build System**: pip (Backend), Vite (Frontend)
**Package Manager**: pip (Backend), npm (Frontend)
**Database**: PostgreSQL 15
**Cache/Queue**: Redis 7

## Dependencies

### Backend Dependencies
**Main Dependencies**:
- FastAPI 0.104.1+: API framework
- SQLAlchemy 1.4.48: ORM
- Alembic 1.12.1: Database migrations
- Celery 5.3.4: Background task processing
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

### React Frontend Dependencies
**Main Dependencies**:
- React 18.2.0: UI framework
- TypeScript: Type-safe development
- React Router 6.30.1: Navigation
- TanStack React Query 4.32.6: Data fetching
- Recharts 2.8.0: Data visualization
- Zustand 4.4.1: State management
- React Dropzone 14.2.3: File upload
- PapaParse 5.4.1: CSV parsing

**Development Dependencies**:
- Vite 4.4.5: Build tool
- Tailwind CSS 3.3.3: Utility-first CSS
- ESLint 8.45.0: Code linting
- TypeScript 5.0.2: Type checking

## Build & Installation

### Backend
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

### React Frontend
```bash
# From repository root
cd react-frontend

# Install dependencies
npm install

# Start development server
npm run dev
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

# Terminal 3: React Frontend
cd react-frontend
npm run dev
# Or use the PowerShell script
.\start_react_frontend.ps1
```

**Access Points**:
- React Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- API Health: http://localhost:8000/health

## Features
- **Dataset Management**: Upload and version prompt datasets
- **Completion Data Upload**: Support for multi-completion relationships
- **Comparative Analysis**: Side-by-side comparison of multiple model completions
- **Statistical Testing**: Significance testing between model outputs
- **Interactive Visualizations**: Charts and metrics for model comparison
- **Automated Insights**: AI-generated observations about model differences
- **Information-Theoretic Analysis**: Metrics like entropy, information gain
- **Background Processing**: Celery-based task queue for analysis jobs
- **Database Migrations**: Alembic for schema versioning
- **Model Comparison**: Side-by-side comparison of multiple model completions
- **Outlier Detection**: Statistical analysis to identify anomalous completions
- **Alignment Analysis**: Coverage statistics and matched input tracking

## API Endpoints
- **Datasets**: `/api/v1/datasets/` - Create, list, and retrieve datasets
- **Outlier Detection**: Statistical analysis to identify anomalous completions
- **Alignment Analysis**: Coverage statistics and matched prompt tracking

## API Endpoints
- **Datasets**: `/api/v1/datasets/` - Create, list, and retrieve prompt datasets
- **Completions**: `/api/v1/datasets/{id}/completions` - Manage completion datasets
- **Analysis**: `/api/v1/analysis/run` - Run analysis jobs
- **Comparisons**: `/api/v1/comparisons/` - Create and manage model comparisons

## React Frontend
**Key Components**:
- **ComparisonTable**: Side-by-side view of model completions
- **DatasetUpload**: CSV upload with validation
- **MetricsComparison**: Statistical visualizations
- **StatisticalTests**: Hypothesis testing results
- **InsightsPanel**: Auto-generated insights
- **Export**: Report generation

**Routes**:
- **Main App** (`/`): Complete comparative analysis workflow
- **Diagnostic** (`#/diagnostic`): System health checks
- **Simple Test** (`#/simple`): Basic rendering verification
- **Debug Hooks** (`#/debug`): API integration debugging

## Performance
- 1,000 prompt/completion pairs: < 5 minutes
- 10,000 prompts with multiple completions: < 15 minutes
- Complex analysis with all metrics: < 2 minutes

## Terminology Update
The project has standardized terminology:
- "Input" → "Prompt": Text provided to the AI model
- "Output" → "Completion": Text generated by the AI model
- Database schema and API endpoints updated accordingly