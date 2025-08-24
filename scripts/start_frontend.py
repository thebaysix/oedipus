#!/usr/bin/env python3
"""
Start the Streamlit frontend
"""
import subprocess
import sys
import os

def main():
    """Start the Streamlit frontend."""
    print("🎨 Starting Oedipus MVP Frontend...")
    
    try:
        # Change to project root
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start Streamlit
        subprocess.run([
            "streamlit", 
            "run", 
            "frontend/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()