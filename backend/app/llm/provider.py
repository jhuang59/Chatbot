import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from . import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI GPT-based LLM provider using LangChain"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=512
        )

    def validate_config(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(os.getenv("OPENAI_API_KEY"))

    def get_response(self, user_message: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get response from OpenAI based on user message and conversation history"""
        try:
            # Build message list from history
            messages = []
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Get response from LLM using message format
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"Error getting response from OpenAI: {str(e)}")


class OpenRouterProvider(LLMProvider):
    """OpenRouter API provider - supports multiple LLM models through a unified API"""

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")

        # OpenRouter uses OpenAI-compatible API
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            base_url="https://openrouter.io/api/v1",
            temperature=0.7,
            max_tokens=512
        )

    def validate_config(self) -> bool:
        """Check if OpenRouter API key is configured"""
        return bool(os.getenv("OPENROUTER_API_KEY"))

    def get_response(self, user_message: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get response from OpenRouter based on user message and conversation history"""
        try:
            # Build message list from history
            messages = []
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Get response from LLM using message format
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"Error getting response from OpenRouter: {str(e)}")


def get_llm_provider() -> LLMProvider:
    """Factory function to get the configured LLM provider"""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        return OpenAIProvider()
    elif provider == "openrouter":
        return OpenRouterProvider()
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            f"Supported providers: 'openai', 'openrouter'"
        )
