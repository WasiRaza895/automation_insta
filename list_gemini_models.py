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
        logger.error("No API key found!")
        logger.info("Solution:")
        logger.info("  Set environment variable:")
        logger.info("  export GOOGLE_API_KEY='your-api-key-here'")
        logger.info("")
        logger.info("  Or for local testing, create a .env file with:")
        logger.info("  GOOGLE_API_KEY=your-api-key-here")
        logger.info("")
        logger.info("  Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    
    try:
        logger.info("=" * 60)
        logger.info("🔍 Listing Available Gemini Models")
        logger.info("=" * 60)
        logger.info("Connecting to Gemini API...")
        
        client = genai.Client(api_key=api_key)
        
        logger.info("Fetching models list...")
        models = client.models.list()
        
        # Filter for models that support generateContent
        generative_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                generative_models.append(model)
        
        if not generative_models:
            logger.error("No models found that support content generation!")
            logger.info("This might indicate:")
            logger.info("  1. API key is invalid or expired")
            logger.info("  2. API access is restricted")
            logger.info("  3. You need to enable the Gemini API in your project")
            return False
        
        logger.info(f"✅ Found {len(generative_models)} model(s) that support content generation:")
        logger.info("-" * 60)
        
        # Sort by name for better readability
        generative_models.sort(key=lambda m: m.name)
        
        for i, model in enumerate(generative_models, 1):
            # Strip "models/" prefix for cleaner display
            model_name = model.name.replace("models/", "")
            logger.info(f"\n{i}. {model_name}")
            logger.info(f"   Display Name: {model.display_name}")
            logger.info(f"   Description: {model.description}")
            
            # Show supported methods
            methods = ", ".join(model.supported_generation_methods)
            logger.info(f"   Supported Methods: {methods}")
        
        logger.info("\n" + "-" * 60)
        logger.info("\n📝 How to use these models:")
        logger.info("\n1. Choose a model from the list above")
        logger.info("2. Update your config.yaml file:")
        logger.info("\n   api:")
        # Strip "models/" prefix to match config format
        example_model = generative_models[0].name.replace("models/", "")
        logger.info(f"     gemini_model: \"{example_model}\"  # Example")
        logger.info("\n3. Recommended models:")
        
        # Suggest best models
        recommended = []
        for model in generative_models:
            model_name = model.name.replace("models/", "")
            if 'flash' in model.name.lower():
                recommended.append(f"   - {model_name} (Fast and efficient)")
            elif 'pro' in model.name.lower():
                recommended.append(f"   - {model_name} (More capable)")
        
        if recommended:
            for rec in recommended[:3]:  # Show top 3 recommendations
                logger.info(rec)
        else:
            model_name = generative_models[0].name.replace("models/", "")
            logger.info(f"   - {model_name} (Available)")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Done! Update your config.yaml with one of the models above.")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        logger.error("Failed to list models")
        logger.error(f"Details: {error_msg}")
        
        if "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            logger.info("💡 Your API key appears to be invalid.")
            logger.info("   Get a new key from: https://aistudio.google.com/app/apikey")
        elif "403" in error_msg or "PERMISSION_DENIED" in error_msg:
            logger.info("💡 Your API key doesn't have permission to access Gemini API.")
            logger.info("   Check your API settings at: https://aistudio.google.com/")
        elif "connection" in error_msg.lower() or "network" in error_msg.lower():
            logger.info("💡 Network connection issue. Check your internet connection.")
        else:
            logger.info("💡 Unexpected error. Check your API key and try again.")
        
        return False


def main():
    """Main entry point."""
    logger.info("\n🤖 Gemini Model List Helper")
    logger.info("This script helps you find available models for your API key.\n")
    
    success = list_available_models()
    
    if success:
        sys.exit(0)
    else:
        logger.warning("Failed to list models. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
