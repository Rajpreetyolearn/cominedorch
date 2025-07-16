"""
Main FastAPI Application for Educational Tool Chatbot
Uses organized architecture with separated concerns
"""

import os
import uvicorn
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from core.config import settings
from core.components import set_components
from services.knowledge_base import EducationalToolKnowledgeBase
from services.intent_classifier import IntentClassifier
from services.memory_service import EducationalMemoryService
from services.analytics import AnalyticsService
from exceptions.handlers import http_exception_handler, general_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from models.schemas import (
    QueryRequest, 
    ToolRecommendation, 
    ChatResponse, 
    HealthResponse,
    UserPreferencesRequest
)
from api.endpoints import (
    get_root_endpoint,
    get_chat_instructions,
    chat_endpoint,
    get_all_tools,
    get_categories,
    get_tools_by_category,
    health_check,
    get_analytics,
    get_user_insights,
    get_user_context_endpoint,
    clear_user_memory,
    update_user_preferences
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    # Validate settings
    settings.validate_settings()
    
    # Initialize components
    knowledge_base = EducationalToolKnowledgeBase()
    intent_classifier = IntentClassifier(settings.OPENAI_API_KEY)
    memory_service = EducationalMemoryService(settings.OPENAI_API_KEY)
    analytics_service = AnalyticsService()
    
    # Set components in the components module
    set_components(knowledge_base, intent_classifier, memory_service, analytics_service)
    
    logger.info("Educational Tool Chatbot with Memory started successfully")
    
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("Educational Tool Chatbot shutting down")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Add exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    return app



# Create the FastAPI app
app = create_app()

# API Endpoints
@app.get("/")
async def root():
    """Serve a simple HTML interface for testing"""
    return get_root_endpoint()

@app.get("/chat")
async def chat_instructions():
    """Get chat endpoint usage instructions"""
    return get_chat_instructions()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: QueryRequest):
    """Main chat endpoint that processes user queries and returns tool recommendations"""
    return await chat_endpoint(request)

@app.get("/tools", response_model=List[ToolRecommendation])
async def get_tools():
    """Get all available educational tools"""
    return await get_all_tools()

@app.get("/categories")
async def get_tool_categories():
    """Get all available tool categories"""
    return await get_categories()

@app.get("/tools/category/{category}", response_model=List[ToolRecommendation])
async def get_tools_by_category_endpoint(category: str):
    """Get tools by specific category"""
    return await get_tools_by_category(category)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return await health_check()

@app.get("/analytics")
async def analytics():
    """Get basic analytics about API usage"""
    return await get_analytics()

@app.get("/memory/insights/{user_id}")
async def get_insights(user_id: str):
    """Get insights about a user's teaching patterns"""
    return await get_user_insights(user_id)

@app.get("/memory/context/{user_id}")
async def get_context(user_id: str, query: str = ""):
    """Get user context for a specific query"""
    return await get_user_context_endpoint(user_id, query)

@app.delete("/memory/clear/{user_id}")
async def clear_memory(user_id: str):
    """Clear all memory for a specific user"""
    return await clear_user_memory(user_id)

@app.post("/memory/preferences/{user_id}")
async def update_preferences(user_id: str, request: UserPreferencesRequest):
    """Update user preferences"""
    return await update_user_preferences(user_id, request)

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    ) 