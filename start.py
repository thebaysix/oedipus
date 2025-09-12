#!/usr/bin/env python3
"""
Simple startup script for Oedipus MVP
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_docker():
    """Check if Docker is available."""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_services():
    """Check if required services are running."""
    try:
        # Check if PostgreSQL is accessible
        subprocess.run(["docker", "ps"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_services():
    """Start Docker services."""
    print("🐳 Starting Docker services...")
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Docker services started")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Docker services: {e}")
        return False

def check_api():
    """Check if API is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main startup function."""
    print("🚀 Starting Oedipus MVP...")
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not available. Please install Docker first.")
        sys.exit(1)
    
    # Start services
    if not start_services():
        print("❌ Failed to start services")
        sys.exit(1)
    
    # Wait for services
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Initialize database:")
    print("   alembic upgrade head")
    print("\n3. Start the application:")
    print("   # Terminal 1:")
    print("   uvicorn app.api.main:app --reload")
    print("   # Terminal 2:")
    print("   celery -A app.workers.analysis_worker worker --loglevel=info")
    print("   # Terminal 3:")
    print("   cd react-frontend && npm run dev")
    print("\n4. Open your browser:")
    print("   Frontend: http://localhost:3000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()