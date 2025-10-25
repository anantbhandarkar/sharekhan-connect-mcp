# Push Sharekhan Connect MCP to GitHub

## 🚀 Quick Push Script

Run the automated script:
```bash
cd "/Users/anantbhandarkar/Documents/Repos/sharekhan-mcp/sharekhan-connect-mcp"
./push_to_github.sh
```

## 🔐 Manual Push Instructions

If the script doesn't work, follow these manual steps:

### Option 1: Using Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`, `write:packages`
   - Copy the token

2. **Push with token:**
   ```bash
   cd "/Users/anantbhandarkar/Documents/Repos/sharekhan-mcp/sharekhan-connect-mcp"
   git remote set-url origin https://anantbhandarkar:YOUR_TOKEN@github.com/anantbhandarkar/sharekhan-connect-mcp.git
   git push -u origin main
   ```

### Option 2: Using Username/Password

```bash
cd "/Users/anantbhandarkar/Documents/Repos/sharekhan-mcp/sharekhan-connect-mcp"
git push -u origin main
# Enter your GitHub username and password when prompted
```

### Option 3: Using SSH Key

1. **Generate SSH key (if you don't have one):**
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

2. **Add SSH key to GitHub:**
   - Copy the public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to GitHub → Settings → SSH and GPG keys → New SSH key
   - Paste the key

3. **Push with SSH:**
   ```bash
   cd "/Users/anantbhandarkar/Documents/Repos/sharekhan-mcp/sharekhan-connect-mcp"
   git remote set-url origin git@github.com:anantbhandarkar/sharekhan-connect-mcp.git
   git push -u origin main
   ```

## 📋 After Successful Push

1. **Visit your repository:** https://github.com/anantbhandarkar/sharekhan-connect-mcp

2. **Configure repository settings:**
   - Go to Settings → General
   - Add description: "A production-ready Model Context Protocol (MCP) server for Sharekhan trading APIs"
   - Add topics: `mcp`, `model-context-protocol`, `sharekhan`, `trading`, `api`, `finance`, `claude`, `ai`, `python`

3. **Enable features:**
   - Go to Settings → Features
   - Enable Issues
   - Enable Discussions
   - Enable Wiki (optional)

4. **Configure GitHub Actions:**
   - Go to Settings → Actions → General
   - Set "Workflow permissions" to "Read and write permissions"

5. **Add PyPI token (for future releases):**
   - Go to Settings → Secrets and variables → Actions
   - Add `PYPI_API_TOKEN` when you're ready to publish to PyPI

## ✅ What's Ready to Push

Your repository contains:
- ✅ Complete MCP server implementation
- ✅ All documentation (README, QUICKSTART, etc.)
- ✅ GitHub Actions workflows for CI/CD
- ✅ Issue and PR templates
- ✅ MIT License and Code of Conduct
- ✅ Professional project structure
- ✅ Environment configuration examples
- ✅ Pre-commit hooks for code quality

## 🎉 Success!

Once pushed, your open-source project will be live at:
**https://github.com/anantbhandarkar/sharekhan-connect-mcp**

The repository is ready for:
- Community contributions
- Issue tracking
- Pull requests
- GitHub Actions CI/CD
- PyPI publishing (when ready)
