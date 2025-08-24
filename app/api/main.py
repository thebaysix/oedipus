from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import datasets, outputs, analysis
from ..core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Oedipus MVP API",
    description="Observability & Analytics Infrastructure for AI Systems",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(datasets.router)
app.include_router(outputs.router)
app.include_router(analysis.router)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Oedipus MVP API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)