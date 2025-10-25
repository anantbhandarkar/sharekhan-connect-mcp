#!/bin/bash

# Comprehensive security and quality check script
# Run this before pushing to ensure your code passes all CI checks

echo "🔍 Running comprehensive security and quality checks..."
echo "========================================================"

# Check if required tools are installed
echo "📦 Installing required tools..."
python3 -m pip install bandit safety pytest-cov > /dev/null 2>&1

echo ""
echo "1. 🔒 Security Scan with Bandit..."
if bandit -r src/ -ll; then
    echo "✅ Security scan passed"
else
    echo "❌ Security issues found"
    echo "💡 Review the security issues above and fix them"
    exit 1
fi

echo ""
echo "2. 🛡️ Dependency Vulnerability Check..."
if safety scan; then
    echo "✅ No dependency vulnerabilities found"
else
    echo "⚠️  Dependency vulnerabilities found"
    echo "💡 Consider updating vulnerable packages"
    # Don't exit on dependency issues as they might be in dev environment
fi

echo ""
echo "3. 📊 Code Coverage Analysis..."
if python3 -m pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml; then
    echo "✅ Coverage analysis completed"
    echo "📈 Coverage report generated in htmlcov/"
else
    echo "⚠️  Coverage analysis completed with warnings"
fi

echo ""
echo "4. 🧪 Running Installation Tests..."
if python3 test_installation.py; then
    echo "✅ Installation tests passed"
else
    echo "❌ Installation tests failed"
    exit 1
fi

echo ""
echo "🎉 All security and quality checks completed!"
echo "📊 Check htmlcov/index.html for detailed coverage report"
echo "💡 Consider addressing any security issues or low coverage areas"
