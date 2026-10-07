#!/usr/bin/env python3
"""Test runner script for library management system.

Provides convenient commands to run different test suites.
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd: list[str], description: str):
    """Run a command and print results.
    
    Args:
        cmd: Command to execute as list of strings
        description: Description of what's being run
    """
    print("=" * 70)
    print(f"Running: {description}")
    print("=" * 70)
    print(f"Command: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    if result.returncode == 0:
        print(f"\n[SUCCESS] {description} completed successfully!")
    else:
        print(f"\n[FAILED] {description} failed with exit code {result.returncode}")
    
    print()
    return result.returncode


def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("Library Management System - Test Runner")
        print("="*70)
        print("\nUsage: python tests/run_tests.py <command>")
        print("\nAvailable commands:")
        print("  all              - Run all tests")
        print("  router           - Run router unit tests only")
        print("  service          - Run service unit tests only")
        print("  unit             - Run all unit tests")
        print("  coverage         - Run tests with coverage report")
        print("  coverage-html    - Run tests with HTML coverage report")
        print("  router-verbose   - Run router tests with verbose output")
        print("\nExamples:")
        print("  python tests/run_tests.py all")
        print("  python tests/run_tests.py router")
        print("  python tests/run_tests.py coverage-html")
        print()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    commands = {
        "all": {
            "cmd": ["pytest", "tests/", "-v"],
            "desc": "All Tests"
        },
        "router": {
            "cmd": ["pytest", "tests/unit/routers/", "-v"],
            "desc": "Router Unit Tests"
        },
        "service": {
            "cmd": ["pytest", "tests/unit/services/", "-v"],
            "desc": "Service Unit Tests"
        },
        "unit": {
            "cmd": ["pytest", "tests/unit/", "-v"],
            "desc": "All Unit Tests"
        },
        "coverage": {
            "cmd": ["pytest", "tests/", "--cov=app", "--cov-report=term-missing"],
            "desc": "Tests with Coverage Report"
        },
        "coverage-html": {
            "cmd": ["pytest", "tests/", "--cov=app", "--cov-report=html", "--cov-report=term"],
            "desc": "Tests with HTML Coverage Report"
        },
        "router-verbose": {
            "cmd": ["pytest", "tests/unit/routers/test_book_router.py", "-vv", "-s"],
            "desc": "Router Tests (Extra Verbose)"
        }
    }
    
    if command not in commands:
        print(f"[ERROR] Unknown command: {command}")
        print(f"\nAvailable commands: {', '.join(commands.keys())}")
        sys.exit(1)
    
    cmd_info = commands[command]
    exit_code = run_command(cmd_info["cmd"], cmd_info["desc"])
    
    if command == "coverage-html" and exit_code == 0:
        print("[INFO] HTML coverage report generated at: htmlcov/index.html")
        print("       Open it in a browser to view detailed coverage.")
        print()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
