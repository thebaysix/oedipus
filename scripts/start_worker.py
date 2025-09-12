#!/usr/bin/env python3
"""
Start the Celery worker
"""
import subprocess
import sys
import os


def in_virtualenv() -> bool:
    """Return True if running inside a virtual environment or conda env.

    Checks common indicators: VIRTUAL_ENV or CONDA_PREFIX env vars, and
    compares sys.prefix vs sys.base_prefix (the standard venv detection).
    """
    if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_PREFIX"):
        return True
    base_prefix = getattr(sys, "base_prefix", None)
    if base_prefix and sys.prefix != base_prefix:
        return True
    # Older virtualenvs set real_prefix
    if getattr(sys, "real_prefix", None):
        return True
    return False


def main():
    """Start the Celery worker."""
    print("🔄 Starting Oedipus MVP Celery Worker...")

    # Ensure we are running inside a virtual environment so the correct
    # Celery executable / package is available.
    if not in_virtualenv():
        print(
            "⚠️  No virtual environment detected. Activate your project's virtualenv before running this script.\n\n"
            "Ubuntu / macOS (bash): source .venv-oed/bin/activate\n"
            "Windows (PowerShell): .\\.venv-oed\\Scripts\\Activate.ps1\n"
            "Windows (cmd.exe): .\\.venv-oed\\Scripts\\activate.bat"
        )
        sys.exit(2)
    
    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start the worker using the current Python interpreter to run Celery as a module
        subprocess.run([
            sys.executable,
            "-m",
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