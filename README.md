# Sharekhan Connect MCP

[![PyPI version](https://badge.fury.io/py/sharekhan-connect-mcp.svg)](https://badge.fury.io/py/sharekhan-connect-mcp)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-available-green.svg)](https://github.com/sharekhan-mcp/sharekhan-connect-mcp#readme)
[![CI](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/workflows/CI/badge.svg)](https://github.com/sharekhan-mcp/sharekhan-connect-mcp/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A production-ready Model Context Protocol (MCP) server for Sharekhan trading APIs, enabling AI agents to perform comprehensive trading operations through a standardized interface.

## 🚀 Quick Start

### Installation

Choose your preferred method:

**Via uv (Recommended):**
```bash
uvx install sharekhan-connect-mcp
```

**Via pip:**
```bash
pip install sharekhan-connect-mcp
```

**From source:**
```bash
git clone https://github.com/sharekhan-mcp/sharekhan-connect-mcp.git
cd sharekhan-connect-mcp
pip install -e .
```

### Configuration

1. **Get your Sharekhan API credentials** from [Sharekhan API Documentation](docs/sharekhan-api-guide.md)

2. **Set up environment variables:**
```bash
export SHAREKHAN_API_KEY="your_api_key"
export SHAREKHAN_SECRET_KEY="your_secret_key"
export SHAREKHAN_CUSTOMER_ID="your_customer_id"
export SHAREKHAN_VERSION_ID="1005"
```

3. **Run the server:**
```bash
sharekhan-mcp
```

### Claude Desktop Integration

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

## ✨ Features

- **📈 Trading Operations**: Place, modify, and cancel orders
- **💼 Portfolio Management**: Access holdings, positions, and trade history
- **📊 Market Data**: Get real-time quotes and historical data
- **🔄 Real-time Updates**: WebSocket integration for live market feeds
- **🔐 Secure Authentication**: OAuth-based authentication with Sharekhan
- **📊 Monitoring**: Built-in health checks and performance metrics
- **🤖 AI-Ready**: Full MCP protocol support for AI agents

## 🛠️ Available Tools

### Trading Operations
- `place_order` - Place trading orders
- `modify_order` - Modify existing orders  
- `cancel_order` - Cancel orders

### Portfolio Management
- `get_holdings` - Retrieve portfolio holdings
- `get_positions` - Get trading positions
- `get_orders` - Access order book
- `get_trades` - Get trade history

### Market Data
- `get_historical_data` - Fetch historical market data
- `get_quote` - Get current market quotes

### Authentication
- `authenticate` - Complete authentication flow
- `get_login_url` - Generate login URL

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - 5-minute setup guide
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed configuration options
- **[MCP Integration](docs/MCP_INTEGRATION.md)** - Claude Desktop and MCP client setup

## 🔧 Configuration

### Required Environment Variables

```bash
SHAREKHAN_API_KEY=your_api_key_here
SHAREKHAN_SECRET_KEY=your_secret_key_here
SHAREKHAN_CUSTOMER_ID=your_customer_id
SHAREKHAN_VERSION_ID=1005  # or 1006, or null
```

### Optional Configuration

```bash
SHAREKHAN_VENDOR_KEY=your_vendor_key  # For vendor login
MCP_HOST=0.0.0.0
MCP_PORT=8080
REDIRECT_URI=http://localhost:8080/auth/callback
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker
docker build -t sharekhan-connect-mcp .
docker run -d \
  --name sharekhan-mcp \
  -p 8080:8080 \
  -e SHAREKHAN_API_KEY=your_key \
  -e SHAREKHAN_SECRET_KEY=your_secret \
  -e SHAREKHAN_CUSTOMER_ID=your_id \
  sharekhan-connect-mcp
```

## 🔒 Security

- ✅ Token-based authentication
- ✅ Input validation with Pydantic
- ✅ Centralized error handling
- ✅ Structured logging
- ✅ Environment-based configuration
- ✅ No credentials in code

## 🏗️ Architecture

The server follows a layered architecture:

- **MCP Protocol Layer** - Tool interface and communication
- **FastAPI Server** - HTTP API and request routing
- **Business Logic** - Trading operations and validation
- **Service Layer** - API client and session management
- **Infrastructure** - Configuration, logging, and monitoring

## 📊 Monitoring

Built-in monitoring includes:

- Request metrics and performance tracking
- System resource monitoring (CPU, memory, disk)
- Error tracking and categorization
- API health checks
- Tool usage analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Configuration Issues**: Check [CONFIGURATION.md](docs/CONFIGURATION.md)
- **Setup Problems**: See [QUICKSTART.md](docs/QUICKSTART.md)
- **API Issues**: Contact [Sharekhan Support](https://www.sharekhan.com/api-documentation)
- **MCP Server Issues**: Open an issue in this repository

## ⚠️ Important Notes

- **Never commit your `.env` file** to version control
- **Test with small amounts** in sandbox mode first
- **Keep your API credentials secure**
- **Monitor your API usage** through Sharekhan's dashboard

## 🔗 Links

- [Sharekhan API Documentation](https://www.sharekhan.com/api-documentation)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)

---

**Ready to get started?** Jump to [QUICKSTART.md](docs/QUICKSTART.md) for a 5-minute setup! 🚀
