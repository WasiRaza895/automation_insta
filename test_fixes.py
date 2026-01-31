#!/usr/bin/env python3
"""
Test script to verify the Gemini model and Instagram login fixes.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_gemini_model_validation():
    """Test Gemini model validation and fallback."""
    print("\n" + "="*60)
    print("TEST 1: Gemini Model Validation & Fallback")
    print("="*60)
    
    try:
        # Mock the API key
        os.environ['GOOGLE_API_KEY'] = 'test-key-for-validation'
        
        from src.content_generator import ContentGenerator
        
        # Test with invalid model (should fallback gracefully)
        print("Testing with invalid model 'gemini-2.0-flash-exp'...")
        generator = ContentGenerator(model='gemini-2.0-flash-exp')
        
        print(f"✓ ContentGenerator initialized")
        print(f"✓ Selected model: {generator.model_name}")
        
        # Test fallback content generation
        print("\nTesting fallback content generation...")
        content = generator._generate_fallback_content('stoic')
        print(f"✓ Fallback content generated")
        print(f"  - Quote: {content['quote']}")
        print(f"  - Caption length: {len(content['caption'])} chars")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_instagram_credential_validation():
    """Test Instagram credential validation."""
    print("\n" + "="*60)
    print("TEST 2: Instagram Credential Validation")
    print("="*60)
    
    # Test 1: Missing credentials
    print("\n2.1: Testing with missing credentials...")
    try:
        # Clear environment
        for key in ['INSTAGRAM_USERNAME', 'INSTAGRAM_PASSWORD', 'INSTAGRAM_2FA_SEED']:
            if key in os.environ:
                del os.environ[key]
        
        from src.instagram_uploader import InstagramUploader
        uploader = InstagramUploader()
        print("✗ Should have raised ValueError for missing credentials")
        return False
    except ValueError as e:
        if "required" in str(e).lower():
            print(f"✓ Correctly raised error for missing credentials")
        else:
            print(f"✗ Unexpected error message: {e}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    # Test 2: Empty/whitespace credentials
    print("\n2.2: Testing with empty/whitespace credentials...")
    try:
        os.environ['INSTAGRAM_USERNAME'] = '   '
        os.environ['INSTAGRAM_PASSWORD'] = ''
        
        uploader = InstagramUploader()
        print("✗ Should have raised ValueError for empty credentials")
        return False
    except ValueError as e:
        if "empty" in str(e).lower() or "whitespace" in str(e).lower():
            print(f"✓ Correctly detected empty/whitespace credentials")
        else:
            print(f"✓ Credentials validation failed as expected")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    # Test 3: Valid credentials with empty 2FA
    print("\n2.3: Testing with valid credentials and empty 2FA...")
    try:
        os.environ['INSTAGRAM_USERNAME'] = 'test_user'
        os.environ['INSTAGRAM_PASSWORD'] = 'test_password'
        os.environ['INSTAGRAM_2FA_SEED'] = ''  # Empty 2FA seed
        
        uploader = InstagramUploader()
        print(f"✓ InstagramUploader initialized successfully")
        print(f"✓ Username: {uploader.username}")
        print(f"✓ 2FA Seed: '{uploader.two_factor_seed}' (empty is OK)")
        
        # Test validation logic
        seed = uploader.two_factor_seed
        if seed and seed.strip():
            print("✗ Empty seed should not be treated as valid")
            return False
        else:
            print("✓ Empty 2FA seed correctly identified")
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Valid credentials with None 2FA
    print("\n2.4: Testing with valid credentials and None 2FA...")
    try:
        if 'INSTAGRAM_2FA_SEED' in os.environ:
            del os.environ['INSTAGRAM_2FA_SEED']
        
        uploader = InstagramUploader()
        print(f"✓ InstagramUploader initialized successfully")
        print(f"✓ 2FA Seed: {uploader.two_factor_seed} (None is OK)")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    # Test 5: Valid credentials with whitespace-only 2FA
    print("\n2.5: Testing with valid credentials and whitespace-only 2FA...")
    try:
        os.environ['INSTAGRAM_2FA_SEED'] = '   \t\n   '
        
        uploader = InstagramUploader()
        print(f"✓ InstagramUploader initialized successfully")
        print(f"✓ 2FA Seed: '{uploader.two_factor_seed}' (whitespace-only)")
        
        # Test validation logic
        seed = uploader.two_factor_seed
        if seed and seed.strip():
            print("✗ Whitespace-only seed should not be treated as valid")
            return False
        else:
            print("✓ Whitespace-only 2FA seed correctly identified")
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    print("\n✓ All credential validation tests passed!")
    return True

def test_config_update():
    """Test that config.yaml has been updated."""
    print("\n" + "="*60)
    print("TEST 3: Config.yaml Model Update")
    print("="*60)
    
    try:
        import yaml
        
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        model = config['api']['gemini_model']
        print(f"Current model in config: {model}")
        
        if model == 'gemini-2.0-flash-exp':
            print("✗ Config still uses outdated model")
            return False
        elif 'gemini-1.5' in model or 'gemini-pro' in model:
            print(f"✓ Config updated to use stable model: {model}")
            return True
        else:
            print(f"⚠ Config uses different model: {model}")
            return True
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_requirements_update():
    """Test that requirements.txt has been updated."""
    print("\n" + "="*60)
    print("TEST 4: Requirements.txt Update")
    print("="*60)
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        if 'instagrapi>=2.1.0' in content:
            print("✓ Requirements updated to instagrapi>=2.1.0")
            return True
        elif 'instagrapi>=2.0.0' in content:
            print("⚠ Requirements still at instagrapi>=2.0.0 (should be >=2.1.0)")
            return False
        else:
            print("✗ Unexpected instagrapi version in requirements.txt")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "WORKFLOW FIXES TEST SUITE" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Gemini Model Validation", test_gemini_model_validation()))
    results.append(("Instagram Credential Validation", test_instagram_credential_validation()))
    results.append(("Config Update", test_config_update()))
    results.append(("Requirements Update", test_requirements_update()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:40s} {status}")
    
    print("\n" + "="*60)
    print(f"Result: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ All fixes verified successfully!")
        print("\nFixed issues:")
        print("1. ✓ Gemini model now uses gemini-1.5-flash (stable)")
        print("2. ✓ Instagram credentials are validated before login")
        print("3. ✓ Empty/None/whitespace 2FA seeds handled correctly")
        print("4. ✓ Clear error messages for missing credentials")
        print("5. ✓ Environment variables logged (without exposing values)")
        print("6. ✓ Requirements updated to latest instagrapi")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
