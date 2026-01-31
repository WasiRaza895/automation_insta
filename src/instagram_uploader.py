"""Instagram uploader using instagrapi library."""

import os
import time
from pathlib import Path
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, ChallengeRequired, PleaseWaitFewMinutes,
    ClientError
)
import pyotp
from src.utils import get_logger, random_delay
from src.session_manager import SessionManager

logger = get_logger(__name__)

class InstagramUploader:
    """Upload content to Instagram."""
    
    def __init__(self, username: str = None, password: str = None, 
                 two_factor_seed: str = None, config: dict = None):
        """
        Initialize the Instagram uploader.
        
        Args:
            username: Instagram username
            password: Instagram password
            two_factor_seed: 2FA seed (optional)
            config: Configuration dictionary
        """
        self.username = username or os.getenv("INSTAGRAM_USERNAME")
        self.password = password or os.getenv("INSTAGRAM_PASSWORD")
        self.two_factor_seed = two_factor_seed or os.getenv("INSTAGRAM_2FA_SEED")
        self.config = config or {}
        
        # Validate credentials with helpful error messages
        self._validate_credentials()
        
        self.client = Client()
        self.session_manager = SessionManager()
        self.logged_in = False
        
        logger.info(f"InstagramUploader initialized for user: {self.username}")
        
        # Log environment variable status (without exposing values)
        self._log_env_status()
    
    def _is_ip_blacklist_error(self, error_msg: str) -> bool:
        """Check if error message indicates IP blacklist or action blocked."""
        return any(keyword in error_msg.lower() for keyword in [
            "ip address", "blacklist", "suspicious", "spam", 
            "action blocked", "try again later", "unusual activity"
        ])
    
    def _log_ip_blacklist_guidance(self):
        """Log comprehensive guidance for IP blacklist errors."""
        logger.error("=" * 60)
        logger.error("🚫 IP ADDRESS BLACKLISTED OR ACTION BLOCKED")
        logger.error("=" * 60)
        logger.error("\n⚠️  Instagram has flagged your IP address as suspicious.")
        logger.error("   This is common when using automation from:")
        logger.error("   • GitHub Actions runners (cloud IPs)")
        logger.error("   • VPS/cloud hosting (flagged data center IPs)")
        logger.error("   • Multiple failed login attempts")
        logger.error("   • Rapid/bot-like activity patterns")
        logger.error("\n💡 SOLUTIONS:")
        logger.error("\n   Option 1: Run from a trusted local IP")
        logger.error("   ----------------------------------------")
        logger.error("   1. Clone the repository to your local machine")
        logger.error("   2. Set up environment variables locally:")
        logger.error("      export INSTAGRAM_USERNAME='your_username'")
        logger.error("      export INSTAGRAM_PASSWORD='your_password'")
        logger.error("      export GOOGLE_API_KEY='your_api_key'")
        logger.error("   3. Run: python run_now.py")
        logger.error("   4. Use your home/mobile network (not VPN/proxy)")
        logger.error("\n   Option 2: Recover your Instagram account")
        logger.error("   ----------------------------------------")
        logger.error("   1. Open Instagram app or website")
        logger.error("   2. Complete any security challenges/verifications")
        logger.error("   3. You may need to reset password or verify via email/SMS")
        logger.error("   4. Wait 24-48 hours before trying automation again")
        logger.error("\n   Option 3: Prevent future blocks")
        logger.error("   ----------------------------------------")
        logger.error("   1. Use Instagram Business/Creator account (more tolerant)")
        logger.error("   2. Reduce posting frequency in config.yaml:")
        logger.error("      safety:")
        logger.error("        max_posts_per_day: 1  # Start with 1 post/day")
        logger.error("   3. Increase delays between actions:")
        logger.error("      safety:")
        logger.error("        min_delay_seconds: 120")
        logger.error("        max_delay_seconds: 300")
        logger.error("   4. Build trust: Post manually from mobile app for a few days")
        logger.error("   5. Verify account with phone number and email")
        logger.error("\n   ⚠️  IMPORTANT:")
        logger.error("   • DO NOT keep retrying from the same blocked IP")
        logger.error("   • DO NOT use multiple accounts from same IP")
        logger.error("   • DO NOT ignore Instagram's security warnings")
        logger.error("   • Repeated violations may lead to permanent account ban")
        logger.error("\n   For GitHub Actions: Consider running automation less")
        logger.error("   frequently (once per day max) or switch to local execution")
        logger.error("   from a residential IP address.")
        logger.error("=" * 60)
    
    def _validate_credentials(self):
        """Validate that required credentials are present."""
        errors = []
        
        if not self.username:
            errors.append("INSTAGRAM_USERNAME is not set")
        elif not self.username.strip():
            errors.append("INSTAGRAM_USERNAME is empty or whitespace only")
        
        if not self.password:
            errors.append("INSTAGRAM_PASSWORD is not set")
        elif not self.password.strip():
            errors.append("INSTAGRAM_PASSWORD is empty or whitespace only")
        
        if errors:
            error_msg = "Instagram credentials validation failed:\n"
            for error in errors:
                error_msg += f"  ❌ {error}\n"
            error_msg += "\n💡 Solution:\n"
            error_msg += "  1. Set environment variables: INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD\n"
            error_msg += "  2. For GitHub Actions: Add these as repository secrets\n"
            error_msg += "  3. For local testing: Export them or add to .env file\n"
            logger.error(error_msg)
            raise ValueError("Instagram username and password are required")
    
    def _log_env_status(self):
        """Log which environment variables are set (without exposing values)."""
        logger.info("Environment variable status:")
        logger.info(f"  INSTAGRAM_USERNAME: {'✓ SET' if self.username else '✗ NOT SET'}")
        logger.info(f"  INSTAGRAM_PASSWORD: {'✓ SET' if self.password else '✗ NOT SET'}")
        
        # Check 2FA seed status more carefully
        if self.two_factor_seed and self.two_factor_seed.strip():
            logger.info(f"  INSTAGRAM_2FA_SEED: ✓ SET (2FA enabled)")
        else:
            logger.info(f"  INSTAGRAM_2FA_SEED: ○ NOT SET (2FA disabled)")
    
    def login(self) -> bool:
        """
        Login to Instagram with session management.
        
        Returns:
            True if login successful
        """
        try:
            # Try to load existing session
            session = self.session_manager.load_session(self.username)
            
            if session:
                logger.info("Loading existing session...")
                self.client.set_settings(session)
                self.client.login(self.username, self.password)
                
                # Verify session is valid
                try:
                    self.client.get_timeline_feed()
                    logger.info("Session is valid, login successful")
                    self.logged_in = True
                    return True
                except Exception as e:
                    logger.warning(f"Session expired or invalid: {e}")
                    # Continue to fresh login
            
            # Fresh login
            logger.info("Performing fresh login...")
            
            # Set device settings to avoid detection
            self.client.delay_range = [1, 3]
            
            # Check if 2FA is configured and valid
            has_2fa = self.two_factor_seed and self.two_factor_seed.strip()
            
            # Login with or without 2FA
            if has_2fa:
                logger.info("2FA is enabled, generating code...")
                try:
                    totp = pyotp.TOTP(self.two_factor_seed)
                    two_factor_code = totp.now()
                    
                    # Validate the code is numeric and has proper length (typically 6 digits)
                    # Note: pyotp returns codes as strings, which may have leading zeros
                    if not two_factor_code or not two_factor_code.isdigit() or len(two_factor_code) != 6:
                        raise ValueError(f"Generated 2FA code is invalid (length: {len(two_factor_code) if two_factor_code else 0})")
                    
                    logger.info(f"Generated 2FA code (length: {len(two_factor_code)})")
                    self.client.login(self.username, self.password, verification_code=two_factor_code)
                    
                except (TypeError, ValueError, AttributeError) as e:
                    # These errors indicate invalid/malformed 2FA seed
                    logger.warning(f"2FA seed appears invalid or malformed: {e}")
                    logger.warning(f"Error type: {type(e).__name__}")
                    logger.info("Attempting login without 2FA code...")
                    logger.info("💡 If you have 2FA enabled, check your INSTAGRAM_2FA_SEED format")
                    logger.info("   Expected format: Base32 encoded string (e.g., JBSWY3DPEHPK3PXP)")
                    
                    # Try login without 2FA
                    try:
                        self.client.login(self.username, self.password)
                    except Exception as login_error:
                        logger.error(f"Login failed without 2FA: {login_error}")
                        logger.error("If your account has 2FA enabled, you must provide a valid 2FA seed")
                        raise
                        
            else:
                logger.info("2FA not configured, logging in without 2FA...")
                self.client.login(self.username, self.password)
            
            # Save session
            session = self.client.get_settings()
            self.session_manager.save_session(self.username, session)
            
            logger.info("✓ Login successful, session saved")
            self.logged_in = True
            return True
            
        except ChallengeRequired as e:
            logger.error(f"❌ Challenge required: {e}")
            logger.error("Instagram is asking for verification.")
            logger.error("💡 Solution:")
            logger.error("   1. Login to Instagram manually from the same network/location")
            logger.error("   2. Complete any verification challenges")
            logger.error("   3. Try again after 24 hours")
            return False
            
        except PleaseWaitFewMinutes as e:
            logger.error(f"❌ Rate limited: {e}")
            logger.error("Instagram is rate limiting your requests.")
            logger.error("💡 Solution:")
            logger.error("   1. Wait at least 6-24 hours before trying again")
            logger.error("   2. Reduce posting frequency in config.yaml")
            logger.error("   3. Increase delay ranges in config.yaml")
            return False
            
        except LoginRequired as e:
            logger.error(f"❌ Login failed: {e}")
            logger.error("💡 Solution:")
            logger.error("   1. Verify your Instagram username and password are correct")
            logger.error("   2. Check if your account is locked or restricted")
            logger.error("   3. Try logging in manually to verify credentials")
            return False
            
        except ClientError as e:
            error_msg = str(e)
            logger.error(f"❌ Instagram API error: {error_msg}")
            
            # Check for specific error patterns
            # Note: This is a heuristic approach that may need updates if Instagram changes their error messages
            
            # Check for IP blacklist / suspicious activity errors
            if self._is_ip_blacklist_error(error_msg):
                self._log_ip_blacklist_guidance()
            elif "user_id" in error_msg.lower() or "nonetype" in error_msg.lower():
                logger.error("This appears to be a credentials or API response error.")
                logger.error("💡 Solution:")
                logger.error("   1. Verify INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD are set correctly")
                logger.error("   2. Check if Instagram changed their API (update instagrapi)")
                logger.error("   3. Try: pip install --upgrade instagrapi")
            elif "checkpoint" in error_msg.lower():
                logger.error("Account checkpoint detected.")
                logger.error("💡 Solution: Complete Instagram's security checkpoint in the app/browser")
            
            return False
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Unexpected error during login: {error_msg}")
            logger.error(f"Error type: {type(e).__name__}")
            
            # Check for IP blacklist / suspicious activity errors (may come as generic exceptions)
            if self._is_ip_blacklist_error(error_msg):
                self._log_ip_blacklist_guidance()
            # Provide context based on error type
            elif "NoneType" in error_msg or "int()" in error_msg:
                logger.error("This error often indicates missing or improperly formatted credentials.")
                logger.error("💡 Solution:")
                logger.error("   1. Ensure INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD are set")
                logger.error("   2. If using GitHub Actions, verify secrets are added correctly")
                logger.error("   3. Check that environment variables don't contain only whitespace")
            
            # Print full traceback for debugging
            import traceback
            logger.error("Full traceback:")
            logger.error(traceback.format_exc())
            
            return False
    
    def upload_reel(self, video_path: str, caption: str, 
                    thumbnail_path: Optional[str] = None) -> bool:
        """
        Upload a reel to Instagram.
        
        Args:
            video_path: Path to video file
            caption: Caption for the reel
            thumbnail_path: Optional custom thumbnail
        
        Returns:
            True if upload successful
        """
        if not self.logged_in:
            logger.error("Not logged in. Please login first.")
            return False
        
        try:
            logger.info(f"Uploading reel: {video_path}")
            logger.info(f"Caption: {caption[:100]}...")
            
            # Add safety delay
            min_delay = self.config.get('min_delay_seconds', 30)
            max_delay = self.config.get('max_delay_seconds', 120)
            random_delay(min_delay, max_delay)
            
            # Upload clip
            media = self.client.clip_upload(
                video_path,
                caption=caption,
                thumbnail=thumbnail_path
            )
            
            logger.info(f"Successfully uploaded reel. Media ID: {media.pk}")
            
            # Add another delay after upload
            time.sleep(5)
            
            return True
            
        except ClientError as e:
            logger.error(f"Client error during upload: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            return False
    
    def post_comment(self, media_id: str, comment: str) -> bool:
        """
        Post a comment on a media.
        
        Args:
            media_id: Media ID to comment on
            comment: Comment text
        
        Returns:
            True if successful
        """
        if not self.logged_in:
            logger.error("Not logged in. Please login first.")
            return False
        
        try:
            logger.info(f"Posting comment: {comment[:50]}...")
            
            # Add delay before comment
            time.sleep(10)
            
            self.client.media_comment(media_id, comment)
            logger.info("Comment posted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error posting comment: {e}")
            return False
    
    def logout(self):
        """
        Cleanup after Instagram operations.
        
        Note: We intentionally do NOT call client.logout() to preserve the session
        for future runs. This avoids repeated logins which can trigger Instagram's
        rate limits and account restrictions. The session is saved and reused.
        """
        try:
            if self.logged_in:
                logger.info("Cleaning up...")
                # Session is already saved by session_manager, just mark as logged out
                self.logged_in = False
                logger.info("Session preserved for next run")
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")

def main():
    """Test the Instagram uploader."""
    # This is a dry run test - it will attempt to login but not upload
    uploader = InstagramUploader()
    
    if uploader.login():
        print("\n✓ Login successful!")
        print("Note: Upload functionality requires a valid video file")
        uploader.logout()
    else:
        print("\n✗ Login failed. Check credentials.")

if __name__ == "__main__":
    main()
