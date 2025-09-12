#!/usr/bin/env python3
"""
Start the backend API server
"""
import subprocess
import sys
import os
import socket
import time


def is_port_free(host: str, port: int) -> bool:
    """Return True if the given host:port can be bound to (i.e. currently free).

    We attempt to bind a temporary socket to detect if another process is already
    listening on the port. Binding to 0.0.0.0 will fail if any process is
    listening on the port on any interface.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def wait_for_service(host: str, port: int, timeout: int = 60) -> bool:
    """Wait until a TCP service at host:port accepts connections or timeout.

    Returns True if the service became available within the timeout period,
    False otherwise. Prints progress (elapsed/timeout) while waiting.
    """
    start = time.time()
    end = start + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"\n{host}:{port} is available")
                return True
        except OSError:
            elapsed = int(time.time() - start)
            print(f"Waiting for {host}:{port} — {elapsed}s/{timeout}s", end="\r")
            time.sleep(1)
    return False


def main():
    """Start the FastAPI backend."""
    print("🚀 Starting Oedipus MVP Backend API...")

    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))

        # If running local dev, wait for DB and Redis to be reachable before starting
        db_host = os.environ.get("POSTGRES_HOST", "localhost")
        db_port = int(os.environ.get("POSTGRES_PORT", "5432"))
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", "6379"))

        # Helpful reminder for common developer flow
        if db_host in ("localhost", "127.0.0.1"):
            print("Reminder: did you run 'docker compose up -d postgres redis' ?")

        print(f"Checking database at {db_host}:{db_port}...")
        if not wait_for_service(db_host, db_port, timeout=60):
            print("\n❌ Database did not become available within 60s. Check 'docker compose logs postgres' and verify the service is healthy.")
            print("Reminder: run 'docker compose up -d postgres redis' if you haven't already.")
            sys.exit(1)

        print(f"Checking Redis at {redis_host}:{redis_port}...")
        if not wait_for_service(redis_host, redis_port, timeout=60):
            print("\n❌ Redis did not become available within 60s. Check 'docker compose logs redis' and verify the service is healthy.")
            sys.exit(1)

        # Optionally run database migrations automatically on startup
        migrate_flag = os.environ.get("MIGRATE_ON_START", "0").lower()
        if migrate_flag in ("1", "true", "yes"):
            print("Running database migrations (alembic upgrade head) as MIGRATE_ON_START is enabled...")
            try:
                subprocess.run(["alembic", "upgrade", "head"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ alembic migration failed: {e}")
                sys.exit(1)

        # Check port availability before attempting to start uvicorn
        host = "0.0.0.0"
        port = 8000
        if not is_port_free(host, port):
            print("❌ Port 8000 is already in use.")
            print("If you started services with Docker, that likely started the backend container which binds port 8000.")
            print("Options to resolve:")
            print("  * Stop the backend container: `docker compose stop backend` (or `docker compose down`) ")
            print("  * Run the backend on a different port by modifying this script or running uvicorn with a different --port")
            print("  * Kill the docker-proxy processes (not recommended because Docker may recreate them)")
            sys.exit(1)

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