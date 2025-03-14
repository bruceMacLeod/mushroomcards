#!/usr/bin/env python3
"""
Simple test runner for the mushroom flashcards backend.
This script runs tests without pytest dependencies.
"""
import sys
import importlib.util
import traceback


def run_test_file(file_path):
    """Run tests in a Python file without pytest."""
    print(f"\n=== Running tests in {file_path} ===\n")
    
    # Import the module
    spec = importlib.util.spec_from_file_location("test_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find all test functions
    test_functions = [name for name in dir(module) if name.startswith("test_")]
    
    if not test_functions:
        print("No test functions found!")
        return 0, 0
    
    # Run the tests
    pass_count = 0
    fail_count = 0
    
    for func_name in test_functions:
        func = getattr(module, func_name)
        if callable(func):
            print(f"Running {func_name}... ", end="")
            try:
                func()
                print("PASS")
                pass_count += 1
            except Exception as e:
                print("FAIL")
                print(f"  Error: {str(e)}")
                traceback.print_exc()
                fail_count += 1
    
    return pass_count, fail_count


def main():
    """Run all simple tests."""
    # Files to test
    test_files = [
        "tests/test_simple.py",
        "tests/test_api_mock.py",
        "tests/test_models_simple.py",
        "tests/test_services_simple.py",
    ]
    
    total_pass = 0
    total_fail = 0
    
    for file_path in test_files:
        passes, fails = run_test_file(file_path)
        total_pass += passes
        total_fail += fails
    
    print("\n=== Test Summary ===")
    print(f"Passed: {total_pass}")
    print(f"Failed: {total_fail}")
    print(f"Total:  {total_pass + total_fail}")
    
    if total_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()