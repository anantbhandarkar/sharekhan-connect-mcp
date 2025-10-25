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
    try:
        # Test help command
        result = subprocess.run(
            ["sharekhan-mcp", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 or "usage:" in result.stdout.lower() or "error" in result.stderr.lower():
            print("✓ CLI command available")
            return True
        else:
            print(f"✗ CLI command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ CLI command not found (sharekhan-mcp)")
        return False
    except subprocess.TimeoutExpired:
        print("✗ CLI command test timed out")
        return False
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
