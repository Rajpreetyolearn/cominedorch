"""
Knowledge Base for Educational Tool URLs
Contains structured information about all 38 educational agents
"""

import json
from typing import Dict, List, Any

class EducationalToolKnowledgeBase:
    def __init__(self):
        self.tools = {
            "curriculum-plan-agent": {
                "url": "https://app.yolearn.ai/teacher/curriculum-plan-agent",
                "name": "Curriculum Planning Agent",
                "description": "Creates comprehensive curriculum plans and educational pathways for courses",
                "keywords": ["curriculum", "plan", "course", "syllabus", "educational pathway", "learning objectives"],
                "use_cases": ["course planning", "curriculum development", "educational structure", "learning progression"],
                "category": "Planning"
            },
            "classgoals-milestone-agent": {
                "url": "https://app.yolearn.ai/teacher/classgoals-milestone-agent",
                "name": "Class Goals & Milestones Agent",
                "description": "Sets learning goals and tracks educational milestones for students",
                "keywords": ["goals", "milestones", "objectives", "targets", "achievements", "progress"],
                "use_cases": ["goal setting", "milestone tracking", "progress monitoring", "achievement planning"],
                "category": "Assessment"
            },
            "teaching-agent": {
                "url": "https://app.yolearn.ai/teacher/teaching-agent",
                "name": "Teaching Calendar Agent",
                "description": "Creates and manages educational calendars, schedules, and time-based planning for teachers",
                "keywords": ["calendar", "schedule", "planning", "timeline", "events", "dates", "appointments", "time management"],
                "use_cases": ["calendar creation", "schedule planning", "event scheduling", "time management", "academic calendar", "class scheduling"],
                "category": "Planning"
            },
            "teacher-reflection-agent": {
                "url": "https://app.yolearn.ai/teacher/teacher-reflection-agent",
                "name": "Teacher Reflection Agent",
                "description": "Helps teachers reflect on their teaching practices and improve methodologies",
                "keywords": ["reflection", "self-assessment", "teaching improvement", "methodology", "practice review"],
                "use_cases": ["teaching reflection", "practice improvement", "self-evaluation", "professional development"],
                "category": "Professional Development"
            },
            "lesson-planner": {
                "url": "https://app.yolearn.ai/teacher/lesson-planner",
                "name": "Lesson Planner",
                "description": "Creates detailed lesson plans with activities, objectives, and timelines",
                "keywords": ["lesson", "plan", "activities", "objectives", "timeline", "structure"],
                "use_cases": ["lesson planning", "class preparation", "activity design", "educational structure"],
                "category": "Planning"
            },
            "quiz-generator": {
                "url": "https://app.yolearn.ai/teacher/quiz-generator",
                "name": "Quiz Generator",
                "description": "Generates quizzes and test questions for various subjects and difficulty levels",
                "keywords": ["quiz", "test", "questions", "assessment", "evaluation", "multiple choice"],
                "use_cases": ["quiz creation", "test preparation", "assessment design", "question generation"],
                "category": "Assessment"
            },
            "worksheet-generator": {
                "url": "https://app.yolearn.ai/teacher/worksheet-generator",
                "name": "Worksheet Generator",
                "description": "Creates educational worksheets and practice exercises for students",
                "keywords": ["worksheet", "exercises", "practice", "problems", "activities", "handouts"],
                "use_cases": ["worksheet creation", "practice exercises", "student activities", "skill building"],
                "category": "Content Creation"
            },
            "homework-generator": {
                "url": "https://app.yolearn.ai/teacher/homework-generator",
                "name": "Homework Generator",
                "description": "Generates homework assignments and take-home exercises",
                "keywords": ["homework", "assignment", "take-home", "practice", "reinforcement", "study"],
                "use_cases": ["homework creation", "assignment design", "practice reinforcement", "study materials"],
                "category": "Content Creation"
            },
            "assignment-generator": {
                "url": "https://app.yolearn.ai/teacher/assignment-generator",
                "name": "Assignment Generator",
                "description": "Creates various types of assignments and projects for students",
                "keywords": ["assignment", "project", "task", "work", "student work", "educational task"],
                "use_cases": ["assignment creation", "project design", "task development", "student work"],
                "category": "Content Creation"
            },
            "assessment-generator": {
                "url": "https://app.yolearn.ai/teacher/assessment-generator",
                "name": "Assessment Generator",
                "description": "Creates comprehensive assessments and evaluation tools",
                "keywords": ["assessment", "evaluation", "grading", "rubric", "measurement", "testing"],
                "use_cases": ["assessment creation", "evaluation design", "grading tools", "performance measurement"],
                "category": "Assessment"
            },
            "generate-message": {
                "url": "https://app.yolearn.ai/teacher/generate-message",
                "name": "Message Generator",
                "description": "Generates educational messages and communications for students and parents",
                "keywords": ["message", "communication", "announcement", "notification", "email", "parent"],
                "use_cases": ["parent communication", "student messages", "announcements", "educational communication"],
                "category": "Communication"
            },
            "report-principal": {
                "url": "https://app.yolearn.ai/teacher/report-principal",
                "name": "Principal Report Generator",
                "description": "Creates reports and summaries for school administrators and principals",
                "keywords": ["report", "principal", "administrator", "summary", "school", "administrative"],
                "use_cases": ["administrative reporting", "principal communication", "school reports", "administrative summaries"],
                "category": "Communication"
            },
            "notification-manager": {
                "url": "https://app.yolearn.ai/teacher/notification-manager",
                "name": "Notification Manager",
                "description": "Manages and creates various types of educational notifications",
                "keywords": ["notification", "alert", "reminder", "announcement", "communication", "inform"],
                "use_cases": ["notification creation", "alert management", "reminder systems", "information distribution"],
                "category": "Communication"
            },
            "co-teacher-coordination": {
                "url": "https://app.yolearn.ai/teacher/co-teacher-coordination",
                "name": "Co-Teacher Coordination",
                "description": "Facilitates coordination and collaboration between co-teachers",
                "keywords": ["co-teacher", "collaboration", "coordination", "teamwork", "partnership", "joint teaching"],
                "use_cases": ["teacher collaboration", "co-teaching coordination", "team teaching", "shared planning"],
                "category": "Communication"
            },
            "generate-exit-ticket": {
                "url": "https://app.yolearn.ai/teacher/generate-exit-ticket",
                "name": "Exit Ticket Generator",
                "description": "Creates exit tickets for quick lesson assessments and feedback",
                "keywords": ["exit ticket", "quick assessment", "lesson feedback", "closure", "review", "check"],
                "use_cases": ["lesson closure", "quick assessment", "student feedback", "understanding check"],
                "category": "Assessment"
            },
            "generate-concept-visual": {
                "url": "https://app.yolearn.ai/teacher/generate-concept-visual",
                "name": "Concept Visual Generator",
                "description": "Creates visual representations and diagrams for educational concepts",
                "keywords": ["visual", "diagram", "concept", "illustration", "graphic", "visual aid"],
                "use_cases": ["concept visualization", "educational diagrams", "visual learning", "graphic design"],
                "category": "Visual Content"
            },
            "generate-comic": {
                "url": "https://app.yolearn.ai/teacher/generate-comic",
                "name": "Comic Generator",
                "description": "Creates educational comics and story-based learning materials",
                "keywords": ["comic", "story", "narrative", "illustration", "entertainment", "visual story"],
                "use_cases": ["educational comics", "story-based learning", "visual narratives", "engaging content"],
                "category": "Visual Content"
            },
            "generate-debate-speech": {
                "url": "https://app.yolearn.ai/teacher/generate-debate-speech",
                "name": "Debate Speech Generator",
                "description": "Creates debate topics, arguments, and speech materials for students",
                "keywords": ["debate", "speech", "argument", "persuasion", "discussion", "rhetoric"],
                "use_cases": ["debate preparation", "speech writing", "argumentative skills", "discussion topics"],
                "category": "Content Creation"
            },
            "generate-creative-prompt": {
                "url": "https://app.yolearn.ai/teacher/generate-creative-prompt",
                "name": "Creative Prompt Generator",
                "description": "Generates creative writing prompts and imaginative activities",
                "keywords": ["creative", "prompt", "writing", "imagination", "creativity", "inspiration"],
                "use_cases": ["creative writing", "imaginative activities", "inspiration prompts", "artistic expression"],
                "category": "Content Creation"
            },
            "graphic-agent": {
                "url": "https://app.yolearn.ai/teacher/graphic-agent",
                "name": "Graphic Design Agent",
                "description": "Creates various graphics and visual elements for educational materials",
                "keywords": ["graphic", "design", "visual", "image", "illustration", "artwork"],
                "use_cases": ["graphic design", "visual materials", "educational graphics", "visual elements"],
                "category": "Visual Content"
            },
            "poster-agent": {
                "url": "https://app.yolearn.ai/teacher/poster-agent",
                "name": "Poster Generator",
                "description": "Creates educational posters and display materials for classrooms",
                "keywords": ["poster", "display", "classroom", "visual", "announcement", "decoration"],
                "use_cases": ["poster creation", "classroom displays", "educational posters", "visual announcements"],
                "category": "Visual Content"
            },
            "problem-card-generator": {
                "url": "https://app.yolearn.ai/teacher/problem-card-generator",
                "name": "Problem Card Generator",
                "description": "Creates problem-solving cards and challenge activities for students",
                "keywords": ["problem", "card", "challenge", "solve", "critical thinking", "puzzle"],
                "use_cases": ["problem solving", "critical thinking", "challenge activities", "educational puzzles"],
                "category": "Content Creation"
            },
            "compare-contrast-card": {
                "url": "https://app.yolearn.ai/teacher/compare-contrast-card",
                "name": "Compare & Contrast Card Generator",
                "description": "Creates cards for comparing and contrasting different concepts or ideas",
                "keywords": ["compare", "contrast", "comparison", "difference", "similarity", "analyze"],
                "use_cases": ["comparative analysis", "concept comparison", "critical thinking", "analytical skills"],
                "category": "Content Creation"
            },
            "cognitive-map": {
                "url": "https://app.yolearn.ai/teacher/cognitive-map",
                "name": "Cognitive Map Generator",
                "description": "Creates cognitive maps and mind maps for organizing information",
                "keywords": ["cognitive map", "mind map", "organization", "structure", "concept mapping", "visual thinking"],
                "use_cases": ["information organization", "concept mapping", "visual thinking", "knowledge structure"],
                "category": "Visual Content"
            },
            "smartnotes": {
                "url": "https://app.yolearn.ai/teacher/smartnotes",
                "name": "Smart Notes Generator",
                "description": "Creates intelligent notes and study materials for students",
                "keywords": ["notes", "study", "summary", "review", "learning materials", "condensed"],
                "use_cases": ["note taking", "study materials", "content summarization", "learning aids"],
                "category": "Content Creation"
            },
            "quick-poll": {
                "url": "https://app.yolearn.ai/teacher/quick-poll",
                "name": "Quick Poll Generator",
                "description": "Creates quick polls and surveys for classroom engagement",
                "keywords": ["poll", "survey", "vote", "opinion", "feedback", "engagement"],
                "use_cases": ["classroom polls", "student feedback", "engagement activities", "opinion gathering"],
                "category": "Assessment"
            },
            "summarygen": {
                "url": "https://app.yolearn.ai/teacher/summarygen",
                "name": "Summary Generator",
                "description": "Creates summaries and condensed versions of educational content",
                "keywords": ["summary", "condensed", "overview", "key points", "main ideas", "digest"],
                "use_cases": ["content summarization", "key point extraction", "overview creation", "information condensing"],
                "category": "Content Creation"
            },
            "tpsprompt": {
                "url": "https://app.yolearn.ai/teacher/tpsprompt",
                "name": "TPS Prompt Generator",
                "description": "Creates Think-Pair-Share prompts and collaborative learning activities",
                "keywords": ["think pair share", "TPS", "collaboration", "discussion", "group work", "peer learning"],
                "use_cases": ["collaborative learning", "peer discussion", "group activities", "interactive learning"],
                "category": "Content Creation"
            },
            "flashcard-generator": {
                "url": "https://app.yolearn.ai/teacher/flashcard-generator",
                "name": "Flashcard Generator",
                "description": "Creates flashcards for memorization and quick review",
                "keywords": ["flashcard", "memorization", "review", "study", "recall", "practice"],
                "use_cases": ["memorization aids", "study tools", "quick review", "knowledge retention"],
                "category": "Content Creation"
            },
            "rhyme-generator": {
                "url": "https://app.yolearn.ai/teacher/rhyme-generator",
                "name": "Rhyme Generator",
                "description": "Creates rhymes and poetry for educational and memory purposes",
                "keywords": ["rhyme", "poetry", "verse", "memory", "song", "musical"],
                "use_cases": ["educational rhymes", "memory aids", "poetry creation", "musical learning"],
                "category": "Content Creation"
            },
            "podcast-generator": {
                "url": "https://app.yolearn.ai/teacher/podcast-generator",
                "name": "Podcast Generator",
                "description": "Creates educational podcast scripts and audio content ideas",
                "keywords": ["podcast", "audio", "script", "educational content", "listening", "media"],
                "use_cases": ["podcast creation", "audio content", "educational media", "listening activities"],
                "category": "Content Creation"
            },
            "pronunciation": {
                "url": "https://app.yolearn.ai/teacher/pronunciation",
                "name": "Pronunciation Guide",
                "description": "Provides pronunciation guidance and phonetic assistance",
                "keywords": ["pronunciation", "phonetic", "speech", "language", "accent", "sound"],
                "use_cases": ["pronunciation practice", "language learning", "speech improvement", "phonetic guidance"],
                "category": "Language Learning"
            },
            "generate-guided-prompt": {
                "url": "https://app.yolearn.ai/teacher/generate-guided-prompt",
                "name": "Guided Prompt Generator",
                "description": "Creates guided prompts and structured activities for student learning",
                "keywords": ["guided", "prompt", "structured", "step-by-step", "scaffolding", "support"],
                "use_cases": ["guided learning", "structured activities", "scaffolded instruction", "step-by-step guidance"],
                "category": "Content Creation"
            },
            "do-it-cards": {
                "url": "https://app.yolearn.ai/teacher/do-it-cards",
                "name": "Do-It Cards Generator",
                "description": "Creates action-oriented cards with tasks and activities for students",
                "keywords": ["action", "task", "activity", "do it", "hands-on", "practical"],
                "use_cases": ["hands-on activities", "practical tasks", "action-oriented learning", "activity cards"],
                "category": "Content Creation"
            },
            "drag-drop-builder": {
                "url": "https://app.yolearn.ai/teacher/drag-drop-builder",
                "name": "Drag & Drop Builder",
                "description": "Creates interactive drag and drop activities and exercises",
                "keywords": ["drag drop", "interactive", "matching", "sorting", "categorization", "activity"],
                "use_cases": ["interactive activities", "matching exercises", "sorting tasks", "categorization activities"],
                "category": "Interactive Content"
            },
            "scenario-card": {
                "url": "https://app.yolearn.ai/teacher/scenario-card",
                "name": "Scenario Card Generator",
                "description": "Creates scenario-based learning cards and situation analysis activities",
                "keywords": ["scenario", "situation", "case study", "analysis", "problem solving", "context"],
                "use_cases": ["scenario-based learning", "case studies", "situational analysis", "contextual learning"],
                "category": "Content Creation"
            },
            "gallary-card": {
                "url": "https://app.yolearn.ai/teacher/gallary-card",
                "name": "Gallery Card Generator",
                "description": "Creates gallery-style cards with images and descriptions for visual learning",
                "keywords": ["gallery", "visual", "image", "card", "collection", "display"],
                "use_cases": ["visual learning", "image galleries", "visual collections", "descriptive cards"],
                "category": "Visual Content"
            },
            "chart-generator": {
                "url": "https://app.yolearn.ai/teacher/chart-generator",
                "name": "Chart Generator",
                "description": "Creates various types of charts and graphs for data visualization",
                "keywords": ["chart", "graph", "data", "visualization", "statistics", "analysis"],
                "use_cases": ["data visualization", "chart creation", "statistical analysis", "graphical representation"],
                "category": "Visual Content"
            }
        }
    
    def get_all_tools(self) -> Dict[str, Any]:
        """Return all tools in the knowledge base"""
        return self.tools
    
    def get_tool_by_key(self, key: str) -> Dict[str, Any]:
        """Get a specific tool by its key"""
        return self.tools.get(key)
    
    def get_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all tools in a specific category"""
        return [tool for tool in self.tools.values() if tool.get('category') == category]
    
    def search_tools_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Search tools by keywords"""
        results = []
        for tool in self.tools.values():
            tool_keywords = tool.get('keywords', [])
            if any(keyword.lower() in ' '.join(tool_keywords).lower() for keyword in keywords):
                results.append(tool)
        return results
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        categories = set()
        for tool in self.tools.values():
            categories.add(tool.get('category', 'Unknown'))
        return sorted(list(categories)) 