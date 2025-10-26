#!/usr/bin/env python3
"""
Startup script to run both backend and frontend servers
"""
import subprocess
import time
import sys
import os
import signal
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def print_colored(message, color=Colors.NC):
    print(f"{color}{message}{Colors.NC}")

def check_ollama():
    """Check if Ollama is installed and model is available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'llama3.2:1b' not in result.stdout:
            print_colored("📥 Pulling llama3.2:1b model...", Colors.BLUE)
            subprocess.run(['ollama', 'pull', 'llama3.2:1b'])
        return True
    except FileNotFoundError:
        print_colored("❌ Ollama is not installed. Please install from https://ollama.ai", Colors.RED)
        return False

def check_api_key():
    """Check if API key file exists"""
    if not Path("API_Key.txt").exists():
        print_colored("⚠️  Warning: API_Key.txt not found. Gemini API features may not work.", Colors.YELLOW)
        print_colored("   Create API_Key.txt with your Google Gemini API key\n", Colors.YELLOW)

def install_backend_deps():
    """Install Python backend dependencies"""
    try:
        import flask
    except ImportError:
        print_colored("📦 Installing Python dependencies...", Colors.BLUE)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'])

def install_frontend_deps():
    """Install frontend dependencies if needed"""
    frontend_path = Path("BOM to Order/frontend")
    if not (frontend_path / "node_modules").exists():
        print_colored("📦 Installing frontend dependencies...", Colors.BLUE)
        subprocess.run(['pnpm', 'install'], cwd=str(frontend_path))

def start_servers():
    """Start both backend and frontend servers"""
    processes = []
    
    # Start backend
    print_colored("🐍 Starting Backend Server (Flask)...", Colors.GREEN)
    backend_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd='backend',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(backend_process)
    
    # Wait for backend to start
    time.sleep(3)
    
    # Check if backend is running
    try:
        import urllib.request
        urllib.request.urlopen('http://localhost:5000/health')
        print_colored("✅ Backend running on http://localhost:5000\n", Colors.GREEN)
    except:
        print_colored("❌ Failed to start backend", Colors.RED)
        backend_process.kill()
        sys.exit(1)
    
    # Start frontend
    print_colored("⚛️  Starting Frontend Server (Vite)...", Colors.GREEN)
    frontend_process = subprocess.Popen(
        ['pnpm', 'dev'],
        cwd='BOM to Order/frontend'
    )
    processes.append(frontend_process)
    
    time.sleep(2)
    
    print_colored("\n✅ Both servers are running!", Colors.GREEN)
    print_colored("Frontend: http://localhost:5173", Colors.BLUE)
    print_colored("Backend:  http://localhost:5000", Colors.BLUE)
    print_colored("\nPress Ctrl+C to stop all servers\n", Colors.GREEN)
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print_colored("\n🛑 Stopping servers...", Colors.RED)
        for process in processes:
            process.kill()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for processes
    for process in processes:
        process.wait()

if __name__ == "__main__":
    print_colored("🚀 Starting BOM to Order Application\n", Colors.BLUE)
    
    # Run checks
    if not check_ollama():
        sys.exit(1)
    
    check_api_key()
    install_backend_deps()
    install_frontend_deps()
    
    # Start servers
    start_servers()
