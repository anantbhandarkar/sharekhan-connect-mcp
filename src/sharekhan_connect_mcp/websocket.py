"""
Sharekhan WebSocket Client
Handles live market data feeds and real-time updates
"""

import asyncio
import json
import websockets
from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
from loguru import logger
import threading
import time

class SharekhanWebSocketClient:
    """Sharekhan WebSocket client for live market data"""

    def __init__(self, access_token: str, ws_url: str = "wss://api.sharekhan.com/v1/stream/websocket"):
        self.access_token = access_token
        self.ws_url = ws_url
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5

        # Subscription management
        self.subscriptions: Dict[str, Dict[str, Any]] = {}
        self.callback_handlers: Dict[str, List[Callable]] = {
            "ticks": [],
            "quotes": [],
            "orders": [],
            "trades": [],
            "errors": []
        }

        # Thread management
        self.ws_thread: Optional[threading.Thread] = None
        self.should_run = False

    def add_callback(self, event_type: str, callback: Callable):
        """Add callback for specific event types"""
        if event_type in self.callback_handlers:
            self.callback_handlers[event_type].append(callback)
            logger.info(f"Added callback for {event_type}")
        else:
            logger.warning(f"Unknown event type: {event_type}")

    def remove_callback(self, event_type: str, callback: Callable):
        """Remove callback for specific event types"""
        if event_type in self.callback_handlers and callback in self.callback_handlers[event_type]:
            self.callback_handlers[event_type].remove(callback)
            logger.info(f"Removed callback for {event_type}")

    async def connect(self) -> bool:
        """Connect to Sharekhan WebSocket"""
        try:
            logger.info(f"Connecting to Sharekhan WebSocket: {self.ws_url}")

            # Prepare connection headers
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": "Sharekhan-MCP-Server/1.0.0"
            }

            self.websocket = await websockets.connect(
                self.ws_url,
                extra_headers=headers,
                ping_interval=30,
                ping_timeout=10
            )

            self.is_connected = True
            self.reconnect_attempts = 0

            logger.info("Connected to Sharekhan WebSocket successfully")

            # Send initial subscription requests
            await self._resubscribe_all()

            # Start message listener
            asyncio.create_task(self._message_listener())

            return True

        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            self.is_connected = False
            return False

    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.should_run = False
        self.is_connected = False

        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("Disconnected from WebSocket")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")

        if self.ws_thread and self.ws_thread.is_alive():
            self.ws_thread.join(timeout=5)

    async def _message_listener(self):
        """Listen for WebSocket messages"""
        try:
            while self.is_connected and self.websocket:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=30)
                    await self._handle_message(message)

                except asyncio.TimeoutError:
                    # Send ping to keep connection alive
                    if self.websocket:
                        await self.websocket.ping()
                    continue

                except websockets.exceptions.ConnectionClosed:
                    logger.warning("WebSocket connection closed")
                    break

                except Exception as e:
                    logger.error(f"Error in message listener: {e}")
                    await self._trigger_error_callbacks(e)
                    break

        except Exception as e:
            logger.error(f"Message listener error: {e}")

        # Attempt reconnection
        if self.should_run:
            await self._attempt_reconnect()

    async def _handle_message(self, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type", "unknown")

            logger.debug(f"Received WebSocket message: {message_type}")

            if message_type == "tick":
                await self._trigger_tick_callbacks(data)
            elif message_type == "quote":
                await self._trigger_quote_callbacks(data)
            elif message_type == "order":
                await self._trigger_order_callbacks(data)
            elif message_type == "trade":
                await self._trigger_trade_callbacks(data)
            elif message_type == "error":
                logger.error(f"WebSocket error: {data}")
                await self._trigger_error_callbacks(data)
            elif message_type == "ping":
                # Respond to server ping
                await self.send_message({"type": "pong"})
            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode WebSocket message: {e}")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")

    async def _trigger_tick_callbacks(self, data: Dict[str, Any]):
        """Trigger tick data callbacks"""
        for callback in self.callback_handlers["ticks"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error in tick callback: {e}")

    async def _trigger_quote_callbacks(self, data: Dict[str, Any]):
        """Trigger quote callbacks"""
        for callback in self.callback_handlers["quotes"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error in quote callback: {e}")

    async def _trigger_order_callbacks(self, data: Dict[str, Any]):
        """Trigger order update callbacks"""
        for callback in self.callback_handlers["orders"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error in order callback: {e}")

    async def _trigger_trade_callbacks(self, data: Dict[str, Any]):
        """Trigger trade update callbacks"""
        for callback in self.callback_handlers["trades"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error in trade callback: {e}")

    async def _trigger_error_callbacks(self, error: Any):
        """Trigger error callbacks"""
        for callback in self.callback_handlers["errors"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(error)
                else:
                    callback(error)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")

    async def send_message(self, message: Dict[str, Any]):
        """Send message to WebSocket"""
        if self.websocket and self.is_connected:
            try:
                await self.websocket.send(json.dumps(message))
                logger.debug(f"Sent WebSocket message: {message.get('type')}")
            except Exception as e:
                logger.error(f"Failed to send WebSocket message: {e}")
        else:
            logger.warning("WebSocket not connected, cannot send message")

    async def subscribe(self, token_list: Dict[str, Any]) -> str:
        """Subscribe to market data (matches SharekhanConnect API)"""
        if not self.is_connected:
            logger.warning("WebSocket not connected, subscription queued")
            # Store subscription for later
            subscription_id = f"subscription_{len(self.subscriptions)}"
            self.subscriptions[subscription_id] = token_list
            return subscription_id

        subscription_id = f"subscription_{len(self.subscriptions)}"
        self.subscriptions[subscription_id] = token_list

        # Send subscription message in Sharekhan format
        await self.send_message(token_list)
        logger.info(f"Subscribed to {token_list.get('key', 'unknown')} for {len(token_list.get('value', []))} instruments")
        return subscription_id

    async def fetchData(self, feed_data: Dict[str, Any]) -> None:
        """Fetch depth data (matches SharekhanConnect API)"""
        if not self.is_connected:
            logger.warning("WebSocket not connected, cannot fetch data")
            return

        await self.send_message(feed_data)
        logger.info(f"Fetching data for {feed_data.get('key', 'unknown')}")

    async def unsubscribe(self, unsubscribefeed: Dict[str, Any]) -> None:
        """Unsubscribe from market data (matches SharekhanConnect API)"""
        if not self.is_connected:
            logger.warning("WebSocket not connected, cannot unsubscribe")
            return

        await self.send_message(unsubscribefeed)
        logger.info(f"Unsubscribed from {unsubscribefeed.get('key', 'unknown')}")

    async def subscribe_legacy(self, subscription_type: str, instruments: List[str], params: Optional[Dict] = None):
        """Subscribe to market data (legacy method)"""
        token_list = {
            "action": "subscribe",
            "key": [subscription_type],
            "value": instruments
        }
        return await self.subscribe(token_list)

    async def unsubscribe_legacy(self, subscription_id: str):
        """Unsubscribe from market data (legacy method)"""
        if subscription_id in self.subscriptions:
            message = {
                "action": "unsubscribe",
                "subscription_id": subscription_id
            }

            await self.send_message(message)
            del self.subscriptions[subscription_id]
            logger.info(f"Unsubscribed from {subscription_id}")

    def close_connection(self):
        """Close WebSocket connection (matches SharekhanConnect API)"""
        asyncio.create_task(self.disconnect())

    async def _resubscribe_all(self):
        """Resubscribe to all previous subscriptions"""
        for subscription_id, subscription_data in self.subscriptions.items():
            message = {
                "type": "subscribe",
                "subscription_id": subscription_id,
                "data": subscription_data
            }
            await self.send_message(message)
            logger.info(f"Resubscribed to {subscription_id}")

    async def _attempt_reconnect(self):
        """Attempt to reconnect to WebSocket"""
        while self.reconnect_attempts < self.max_reconnect_attempts and self.should_run:
            self.reconnect_attempts += 1
            logger.info(f"Attempting reconnection {self.reconnect_attempts}/{self.max_reconnect_attempts}")

            await asyncio.sleep(self.reconnect_delay)

            if await self.connect():
                logger.info("WebSocket reconnected successfully")
                return

        logger.error(f"Failed to reconnect after {self.max_reconnect_attempts} attempts")

    def start(self):
        """Start WebSocket connection in background thread"""
        self.should_run = True

        def run_websocket():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(self.connect())
                loop.run_forever()
            except Exception as e:
                logger.error(f"WebSocket thread error: {e}")
            finally:
                loop.close()

        self.ws_thread = threading.Thread(target=run_websocket, daemon=True)
        self.ws_thread.start()
        logger.info("WebSocket background thread started")

    def stop(self):
        """Stop WebSocket connection"""
        self.should_run = False
        logger.info("Stopping WebSocket client")
