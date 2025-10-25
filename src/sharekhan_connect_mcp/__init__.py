"""
Sharekhan Connect MCP Package
A Model Context Protocol (MCP) server for Sharekhan trading APIs
"""

from .client import SharekhanClient
from .server import SharekhanMCPServer
from .tools import SharekhanMCPTools
from .session import SharekhanSessionManager
from .websocket import SharekhanWebSocketClient

__version__ = "1.0.0"
__author__ = "Sharekhan MCP Team"
__license__ = "MIT"

__all__ = [
    "SharekhanClient",
    "SharekhanMCPServer", 
    "SharekhanMCPTools",
    "SharekhanSessionManager",
    "SharekhanWebSocketClient",
]
