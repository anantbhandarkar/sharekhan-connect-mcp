"""
MCP Tools for Sharekhan Trading API
Defines all available tools for AI agents
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field

from .client import SharekhanClient
from .session import SharekhanSessionManager


# Pydantic models for tool inputs
class OrderInput(BaseModel):
    """Input model for placing orders"""

    exchange: str = Field(..., description="Exchange name (NSE, BSE)")
    scrip_code: str = Field(..., description="Security code")
    quantity: int = Field(..., description="Order quantity")
    price: Optional[float] = Field(
        None, description="Order price (None for market orders)"
    )
    transaction_type: str = Field(..., description="BUY or SELL")
    order_type: str = Field(..., description="MARKET, LIMIT, SL, SL-M")
    product: str = Field(..., description="NRML, MIS, CNC")
    validity: str = Field("DAY", description="Order validity (DAY, IOC)")
    customer_id: str = Field("12345", description="Customer ID")


class HoldingsInput(BaseModel):
    """Input model for getting holdings"""

    customer_id: str = Field("12345", description="Customer ID")


class HistoricalDataInput(BaseModel):
    """Input model for historical data"""

    exchange: str = Field(..., description="Exchange name")
    scrip_code: str = Field(..., description="Security code")
    interval: str = Field(..., description="Time interval (1minute, 5minute, day)")
    from_date: str = Field(..., description="From date (YYYY-MM-DD)")
    to_date: str = Field(..., description="To date (YYYY-MM-DD)")


class QuoteInput(BaseModel):
    """Input model for market quotes"""

    exchange: str = Field(..., description="Exchange name")
    scrip_code: str = Field(..., description="Security code")


class ModifyOrderInput(BaseModel):
    """Input model for modifying orders"""

    order_id: str = Field(..., description="Order ID to modify")
    price: Optional[float] = Field(None, description="New price")
    quantity: Optional[int] = Field(None, description="New quantity")
    order_type: Optional[str] = Field(None, description="New order type")


class SharekhanMCPTools:
    """MCP Tools for Sharekhan trading operations"""

    def __init__(
        self, client: SharekhanClient, session_manager: SharekhanSessionManager
    ):
        self.client = client
        self.session_manager = session_manager

    def _ensure_authenticated(self) -> bool:
        """Ensure client is authenticated before making API calls"""
        if not self.session_manager.is_token_valid():
            logger.error("Client not authenticated")
            return False
        return True

    async def place_order(self, input_data: OrderInput) -> Dict[str, Any]:
        """Place a new order"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            order_params = {
                "exchange": input_data.exchange,
                "scrip_code": input_data.scrip_code,
                "quantity": input_data.quantity,
                "transaction_type": input_data.transaction_type,
                "order_type": input_data.order_type,
                "product": input_data.product,
                "validity": input_data.validity,
                "customer_id": input_data.customer_id,
            }

            if input_data.price:
                order_params["price"] = input_data.price

            result = self.client.place_order(order_params)
            logger.info(f"Order placed: {result}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return {"status": "error", "message": str(e)}

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            result = self.client.cancel_order(order_id)
            logger.info(f"Order cancelled: {result}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return {"status": "error", "message": str(e)}

    async def modify_order(self, input_data: ModifyOrderInput) -> Dict[str, Any]:
        """Modify an existing order"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            modify_params = {}
            if input_data.price:
                modify_params["price"] = input_data.price
            if input_data.quantity:
                modify_params["quantity"] = input_data.quantity
            if input_data.order_type:
                modify_params["order_type"] = str(input_data.order_type)  # type: ignore

            result = self.client.modify_order(input_data.order_id, modify_params)
            logger.info(f"Order modified: {result}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Failed to modify order: {e}")
            return {"status": "error", "message": str(e)}

    async def get_holdings(self, input_data: HoldingsInput) -> Dict[str, Any]:
        """Get customer holdings"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            holdings = self.client.holdings(input_data.customer_id)
            logger.info(f"Retrieved {len(holdings)} holdings")
            return {"status": "success", "data": holdings}

        except Exception as e:
            logger.error(f"Failed to get holdings: {e}")
            return {"status": "error", "message": str(e)}

    async def get_positions(self, customer_id: str = "12345") -> Dict[str, Any]:
        """Get customer positions"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            positions = self.client.positions(customer_id)
            logger.info(f"Retrieved positions for customer {customer_id}")
            return {"status": "success", "data": positions}

        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            return {"status": "error", "message": str(e)}

    async def get_orders(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get order book"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            orders = self.client.orders(customer_id)
            logger.info(f"Retrieved {len(orders)} orders")
            return {"status": "success", "data": orders}

        except Exception as e:
            logger.error(f"Failed to get orders: {e}")
            return {"status": "error", "message": str(e)}

    async def get_trades(self, customer_id: str = "12345") -> Dict[str, Any]:
        """Get trade history"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            trades = self.client.trades(customer_id)
            logger.info(f"Retrieved {len(trades)} trades")
            return {"status": "success", "data": trades}

        except Exception as e:
            logger.error(f"Failed to get trades: {e}")
            return {"status": "error", "message": str(e)}

    async def get_historical_data(
        self, input_data: HistoricalDataInput
    ) -> Dict[str, Any]:
        """Get historical market data"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            from_date = datetime.strptime(input_data.from_date, "%Y-%m-%d")
            to_date = datetime.strptime(input_data.to_date, "%Y-%m-%d")

            data = self.client.historical_data(
                input_data.exchange,
                input_data.scrip_code,
                input_data.interval,
                from_date,
                to_date,
            )
            logger.info(f"Retrieved {len(data)} historical data points")
            return {"status": "success", "data": data}

        except Exception as e:
            logger.error(f"Failed to get historical data: {e}")
            return {"status": "error", "message": str(e)}

    async def get_quote(self, input_data: QuoteInput) -> Dict[str, Any]:
        """Get market quote"""
        try:
            if not self._ensure_authenticated():
                return {"status": "error", "message": "Authentication required"}

            quote = self.client.quote(input_data.exchange, input_data.scrip_code)
            logger.info(f"Retrieved quote for {input_data.scrip_code}")
            return {"status": "success", "data": quote}

        except Exception as e:
            logger.error(f"Failed to get quote: {e}")
            return {"status": "error", "message": str(e)}

    async def authenticate(
        self, request_token: str, customer_id: str = "12345"
    ) -> Dict[str, Any]:
        """Authenticate with Sharekhan using request token"""
        try:
            success = self.session_manager.authenticate(request_token, customer_id)
            if success:
                return {"status": "success", "message": "Authentication successful"}
            else:
                return {"status": "error", "message": "Authentication failed"}

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {"status": "error", "message": str(e)}

    async def get_login_url(self) -> Dict[str, Any]:
        """Get login URL for Sharekhan authentication"""
        try:
            login_url = self.client.get_login_url()
            return {"status": "success", "data": {"login_url": login_url}}

        except Exception as e:
            logger.error(f"Failed to get login URL: {e}")
            return {"status": "error", "message": str(e)}
