# Educational Tool Chatbot - Complete Guide

## 🎯 Overview
An intelligent chatbot system that analyzes user queries and recommends the most appropriate educational tool from 38 available agents on the YoLearn platform. Features advanced memory integration, personalized recommendations, and intelligent filtering.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- mem0 Platform API key (for memory features)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd CombinedOrch
   pip install -r requirements.txt
   ```

2. **Environment setup:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "MEM0_API_KEY=your_mem0_api_key_here" >> .env
   echo "HOST=0.0.0.0" >> .env
   echo "PORT=8000" >> .env
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Access the interface:**
   - Web UI: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🏗️ Architecture

### Core Components
- **Main Application** (`main.py`): FastAPI app with all endpoints and initialization
- **Knowledge Base** (`services/knowledge_base.py`): 38 educational tools with metadata
- **Intent Classifier** (`services/intent_classifier.py`): OpenAI-powered query understanding
- **Memory Service** (`services/memory_service.py`): Intelligent personalization system
- **Analytics** (`services/analytics.py`): Usage tracking and insights

### Directory Structure
```
CombinedOrch/
├── main.py                    # Main FastAPI application
├── core/
│   └── config.py             # Configuration management
├── services/                 # Business logic
│   ├── knowledge_base.py     # Tool database
│   ├── intent_classifier.py  # Query processing
│   ├── memory_service.py     # User personalization
│   └── analytics.py          # Usage analytics
├── api/
│   └── endpoints.py          # API endpoint handlers
├── models/
│   └── schemas.py            # Pydantic models
├── exceptions/
│   └── handlers.py           # Error handling
└── templates/
    └── index.html            # Web interface
```

## 🧠 Memory & Personalization

### Intelligent Memory System
The chatbot features smart memory filtering that only stores valuable interactions:

**High Value (Always Stored):**
- User preferences: "I prefer...", "I like...", "I don't like..."
- Tool feedback: "This worked well", "Perfect!", "Not helpful"
- Teaching context: "My students", "My class", "I teach", "Grade level"

**Medium Value (Contextual):**
- Subject information: "Math", "Science", "History"
- Teaching style: "Interactive", "Hands-on", "Creative"
- Usage patterns: "Again", "Like before", "As usual"

**Learning Value:**
- Low confidence responses (< 0.7) for system improvement

### Personalization Features
- **Contextual Recommendations**: Based on teaching patterns
- **User Insights**: Analytics on tool usage and preferences
- **Teaching Style Analysis**: Identifies patterns (Content Creator, Assessment Focused, etc.)
- **Continuous Learning**: Improves recommendations over time

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Web interface
- `POST /chat` - Main chatbot interaction
- `GET /tools` - List all available tools
- `GET /categories` - Get tool categories
- `GET /health` - System health check

### Memory Endpoints
- `GET /memory/insights/{user_id}` - Get user insights
- `GET /memory/context/{user_id}` - Get user context
- `DELETE /memory/clear/{user_id}` - Clear user memory
- `POST /memory/preferences/{user_id}` - Update preferences

### Analytics
- `GET /analytics` - System usage statistics

## 🛠️ Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
MEM0_API_KEY=your_mem0_api_key_here

# Optional (with defaults)
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["*"]
```

## 📊 Educational Tools

The system includes 38 educational tools across 8 categories:

### Categories
1. **Content Creation** - Lesson plans, presentations, worksheets
2. **Assessment** - Quizzes, tests, rubrics
3. **Interactive** - Games, simulations, activities
4. **Visual** - Posters, infographics, diagrams
5. **Communication** - Newsletters, announcements
6. **Planning** - Calendars, schedules, timelines
7. **Research** - Citation tools, research guides
8. **Accessibility** - Inclusive design tools

### Tool Recommendation Logic
- **Semantic Analysis**: Uses OpenAI to understand query intent
- **Confidence Scoring**: Provides reliability metrics
- **Multi-tool Responses**: Suggests primary and secondary options
- **Context Awareness**: Considers user history and preferences

## 🔍 Usage Examples

### Basic Chat Interaction
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "I need help creating a lesson plan for my math class", "user_id": "teacher123"}'
```

### Get User Insights
```bash
curl "http://localhost:8000/memory/insights/teacher123"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
# Using gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

### Manual Testing
Access the web interface at `http://localhost:8000` and try these queries:
- "I need help creating a lesson plan for my math class"
- "My students are bored in class"
- "I need to create a quiz for my history class"
- "I need help with visual content for my classroom"

### API Testing
Use the interactive API documentation at `http://localhost:8000/docs`

## 📈 Monitoring & Analytics

### System Metrics
- Request count and success rates
- Tool recommendation accuracy
- User engagement patterns
- Memory system performance

### User Analytics
- Teaching pattern analysis
- Tool usage preferences
- Personalization effectiveness
- Learning progression tracking

## 🔧 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify OpenAI and mem0 API keys are correct
3. **Memory Errors**: Check mem0 Platform connectivity
4. **Performance Issues**: Monitor API rate limits

### Debug Mode
Set `LOG_LEVEL=DEBUG` in environment for detailed logging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

---

## 🎓 About YoLearn Platform

This chatbot integrates with the YoLearn platform's 38 educational tools, providing intelligent recommendations to enhance teaching and learning experiences. 