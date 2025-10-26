"""
Sharekhan API Client
Replaces KiteConnect functionality with Sharekhan APIs
"""

import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, cast

import requests
from loguru import logger


class SharekhanClient:
    """Sharekhan API client replacing KiteConnect functionality"""

    def __init__(self, api_key: str, secret_key: str, vendor_key: Optional[str] = None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.vendor_key = vendor_key
        self.access_token: Optional[str] = None
        self.session_token: Optional[str] = None
        self.base_url = "https://api.sharekhan.com/v1"

        # API endpoints
        self.endpoints = {
            "login": "/auth/login",
            "session": "/auth/session",
            "token": "/auth/token",
            "holdings": "/portfolio/holdings",
            "positions": "/portfolio/positions",
            "orders": "/orders",
            "trades": "/orders/trades",
            "history": "/market/history",
            "quote": "/market/quote",
            "websocket": "/stream/websocket",
        }

    def login_url(
        self, vendor_key: str = "", version_id: str = "1005", state: str = "12345"
    ) -> str:
        """Generate login URL for Sharekhan authentication (matches SharekhanConnect API)"""
        params = {
            "api_key": self.api_key,
            "vendor_key": vendor_key or self.vendor_key or "",
            "version_id": version_id,
            "state": state,
            "redirect_uri": "http://localhost:8080/auth/callback",
        }

        url = f"{self.base_url}{self.endpoints['login']}"
        logger.info(f"Generated login URL: {url}")
        return f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    def get_login_url(self, version_id: str = "1005") -> str:
        """Generate login URL for Sharekhan authentication (legacy method)"""
        return self.login_url(version_id=version_id)

    def generate_session(
        self, request_token: str, secret_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate session using request token (matches SharekhanConnect API)"""
        try:
            url = f"{self.base_url}{self.endpoints['session']}"
            payload = {
                "api_key": self.api_key,
                "request_token": request_token,
                "secret_key": secret_key or self.secret_key,
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            session_data = response.json()
            self.session_token = session_data.get("session_token")

            logger.info("Session generated successfully")
            return cast(Dict[str, Any], session_data)

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate session: {e}")
            raise

    def generate_session_without_versionId(
        self, request_token: str, secret_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate session without version ID (matches SharekhanConnect API)"""
        return self.generate_session(request_token, secret_key)

    def get_access_token(
        self, api_key: str, session: str, state: str, versionId: Optional[str] = None
    ) -> str:
        """Get access token using session (matches SharekhanConnect API)"""
        try:
            url = f"{self.base_url}{self.endpoints['token']}"
            payload = {"api_key": api_key, "session_token": session, "state": state}

            if versionId:
                payload["versionId"] = versionId

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            token_data: Dict[str, Any] = response.json()
            access_token: Optional[str] = token_data.get("access_token")

            if not access_token:
                raise ValueError("No access token in API response")

            self.access_token = access_token
            logger.info("Access token obtained successfully")
            return access_token

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            raise

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make authenticated API request"""
        if not self.access_token:
            raise ValueError("Access token not available. Please authenticate first.")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30,
            )
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    def requestHeaders(self) -> Dict[str, str]:
        """Get request headers (matches SharekhanConnect API)"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

    # Trading Operations (matches SharekhanConnect API)
    def placeOrder(self, orderparams: Dict[str, Any]) -> Dict[str, Any]:
        """Place an order (matches SharekhanConnect API)"""
        return self._make_request("POST", self.endpoints["orders"], data=orderparams)

    def place_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Place an order (legacy method)"""
        return self.placeOrder(params)

    def modifyOrder(self, orderparams: Dict[str, Any]) -> Dict[str, Any]:
        """Modify an existing order (matches SharekhanConnect API)"""
        order_id = orderparams.get("orderId")
        if not order_id:
            raise ValueError("orderId is required in orderparams")

        endpoint = f"{self.endpoints['orders']}/{order_id}"
        return self._make_request("PUT", endpoint, data=orderparams)

    def modify_order(self, order_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Modify an existing order (legacy method)"""
        params["orderId"] = order_id
        return self.modifyOrder(params)

    def cancelOrder(self, orderparams: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel an order (matches SharekhanConnect API)"""
        order_id = orderparams.get("orderId")
        if not order_id:
            raise ValueError("orderId is required in orderparams")

        endpoint = f"{self.endpoints['orders']}/{order_id}"
        return self._make_request("DELETE", endpoint, data=orderparams)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order (legacy method)"""
        return self.cancelOrder({"orderId": order_id})

    # Portfolio Operations (matches SharekhanConnect API)
    def holdings(self, customerId: str) -> List[Dict[str, Any]]:
        """Get holdings for customer (matches SharekhanConnect API)"""
        params = {"customer_id": customerId}
        result = self._make_request("GET", self.endpoints["holdings"], params=params)
        return cast(List[Dict[str, Any]], result.get("holdings", []))

    def positions(self, customerId: str) -> Dict[str, Any]:
        """Get positions for customer (matches SharekhanConnect API)"""
        params = {"customer_id": customerId}
        return self._make_request("GET", self.endpoints["positions"], params=params)

    def trades(self, customerId: str) -> List[Dict[str, Any]]:
        """Get trade history for customer (matches SharekhanConnect API)"""
        params = {"customer_id": customerId}
        result = self._make_request("GET", self.endpoints["trades"], params=params)
        return cast(List[Dict[str, Any]], result.get("trades", []))

    def exchange(self, exchange: str, customerId: str, orderId: str) -> Dict[str, Any]:
        """Get order details (matches SharekhanConnect API)"""
        params = {"exchange": exchange, "customer_id": customerId, "order_id": orderId}
        return self._make_request(
            "GET", f"{self.endpoints['orders']}/details", params=params
        )

    def exchangetrades(
        self, exchange: str, customerId: str, orderId: str
    ) -> List[Dict[str, Any]]:
        """Get trades generated by an order (matches SharekhanConnect API)"""
        params = {"exchange": exchange, "customer_id": customerId, "order_id": orderId}
        result = self._make_request(
            "GET", f"{self.endpoints['trades']}/by-order", params=params
        )
        return cast(List[Dict[str, Any]], result.get("trades", []))

    # Market Data Operations (matches SharekhanConnect API)
    def historicaldata(
        self, exchange: str, scripcode: str, interval: str
    ) -> List[Dict[str, Any]]:
        """Get historical market data (matches SharekhanConnect API)"""
        params = {"exchange": exchange, "scripcode": scripcode, "interval": interval}
        result = self._make_request("GET", self.endpoints["history"], params=params)
        return cast(List[Dict[str, Any]], result.get("data", []))

    def historical_data(
        self,
        exchange: str,
        scrip_code: str,
        interval: str,
        from_date: datetime,
        to_date: datetime,
    ) -> List[Dict[str, Any]]:
        """Get historical market data (legacy method)"""
        return self.historicaldata(exchange, scrip_code, interval)

    def quote(self, exchange: str, scrip_code: str) -> Dict[str, Any]:
        """Get market quote"""
        params = {"exchange": exchange, "scrip_code": scrip_code}
        return self._make_request("GET", self.endpoints["quote"], params=params)

    def master(self, exchange: str) -> List[Dict[str, Any]]:
        """Get script master data (matches SharekhanConnect API)"""
        params = {"exchange": exchange}
        result = self._make_request("GET", "/master", params=params)
        return cast(List[Dict[str, Any]], result.get("master", []))

    # Order Book Operations
    def orders(self, customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get order book"""
        params = {}
        if customer_id:
            params["customer_id"] = customer_id
        result = self._make_request("GET", self.endpoints["orders"], params=params)
        return cast(List[Dict[str, Any]], result.get("orders", []))
