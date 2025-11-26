from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def get_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Get response from LLM based on user message and history

        Args:
            user_message: The current user message
            conversation_history: List of previous messages with roles
            system_prompt: Optional system prompt to guide behavior

        Returns:
            The LLM response text
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate that the provider is properly configured"""
        pass
