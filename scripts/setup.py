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

def install_dependencies():
    """Install Python dependencies with fallback for psycopg2 issues."""
    print("\n🔄 Installing Python dependencies...")
    
    # First try to install all dependencies
    try:
        result = subprocess.run("pip install -r requirements.txt", shell=True, check=True, capture_output=True, text=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        if "psycopg2" in e.stderr:
            print("⚠️  psycopg2-binary installation failed. Trying alternative approach...")
            
            # Try installing without psycopg2 first
            print("🔄 Installing other dependencies...")
            try:
                # Install everything except psycopg2
                subprocess.run("pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==1.4.48", shell=True, check=True)
                subprocess.run("pip install alembic==1.12.1 redis==5.0.1 celery==5.3.4 pydantic==1.10.13", shell=True, check=True)
                subprocess.run("pip install python-multipart==0.0.6 streamlit==1.28.1 plotly==5.17.0", shell=True, check=True)
                subprocess.run("pip install pandas==2.1.3 requests==2.31.0 numpy==1.25.2 scipy==1.11.4", shell=True, check=True)
                subprocess.run("pip install tiktoken==0.5.1 pytest==7.4.3 pytest-asyncio==0.21.1", shell=True, check=True)
                subprocess.run("pip install httpx==0.25.2 python-dotenv==1.0.0", shell=True, check=True)
                
                print("✅ Core dependencies installed successfully")
                
                # Now try different approaches for psycopg2
                print("🔄 Attempting to install psycopg2...")
                
                # Try different versions
                for version in ["2.9.7", "2.9.6", "2.9.5"]:
                    try:
                        subprocess.run(f"pip install psycopg2-binary=={version}", shell=True, check=True, capture_output=True)
                        print(f"✅ psycopg2-binary {version} installed successfully")
                        return True
                    except subprocess.CalledProcessError:
                        continue
                
                # If all versions fail, suggest manual installation
                print("⚠️  Could not install psycopg2-binary automatically.")
                print("📋 Please try one of these manual approaches:")
                print("1. Install PostgreSQL development libraries:")
                print("   - Download and install PostgreSQL from https://www.postgresql.org/download/windows/")
                print("   - Or use conda: conda install psycopg2")
                print("2. Use alternative database adapter:")
                print("   pip install asyncpg  # For async PostgreSQL")
                print("3. For development only, you can use SQLite temporarily")
                
                return False
                
            except subprocess.CalledProcessError as e2:
                print(f"❌ Failed to install core dependencies: {e2.stderr}")
                return False
        else:
            print(f"❌ Dependency installation failed: {e.stderr}")
            return False

def main():
    """Main setup function."""
    print("🚀 Setting up Oedipus MVP...")
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml not found in project root")
        sys.exit(1)
    
    # Install Python dependencies
    if not install_dependencies():
        print("⚠️  Some dependencies failed to install. Please check the messages above.")
        print("   You may need to install PostgreSQL or use alternative approaches.")
        return
    
    # Check if Docker is available
    print("\n🔄 Checking Docker availability...")
    try:
        subprocess.run("docker --version", shell=True, check=True, capture_output=True)
        print("✅ Docker is available")
        
        # Try docker-compose first, then docker compose
        docker_compose_cmd = None
        try:
            subprocess.run("docker-compose --version", shell=True, check=True, capture_output=True)
            docker_compose_cmd = "docker-compose up -d"
        except subprocess.CalledProcessError:
            try:
                subprocess.run("docker compose version", shell=True, check=True, capture_output=True)
                docker_compose_cmd = "docker compose up -d"
            except subprocess.CalledProcessError:
                pass
        
        if docker_compose_cmd:
            if not run_command(docker_compose_cmd, "Starting PostgreSQL and Redis"):
                print("⚠️  Failed to start Docker services. Please start manually:")
                print(f"   {docker_compose_cmd}")
                print("   Or check if Docker Desktop is running")
                return
        else:
            print("⚠️  Docker Compose not found. Please install Docker Desktop or Docker Compose")
            print("   Download from: https://www.docker.com/products/docker-desktop")
            return
            
    except subprocess.CalledProcessError:
        print("⚠️  Docker not found. Please install Docker Desktop:")
        print("   Download from: https://www.docker.com/products/docker-desktop")
        print("   After installation, you can run the services manually:")
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
    print("\n💡 Tip: You can also use the individual start scripts:")
    print("   python scripts/start_backend.py")
    print("   python scripts/start_worker.py")
    print("   python scripts/start_frontend.py")

if __name__ == "__main__":
    main()