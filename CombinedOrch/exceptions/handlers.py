"""
Exception handlers for the Educational Tool Chatbot API
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with custom error responses"""
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Endpoint not found",
                "message": f"The requested endpoint '{request.url.path}' does not exist",
                "available_endpoints": {
                    "GET /": "Web interface for testing",
                    "POST /chat": "Main chatbot endpoint", 
                    "GET /chat": "Usage instructions for chat endpoint",
                    "GET /health": "Health check",
                    "GET /tools": "List all educational tools",
                    "GET /categories": "List tool categories",
                    "GET /analytics": "Usage analytics"
                },
                "tip": "💡 Try GET / for the web interface or POST /chat for API access"
            }
        )
    elif exc.status_code == 405:
        return JSONResponse(
            status_code=405,
            content={
                "error": "Method not allowed",
                "message": f"The method {request.method} is not allowed for '{request.url.path}'",
                "suggestion": "Use GET /chat for usage instructions or POST /chat to send a query",
                "example": {
                    "correct_usage": "POST /chat with JSON body: {'query': 'your question here'}",
                    "curl_example": 'curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d \'{"query": "help me with lesson planning"}\''
                },
                "tip": "💡 Visit http://localhost:8000 for an easy-to-use web interface!"
            }
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "tip": "💡 Try again or contact support if the issue persists"
        }
    ) 