from typing import List, Dict
from models.content_models import GeneratedContent, ContentIdea
from services.gemini_media_api import GeminiMediaAPI
import random


class ContentCreator:
    def __init__(self):
        self.gemini_api = GeminiMediaAPI()

    def create_video_content(self, idea: ContentIdea, trend_data: Dict, user_prefs: Dict) -> GeneratedContent:
        """Create video content with AI-generated titles and descriptions"""
        viral_keywords = trend_data.get("viral_keywords", [])
        main_topic = viral_keywords[0] if viral_keywords else "technology"

        # Generate complete video content using Gemini
        video_content = self.gemini_api.generate_video_content(
            topic=main_topic,
            duration=60
        )

        # Combine keywords
        keywords = user_prefs.get("preferred_keywords", []) + viral_keywords + ["video", "AIgenerated", "AbimanyuAI"]
        keywords = list(dict.fromkeys(keywords))[:6]

        return GeneratedContent(
            content_type="video",
            caption=video_content["title"],
            description=video_content["description"],
            keywords=keywords,
            media_source=video_content["media_source"],
            viral_score=idea.viral_score,
            trend_alignment=viral_keywords
        )