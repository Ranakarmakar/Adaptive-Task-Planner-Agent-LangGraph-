#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Runner Script

Simple script to launch the Streamlit demo UI for the Adaptive Task Planner Agent.
"""

import subprocess
import sys
import os


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        from agent import create_initial_state
        print("✓ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False


def main():
    """Main function to run the Streamlit demo."""
    print("Adaptive Task Planner Agent - Streamlit Demo")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run Streamlit app
    print("Starting Streamlit demo...")
    print("The demo will open in your default web browser")
    print("Press Ctrl+C to stop the demo")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\nDemo stopped. Thanks for trying the Adaptive Task Planner Agent!")
    except Exception as e:
        print(f"Error running demo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()