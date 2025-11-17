# LLM Chatbot

A modern, extensible web-based chatbot powered by Large Language Models (LLMs). Built with FastAPI, React, and Docker for easy deployment.

## Features

- 💬 **LLM-Based Conversations** - Real-time chat with AI models
- 🎨 **Clean Web Interface** - Beautiful React-based UI
- 🔄 **Conversation History** - Persistent storage of chat history
- 🚀 **Docker Ready** - One-command deployment
- 🔌 **Extensible Architecture** - Easy to add new LLM providers
- ⚙️ **Environment Configuration** - Flexible configuration via environment variables
- 📚 **API Documentation** - Auto-generated FastAPI docs

## Project Structure

```
Chatbot/
├── backend/                 # FastAPI server with LangChain integration
│   ├── app/
│   │   ├── llm/            # LLM provider implementations
│   │   ├── api/            # API endpoints
│   │   ├── db/             # Database models and initialization
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               # React web interface
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.jsx
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml      # Docker Compose orchestration
└── .env.example           # Environment configuration template
```

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM Integration**: LangChain
- **Database**: SQLite (with SQLAlchemy ORM)
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS3

### Deployment
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose (for containerized deployment)
- OR Python 3.11+ and Node.js 18+ (for local development)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository and navigate to the project**
   ```bash
   cd Chatbot
   ```

2. **Create environment configuration**
   ```bash
   cp .env.example .env
   ```

3. **Add your LLM API key** (e.g., OpenAI)
   ```bash
   # Edit .env and add your OPENAI_API_KEY
   nano .env
   ```

4. **Start the application**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY to .env
   ```

5. **Run the server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Open new terminal and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Start development server**
   ```bash
   npm start
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API will connect to: http://localhost:8000

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Database
DATABASE_URL=sqlite:///./chatbot.db

# Server
BACKEND_PORT=8000
PYTHONUNBUFFERED=1
```

### Supported LLM Providers

Currently supported:
- **OpenAI** (GPT-3.5-turbo, GPT-4)

Easily extensible for:
- **Anthropic Claude**
- **Local Models (Ollama)**
- **Other providers**

To add a new provider:
1. Create a new class in `backend/app/llm/provider.py` that extends `LLMProvider`
2. Implement `get_response()` and `validate_config()` methods
3. Update `get_llm_provider()` factory function
4. Add required environment variables to `.env.example`

## API Endpoints

### Chat Endpoints

#### Create Conversation
```
POST /api/chat/conversations
Content-Type: application/json

{
  "title": "Optional conversation title"
}

Response:
{
  "id": "uuid-string",
  "title": "conversation title",
  "messages": []
}
```

#### Send Message
```
POST /api/chat/send
Content-Type: application/json

{
  "conversation_id": "uuid-string",
  "content": "Your message here"
}

Response:
{
  "conversation_id": "uuid-string",
  "response": "Assistant's response",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

#### Get Conversation
```
GET /api/chat/conversations/{conversation_id}

Response:
{
  "id": "uuid-string",
  "title": "conversation title",
  "messages": [...]
}
```

### Health Check
```
GET /health

Response: {"status": "ok"}
```

### API Documentation
Auto-generated interactive docs available at: `http://localhost:8000/docs`

## Development

### Project Goals

**Stage 1 (Current)**
- ✅ Simple, clean chat interface
- ✅ Text-based LLM integration
- ✅ Conversation persistence
- ✅ Docker deployment
- ✅ Extensible architecture

**Future Stages**
- Multi-turn conversation optimization
- File upload support
- Conversation search and filtering
- User authentication
- Multiple model selection
- Custom system prompts
- Chat export (PDF, Markdown)
- Advanced memory management

### Adding New Features

The architecture supports easy extensibility:

1. **New LLM Providers**: Add to `backend/app/llm/provider.py`
2. **New API Endpoints**: Add to `backend/app/api/chat.py`
3. **UI Components**: Add to `frontend/src/components/`
4. **Database Models**: Update `backend/app/db/models.py`

## Docker Compose Details

### Services

- **backend**: FastAPI server (port 8000)
- **frontend**: React app served by Express (port 3000)

### Volumes

- `chatbot_data`: Persistent storage for SQLite database

### Network

- Services communicate via `chatbot-network` bridge network

### Health Checks

Both services include health checks to ensure proper startup order.

## Troubleshooting

### Backend won't start
- Check that `OPENAI_API_KEY` is set in `.env`
- Verify port 8000 is not in use
- Check logs: `docker-compose logs backend`

### Frontend won't connect to backend
- Ensure backend is running and healthy
- Check that `REACT_APP_API_URL` is correct
- In Docker: Use `http://backend:8000` (service name)
- Locally: Use `http://localhost:8000`

### Database errors
- Delete `chatbot.db` file to reset database
- For Docker: `docker volume rm chatbot_chatbot_data`

## Performance Considerations

- **Token Limits**: Configure max tokens in LLM provider
- **Model Selection**: Larger models = slower but smarter responses
- **Temperature**: Controls response randomness (0.0-1.0)
- **Context Length**: Long conversations may slow responses

## Security Notes

- Never commit `.env` files with real API keys
- Use `.env.example` as template
- Consider API key rotation for production
- Frontend makes direct API calls (implement backend proxy for auth in production)

## License

MIT

## Support

For issues, feature requests, or contributions, please refer to the repository.
