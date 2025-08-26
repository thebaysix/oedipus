# Oedipus MVP - Phase 1 Architecture
*Observability & Analytics Infrastructure for AI Systems*

## Overview

Oedipus Phase 1 is a lightweight MVP focused on bulk upload analysis of AI model outputs. Users upload input datasets and corresponding output datasets, then receive comprehensive information-theoretic analysis to understand their model's behavior patterns.

**Core Value Proposition**: Bring your own data (inputs + outputs), get professional-grade analytics on model behavior without writing custom evaluation scripts.

## System Architecture

### Technology Stack

**Backend:**
- **FastAPI**: Async REST API with automatic OpenAPI documentation
- **PostgreSQL**: Primary database for structured data storage
- **Redis**: Caching and background job queue
- **Celery**: Asynchronous task processing for analysis jobs

**Frontend:**
- **Streamlit**: Rapid prototyping UI for MVP (will migrate to React in Phase 2)
- **Plotly**: Interactive visualizations and charts
- **Pandas**: Data manipulation and analysis

**Deployment:**
- **Docker**: Containerized application stack
- **Railway/Fly.io**: Simple deployment and scaling
- **Environment**: Single-server setup with horizontal scaling capability

### Core Data Models

```python
# Database Schema (SQLAlchemy models)

class Dataset(Base):
    id: UUID
    name: str
    user_id: UUID
    created_at: datetime
    inputs: Dict[str, str]  # mapping inputId -> input_string
    metadata: Dict  # user-defined metadata

class OutputDataset(Base):
    id: UUID
    name: str
    dataset_id: UUID  # foreign key to Dataset
    created_at: datetime
    outputs: Dict  # mapping (dataset_name, input_id) -> [output_strings]
    metadata: Dict

class AnalysisJob(Base):
    id: UUID
    output_dataset_id: UUID
    status: str  # pending/running/completed/failed
    results: Dict  # computed metrics
    created_at: datetime
    completed_at: datetime
```

### API Endpoints

```python
# Core REST API structure

POST /api/v1/datasets
GET  /api/v1/datasets
GET  /api/v1/datasets/{dataset_id}

POST /api/v1/datasets/{dataset_id}/outputs
GET  /api/v1/datasets/{dataset_id}/outputs

POST /api/v1/analysis/run
GET  /api/v1/analysis/{job_id}/status
GET  /api/v1/analysis/{job_id}/results
```

### Data Flow Architecture

```
User Upload → Data Validation → Storage → Analysis Queue → Metrics Computation → Results Storage → Visualization
```

1. **Data Ingestion Layer**
   - JSON file upload and validation
   - Schema verification for input/output mappings
   - Data cleaning and preprocessing

2. **Analysis Engine** 
   - Celery worker processes for async computation
   - Information-theoretic metrics calculation
   - Result caching and storage

3. **Presentation Layer**
   - Streamlit dashboard for data upload and visualization
   - Interactive charts and metric displays
   - Export capabilities for results

## Core Features - Phase 1

### 1. Dataset Management
- **Input Dataset Creation**: Upload JSON mapping `{inputId: input_string}`
- **Custom Naming**: User-defined dataset names and metadata
- **Dataset Versioning**: Track different versions of input datasets

### 2. Output Data Upload
- **Multi-Output Support**: One-to-many input→output relationships
- **Structured Format**: JSON mapping `{(dataset_name, input_id): [output_array]}`
- **Validation**: Ensure output data matches existing input datasets

### 3. Information-Theoretic Analysis

**Implemented Metrics:**

- **Input Entropy**: Measures distribution spread over inputs
  ```
  H(X) = -Σ p(x) log p(x)
  ```

- **Response Entropy**: Entropy of model outputs given inputs
  ```
  H(Y|X) = -Σ p(x,y) log p(y|x)
  ```

- **Information Gain**: Mutual information between inputs and outputs
  ```
  I(X;Y) = H(X) - H(X|Y)
  ```

- **Empowerment**: Influence of model decisions on output diversity
  ```
  E = I(A;X'|X) = H(A|X) - H(A|X,X')
  ```

**Basic Metrics:**
- **Character Count**: Distribution of output lengths
- **Token Count**: Using tiktoken for accurate token counting

### 4. Visualization Dashboard

**Streamlit Interface:**
- Upload forms for datasets and outputs
- Real-time analysis job status
- Interactive metric visualizations
- Data export functionality

## File Structure

```
oedipus-mvp/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── datasets.py
│   │   │   ├── outputs.py
│   │   │   └── analysis.py
│   │   └── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── redis.py
│   ├── models/
│   │   ├── dataset.py
│   │   ├── output.py
│   │   └── analysis.py
│   ├── services/
│   │   ├── dataset_service.py
│   │   ├── analysis_service.py
│   │   └── metrics/
│   │       ├── entropy.py
│   │       ├── information_gain.py
│   │       └── empowerment.py
│   └── workers/
│       └── analysis_worker.py
├── frontend/
│   ├── streamlit_app.py
│   ├── components/
│   │   ├── upload.py
│   │   ├── dashboard.py
│   │   └── visualizations.py
│   └── utils/
│       └── data_processing.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Development Workflow

### Local Development
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

### Data Processing Pipeline

1. **Upload Validation**
   - JSON schema validation
   - Input/output mapping verification
   - File size and format checks

2. **Background Processing**
   - Celery task queuing for heavy computations
   - Progress tracking and status updates
   - Error handling and retry logic

3. **Metrics Computation**
   - Parallel processing of information-theoretic metrics
   - Efficient algorithms for large datasets
   - Results caching and optimization

## Future Architecture Evolution

### Phase 2: Team Collaboration + CI/CD
**Planned Changes:**
- **Frontend**: Migrate from Streamlit to React/Next.js
- **Authentication**: User management and team workspaces
- **API Expansion**: RESTful API for external integrations
- **Real-time Updates**: WebSocket support for live analysis
- **Performance**: Database optimization and caching layers

### Phase 3: Agent Execution Support
**New Components:**
- **Time-series Database**: TimescaleDB for execution traces
- **Graph Analysis**: NetworkX for agent decision trees
- **Streaming Pipeline**: Kafka/Redis Streams for real-time data
- **Agent Framework Integrations**: LangChain, CrewAI plugins

### Phase 4: Statistical Analysis + Export
**Advanced Features:**
- **Statistical Engine**: SciPy/StatsModels integration
- **Report Generation**: PDF/HTML report templates
- **Advanced Visualizations**: D3.js custom charts
- **Data Pipeline**: ETL processes for external tools

## Success Metrics - Phase 1

**Technical:**
- Upload→Analysis→Results cycle < 5 minutes for 1000 input/output pairs
- Support datasets up to 10,000 inputs with multiple outputs
- 99% uptime for analysis processing

**User Experience:**
- Users can complete full workflow (upload→analyze→insights) in < 30 minutes
- Clear visualizations make metric trends immediately obvious
- Export functionality enables integration with existing workflows

**Business:**
- 10+ developers using weekly within first month
- Average session time > 20 minutes (indicating deep engagement)
- User return rate > 70% within one week

## Technical Considerations

### Scalability
- **Database**: Indexed queries for fast dataset retrieval
- **Compute**: Celery horizontal scaling for analysis jobs
- **Storage**: Efficient JSON storage with compression

### Security
- **Input Validation**: Strict schema validation for all uploads
- **Rate Limiting**: API throttling to prevent abuse
- **Data Privacy**: No data retention beyond user session (configurable)

### Monitoring
- **Application**: FastAPI built-in logging and metrics
- **Infrastructure**: Basic health checks and error tracking
- **User Analytics**: Upload patterns and feature usage

---

## Getting Started

1. **Prerequisites**: Docker, Python 3.9+, PostgreSQL, Redis
2. **Installation**: `docker-compose up` for full stack
3. **Usage**: Navigate to Streamlit interface, upload datasets, run analysis
4. **API**: OpenAPI documentation available at `/docs`

This MVP architecture prioritizes rapid development and user validation while maintaining a clear path to the comprehensive platform outlined in the full roadmap.