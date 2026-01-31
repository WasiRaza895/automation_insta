#!/usr/bin/env python3
"""Helper script to list available Gemini models for your API key."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from google import genai
from src.utils import get_logger

logger = get_logger(__name__)


def list_available_models():
    """List all available Gemini models that support content generation."""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("\n❌ ERROR: No API key found!")
        print("\n💡 Solution:")
        print("   Set environment variable:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("\n   Or for local testing, create a .env file with:")
        print("   GOOGLE_API_KEY=your-api-key-here")
        print("\n   Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    
    try:
        print("\n" + "=" * 60)
        print("🔍 Listing Available Gemini Models")
        print("=" * 60)
        print(f"\nConnecting to Gemini API...")
        
        client = genai.Client(api_key=api_key)
        
        print("Fetching models list...\n")
        models = client.models.list()
        
        # Filter for models that support generateContent
        generative_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                generative_models.append(model)
        
        if not generative_models:
            print("❌ No models found that support content generation!")
            print("\n💡 This might indicate:")
            print("   1. API key is invalid or expired")
            print("   2. API access is restricted")
            print("   3. You need to enable the Gemini API in your project")
            return False
        
        print(f"✅ Found {len(generative_models)} model(s) that support content generation:\n")
        print("-" * 60)
        
        # Sort by name for better readability
        generative_models.sort(key=lambda m: m.name)
        
        for i, model in enumerate(generative_models, 1):
            print(f"\n{i}. {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            
            # Show supported methods
            methods = ", ".join(model.supported_generation_methods)
            print(f"   Supported Methods: {methods}")
        
        print("\n" + "-" * 60)
        print("\n📝 How to use these models:")
        print("\n1. Choose a model from the list above")
        print("2. Update your config.yaml file:")
        print("\n   api:")
        print(f"     gemini_model: \"{generative_models[0].name}\"  # Example")
        print("\n3. Recommended models:")
        
        # Suggest best models
        recommended = []
        for model in generative_models:
            if 'flash' in model.name.lower():
                recommended.append(f"   - {model.name} (Fast and efficient)")
            elif 'pro' in model.name.lower():
                recommended.append(f"   - {model.name} (More capable)")
        
        if recommended:
            for rec in recommended[:3]:  # Show top 3 recommendations
                print(rec)
        else:
            print(f"   - {generative_models[0].name} (Available)")
        
        print("\n" + "=" * 60)
        print("✅ Done! Update your config.yaml with one of the models above.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ ERROR: Failed to list models")
        print(f"\nDetails: {error_msg}\n")
        
        if "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            print("💡 Your API key appears to be invalid.")
            print("   Get a new key from: https://aistudio.google.com/app/apikey")
        elif "403" in error_msg or "PERMISSION_DENIED" in error_msg:
            print("💡 Your API key doesn't have permission to access Gemini API.")
            print("   Check your API settings at: https://aistudio.google.com/")
        elif "connection" in error_msg.lower() or "network" in error_msg.lower():
            print("💡 Network connection issue. Check your internet connection.")
        else:
            print("💡 Unexpected error. Check your API key and try again.")
        
        return False


def main():
    """Main entry point."""
    print("\n🤖 Gemini Model List Helper")
    print("This script helps you find available models for your API key.\n")
    
    success = list_available_models()
    
    if success:
        sys.exit(0)
    else:
        print("\n⚠️  Failed to list models. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
