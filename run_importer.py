#!/usr/bin/env python3
"""
Simple runner script for the Telegram to WordPress importer
This script can work without a virtual environment
"""

import sys
import os
import subprocess

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []

    try:
        import requests
        print("✓ requests module available")
    except ImportError:
        missing_deps.append("requests")
        print("✗ requests module missing")

    try:
        import dateutil
        print("✓ python-dateutil module available")
    except ImportError:
        missing_deps.append("python-dateutil")
        print("✗ python-dateutil module missing")

    try:
        import PIL
        print("✓ Pillow module available")
    except ImportError:
        missing_deps.append("Pillow")
        print("✗ Pillow module missing")

    try:
        import dotenv
        print("✓ python-dotenv module available")
    except ImportError:
        missing_deps.append("python-dotenv")
        print("✗ python-dotenv module missing")

    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("\nTo install dependencies:")
        print("1. Create virtual environment: python3 -m venv venv")
        print("2. Activate it: source venv/bin/activate")
        print("3. Install: pip install -r requirements.txt")
        print("\nOr install directly: pip3 install --user " + " ".join(missing_deps))
        return False

    return True

def run_with_system_python():
    """Run the importer using system Python to avoid Chrome sandbox issues"""
    # Get the system Python path
    system_python = "/usr/bin/python3"

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the command to run the importer
    cmd = [system_python, os.path.join(script_dir, "telegram_importer.py")]

    # Add command line arguments
    cmd.extend(sys.argv[1:])

    # Run the command
    try:
        result = subprocess.run(cmd, cwd=script_dir, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running importer: {e}")
        return e.returncode
    except FileNotFoundError:
        print("System Python not found at /usr/bin/python3")
        return 1

def main():
    """Main function"""
    print("Telegram to WordPress Importer - Dependency Check")
    print("=" * 50)

    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return 1

    print("\n✓ All dependencies available!")
    print("\nStarting importer with system Python...")

    # Run with system Python to avoid Chrome sandbox issues
    return run_with_system_python()

if __name__ == "__main__":
    sys.exit(main())