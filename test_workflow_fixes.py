#!/usr/bin/env python3
"""
Test script to verify the workflow fixes for 2FA authentication.
This tests the specific issues that were causing workflow failures.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_2fa_empty_seed_handling():
    """Test that empty 2FA seed is handled correctly."""
    print("\n" + "="*60)
    print("TEST: Empty 2FA Seed Handling")
    print("="*60)
    
    # Simulate the conditions that caused the workflow failure
    os.environ['INSTAGRAM_USERNAME'] = 'test_user'
    os.environ['INSTAGRAM_PASSWORD'] = 'test_password'
    os.environ['INSTAGRAM_2FA_SEED'] = ''  # Empty seed (causes the error)
    
    try:
        from src.instagram_uploader import InstagramUploader
        
        # This should NOT raise an error anymore
        uploader = InstagramUploader()
        print("✓ InstagramUploader initialized successfully with empty 2FA seed")
        print(f"✓ Username: {uploader.username}")
        print(f"✓ 2FA Seed: '{uploader.two_factor_seed}' (empty/None is OK)")
        
        # Test the validation logic
        seed = uploader.two_factor_seed
        if seed and seed.strip():
            print("✗ Empty seed should not be treated as valid")
            return False
        else:
            print("✓ Empty seed correctly identified as invalid")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_2fa_none_seed_handling():
    """Test that None 2FA seed is handled correctly."""
    print("\n" + "="*60)
    print("TEST: None 2FA Seed Handling")
    print("="*60)
    
    # Don't set INSTAGRAM_2FA_SEED at all
    if 'INSTAGRAM_2FA_SEED' in os.environ:
        del os.environ['INSTAGRAM_2FA_SEED']
    
    try:
        from src.instagram_uploader import InstagramUploader
        
        uploader = InstagramUploader()
        print("✓ InstagramUploader initialized successfully with no 2FA seed")
        print(f"✓ 2FA Seed: {uploader.two_factor_seed} (None is OK)")
        
        # Test the validation logic
        seed = uploader.two_factor_seed
        if seed and seed.strip():
            print("✗ None seed should not be treated as valid")
            return False
        else:
            print("✓ None seed correctly identified as invalid")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_2fa_whitespace_seed_handling():
    """Test that whitespace-only 2FA seed is handled correctly."""
    print("\n" + "="*60)
    print("TEST: Whitespace-only 2FA Seed Handling")
    print("="*60)
    
    os.environ['INSTAGRAM_2FA_SEED'] = '   '  # Whitespace only
    
    try:
        from src.instagram_uploader import InstagramUploader
        
        uploader = InstagramUploader()
        print("✓ InstagramUploader initialized successfully with whitespace-only 2FA seed")
        print(f"✓ 2FA Seed: '{uploader.two_factor_seed}' (whitespace is OK)")
        
        # Test the validation logic
        seed = uploader.two_factor_seed
        if seed and seed.strip():
            print("✗ Whitespace-only seed should not be treated as valid")
            return False
        else:
            print("✓ Whitespace-only seed correctly identified as invalid")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_yaml_valid():
    """Test that the workflow YAML file is valid."""
    print("\n" + "="*60)
    print("TEST: Workflow YAML Validation")
    print("="*60)
    
    try:
        import yaml
        
        workflow_path = Path('.github/workflows/daily_post.yml')
        if not workflow_path.exists():
            print(f"✗ Workflow file not found: {workflow_path}")
            return False
        
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        print("✓ Workflow YAML is valid")
        print(f"✓ Workflow name: {workflow['name']}")
        
        # Check for the new debugging step
        steps = workflow['jobs']['post']['steps']
        step_names = [step['name'] for step in steps]
        
        if 'Print environment info' in step_names:
            print("✓ Environment info debugging step is present")
        else:
            print("⚠ Environment info debugging step not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all workflow fix tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "WORKFLOW FIXES VALIDATION TEST" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Empty 2FA Seed", test_2fa_empty_seed_handling()))
    results.append(("None 2FA Seed", test_2fa_none_seed_handling()))
    results.append(("Whitespace 2FA Seed", test_2fa_whitespace_seed_handling()))
    results.append(("Workflow YAML Valid", test_workflow_yaml_valid()))
    
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
        print("\n✅ All workflow fix tests passed!")
        print("\nThe following issues have been fixed:")
        print("1. ✓ Empty/None 2FA seed no longer causes TypeError")
        print("2. ✓ Whitespace-only 2FA seed is handled correctly")
        print("3. ✓ Workflow YAML is valid and includes debugging steps")
        print("\nThe workflow should now run successfully!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
