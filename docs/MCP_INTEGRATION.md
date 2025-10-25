# MCP Integration Guide

Complete guide for integrating Sharekhan Connect MCP with various MCP clients.

## Claude Desktop Integration

### Prerequisites

- Claude Desktop installed
- Sharekhan Connect MCP installed (`pip install sharekhan-connect-mcp` or `uvx install sharekhan-connect-mcp`)

### Configuration

1. **Locate Claude Desktop MCP configuration file**:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. **Add Sharekhan MCP server configuration**:

```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_api_key",
        "SHAREKHAN_SECRET_KEY": "your_secret_key",
        "SHAREKHAN_CUSTOMER_ID": "your_customer_id",
        "SHAREKHAN_VERSION_ID": "1005"
      }
    }
  }
}
```

### Alternative Configuration Methods

#### Method 1: Using uvx (Recommended)
```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id"
      }
    }
  }
}
```

#### Method 2: Using pip-installed package
```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "python",
      "args": ["-m", "sharekhan_connect_mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id"
      }
    }
  }
}
```

#### Method 3: Local development
```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "python",
      "args": ["-m", "sharekhan_connect_mcp"],
      "cwd": "/path/to/sharekhan-connect-mcp",
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id"
      }
    }
  }
}
```

### Testing the Integration

1. **Restart Claude Desktop** after adding the configuration
2. **Check MCP connection** in Claude Desktop settings
3. **Test with a simple query**:
   - "What trading tools are available?"
   - "Help me get my portfolio holdings"

## Other MCP Clients

### Generic MCP Client

For any MCP-compatible client, use the stdio mode:

```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id"
      }
    }
  }
}
```

### HTTP Mode

For clients that support HTTP mode:

```json
{
  "mcpServers": {
    "sharekhan": {
      "url": "http://localhost:8080",
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id"
      }
    }
  }
}
```

## Available Tools

Once integrated, the following tools are available:

### Trading Operations
- `place_order` - Place trading orders
- `modify_order` - Modify existing orders
- `cancel_order` - Cancel orders

### Portfolio Management
- `get_holdings` - Get portfolio holdings
- `get_positions` - Get trading positions
- `get_orders` - Get order book
- `get_trades` - Get trade history

### Market Data
- `get_historical_data` - Get historical market data
- `get_quote` - Get current market quotes

### Authentication
- `authenticate` - Complete authentication flow
- `get_login_url` - Generate login URL

## Usage Examples

### Example 1: Get Portfolio Holdings

```
User: "Show me my current holdings"
Claude: I'll help you get your portfolio holdings. Let me retrieve that information for you.
[Uses get_holdings tool]
```

### Example 2: Place an Order

```
User: "Buy 10 shares of RELIANCE at market price"
Claude: I'll help you place a market order for 10 shares of RELIANCE. Let me execute that for you.
[Uses place_order tool with appropriate parameters]
```

### Example 3: Get Market Quote

```
User: "What's the current price of TCS?"
Claude: Let me get the current market quote for TCS.
[Uses get_quote tool]
```

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Starting

**Problem**: Claude Desktop shows "MCP server not responding"

**Solutions**:
- Check that `uvx` is installed: `uvx --version`
- Verify the package is installed: `uvx list | grep sharekhan`
- Check environment variables are set correctly
- Review Claude Desktop logs for error details

#### 2. Authentication Required

**Problem**: Tools return "Authentication required" error

**Solutions**:
- Use the `get_login_url` tool to get the login URL
- Complete the authentication flow
- Use the `authenticate` tool with the request token

#### 3. Tool Not Found

**Problem**: "Tool not found" error

**Solutions**:
- Check that the MCP server is running
- Verify the tool name is correct
- Restart Claude Desktop
- Check MCP server logs

#### 4. Environment Variables Not Set

**Problem**: "Configuration error" or missing credentials

**Solutions**:
- Ensure all required environment variables are set
- Check the configuration in Claude Desktop
- Verify the `.env` file if using one
- Test with manual environment variable setting

### Debug Mode

Enable debug logging for troubleshooting:

```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Health Checks

Check if the MCP server is running:

```bash
# Check if server is responding
curl http://localhost:8080/health

# List available tools
curl http://localhost:8080/tools
```

## Security Considerations

### Environment Variables

- Never hardcode credentials in configuration files
- Use environment variables for sensitive data
- Consider using secure credential management systems

### Network Security

- Use HTTPS in production environments
- Restrict access to the MCP server
- Monitor API usage and access patterns

### Authentication

- Complete the authentication flow before using trading tools
- Monitor token expiry and re-authenticate as needed
- Use strong, unique credentials

## Advanced Configuration

### Custom Server Settings

```json
{
  "mcpServers": {
    "sharekhan": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "your_key",
        "SHAREKHAN_SECRET_KEY": "your_secret",
        "SHAREKHAN_CUSTOMER_ID": "your_id",
        "MCP_HOST": "0.0.0.0",
        "MCP_PORT": "8080",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Multiple Instances

You can run multiple instances with different configurations:

```json
{
  "mcpServers": {
    "sharekhan-dev": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "dev_key",
        "SHAREKHAN_SECRET_KEY": "dev_secret",
        "SHAREKHAN_CUSTOMER_ID": "dev_id",
        "MCP_PORT": "8080"
      }
    },
    "sharekhan-prod": {
      "command": "uvx",
      "args": ["sharekhan-connect-mcp"],
      "env": {
        "SHAREKHAN_API_KEY": "prod_key",
        "SHAREKHAN_SECRET_KEY": "prod_secret",
        "SHAREKHAN_CUSTOMER_ID": "prod_id",
        "MCP_PORT": "8081"
      }
    }
  }
}
```

## Support

If you encounter issues with MCP integration:

1. Check this integration guide
2. Review the [Configuration Guide](CONFIGURATION.md)
3. Check Claude Desktop logs
4. Open an issue in the repository
5. Contact support for MCP-specific issues
