#!/usr/bin/env python3
"""
Setup script for Oedipus MVP with dynamic Docker service checks
and proper timeout handling
"""
import subprocess
import sys
from pathlib import Path
import time
import yaml

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:\n{e.stderr}")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("\n🔄 Installing Python dependencies...")
    try:
        subprocess.run("pip install -r requirements.txt", shell=True, check=True, capture_output=True, text=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed:\n{e.stderr}")
        return False

def check_docker():
    """Check Docker installation and Compose availability."""
    try:
        subprocess.run("docker --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("\n❌ Docker not found. Please install Docker Desktop:")
        print("   https://www.docker.com/products/docker-desktop")
        print("   Ensure Docker is running and added to your PATH.")
        return None

    compose_cmd = None
    try:
        subprocess.run("docker compose version", shell=True, check=True, capture_output=True)
        compose_cmd = "docker compose up -d"
    except subprocess.CalledProcessError:
        try:
            subprocess.run("docker-compose --version", shell=True, check=True, capture_output=True)
            compose_cmd = "docker-compose up -d"
        except subprocess.CalledProcessError:
            print("\n❌ Docker Compose not found. Please install or update Docker Desktop.")
            return None

    return compose_cmd

def get_services_from_compose(file_path="docker-compose.yml"):
    """Read services from docker-compose.yml"""
    if not Path(file_path).exists():
        print(f"❌ {file_path} not found.")
        return []

    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return list(data.get("services", {}).keys())

def wait_for_container(service_name, timeout=120):
    """Wait until a Docker container for the given service is healthy."""
    print(f"\n⏳ Waiting for container '{service_name}' to be ready...")
    start_time = time.time()
    while True:
        try:
            # Find the first container name matching the service
            output = subprocess.run(
                f'docker ps --filter "name={service_name}" --format "{{{{.Names}}}}"',
                shell=True, check=True, capture_output=True, text=True
            ).stdout.strip()
            if not output:
                raise ValueError("Container not found yet")
            container_name = output.splitlines()[0]

            # Check container health
            health = subprocess.run(
                f'docker inspect -f "{{{{.State.Health.Status}}}}" {container_name}',
                shell=True, check=True, capture_output=True, text=True
            ).stdout.strip()

            if health == "healthy":
                print(f"✅ Container '{container_name}' is healthy")
                return True
        except Exception:
            pass

        if time.time() - start_time > timeout:
            print(f"⚠️ Timeout waiting for container '{service_name}'")
            return False
        time.sleep(2)

def main():
    print("🚀 Setting up Oedipus MVP...")

    if not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml not found in project root")
        sys.exit(1)

    # Install Python dependencies
    if not install_dependencies():
        print("⚠️  Some dependencies failed to install. Please check the messages above.")
        return

    # Check Docker
    compose_cmd = check_docker()
    if not compose_cmd:
        print("⚠️  Cannot proceed without Docker. Setup terminated.")
        return

    # Start Docker services
    if not run_command(compose_cmd, "Starting Docker services"):
        print(f"⚠️  Failed to start Docker services. Please start manually using:\n   {compose_cmd}")
        return

    # Detect services from docker-compose.yml
    services = get_services_from_compose()
    if not services:
        print("⚠️  No services detected. Skipping container readiness checks.")
        all_healthy = False
    else:
        # Wait for each service container to be healthy
        all_healthy = True
        for service in services:
            healthy = wait_for_container(service)
            if not healthy:
                all_healthy = False

    if not all_healthy:
        print("\n⚠️  One or more containers failed to become healthy. Setup may not be complete.")
        return  # Stop the script before running Alembic

    # Initialize database
    if not run_command("alembic upgrade head", "Initializing database"):
        print("⚠️  Database initialization failed. You may need to run manually:\n   alembic upgrade head")
        return

    # Final instructions
    print("\n🎉 Setup completed!\n")
    print("📋 Next steps:")
    print("1. Start the backend API:\n   uvicorn app.api.main:app --reload")
    print("2. Start the Celery worker (in another terminal):\n   celery -A app.workers.analysis_worker worker --loglevel=info --pool=solo")
    print("3. Start the frontend (in another terminal):\n   streamlit run frontend/streamlit_app.py")
    print("4. Open your browser to:\n   Frontend: http://localhost:8501\n   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
