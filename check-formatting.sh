#!/bin/bash

# Pre-commit formatting check script
# Run this before pushing to ensure your code passes CI formatting checks

echo "🔍 Running pre-commit formatting checks..."
echo "================================================"

# Check if Black is installed
if ! command -v black &> /dev/null; then
    echo "❌ Black is not installed. Installing..."
    python3 -m pip install black
fi

# Check if isort is installed
if ! command -v isort &> /dev/null; then
    echo "❌ isort is not installed. Installing..."
    python3 -m pip install isort
fi

echo ""
echo "1. Checking code formatting with Black..."
if black --check --diff src/; then
    echo "✅ Black formatting check passed"
else
    echo "❌ Black formatting check failed"
    echo "💡 Run 'black src/' to fix formatting issues"
    exit 1
fi

echo ""
echo "2. Checking import sorting with isort..."
if python3 -m isort --check-only --diff src/; then
    echo "✅ Import sorting check passed"
else
    echo "❌ Import sorting check failed"
    echo "💡 Run 'python3 -m isort src/' to fix import sorting"
    exit 1
fi

echo ""
echo "3. Running quick linting check..."
if command -v flake8 &> /dev/null; then
    if flake8 src/ --max-line-length=88 --extend-ignore=E203,W503 --count --statistics; then
        echo "✅ Linting check passed"
    else
        echo "⚠️  Linting issues found (non-blocking)"
    fi
else
    echo "ℹ️  flake8 not installed, skipping linting check"
fi

echo ""
echo "🎉 All formatting checks passed! Your code is ready for CI."
echo "💡 Consider using 'pre-commit install' to run these checks automatically on commit."
