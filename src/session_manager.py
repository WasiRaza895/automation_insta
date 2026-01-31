"""Session manager for Instagram login persistence."""

import json
import os
from pathlib import Path
from typing import Optional, Dict
from src.utils import get_logger, ensure_dir

logger = get_logger(__name__)

class SessionManager:
    """Manage Instagram login sessions."""
    
    def __init__(self, session_dir: str = "sessions"):
        """Initialize the session manager."""
        self.session_dir = ensure_dir(session_dir)
        logger.info(f"SessionManager initialized with directory: {self.session_dir}")
    
    def _get_session_path(self, username: str) -> Path:
        """Get the session file path for a username."""
        return Path(self.session_dir) / f"{username}_session.json"
    
    def save_session(self, username: str, session_data: Dict) -> bool:
        """
        Save a session to file.
        
        Args:
            username: Instagram username
            session_data: Session data dictionary
        
        Returns:
            True if save successful
        """
        try:
            session_path = self._get_session_path(username)
            
            with open(session_path, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Session saved for user: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            return False
    
    def load_session(self, username: str) -> Optional[Dict]:
        """
        Load a session from file.
        
        Args:
            username: Instagram username
        
        Returns:
            Session data dictionary or None if not found
        """
        try:
            session_path = self._get_session_path(username)
            
            if not session_path.exists():
                logger.info(f"No existing session found for user: {username}")
                return None
            
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            
            logger.info(f"Session loaded for user: {username}")
            return session_data
            
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None
    
    def delete_session(self, username: str) -> bool:
        """
        Delete a session file.
        
        Args:
            username: Instagram username
        
        Returns:
            True if delete successful
        """
        try:
            session_path = self._get_session_path(username)
            
            if session_path.exists():
                session_path.unlink()
                logger.info(f"Session deleted for user: {username}")
                return True
            else:
                logger.warning(f"No session file to delete for user: {username}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False
