# Oedipus Setup Guide

This guide covers the streamlined setup process for the Oedipus MVP.

## Quick Setup

### Backend Setup
```powershell
# Setup Python backend with Docker services
.\setup_backend.ps1

# Or skip Docker if you want to run services separately
.\setup_backend.ps1 -SkipDocker
```

### Frontend Setup
```powershell
# Setup React frontend with Node.js dependencies
.\setup_frontend.ps1
```

## Starting the Application

### Backend Services
```powershell
# Terminal 1: Start the API server
python scripts\start_backend.py

# Terminal 2: Start the Celery worker
python scripts\start_worker.py
```

### Frontend
```powershell
# Terminal 3: Start React frontend
.\start_react_frontend.ps1

# Or from the react-frontend directory
cd react-frontend
npm run dev
```

## Access Points

- **React Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## Prerequisites

### Backend
- Python 3.11+ (with pip)
- Docker Desktop (optional, for PostgreSQL and Redis)

### Frontend
- Node.js 18+ (with npm)

## Setup Scripts Overview

| Script | Purpose | Requirements |
|--------|---------|--------------|
| `setup_backend.ps1` | Python dependencies + Docker services | Python, Docker (optional) |
| `setup_frontend.ps1` | Node.js dependencies | Node.js |
| `start_react_frontend.ps1` | Start React dev server | Frontend setup complete |

## Troubleshooting

### Backend Issues
- Ensure Python is in your PATH
- For Docker issues, make sure Docker Desktop is running
- Use `-SkipDocker` flag if you want to run PostgreSQL/Redis separately

### Frontend Issues
- Ensure Node.js is in your PATH
- Delete `node_modules` and run setup again if needed
- Check that port 3000 is available

### Database Issues
- Run `alembic upgrade head` manually if database initialization fails
- Ensure PostgreSQL is running (via Docker or locally)

## Development Workflow

1. Run backend setup once: `.\setup_backend.ps1`
2. Run frontend setup once: `.\setup_frontend.ps1`
3. Start backend services: `python scripts\start_backend.py` + `python scripts\start_worker.py`
4. Start frontend: `.\start_react_frontend.ps1`
5. Access the application at http://localhost:3000

The setup scripts only need to be run once or when dependencies change.