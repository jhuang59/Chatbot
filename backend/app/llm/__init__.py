from abc import ABC, abstractmethod
from typing import List, Dict


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def get_response(self, user_message: str, conversation_history: List[Dict[str, str]]) -> str:
        """Get response from LLM based on user message and history"""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate that the provider is properly configured"""
        pass
