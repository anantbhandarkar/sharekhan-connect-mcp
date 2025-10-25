"""
Error Handler Module
Centralized error handling for Sharekhan MCP Server
"""

import traceback
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
from loguru import logger

class ErrorType(Enum):
    """Error types for categorization"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    WEBSOCKET_ERROR = "websocket_error"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    UNKNOWN = "unknown"

class SharekhanError(Exception):
    """Base class for Sharekhan MCP errors"""

    def __init__(
        self,
        message: str,
        error_type: ErrorType = ErrorType.UNKNOWN,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_type = error_type
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)

class AuthenticationError(SharekhanError):
    """Authentication related errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.AUTHENTICATION,
            error_code="AUTH_FAILED",
            details=details
        )

class AuthorizationError(SharekhanError):
    """Authorization related errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.AUTHORIZATION,
            error_code="ACCESS_DENIED",
            details=details
        )

class ValidationError(SharekhanError):
    """Input validation errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.VALIDATION,
            error_code="VALIDATION_FAILED",
            details=details
        )

class APIError(SharekhanError):
    """Sharekhan API errors"""

    def __init__(self, message: str, api_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.API_ERROR,
            error_code=api_code or "API_ERROR",
            details=details
        )

class RateLimitError(SharekhanError):
    """Rate limiting errors"""

    def __init__(self, message: str, retry_after: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        if details is None:
            details = {}
        if retry_after:
            details["retry_after"] = retry_after

        super().__init__(
            message=message,
            error_type=ErrorType.RATE_LIMIT,
            error_code="RATE_LIMITED",
            details=details
        )

class NetworkError(SharekhanError):
    """Network related errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.NETWORK_ERROR,
            error_code="NETWORK_ERROR",
            details=details
        )

class WebSocketError(SharekhanError):
    """WebSocket related errors"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.WEBSOCKET_ERROR,
            error_code="WEBSOCKET_ERROR",
            details=details
        )

class ErrorHandler:
    """Centralized error handler"""

    @staticmethod
    def handle_exception(exc: Exception, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle exceptions and return standardized error response

        Args:
            exc: The exception to handle
            context: Optional context where the error occurred

        Returns:
            Standardized error response dictionary
        """
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(exc)}"

        # Log the error
        logger.error(f"Error ID: {error_id}, Context: {context}, Exception: {str(exc)}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")

        # Determine error type and create response
        if isinstance(exc, SharekhanError):
            error_response = {
                "status": "error",
                "error_id": error_id,
                "error_type": exc.error_type.value,
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "timestamp": exc.timestamp.isoformat(),
                "context": context
            }
        else:
            error_response = {
                "status": "error",
                "error_id": error_id,
                "error_type": ErrorType.UNKNOWN.value,
                "error_code": "UNKNOWN_ERROR",
                "message": "An unexpected error occurred",
                "details": {
                    "original_error": str(exc),
                    "exception_type": type(exc).__name__
                },
                "timestamp": datetime.now().isoformat(),
                "context": context
            }

        return error_response

    @staticmethod
    def create_sharekhan_error(response_data: Dict[str, Any], context: Optional[str] = None) -> SharekhanError:
        """
        Create SharekhanError from API response

        Args:
            response_data: API response data
            context: Optional context

        Returns:
            SharekhanError instance
        """
        message = response_data.get("message", "Unknown API error")
        error_code = response_data.get("error_code")

        # Determine error type based on status code or error code
        status_code = response_data.get("status_code")

        if status_code == 401 or "unauthorized" in message.lower():
            return AuthenticationError(message, {"response": response_data, "context": context})
        elif status_code == 403 or "forbidden" in message.lower():
            return AuthorizationError(message, {"response": response_data, "context": context})
        elif status_code == 429 or "rate limit" in message.lower():
            retry_after = response_data.get("retry_after")
            return RateLimitError(message, retry_after, {"response": response_data, "context": context})
        elif status_code and status_code >= 500:
            return APIError(message, error_code, {"response": response_data, "context": context})
        else:
            return APIError(message, error_code, {"response": response_data, "context": context})

    @staticmethod
    def validate_input(data: Dict[str, Any], required_fields: list, context: str = "validation") -> None:
        """
        Validate input data against required fields

        Args:
            data: Input data to validate
            required_fields: List of required field names
            context: Context for validation

        Raises:
            ValidationError: If validation fails
        """
        missing_fields = []
        invalid_fields = []

        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
            elif data[field] is None or data[field] == "":
                invalid_fields.append(field)

        if missing_fields or invalid_fields:
            error_details = {
                "missing_fields": missing_fields,
                "invalid_fields": invalid_fields,
                "provided_fields": list(data.keys())
            }

            error_message = "Validation failed"
            if missing_fields:
                error_message += f". Missing fields: {', '.join(missing_fields)}"
            if invalid_fields:
                error_message += f". Invalid fields: {', '.join(invalid_fields)}"

            raise ValidationError(error_message, error_details)

    @staticmethod
    def wrap_api_call(func, *args, context: Optional[str] = None, **kwargs):
        """
        Wrap API calls with error handling

        Args:
            func: Function to call
            *args: Function arguments
            context: Optional context
            **kwargs: Function keyword arguments

        Returns:
            Function result or error response
        """
        try:
            return func(*args, **kwargs)
        except SharekhanError:
            # Re-raise Sharekhan errors as-is
            raise
        except ConnectionError as e:
            raise NetworkError(f"Network connection failed: {str(e)}", {"context": context})
        except TimeoutError as e:
            raise NetworkError(f"Request timed out: {str(e)}", {"context": context})
        except Exception as e:
            raise APIError(f"Unexpected API error: {str(e)}", details={"context": context, "exception_type": type(e).__name__})
