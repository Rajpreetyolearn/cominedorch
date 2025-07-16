"""
Analytics service for the Educational Tool Chatbot API
"""

from typing import Dict, Any

class AnalyticsService:
    """Service for managing API analytics and request counting"""
    
    def __init__(self):
        self.request_count = 0
        self.successful_queries = 0
        self.failed_queries = 0
    
    def increment_request_count(self):
        """Increment the total request count"""
        self.request_count += 1
    
    def increment_successful_queries(self):
        """Increment successful queries count"""
        self.successful_queries += 1
    
    def increment_failed_queries(self):
        """Increment failed queries count"""
        self.failed_queries += 1
    
    def get_analytics(self, knowledge_base, memory_service) -> Dict[str, Any]:
        """Get analytics data"""
        memory_stats = {}
        if memory_service:
            try:
                memory_stats = memory_service.get_memory_stats()
            except Exception as e:
                memory_stats = {"error": str(e)}
        
        return {
            "total_requests": self.request_count,
            "successful_queries": self.successful_queries,
            "failed_queries": self.failed_queries,
            "success_rate": (self.successful_queries / self.request_count * 100) if self.request_count > 0 else 0,
            "total_tools": len(knowledge_base.get_all_tools()),
            "categories": len(knowledge_base.get_categories()),
            "memory_service": memory_stats
        }
    
    def reset_analytics(self):
        """Reset all analytics counters"""
        self.request_count = 0
        self.successful_queries = 0
        self.failed_queries = 0 