# src/config/llm_config.py
"""
LLM Configuration - Supports multiple providers
"""
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.3):
    """
    Get LLM instance based on available API keys.
    Priority: Groq > OpenAI > Grok
    """
    
    # Check for Groq API key (RECOMMENDED - FREE & FAST)
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            print("✓ Using Groq (FREE) as LLM provider")
            return ChatGroq(
                model="llama-3.1-8b-instant",  # Great free model
                temperature=0.3,
                api_key=groq_key
            )
        except ImportError:
            print("⚠ langchain-groq not installed. Run: pip install langchain-groq")
    
    # Check for OpenAI (if you have it)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        from langchain_openai import ChatOpenAI
        print("✓ Using OpenAI as LLM provider")
        return ChatOpenAI(
            model="gpt-4",
            temperature=temperature,
            api_key=openai_key
        )
    
    # Check for Grok/X.AI (requires X account)
    xai_key = os.getenv("XAI_API_KEY")
    if xai_key:
        from langchain_openai import ChatOpenAI
        print("✓ Using Grok (X.AI) as LLM provider")
        return ChatOpenAI(
            model="grok-beta",
            temperature=temperature,
            api_key=xai_key,
            base_url="https://api.x.ai/v1"
        )
    
    raise ValueError(
        "No API key found! Please add one of these to .env file:\n"
        "  - GROQ_API_KEY (recommended - free)\n"
        "  - OPENAI_API_KEY (paid)\n"
        "  - XAI_API_KEY (free but needs X account)"
    )