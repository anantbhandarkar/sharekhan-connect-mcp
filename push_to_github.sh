#!/bin/bash

# Script to push Sharekhan Connect MCP to GitHub
# Run this script from the sharekhan-connect-mcp directory

echo "🚀 Pushing Sharekhan Connect MCP to GitHub..."

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the sharekhan-connect-mcp directory"
    exit 1
fi

# Check git status
echo "📋 Current git status:"
git status

echo ""
echo "🔐 Authentication Options:"
echo "1. Use GitHub CLI (if installed)"
echo "2. Use Personal Access Token"
echo "3. Use SSH key"
echo "4. Manual push with username/password"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "🔑 Using GitHub CLI..."
        if command -v gh &> /dev/null; then
            gh auth login
            git push -u origin main
        else
            echo "❌ GitHub CLI not found. Please install it first: https://cli.github.com/"
            exit 1
        fi
        ;;
    2)
        echo "🔑 Using Personal Access Token..."
        echo "Enter your GitHub Personal Access Token:"
        read -s token
        git remote set-url origin https://anantbhandarkar:$token@github.com/anantbhandarkar/sharekhan-connect-mcp.git
        git push -u origin main
        ;;
    3)
        echo "🔑 Using SSH key..."
        git remote set-url origin git@github.com:anantbhandarkar/sharekhan-connect-mcp.git
        git push -u origin main
        ;;
    4)
        echo "🔑 Manual push with username/password..."
        echo "You'll be prompted for your GitHub username and password/token"
        git push -u origin main
        ;;
    *)
        echo "❌ Invalid option. Exiting."
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/anantbhandarkar/sharekhan-connect-mcp"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Add topics: mcp, model-context-protocol, sharekhan, trading, api, finance, claude, ai, python"
    echo "3. Enable Issues and Discussions"
    echo "4. Configure branch protection (optional)"
    echo "5. Add PyPI token to GitHub Secrets if you plan to publish to PyPI"
else
    echo ""
    echo "❌ Push failed. Please check your authentication and try again."
    echo ""
    echo "🔧 Troubleshooting:"
    echo "1. Make sure you have access to the repository"
    echo "2. Check your GitHub credentials"
    echo "3. Verify the repository URL is correct"
    echo "4. Try using a Personal Access Token instead of password"
fi
