import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.main import app
from app.core.database import get_db, Base
import tempfile
import os

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Oedipus MVP API"

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_dataset():
    """Test creating a dataset."""
    dataset_data = {
        "name": "Test Dataset",
        "inputs": {
            "input_1": "What is AI?",
            "input_2": "Explain machine learning"
        },
        "metadata": {"test": True}
    }
    
    response = client.post("/api/v1/datasets/", json=dataset_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "Test Dataset"
    assert len(data["inputs"]) == 2
    assert "id" in data

def test_get_datasets():
    """Test getting datasets."""
    response = client.get("/api/v1/datasets/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_create_output_dataset():
    """Test creating an output dataset."""
    # First create an input dataset
    dataset_data = {
        "name": "Test Dataset for Outputs",
        "inputs": {
            "input_1": "What is AI?",
            "input_2": "Explain ML"
        }
    }
    
    dataset_response = client.post("/api/v1/datasets/", json=dataset_data)
    assert dataset_response.status_code == 201
    dataset_id = dataset_response.json()["id"]
    
    # Now create output dataset
    output_data = {
        "name": "Test Outputs",
        "outputs": {
            "input_1": ["AI is artificial intelligence", "AI mimics human intelligence"],
            "input_2": ["ML is machine learning"]
        }
    }
    
    response = client.post(f"/api/v1/datasets/{dataset_id}/outputs", json=output_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "Test Outputs"
    assert data["dataset_id"] == dataset_id

def test_analysis_job_creation():
    """Test creating an analysis job."""
    # Create dataset and output dataset first
    dataset_data = {
        "name": "Analysis Test Dataset",
        "inputs": {"input_1": "Test input"}
    }
    
    dataset_response = client.post("/api/v1/datasets/", json=dataset_data)
    dataset_id = dataset_response.json()["id"]
    
    output_data = {
        "name": "Analysis Test Outputs",
        "outputs": {"input_1": ["Test output 1", "Test output 2"]}
    }
    
    output_response = client.post(f"/api/v1/datasets/{dataset_id}/outputs", json=output_data)
    output_id = output_response.json()["id"]
    
    # Create analysis job
    job_data = {"output_dataset_id": output_id}
    response = client.post("/api/v1/analysis/run", json=job_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "pending"

# Cleanup
def teardown_module():
    """Clean up test database."""
    if os.path.exists("./test.db"):
        os.remove("./test.db")