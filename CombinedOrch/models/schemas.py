"""
Pydantic models for the Educational Tool Chatbot API
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: Optional[int] = None

class ToolRecommendation(BaseModel):
    name: str
    description: str
    url: str

class ChatResponse(BaseModel):
    response_text: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    components: Dict[str, str]

class UserPreferencesRequest(BaseModel):
    preferences: Dict[str, Any] 