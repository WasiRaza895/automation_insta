"""Content generator using Google Gemini API."""

import os
import json
from typing import Dict
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
        self.model_name = model
        logger.info(f"ContentGenerator initialized with model: {model}")
    
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
            # Return fallback content
            return self._generate_fallback_content(theme)
        except Exception as e:
            logger.error(f"Error generating content: {e}")
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
