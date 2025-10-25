# Support

We're here to help! This document provides information about getting support for Sharekhan Connect MCP.

## Getting Help

### 📚 Documentation First

Before reaching out for support, please check our comprehensive documentation:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed setup instructions
- **[MCP Integration Guide](docs/MCP_INTEGRATION.md)** - Claude Desktop and MCP client setup
- **[API Reference](README.md#available-tools)** - Complete tool documentation

### 🐛 Bug Reports

Found a bug? Please report it using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md):

1. Go to the [Issues](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/issues) page
2. Click "New Issue"
3. Select "Bug report"
4. Fill out the template with as much detail as possible

**Please include:**
- Your environment details (OS, Python version, package version)
- Steps to reproduce the issue
- Expected vs actual behavior
- Relevant logs and error messages
- Your configuration (with sensitive data removed)

### 💡 Feature Requests

Have an idea for a new feature? We'd love to hear it!

1. Go to the [Issues](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/issues) page
2. Click "New Issue"
3. Select "Feature request"
4. Describe your idea and use case

### 💬 Community Support

For general questions and discussions:

- **[GitHub Discussions](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/discussions)** - Ask questions, share ideas, get help from the community
- **[GitHub Issues](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/issues)** - Report bugs and request features

### 📧 Direct Support

For urgent issues or private matters:

- **Email**: [support@sharekhan-mcp.com](mailto:support@sharekhan-mcp.com)
- **Security Issues**: [security@sharekhan-mcp.com](mailto:security@sharekhan-mcp.com)

## Common Issues

### Installation Problems

**Problem**: Package won't install
**Solutions**:
- Ensure you have Python 3.8 or higher
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment
- Check your internet connection

**Problem**: Import errors after installation
**Solutions**:
- Verify the package is installed: `pip list | grep sharekhan`
- Check your Python path
- Try reinstalling: `pip uninstall sharekhan-connect-mcp && pip install sharekhan-connect-mcp`

### Configuration Issues

**Problem**: "Authentication required" error
**Solutions**:
- Complete the authentication flow using `get_login_url` and `authenticate` tools
- Verify your API credentials are correct
- Check that your Customer ID is numeric
- Ensure your API keys are active

**Problem**: "Configuration error" on startup
**Solutions**:
- Check all required environment variables are set
- Verify the format of your configuration values
- Use the `.env.example` file as a template
- Run the configuration validation

### MCP Integration Issues

**Problem**: Claude Desktop can't connect to MCP server
**Solutions**:
- Check your MCP configuration in Claude Desktop
- Verify the server is running: `curl http://localhost:8080/health`
- Check environment variables are passed correctly
- Review Claude Desktop logs for error messages

**Problem**: Tools not appearing in Claude Desktop
**Solutions**:
- Restart Claude Desktop after configuration changes
- Verify the MCP server is running
- Check the tool list: `curl http://localhost:8080/tools`
- Ensure authentication is complete

### API Issues

**Problem**: Sharekhan API errors
**Solutions**:
- Check your API credentials with Sharekhan
- Verify your account has API access
- Check API rate limits
- Contact Sharekhan support for API-specific issues

**Problem**: WebSocket connection issues
**Solutions**:
- Check your internet connection
- Verify WebSocket URL is accessible
- Check firewall settings
- Review WebSocket logs

## Troubleshooting Steps

### 1. Check Installation

```bash
# Verify package is installed
pip list | grep sharekhan

# Test import
python -c "import sharekhan_connect_mcp; print('OK')"

# Run installation test
python test_installation.py
```

### 2. Check Configuration

```bash
# Verify environment variables
echo $SHAREKHAN_API_KEY
echo $SHAREKHAN_SECRET_KEY
echo $SHAREKHAN_CUSTOMER_ID

# Test configuration
python -c "from sharekhan_connect_mcp.config import Settings; s = Settings(); print(s.validate_configuration())"
```

### 3. Check Server Health

```bash
# Start server
sharekhan-mcp

# In another terminal, check health
curl http://localhost:8080/health

# Check available tools
curl http://localhost:8080/tools
```

### 4. Check Logs

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
sharekhan-mcp

# Check log files
tail -f logs/sharekhan_mcp.log
```

## Response Times

We aim to respond to support requests within:

- **GitHub Issues**: 2-3 business days
- **GitHub Discussions**: 1-2 business days
- **Email Support**: 1-2 business days
- **Security Issues**: 24 hours

## Contributing to Support

You can help improve our support by:

- **Answering questions** in GitHub Discussions
- **Improving documentation** by submitting pull requests
- **Reporting issues** with detailed information
- **Sharing solutions** that worked for you

## Resources

- **[Sharekhan API Documentation](https://www.sharekhan.com/api-documentation)** - Official Sharekhan API docs
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - MCP specification
- **[Claude Desktop](https://claude.ai/desktop)** - Claude Desktop documentation
- **[Python Documentation](https://docs.python.org/)** - Python language reference

## Feedback

We value your feedback! If you have suggestions for improving our support:

- Open a [GitHub Discussion](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/discussions)
- Submit a [Feature Request](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/issues/new?template=feature_request.md)
- Email us at [feedback@sharekhan-mcp.com](mailto:feedback@sharekhan-mcp.com)

Thank you for using Sharekhan Connect MCP! 🚀
