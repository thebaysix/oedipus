# Oedipus

Observation → grounding in monitoring/logging model completions.
Evaluation → structured scoring of model behaviors.
Diagnostics → pinpointing failure modes, systematic weaknesses.
Information-theoretic → ties directly to your entropy/empowerment/information gain metrics.
Performance → addresses task completion, factual accuracy, benchmarks.
Understanding → reflects deeper interpretability and model behavior insights.
Safety → emphasizes alignment, risk detection, and responsible deployment.

# Oedipus MVP - Phase 1

*Observability & Analytics Infrastructure for AI Systems*

## Quick Start

### Prerequisites
1. Python 3.11+
2. Docker Desktop (https://www.docker.com/products/docker-desktop)
   - Make sure Docker is running and added to your system PATH.
3. Git

---

## Option 1: Run with Docker

This starts everything (API, DB, Redis, Worker, Frontend) in containers.

```bash
# Clone repository
git clone <repository>
cd oedipus

# Start full stack
docker compose up --build
```

### Access the Application
- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

To stop:
```bash
docker compose down
```

---

## Option 2: Local Development Setup

### 1. Setup Environment
```bash
# Clone and setup
git clone <repository>
cd oedipus
python scripts/setup.py
```

### 2. Start Infrastructure
```bash
docker compose up -d  # PostgreSQL + Redis
```

### 3. Initialize Database
```bash
alembic upgrade head
```

### 4. Start Services
```bash
# Terminal 1: Backend API
python scripts/start_backend.py

# Terminal 2: Celery worker
python scripts/start_worker.py

# Terminal 3: Frontend
python scripts/start_frontend.py
```

### Access the Application
- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

---

## Usage

### 1. Upload Prompt Dataset
- Navigate to "Upload Data" page
- Create JSON mapping: `{"prompt_id": "prompt_text"}`
- Use sample data or upload your own

### 2. Upload Completion Dataset
- Select your prompt dataset
- Create JSON mapping: `{"prompt_id": ["completion1", "completion2"]}`
- Validate against prompt dataset

### 3. Run Analysis
- Go to "Analysis" page
- Click "Run Analysis"
- View real-time progress
- Explore comprehensive results

## Features

### Information-Theoretic Metrics
- **Input Entropy**: Diversity of input prompts
- **Response Entropy**: Diversity of completions given prompts
- **Information Gain**: Mutual information between prompts/completions
- **Empowerment**: Model decision influence on output diversity

### Visualizations
- Interactive entropy charts
- Output length distributions
- Diversity metrics dashboard
- Export capabilities (JSON/CSV)

### Data Processing
- JSON validation and error handling
- Sample data for quick testing
- Real-time analysis progress
- Background job processing

## API Endpoints

```
POST /api/v1/datasets                    # Create dataset
GET  /api/v1/datasets                    # List datasets
GET  /api/v1/datasets/{id}               # Get dataset

POST /api/v1/datasets/{id}/completions       # Create completion dataset
GET  /api/v1/datasets/{id}/completions       # List completion datasets

POST /api/v1/analysis/run                # Start analysis job
GET  /api/v1/analysis/{job_id}/status    # Check job status
GET  /api/v1/analysis/{job_id}/results   # Get results
```

## Architecture

```
Frontend (Streamlit) → API (FastAPI) → Database (PostgreSQL)
                    ↓
                 Worker (Celery) → Cache (Redis)
```

### Components
- **FastAPI**: REST API with automatic documentation
- **PostgreSQL**: Primary data storage
- **Redis**: Caching and job queue
- **Celery**: Background task processing
- **Streamlit**: Interactive web interface

## Data Format

### Prompt Dataset
```json
{
    "input_1": "What is the capital of France?",
    "input_2": "Explain quantum computing",
    "input_3": "Write a haiku about spring"
}
```

### Completion Dataset
```json
{
    "input_1": [
        "The capital of France is Paris.",
        "Paris is the capital city of France."
    ],
    "input_2": [
        "Quantum computing uses quantum mechanics...",
        "It's a type of computation that harnesses..."
    ]
}
```

## Development

### Project Structure
```
oedipus/
├── app/
│   ├── api/           # FastAPI routes
│   ├── core/          # Configuration & database
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── workers/       # Celery tasks
├── frontend/
│   ├── components/    # Streamlit components
│   └── utils/         # Helper functions
├── scripts/           # Setup & start scripts
└── docker compose.yml
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Troubleshooting

### Common Issues

**API Connection Failed**
- Ensure backend is running on port 8000
- Check Docker services: `docker compose ps`

**Database Connection Error**
- Verify PostgreSQL is running: `docker compose logs postgres`
- Check connection string in `.env`

**Celery Worker Not Processing**
- Ensure Redis is running: `docker compose logs redis`
- Check worker logs for errors

**Analysis Takes Too Long**
- Large datasets may take several minutes
- Check worker status and logs
- Consider reducing dataset size for testing

### Logs
```bash
# API logs
uvicorn app.api.main:app --log-level debug

# Worker logs
celery -A app.workers.analysis_worker worker --loglevel=debug

# Docker service logs
docker compose logs [service_name]
```

## Performance

### Tested Limits
- ✅ 1,000 prompt/completion pairs: < 5 minutes
- ✅ 10,000 prompts with multiple completions: < 15 minutes
- ✅ Complex analysis with all metrics: < 2 minutes

### Optimization Tips
- Use smaller datasets for initial testing
- Monitor memory usage with large datasets
- Consider horizontal scaling for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- 📖 Full documentation: See `oedipus_mvp_readme.md`
- 🐛 Issues: Create GitHub issue
- 💬 Questions: Open discussion

---

**Built with ❤️ using FastAPI, Streamlit, and modern Python tools**