from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Generator
import uuid
import os
from sqlalchemy.orm import Session

from ..db.models import Conversation, Message
from ..llm.provider import get_llm_provider

router = APIRouter(prefix="/api/chat", tags=["chat"])


class MessageRequest(BaseModel):
    conversation_id: str
    content: str


class MessageResponse(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    messages: List[MessageResponse]


class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: str
    title: str
    messages: List[MessageResponse]


# Global session factory
_SessionLocal = None


def init_db_session(database_url: str):
    """Initialize database session factory"""
    global _SessionLocal
    from ..db import get_session_factory
    _SessionLocal = get_session_factory(database_url)


def get_db() -> Generator[Session, None, None]:
    """Dependency for database session"""
    if _SessionLocal is None:
        database_url = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
        init_db_session(database_url)
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    req: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    try:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            title=req.title or f"Conversation {conversation_id[:8]}"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            messages=[]
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation and its messages"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = [
            MessageResponse(role=msg.role, content=msg.content)
            for msg in conversation.messages
        ]

        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            messages=messages
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send", response_model=ChatResponse)
def send_message(
    req: MessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get a response from the chatbot"""
    try:
        # Get conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == req.conversation_id
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Store user message
        user_msg = Message(
            conversation_id=req.conversation_id,
            role="user",
            content=req.content
        )
        db.add(user_msg)
        db.commit()

        # Get conversation history
        messages = db.query(Message).filter(
            Message.conversation_id == req.conversation_id
        ).order_by(Message.created_at).all()

        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages[:-1]  # Exclude the current message for context
        ]

        # Get LLM response
        llm_provider = get_llm_provider()
        response_content = llm_provider.get_response(req.content, history)

        # Store assistant message
        assistant_msg = Message(
            conversation_id=req.conversation_id,
            role="assistant",
            content=response_content
        )
        db.add(assistant_msg)
        db.commit()

        # Get updated message list
        all_messages = db.query(Message).filter(
            Message.conversation_id == req.conversation_id
        ).order_by(Message.created_at).all()

        return ChatResponse(
            conversation_id=req.conversation_id,
            response=response_content,
            messages=[
                MessageResponse(role=msg.role, content=msg.content)
                for msg in all_messages
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
