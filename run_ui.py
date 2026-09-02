"""1-Click Launcher for Streamlit RAG Document Assistant."""

import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🚀 Launching RAG Document Assistant (Streamlit UI)...")
    print("=" * 60)

    # Determine project root and app.py path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_dir, "app.py")

    # Prefer virtual environment streamlit/python if present
    venv_streamlit = os.path.join(project_dir, "venv", "Scripts", "streamlit.exe")
    venv_python = os.path.join(project_dir, "venv", "Scripts", "python.exe")

    if os.path.exists(venv_streamlit):
        cmd = [venv_streamlit, "run", app_path]
    elif os.path.exists(venv_python):
        cmd = [venv_python, "-m", "streamlit", "run", app_path]
    else:
        cmd = [sys.executable, "-m", "streamlit", "run", app_path]

    print(f"Running command: {' '.join(cmd)}")
    print("Opening browser at: http://localhost:8501\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user.")

if __name__ == "__main__":
    main()
