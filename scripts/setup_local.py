#!/usr/bin/env python3
"""
Local setup script for Oedipus MVP (Postgres-only, no Docker)
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:\n{e}")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("\n🔄 Installing Python dependencies...")
    try:
        subprocess.run("pip install -r requirements.txt", shell=True, check=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed:\n{e}")
        return False

def check_postgres_connection():
    """Check if local Postgres is accessible."""
    import psycopg2
    from psycopg2 import OperationalError

    POSTGRES_USER = os.getenv("POSTGRES_USER", "oedipus")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "oedipus_password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "oedipus")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.close()
        print(f"✅ Connected to Postgres at {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
        return True
    except OperationalError as e:
        print(f"❌ Could not connect to Postgres:\n{e}")
        return False

def main():
    print("🚀 Setting up Oedipus MVP (local Postgres-only)...")

    # Check requirements.txt
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Run this script from the project root.")
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("⚠️  Failed to install dependencies.")
        return

    # Check Postgres connection
    if not check_postgres_connection():
        print("⚠️  Please start your local Postgres and ensure credentials match your .env file.")
        return

    # Run Alembic migrations
    if not run_command("alembic upgrade head", "Initializing database"):
        print("⚠️  Database initialization failed. Run manually: alembic upgrade head")
        return

    print("\n🎉 Local setup complete!")
    print("\n📋 Next steps:")
    print("1. Start backend API:")
    print("   uvicorn app.api.main:app --reload")
    print("2. Start frontend:")
    print("   streamlit run frontend/streamlit_app.py")
    print("3. (Optional) Run Celery tasks if you have Redis available:")
    print("   python -m celery -A app.workers.analysis_worker worker --loglevel=info --pool=solo")

if __name__ == "__main__":
    main()
