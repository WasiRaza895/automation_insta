#!/usr/bin/env python3
"""
Example/Demo script for Instagram automation.
This demonstrates how to use individual components.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def demo_content_generation():
    """Demonstrate content generation."""
    print("\n" + "="*60)
    print("DEMO: Content Generation")
    print("="*60)
    
    from src.content_generator import ContentGenerator
    
    try:
        # This will use fallback content if API key not set
        content = ContentGenerator._generate_fallback_content('stoic')
        
        print(f"\n📝 Generated Content:")
        print(f"\nQuote: \"{content['quote']}\"")
        print(f"\nCaption:\n{content['caption']}")
        print(f"\nHashtags: {content['hashtags'][:100]}...")
        print(f"\nFirst Comment: {content['first_comment']}")
        
        return content
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def demo_video_creation(quote: str):
    """Demonstrate video creation."""
    print("\n" + "="*60)
    print("DEMO: Video Creation")
    print("="*60)
    
    from src.video_processor import VideoProcessor
    
    try:
        processor = VideoProcessor()
        
        # Create output directory
        Path('output').mkdir(exist_ok=True)
        
        print(f"\n🎬 Creating video with quote: \"{quote}\"")
        print("⏳ This may take 5-10 seconds...")
        
        video_path = processor.create_placeholder_video(
            text=quote,
            duration=5,  # Short demo video
            output_path='output/demo_video.mp4'
        )
        
        if Path(video_path).exists():
            size_kb = Path(video_path).stat().st_size / 1024
            print(f"\n✅ Video created: {video_path}")
            print(f"📦 File size: {size_kb:.1f} KB")
            return video_path
        else:
            print("❌ Video creation failed")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_session_management():
    """Demonstrate session management."""
    print("\n" + "="*60)
    print("DEMO: Session Management")
    print("="*60)
    
    from src.session_manager import SessionManager
    
    try:
        manager = SessionManager()
        
        # Demo saving a session
        test_session = {
            "user_id": "12345",
            "device_id": "device_12345",
            "session_token": "demo_token"
        }
        
        print("\n💾 Saving demo session...")
        manager.save_session("demo_user", test_session)
        print("✅ Session saved")
        
        print("\n📂 Loading demo session...")
        loaded_session = manager.load_session("demo_user")
        
        if loaded_session:
            print("✅ Session loaded successfully")
            print(f"Session data: {loaded_session}")
        else:
            print("❌ Session not found")
        
        # Cleanup
        print("\n🗑️ Cleaning up demo session...")
        manager.delete_session("demo_user")
        print("✅ Cleanup complete")
        
    except Exception as e:
        print(f"Error: {e}")

def demo_config_loading():
    """Demonstrate configuration loading."""
    print("\n" + "="*60)
    print("DEMO: Configuration Loading")
    print("="*60)
    
    try:
        import yaml
        
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("\n⚙️ Configuration:")
        print(f"  - Content theme: {config['content']['theme']}")
        print(f"  - Quote style: {config['content']['quote_style']}")
        print(f"  - Video duration: {config['video']['duration']}s")
        print(f"  - Font size: {config['video']['font_size']}px")
        print(f"  - Max posts per day: {config['safety']['max_posts_per_day']}")
        print(f"  - Gemini model: {config['api']['gemini_model']}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all demos."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "INSTAGRAM AUTOMATION DEMO" + " "*21 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\nThis demo shows how individual components work.")
    print("Set environment variables to test with real APIs.\n")
    
    # Demo 1: Content Generation
    content = demo_content_generation()
    
    # Demo 2: Video Creation
    if content:
        video_path = demo_video_creation(content['quote'])
    
    # Demo 3: Session Management
    demo_session_management()
    
    # Demo 4: Config Loading
    demo_config_loading()
    
    # Summary
    print("\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    print("\n✅ All demos completed!")
    print("\nNext steps:")
    print("1. Set your API keys and credentials in environment variables")
    print("2. Run: python test_setup.py  # To validate setup")
    print("3. Run: python main.py         # To execute full automation")
    print("\nFor testing without Instagram upload:")
    print("  - Comment out the upload section in main.py")
    print("  - The system will generate content and videos locally")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
