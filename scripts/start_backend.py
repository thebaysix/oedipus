#!/usr/bin/env python3
"""
Start the backend API server
"""
import subprocess
import sys
import os

def main():
    """Start the FastAPI backend."""
    print("🚀 Starting Oedipus MVP Backend API...")
    
    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start the API server
        subprocess.run([
            "uvicorn", 
            "app.api.main:app", 
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Backend API stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()