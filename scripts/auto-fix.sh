#!/bin/bash
# Auto-fix formatting and import issues

echo "🔧 Auto-fixing code quality issues..."

echo "Formatting code with Black..."
black src/

echo "Sorting imports with isort..."
isort src/

echo "✅ Auto-fixes applied. Review changes with 'git diff'"
