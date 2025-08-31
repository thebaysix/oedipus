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
- **React Frontend**: http://localhost:3000 (Primary Interface)
- **Legacy Streamlit UI**: http://localhost:8501 (Alternative Interface)
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

# Terminal 3: React Frontend
cd react-frontend
npm install
npm run dev

# Terminal 4: Legacy Streamlit Frontend (optional)
python scripts/start_frontend.py
```

### Access the Application
- **React Frontend**: http://localhost:3000 (Primary Interface)
- **Legacy Streamlit UI**: http://localhost:8501 (Alternative Interface)
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

---

## Usage

### 1. Upload Prompt Dataset
- Navigate to the main application at http://localhost:3000
- **Step 1: Upload Data** - Drag and drop your CSV file containing prompts
- Required format: `prompt_id,prompt_text`
- Example:
  ```csv
  prompt_1,"What is artificial intelligence?"
  prompt_2,"Explain quantum computing"
  prompt_3,"Write a short story about robots"
  ```

### 2. Upload Completion Datasets
- **Step 1 (continued)** - Upload CSV files containing model completions
- Required format: `prompt_id,completion_text`
- Example:
  ```csv
  prompt_1,"AI is machine intelligence that simulates human cognition"
  prompt_1,"Artificial intelligence refers to computer systems that can think"
  prompt_2,"Quantum computing uses quantum mechanics for computation"
  prompt_2,"It leverages quantum bits to process information"
  ```
- Upload multiple completion datasets to compare different models

### 3. Create Comparison
- **Step 2: Create Comparison** - Configure your analysis
- Select which completion datasets to compare
- Choose alignment key (typically "prompt_id")
- Set comparison name and parameters

### 4. View Results
- **Step 3: View Results** - Explore comprehensive analysis
- **Real-time Progress**: Watch analysis progress with visual indicators
- **Statistical Metrics**: View detailed comparison statistics
- **Automated Insights**: Read AI-generated observations about your data
- **Interactive Charts**: Explore visual comparisons between models
- **Export Options**: Download results for further analysis

### Example Workflow
1. **Upload prompts.csv** with your test prompts
2. **Upload gpt4_completions.csv** with GPT-4 responses
3. **Upload claude_completions.csv** with Claude responses
4. **Create comparison** named "GPT-4 vs Claude Analysis"
5. **Monitor progress** through the 4-step analysis process
6. **Explore results** with statistical significance testing and insights

## Features

### Comparative Analysis
- **Side-by-side Model Comparison**: Compare multiple AI model completions
- **Statistical Significance Testing**: T-tests with p-values and effect sizes
- **Data Alignment**: Automatic matching of prompts across completion datasets
- **Real-time Progress Tracking**: Visual progress bar with step-by-step updates

### Statistical Metrics
The analysis computes comprehensive metrics for comparing model performance:

#### **Completion Length Analysis**
- **Purpose**: Compares average response length between models
- **Interpretation**: 
  - Positive effect size: Model A generates longer responses
  - Negative effect size: Model B generates longer responses
  - P-value < 0.05: Statistically significant difference in length

#### **Completion Count Analysis**
- **Purpose**: Compares number of completions per prompt
- **Interpretation**: 
  - Higher count indicates more diverse/multiple responses
  - Useful for evaluating model creativity and response variety

#### **Unique Completion Ratio**
- **Purpose**: Measures response diversity within each model
- **Interpretation**: 
  - Higher ratio = more unique, diverse responses
  - Lower ratio = more repetitive responses
  - Range: 0.0 (all identical) to 1.0 (all unique)

#### **Word Count Distribution**
- **Purpose**: Analyzes vocabulary richness and response complexity
- **Interpretation**: 
  - Higher word count may indicate more detailed responses
  - Significant differences suggest varying response styles

#### **Response Diversity Index**
- **Purpose**: Measures overall variation in completion patterns
- **Interpretation**: 
  - Higher diversity = more varied response patterns
  - Lower diversity = more consistent response patterns

### Statistical Interpretation Guide

#### **P-Values (Statistical Significance)**
- **p < 0.001**: Highly significant difference (⭐⭐⭐)
- **p < 0.01**: Very significant difference (⭐⭐)
- **p < 0.05**: Significant difference (⭐)
- **p ≥ 0.05**: No significant difference

#### **Effect Sizes (Cohen's d)**
- **|d| ≥ 0.8**: Large effect (substantial difference)
- **|d| ≥ 0.5**: Medium effect (moderate difference)
- **|d| ≥ 0.2**: Small effect (minor difference)
- **|d| < 0.2**: Negligible effect (minimal difference)

#### **Confidence Intervals**
- **95% Confidence Interval**: Range where true difference likely falls
- **Doesn't include 0**: Suggests reliable difference between models
- **Includes 0**: Difference may not be reliable

### Automated Insights
The system generates intelligent observations about your data:

#### **Dataset Coverage Analysis**
- Reports alignment success rate between prompt and completion datasets
- Identifies unmatched prompts that couldn't be compared
- Provides coverage statistics for data quality assessment

#### **Statistical Summary**
- Highlights significant differences between models
- Identifies which model performs better on specific metrics
- Suggests areas for further investigation

#### **Performance Patterns**
- Detects consistent patterns across multiple metrics
- Identifies outliers or unusual response behaviors
- Provides actionable recommendations for model improvement

### Visualizations
- **Interactive Statistical Charts**: Bar charts showing metric comparisons
- **Progress Tracking**: Real-time analysis progress with step indicators
- **Comparison Tables**: Side-by-side view of aligned completions
- **Export Capabilities**: Download results as JSON/CSV for further analysis

### Data Processing
- **CSV Upload Support**: Easy drag-and-drop file upload
- **Data Validation**: Automatic format checking and error reporting
- **Real-time Preview**: See your data before processing
- **Background Analysis**: Non-blocking statistical computation

## API Endpoints

### Dataset Management
```
POST /api/v1/datasets/                   # Create prompt dataset
GET  /api/v1/datasets/                   # List prompt datasets
GET  /api/v1/datasets/{id}               # Get specific dataset

POST /api/v1/datasets/{id}/completions   # Create completion dataset
GET  /api/v1/datasets/{id}/completions   # List completion datasets for dataset
```

### Comparison Analysis
```
POST /api/v1/comparisons/create          # Create new comparison analysis
GET  /api/v1/comparisons/                # List all comparisons
GET  /api/v1/comparisons/{id}            # Get comparison results
DELETE /api/v1/comparisons/{id}          # Delete comparison
```

### System Health
```
GET  /health                             # API health check
GET  /api/v1/datasets/                   # Database connectivity test
```

## Architecture

```
React Frontend → API (FastAPI) → Database (PostgreSQL)
             ↓
    Streamlit (Legacy) → Background Tasks → Redis Cache
```

### Components
- **React Frontend**: Modern TypeScript-based UI with real-time updates
- **FastAPI**: REST API with automatic documentation and background tasks
- **PostgreSQL**: Primary data storage with JSON support
- **Redis**: Caching and session storage
- **Streamlit**: Legacy interface (still available)
- **Background Tasks**: Async analysis processing

## Data Format

### Prompt Dataset (CSV)
```csv
prompt_id,prompt_text
prompt_1,"What is the capital of France?"
prompt_2,"Explain quantum computing"
prompt_3,"Write a haiku about spring"
```

### Completion Dataset (CSV)
```csv
prompt_id,completion_text
prompt_1,"The capital of France is Paris."
prompt_1,"Paris is the capital city of France."
prompt_2,"Quantum computing uses quantum mechanics for computation."
prompt_2,"It's a type of computation that harnesses quantum properties."
prompt_3,"Cherry blossoms bloom, / Gentle breeze carries petals, / Spring awakens life."
```

### Alternative: JSON Format (Legacy)
Both JSON and CSV formats are supported for backward compatibility:

**Prompt Dataset (JSON)**:
```json
{
    "prompt_1": "What is the capital of France?",
    "prompt_2": "Explain quantum computing",
    "prompt_3": "Write a haiku about spring"
}
```

**Completion Dataset (JSON)**:
```json
{
    "prompt_1": [
        "The capital of France is Paris.",
        "Paris is the capital city of France."
    ],
    "prompt_2": [
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
│   ├── services/      # Business logic & statistical analysis
│   └── workers/       # Background tasks
├── react-frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── types/         # TypeScript definitions
│   │   └── utils/         # Helper functions
│   ├── package.json       # Node.js dependencies
│   └── vite.config.ts     # Build configuration
├── frontend/              # Legacy Streamlit interface
│   ├── components/        # Streamlit components
│   └── utils/             # Helper functions
├── scripts/               # Setup & start scripts
├── tests/                 # Test suite
├── alembic/              # Database migrations
└── docker-compose.yml    # Container orchestration
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