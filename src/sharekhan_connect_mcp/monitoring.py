"""
Monitoring Module
Performance and health monitoring for Sharekhan MCP Server
"""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import psutil
from loguru import logger


@dataclass
class RequestMetrics:
    """Request metrics data class"""

    endpoint: str
    method: str
    status_code: int
    response_time: float
    timestamp: datetime
    user_id: Optional[str] = None
    tool_name: Optional[str] = None


@dataclass
class SystemMetrics:
    """System metrics data class"""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    active_connections: int
    uptime_seconds: float


@dataclass
class APIHealthMetrics:
    """API health metrics"""

    api_endpoint: str
    status: str  # healthy, degraded, unhealthy
    response_time: float
    last_check: datetime
    consecutive_failures: int
    error_details: Optional[str] = None


class MetricsCollector:
    """Collects and stores metrics"""

    def __init__(self, max_history_size: int = 10000):
        self.max_history_size = max_history_size
        self.start_time = datetime.now()

        # Request metrics
        self.request_history: deque = deque(maxlen=max_history_size)
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)

        # Error tracking
        self.error_counts = defaultdict(int)
        self.error_history: deque = deque(maxlen=1000)

        # System metrics
        self.system_metrics_history: deque = deque(maxlen=1000)

        # API health metrics
        self.api_health: Dict[str, APIHealthMetrics] = {}

        # Tool usage metrics
        self.tool_usage_counts = defaultdict(int)
        self.tool_response_times = defaultdict(list)

    def record_request(self, metrics: RequestMetrics):
        """Record request metrics"""
        self.request_history.append(metrics)

        # Update counters
        endpoint_key = f"{metrics.method} {metrics.endpoint}"
        self.request_counts[endpoint_key] += 1
        self.response_times[endpoint_key].append(metrics.response_time)

        # Record tool usage if applicable
        if metrics.tool_name:
            self.tool_usage_counts[metrics.tool_name] += 1
            self.tool_response_times[metrics.tool_name].append(metrics.response_time)

    def record_error(self, error_type: str, error_details: Dict[str, Any]):
        """Record error metrics"""
        self.error_counts[error_type] += 1
        self.error_history.append(
            {
                "error_type": error_type,
                "details": error_details,
                "timestamp": datetime.now(),
            }
        )

    def record_system_metrics(self):
        """Record current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # Get network connections count (approximation)
        try:
            connections = len(psutil.net_connections())
        except:
            connections = 0

        metrics = SystemMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / 1024 / 1024,
            disk_usage_percent=disk.percent,
            active_connections=connections,
            uptime_seconds=(datetime.now() - self.start_time).total_seconds(),
        )

        self.system_metrics_history.append(metrics)

    def update_api_health(
        self,
        endpoint: str,
        is_healthy: bool,
        response_time: float,
        error_details: Optional[str] = None,
    ):
        """Update API health status"""
        current_health = self.api_health.get(endpoint)

        if is_healthy:
            # Reset failure count on success
            consecutive_failures = 0
            status = "healthy"
        else:
            # Increment failure count
            consecutive_failures = (
                (current_health.consecutive_failures + 1) if current_health else 1
            )

            # Determine status based on failure count
            if consecutive_failures <= 2:
                status = "degraded"
            else:
                status = "unhealthy"

        self.api_health[endpoint] = APIHealthMetrics(
            api_endpoint=endpoint,
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            consecutive_failures=consecutive_failures,
            error_details=error_details,
        )

    def get_summary_metrics(self, time_window_minutes: int = 5) -> Dict[str, Any]:
        """Get summary metrics for the specified time window"""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)

        # Filter recent requests
        recent_requests = [
            r for r in self.request_history if r.timestamp >= cutoff_time
        ]

        # Calculate request statistics
        total_requests = len(recent_requests)
        successful_requests = len(
            [r for r in recent_requests if 200 <= r.status_code < 400]
        )
        error_requests = total_requests - successful_requests

        # Calculate response time statistics
        response_times = [r.response_time for r in recent_requests]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0

        # Get system metrics
        recent_system_metrics = [
            m for m in self.system_metrics_history if m.timestamp >= cutoff_time
        ]
        latest_system = recent_system_metrics[-1] if recent_system_metrics else None

        # Calculate error statistics
        recent_errors = [e for e in self.error_history if e["timestamp"] >= cutoff_time]
        error_by_type = defaultdict(int)
        for error in recent_errors:
            error_by_type[error["error_type"]] += 1

        return {
            "time_window_minutes": time_window_minutes,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "request_metrics": {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "error_requests": error_requests,
                "success_rate": (
                    successful_requests / total_requests if total_requests > 0 else 0
                ),
                "requests_per_minute": (
                    total_requests / time_window_minutes
                    if time_window_minutes > 0
                    else 0
                ),
                "avg_response_time_ms": avg_response_time * 1000,
                "max_response_time_ms": max_response_time * 1000,
                "min_response_time_ms": min_response_time * 1000,
            },
            "system_metrics": {
                "cpu_percent": latest_system.cpu_percent if latest_system else 0,
                "memory_percent": latest_system.memory_percent if latest_system else 0,
                "memory_used_mb": latest_system.memory_used_mb if latest_system else 0,
                "disk_usage_percent": (
                    latest_system.disk_usage_percent if latest_system else 0
                ),
                "active_connections": (
                    latest_system.active_connections if latest_system else 0
                ),
            },
            "error_metrics": {
                "total_errors": len(recent_errors),
                "error_rate": (
                    len(recent_errors) / total_requests if total_requests > 0 else 0
                ),
                "errors_by_type": dict(error_by_type),
            },
            "tool_usage": dict(self.tool_usage_counts),
            "api_health": {
                endpoint: asdict(health) for endpoint, health in self.api_health.items()
            },
        }


class MonitoringService:
    """Main monitoring service"""

    def __init__(self, max_history_size: int = 10000):
        self.metrics_collector = MetricsCollector(max_history_size)
        self.system_monitor_task = None

    async def start(self):
        """Start monitoring services"""
        logger.info("Starting monitoring service")

        # Start system metrics collection
        self.system_monitor_task = asyncio.create_task(self._collect_system_metrics())

        logger.info("Monitoring service started")

    async def stop(self):
        """Stop monitoring services"""
        logger.info("Stopping monitoring service")

        # Cancel tasks
        if self.system_monitor_task:
            self.system_monitor_task.cancel()

        logger.info("Monitoring service stopped")

    async def _collect_system_metrics(self):
        """Collect system metrics periodically"""
        while True:
            try:
                self.metrics_collector.record_system_metrics()
                await asyncio.sleep(30)  # Collect every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"System metrics collection error: {e}")
                await asyncio.sleep(30)

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        summary = self.metrics_collector.get_summary_metrics()

        # Determine overall health
        overall_health = "healthy"
        issues = []

        # Check error rate
        if summary["error_metrics"]["error_rate"] > 0.1:  # 10% error rate
            overall_health = "degraded"
            issues.append(
                f"High error rate: {summary['error_metrics']['error_rate']:.2%}"
            )

        # Check response time
        if summary["request_metrics"]["avg_response_time_ms"] > 5000:  # 5 seconds
            overall_health = "degraded"
            issues.append(
                f"High response time: {summary['request_metrics']['avg_response_time_ms']:.0f}ms"
            )

        # Check system resources
        if summary["system_metrics"]["cpu_percent"] > 90:
            overall_health = "degraded"
            issues.append(
                f"High CPU usage: {summary['system_metrics']['cpu_percent']:.1f}%"
            )

        if summary["system_metrics"]["memory_percent"] > 90:
            overall_health = "degraded"
            issues.append(
                f"High memory usage: {summary['system_metrics']['memory_percent']:.1f}%"
            )

        return {
            "status": overall_health,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": summary["uptime_seconds"],
            "issues": issues,
            "summary": summary,
        }
