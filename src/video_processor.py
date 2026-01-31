"""Video processor for overlaying text on videos using MoviePy."""

import os
from pathlib import Path
from typing import Tuple

# Configure MoviePy to find ImageMagick
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from src.utils import get_logger, ensure_dir, sanitize_filename

logger = get_logger(__name__)

class VideoProcessor:
    """Process videos by adding text overlays and effects."""
    
    def __init__(self, config: dict = None):
        """Initialize the video processor."""
        self.config = config or {}
        self.font_size = self.config.get('font_size', 60)
        self.text_color = self.config.get('text_color', 'white')
        self.output_dir = ensure_dir('output')
        logger.info("VideoProcessor initialized")
    
    def create_text_clip(self, text: str, duration: float, video_size: Tuple[int, int]) -> TextClip:
        """
        Create a text clip with styling.
        
        Args:
            text: Text to display
            duration: Duration in seconds
            video_size: Video dimensions (width, height)
        
        Returns:
            TextClip object
        """
        try:
            # Try to use a nice font if available
            font_path = None
            possible_fonts = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                'assets/fonts/Montserrat-Bold.ttf',
                'DejaVu-Sans-Bold'  # System font name
            ]
            
            for font in possible_fonts:
                if font and Path(font).exists() if '/' in font else True:
                    font_path = font
                    break
            
            txt_clip = TextClip(
                txt=text,
                font=font_path,
                fontsize=self.font_size,
                color=self.text_color,
                size=(video_size[0] - 100, None),  # Leave margin
                method='caption',
                align='center'
            )
            
            txt_clip = txt_clip.set_duration(duration)
            txt_clip = txt_clip.set_position('center')
            
            logger.info(f"Created text clip: '{text[:30]}...'")
            return txt_clip
            
        except Exception as e:
            logger.error(f"Error creating text clip: {e}")
            raise
    
    def add_text_to_video(self, video_path: str, text: str, output_path: str = None) -> str:
        """
        Add text overlay to a video.
        
        Args:
            video_path: Path to input video
            text: Text to overlay
            output_path: Path for output video
        
        Returns:
            Path to processed video
        """
        try:
            logger.info(f"Processing video: {video_path}")
            
            # Load video
            video = VideoFileClip(video_path)
            
            # Create text clip
            txt_clip = self.create_text_clip(text, video.duration, video.size)
            
            # Create a semi-transparent background for better text readability
            bg_clip = ColorClip(
                size=(video.size[0], txt_clip.h + 40),
                color=(0, 0, 0)
            ).set_opacity(0.3).set_duration(video.duration).set_position(('center', 'center'))
            
            # Composite video
            final_video = CompositeVideoClip([video, bg_clip, txt_clip])
            
            # Set output path
            if not output_path:
                filename = sanitize_filename(text[:30]) + "_overlay.mp4"
                output_path = os.path.join(self.output_dir, filename)
            
            # Write video
            logger.info(f"Writing processed video to: {output_path}")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=video.fps,
                preset='medium'
            )
            
            # Close clips
            video.close()
            final_video.close()
            
            logger.info(f"Successfully processed video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            raise
    
    def create_placeholder_video(self, text: str, duration: int = 15, output_path: str = None) -> str:
        """
        Create a simple placeholder video with text (for testing when Veo API is unavailable).
        
        Args:
            text: Text to display
            duration: Video duration in seconds
            output_path: Path for output video
        
        Returns:
            Path to created video
        """
        try:
            logger.info(f"Creating placeholder video with duration: {duration}s")
            
            # Create a dark background video (9:16 aspect ratio for Instagram Reels)
            width, height = 1080, 1920
            
            # Create background clip
            bg_clip = ColorClip(
                size=(width, height),
                color=(20, 20, 20),
                duration=duration
            )
            
            # Create text clip
            txt_clip = self.create_text_clip(text, duration, (width, height))
            
            # Composite
            video = CompositeVideoClip([bg_clip, txt_clip])
            
            # Set output path
            if not output_path:
                filename = sanitize_filename(text[:30]) + "_placeholder.mp4"
                output_path = os.path.join(self.output_dir, filename)
            
            # Write video
            logger.info(f"Writing placeholder video to: {output_path}")
            video.write_videofile(
                output_path,
                codec='libx264',
                fps=24,
                preset='ultrafast'
            )
            
            # Close clips
            video.close()
            
            logger.info(f"Successfully created placeholder video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating placeholder video: {e}")
            raise

def main():
    """Test the video processor."""
    processor = VideoProcessor()
    
    # Create a test placeholder video
    video_path = processor.create_placeholder_video(
        text="The obstacle is the way.",
        duration=10
    )
    
    print(f"\n✓ Created test video: {video_path}")

if __name__ == "__main__":
    main()
