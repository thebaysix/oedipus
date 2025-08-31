# Oedipus React Frontend - Complete Setup Guide

This guide will help you set up and run the Oedipus Comparative Analysis React frontend application.

## Prerequisites

1. **Node.js 16+**: Required for running the React application
2. **Oedipus Backend**: Must be running on `http://localhost:8000`

## Quick Start

### Option 1: Automated Setup (Recommended)

```powershell
# Navigate to the React frontend directory
cd c:\Code\oedipus\react-frontend

# Run the automated setup (installs Node.js if needed)
.\setup.ps1

# Start the development server
.\start_react_frontend.ps1
```

### Option 2: Manual Setup

1. **Install Node.js**:
   - Visit https://nodejs.org/
   - Download and install the LTS version
   - Verify installation: `node --version` and `npm --version`

2. **Install dependencies**:
   ```powershell
   cd c:\Code\oedipus\react-frontend
   npm install
   ```

3. **Start the application**:
   ```powershell
   npm run dev
   ```

## Available Scripts

- `npm run dev` - Start development server (localhost:3000)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## PowerShell Helper Scripts

### `setup.ps1`
Installs Node.js (if needed) and project dependencies.

### `start_react_frontend.ps1`
Comprehensive startup script with backend connectivity checks.

**Options**:
- `-Install` - Force reinstall dependencies
- `-Build` - Build production version
- `-SkipNodeCheck` - Skip Node.js version check

**Examples**:
```powershell
# Standard startup
.\start_react_frontend.ps1

# Force dependency reinstall
.\start_react_frontend.ps1 -Install

# Build production version
.\start_react_frontend.ps1 -Build
```

## Backend Connection

The React app connects to the Oedipus FastAPI backend at `http://localhost:8000`.

**Required Backend Endpoints**:
- `GET /api/v1/datasets/` - List datasets
- `POST /api/v1/datasets/` - Upload prompt dataset
- `POST /api/v1/datasets/{id}/completions` - Upload completion dataset
- `POST /api/v1/comparisons/create` - Create comparison analysis
- `GET /api/v1/comparisons/{id}` - Get comparison results

**Start Backend Before Frontend**:
```powershell
# In the main Oedipus directory
cd c:\Code\oedipus
python scripts\start_backend.py
```

## Project Structure

```
react-frontend/
├── src/
│   ├── components/           # React components
│   │   ├── DatasetUpload/    # File upload and validation
│   │   ├── ComparisonTable/  # Data comparison interface
│   │   ├── MetricsComparison/ # Charts and statistics
│   │   ├── StatisticalTests/ # Test results display
│   │   ├── InsightsPanel/    # Auto-generated insights
│   │   └── Export/           # Report generation
│   ├── hooks/                # Custom React hooks
│   ├── types/                # TypeScript definitions
│   ├── utils/                # Helper functions
│   └── App.tsx               # Main application
├── public/                   # Static assets
├── package.json              # Dependencies and scripts
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # Tailwind CSS config
└── tsconfig.json             # TypeScript config
```

## Usage Workflow

1. **Upload Data**: Drag and drop CSV files (prompt + completion datasets)
2. **Review & Validate**: Check data preview and fix any issues
3. **Create Comparison**: Configure comparative analysis
4. **Explore Results**: View statistics, insights, and visualizations
5. **Export Reports**: Download or share analysis results

## CSV Data Format

### Prompt Dataset
```csv
prompt_id,prompt_text,category
001,What is machine learning?,technical
002,How to bake a cake?,lifestyle
```

### Completion Dataset
```csv
prompt_id,completion_text,model_version,timestamp
001,Machine learning is...,v1.0,2024-01-01
002,To bake a cake you...,v1.0,2024-01-01
```

**Required Columns**:
- Prompt Dataset: `prompt_id`, `prompt_text`
- Completion Dataset: `prompt_id`, `completion_text`

## Troubleshooting

### Common Issues

**Node.js Not Found**:
```
Error: 'node' is not recognized
```
- Install Node.js from https://nodejs.org/
- Restart PowerShell after installation

**Port Already in Use**:
```
Error: Port 3000 is already in use
```
- Find and stop the process using port 3000
- Or modify port in `vite.config.ts`

**Backend Connection Failed**:
```
API Error: Connection refused
```
- Ensure Oedipus backend is running on localhost:8000
- Check backend health: http://localhost:8000/health

**Dependencies Installation Failed**:
```powershell
# Clear cache and reinstall
npm cache clean --force
rm -r node_modules
rm package-lock.json
npm install
```

### Performance Optimization

**Large Datasets**:
- The app handles up to 50,000 rows per dataset
- For larger datasets, consider sampling or server-side processing

**Memory Usage**:
- Large comparisons are processed in the backend
- Frontend displays paginated results

## Development

### Adding New Components

1. Create component in appropriate `src/components/` subdirectory
2. Export from subdirectory `index.ts`
3. Import and use in parent components

### API Integration

API calls are centralized in `src/utils/api.ts` using the `ApiClient` class.

**Example**:
```typescript
import { apiClient } from '../utils/api';

const datasets = await apiClient.get<Dataset[]>('/api/v1/datasets/');
```

### State Management

- **Server State**: TanStack Query (`@tanstack/react-query`)
- **Client State**: Zustand (for complex state) or React hooks
- **Forms**: React Hook Form with validation

## Production Deployment

```powershell
# Build production version
npm run build

# Preview build (optional)
npm run preview

# Serve built files (dist/ directory)
```

The built application will be in the `dist/` directory and can be served by any static file server.

## Support

For issues with the React frontend:
1. Check browser console for JavaScript errors
2. Verify backend connectivity
3. Review network requests in browser dev tools
4. Check component props and state in React dev tools

For backend-related issues, refer to the main Oedipus documentation.