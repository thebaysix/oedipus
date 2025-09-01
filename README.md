# Oedipus

Observation → grounding in monitoring/logging model completions.

Evaluation → structured scoring of model behaviors.

Diagnostics → pinpointing failure modes, systematic weaknesses.

Information-theoretic → ties directly to your entropy/empowerment/information gain metrics.

Performance → addresses task completion, factual accuracy, benchmarks.

Understanding → reflects deeper interpretability and model behavior insights.

Safety → emphasizes alignment, risk detection, and responsible deployment.

## Preview

![Preview of Oedipus](assets/oedipus-preview.png)

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

### 4. View Results - Business-Focused Analysis
- **Step 3: View Results** - Get actionable insights for decision-making
- **Model Comparison Summary**: Instant overview with decision guidance
- **⭐ Star Ratings**: See statistical significance at a glance (1-3 stars)
- **🔴🟡🟢 Impact Indicators**: Visual cues for business impact levels
- **📊 Performance Numbers**: Raw dataset values always visible (e.g., Dataset A: 124.920, Dataset B: 170.911)
- **💡 Business Insights**: Plain-language explanations with percentage differences
- **🎯 Recommendations**: Specific advice on which metrics should drive your decision
- **📋 Technical Details**: Expandable sections for statistical depth (p-values, effect sizes, confidence intervals)
- **📊 Interactive Charts**: Visual comparisons with business context
- **📤 Export Options**: Business reports and technical data downloads

### Example Workflow & Expected Results
1. **Upload prompts.csv** with your test prompts (e.g., 500 customer service scenarios)
2. **Upload gpt4_completions.csv** with GPT-4 responses
3. **Upload claude_completions.csv** with Claude responses  
4. **Create comparison** named "GPT-4 vs Claude for Customer Service"
5. **Monitor progress** through the 4-step analysis process with real-time updates
6. **Get business insights** like:
   - 🔴 **Completion Length**: "Claude shows 26.9% longer responses - major factor for detailed support"
   - ⭐⭐⭐ **High Confidence**: "Very significant difference (p < 0.001) - reliable for decision-making"
   - 🎯 **Recommendation**: "Choose Claude for comprehensive support, GPT-4 for concise responses"
7. **Make informed decisions** based on clear business impact indicators

## Features

### Business-Focused Comparative Analysis
Oedipus provides an intuitive, business-friendly interface for comparing AI model performance with actionable insights for decision-making.

#### **Quick Decision Making**
- **⭐ Star Rating System**: Instantly see statistical significance (1-3 stars)
- **🔴🟡🟢 Impact Indicators**: Visual cues for business impact (Large/Medium/Small)
- **📊 At-a-Glance Numbers**: Raw performance values always visible
- **🎯 Decision Guidance**: Contextual recommendations based on your results

#### **Progressive Information Disclosure**
- **Business Summary First**: Key insights and recommendations prominently displayed
- **Technical Details Available**: Expandable sections for statistical details (p-values, effect sizes, confidence intervals)
- **Plain Language Explanations**: Complex statistics translated into business terms
- **Actionable Recommendations**: Specific guidance on which metrics matter most

#### **Comprehensive Model Comparison**
- **Side-by-side Analysis**: Compare multiple AI model completions simultaneously
- **Automatic Data Alignment**: Smart matching of prompts across completion datasets
- **Real-time Progress Tracking**: Visual progress bar with step-by-step updates
- **Coverage Analysis**: Data quality assessment and alignment statistics

### Statistical Metrics & Business Interpretation

The system analyzes multiple dimensions of model performance with both statistical rigor and business relevance:

#### **Completion Length Analysis**
- **Business Value**: Understand which model provides more detailed vs. concise responses
- **Decision Impact**: Choose models based on your need for brevity or comprehensiveness
- **Statistical Measure**: Compares average response length between models
- **Interpretation**: 
  - 🔴 Large differences (≥26% variation): Major factor in model selection
  - 🟡 Medium differences (10-25% variation): Consider for specific use cases
  - 🟢 Small differences (<10% variation): Minor consideration

#### **Completion Count Analysis**
- **Business Value**: Evaluate model creativity and response variety
- **Decision Impact**: Important for applications requiring diverse outputs
- **Statistical Measure**: Compares number of completions per prompt
- **Interpretation**: 
  - Higher count = More diverse/multiple responses per prompt
  - Lower count = More focused, single-response behavior

#### **Unique Completion Ratio**
- **Business Value**: Measure response originality and avoid repetitive outputs
- **Decision Impact**: Critical for creative applications and user engagement
- **Statistical Measure**: Ratio of unique responses within each model
- **Interpretation**: 
  - 1.0 = All responses unique (maximum creativity)
  - 0.5 = Half of responses are duplicates
  - 0.0 = All responses identical (no creativity)

#### **Word Count Distribution**
- **Business Value**: Assess vocabulary richness and response complexity
- **Decision Impact**: Choose models that match your content depth requirements
- **Statistical Measure**: Analyzes vocabulary usage patterns
- **Interpretation**: 
  - Higher word count = More detailed, comprehensive responses
  - Lower word count = More concise, focused responses

#### **Response Diversity Index**
- **Business Value**: Understand consistency vs. variability in model behavior
- **Decision Impact**: Balance predictability with creative variation
- **Statistical Measure**: Overall variation in completion patterns
- **Interpretation**: 
  - Higher diversity = More varied response patterns (creative but less predictable)
  - Lower diversity = More consistent response patterns (predictable but potentially repetitive)

### Statistical Interpretation Guide

The system uses a business-friendly approach to statistical analysis while maintaining scientific rigor:

#### **Star Rating System (Statistical Significance)**
- **⭐⭐⭐ Highly Significant** (p < 0.001): Very strong evidence of difference - high confidence for decision-making
- **⭐⭐ Very Significant** (p < 0.01): Strong evidence of difference - reliable for business decisions  
- **⭐ Significant** (p < 0.05): Moderate evidence of difference - consider alongside other factors
- **No Stars** (p ≥ 0.05): No significant difference - models perform similarly on this metric

#### **Business Impact Indicators (Effect Sizes)**
- **🔴 Large Impact** (|d| ≥ 0.8): Substantial difference - major factor in model selection
- **🟡 Medium Impact** (|d| ≥ 0.5): Moderate difference - important consideration for specific use cases
- **🟢 Small Impact** (|d| ≥ 0.2): Minor difference - may not affect most business decisions
- **⚪ Minimal Impact** (|d| < 0.2): Negligible difference - focus on other metrics

#### **Confidence Indicators**
- **✅ High Confidence**: 95% confidence interval doesn't include 0 - reliable difference between models
- **⚠️ Low Confidence**: 95% confidence interval includes 0 - difference may not be reliable

#### **Technical Details (Available on Demand)**
For users who need detailed statistical information, each metric provides expandable access to:
- **P-values**: Exact statistical significance values
- **Effect Sizes (Cohen's d)**: Standardized measure of difference magnitude  
- **95% Confidence Intervals**: Range where true difference likely falls
- **Technical Notes**: Explanations of statistical concepts and limitations

### Intelligent Business Insights

The system automatically generates actionable insights tailored for business decision-making:

#### **Model Comparison Summary**
- **Quick Decision Guide**: Immediate recommendations based on high-impact differences
- **Balanced Comparison**: Guidance when differences are moderate but significant
- **Similar Performance**: Advice when models perform equivalently

#### **Key Business Insights**
- **High Impact Metrics** (🔴): Major differentiators that should influence model choice
- **Medium Impact Metrics** (🟡): Moderate differences to consider for specific use cases  
- **Performance Percentages**: Concrete numbers showing relative performance differences
- **Contextual Recommendations**: Specific advice on whether differences matter for your use case

#### **Dataset Quality Assessment**
- **Coverage Analysis**: Alignment success rate between prompt and completion datasets
- **Data Quality Metrics**: Identification of unmatched prompts and data completeness
- **Reliability Indicators**: Assessment of statistical confidence in results

#### **Decision Support**
- **Primary Decision Factors**: Highlights which metrics should drive your model selection
- **Secondary Considerations**: Additional factors that may influence specific use cases
- **Risk Assessment**: Confidence levels and reliability of observed differences
- **Use Case Guidance**: Recommendations based on whether you need consistency vs. creativity

### User Experience & Interface

#### **Business-First Design**
- **Clean, Intuitive Layout**: Information organized by business priority, not statistical complexity
- **Visual Hierarchy**: Most important insights prominently displayed, technical details available on demand
- **Progressive Disclosure**: Start with business summary, expand to technical details as needed
- **Mobile-Responsive**: Works on desktop, tablet, and mobile devices

#### **Interactive Visualizations**
- **Statistical Summary Cards**: Each metric displayed as an easy-to-scan card with visual indicators
- **Comparison Charts**: Interactive bar charts showing metric comparisons with business context
- **Progress Tracking**: Real-time analysis progress with step-by-step updates and estimated completion
- **Data Tables**: Side-by-side view of aligned completions for detailed inspection

#### **Export & Sharing**
- **Business Reports**: Export analysis results formatted for stakeholder presentations
- **Technical Data**: Download raw statistical data (JSON/CSV) for further analysis
- **Shareable Links**: Generate URLs to share specific comparison results
- **Print-Friendly**: Optimized layouts for printing reports

### Data Processing & Quality

#### **Smart Data Handling**
- **Drag-and-Drop Upload**: Easy CSV file upload with instant validation
- **Automatic Format Detection**: Recognizes prompt_id/prompt_text and completion formats
- **Real-time Preview**: See your data structure before processing
- **Error Detection**: Clear feedback on data format issues with suggested fixes

#### **Quality Assurance**
- **Data Alignment**: Automatic matching of prompts across completion datasets
- **Coverage Analysis**: Reports on data completeness and alignment success rates
- **Validation Checks**: Ensures statistical analysis requirements are met
- **Background Processing**: Non-blocking analysis with progress indicators

#### **Performance & Reliability**
- **Scalable Analysis**: Handles datasets from hundreds to tens of thousands of entries
- **Robust Statistics**: Uses established statistical methods (t-tests, Cohen's d, confidence intervals)
- **Error Handling**: Graceful handling of edge cases and data quality issues
- **Real-time Updates**: Live progress tracking during analysis

## Why Choose Oedipus for AI Model Comparison?

### **Business-First Approach**
Unlike traditional statistical tools that overwhelm users with technical jargon, Oedipus translates complex statistical analysis into clear business insights. You get immediate answers to questions like "Which model should I choose?" and "How confident can I be in this decision?"

### **No Statistics Background Required**
- **⭐ Star ratings** indicating significance (p-values)
- **🔴🟡🟢 Visual indicators** show business impact at a glance  
- **Plain language explanations** eliminate statistical complexity
- **Actionable recommendations** guide decision-making

### **Technical Rigor Maintained**
While the interface is business-friendly, the underlying analysis uses rigorous statistical methods:
- **T-tests** for significance testing
- **Cohen's d** for effect size measurement
- **95% Confidence intervals** for reliability assessment
- **Multiple comparison corrections** when appropriate

### **Progressive Disclosure**
- **Start simple**: See business impact and recommendations first
- **Dig deeper**: Expand to view technical details when needed
- **Full transparency**: Access all statistical calculations and assumptions
- **Flexible depth**: Choose your level of detail based on your role and needs

### **Real-World Impact**
Perfect for:
- **Product Managers**: Make data-driven model selection decisions
- **Engineering Teams**: Validate model performance with statistical confidence
- **Business Stakeholders**: Understand AI performance without statistical training
- **Data Scientists**: Access full statistical details while communicating results clearly

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