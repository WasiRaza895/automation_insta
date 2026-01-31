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
        
        if not self.username or not self.password:
            raise ValueError("Instagram username and password are required")
        
        self.client = Client()
        self.session_manager = SessionManager()
        self.logged_in = False
        
        logger.info(f"InstagramUploader initialized for user: {self.username}")
    
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
            
            # Login
            if self.two_factor_seed:
                logger.info("2FA is enabled, generating code...")
                totp = pyotp.TOTP(self.two_factor_seed)
                two_factor_code = totp.now()
                self.client.login(self.username, self.password, verification_code=two_factor_code)
            else:
                self.client.login(self.username, self.password)
            
            # Save session
            session = self.client.get_settings()
            self.session_manager.save_session(self.username, session)
            
            logger.info("Login successful, session saved")
            self.logged_in = True
            return True
            
        except ChallengeRequired as e:
            logger.error(f"Challenge required: {e}")
            logger.error("Instagram is asking for verification. Please verify your account manually.")
            return False
        except PleaseWaitFewMinutes as e:
            logger.error(f"Rate limited: {e}")
            logger.error("Instagram is rate limiting. Please wait and try again later.")
            return False
        except LoginRequired as e:
            logger.error(f"Login failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
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
