"""
Component management for the Educational Tool Chatbot
"""

# Global variables for components
knowledge_base = None
intent_classifier = None
memory_service = None
analytics_service = None

def get_components():
    """Get initialized components"""
    return {
        "knowledge_base": knowledge_base,
        "intent_classifier": intent_classifier,
        "memory_service": memory_service,
        "analytics_service": analytics_service
    }

def set_components(kb, ic, ms, as_service):
    """Set the initialized components"""
    global knowledge_base, intent_classifier, memory_service, analytics_service
    knowledge_base = kb
    intent_classifier = ic
    memory_service = ms
    analytics_service = as_service 