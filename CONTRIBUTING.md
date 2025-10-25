# Contributing to Sharekhan Connect MCP

Thank you for your interest in contributing to Sharekhan Connect MCP! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Sharekhan API credentials (for testing)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sharekhan-connect-mcp.git
   cd sharekhan-connect-mcp
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/sharekhan-mcp/sharekhan-connect-mcp.git
   ```

## Development Setup

### 1. Create a Virtual Environment

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n sharekhan-mcp python=3.9
conda activate sharekhan-mcp
```

### 2. Install Dependencies

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### 3. Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your test credentials
```

## Making Changes

### Branch Naming

Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
# or
git checkout -b docs/update-readme
```

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these tools before committing:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer(s)]
```

Examples:
- `feat(client): add support for new order types`
- `fix(websocket): handle connection timeout gracefully`
- `docs(readme): update installation instructions`
- `test(tools): add unit tests for order placement`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sharekhan_connect_mcp

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Writing Tests

1. Create test files in the `tests/` directory
2. Use descriptive test names
3. Follow the AAA pattern: Arrange, Act, Assert
4. Mock external dependencies
5. Test both success and failure cases

Example:

```python
def test_place_order_success():
    # Arrange
    client = SharekhanClient("test_key", "test_secret")
    order_data = {"symbol": "RELIANCE", "quantity": 10}
    
    # Act
    result = client.place_order(order_data)
    
    # Assert
    assert result["status"] == "success"
    assert "order_id" in result
```

## Submitting Changes

### 1. Update Your Branch

Before submitting, make sure your branch is up to date:

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Run All Checks

```bash
# Run tests
pytest

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run the installation test
python test_installation.py
```

### 3. Create a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub
3. Fill out the PR template
4. Request review from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a Release

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a release tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
4. Create a GitHub release
5. Package will be automatically published to PyPI

## Documentation

### Updating Documentation

- Update relevant `.md` files in the `docs/` directory
- Update docstrings in code
- Update README.md if needed
- Update type hints for better IDE support

### Documentation Standards

- Use clear, concise language
- Include code examples
- Update all related sections when making changes
- Test all links and examples

## Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and general discussion
- **Email**: Contact maintainers directly for sensitive issues

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README (for significant contributions)

Thank you for contributing to Sharekhan Connect MCP! 🚀
