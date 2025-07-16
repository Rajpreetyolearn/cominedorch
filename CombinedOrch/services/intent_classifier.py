"""
Intent Classification System for Educational Tool Chatbot
Uses OpenAI GPT-4 for semantic understanding and intent classification
"""

import openai
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from services.knowledge_base import EducationalToolKnowledgeBase


@dataclass
class IntentResult:
    """Represents the result of intent classification"""
    primary_tools: List[Dict[str, Any]]
    secondary_tools: List[Dict[str, Any]]
    confidence_score: float
    reasoning: str
    query_type: str
    suggested_response: str


class IntentClassifier:
    def __init__(self, openai_api_key: str):
        """Initialize the intent classifier with OpenAI API key"""
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.knowledge_base = EducationalToolKnowledgeBase()
        
        # Define query types for classification
        self.query_types = {
            "SPECIFIC_TOOL": "User wants a specific educational tool",
            "GENERAL_PLANNING": "User needs help with educational planning",
            "CONTENT_CREATION": "User wants to create educational content",
            "ASSESSMENT": "User needs assessment or evaluation tools",
            "VISUAL_CONTENT": "User wants visual or graphic content",
            "COMMUNICATION": "User needs communication tools",
            "UNCLEAR": "User query is ambiguous or unclear"
        }
    
    def classify_intent(self, user_query: str, user_context: Optional[Dict[str, Any]] = None) -> IntentResult:
        """
        Main method to classify user intent and return appropriate tools
        """
        # Step 1: Basic preprocessing
        cleaned_query = self._preprocess_query(user_query)
        
        # Step 2: Use OpenAI for semantic understanding (with context)
        semantic_analysis = self._analyze_with_openai(cleaned_query, user_context)
        
        # Step 3: Find matching tools
        primary_tools, secondary_tools = self._find_matching_tools(semantic_analysis, cleaned_query)
        
        # Step 4: Calculate confidence score
        confidence_score = self._calculate_confidence(semantic_analysis, primary_tools, secondary_tools)
        
        # Step 5: Generate response (with context)
        suggested_response = self._generate_response(primary_tools, secondary_tools, semantic_analysis, user_context)
        
        return IntentResult(
            primary_tools=primary_tools,
            secondary_tools=secondary_tools,
            confidence_score=confidence_score,
            reasoning=semantic_analysis.get('reasoning', ''),
            query_type=semantic_analysis.get('query_type', 'UNCLEAR'),
            suggested_response=suggested_response
        )
    
    def _preprocess_query(self, query: str) -> str:
        """Clean and preprocess the user query"""
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Convert to lowercase for processing
        query = query.lower()
        
        # Remove special characters but keep essential punctuation
        query = re.sub(r'[^\w\s\-\?\!\.]', '', query)
        
        return query
    
    def _analyze_with_openai(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Use OpenAI to analyze the semantic meaning of the query with human-like understanding"""
        
        # Build context information if available
        context_info = ""
        if user_context and user_context.get('has_context'):
            context_info = f"""
            
        IMPORTANT: This teacher has previous interactions with you. Consider their history:
        - Previous queries: {user_context.get('previous_queries', [])}
        - Frequently used categories: {user_context.get('frequent_categories', [])}
        - Recently used tools: {user_context.get('recent_tools', [])}
        - Teaching patterns: {user_context.get('teaching_patterns', [])}
        
        Use this context to provide more personalized and relevant recommendations. If they've used certain tools before, consider suggesting similar or complementary tools. If they have patterns in their teaching style, tailor your recommendations accordingly.
            """
        
        # Create a comprehensive prompt for intelligent analysis
        analysis_prompt = f"""
        You are a world-class AI assistant specialized in education, similar to ChatGPT or Claude. A teacher has asked you this question:
        
        "{query}"
        {context_info}
        
        Your goal is to understand their need and provide analysis that will lead to clear, helpful, and empathetic responses. Think like the best AI assistants:
        
        - Be direct and clear, not overly wordy
        - Show empathy and understanding of teaching challenges
        - Focus on practical solutions that save time and effort
        - Use natural, conversational language
        - Acknowledge the teacher's expertise and dedication
        
        Available educational tool categories:
        - Planning: Curriculum planning, lesson planning, goal setting, calendar creation, academic scheduling
        - Content Creation: Worksheets, homework, assignments, creative materials, flashcards, study guides
        - Assessment: Quizzes, tests, evaluations, exit tickets, polls, rubrics, grading tools
        - Visual Content: Graphics, posters, charts, comics, concept visuals, diagrams
        - Communication: Messages, reports, notifications, coordination, parent communication
        - Interactive Content: Drag-drop activities, interactive exercises, matching games
        - Language Learning: Pronunciation, language-specific tools, phonetic guidance
        - Professional Development: Reflection, improvement tools, self-assessment
        
        Analyze their request with the understanding that:
        - Teachers are busy and need efficient solutions
        - They want tools that actually work and save time
        - They care deeply about student success
        - They appreciate both practical guidance and emotional support
        
        Provide your analysis in this JSON format:
        {{
            "query_type": "SPECIFIC_TOOL|GENERAL_PLANNING|CONTENT_CREATION|ASSESSMENT|VISUAL_CONTENT|COMMUNICATION|UNCLEAR",
            "intent_keywords": ["practical_keyword1", "relevant_keyword2", "useful_keyword3"],
            "primary_categories": ["most_relevant_category1", "secondary_relevant_category2"],
            "secondary_categories": ["alternative_category3"],
            "confidence_level": 0.85,
            "reasoning": "Clear, empathetic explanation of what the teacher needs and why, focusing on practical benefits and understanding their situation",
            "specific_tools_mentioned": ["any_specific_tools_if_mentioned"],
            "educational_context": "Practical context about their teaching situation, challenges they face, and what would help them most",
            "suggested_tool_types": ["most_helpful_tool_type1", "alternative_tool_type2"],
            "human_insight": "What would be most helpful for this teacher right now, considering their workload and student needs",
            "implied_needs": ["practical_need1", "time_saving_solution2"],
            "personalization_note": "How this fits with their teaching style and previous requests" if user_context and user_context.get('has_context') else "First interaction - focus on immediate practical help"
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful, empathetic AI assistant specialized in education. You communicate clearly and directly, similar to ChatGPT or Claude. You understand that teachers are dedicated professionals who need practical solutions. Your analysis should lead to responses that are supportive, actionable, and respectful of their expertise. Focus on being genuinely helpful rather than overly enthusiastic."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the JSON response
            analysis_text = response.choices[0].message.content
            # Extract JSON from the response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            else:
                return self._fallback_analysis(query)
                
        except Exception as e:
            print(f"OpenAI analysis error: {e}")
            return self._fallback_analysis(query)
    
    def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Human-like fallback analysis when OpenAI fails - using conversational, direct language"""
        # Enhanced keyword-based analysis with natural language understanding
        intent_keywords = []
        query_type = "UNCLEAR"
        primary_categories = []
        educational_context = "General teaching support needed"
        human_insight = "Let me help you find the right tool for your teaching needs."
        implied_needs = []
        
        # More natural keyword matching with context
        planning_keywords = ["plan", "curriculum", "lesson", "schedule", "organize", "calendar", "timeline", "structure", "prepare"]
        assessment_keywords = ["quiz", "test", "assessment", "evaluate", "grade", "measure", "check", "exam", "review", "feedback"]
        content_keywords = ["create", "generate", "make", "build", "develop", "design", "produce", "write", "worksheet", "assignment"]
        visual_keywords = ["visual", "graphic", "chart", "poster", "image", "diagram", "illustration", "picture", "display"]
        communication_keywords = ["message", "email", "report", "communicate", "send", "notify", "inform", "parent", "contact"]
        interactive_keywords = ["interactive", "activity", "game", "engagement", "hands-on", "drag", "drop", "fun", "engaging"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in planning_keywords):
            query_type = "GENERAL_PLANNING"
            primary_categories = ["Planning"]
            intent_keywords = ["planning", "organization", "preparation"]
            educational_context = "You're looking to get organized and plan your teaching more effectively"
            human_insight = "Planning is key to great teaching! Let's find tools that'll make this easier for you."
            implied_needs = ["time management", "organization tools", "structure"]
            
        elif any(keyword in query_lower for keyword in assessment_keywords):
            query_type = "ASSESSMENT"
            primary_categories = ["Assessment"]
            intent_keywords = ["assessment", "evaluation", "grading"]
            educational_context = "You need ways to assess and track your students' progress"
            human_insight = "Assessment helps you understand how your students are doing. I'll help you find the right tools."
            implied_needs = ["grading efficiency", "progress tracking", "feedback tools"]
            
        elif any(keyword in query_lower for keyword in content_keywords):
            query_type = "CONTENT_CREATION"
            primary_categories = ["Content Creation"]
            intent_keywords = ["creation", "materials", "resources"]
            educational_context = "You want to create engaging materials for your students"
            human_insight = "Creating great content takes time, but the right tools can make it much faster and easier."
            implied_needs = ["templates", "design resources", "time-saving tools"]
            
        elif any(keyword in query_lower for keyword in visual_keywords):
            query_type = "VISUAL_CONTENT"
            primary_categories = ["Visual Content"]
            intent_keywords = ["visual", "graphics", "design"]
            educational_context = "You're looking to create visual materials that'll help your students learn better"
            human_insight = "Visual content really helps students understand concepts! Great thinking."
            implied_needs = ["design templates", "visual resources", "easy-to-use tools"]
            
        elif any(keyword in query_lower for keyword in communication_keywords):
            query_type = "COMMUNICATION"
            primary_categories = ["Communication"]
            intent_keywords = ["communication", "messaging", "outreach"]
            educational_context = "You need to communicate effectively with students, parents, or colleagues"
            human_insight = "Good communication makes everything run smoother. Let's find tools that help."
            implied_needs = ["message templates", "communication efficiency", "professional tools"]
            
        elif any(keyword in query_lower for keyword in interactive_keywords):
            query_type = "CONTENT_CREATION"
            primary_categories = ["Interactive Content", "Content Creation"]
            intent_keywords = ["interactive", "engagement", "activities"]
            educational_context = "You want to create interactive experiences that keep students engaged"
            human_insight = "Interactive content is fantastic for keeping students engaged! You're on the right track."
            implied_needs = ["activity templates", "engagement tools", "interactive resources"]
        
        # Handle common teaching challenges with empathy
        if any(word in query_lower for word in ["boring", "bored", "not engaged", "disengaged", "uninterested"]):
            educational_context = "You're dealing with student engagement challenges - that's tough but very common"
            human_insight = "Student engagement is one of the biggest challenges teachers face. You're not alone in this!"
            implied_needs = ["engagement strategies", "interactive tools", "motivational resources"]
            
        elif any(word in query_lower for word in ["overwhelmed", "stressed", "too much", "no time"]):
            educational_context = "You're feeling overwhelmed with your teaching workload"
            human_insight = "Teaching can be overwhelming, but the right tools can really help lighten the load."
            implied_needs = ["time-saving tools", "efficiency solutions", "organization help"]
        
        return {
            "query_type": query_type,
            "intent_keywords": intent_keywords,
            "primary_categories": primary_categories,
            "secondary_categories": [],
            "confidence_level": 0.7,
            "reasoning": f"I understand you're looking for help with {query_type.lower().replace('_', ' ')}. While I'd love to provide more detailed analysis, I can still help you find the right tools.",
            "specific_tools_mentioned": [],
            "educational_context": educational_context,
            "suggested_tool_types": primary_categories,
            "human_insight": human_insight,
            "implied_needs": implied_needs
        }
    
    def _find_matching_tools(self, semantic_analysis: Dict[str, Any], query: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Find tools that match the semantic analysis"""
        primary_tools = []
        secondary_tools = []
        
        # Get all tools from knowledge base
        all_tools = self.knowledge_base.get_all_tools()
        
        # Check for specific tool mentions first
        specific_tools = semantic_analysis.get('specific_tools_mentioned', [])
        for tool_key in specific_tools:
            tool = self.knowledge_base.get_tool_by_key(tool_key)
            if tool:
                primary_tools.append(tool)
        
        # Match by primary categories
        primary_categories = semantic_analysis.get('primary_categories', [])
        for category in primary_categories:
            category_tools = self.knowledge_base.get_tools_by_category(category)
            for tool in category_tools:
                if tool not in primary_tools:
                    # Check if tool keywords match intent keywords
                    intent_keywords = semantic_analysis.get('intent_keywords', [])
                    tool_keywords = tool.get('keywords', [])
                    
                    if any(intent_keyword in ' '.join(tool_keywords).lower() for intent_keyword in intent_keywords):
                        primary_tools.append(tool)
                    else:
                        secondary_tools.append(tool)
        
        # Match by secondary categories
        secondary_categories = semantic_analysis.get('secondary_categories', [])
        for category in secondary_categories:
            category_tools = self.knowledge_base.get_tools_by_category(category)
            for tool in category_tools:
                if tool not in primary_tools and tool not in secondary_tools:
                    secondary_tools.append(tool)
        
        # If no primary tools found, promote best secondary tools
        if not primary_tools and secondary_tools:
            primary_tools = secondary_tools[:2]  # Take top 2
            secondary_tools = secondary_tools[2:]
        
        # Limit results
        primary_tools = primary_tools[:3]
        secondary_tools = secondary_tools[:3]
        
        return primary_tools, secondary_tools
    
    def _calculate_confidence(self, semantic_analysis: Dict[str, Any], primary_tools: List[Dict[str, Any]], secondary_tools: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for the classification"""
        base_confidence = semantic_analysis.get('confidence_level', 0.5)
        
        # Adjust confidence based on results
        if primary_tools:
            if len(primary_tools) == 1:
                base_confidence += 0.2  # High confidence for single clear match
            elif len(primary_tools) <= 3:
                base_confidence += 0.1  # Good confidence for few matches
        else:
            base_confidence -= 0.3  # Lower confidence if no primary tools
        
        if secondary_tools:
            base_confidence += 0.05  # Slight boost for having alternatives
        
        # Ensure confidence is within bounds
        return max(0.0, min(1.0, base_confidence))
    
    def _generate_response(self, primary_tools: List[Dict[str, Any]], secondary_tools: List[Dict[str, Any]], semantic_analysis: Dict[str, Any], user_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate clear, human-like responses similar to top LLMs"""
        
        if not primary_tools and not secondary_tools:
            return "I'd love to help you find the perfect tool! Could you tell me a bit more about what you're trying to accomplish in your classroom? The more specific you can be, the better I can assist you."
        
        import random
        
        # Get user context for personalization
        has_history = user_context and user_context.get('has_context')
        recent_queries = user_context.get('previous_queries', []) if has_history else []
        
        # Generate responses with better structure and clarity
        response_styles = [
            self._generate_clear_helpful_response,
            self._generate_supportive_response,
            self._generate_practical_direct_response,
            self._generate_encouraging_response
        ]
        
        # Choose a random response style for variety
        response_generator = random.choice(response_styles)
        return response_generator(primary_tools, secondary_tools, semantic_analysis, user_context, recent_queries)
    
    def _generate_clear_helpful_response(self, primary_tools, secondary_tools, semantic_analysis, user_context, recent_queries):
        """Generate a clear, helpful response with direct guidance"""
        import random
        
        response = ""
        
        # More varied personalized openings if user has history
        if recent_queries:
            context_openings = [
                f"Great! I see you've been working on {recent_queries[0].lower()}. Here's what I'd recommend next:",
                f"Perfect timing! Since you've been focusing on {recent_queries[0].lower()}, this will complement that work nicely:",
                f"Building on your recent work with {recent_queries[0].lower()}, here's exactly what you need:",
                f"I noticed you've been exploring {recent_queries[0].lower()}. This next tool will fit perfectly:",
                f"Since you're already working on {recent_queries[0].lower()}, let's add this to your toolkit:",
                f"Following up on your {recent_queries[0].lower()} work, here's a great next step:"
            ]
            response += random.choice(context_openings) + "\n\n"
        else:
            # More varied friendly, direct openings
            openings = [
                "I've got just the thing for you!",
                "Here's what I'd recommend:",
                "I think this will be perfect for what you need:",
                "Let me help you with this:",
                "Here's exactly what you're looking for:",
                "I found the perfect tool for your situation:",
                "This should be exactly what you need:",
                "Let me point you in the right direction:"
            ]
            response += random.choice(openings) + "\n\n"
        
        # Main recommendation with clear benefits and better formatting
        if primary_tools:
            tool = primary_tools[0]
            response += f"**{tool['name']}** - {tool['description']}\n"
            response += f"👉 [Get started here]({tool['url']})\n\n"
            
            # Add context-specific benefits with more variety
            context = semantic_analysis.get('educational_context', '')
            if context and len(context) > 30:
                benefit_intros = [
                    "This will be especially helpful because",
                    "Perfect for your situation since",
                    "This works great when",
                    "You'll find this particularly useful because"
                ]
                response += f"{random.choice(benefit_intros)} {context.lower()[:100]}.\n\n"
        
        # More varied clear, encouraging closings
        closings = [
            "Try it out and let me know how it works for you!",
            "Give it a try - I think you'll find it really helpful!",
            "Hope this makes your teaching life a bit easier!",
            "Let me know if you need help with anything else!",
            "I'd love to hear how this works out for you!",
            "Feel free to ask if you need more suggestions!",
            "Hope this is exactly what you were looking for!",
            "Let me know if you want to explore more options!"
        ]
        response += random.choice(closings)
        
        return response
    
    def _generate_supportive_response(self, primary_tools, secondary_tools, semantic_analysis, user_context, recent_queries):
        """Generate an empathetic, supportive response"""
        import random
        
        response = ""
        
        # More varied empathetic openings
        if recent_queries:
            supportive_openings = [
                f"I can see you've been putting a lot of thought into {recent_queries[0].lower()}. Here's something that should help:",
                f"You're doing great work with {recent_queries[0].lower()}! This next step will build on that perfectly:",
                f"Since you've been working on {recent_queries[0].lower()}, I think you'll really appreciate this tool:",
                f"I love seeing your dedication to {recent_queries[0].lower()}. Here's what I'd suggest next:",
                f"You're making real progress with {recent_queries[0].lower()}. This will take it even further:",
                f"Building on your thoughtful work with {recent_queries[0].lower()}, here's a perfect addition:",
                f"Your focus on {recent_queries[0].lower()} shows you really care about your students. Here's what I recommend:"
            ]
            response += random.choice(supportive_openings) + "\n\n"
        else:
            # Acknowledge the challenge or show understanding
            context = semantic_analysis.get('educational_context', '')
            if any(word in context.lower() for word in ['challenge', 'difficult', 'hard', 'struggle', 'overwhelmed', 'stressed']):
                understanding_starts = [
                    "I understand this can be challenging. Let me help you find something that'll make it easier:",
                    "Teaching challenges are part of the job, but you don't have to face them alone. Here's what can help:",
                    "I can see this is something you're working through. Let me suggest a tool that should help:",
                    "These kinds of challenges are what make teaching both difficult and rewarding. Here's support:",
                    "You're tackling something important here. Let me help you find the right solution:"
                ]
                response += random.choice(understanding_starts) + "\n\n"
            else:
                supportive_starts = [
                    "Teaching is such important work, and I'm here to help make it easier:",
                    "I know how much you care about your students. Here's a tool that can help:",
                    "You're looking for ways to improve your teaching - I love that! Here's what I suggest:",
                    "Your dedication to your students really shows. Here's something that'll support your work:",
                    "I can tell you're a thoughtful teacher. Here's a tool that matches your approach:",
                    "You're always thinking about how to do better for your students. Here's what I recommend:",
                    "Your commitment to excellence is inspiring. Let me help you with this:"
                ]
                response += random.choice(supportive_starts) + "\n\n"
        
        # Main tool with more varied encouraging language
        if primary_tools:
            tool = primary_tools[0]
            encouraging_intros = [
                f"The **{tool['name']}** is designed exactly for situations like yours.",
                f"I think you'll find the **{tool['name']}** really helpful.",
                f"The **{tool['name']}** should make this much easier for you.",
                f"Many teachers love the **{tool['name']}** for this exact reason.",
                f"The **{tool['name']}** is perfect for what you're trying to accomplish.",
                f"I've seen great results when teachers use the **{tool['name']}** for this.",
                f"The **{tool['name']}** will be a game-changer for your situation.",
                f"You'll appreciate how the **{tool['name']}** simplifies this process."
            ]
            response += f"{random.choice(encouraging_intros)} {tool['description']}\n\n"
            response += f"🔗 [Start using it here]({tool['url']})\n\n"
        
        # More varied supportive closings
        supportive_closings = [
            "You're doing amazing work. Remember, every small step makes a difference for your students!",
            "Keep up the great work - your students are lucky to have someone who cares so much!",
            "You're making a real difference in your students' lives. I'm here if you need more help!",
            "Your dedication to your students is inspiring. Feel free to reach out anytime!",
            "You're on the right track. Teaching is challenging, but you're handling it beautifully!",
            "Remember, you're doing important work. Every effort you make matters to your students!",
            "You've got this! Your thoughtful approach to teaching really shows.",
            "Keep being the amazing teacher you are. Your students benefit from your care every day!"
        ]
        response += random.choice(supportive_closings)
        
        return response
    
    def _generate_practical_direct_response(self, primary_tools, secondary_tools, semantic_analysis, user_context, recent_queries):
        """Generate a practical, no-nonsense response"""
        import random
        
        response = ""
        
        # More varied direct, practical openings
        if recent_queries:
            practical_openings = [
                f"Following up on your {recent_queries[0].lower()} work, here's what you need:",
                f"To build on your {recent_queries[0].lower()}, I'd go with this:",
                f"Since you've been working on {recent_queries[0].lower()}, this is the logical next step:",
                f"Based on your {recent_queries[0].lower()} focus, here's the best tool:",
                f"Continuing your {recent_queries[0].lower()} work, this will be perfect:",
                f"For your {recent_queries[0].lower()} needs, here's the most efficient solution:"
            ]
            response += random.choice(practical_openings) + "\n\n"
        else:
            direct_starts = [
                "Here's exactly what you need:",
                "The best tool for this is:",
                "I'd recommend this approach:",
                "This will solve your problem:",
                "Here's the most efficient solution:",
                "This is your best option:",
                "The quickest way to handle this:",
                "Here's what will work best:"
            ]
            response += random.choice(direct_starts) + "\n\n"
        
        # Main recommendation - clear and direct with more variety
        if primary_tools:
            tool = primary_tools[0]
            response += f"**{tool['name']}**\n"
            response += f"What it does: {tool['description']}\n"
            response += f"Access it: {tool['url']}\n\n"
            
            # More varied practical benefits
            practical_benefits = [
                "Why this works: It's specifically designed for your situation and will save you time.",
                "The advantage: It's built for exactly what you need and streamlines the process.",
                "Why it's effective: It handles this task efficiently and gets results quickly.",
                "The benefit: It's designed to solve this specific problem and save you effort.",
                "Why I recommend it: It's proven to work well for this exact situation.",
                "The key: It's tailored for your needs and eliminates the guesswork."
            ]
            response += f"{random.choice(practical_benefits)}\n\n"
        
        # More varied practical closings
        practical_closings = [
            "That should get you sorted. Let me know if you need anything else!",
            "This should handle what you need. Feel free to ask if you want more options!",
            "That's the most direct solution. Reach out if you need additional help!",
            "This will get the job done efficiently. Let me know how it works!",
            "That should solve your problem quickly. Ask if you need more suggestions!",
            "This is your most straightforward option. Happy to help with anything else!"
        ]
        response += random.choice(practical_closings)
        
        return response
    
    def _generate_encouraging_response(self, primary_tools, secondary_tools, semantic_analysis, user_context, recent_queries):
        """Generate an encouraging, motivational response"""
        import random
        
        response = ""
        
        # More varied encouraging openings
        if recent_queries:
            encouraging_openings = [
                f"I love seeing your dedication to {recent_queries[0].lower()}! Here's what will take it to the next level:",
                f"You're building something great with your {recent_queries[0].lower()} work. This will be the perfect addition:",
                f"Your focus on {recent_queries[0].lower()} shows real commitment to your students. Here's what I'd add:",
                f"The progress you're making with {recent_queries[0].lower()} is impressive! Here's what comes next:",
                f"Your thoughtful approach to {recent_queries[0].lower()} is exactly what great teachers do. Here's more support:",
                f"I can see how much care you're putting into {recent_queries[0].lower()}. This will amplify that effort:",
                f"Your students are so lucky to have someone focused on {recent_queries[0].lower()} like you are. Here's what I suggest:"
            ]
            response += random.choice(encouraging_openings) + "\n\n"
        else:
            motivational_starts = [
                "You're taking all the right steps to improve your teaching!",
                "I can tell you really care about giving your students the best experience.",
                "This is exactly the kind of thinking that makes great teachers!",
                "Your students are lucky to have someone who thinks this way!",
                "Your commitment to excellence really shows in everything you do.",
                "I love seeing teachers who are always looking for ways to improve!",
                "You're approaching this with exactly the right mindset.",
                "This kind of dedication is what makes teaching so impactful!"
            ]
            response += f"{random.choice(motivational_starts)} Here's what I recommend:\n\n"
        
        # Main tool with more varied positive framing
        if primary_tools:
            tool = primary_tools[0]
            positive_intros = [
                f"The **{tool['name']}** is going to be a game-changer for you.",
                f"You'll love how the **{tool['name']}** streamlines this process.",
                f"The **{tool['name']}** is exactly what innovative teachers like you need.",
                f"I'm excited for you to try the **{tool['name']}** - it's going to make such a difference!",
                f"The **{tool['name']}** will transform how you handle this.",
                f"You're going to see amazing results with the **{tool['name']}**.",
                f"The **{tool['name']}** is perfect for teachers who care about quality like you do.",
                f"I can already imagine how much the **{tool['name']}** will help your students!"
            ]
            response += f"{random.choice(positive_intros)} {tool['description']}\n\n"
            response += f"🚀 [Start creating amazing results]({tool['url']})\n\n"
        
        # More varied motivational closings
        motivational_closings = [
            "Your students are going to benefit so much from your thoughtful approach!",
            "Keep up the fantastic work - you're making a real difference!",
            "I can't wait to hear about the positive impact this has on your classroom!",
            "You're doing incredible work. Your dedication shows in everything you do!",
            "Your students are so fortunate to have a teacher who cares this much!",
            "The effort you put in really makes a difference - keep being amazing!",
            "You're creating such a positive impact on your students' lives!",
            "Your passion for teaching is inspiring. Keep up the excellent work!"
        ]
        response += random.choice(motivational_closings)
        
        return response


# Example usage and testing
if __name__ == "__main__":
    # Initialize classifier (API key would be loaded from environment)
    classifier = IntentClassifier("your-openai-api-key")
    
    # Test queries
    test_queries = [
        "I need to create a lesson plan for my math class",
        "Help me generate quiz questions for history",
        "I want to make visual content for my students",
        "Create homework assignments",
        "I need to send a message to parents"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = classifier.classify_intent(query)
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Primary tools: {len(result.primary_tools)}")
        print(f"Response: {result.suggested_response[:100]}...") 