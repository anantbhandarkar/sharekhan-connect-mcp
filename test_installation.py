#!/usr/bin/env python3
"""
Test that sharekhan-connect-mcp is properly installed
"""

import sys
import subprocess
import importlib.util

def test_import():
    """Test that the package can be imported"""
    try:
        import sys
        sys.path.insert(0, 'src')
        import sharekhan_connect_mcp
        print(f"✓ Package imported successfully (v{sharekhan_connect_mcp.__version__})")
        return True
    except ImportError as e:
        print(f"✗ Failed to import package: {e}")
        return False

def test_entry_point():
    """Test that the CLI entry point exists"""
    try:
        # Test if the entry point is available
        result = subprocess.run(
            ["python3", "-c", "import sys; sys.path.insert(0, 'src'); from sharekhan_connect_mcp.server import main; print('Entry point available')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ CLI entry point available")
            return True
        else:
            print(f"✗ CLI entry point failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ CLI entry point test timed out")
        return False
    except Exception as e:
        print(f"✗ CLI entry point test failed: {e}")
        return False

def test_components():
    """Test that main components can be imported"""
    components = [
        "sharekhan_connect_mcp.client",
        "sharekhan_connect_mcp.server", 
        "sharekhan_connect_mcp.tools",
        "sharekhan_connect_mcp.session",
        "sharekhan_connect_mcp.websocket",
        "sharekhan_connect_mcp.config",
        "sharekhan_connect_mcp.logger"
    ]
    
    all_imported = True
    import sys
    sys.path.insert(0, 'src')
    for component in components:
        try:
            importlib.import_module(component)
            print(f"✓ {component} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {component}: {e}")
            all_imported = False
    
    return all_imported

def test_cli_command():
    """Test that the CLI command works"""
    import os
    import tempfile
    try:
        # Test help command using Python module invocation (works in CI)
        # Set mock environment variables to allow Settings() to work
        env = {
            'SHAREKHAN_API_KEY': 'test_key',
            'SHAREKHAN_SECRET_KEY': 'test_secret',
            'SHAREKHAN_CUSTOMER_ID': '12345'
        }

        # Create a test script to verify CLI works
        test_script = '''
import os
os.environ["SHAREKHAN_API_KEY"] = "test_key"
os.environ["SHAREKHAN_SECRET_KEY"] = "test_secret"
os.environ["SHAREKHAN_CUSTOMER_ID"] = "12345"

import sys
sys.path.insert(0, "src")
from sharekhan_connect_mcp.server import main

# Test that main() can be called without crashing
try:
    # Simulate sys.argv = ["script", "--help"]
    original_argv = sys.argv
    sys.argv = ["test_script", "--help"]
    main()
except SystemExit as e:
    # --help causes sys.exit(0), which is expected
    if e.code == 0:
        print("CLI help test passed")
        sys.exit(0)
    else:
        print(f"CLI failed with exit code: {e.code}")
        sys.exit(1)
finally:
    sys.argv = original_argv
'''

        # Write test script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_script)
            test_file = f.name

        try:
            result = subprocess.run(
                ["python3", test_file],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=".",
                env={**os.environ, **env}
            )
            if result.returncode == 0 and "CLI help test passed" in result.stdout:
                print("✓ CLI command available (help test passed)")
                return True
            else:
                print(f"✗ CLI command failed: {result.stderr}")
                return False
        finally:
            os.unlink(test_file)

    except Exception as e:
        print(f"✗ CLI command test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing sharekhan-connect-mcp installation...")
    print("=" * 50)
    
    tests = [
        ("Package Import", test_import),
        ("Component Imports", test_components),
        ("Entry Point", test_entry_point),
        ("CLI Command", test_cli_command)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
