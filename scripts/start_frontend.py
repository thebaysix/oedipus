#!/usr/bin/env python3
"""
Start the React frontend (Vite)
"""
import subprocess
import sys
import os

def main():
    """Start the React frontend (Vite dev server)."""
    print("🎨 Starting Oedipus React Frontend...")
    
    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start React dev server
        subprocess.run([
            "npm",
            "run",
            "dev",
        ], check=True, cwd=os.path.join(os.getcwd(), "react-frontend"))
        
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()