# LLM Chatbot Architecture

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CHATBOT SYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────┐         ┌──────────────────────────────────┐ │
│  │   FRONTEND LAYER     │         │     BACKEND LAYER              │ │
│  │   (Client Side)      │         │     (Server Side)              │ │
│  ├──────────────────────┤         ├──────────────────────────────────┤ │
│  │                      │         │                                │ │
│  │  React Application   │────────▶│  FastAPI Server                │ │
│  │  - Chat UI           │◀────────│  - REST API Endpoints          │ │
│  │  - Message Display   │  HTTP   │  - Request Handling            │ │
│  │  - User Input        │  REST   │  - Response Generation         │ │
│  │  - Conversation Mgmt │         │                                │ │
│  │                      │         │  ┌────────────────────────┐   │ │
│  │  Port: 3000          │         │  │   LangChain Layer      │   │ │
│  │                      │         │  │  - Message Management  │   │ │
│  └──────────────────────┘         │  │  - Provider Abstraction│   │ │
│                                   │  │  - Request Building    │   │ │
│                                   │  └────────────────────────┘   │ │
│                                   │                                │ │
│                                   │  ┌────────────────────────┐   │ │
│                                   │  │  LLM Provider Layer    │   │ │
│                                   │  │  - OpenAI Provider     │   │ │
│                                   │  │  - OpenRouter Provider │   │ │
│                                   │  │  - Provider Factory    │   │ │
│                                   │  └────────────────────────┘   │ │
│                                   │                                │ │
│                                   │  ┌────────────────────────┐   │ │
│                                   │  │  Database Layer        │   │ │
│                                   │  │  - SQLAlchemy ORM      │   │ │
│                                   │  │  - Conversation Model  │   │ │
│                                   │  │  - Message Model       │   │ │
│                                   │  └────────────────────────┘   │ │
│                                   │                                │ │
│                                   │  Port: 8000                    │ │
│                                   └──────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────┐         ┌──────────────────────────────────┐ │
│  │   DATA PERSISTENCE   │         │   EXTERNAL SERVICES            │ │
│  ├──────────────────────┤         ├──────────────────────────────────┤ │
│  │                      │         │                                │ │
│  │  SQLite Database     │         │  ┌────────────────────────┐   │ │
│  │  - Conversations     │         │  │  OpenAI API            │   │ │
│  │  - Messages          │         │  │  - GPT Models          │   │ │
│  │  - Chat History      │         │  │  - Endpoint: openai.com│   │ │
│  │                      │         │  └────────────────────────┘   │ │
│  │  File: chatbot.db    │         │                                │ │
│  │                      │         │  ┌────────────────────────┐   │ │
│  │                      │         │  │  OpenRouter API        │   │ │
│  │                      │         │  │  - 150+ Models         │   │ │
│  │                      │         │  │  - Claude, Mistral, etc│   │ │
│  │                      │         │  │  - Endpoint: openrouter.ai  │ │
│  │                      │         │  └────────────────────────┘   │ │
│  └──────────────────────┘         └──────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. Network Communication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE FLOW SEQUENCE                                 │
└─────────────────────────────────────────────────────────────────────────┘

USER INTERACTION FLOW:
════════════════════════════════════════════════════════════════════════════

1. USER SENDS MESSAGE
   ┌─────────────┐
   │   Browser   │
   │  (React)    │
   └──────┬──────┘
          │ User types "Hello" and clicks Send
          │
          ▼
   ┌─────────────────────────────────────┐
   │  ChatWindow Component               │
   │  - Captures user input              │
   │  - Calls onSendMessage()            │
   └──────┬──────────────────────────────┘
          │
          │ HTTP POST Request
          │ /api/chat/send
          │ Body: {
          │   "conversation_id": "uuid",
          │   "content": "Hello"
          │ }
          ▼
   ┌──────────────────────────────────────┐
   │  FastAPI Backend                     │
   │  Port: 8000                          │
   │                                      │
   │  receive_message(request)            │
   └──────┬───────────────────────────────┘
          │
          ▼
   ┌──────────────────────────────────────┐
   │  Database Operations (SQLAlchemy)    │
   │  - Save user message                 │
   │  - Fetch conversation history        │
   │  - FROM: conversations, messages     │
   └──────┬───────────────────────────────┘
          │
          ▼
   ┌──────────────────────────────────────┐
   │  LangChain Layer                     │
   │  - Build message list                │
   │  - Format for LLM API                │
   │  - Handle response parsing           │
   └──────┬───────────────────────────────┘
          │
          ▼
   ┌──────────────────────────────────────┐
   │  LLM Provider Factory                │
   │  - Check: LLM_PROVIDER env var       │
   │  - Create appropriate provider       │
   │  - Return OpenAI or OpenRouter       │
   └──────┬───────────────────────────────┘
          │
          ├─────────────────────┬──────────────────────┐
          │                     │                      │
          ▼                     ▼                      ▼
    (OpenAI Path)        (OpenRouter Path)      (Error Path)
    │                    │                      │
    │ HTTPS              │ HTTPS                │
    │ POST               │ POST                 │
    ▼                    ▼                      ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│ OpenAI API  │     │ OpenRouter  │     │ Return Error │
│ api.openai  │     │ openrouter  │     │ 500 Error    │
│ .com        │     │ .ai         │     └──────────────┘
│             │     │             │
│ Response:   │     │ Response:   │
│ {           │     │ {           │
│   "content":│     │   "content":│
│   "..."     │     │   "..."     │
│ }           │     │ }           │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └────────┬──────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │  LangChain Response Handler          │
    │  - Parse LLM response                │
    │  - Extract text content              │
    └──────┬───────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  Save Assistant Message              │
    │  - Store in database                 │
    │  - Role: "assistant"                 │
    └──────┬───────────────────────────────┘
           │
           │ HTTP Response (JSON)
           │ {
           │   "conversation_id": "uuid",
           │   "response": "Hi! How are you?",
           │   "messages": [...]
           │ }
           ▼
    ┌──────────────────────────────────────┐
    │  React Frontend                      │
    │  - Receive response                  │
    │  - Update state                      │
    │  - Display assistant message         │
    │  - Scroll to bottom                  │
    └──────────────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────────────┐
    │  User Sees Response                  │
    │  "Hi! How are you?"                  │
    └──────────────────────────────────────┘
```

## 3. LangChain Integration Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    LANGCHAIN ABSTRACTION LAYER                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  WITHOUT LANGCHAIN (Direct API Calls):                                  │
│  ════════════════════════════════════════════════════════════════════   │
│                                                                           │
│     Your Code                OpenAI API        OpenRouter API            │
│         │                       │                    │                   │
│         ├──────────────────────▶│                    │                   │
│         │    POST /v1/messages  │                    │                   │
│         │    Headers: {...}     │                    │                   │
│         │    Body: {...}        │                    │                   │
│         │                       │◀───────────────────┤ (different!)      │
│         │                       │    Response        │                   │
│         │                                                                │
│         └──────────────────────▶│ (need different code for OpenRouter)  │
│              (Repeated code)    │                                        │
│              (Different logic)  │                                        │
│                                                                           │
│  ════════════════════════════════════════════════════════════════════   │
│                                                                           │
│  WITH LANGCHAIN (Unified Interface):                                    │
│  ════════════════════════════════════════════════════════════════════   │
│                                                                           │
│                          Your Code                                       │
│                              │                                           │
│                              ▼                                           │
│                  ┌────────────────────────┐                              │
│                  │   LangChain Layer      │                              │
│                  │                        │                              │
│                  │  ChatOpenAI Instance   │                              │
│                  │  - Unified interface   │                              │
│                  │  - Provider agnostic   │                              │
│                  │  - Message formatting  │                              │
│                  │  - Response parsing    │                              │
│                  └────────┬───────────────┘                              │
│                           │                                              │
│                ┌──────────┴──────────┐                                   │
│                │                     │                                   │
│                ▼                     ▼                                   │
│         ┌────────────────┐     ┌────────────────┐                       │
│         │   OpenAI SDK   │     │ OpenRouter SDK │                       │
│         │  (ChatOpenAI   │     │  (ChatOpenAI   │                       │
│         │   for OpenAI)  │     │ for OpenRouter)│                       │
│         └────────┬───────┘     └────────┬───────┘                       │
│                  │                     │                                 │
│                  ▼                     ▼                                 │
│         ┌────────────────┐     ┌────────────────┐                       │
│         │  OpenAI API    │     │ OpenRouter API │                       │
│         │  api.openai.com│     │ openrouter.ai  │                       │
│         └────────────────┘     └────────────────┘                       │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## 4. Data Flow in LangChain

```
┌──────────────────────────────────────────────────────────────────────────┐
│              HOW LANGCHAIN PROCESSES MESSAGES                            │
└──────────────────────────────────────────────────────────────────────────┘

INPUT: User Message + Conversation History
═════════════════════════════════════════════════════════════════════════

user_message = "What is the capital of France?"

conversation_history = [
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi! How can I help?"}
]

STEP 1: Build Message List
────────────────────────────────────────────────────────────────────────

LangChain converts to standard format:

messages = [
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi! How can I help?"},
  {"role": "user", "content": "What is the capital of France?"}
]

STEP 2: Format for API
──────────────────────────────────────────────────────────────────────

LangChain converts to provider-specific format:

For OpenAI:
──────────
POST /v1/chat/completions
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}

For OpenRouter:
───────────────
POST /api/v1/chat/completions  (Same format!)
Headers: {
  "Authorization": "Bearer sk-or-...",
  "HTTP-Referer": "your-site.com",  (optional ranking)
  "X-Title": "Your Site"            (optional ranking)
}
{
  "model": "anthropic/claude-3-5-sonnet",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}

Note: LangChain handles BOTH formats without your code needing to change!

STEP 3: Send to LLM
──────────────────────────────────────────────────────────────────────

response = self.llm.invoke(messages)

LangChain automatically:
- Makes HTTP request to correct endpoint
- Handles authentication
- Manages retries
- Parses response

STEP 4: Extract Response
──────────────────────────────────────────────────────────────────────

response.content = "Paris is the capital of France."

LangChain returns:
- Unified response object
- Same interface for all providers
- Easy to extract text content

OUTPUT: Assistant Message
═════════════════════════════════════════════════════════════════════════

"Paris is the capital of France."
(Sent back to user)
```

## 5. Database & Message Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│               DATABASE SCHEMA & RELATIONSHIPS                            │
└──────────────────────────────────────────────────────────────────────────┘

CONVERSATION TABLE
╔════════════════════════════════════════════════════════════════════════╗
║ id (String, PK)                                                        ║
║ title (String)                "Test Chat"                              ║
║ created_at (DateTime)          2025-11-18 10:30:00                     ║
║ updated_at (DateTime)          2025-11-18 10:35:00                     ║
╚════════════════════════════════════════════════════════════════════════╝
                                    │
                    ONE-TO-MANY RELATIONSHIP
                           (cascade delete)
                                    │
                                    ▼
MESSAGE TABLE (Conversation ID as Foreign Key)
╔════════════════════════════════════════════════════════════════════════╗
║ id (Integer, PK)  │ conversation_id (FK) │ role       │ content       ║
╠═══════════════════╪═════════════════════════════════════════════════════╣
║ 1                 │ abc-123-xyz          │ user       │ "Hello"       ║
║ 2                 │ abc-123-xyz          │ assistant  │ "Hi there!"   ║
║ 3                 │ abc-123-xyz          │ user       │ "How are you?"║
║ 4                 │ abc-123-xyz          │ assistant  │ "I'm good!"   ║
║ 5                 │ def-456-uvw          │ user       │ "Hi"          ║
║ 6                 │ def-456-uvw          │ assistant  │ "Hello!"      ║
╚═══════════════════╧═════════════════════════════════════════════════════╝

QUERY EXAMPLE: Get all messages for a conversation
──────────────────────────────────────────────────
SELECT * FROM messages
WHERE conversation_id = 'abc-123-xyz'
ORDER BY created_at

RESULT:
┌────┬────────────────┬────────────┬──────────────────┐
│ ID │ conversation_id│   role     │ content          │
├────┼────────────────┼────────────┼──────────────────┤
│ 1  │ abc-123-xyz    │ user       │ Hello            │
│ 2  │ abc-123-xyz    │ assistant  │ Hi there!        │
│ 3  │ abc-123-xyz    │ user       │ How are you?     │
│ 4  │ abc-123-xyz    │ assistant  │ I'm good!        │
└────┴────────────────┴────────────┴──────────────────┘

This becomes the conversation_history passed to LangChain!
```

## 6. Request/Response Example

```
┌──────────────────────────────────────────────────────────────────────────┐
│                 COMPLETE REQUEST/RESPONSE CYCLE                          │
└──────────────────────────────────────────────────────────────────────────┘

1. FRONTEND SENDS REQUEST
═════════════════════════════════════════════════════════════════════════

POST http://localhost:8000/api/chat/send

{
  "conversation_id": "abc-123-xyz",
  "content": "What is 2+2?"
}

2. BACKEND PROCESSES
═════════════════════════════════════════════════════════════════════════

FastAPI receives request
    ↓
Save user message to database
    ↓
Fetch conversation history:
  [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"}
  ]
    ↓
Create LangChain instance (OpenRouter):
  llm = ChatOpenAI(
    api_key="sk-or-...",
    model="anthropic/claude-3-5-sonnet",
    base_url="https://openrouter.ai/api/v1",
    default_headers={
      "HTTP-Referer": "your-site.com",
      "X-Title": "Your Site"
    }
  )
    ↓
Build message list:
  [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "What is 2+2?"}
  ]
    ↓
Call LangChain:
  response = llm.invoke(messages)
    ↓
LangChain HTTPS POST to https://openrouter.ai/api/v1/chat/completions
    ↓
OpenRouter processes with Claude model
    ↓
Returns: "2+2 equals 4"
    ↓
Extract response content
    ↓
Save assistant message to database
    ↓

3. BACKEND RETURNS RESPONSE
═════════════════════════════════════════════════════════════════════════

{
  "conversation_id": "abc-123-xyz",
  "response": "2+2 equals 4",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4"}
  ]
}

4. FRONTEND DISPLAYS
═════════════════════════════════════════════════════════════════════════

User sees:
┌─────────────────────────────────┐
│  You: What is 2+2?              │
│  Claude: 2+2 equals 4           │
└─────────────────────────────────┘
```

## 7. Why Use LangChain This Way?

```
┌──────────────────────────────────────────────────────────────────────────┐
│               BENEFITS OF LANGCHAIN ABSTRACTION                          │
└──────────────────────────────────────────────────────────────────────────┘

PROBLEM 1: Multiple LLM Providers Have Different APIs
═════════════════════════════════════════════════════════════════════════

WITHOUT LangChain:
┌─────────────────────────────────────────────────────────────────────┐
│ if provider == "openai":                                            │
│     # Different imports                                             │
│     from openai import OpenAI                                      │
│     client = OpenAI(api_key=key)                                   │
│     response = client.chat.completions.create(                     │
│         model="gpt-3.5-turbo",                                     │
│         messages=messages                                           │
│     )                                                               │
│     text = response.choices[0].message.content                    │
│                                                                     │
│ elif provider == "anthropic":                                      │
│     # Different imports                                            │
│     from anthropic import Anthropic                               │
│     client = Anthropic(api_key=key)                               │
│     response = client.messages.create(                            │
│         model="claude-3-5-sonnet",                                │
│         max_tokens=512,                                            │
│         messages=messages                                          │
│     )                                                               │
│     text = response.content[0].text                               │
│                                                                     │
│ elif provider == "openrouter":                                     │
│     # Different imports again!                                    │
│     # Different API calls                                          │
│     # Different response parsing                                   │
│                                                                     │
│ # Your code is FULL OF IF/ELIF BRANCHES!                          │
│ # Hard to maintain                                                 │
│ # Easy to break                                                    │
└─────────────────────────────────────────────────────────────────────┘

WITH LangChain:
┌─────────────────────────────────────────────────────────────────────┐
│ # Same code for ALL providers!                                      │
│ from langchain_openai import ChatOpenAI                            │
│                                                                     │
│ llm = ChatOpenAI(                                                  │
│     api_key=api_key,                                              │
│     model=model,                                                  │
│     base_url="https://openrouter.ai/api/v1"  # Different URL!    │
│ )                                                                   │
│                                                                     │
│ response = llm.invoke(messages)  # SAME for all!                  │
│ text = response.content           # SAME for all!                 │
│                                                                     │
│ # That's it! Change model/url, everything works!                  │
│ # No code changes needed                                           │
│ # Just change .env file                                           │
└─────────────────────────────────────────────────────────────────────┘

BENEFIT:
 ✅ Single line change to switch providers: just set env vars!
 ✅ No code refactoring needed
 ✅ Reduced bugs from copy-paste errors


PROBLEM 2: Message Formatting
═════════════════════════════════════════════════════════════════════

Different providers expect different formats:

OpenAI expects:
  [{"role": "user", "content": "..."}, ...]

Anthropic expects:
  Same format ✓ (but different handling)

OpenRouter expects:
  Same as OpenAI (compatible API)

WITHOUT LangChain: You must format manually for each provider
WITH LangChain: It handles formatting automatically ✓


PROBLEM 3: API Response Parsing
═════════════════════════════════════════════════════════════════════

OpenAI returns:
  response.choices[0].message.content

Anthropic returns:
  response.content[0].text

WITHOUT LangChain:
  if provider == "openai":
      text = response.choices[0].message.content
  elif provider == "anthropic":
      text = response.content[0].text

WITH LangChain:
  text = response.content  # Always the same!


BENEFIT:
 ✅ Consistent response handling
 ✅ No try/except for different formats
 ✅ Easier to debug


PROBLEM 4: Error Handling & Retries
═════════════════════════════════════════════════════════════════════

WITHOUT LangChain:
  You must implement:
  - Connection retries
  - Rate limit handling
  - Timeout management
  - Response validation

WITH LangChain:
  Built-in:
  - Automatic retries ✓
  - Rate limit awareness ✓
  - Timeout handling ✓
  - Response validation ✓


BENEFIT:
 ✅ Robust API handling
 ✅ Better error recovery
 ✅ Production-ready


PROBLEM 5: Future Provider Support
═════════════════════════════════════════════════════════════════════

New providers emerge (Groq, Together AI, vLLM, etc.)

WITHOUT LangChain:
  You rewrite API integration for each new provider
  Lots of code duplication
  Risk of bugs
  Time-consuming

WITH LangChain:
  LangChain community adds support
  You just use it
  Minimal code changes needed


BENEFIT:
 ✅ Future-proof architecture
 ✅ Community-maintained code
 ✅ Quick to add new providers
```

## 8. Architecture Summary Table

| Component | Purpose | Technology | Why? |
|-----------|---------|-----------|------|
| **React Frontend** | User interface | React 18 + Axios | Component-based, modern, extensive ecosystem |
| **FastAPI** | API server | FastAPI + Uvicorn | Fast, async, auto-documentation, type-safe |
| **LangChain** | LLM abstraction | LangChain | Unified interface for 100+ LLM providers |
| **OpenAI/OpenRouter** | LLM service | ChatOpenAI (LangChain) | GPT/Claude models, 150+ options |
| **SQLite** | Persistence | SQLAlchemy ORM | Lightweight, serverless, no setup needed |
| **Docker** | Deployment | Docker Compose | Portable, reproducible, production-ready |

## 9. Benefits of This Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURE BENEFITS                             │
└──────────────────────────────────────────────────────────────────────────┘

SEPARATION OF CONCERNS
═════════════════════════════════════════════════════════════════════════
✅ Frontend: React handles UI/UX only
✅ Backend: FastAPI handles business logic
✅ LLM: LangChain abstracts LLM details
✅ Data: SQLAlchemy handles persistence

Result: Each layer can be updated independently


SCALABILITY
═════════════════════════════════════════════════════════════════════════
✅ Frontend: Can scale with more features
✅ Backend: Can add more endpoints
✅ Providers: Can switch/add providers without code changes
✅ Database: Can migrate from SQLite to PostgreSQL (ORM handles it)


MAINTAINABILITY
═════════════════════════════════════════════════════════════════════════
✅ Single responsibility principle
✅ Clear interfaces between layers
✅ Easy to test each component
✅ Easy to add new features


EXTENSIBILITY
═════════════════════════════════════════════════════════════════════════
Future enhancements:

Add user authentication:
  - Just add auth middleware to FastAPI ✓

Add conversation search:
  - Just add database index ✓

Add multiple models:
  - Just expose model selection in UI ✓

Add conversation export:
  - Just add new endpoint ✓

Add system prompts:
  - Just add to Message formatting ✓

Add streaming responses:
  - LangChain supports streaming! ✓

Add memory optimization:
  - LangChain has memory modules! ✓


PROVIDER FLEXIBILITY
═════════════════════════════════════════════════════════════════════════
✅ Switch providers with .env change
✅ No code recompilation
✅ No deployment needed
✅ Fast A/B testing of models


PRODUCTION READINESS
═════════════════════════════════════════════════════════════════════════
✅ Health checks built-in
✅ Error handling
✅ CORS configured
✅ Docker containerization
✅ Environment-based configuration
✅ Database transactions (ACID)
✅ Request validation (Pydantic)
```

