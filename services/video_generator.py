import requests
import json
from config.settings import settings


class VideoGenerator:
    """AI Video Generation Service"""

    def generate_series_episode_video(self, script: str, theme: str, duration: int = 60) -> str:
        """Generate video using AI video generation APIs"""

        # Option 1: Runway ML API (if available)
        # return self._generate_with_runway(script, theme, duration)

        # Option 2: Stable Video Diffusion (if available)
        # return self._generate_with_svd(script, theme, duration)

        # Option 3: Fallback to relevant stock video
        return self._get_relevant_stock_video(theme, duration)

    def _get_relevant_stock_video(self, theme: str, duration: int) -> str:
        """Get relevant stock video based on theme"""
        stock_videos = {
            "tech": [
                "https://assets.mixkit.co/videos/preview/mixkit-white-clouds-time-lapse-1177-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-circuit-board-texture-1175-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-close-up-of-computer-chip-1176-large.mp4"
            ],
            "ai": [
                "https://assets.mixkit.co/videos/preview/mixkit-robot-working-in-a-factory-1182-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-artificial-intelligence-concept-1183-large.mp4"
            ],
            "innovation": [
                "https://assets.mixkit.co/videos/preview/mixkit-ideas-innovation-1178-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-light-bulb-innovation-1179-large.mp4"
            ],
            "music": [
                "https://assets.mixkit.co/videos/preview/mixkit-concert-audience-clapping-1184-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-musician-playing-guitar-1185-large.mp4"
            ],
            "travel": [
                "https://assets.mixkit.co/videos/preview/mixkit-road-trip-through-the-mountains-1186-large.mp4",
                "https://assets.mixkit.co/videos/preview/mixkit-golden-hour-landscape-1187-large.mp4"
            ]
        }

        import random
        videos = stock_videos.get(theme.lower(), stock_videos["tech"])
        return random.choice(videos)