#!/bin/bash

# Basic quality check script
set -e

echo "🚀 Running quality checks..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# 1. Type checking
echo "🔍 Running type checking with mypy..."
if mypy src/ --config-file=pyproject.toml; then
    echo "✅ Type checking passed"
else
    echo "❌ Type checking failed"
    exit 1
fi

# 2. Code formatting
echo "🔍 Checking code formatting with black..."
if black --check --diff src/ > /dev/null 2>&1; then
    echo "✅ Code formatting is correct"
else
    echo "⚠️ Code formatting issues found. Run 'black src/' to fix."
fi

# 3. Import sorting
echo "🔍 Checking import sorting with isort..."
if isort --check-only --diff src/ > /dev/null 2>&1; then
    echo "✅ Import sorting is correct"
else
    echo "⚠️ Import sorting issues found. Run 'isort src/' to fix."
fi

# 4. Linting
echo "🔍 Running linting with flake8..."
if flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics > /dev/null 2>&1; then
    echo "✅ Linting passed"
else
    echo "⚠️ Linting issues found"
fi

# 5. Security
echo "🔍 Running security scan with bandit..."
if bandit -r src/ > /dev/null 2>&1; then
    echo "✅ Security scan passed"
else
    echo "⚠️ Security issues found"
fi

echo ""
echo "🎉 Quality checks completed!"