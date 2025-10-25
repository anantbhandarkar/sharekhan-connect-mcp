"""
Session Manager for Sharekhan Authentication
Handles authentication flow and token refresh
"""

import time
from datetime import datetime, timedelta
from typing import Optional

from loguru import logger

from .client import SharekhanClient


class SharekhanSessionManager:
    """Manages Sharekhan authentication sessions"""

    def __init__(
        self,
        client: SharekhanClient,
        customer_id: str = "12345",
        version_id: str = "1005",
        state: str = "12345",
    ):
        self.client = client
        self.customer_id = customer_id
        self.version_id = version_id
        self.state = state
        self.token_expiry: Optional[datetime] = None
        self.session_expiry: Optional[datetime] = None
        self.refresh_threshold = timedelta(minutes=30)  # Refresh 30 mins before expiry

    def authenticate(
        self, request_token: str, customer_id: Optional[str] = None
    ) -> bool:
        """
        Complete authentication flow (supports both version ID and non-version flows)
        Returns True if authentication successful
        """
        try:
            customer_id = customer_id or self.customer_id

            # Generate session based on version ID
            logger.info("Generating session...")
            if self.version_id and self.version_id != "null":
                # Use version ID flow
                session_data = self.client.generate_session(request_token)
                access_token = self.client.get_access_token(
                    self.client.api_key,
                    session_data.get("session_token"),
                    self.state,
                    versionId=self.version_id,
                )
            else:
                # Use non-version ID flow
                session_data = self.client.generate_session_without_versionId(
                    request_token
                )
                access_token = self.client.get_access_token(
                    self.client.api_key, session_data.get("session_token"), self.state
                )

            if not access_token:
                logger.error("Failed to get access token")
                return False

            # Set expiry times (typically 24 hours)
            self.session_expiry = datetime.now() + timedelta(hours=23)
            self.token_expiry = datetime.now() + timedelta(hours=23)

            logger.info("Authentication completed successfully")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def is_token_valid(self) -> bool:
        """Check if access token is valid"""
        if not self.client.access_token or not self.token_expiry:
            return False

        # Check if token is expired or will expire soon
        if datetime.now() >= (self.token_expiry - self.refresh_threshold):
            logger.warning("Access token expired or expiring soon")
            return False

        return True

    def refresh_token_if_needed(self) -> bool:
        """Refresh token if needed"""
        if self.is_token_valid():
            return True

        logger.info("Attempting to refresh access token...")

        # Implementation would depend on Sharekhan's refresh mechanism
        # For now, we'll require re-authentication
        logger.warning("Token refresh not implemented. Please re-authenticate.")
        return False

    def get_login_url(self, vendor_key: str = "") -> str:
        """Get login URL with proper parameters"""
        return self.client.login_url(
            vendor_key=vendor_key or self.client.vendor_key or "",
            version_id=self.version_id,
            state=self.state,
        )

    def logout(self) -> None:
        """Logout and clear session"""
        self.client.access_token = None
        self.client.session_token = None
        self.token_expiry = None
        self.session_expiry = None
        logger.info("Session cleared")
