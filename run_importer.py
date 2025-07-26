#!/usr/bin/env python3
"""
Simple runner script for the Telegram to WordPress importer
This script can work without a virtual environment
"""

import sys
import os

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

def main():
    """Main function"""
    print("Telegram to WordPress Importer - Dependency Check")
    print("=" * 50)

    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return 1

    print("\n✓ All dependencies available!")
    print("\nStarting importer...")

    try:
        from telegram_importer import TelegramImporter

        # Parse command line arguments
        start_index = 0
        batch_size = None

        if len(sys.argv) > 1:
            try:
                start_index = int(sys.argv[1])
            except ValueError:
                print("Invalid start index. Using 0.")

        if len(sys.argv) > 2:
            try:
                batch_size = int(sys.argv[2])
            except ValueError:
                print("Invalid batch size. Using default.")

        # Run importer
        importer = TelegramImporter()
        next_index = importer.run(start_index, batch_size)

        if batch_size and batch_size > 0:
            print(f"\nTo continue, run: python3 run_importer.py {next_index} {batch_size}")

        return 0

    except Exception as e:
        print(f"Error running importer: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())