#!/usr/bin/env python3
"""
Test script to validate Instagram automation setup.
Run this to test individual components before running the full automation.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required packages can be imported."""
    print("\n" + "="*60)
    print("TEST 1: Checking Python package imports")
    print("="*60)
    
    packages = [
        ("google.genai", "Google Gemini API"),
        ("instagrapi", "Instagram API"),
        ("moviepy", "Video processing"),
        ("PIL", "Image processing"),
        ("yaml", "Configuration"),
    ]
    
    all_good = True
    for package, name in packages:
        try:
            __import__(package)
            print(f"✓ {name:30s} - OK")
        except ImportError as e:
            print(f"✗ {name:30s} - MISSING: {e}")
            all_good = False
    
    return all_good

def test_content_generator():
    """Test content generation with fallback."""
    print("\n" + "="*60)
    print("TEST 2: Content Generation (Fallback)")
    print("="*60)
    
    try:
        from src.content_generator import ContentGenerator
        
        # Test fallback content generation
        content = ContentGenerator._generate_fallback_content('stoic')
        
        print(f"✓ Quote: {content['quote']}")
        print(f"✓ Caption length: {len(content['caption'])} chars")
        print(f"✓ Hashtags: {len(content['hashtags'].split())} tags")
        print(f"✓ Video prompt: {content['video_prompt'][:60]}...")
        print("\n✓ Content generation works!")
        return True
        
    except Exception as e:
        print(f"✗ Content generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_processor():
    """Test video creation."""
    print("\n" + "="*60)
    print("TEST 3: Video Processing")
    print("="*60)
    
    try:
        from src.video_processor import VideoProcessor
        
        processor = VideoProcessor()
        print("✓ VideoProcessor initialized")
        
        # Create a very short test video
        Path('output').mkdir(exist_ok=True)
        video_path = processor.create_placeholder_video(
            text='Test Quote',
            duration=3,
            output_path='output/test_validation.mp4'
        )
        
        if Path(video_path).exists():
            size_kb = Path(video_path).stat().st_size / 1024
            print(f"✓ Test video created: {video_path}")
            print(f"✓ File size: {size_kb:.1f} KB")
            
            # Cleanup
            Path(video_path).unlink()
            print("✓ Test cleanup complete")
            return True
        else:
            print("✗ Video file not created")
            return False
            
    except Exception as e:
        print(f"✗ Video processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading."""
    print("\n" + "="*60)
    print("TEST 4: Configuration")
    print("="*60)
    
    try:
        import yaml
        
        config_path = Path('config.yaml')
        if not config_path.exists():
            print("✗ config.yaml not found")
            return False
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✓ Config loaded successfully")
        print(f"  - Theme: {config['content']['theme']}")
        print(f"  - Video duration: {config['video']['duration']}s")
        print(f"  - Max posts per day: {config['safety']['max_posts_per_day']}")
        return True
        
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_environment():
    """Test environment variables."""
    print("\n" + "="*60)
    print("TEST 5: Environment Variables")
    print("="*60)
    
    required = {
        'GOOGLE_API_KEY or GEMINI_API_KEY': ['GOOGLE_API_KEY', 'GEMINI_API_KEY'],
        'INSTAGRAM_USERNAME': ['INSTAGRAM_USERNAME'],
        'INSTAGRAM_PASSWORD': ['INSTAGRAM_PASSWORD'],
    }
    
    all_set = True
    for name, env_vars in required.items():
        found = any(os.getenv(var) for var in env_vars)
        if found:
            print(f"✓ {name:30s} - SET")
        else:
            print(f"⚠ {name:30s} - NOT SET (required for full automation)")
            if 'GOOGLE' in name or 'GEMINI' in name:
                all_set = False
    
    # Optional
    if os.getenv('INSTAGRAM_2FA_SEED'):
        print(f"✓ {'INSTAGRAM_2FA_SEED':30s} - SET (2FA enabled)")
    else:
        print(f"  {'INSTAGRAM_2FA_SEED':30s} - NOT SET (optional)")
    
    return all_set

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "INSTAGRAM AUTOMATION TEST" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Content Generation", test_content_generator()))
    results.append(("Video Processing", test_video_processor()))
    results.append(("Configuration", test_config()))
    results.append(("Environment", test_environment()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:30s} {status}")
    
    print("\n" + "="*60)
    print(f"Result: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Set environment variables (if not already set)")
        print("2. Run: python main.py")
        print("3. Check output/ directory for generated video")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before running.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set environment variables in .env file or export them")
        print("3. Check README.md for detailed setup instructions")
        return 1

if __name__ == "__main__":
    sys.exit(main())
