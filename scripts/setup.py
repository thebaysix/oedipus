#!/usr/bin/env python3
"""
Simple project setup helper.

- Installs Python dependencies from requirements.txt using the active Python interpreter
- Prints guidance for next steps (start infra, run alembic, etc.)

Intended to be run inside the project's virtual environment (see README).
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ_FILE = ROOT / "requirements.txt"


def in_venv():
    # sys.base_prefix is different from sys.prefix inside a venv
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def run(cmd, **kwargs):
    print(f">>> Running: {cmd}\n")
    try:
        subprocess.check_call(cmd, **kwargs)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return False


def install_requirements():
    if not REQ_FILE.exists():
        print(f"requirements.txt not found at {REQ_FILE}, skipping dependency installation.")
        return True

    # Upgrade pip first (recommended)
    if not run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"]):
        print("Failed to upgrade pip, continuing to try installing requirements.")

    cmd = [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)]
    return run(cmd)


def main():
    print("\nOedipus - setup helper\n")

    if not in_venv():
        print("WARNING: It looks like you are not running inside a virtual environment.")
        print("Please create and activate the venv named .venv-oed before running this script.")
        print("See README for exact commands.\n")
        sys.exit(1)

    success = install_requirements()

    if not success:
        print("\nOne or more setup steps failed. Please inspect the output above and try again.")
        sys.exit(1)

    print("\nSetup completed successfully (dependencies installed).\n")
    print("Next steps:")
    print("  1) Start required infrastructure: 'docker compose up -d' (Postgres + Redis)")
    print("  2) Initialize the database: 'alembic upgrade head' (requires DB to be running)")
    print("  3) Start services as described in the README (backend, worker, frontend)")
    print("\nIf you need to re-run dependency installation later, run: python scripts/setup.py")


if __name__ == '__main__':
    main()
