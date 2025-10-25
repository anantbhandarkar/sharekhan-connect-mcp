# Configuration Guide

Complete guide for configuring the Sharekhan Connect MCP server.

## Getting API Credentials

### 1. Register with Sharekhan

1. Visit [Sharekhan API Documentation](https://www.sharekhan.com/api-documentation)
2. Register for API access
3. Complete the application process
4. Wait for approval

### 2. Required Credentials

Once approved, you'll receive:

- **API Key**: Your unique API identifier
- **Secret Key**: Used for token decryption
- **Customer ID**: Your Sharekhan customer/login ID
- **Vendor Key**: (Optional) Only for vendor login mode

## Environment Variables

### Required Variables

```bash
# Your Sharekhan API credentials
SHAREKHAN_API_KEY=your_api_key_here
SHAREKHAN_SECRET_KEY=your_secret_key_here
SHAREKHAN_CUSTOMER_ID=your_customer_id
SHAREKHAN_VERSION_ID=1005  # or 1006, or null
```

### Optional Variables

```bash
# Vendor login (if applicable)
SHAREKHAN_VENDOR_KEY=your_vendor_key

# Server configuration
MCP_HOST=0.0.0.0
MCP_PORT=8080
REDIRECT_URI=http://localhost:8080/auth/callback

# OAuth security
SHAREKHAN_STATE=12345

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/sharekhan_mcp.log

# API settings
API_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1.0

# WebSocket settings
WS_TIMEOUT=60
WS_RECONNECT_ATTEMPTS=5
```

## Configuration Methods

### Method 1: Environment Variables

Set variables in your shell:

```bash
export SHAREKHAN_API_KEY="your_key"
export SHAREKHAN_SECRET_KEY="your_secret"
export SHAREKHAN_CUSTOMER_ID="your_id"
```

### Method 2: .env File

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
SHAREKHAN_API_KEY=your_actual_api_key
SHAREKHAN_SECRET_KEY=your_actual_secret_key
SHAREKHAN_CUSTOMER_ID=your_actual_customer_id
```

### Method 3: System Environment

Set in your system environment (Linux/macOS):
```bash
# Add to ~/.bashrc or ~/.zshrc
export SHAREKHAN_API_KEY="your_key"
export SHAREKHAN_SECRET_KEY="your_secret"
export SHAREKHAN_CUSTOMER_ID="your_id"
```

## API Version Configuration

### Version ID Options

- **1005**: Recommended for most use cases
- **1006**: Alternative version
- **null**: No version ID (legacy mode)

### Setting Version ID

```bash
# Via environment variable
export SHAREKHAN_VERSION_ID=1005

# Via .env file
SHAREKHAN_VERSION_ID=1005
```

## Authentication Flow

### 1. Get Login URL

```bash
curl http://localhost:8080/auth/login
```

Response:
```json
{
  "status": "success",
  "data": {
    "login_url": "https://api.sharekhan.com/v1/auth/login?api_key=..."
  }
}
```

### 2. Complete Login

1. Open the `login_url` in your browser
2. Login with your Sharekhan credentials
3. You'll be redirected to the callback URL
4. Extract the `request_token` from the URL

### 3. Exchange Token

```bash
curl -X POST "http://localhost:8080/auth/callback" \
  -H "Content-Type: application/json" \
  -d '{
    "request_token": "YOUR_REQUEST_TOKEN",
    "customer_id": "YOUR_CUSTOMER_ID"
  }'
```

## Configuration Validation

The server validates your configuration on startup:

### Check Configuration

```bash
# Start the server to see validation results
sharekhan-mcp
```

### Common Validation Errors

1. **Missing API Key**:
   ```
   ERROR: SHAREKHAN_API_KEY is not configured
   ```

2. **Invalid Version ID**:
   ```
   ERROR: SHAREKHAN_VERSION_ID must be null, 1005, or 1006
   ```

3. **Invalid Customer ID**:
   ```
   ERROR: SHAREKHAN_CUSTOMER_ID must be numeric
   ```

## Troubleshooting

### Common Issues

#### 1. Authentication Failed

**Problem**: `Authentication failed` error

**Solutions**:
- Verify your API credentials are correct
- Check that your Customer ID is numeric
- Ensure you're using the correct Version ID
- Try regenerating your API credentials

#### 2. Connection Refused

**Problem**: `Connection refused` when starting server

**Solutions**:
- Check if port 8080 is available
- Try changing the port: `MCP_PORT=8081`
- Check firewall settings

#### 3. Invalid Credentials

**Problem**: `Invalid credentials` error

**Solutions**:
- Double-check your API Key and Secret Key
- Ensure no extra spaces in environment variables
- Verify credentials are active in Sharekhan dashboard

#### 4. Token Expired

**Problem**: `Token expired` error

**Solutions**:
- Re-authenticate using the login flow
- Check system time synchronization
- Verify token refresh mechanism

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
export LOG_LEVEL=DEBUG
sharekhan-mcp
```

### Health Checks

Check server health:

```bash
# Basic health check
curl http://localhost:8080/health

# Detailed health status
curl http://localhost:8080/monitoring/health
```

## Security Best Practices

### 1. Environment Variables

- Never commit `.env` files to version control
- Use strong, unique API keys
- Rotate credentials regularly

### 2. Network Security

- Use HTTPS in production
- Restrict server access with firewall rules
- Monitor API usage

### 3. Credential Management

- Store credentials in secure environment variable systems
- Use different credentials for development and production
- Implement proper access controls

## Production Deployment

### Environment Setup

```bash
# Production environment variables
export SHAREKHAN_API_KEY="prod_api_key"
export SHAREKHAN_SECRET_KEY="prod_secret_key"
export SHAREKHAN_CUSTOMER_ID="prod_customer_id"
export MCP_HOST="0.0.0.0"
export MCP_PORT="8080"
export LOG_LEVEL="INFO"
export REDIRECT_URI="https://yourdomain.com/auth/callback"
```

### Docker Deployment

```bash
docker run -d \
  --name sharekhan-mcp \
  -p 8080:8080 \
  -e SHAREKHAN_API_KEY=your_key \
  -e SHAREKHAN_SECRET_KEY=your_secret \
  -e SHAREKHAN_CUSTOMER_ID=your_id \
  sharekhan-connect-mcp
```

## Support

If you encounter issues:

1. Check this configuration guide
2. Review the [Quick Start Guide](QUICKSTART.md)
3. Check server logs for error details
4. Open an issue in the repository
5. Contact Sharekhan support for API-related issues
