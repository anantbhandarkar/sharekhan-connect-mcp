# Development Guide

This document outlines the development practices and tooling used in the Sharekhan MCP project.

## 🛠️ Development Workflow

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/anantbhandarkar/sharekhan-connect-mcp.git
cd sharekhan-connect-mcp

# Install development dependencies
pip install -e ".[dev,quality,security,test]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Quality Tools

The project includes several quality tools:

#### Code Quality
- **mypy**: Static type checking
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **radon**: Code complexity analysis
- **xenon**: Maintainability index
- **pydocstyle**: Documentation quality

#### Security
- **bandit**: Security vulnerability scanning
- **detect-secrets**: Secrets detection
- **pip-audit**: Dependency vulnerability scanning
- **pip-licenses**: License validation

#### Testing
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-benchmark**: Performance testing

### Running Quality Checks

```bash
# Run all quality checks
./scripts/quality-check.sh

# Individual checks
mypy src/
black --check src/
isort --check src/
flake8 src/
radon cc src/
bandit -r src/
```

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Run quality checks locally
./scripts/quality-check.sh

# Commit changes
git add .
git commit -m "feat: add your feature"
```

## 📊 Quality Metrics

### Code Quality Targets

| Metric | Target | Tool |
|--------|--------|------|
| Type Coverage | 100% | mypy |
| Code Complexity | ≤ B | radon |
| Maintainability | A | xenon |
| Documentation | Google style | pydocstyle |
| Security Score | A | bandit |

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run benchmarks
pytest --benchmark-only
```

## 🚀 Continuous Integration

The CI pipeline includes:

1. **Type checking** with mypy
2. **Code quality analysis** with radon, xenon, pydocstyle
3. **Security analysis** with bandit, detect-secrets
4. **Code formatting** with black, isort
5. **Testing** with pytest
6. **Package validation**

## 📞 Getting Help

If you encounter issues with the quality tools:

1. Check the tool documentation
2. Run tools locally first to debug issues
3. Check the CI logs for detailed error messages
4. Ask questions in GitHub Issues

Remember: Quality tools are here to help maintain code quality!