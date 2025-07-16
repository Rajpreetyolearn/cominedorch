"""
Memory Service for Educational Tool Chatbot
Integrates with mem0 to store user interactions and provide contextual recommendations
"""

import os
from mem0 import MemoryClient
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class EducationalMemoryService:
    def __init__(self, openai_api_key: str):
        """Initialize the memory service with mem0 Platform (managed service)"""
        
        self.openai_api_key = openai_api_key
        
        # Initialize mem0 Platform client
        try:
            mem0_api_key = os.getenv("MEM0_API_KEY")
            if not mem0_api_key:
                raise ValueError("MEM0_API_KEY environment variable is required for mem0 Platform")
            
            # Use mem0 Platform managed service
            self.memory = MemoryClient(api_key=mem0_api_key)
            self.using_platform = True
            logger.info("Memory service initialized successfully with mem0 Platform")
        except Exception as e:
            logger.warning(f"Failed to initialize mem0 Platform: {e}")
            # Fallback to a simple in-memory dictionary for basic functionality
            self.memory = None
            self.using_platform = False
            self.fallback_memory = {}
            logger.info("Using fallback memory storage")
    
    def _should_store_memory(self, user_id: str, query: str, response: Dict[str, Any], 
                            context: Optional[Dict[str, Any]] = None) -> tuple[bool, str]:
        """Determine if this interaction should be stored in memory"""
        
        # Criteria for storing memory
        store_reasons = []
        
        # 1. User preferences and constraints (high value)
        preference_indicators = [
            "i prefer", "i like", "i don't like", "i hate", "i avoid",
            "i always", "i never", "my students", "my class", "my teaching style",
            "i teach", "grade level", "subject area", "curriculum"
        ]
        
        if any(indicator in query.lower() for indicator in preference_indicators):
            store_reasons.append("user_preferences")
        
        # 2. Feedback on recommendations (high value)
        feedback_indicators = [
            "this worked well", "this didn't work", "perfect", "exactly what i needed",
            "not helpful", "great suggestion", "love this tool", "hate this tool",
            "better than", "worse than", "prefer this over"
        ]
        
        if any(indicator in query.lower() for indicator in feedback_indicators):
            store_reasons.append("tool_feedback")
        
        # 3. Recurring patterns or specific needs (medium value)
        pattern_indicators = [
            "again", "similar to", "like before", "as usual", "typically",
            "my usual", "my go-to", "i often", "frequently", "regularly"
        ]
        
        if any(indicator in query.lower() for indicator in pattern_indicators):
            store_reasons.append("usage_pattern")
        
        # 4. Context that reveals teaching style (medium value)
        style_indicators = [
            "interactive", "hands-on", "visual", "creative", "traditional",
            "project-based", "collaborative", "individual", "group work",
            "assessment focused", "creative assignments"
        ]
        
        if any(indicator in query.lower() for indicator in style_indicators):
            store_reasons.append("teaching_style")
        
        # 5. Subject-specific or grade-specific information (medium value)
        subject_indicators = [
            "math", "science", "english", "history", "art", "music",
            "elementary", "middle school", "high school", "kindergarten",
            "1st grade", "2nd grade", "3rd grade", "4th grade", "5th grade"
        ]
        
        if any(indicator in query.lower() for indicator in subject_indicators):
            store_reasons.append("subject_context")
        
        # 6. Skip generic/routine queries first
        generic_queries = [
            "hello", "hi", "help", "what can you do", "how are you",
            "test", "testing", "check", "status", "help me", "what tools do you have",
            "what tools", "show me tools", "list tools"
        ]
        
        if query.lower().strip() in generic_queries:
            return False, "generic_query"
        
        # 7. Skip very short queries without context
        if len(query.split()) < 3 and not store_reasons:
            return False, "too_short"
        
        # 8. Low confidence responses (store to learn from) - only if not generic
        if response.get("confidence_score", 1.0) < 0.7 and len(query.split()) >= 5:
            store_reasons.append("low_confidence")
        
        # Decision logic
        if store_reasons:
            return True, f"storing_for: {', '.join(store_reasons)}"
        else:
            return False, "no_personalization_value"
    
    def _extract_personalization_info(self, query: str, response: Dict[str, Any], 
                                    context: Optional[Dict[str, Any]] = None) -> str:
        """Extract the key personalization information from an interaction"""
        
        # Focus on information that helps with future personalization
        personalization_parts = []
        
        # Extract user preferences and constraints
        if any(word in query.lower() for word in ["prefer", "like", "don't like", "avoid", "always", "never"]):
            personalization_parts.append(f"User preference: {query}")
        
        # Extract teaching context
        if any(word in query.lower() for word in ["teach", "grade", "subject", "class", "students"]):
            personalization_parts.append(f"Teaching context: {query}")
        
        # Extract tool feedback
        if any(word in query.lower() for word in ["worked well", "didn't work", "perfect", "not helpful", "love", "hate"]):
            personalization_parts.append(f"Tool feedback: {query}")
        
        # Extract successful recommendations for future reference
        if response.get("confidence_score", 0) > 0.8:
            recommended_tools = [tool.get("name") for tool in response.get("recommendations", [])]
            if recommended_tools:
                personalization_parts.append(f"Successfully recommended: {', '.join(recommended_tools)} for {response.get('query_type', 'general')} needs")
        
        # Extract subject/grade information
        subjects = ["math", "science", "english", "history", "art", "music"]
        grades = ["elementary", "middle school", "high school", "kindergarten"]
        
        for subject in subjects:
            if subject in query.lower():
                personalization_parts.append(f"Subject focus: {subject}")
                break
        
        for grade in grades:
            if grade in query.lower():
                personalization_parts.append(f"Grade level: {grade}")
                break
        
        # If no specific personalization info found, store the essential context
        if not personalization_parts:
            personalization_parts.append(f"User asked about {response.get('query_type', 'general')} tools")
        
        return ". ".join(personalization_parts)

    def store_interaction(self, user_id: str, query: str, response: Dict[str, Any], 
                         context: Optional[Dict[str, Any]] = None):
        """Store a user interaction in memory only if it's valuable for personalization"""
        try:
            # Check if this interaction should be stored
            should_store, reason = self._should_store_memory(user_id, query, response, context)
            
            if not should_store:
                logger.info(f"Skipping memory storage for user {user_id}: {reason}")
                return True
            
            # Create a personalization-focused memory entry
            personalization_content = self._extract_personalization_info(query, response, context)
            
            if self.memory and self.using_platform:
                # Use mem0 Platform storage with personalization focus
                messages = [
                    {
                        "role": "user",
                        "content": personalization_content
                    }
                ]
                
                self.memory.add(
                    messages=messages,
                    user_id=user_id,
                    metadata={
                        "type": "personalization",
                        "timestamp": datetime.now().isoformat(),
                        "query_type": response.get("query_type", "unknown"),
                        "store_reason": reason,
                        "confidence_score": response.get("confidence_score", 0.0)
                    }
                )
            else:
                # Use fallback storage
                if user_id not in self.fallback_memory:
                    self.fallback_memory[user_id] = []
                self.fallback_memory[user_id].append({
                    "timestamp": datetime.now().isoformat(),
                    "personalization_content": personalization_content,
                    "query_type": response.get("query_type", "unknown"),
                    "store_reason": reason,
                    "confidence_score": response.get("confidence_score", 0.0)
                })
                
                # Keep only last 50 personalization entries per user
                if len(self.fallback_memory[user_id]) > 50:
                    self.fallback_memory[user_id] = self.fallback_memory[user_id][-50:]
            
            logger.info(f"Stored personalization memory for user {user_id}: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
            return False
    
    def get_user_context(self, user_id: str, current_query: str) -> Dict[str, Any]:
        """Retrieve relevant context for a user based on their history"""
        try:
            relevant_memories = []
            
            if self.memory and self.using_platform:
                # Use mem0 Platform search
                try:
                    # Create filters for mem0 Platform API
                    filters = {
                        "AND": [
                            {"user_id": user_id}
                        ]
                    }
                    
                    relevant_memories = self.memory.search(
                        query=current_query,
                        version="v2",
                        filters=filters,
                        limit=5
                    )
                except Exception as search_error:
                    logger.error(f"Error searching mem0 Platform: {search_error}")
                    relevant_memories = []
            else:
                # Use fallback memory
                if user_id in self.fallback_memory:
                    # Simple search - just get the last 5 interactions
                    relevant_memories = self.fallback_memory[user_id][-5:]
                    # Convert to expected format
                    relevant_memories = [{"metadata": memory} for memory in relevant_memories]
            
            if not relevant_memories:
                return {"has_context": False, "context": "No previous interactions found"}
            
            # Analyze the memories to extract context
            context_info = {
                "has_context": True,
                "previous_queries": [],
                "frequent_categories": [],
                "recent_tools": [],
                "teaching_patterns": []
            }
            
            logger.info(f"Retrieved context for user {user_id}: {len(relevant_memories)} memories")
            
            for memory in relevant_memories:
                # Handle mem0 Platform response format
                if self.using_platform:
                    # Platform returns personalization-focused content
                    memory_text = memory.get("memory", "") if isinstance(memory, dict) else str(memory)
                    
                    # Log the memory content for debugging
                    logger.debug(f"Processing memory: {memory_text[:100]}...")
                    
                    # Extract user preferences
                    if "User preference:" in memory_text:
                        pref_text = memory_text.split("User preference:")[1].split(".")[0].strip()
                        context_info["previous_queries"].append(pref_text)
                    
                    # Extract teaching context
                    if "Teaching context:" in memory_text:
                        context_text = memory_text.split("Teaching context:")[1].split(".")[0].strip()
                        context_info["previous_queries"].append(context_text)
                    
                    # Extract tool feedback
                    if "Tool feedback:" in memory_text:
                        feedback_text = memory_text.split("Tool feedback:")[1].split(".")[0].strip()
                        context_info["previous_queries"].append(feedback_text)
                    
                    # Extract successful recommendations
                    if "Successfully recommended:" in memory_text:
                        rec_text = memory_text.split("Successfully recommended:")[1].split(".")[0].strip()
                        tools = [tool.strip() for tool in rec_text.split("for")[0].split(",")]
                        context_info["recent_tools"].extend(tools)
                    
                    # Extract subject and grade information
                    if "Subject focus:" in memory_text:
                        subject = memory_text.split("Subject focus:")[1].split(".")[0].strip()
                        context_info["frequent_categories"].append(subject)
                    
                    if "Grade level:" in memory_text:
                        grade = memory_text.split("Grade level:")[1].split(".")[0].strip()
                        context_info["frequent_categories"].append(grade)
                    
                    # Also extract general context from the full memory text
                    if memory_text and not any(pattern in memory_text for pattern in ["User preference:", "Teaching context:", "Tool feedback:", "Successfully recommended:", "Subject focus:", "Grade level:"]):
                        # This is a general memory, add it to previous queries
                        context_info["previous_queries"].append(memory_text[:100])
                else:
                    # Fallback format with personalization content
                    metadata = memory.get("metadata", {})
                    
                    # Extract personalization content
                    if "personalization_content" in metadata:
                        content = metadata["personalization_content"]
                        context_info["previous_queries"].append(content)
                    
                    # Extract frequent categories
                    if "query_type" in metadata:
                        context_info["frequent_categories"].append(metadata["query_type"])
                    
                    # Extract store reason for understanding what was valuable
                    if "store_reason" in metadata:
                        reason = metadata["store_reason"]
                        if "user_preferences" in reason:
                            context_info["teaching_patterns"].append("Has expressed preferences")
                        if "tool_feedback" in reason:
                            context_info["teaching_patterns"].append("Provides feedback on tools")
                        if "subject_context" in reason:
                            context_info["teaching_patterns"].append("Subject-specific teacher")
            
            # Remove duplicates and get top items
            context_info["frequent_categories"] = list(set(context_info["frequent_categories"]))[:3]
            context_info["recent_tools"] = list(set(context_info["recent_tools"]))[:5]
            context_info["previous_queries"] = context_info["previous_queries"][:3]
            
            # Generate teaching patterns insight
            if context_info["frequent_categories"]:
                most_common = max(set(context_info["frequent_categories"]), 
                                key=context_info["frequent_categories"].count)
                context_info["teaching_patterns"] = [
                    f"Frequently asks about {most_common.lower()} related topics",
                    f"Has used {len(context_info['recent_tools'])} different tools recently"
                ]
            
            # Ensure has_context is True if we have any meaningful content
            has_meaningful_content = bool(
                context_info["previous_queries"] or 
                context_info["frequent_categories"] or 
                context_info["recent_tools"] or 
                context_info["teaching_patterns"]
            )
            
            context_info["has_context"] = has_meaningful_content
            
            logger.info(f"Retrieved context for user {user_id}: {len(relevant_memories)} memories, has_context: {has_meaningful_content}")
            logger.info(f"Context summary - queries: {len(context_info['previous_queries'])}, categories: {len(context_info['frequent_categories'])}, tools: {len(context_info['recent_tools'])}")
            
            return context_info
            
        except Exception as e:
            logger.error(f"Error retrieving user context: {e}")
            return {"has_context": False, "context": "Error retrieving context"}
    
    def get_personalized_recommendations(self, user_id: str, current_query: str, 
                                       base_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance recommendations based on user history"""
        try:
            context = self.get_user_context(user_id, current_query)
            
            if not context.get("has_context"):
                return base_recommendations
            
            # Get user's tool usage history
            recent_tools = context.get("recent_tools", [])
            frequent_categories = context.get("frequent_categories", [])
            
            # Score recommendations based on history
            scored_recommendations = []
            
            for tool in base_recommendations:
                score = 1.0  # Base score
                
                # Boost score if user has used this tool before
                if tool["name"] in recent_tools:
                    score += 0.3
                
                # Boost score if it's in user's frequent categories
                if tool["category"] in frequent_categories:
                    score += 0.2
                
                # Add personalization reason
                reasons = []
                if tool["name"] in recent_tools:
                    reasons.append("You've used this tool before")
                if tool["category"] in frequent_categories:
                    reasons.append(f"You frequently work with {tool['category'].lower()} tools")
                
                tool_copy = tool.copy()
                tool_copy["personalization_score"] = score
                tool_copy["personalization_reasons"] = reasons
                
                scored_recommendations.append(tool_copy)
            
            # Sort by personalization score
            scored_recommendations.sort(key=lambda x: x["personalization_score"], reverse=True)
            
            logger.info(f"Personalized {len(scored_recommendations)} recommendations for user {user_id}")
            return scored_recommendations
            
        except Exception as e:
            logger.error(f"Error personalizing recommendations: {e}")
            return base_recommendations
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user's teaching patterns"""
        try:
            all_memories = []
            
            if self.memory and self.using_platform:
                # Use mem0 Platform storage
                try:
                    # Create filters for mem0 Platform API
                    filters = {
                        "AND": [
                            {"user_id": user_id}
                        ]
                    }
                    
                    all_memories = self.memory.get_all(
                        version="v2",
                        filters=filters,
                        page_size=50
                    )
                except Exception as get_error:
                    logger.error(f"Error getting memories from mem0 Platform: {get_error}")
                    all_memories = []
            else:
                # Use fallback memory
                if user_id in self.fallback_memory:
                    all_memories = [{"metadata": memory} for memory in self.fallback_memory[user_id]]
            
            if not all_memories:
                return {"total_interactions": 0, "insights": "No interaction history available"}
            
            insights = {
                "total_interactions": len(all_memories),
                "most_common_category": "Unknown",
                "favorite_tools": [],
                "teaching_style": "Unknown",
                "activity_summary": f"You have {len(all_memories)} personalization memories stored",
                "user_preferences": [],
                "primary_subject": "Unknown",
                "grade_level": "Unknown",
                "personalization_focus": []
            }
            
            # Analyze patterns from personalization-focused memories
            categories = []
            tools = []
            preferences = []
            subjects = []
            grades = []
            store_reasons = []
            
            for memory in all_memories:
                if self.using_platform:
                    # Platform returns personalization-focused content
                    memory_text = memory.get("memory", "") if isinstance(memory, dict) else str(memory)
                    
                    # Extract user preferences
                    if "User preference:" in memory_text:
                        pref_text = memory_text.split("User preference:")[1].split(".")[0].strip()
                        preferences.append(pref_text)
                    
                    # Extract successful tool recommendations
                    if "Successfully recommended:" in memory_text:
                        rec_text = memory_text.split("Successfully recommended:")[1].split(".")[0].strip()
                        if " for " in rec_text:
                            tools_part = rec_text.split(" for ")[0].strip()
                            category_part = rec_text.split(" for ")[1].replace(" needs", "").strip()
                            extracted_tools = [tool.strip() for tool in tools_part.split(",")]
                            tools.extend(extracted_tools)
                            categories.append(category_part)
                    
                    # Extract subject and grade information
                    if "Subject focus:" in memory_text:
                        subject = memory_text.split("Subject focus:")[1].split(".")[0].strip()
                        subjects.append(subject)
                    
                    if "Grade level:" in memory_text:
                        grade = memory_text.split("Grade level:")[1].split(".")[0].strip()
                        grades.append(grade)
                    
                    # Extract general query types
                    if "User asked about" in memory_text:
                        query_type = memory_text.split("User asked about")[1].split("tools")[0].strip()
                        categories.append(query_type)
                else:
                    # Fallback format with personalization content
                    metadata = memory.get("metadata", {})
                    
                    if "query_type" in metadata:
                        categories.append(metadata["query_type"])
                    
                    if "store_reason" in metadata:
                        store_reasons.append(metadata["store_reason"])
                    
                    # Extract tools from personalization content
                    if "personalization_content" in metadata:
                        content = metadata["personalization_content"]
                        if "Successfully recommended:" in content:
                            rec_text = content.split("Successfully recommended:")[1].split(".")[0].strip()
                            if " for " in rec_text:
                                tools_part = rec_text.split(" for ")[0].strip()
                                extracted_tools = [tool.strip() for tool in tools_part.split(",")]
                                tools.extend(extracted_tools)
            
            # Process categories
            if categories:
                insights["most_common_category"] = max(set(categories), key=categories.count)
            
            # Process tools
            if tools:
                tool_counts = {}
                for tool in tools:
                    if tool:  # Skip empty tools
                        tool_counts[tool] = tool_counts.get(tool, 0) + 1
                insights["favorite_tools"] = sorted(tool_counts.items(), 
                                                  key=lambda x: x[1], reverse=True)[:3]
            
            # Process user preferences
            if preferences:
                insights["user_preferences"] = preferences[:3]  # Keep top 3 preferences
            
            # Process subjects and grades
            if subjects:
                insights["primary_subject"] = max(set(subjects), key=subjects.count)
            
            if grades:
                insights["grade_level"] = max(set(grades), key=grades.count)
            
            # Process personalization focus from store reasons
            focus_areas = []
            for reason in store_reasons:
                if "user_preferences" in reason:
                    focus_areas.append("Preference-based personalization")
                if "tool_feedback" in reason:
                    focus_areas.append("Tool feedback integration")
                if "subject_context" in reason:
                    focus_areas.append("Subject-specific customization")
                if "teaching_style" in reason:
                    focus_areas.append("Teaching style adaptation")
            
            if focus_areas:
                insights["personalization_focus"] = list(set(focus_areas))
            
            # Determine teaching style based on personalization data
            if insights["most_common_category"] == "CONTENT_CREATION":
                insights["teaching_style"] = "Content Creator - You love creating materials"
            elif insights["most_common_category"] == "ASSESSMENT":
                insights["teaching_style"] = "Assessment Focused - You prioritize evaluation"
            elif insights["most_common_category"] == "GENERAL_PLANNING":
                insights["teaching_style"] = "Strategic Planner - You focus on organization"
            elif len(preferences) > 0:
                insights["teaching_style"] = "Preference-Driven - You have clear teaching preferences"
            elif len(subjects) > 0:
                insights["teaching_style"] = f"Subject Specialist - Focused on {insights['primary_subject']}"
            else:
                insights["teaching_style"] = "Balanced Educator - You use varied approaches"
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting user insights: {e}")
            return {"total_interactions": 0, "insights": "Error retrieving insights"}
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences in memory"""
        try:
            preference_data = {
                "type": "preferences",
                "timestamp": datetime.now().isoformat(),
                "preferences": preferences
            }
            
            if self.memory:
                # Store preferences as a special message
                messages = [
                    {
                        "role": "system",
                        "content": f"User preferences updated: {json.dumps(preferences)}"
                    }
                ]
                
                self.memory.add(
                    messages=messages,
                    user_id=user_id,
                    metadata=preference_data
                )
            else:
                # Use fallback memory
                if user_id not in self.fallback_memory:
                    self.fallback_memory[user_id] = []
                self.fallback_memory[user_id].append(preference_data)
            
            logger.info(f"Updated preferences for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
    
    def clear_user_memory(self, user_id: str):
        """Clear all memory for a specific user"""
        try:
            if self.memory:
                # Use mem0 storage
                all_memories = self.memory.get_all(user_id=user_id)
                
                for memory in all_memories:
                    memory_id = memory.get("id")
                    if memory_id:
                        self.memory.delete(memory_id)
            else:
                # Use fallback memory
                if user_id in self.fallback_memory:
                    del self.fallback_memory[user_id]
            
            logger.info(f"Cleared memory for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error clearing user memory: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics"""
        try:
            if self.memory:
                return {
                    "status": "active",
                    "provider": "mem0",
                    "message": "Memory service is running with mem0 integration"
                }
            else:
                total_users = len(self.fallback_memory)
                total_interactions = sum(len(memories) for memories in self.fallback_memory.values())
                return {
                    "status": "active",
                    "provider": "fallback",
                    "total_users": total_users,
                    "total_interactions": total_interactions,
                    "message": "Memory service is running with fallback storage"
                }
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"status": "error", "message": str(e)}

# Example usage and testing
if __name__ == "__main__":
    # This would be used for testing
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        memory_service = EducationalMemoryService(api_key)
        
        # Test storing an interaction
        test_response = {
            "query_type": "CONTENT_CREATION",
            "confidence_score": 0.85,
            "recommendations": [{"name": "Quiz Generator"}],
            "alternative_tools": [{"name": "Worksheet Generator"}],
            "reasoning": "User needs assessment tools"
        }
        
        memory_service.store_interaction("test_user", "I need to create a quiz", test_response)
        
        # Test getting context
        context = memory_service.get_user_context("test_user", "I want to make homework")
        print("Context:", context)
        
        # Test insights
        insights = memory_service.get_user_insights("test_user")
        print("Insights:", insights)
        
        # Test memory stats
        stats = memory_service.get_memory_stats()
        print("Memory stats:", stats)
    else:
        print("Please set OPENAI_API_KEY environment variable") 