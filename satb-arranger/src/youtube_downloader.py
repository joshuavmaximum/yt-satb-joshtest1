"""YouTube audio downloader module using yt-dlp."""

import os
import yt_dlp
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeDownloader:
    def __init__(self, output_dir="output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_audio(self, url, filename=None):
        """
        Download audio from YouTube URL.
        
        Args:
            url (str): YouTube video URL
            filename (str): Optional custom filename
            
        Returns:
            str: Path to downloaded audio file
        """
        if not filename:
            filename = "youtube_audio"
            
        output_path = self.output_dir / f"{filename}.%(ext)s"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Downloading audio from: {url}")
                info = ydl.extract_info(url, download=True)
                
                # Get the actual output filename
                actual_filename = ydl.prepare_filename(info)
                actual_filename = actual_filename.rsplit('.', 1)[0] + '.wav'
                
                logger.info(f"Audio downloaded successfully: {actual_filename}")
                return actual_filename
                
        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            raise
            
    def get_video_info(self, url):
        """Get video metadata without downloading."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date', 'Unknown'),
                }
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return None