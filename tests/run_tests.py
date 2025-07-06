#!/usr/bin/env python3
"""
CeWLio Test Runner
Runs all tests or individual tests based on command line arguments.
"""

import sys
import os
import subprocess
from pathlib import Path

# Available test classes
TEST_CLASSES = {
    "cewlio": "Core CeWLio functionality tests",
    "extract_html": "HTML extraction tests", 
    "process_url": "URL processing tests",
    "integration": "Integration tests",
    "edge_cases": "Edge case tests"
}

def run_test_class(test_class):
    """Run a single test class."""
    print(f"\n🚀 Running test class: {test_class}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, "run_tests.py", "--class", test_class], 
                              capture_output=False, 
                              timeout=300)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Test timed out: {test_class}")
        return False
    except Exception as e:
        print(f"❌ Error running test class {test_class}: {e}")
        return False

def run_all_tests():
    """Run all available tests."""
    print("🧪 CeWLio Test Suite")
    print("=" * 60)
    print(f"Running {len(TEST_CLASSES)} test classes...")
    
    results = {}
    passed = 0
    failed = 0
    
    for test_class in TEST_CLASSES.keys():
        success = run_test_class(test_class)
        results[test_class] = success
        
        if success:
            passed += 1
            print(f"✅ {test_class}: PASSED")
        else:
            failed += 1
            print(f"❌ {test_class}: FAILED")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total test classes: {len(TEST_CLASSES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 All test classes passed!")
        return True
    else:
        print("💥 Some test classes failed!")
        return False

def show_help():
    """Show help information."""
    print("CeWLio Test Runner")
    print("=" * 30)
    print("Usage:")
    print("  python run_tests.py                    # Run all test classes")
    print("  python run_tests.py <test_class>       # Run specific test class")
    print("  python run_tests.py --help             # Show this help")
    print("\nAvailable test classes:")
    for test_class, description in TEST_CLASSES.items():
        print(f"  {test_class} - {description}")
    print("\nExamples:")
    print("  python run_tests.py cewlio")
    print("  python run_tests.py integration")
    print("  python run_tests.py cewlio edge_cases")

def main():
    if len(sys.argv) == 1:
        # No arguments, run all tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
    
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["--help", "-h", "help"]:
            show_help()
            sys.exit(0)
        
        test_class = sys.argv[1]
        if test_class in TEST_CLASSES:
            # Run specific test class
            success = run_test_class(test_class)
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Unknown test class: {test_class}")
            print("Available test classes:")
            for name in TEST_CLASSES.keys():
                print(f"  {name}")
            sys.exit(1)
    
    else:
        # Multiple arguments, run multiple specific test classes
        test_classes = sys.argv[1:]
        unknown_classes = [name for name in test_classes if name not in TEST_CLASSES]
        
        if unknown_classes:
            print(f"❌ Unknown test classes: {unknown_classes}")
            print("Available test classes:")
            for name in TEST_CLASSES.keys():
                print(f"  {name}")
            sys.exit(1)
        
        print("🧪 CeWLio Test Suite (Selected Test Classes)")
        print("=" * 60)
        
        results = {}
        passed = 0
        failed = 0
        
        for test_class in test_classes:
            success = run_test_class(test_class)
            results[test_class] = success
            
            if success:
                passed += 1
                print(f"✅ {test_class}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_class}: FAILED")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total test classes: {len(test_classes)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed == 0:
            print("🎉 All selected test classes passed!")
            sys.exit(0)
        else:
            print("💥 Some test classes failed!")
            sys.exit(1)

if __name__ == "__main__":
    main() 