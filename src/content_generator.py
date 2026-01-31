"""Content generator using Google Gemini API."""

import os
import json
from typing import Dict, List
from google import genai
from google.genai import types
from src.utils import get_logger

logger = get_logger(__name__)

class ContentGenerator:
    """Generate content for Instagram posts using Gemini."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash-exp"):
        """Initialize the content generator."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        
        # Validate and potentially update model name
        self.model_name = self._validate_and_get_model(model)
        logger.info(f"ContentGenerator initialized with model: {self.model_name}")
    
    def _list_available_models(self) -> List[str]:
        """List all available Gemini models."""
        try:
            models = self.client.models.list()
            available_models = []
            for model in models:
                # Filter for generative models (not embeddings, etc.)
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            return available_models
        except Exception as e:
            logger.warning(f"Failed to list models: {e}")
            return []
    
    def _validate_and_get_model(self, requested_model: str) -> str:
        """
        Validate the requested model and return a working model name.
        Falls back to available alternatives if the requested model is not found.
        
        Note: This method uses heuristics to select a fallback model since we can't
        validate the model without making an API call. The first actual API call
        (generate_content) will verify if the model is valid.
        """
        # List available models and find a suitable alternative if needed
        logger.info(f"Requested model: {requested_model}")
        available_models = self._list_available_models()
        
        if not available_models:
            logger.warning("Could not retrieve available models list, will use requested model")
            # Common fallback models (in order of preference)
            fallback_models = [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-pro",
                "gemini-1.0-pro"
            ]
            
            # Check if requested model is a known good one
            if requested_model in fallback_models:
                logger.info(f"Using requested model (known stable): {requested_model}")
                return requested_model
            
            # Otherwise suggest fallback but use requested model
            for fallback in fallback_models:
                logger.warning(f"Cannot verify model availability. Consider using: {fallback}")
                break
            
            return requested_model
        
        logger.info(f"Available models: {', '.join(available_models)}")
        
        # Check if requested model is in the list
        for model_name in available_models:
            if requested_model in model_name or model_name in requested_model:
                logger.info(f"✓ Found matching model: {model_name}")
                return model_name
        
        # Try to find the latest flash or pro model
        for model_name in available_models:
            if 'flash' in model_name.lower():
                logger.warning(f"Requested model not found. Using alternative: {model_name}")
                logger.warning(f"⚠️  Please update config.yaml to use: {model_name}")
                return model_name
        
        for model_name in available_models:
            if 'pro' in model_name.lower():
                logger.warning(f"Requested model not found. Using alternative: {model_name}")
                logger.warning(f"⚠️  Please update config.yaml to use: {model_name}")
                return model_name
        
        # Last resort: use the first available model
        if available_models:
            logger.warning(f"Using first available model: {available_models[0]}")
            logger.warning(f"⚠️  Please update config.yaml to use: {available_models[0]}")
            return available_models[0]
        
        # If we got here, something is very wrong - use requested model and let it fail with clear error
        logger.error("No suitable model found. Will attempt to use requested model anyway.")
        return requested_model
    
    def generate_content(self, theme: str = "stoic", quote_style: str = "short") -> Dict[str, str]:
        """
        Generate complete content for an Instagram post.
        
        Args:
            theme: Content theme (stoic, motivational, minimalist)
            quote_style: Quote length (short, medium, long)
        
        Returns:
            Dictionary with quote, video_prompt, caption, hashtags, first_comment
        """
        prompt = f"""Generate content for an Instagram Reel about {theme} philosophy.

Requirements:
1. A {quote_style} {theme} quote (max 15 words for short, 30 for medium, 50 for long)
2. A cinematic video prompt for an 8-15 second video (describe a beautiful, minimalist scene that matches the quote's mood)
3. An engaging Instagram caption (include the quote, a brief reflection, emoji, call-to-action)
4. 25 relevant hashtags (mix popular and niche hashtags for {theme} content)
5. A first comment to post (engaging question or call to action)

Return the response as valid JSON with these exact keys:
- "quote": the quote text only
- "video_prompt": cinematic video description
- "caption": full Instagram caption with emojis
- "hashtags": space-separated hashtags
- "first_comment": engaging first comment

Make it authentic, engaging, and optimized for Instagram algorithm."""

        try:
            logger.info(f"Generating content with theme: {theme}, style: {quote_style}")
            logger.info(f"Using model: {self.model_name}")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            content = json.loads(response_text)
            
            # Validate required keys
            required_keys = ["quote", "video_prompt", "caption", "hashtags", "first_comment"]
            for key in required_keys:
                if key not in content:
                    raise ValueError(f"Missing required key: {key}")
            
            logger.info(f"Successfully generated content. Quote: {content['quote'][:50]}...")
            return content
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            logger.warning("Falling back to static content")
            # Return fallback content
            return self._generate_fallback_content(theme)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating content: {error_msg}")
            
            # Provide helpful error messages
            if "404" in error_msg or "NOT_FOUND" in error_msg:
                logger.error(f"❌ Model '{self.model_name}' not found!")
                logger.error("💡 Solution: Update 'gemini_model' in config.yaml to an available model")
                logger.error("   Common models: gemini-1.5-flash, gemini-1.5-pro")
                logger.error(f"   Error details: {error_msg}")
            elif "403" in error_msg or "PERMISSION_DENIED" in error_msg:
                logger.error("❌ API key invalid or permissions denied")
                logger.error("💡 Solution: Check your GOOGLE_API_KEY environment variable")
            elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                logger.error("❌ API quota exceeded or rate limited")
                logger.error("💡 Solution: Wait a few minutes or check your API quota")
            
            logger.warning("Falling back to static content")
            return self._generate_fallback_content(theme)
    
    @staticmethod
    def _generate_fallback_content(theme: str) -> Dict[str, str]:
        """Generate fallback content if API fails."""
        logger.warning("Using fallback content generation")
        
        fallback_quotes = {
            "stoic": "The obstacle is the way.",
            "motivational": "Your only limit is you.",
            "minimalist": "Less is more."
        }
        
        quote = fallback_quotes.get(theme, "The obstacle is the way.")
        
        return {
            "quote": quote,
            "video_prompt": "Cinematic shot of morning fog rolling over mountains, golden hour lighting, slow motion, 4K quality",
            "caption": f"🔥 {quote}\n\nEvery challenge is an opportunity in disguise. What's blocking you today might be exactly what you need to grow tomorrow.\n\n💭 Save this for when you need a reminder.",
            "hashtags": "#stoicquotes #motivation #mindset #growth #wisdom #philosophy #marcusaurelius #stoicism #dailymotivation #successmindset #mindfulness #personalgrowth #selfdevelopment #lifequotes #deepthoughts #motivationalquotes #inspiration #grindset #entrepreneurmindset #mentalhealth #quotes #motivational #dailyquote #mindsetmatters #personaldevelopment",
            "first_comment": "Drop a 🔥 if this resonates with you!"
        }

def main():
    """Test the content generator."""
    generator = ContentGenerator()
    content = generator.generate_content(theme="stoic", quote_style="short")
    
    print("\n=== Generated Content ===")
    print(f"\nQuote: {content['quote']}")
    print(f"\nVideo Prompt: {content['video_prompt']}")
    print(f"\nCaption:\n{content['caption']}")
    print(f"\nHashtags: {content['hashtags']}")
    print(f"\nFirst Comment: {content['first_comment']}")

if __name__ == "__main__":
    main()
