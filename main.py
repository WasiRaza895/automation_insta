"""Main orchestrator for Instagram automation system."""

import os
import sys
from pathlib import Path
import yaml
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.content_generator import ContentGenerator
from src.video_generator import VideoGenerator
from src.video_processor import VideoProcessor
from src.instagram_uploader import InstagramUploader
from src.utils import get_logger, ensure_dir

logger = get_logger(__name__)

class InstagramAutomation:
    """Main automation orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the automation system."""
        logger.info("=" * 50)
        logger.info("Instagram Automation System Starting")
        logger.info("=" * 50)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.content_generator = ContentGenerator(
            model=self.config['api']['gemini_model']
        )
        self.video_generator = VideoGenerator()
        self.video_processor = VideoProcessor(
            config=self.config['video']
        )
        self.instagram_uploader = InstagramUploader(
            config=self.config['safety']
        )
        
        # Create output directory
        ensure_dir('output')
        
        logger.info("All components initialized successfully")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Expand environment variables
            if 'instagram' in config and 'username' in config['instagram']:
                username = config['instagram']['username']
                if username.startswith('${') and username.endswith('}'):
                    env_var = username[2:-1]
                    config['instagram']['username'] = os.getenv(env_var, username)
            
            logger.info(f"Configuration loaded from: {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            logger.warning("Using default configuration")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration."""
        return {
            'content': {
                'theme': 'stoic',
                'quote_style': 'short',
                'hashtag_count': 25
            },
            'video': {
                'duration': 15,
                'font_size': 60,
                'text_color': 'white'
            },
            'safety': {
                'min_delay_seconds': 30,
                'max_delay_seconds': 120
            },
            'api': {
                'gemini_model': 'gemini-2.0-flash-exp',
                'veo_enabled': False
            }
        }
    
    def run(self):
        """Execute the full automation pipeline."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Step 1: Generate content
            logger.info("\n" + "=" * 50)
            logger.info("📝 Step 1/6: Generating Content with Gemini")
            logger.info("=" * 50)
            
            content = self.content_generator.generate_content(
                theme=self.config['content']['theme'],
                quote_style=self.config['content']['quote_style']
            )
            
            logger.info(f"✓ Quote: {content['quote']}")
            logger.info(f"✓ Video Prompt: {content['video_prompt'][:80]}...")
            
            # Step 2: Generate/Get video
            logger.info("\n" + "=" * 50)
            logger.info("🎬 Step 2/6: Video Generation (Cinematic)")
            logger.info("=" * 50)
            
            video_path = None
            
            if self.config['api']['veo_enabled']:
                logger.info("🎥 Attempting Veo video generation...")
                video_path = self.video_generator.generate_video(
                    prompt=content['video_prompt'],
                    duration=self.config['video']['duration']
                )
            
            if not video_path:
                logger.info("Creating placeholder video (Veo not available)...")
                video_path = self.video_processor.create_placeholder_video(
                    text=content['quote'],
                    duration=self.config['video']['duration'],
                    output_path=f"output/video_{timestamp}.mp4"
                )
            
            logger.info(f"✓ Video ready: {video_path}")
            
            # Step 3: Process video (add text overlay if needed)
            logger.info("\n" + "=" * 50)
            logger.info("✨ Step 3/6: Video Processing (1080x1920 Reel Format)")
            logger.info("=" * 50)
            
            if self.config['api']['veo_enabled'] and video_path:
                logger.info("Adding text overlay to Veo-generated video...")
                video_path = self.video_processor.add_text_to_video(
                    video_path=video_path,
                    text=content['quote']
                )
            else:
                logger.info("Skipping overlay (text already on placeholder video)")
            
            logger.info(f"✓ Final video: {video_path}")
            
            # Step 4: Upload to Instagram
            logger.info("\n" + "=" * 50)
            logger.info("📱 Step 4/6: Uploading to Instagram as Reel")
            logger.info("=" * 50)
            
            # Prepare caption
            full_caption = f"{content['caption']}\n\n{content['hashtags']}"
            
            logger.info("Logging into Instagram...")
            if not self.instagram_uploader.login():
                logger.error("Failed to login to Instagram")
                return False
            
            logger.info("Uploading reel...")
            if not self.instagram_uploader.upload_reel(
                video_path=video_path,
                caption=full_caption
            ):
                logger.error("Failed to upload reel")
                self.instagram_uploader.logout()
                return False
            
            logger.info("✓ Reel uploaded successfully!")
            
            # Step 5: Post first comment (optional)
            logger.info("\n" + "=" * 50)
            logger.info("💬 Step 5/6: Adding First Comment (Optional)")
            logger.info("=" * 50)
            logger.info("Note: First comment feature requires media ID from upload")
            # Note: We'd need the media ID from upload to post comment
            # This is left as a TODO for now
            
            # Step 6: Cleanup
            logger.info("\n" + "=" * 50)
            logger.info("🧹 Step 6/6: Cleanup")
            logger.info("=" * 50)
            self.instagram_uploader.logout()
            logger.info("✓ Session cleanup complete")
            
            logger.info("\n" + "=" * 50)
            logger.info("✅ SUCCESS! Your Reel is now live!")
            username = self.instagram_uploader.username
            logger.info(f"🔗 View it: https://instagram.com/{username}/")
            logger.info("=" * 50)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in automation pipeline: {e}", exc_info=True)
            return False

def main():
    """Main entry point."""
    automation = InstagramAutomation()
    success = automation.run()
    
    if success:
        logger.info("\n✓ All done! Check your Instagram account.")
        sys.exit(0)
    else:
        logger.error("\n✗ Automation failed. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
