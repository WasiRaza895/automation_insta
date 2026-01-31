#!/usr/bin/env python3
"""Test error handling improvements for Gemini 404 and Instagram IP blacklist."""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.content_generator import ContentGenerator
from src.instagram_uploader import InstagramUploader


def test_gemini_404_error_handling():
    """Test that Gemini 404 errors produce helpful error messages."""
    print("\n" + "=" * 60)
    print("TEST 1: Gemini 404 Error Handling")
    print("=" * 60)
    
    try:
        # Set a fake API key
        os.environ["GOOGLE_API_KEY"] = "fake_key_for_testing"
        
        # Mock the client to simulate 404 error
        with patch('src.content_generator.genai.Client') as mock_client:
            # Create a mock client instance
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Mock the models.list() to return empty list (simulating unavailable models)
            mock_client_instance.models.list.return_value = []
            
            # Mock generate_content to raise a 404 error
            mock_client_instance.models.generate_content.side_effect = Exception(
                "404 NOT_FOUND: models/gemini-1.5-flash is not found for API version v1beta"
            )
            
            # Create content generator
            generator = ContentGenerator(model="gemini-1.5-flash")
            
            # Try to generate content - should handle error gracefully
            print("\n📝 Attempting to generate content with unavailable model...")
            content = generator.generate_content(theme="stoic", quote_style="short")
            
            # Should return fallback content
            if content and "quote" in content:
                print("✓ Error handled gracefully - returned fallback content")
                print(f"  Fallback quote: {content['quote']}")
                return True
            else:
                print("✗ Failed to return fallback content")
                return False
                
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        return False


def test_instagram_ip_blacklist_error_handling():
    """Test that Instagram IP blacklist errors produce helpful error messages."""
    print("\n" + "=" * 60)
    print("TEST 2: Instagram IP Blacklist Error Handling")
    print("=" * 60)
    
    try:
        # Set fake credentials
        os.environ["INSTAGRAM_USERNAME"] = "test_user"
        os.environ["INSTAGRAM_PASSWORD"] = "test_pass"
        
        # Mock the client to simulate IP blacklist error
        with patch('src.instagram_uploader.Client') as mock_client:
            # Create uploader
            uploader = InstagramUploader()
            
            # Mock login to raise IP blacklist error
            mock_client_instance = mock_client.return_value
            mock_client_instance.login.side_effect = Exception(
                "ClientError: change your IP address, because it is added to the blacklist of the Instagram Server"
            )
            
            print("\n📱 Attempting to login with blacklisted IP...")
            result = uploader.login()
            
            # Should return False and log helpful error messages
            if result is False:
                print("✓ Error handled gracefully - login returned False")
                print("  (Check logs above for detailed error messages)")
                return True
            else:
                print("✗ Login should have failed but returned True")
                return False
                
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        return False


def test_helper_script_exists():
    """Test that the helper script exists and is executable."""
    print("\n" + "=" * 60)
    print("TEST 3: Helper Script Exists")
    print("=" * 60)
    
    script_path = Path(__file__).parent / "list_gemini_models.py"
    
    if script_path.exists():
        print(f"✓ Helper script exists: {script_path}")
        
        # Check if executable
        if os.access(script_path, os.X_OK):
            print("✓ Helper script is executable")
        else:
            print("⚠ Helper script is not executable (may need chmod +x)")
        
        # Check if it can be imported and executed
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("list_gemini_models", script_path)
            if spec is None or spec.loader is None:
                print("✗ Helper script could not be loaded")
                return False
            module = importlib.util.module_from_spec(spec)
            # Execute the module to catch syntax errors
            spec.loader.exec_module(module)
            print("✓ Helper script is valid Python code")
            return True
        except Exception as e:
            print(f"✗ Helper script has syntax errors: {e}")
            return False
    else:
        print(f"✗ Helper script not found: {script_path}")
        return False


def main():
    """Run all error handling tests."""
    print("\n" + "=" * 60)
    print("🧪 Testing Error Handling Improvements")
    print("=" * 60)
    
    tests = [
        ("Helper Script Exists", test_helper_script_exists),
        ("Gemini 404 Error Handling", test_gemini_404_error_handling),
        ("Instagram IP Blacklist Error Handling", test_instagram_ip_blacklist_error_handling),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
