# Oedipus MVP - Phase 1

*Observability & Analytics Infrastructure for AI Systems*

## Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

### 1. Setup
```bash
# Clone and setup
git clone <repository>
cd oedipus
python scripts/setup.py
```

### 2. Start Services
```bash
# Terminal 1: Start backend API
python scripts/start_backend.py

# Terminal 2: Start Celery worker
python scripts/start_worker.py

# Terminal 3: Start frontend
python scripts/start_frontend.py
```

### 3. Access the Application
- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Manual Setup (Alternative)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Infrastructure
```bash
docker-compose up -d  # PostgreSQL + Redis
```

### 3. Initialize Database
```bash
alembic upgrade head
```

### 4. Start Services
```bash
# Backend API
uvicorn app.api.main:app --reload

# Celery Worker (new terminal)
celery -A app.workers.analysis_worker worker --loglevel=info

# Frontend (new terminal)
streamlit run frontend/streamlit_app.py
```

## Usage

### 1. Upload Input Dataset
- Navigate to "Upload Data" page
- Create JSON mapping: `{"input_id": "prompt_text"}`
- Use sample data or upload your own

### 2. Upload Output Dataset
- Select your input dataset
- Create JSON mapping: `{"input_id": ["output1", "output2"]}`
- Validate against input dataset

### 3. Run Analysis
- Go to "Analysis" page
- Click "Run Analysis"
- View real-time progress
- Explore comprehensive results

## Features

### Information-Theoretic Metrics
- **Input Entropy**: Diversity of input prompts
- **Response Entropy**: Diversity of outputs given inputs
- **Information Gain**: Mutual information between inputs/outputs
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

POST /api/v1/datasets/{id}/outputs       # Create output dataset
GET  /api/v1/datasets/{id}/outputs       # List output datasets

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

### Input Dataset
```json
{
    "input_1": "What is the capital of France?",
    "input_2": "Explain quantum computing",
    "input_3": "Write a haiku about spring"
}
```

### Output Dataset
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
└── docker-compose.yml
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
- Check Docker services: `docker-compose ps`

**Database Connection Error**
- Verify PostgreSQL is running: `docker-compose logs postgres`
- Check connection string in `.env`

**Celery Worker Not Processing**
- Ensure Redis is running: `docker-compose logs redis`
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
docker-compose logs [service_name]
```

## Performance

### Tested Limits
- ✅ 1,000 input/output pairs: < 5 minutes
- ✅ 10,000 inputs with multiple outputs: < 15 minutes
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