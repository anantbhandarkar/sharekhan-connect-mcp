"""
Configuration settings for Sharekhan MCP Server
"""

import os
from typing import Optional, Union

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Sharekhan API Configuration (Required)
    sharekhan_api_key: str = Field(
        ..., env="SHAREKHAN_API_KEY", description="Your Sharekhan API Key"
    )
    sharekhan_secret_key: str = Field(
        ...,
        env="SHAREKHAN_SECRET_KEY",
        description="Your Secret Key for token decryption",
    )
    sharekhan_customer_id: str = Field(
        ..., env="SHAREKHAN_CUSTOMER_ID", description="Your Sharekhan Customer/Login ID"
    )
    sharekhan_version_id: Union[str, int, None] = Field(
        "1005",
        env="SHAREKHAN_VERSION_ID",
        description="API Version ID (null/1005/1006)",
    )

    # Optional Sharekhan Configuration
    sharekhan_vendor_key: Optional[str] = Field(
        None,
        env="SHAREKHAN_VENDOR_KEY",
        description="Vendor Key (only for vendor login)",
    )
    sharekhan_state: str = Field(
        "12345", env="SHAREKHAN_STATE", description="OAuth state parameter"
    )

    # MCP Server Configuration
    mcp_port: int = Field(8080, env="MCP_PORT", description="MCP server port")
    mcp_host: str = Field("0.0.0.0", env="MCP_HOST", description="MCP server host")
    redirect_uri: str = Field(
        "http://localhost:8080/auth/callback",
        env="REDIRECT_URI",
        description="OAuth redirect URI",
    )

    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL", description="Logging level")
    log_file: str = Field(
        "logs/sharekhan_mcp.log", env="LOG_FILE", description="Log file path"
    )

    # API Configuration
    api_timeout: int = Field(
        30, env="API_TIMEOUT", description="API request timeout in seconds"
    )
    max_retries: int = Field(3, env="MAX_RETRIES", description="Maximum retry attempts")
    retry_delay: float = Field(
        1.0, env="RETRY_DELAY", description="Delay between retries in seconds"
    )

    # WebSocket Configuration
    ws_timeout: int = Field(
        60, env="WS_TIMEOUT", description="WebSocket connection timeout"
    )
    ws_reconnect_attempts: int = Field(
        5, env="WS_RECONNECT_ATTEMPTS", description="Maximum reconnection attempts"
    )

    @validator("sharekhan_version_id")
    def validate_version_id(cls, v):
        """Validate version ID is one of the allowed values"""
        if v is None or v == "null":
            return None
        if str(v) in ["1005", "1006"]:
            return str(v)
        raise ValueError("SHAREKHAN_VERSION_ID must be null, 1005, or 1006")

    @validator("sharekhan_customer_id")
    def validate_customer_id(cls, v):
        """Validate customer ID is numeric"""
        if not str(v).isdigit():
            raise ValueError("SHAREKHAN_CUSTOMER_ID must be numeric")
        return str(v)

    @validator("sharekhan_api_key", "sharekhan_secret_key")
    def validate_required_fields(cls, v):
        """Validate required fields are not empty"""
        if not v or v.strip() == "":
            raise ValueError("API credentials cannot be empty")
        return v

    def validate_configuration(self) -> dict:
        """Validate the complete configuration and return validation results"""
        errors = []
        warnings = []

        # Check required fields
        if not self.sharekhan_api_key or self.sharekhan_api_key == "your_api_key_here":
            errors.append("SHAREKHAN_API_KEY is not configured")

        if (
            not self.sharekhan_secret_key
            or self.sharekhan_secret_key == "your_secret_key_here"
        ):
            errors.append("SHAREKHAN_SECRET_KEY is not configured")

        if not self.sharekhan_customer_id or self.sharekhan_customer_id == "12345":
            errors.append("SHAREKHAN_CUSTOMER_ID is not configured")

        # Check API key format (basic validation)
        if self.sharekhan_api_key and len(self.sharekhan_api_key) < 10:
            warnings.append("SHAREKHAN_API_KEY seems too short")

        # Check redirect URI format
        if not self.redirect_uri.startswith(("http://", "https://")):
            errors.append("REDIRECT_URI must start with http:// or https://")

        # Check port range
        if not (1 <= self.mcp_port <= 65535):
            errors.append("MCP_PORT must be between 1 and 65535")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def get_sharekhan_credentials(self) -> dict:
        """Get Sharekhan credentials in a clean format"""
        return {
            "api_key": self.sharekhan_api_key,
            "secret_key": self.sharekhan_secret_key,
            "customer_id": self.sharekhan_customer_id,
            "vendor_key": self.sharekhan_vendor_key,
            "version_id": self.sharekhan_version_id,
            "state": self.sharekhan_state,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
