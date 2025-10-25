"""
Sharekhan MCP Server
Main MCP server implementation with authentication and session handling
"""

import asyncio
import sys
import os
from typing import Dict, Any, List
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .config import Settings
from .client import SharekhanClient
from .session import SharekhanSessionManager
from .tools import SharekhanMCPTools
from .websocket import SharekhanWebSocketClient
from .logger import setup_logging

# Mock MCP classes for compatibility
class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class MCPServer:
    def __init__(self):
        self.tools = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Sharekhan MCP Server...")

    # Initialize components
    settings = app.state.settings
    client = SharekhanClient(
        api_key=settings.sharekhan_api_key,
        secret_key=settings.sharekhan_secret_key,
        vendor_key=settings.sharekhan_vendor_key
    )

    session_manager = SharekhanSessionManager(
        client, 
        customer_id=settings.sharekhan_customer_id,
        version_id=str(settings.sharekhan_version_id) if settings.sharekhan_version_id else None,
        state=settings.sharekhan_state
    )
    tools = SharekhanMCPTools(client, session_manager)

    # Initialize WebSocket client (will be connected after authentication)
    ws_client = SharekhanWebSocketClient(access_token="")

    # Store in app state
    app.state.client = client
    app.state.session_manager = session_manager
    app.state.tools = tools
    app.state.ws_client = ws_client

    logger.info("Sharekhan MCP Server initialized")

    yield

    logger.info("Shutting down Sharekhan MCP Server...")
    if session_manager:
        session_manager.logout()

    # Disconnect WebSocket
    ws_client = getattr(app.state, 'ws_client', None)
    if ws_client:
        await ws_client.disconnect()

class SharekhanMCPServer:
    """Main MCP Server for Sharekhan Trading APIs"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.app = FastAPI(
            title="Sharekhan MCP Server",
            description="MCP server for Sharekhan trading APIs",
            version="1.0.0",
            lifespan=lifespan
        )

        # Store settings in app state
        self.app.state.settings = settings

        # Setup middleware
        self._setup_middleware()

        # Setup routes
        self._setup_routes()

    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Setup API routes"""

        @self.app.get("/")
        async def root():
            """Root endpoint"""
            return {
                "message": "Sharekhan MCP Server",
                "version": "1.0.0",
                "status": "running"
            }

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            try:
                # Check if components are initialized
                client = getattr(self.app.state, 'client', None)
                session_manager = getattr(self.app.state, 'session_manager', None)

                if not client or not session_manager:
                    return {"status": "unhealthy", "message": "Components not initialized"}

                # Check authentication status
                is_authenticated = session_manager.is_token_valid()

                return {
                    "status": "healthy",
                    "authenticated": is_authenticated,
                    "timestamp": asyncio.get_event_loop().time()
                }

            except Exception as e:
                logger.error(f"Health check failed: {e}")
                raise HTTPException(status_code=503, detail=str(e))

        @self.app.get("/auth/login")
        async def get_login_url():
            """Get login URL for authentication"""
            try:
                tools = getattr(self.app.state, 'tools', None)
                if not tools:
                    raise HTTPException(status_code=503, detail="Tools not initialized")

                result = await tools.get_login_url()
                return result

            except Exception as e:
                logger.error(f"Failed to get login URL: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/auth/callback")
        async def auth_callback(request_token: str, customer_id: str = "12345"):
            """Handle authentication callback"""
            try:
                session_manager = getattr(self.app.state, 'session_manager', None)
                if not session_manager:
                    raise HTTPException(status_code=503, detail="Session manager not initialized")

                success = session_manager.authenticate(request_token, customer_id)

                if success:
                    return {"status": "success", "message": "Authentication successful"}
                else:
                    raise HTTPException(status_code=401, detail="Authentication failed")

            except Exception as e:
                logger.error(f"Authentication callback failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/tools")
        async def list_tools():
            """List available MCP tools"""
            try:
                tools = getattr(self.app.state, 'tools', None)
                if not tools:
                    raise HTTPException(status_code=503, detail="Tools not initialized")

                # Get all tool methods from the tools class
                tool_methods = [method for method in dir(tools)
                              if not method.startswith('_') and hasattr(getattr(tools, method), '__name__')]

                return {
                    "tools": tool_methods,
                    "total": len(tool_methods)
                }

            except Exception as e:
                logger.error(f"Failed to list tools: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/tools/{tool_name}")
        async def execute_tool(tool_name: str, request_data: Dict[str, Any]):
            """Execute a specific MCP tool"""
            try:
                tools = getattr(self.app.state, 'tools', None)
                if not tools:
                    raise HTTPException(status_code=503, detail="Tools not initialized")

                # Get the tool method
                tool_method = getattr(tools, tool_name, None)
                if not tool_method:
                    raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

                # Execute the tool
                result = await tool_method(**request_data)
                return result

            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/auth/status")
        async def auth_status():
            """Get authentication status"""
            try:
                session_manager = getattr(self.app.state, 'session_manager', None)
                if not session_manager:
                    raise HTTPException(status_code=503, detail="Session manager not initialized")

                is_authenticated = session_manager.is_token_valid()

                return {
                    "authenticated": is_authenticated,
                    "has_access_token": bool(session_manager.client.access_token),
                    "token_expiry": session_manager.token_expiry.isoformat() if session_manager.token_expiry else None
                }

            except Exception as e:
                logger.error(f"Failed to get auth status: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/auth/logout")
        async def logout():
            """Logout and clear session"""
            try:
                session_manager = getattr(self.app.state, 'session_manager', None)
                if not session_manager:
                    raise HTTPException(status_code=503, detail="Session manager not initialized")

                session_manager.logout()
                return {"status": "success", "message": "Logged out successfully"}

            except Exception as e:
                logger.error(f"Logout failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    def run(self):
        """Run the MCP server"""
        import uvicorn

        logger.info(f"Starting Sharekhan MCP Server on {self.settings.mcp_host}:{self.settings.mcp_port}")

        uvicorn.run(
            self.app,
            host=self.settings.mcp_host,
            port=self.settings.mcp_port,
            log_level=self.settings.log_level.lower(),
            access_log=True
        )

def main():
    """Entry point for CLI and MCP invocation"""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Initialize settings
    settings = Settings()
    
    # Setup logging
    logger = setup_logging(settings)
    logger.info("Starting Sharekhan MCP Server")
    
    # Initialize and run the MCP server
    try:
        server = SharekhanMCPServer(settings)
        server.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
