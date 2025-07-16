"""
API endpoints for the Educational Tool Chatbot
"""

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from datetime import datetime
import logging

from models.schemas import (
    QueryRequest, 
    ToolRecommendation, 
    ChatResponse, 
    HealthResponse,
    UserPreferencesRequest
)
from services.intent_classifier import IntentResult
from core.components import get_components

logger = logging.getLogger(__name__)

def get_root_endpoint():
    """Serve a simple HTML interface for testing"""
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

def get_chat_instructions():
    """Get chat endpoint usage instructions"""
    return {
        "message": "Use POST method to send queries to the chatbot",
        "usage": {
            "method": "POST",
            "url": "http://localhost:8000/chat",
            "headers": {
                "Content-Type": "application/json"
            },
            "body_example": {
                "query": "My students seem bored during class",
                "context": "5th grade math class (optional)",
                "user_id": "teacher_123 (optional)"
            }
        },
        "curl_example": 'curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d \'{"query": "I need help with lesson planning"}\'',
        "available_endpoints": {
            "POST /chat": "Main chatbot endpoint",
            "GET /": "Web interface for testing",
            "GET /health": "Health check",
            "GET /tools": "List all tools",
            "GET /categories": "List categories"
        },
        "tip": "💡 Use the web interface at http://localhost:8000 for easy testing!"
    }

async def chat_endpoint(request: QueryRequest) -> ChatResponse:
    """Main chat endpoint that processes user queries and returns tool recommendations"""
    components = get_components()
    knowledge_base = components["knowledge_base"]
    intent_classifier = components["intent_classifier"]
    memory_service = components["memory_service"]
    analytics_service = components["analytics_service"]
    
    analytics_service.increment_request_count()
    
    try:
        # Validate input
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Generate user ID if not provided
        user_id = request.user_id or f"anonymous_{request.timestamp or int(datetime.now().timestamp())}"
        
        # Log the request with timestamp for debugging
        timestamp_info = f" (timestamp: {request.timestamp})" if request.timestamp else ""
        logger.info(f"Processing query for user {user_id}: {request.query[:100]}...{timestamp_info}")
        
        # Get user context from memory
        user_context = None
        if memory_service:
            try:
                user_context = memory_service.get_user_context(user_id, request.query)
                logger.info(f"Retrieved context for user {user_id}: {user_context.get('has_context', False)}")
            except Exception as e:
                logger.warning(f"Failed to retrieve user context: {e}")
        
        # Classify intent and get recommendations (with context)
        intent_result: IntentResult = intent_classifier.classify_intent(request.query, user_context)
        
        # Convert tools to response format
        recommendations = []
        for tool in intent_result.primary_tools:
            recommendations.append(ToolRecommendation(
                name=tool["name"],
                description=tool["description"],
                url=tool["url"]
            ))
        
        # Personalize recommendations based on user history
        if memory_service and user_context and user_context.get('has_context'):
            try:
                personalized_recommendations = memory_service.get_personalized_recommendations(
                    user_id, request.query, [tool.model_dump() for tool in recommendations]
                )
                # Update recommendations with personalization
                for i, rec in enumerate(recommendations):
                    if i < len(personalized_recommendations):
                        if personalized_recommendations[i].get("personalization_reasons"):
                            rec.description += f" (Personalized: {', '.join(personalized_recommendations[i]['personalization_reasons'])})"
            except Exception as e:
                logger.warning(f"Failed to personalize recommendations: {e}")
        
        analytics_service.increment_successful_queries()
        
        response = ChatResponse(
            response_text=intent_result.suggested_response,
            timestamp=datetime.now().isoformat()
        )
        
        # Store interaction in memory
        if memory_service:
            try:
                memory_service.store_interaction(
                    user_id=user_id,
                    query=request.query,
                    response={
                        "query_type": intent_result.query_type,
                        "confidence_score": intent_result.confidence_score,
                        "recommendations": [tool.model_dump() for tool in recommendations],
                        "reasoning": intent_result.reasoning
                    },
                    context={"user_context": user_context}
                )
                logger.info(f"Stored interaction for user {user_id}")
            except Exception as e:
                logger.warning(f"Failed to store interaction: {e}")
        
        # Add cache-busting headers
        return JSONResponse(
            content=response.model_dump(),
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        analytics_service.increment_failed_queries()
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_all_tools() -> List[ToolRecommendation]:
    """Get all available educational tools"""
    components = get_components()
    knowledge_base = components["knowledge_base"]
    
    try:
        all_tools = knowledge_base.get_all_tools()
        tools_list = []
        
        for tool_data in all_tools.values():
            tools_list.append(ToolRecommendation(
                name=tool_data["name"],
                description=tool_data["description"],
                url=tool_data["url"],
                category=tool_data["category"],
                keywords=tool_data["keywords"],
                use_cases=tool_data["use_cases"]
            ))
        
        return tools_list
        
    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tools: {str(e)}")

async def get_categories():
    """Get all available tool categories"""
    components = get_components()
    knowledge_base = components["knowledge_base"]
    
    try:
        categories = knowledge_base.get_categories()
        category_counts = {}
        
        for category in categories:
            tools = knowledge_base.get_tools_by_category(category)
            category_counts[category] = len(tools)
        
        return {
            "categories": category_counts,
            "total_tools": len(knowledge_base.get_all_tools())
        }
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

async def get_tools_by_category(category: str) -> List[ToolRecommendation]:
    """Get tools by specific category"""
    components = get_components()
    knowledge_base = components["knowledge_base"]
    
    try:
        tools = knowledge_base.get_tools_by_category(category)
        if not tools:
            raise HTTPException(status_code=404, detail=f"No tools found for category: {category}")
        
        tools_list = []
        for tool_data in tools:
            tools_list.append(ToolRecommendation(
                name=tool_data["name"],
                description=tool_data["description"],
                url=tool_data["url"],
                category=tool_data["category"],
                keywords=tool_data["keywords"],
                use_cases=tool_data["use_cases"]
            ))
        
        return tools_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tools by category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tools: {str(e)}")

async def health_check() -> HealthResponse:
    """Health check endpoint"""
    import os
    components = get_components()
    knowledge_base = components["knowledge_base"]
    intent_classifier = components["intent_classifier"]
    memory_service = components["memory_service"]
    
    components_status = {
        "knowledge_base": "healthy" if knowledge_base else "unhealthy",
        "intent_classifier": "healthy" if intent_classifier else "unhealthy",
        "memory_service": "healthy" if memory_service else "unhealthy",
        "openai_api": "healthy" if os.getenv("OPENAI_API_KEY") else "unhealthy"
    }
    
    overall_status = "healthy" if all(status == "healthy" for status in components_status.values()) else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now().isoformat(),
        components=components_status
    )

async def get_analytics():
    """Get basic analytics about API usage"""
    components = get_components()
    knowledge_base = components["knowledge_base"]
    memory_service = components["memory_service"]
    analytics_service = components["analytics_service"]
    
    return analytics_service.get_analytics(knowledge_base, memory_service)

async def get_user_insights(user_id: str):
    """Get insights about a user's teaching patterns"""
    components = get_components()
    memory_service = components["memory_service"]
    
    if not memory_service:
        raise HTTPException(status_code=503, detail="Memory service not available")
    
    try:
        insights = memory_service.get_user_insights(user_id)
        return {
            "user_id": user_id,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting user insights: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving insights: {str(e)}")

async def get_user_context_endpoint(user_id: str, query: str = ""):
    """Get user context for a specific query"""
    components = get_components()
    memory_service = components["memory_service"]
    
    if not memory_service:
        raise HTTPException(status_code=503, detail="Memory service not available")
    
    try:
        context = memory_service.get_user_context(user_id, query)
        return {
            "user_id": user_id,
            "query": query,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting user context: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {str(e)}")

async def clear_user_memory(user_id: str):
    """Clear all memory for a specific user"""
    components = get_components()
    memory_service = components["memory_service"]
    
    if not memory_service:
        raise HTTPException(status_code=503, detail="Memory service not available")
    
    try:
        memory_service.clear_user_memory(user_id)
        return {
            "message": f"Memory cleared for user {user_id}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing user memory: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

async def update_user_preferences(user_id: str, request: UserPreferencesRequest):
    """Update user preferences"""
    components = get_components()
    memory_service = components["memory_service"]
    
    if not memory_service:
        raise HTTPException(status_code=503, detail="Memory service not available")
    
    try:
        memory_service.update_user_preferences(user_id, request.preferences)
        return {
            "message": f"Preferences updated for user {user_id}",
            "preferences": request.preferences,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating preferences: {str(e)}") 