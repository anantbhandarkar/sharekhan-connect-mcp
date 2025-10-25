# Sharekhan Connect MCP - Quick Start Guide

Get your Sharekhan MCP Server running in 5 minutes! 🚀

## Prerequisites

- Python 3.8+
- Sharekhan API credentials (see [CONFIGURATION.md](CONFIGURATION.md) for details)

## Step 1: Get Your Credentials

Contact Sharekhan support to get:
- API Key
- Secret Key  
- Customer ID
- (Optional) Vendor Key

## Step 2: Installation

Choose your preferred method:

### Option A: Via uv (Recommended)
```bash
uvx install sharekhan-connect-mcp
```

### Option B: Via pip
```bash
pip install sharekhan-connect-mcp
```

### Option C: From source
```bash
git clone https://github.com/sharekhan-mcp/sharekhan-connect-mcp.git
cd sharekhan-connect-mcp
pip install -e .
```

## Step 3: Configure

Set your environment variables:

```bash
# Required - Replace with your actual values
export SHAREKHAN_API_KEY=your_actual_api_key
export SHAREKHAN_SECRET_KEY=your_actual_secret_key
export SHAREKHAN_CUSTOMER_ID=your_actual_customer_id
export SHAREKHAN_VERSION_ID=1005

# Optional
export SHAREKHAN_VENDOR_KEY=your_vendor_key_if_applicable
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Step 4: Start Server

```bash
sharekhan-mcp
```

You should see:
```
Starting Sharekhan MCP Server
Sharekhan MCP Server initialized
Starting Sharekhan MCP Server on 0.0.0.0:8080
```

## Step 5: Authenticate

### Get Login URL
```bash
curl http://localhost:8080/auth/login
```

### Complete Login
1. Copy the `login_url` from the response
2. Open it in your browser
3. Login with your Sharekhan credentials
4. Note the `request_token` from the callback URL

### Exchange Token
```bash
curl -X POST "http://localhost:8080/auth/callback" \
  -H "Content-Type: application/json" \
  -d '{"request_token": "YOUR_REQUEST_TOKEN", "customer_id": "YOUR_CUSTOMER_ID"}'
```

## Step 6: Test

### Check Status
```bash
curl http://localhost:8080/auth/status
```

### List Tools
```bash
curl http://localhost:8080/tools
```

### Test Holdings
```bash
curl -X POST "http://localhost:8080/tools/get_holdings" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "YOUR_CUSTOMER_ID"}'
```

## Claude Desktop Integration

Add to your Claude Desktop MCP configuration:

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

## ✅ You're Done!

Your Sharekhan MCP Server is now running and ready to use!

## Need Help?

- **Detailed Setup**: See [CONFIGURATION.md](CONFIGURATION.md)
- **MCP Integration**: See [MCP_INTEGRATION.md](MCP_INTEGRATION.md)
- **Troubleshooting**: Check the troubleshooting section in CONFIGURATION.md

## Next Steps

1. **Integrate with AI agents** using MCP protocol
2. **Test trading operations** in sandbox mode
3. **Deploy to production** with proper security

---

**Happy Trading!** 📈
