# Testing Guide

## Quick Test of LLM Providers

Use the `test_llm.py` script to verify your LLM provider is working before deploying.

### Prerequisites

```bash
cd backend
pip install -r requirements.txt
```

### Test OpenAI

```bash
python test_llm.py openai sk-your-openai-key-here gpt-3.5-turbo
```

Or using environment variables:

```bash
export OPENAI_API_KEY=sk-your-openai-key-here
export OPENAI_MODEL=gpt-3.5-turbo
python test_llm.py openai
```

### Test OpenRouter

```bash
python test_llm.py openrouter sk-or-your-openrouter-key-here anthropic/claude-3-5-sonnet
```

Or using environment variables:

```bash
export OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
export OPENROUTER_MODEL=anthropic/claude-3-5-sonnet
python test_llm.py openrouter
```

## Popular OpenRouter Models to Test

```bash
# Anthropic Claude (excellent reasoning)
python test_llm.py openrouter sk-or-... anthropic/claude-3-5-sonnet

# Mistral (fast and cheap)
python test_llm.py openrouter sk-or-... mistral/mistral-7b

# Meta LLaMA (open source)
python test_llm.py openrouter sk-or-... meta-llama/llama-2-70b-chat

# OpenAI via OpenRouter
python test_llm.py openrouter sk-or-... openai/gpt-4
```

## Test API Endpoints Locally

### 1. Start Backend

```bash
cd backend
export OPENROUTER_API_KEY=sk-or-your-key-here
export OPENROUTER_MODEL=anthropic/claude-3-5-sonnet
python -m uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000

### 2. Create Conversation

```bash
curl -X POST http://localhost:8000/api/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Chat"}'
```

Response:
```json
{
  "id": "abc123...",
  "title": "Test Chat",
  "messages": []
}
```

Save the `id` for next step.

### 3. Send Message

```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "abc123...",
    "content": "Say hello briefly in 2 sentences"
  }'
```

Response:
```json
{
  "conversation_id": "abc123...",
  "response": "Hello! I'm here and ready to help.",
  "messages": [
    {"role": "user", "content": "Say hello briefly in 2 sentences"},
    {"role": "assistant", "content": "Hello! I'm here and ready to help."}
  ]
}
```

### 4. Get Conversation History

```bash
curl http://localhost:8000/api/chat/conversations/abc123...
```

## Check API Documentation

Once backend is running, visit:
http://localhost:8000/docs

This shows auto-generated interactive API documentation.

## Troubleshooting

### "Couldn't connect to Docker daemon"
Your Docker daemon isn't running:
```bash
sudo systemctl start docker
```

### "OPENROUTER_API_KEY environment variable is not set"
Set your API key:
```bash
export OPENROUTER_API_KEY=sk-or-your-key-here
python test_llm.py openrouter
```

### "401 Unauthorized" from OpenRouter
- Check your API key is correct
- Verify at https://openrouter.io/keys
- Make sure account has credits

### "Unknown model" from OpenRouter
- Check model name is correct
- Visit https://openrouter.io/models for available models
- Example: `anthropic/claude-3-5-sonnet`

### Database Relationship Error
If you see "Could not determine join condition between parent/child tables":
1. Delete old database: `rm chatbot.db`
2. Restart application (database will be recreated)

## Full Integration Test

Test the entire stack locally:

```bash
# Terminal 1: Backend
cd backend
export OPENROUTER_API_KEY=sk-or-...
export OPENROUTER_MODEL=anthropic/claude-3-5-sonnet
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm start

# Terminal 3: Test
# Visit http://localhost:3000 and chat with the bot
```

## Deploy with Docker

Once local testing is successful:

```bash
# Create .env file
cp .env.example .env

# Edit .env with your API key
nano .env

# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Performance Testing

### Test with Different Models

Compare response times across models:

```bash
# Fast but less capable
time python test_llm.py openrouter $KEY mistral/mistral-7b

# Slower but more capable
time python test_llm.py openrouter $KEY anthropic/claude-3-5-sonnet

# Most capable
time python test_llm.py openrouter $KEY openai/gpt-4
```

### Test with Long Conversations

The API maintains conversation history. Test with multiple messages:

```bash
# Create conversation
CONV_ID=$(curl -s -X POST http://localhost:8000/api/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{"title":"Long Test"}' | jq -r '.id')

# Send first message
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":\"$CONV_ID\",\"content\":\"Hello\"}"

# Send follow-up
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":\"$CONV_ID\",\"content\":\"What did I just say?\"}"
```
