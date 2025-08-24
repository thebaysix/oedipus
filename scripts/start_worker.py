#!/usr/bin/env python3
"""
Start the Celery worker
"""
import subprocess
import sys
import os

def main():
    """Start the Celery worker."""
    print("🔄 Starting Oedipus MVP Celery Worker...")
    
    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start the worker
        subprocess.run([
            "celery", 
            "-A", "app.workers.analysis_worker",
            "worker",
            "--loglevel=info",
            "--concurrency=2"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Celery worker stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start worker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()