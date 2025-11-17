#!/usr/bin/env python3
"""
Test script to verify LLM provider integration
Usage: python test_llm.py [provider] [api_key] [model]

Examples:
  python test_llm.py openai sk-... gpt-3.5-turbo
  python test_llm.py openrouter sk-or-... anthropic/claude-3-5-sonnet
"""

import sys
import os
from typing import Optional

def test_openai(api_key: str, model: str = "gpt-3.5-turbo"):
    """Test OpenAI provider"""
    try:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=256
        )

        messages = [
            {"role": "user", "content": "Say 'Hello from OpenAI!' in exactly 5 words."}
        ]

        response = llm.invoke(messages)
        print(f"✓ OpenAI ({model}) Response:")
        print(f"  {response.content}\n")
        return True
    except Exception as e:
        print(f"✗ OpenAI Error: {str(e)}\n")
        return False


def test_openrouter(api_key: str, model: str = "openai/gpt-3.5-turbo"):
    """Test OpenRouter provider"""
    try:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            base_url="https://openrouter.io/api/v1",
            temperature=0.7,
            max_tokens=256
        )

        messages = [
            {"role": "user", "content": "Say 'Hello from OpenRouter!' in exactly 5 words."}
        ]

        response = llm.invoke(messages)
        print(f"✓ OpenRouter ({model}) Response:")
        print(f"  {response.content}\n")
        return True
    except Exception as e:
        print(f"✗ OpenRouter Error: {str(e)}\n")
        return False


def main():
    print("=" * 60)
    print("LLM Provider Test Script")
    print("=" * 60 + "\n")

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python test_llm.py [provider] [api_key] [model]\n")
        print("Providers: openai, openrouter\n")
        print("Examples:")
        print("  python test_llm.py openai sk-... gpt-3.5-turbo")
        print("  python test_llm.py openrouter sk-or-... anthropic/claude-3-5-sonnet")
        print("  python test_llm.py openrouter sk-or-... mistral/mistral-7b\n")
        print("Or set environment variables:")
        print("  export LLM_PROVIDER=openrouter")
        print("  export OPENROUTER_API_KEY=sk-or-...")
        print("  export OPENROUTER_MODEL=anthropic/claude-3-5-sonnet")
        print("  python test_llm.py\n")
        return

    provider = sys.argv[1].lower()

    # Get credentials from command line or environment
    if provider == "openai":
        api_key = sys.argv[2] if len(sys.argv) > 2 else os.getenv("OPENAI_API_KEY")
        model = sys.argv[3] if len(sys.argv) > 3 else os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        if not api_key:
            print("Error: OpenAI API key not provided")
            print("Usage: python test_llm.py openai <api_key> [model]\n")
            return

        success = test_openai(api_key, model)

    elif provider == "openrouter":
        api_key = sys.argv[2] if len(sys.argv) > 2 else os.getenv("OPENROUTER_API_KEY")
        model = sys.argv[3] if len(sys.argv) > 3 else os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

        if not api_key:
            print("Error: OpenRouter API key not provided")
            print("Usage: python test_llm.py openrouter <api_key> [model]\n")
            return

        success = test_openrouter(api_key, model)

    else:
        print(f"Error: Unknown provider '{provider}'")
        print("Supported providers: openai, openrouter\n")
        return

    if success:
        print("✓ Provider test successful!")
        sys.exit(0)
    else:
        print("✗ Provider test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
