# test_setup.py - FIXED VERSION

import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("TESTING SETUP - Interior Design Agent System")
print("="*60)

# Test imports
print("\n1. Testing Package Imports...")
print("-" * 60)

try:
    from crewai import Agent, Task, Crew
    print("✓ CrewAI imported successfully")
except Exception as e:
    print(f"✗ CrewAI import failed: {e}")

try:
    from crewai_tools import SerperDevTool
    print("✓ CrewAI Tools imported successfully")
except Exception as e:
    print(f"✗ CrewAI Tools import failed: {e}")

try:
    import numpy as np
    print(f"✓ NumPy imported successfully (version {np.__version__})")
except Exception as e:
    print(f"✗ NumPy import failed: {e}")

try:
    import pandas as pd
    print(f"✓ Pandas imported successfully (version {pd.__version__})")
except Exception as e:
    print(f"✗ Pandas import failed: {e}")

try:
    import requests
    print("✓ Requests imported successfully")
except Exception as e:
    print(f"✗ Requests import failed: {e}")

try:
    from bs4 import BeautifulSoup
    print("✓ BeautifulSoup imported successfully")
except Exception as e:
    print(f"✗ BeautifulSoup import failed: {e}")

# Test API keys
print("\n2. Testing API Keys...")
print("-" * 60)

groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
xai_key = os.getenv("XAI_API_KEY")
serper_key = os.getenv("SERPER_API_KEY")

# Check for any LLM provider
llm_found = False
provider_name = "None"  # FIXED: Initialize variable

if groq_key and groq_key.startswith("gsk_"):
    print(f"✓ Groq API key found (starts with: {groq_key[:10]}...)")
    llm_found = True
    llm_provider = "groq"
    provider_name = "Groq (FREE & FAST)"
elif openai_key and openai_key.startswith("sk-"):
    print(f"✓ OpenAI API key found (starts with: {openai_key[:10]}...)")
    llm_found = True
    llm_provider = "openai"
    provider_name = "OpenAI"
elif xai_key and xai_key.startswith("xai-"):
    print(f"✓ Grok (X.AI) API key found (starts with: {xai_key[:10]}...)")
    llm_found = True
    llm_provider = "xai"
    provider_name = "Grok (X.AI)"
else:
    print("✗ No LLM API key found")
    print("  → Recommended: Get free Groq API key from https://console.groq.com/")
    print("  → Or use OpenAI API key")

if serper_key and len(serper_key) > 10:
    print(f"✓ Serper API key found (starts with: {serper_key[:10]}...)")
else:
    print("✗ Serper API key missing")
    print("  → Get free key from https://serper.dev/")

# Test LLM connection
print("\n3. Testing LLM Connection...")
print("-" * 60)

if llm_found:
    try:
        print("Attempting to connect to LLM... (this may take a few seconds)")
        
        if llm_provider == "groq":
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",  # NEW MODEL
                temperature=0.7,
                api_key=groq_key
            )
            
        elif llm_provider == "openai":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=openai_key
            )
            
        elif llm_provider == "xai":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model="grok-beta",
                temperature=0.7,
                api_key=xai_key,
                base_url="https://api.x.ai/v1"
            )
        
        response = llm.invoke("Say 'Setup successful!' if you can read this.")
        print(f"✓ {provider_name} connected successfully!")
        print(f"  Response: {response.content}")
        
    except Exception as e:
        print(f"✗ LLM connection failed: {e}")
        print("  → Check if your API key is valid")
else:
    print("⊘ Skipping LLM test (no API key found)")

# Summary
print("\n" + "="*60)
print("SETUP VERIFICATION SUMMARY")
print("="*60)

api_keys_ok = llm_found and serper_key

if api_keys_ok:
    print("✓✓✓ ALL CHECKS PASSED! ✓✓✓")
    print("\nYou're ready to build the Interior Design Agent!")
    print(f"\nUsing: {provider_name}")  # FIXED: This will always be defined now
    print("\nNext Step: Build the Custom Tool (Room Layout Optimizer)")
else:
    print("\n⚠ Some issues found:")
    if not llm_found:
        print("  - No LLM API key found")
        print("    Get free Groq key: https://console.groq.com/")
    if not serper_key:
        print("  - Serper API key missing")
        print("    Get free Serper key: https://serper.dev/")
    print("\nPlease fix these issues before continuing.")

print("="*60)