#!/bin/bash
# Comprehensive pre-commit quality gate
# This script runs ALL checks that will run in CI

set -e  # Exit on first error

echo "🚀 Running Pre-Commit Quality Checks"
echo "===================================="

# 1. Type checking with mypy
echo ""
echo "1. 🔍 Type Checking with MyPy..."
if ! python3 -m mypy src/ --pretty; then
    echo "❌ MyPy type checking failed"
    echo "💡 Fix type hints in the files listed above"
    exit 1
fi
echo "✅ MyPy type checking passed"

# 2. Code formatting with Black
echo ""
echo "2. 🎨 Checking Code Formatting (Black)..."
if ! black --check --diff src/; then
    echo "❌ Black formatting check failed"
    echo "💡 Run 'black src/' to fix formatting"
    exit 1
fi
echo "✅ Black formatting passed"

# 3. Import sorting with isort
echo ""
echo "3. 📚 Checking Import Sorting (isort)..."
if ! isort --check-only --diff src/; then
    echo "❌ Import sorting check failed"
    echo "💡 Run 'isort src/' to fix imports"
    exit 1
fi
echo "✅ Import sorting passed"

# 4. Linting with flake8
echo ""
echo "4. 🔎 Linting Code (flake8)..."
if ! flake8 src/ --count --max-line-length=88 --extend-ignore=E203,W503 --show-source --statistics; then
    echo "❌ Flake8 linting failed"
    echo "💡 Fix linting issues listed above"
    exit 1
fi
echo "✅ Flake8 linting passed"

# 5. Run tests
echo ""
echo "5. 🧪 Running Tests..."
if ! python3 -m pytest tests/ -v; then
    echo "❌ Tests failed"
    echo "💡 Fix failing tests before committing"
    exit 1
fi
echo "✅ All tests passed"

# 6. Security scan (non-blocking)
echo ""
echo "6. 🔒 Running Security Scan (Bandit)..."
if command -v bandit &> /dev/null; then
    bandit -r src/ -ll || echo "⚠️  Security issues found (review recommended)"
else
    echo "ℹ️  Bandit not installed, skipping"
fi

echo ""
echo "🎉 All pre-commit checks passed!"
echo "✅ Your code is ready to be committed and pushed"
