#!/usr/bin/env python3
"""
Setup script for Oedipus MVP
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Oedipus MVP...")
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Start Docker services
    if not run_command("docker-compose up -d", "Starting PostgreSQL and Redis"):
        print("⚠️  Failed to start Docker services. Please start manually:")
        print("   docker-compose up -d")
        return
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    import time
    time.sleep(10)
    
    # Initialize database
    if not run_command("alembic upgrade head", "Initializing database"):
        print("⚠️  Database initialization failed. You may need to run manually:")
        print("   alembic upgrade head")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Start the backend API:")
    print("   uvicorn app.api.main:app --reload")
    print("\n2. Start the Celery worker (in another terminal):")
    print("   celery -A app.workers.analysis_worker worker --loglevel=info")
    print("\n3. Start the frontend (in another terminal):")
    print("   streamlit run frontend/streamlit_app.py")
    print("\n4. Open your browser to:")
    print("   Frontend: http://localhost:8501")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()