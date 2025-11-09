from typing import List, Dict
from models.content_models import GeneratedContent, ContentIdea
from services.gemini_media_api import GeminiMediaAPI
import random


class VisualFactory:
    """Visual Factory for meme discovery and image generation with REAL Gemini AI"""

    def __init__(self):
        self.gemini_api = GeminiMediaAPI()
        self.meme_templates = [
            {
                "name": "Reaction Meme",
                "format": "Image with text reaction",
                "style": "humorous",
                "elements": ["funny situation", "relatable moment", "surprise element"]
            },
            {
                "name": "Comparison Meme",
                "format": "Before/After or This/That",
                "style": "comparative",
                "elements": ["two scenarios", "contrast", "choice"]
            }
        ]

    def create_visual_content(self, content_ideas: List[ContentIdea],
                              trend_data: Dict, user_prefs: Dict) -> List[GeneratedContent]:
        """Create visual content including memes and images using REAL Gemini AI"""
        print("🏭 Visual Factory: Generating REAL AI-powered images and memes...")

        generated_content = []

        for i, idea in enumerate(content_ideas):
            if idea.content_type == "image":
                # Decide between regular image and meme
                if self._should_create_meme(trend_data, i):
                    content = self._create_meme_content(idea, trend_data, user_prefs, i)
                else:
                    content = self._create_regular_image(idea, trend_data, user_prefs, i)

                if content:
                    generated_content.append(content)
                    content_type = "AI meme" if "meme" in content.description.lower() else "AI image"
                    print(f"   ✅ Created {content_type}: {content.caption[:50]}...")

        return generated_content

    def _should_create_meme(self, trend_data: Dict, index: int) -> bool:
        """Decide whether to create a meme"""
        meme_keywords = trend_data.get("meme_keywords", [])
        return len(meme_keywords) > 0 and index % 2 == 0

    def _create_meme_content(self, idea: ContentIdea, trend_data: Dict,
                             user_prefs: Dict, index: int) -> GeneratedContent:
        """Create meme content using REAL Gemini AI"""
        meme_template = random.choice(self.meme_templates)
        viral_keywords = trend_data.get("viral_keywords", [])

        # Generate meme text
        top_text, bottom_text = self._generate_meme_text(viral_keywords, index)

        # Generate REAL meme image using Gemini
        media_source = self.gemini_api.generate_meme_image(
            template=meme_template["name"],
            top_text=top_text,
            bottom_text=bottom_text
        )

        caption = f"😂 {top_text}... {bottom_text} by Abimanyu-AI Hackathon #Meme #Viral"

        # Combine keywords
        keywords = user_prefs.get("preferred_keywords", []) + viral_keywords + ["meme", "funny", "viral", "AbimanyuAI"]
        keywords = list(dict.fromkeys(keywords))[:6]

        return GeneratedContent(
            content_type="image",
            caption=caption,
            description=f"AI-generated {meme_template['name']} meme about {viral_keywords[0] if viral_keywords else 'trending topic'}",
            keywords=keywords,
            media_source=media_source,
            viral_score=idea.viral_score + 15,
            trend_alignment=viral_keywords
        )

    def _create_regular_image(self, idea: ContentIdea, trend_data: Dict,
                              user_prefs: Dict, index: int) -> GeneratedContent:
        """Create regular image content using REAL Gemini AI"""
        viral_keywords = trend_data.get("viral_keywords", [])

        # Generate image prompt based on trends and user preferences
        image_prompt = self._generate_image_prompt(viral_keywords, user_prefs, index)

        # Generate REAL image using Gemini
        media_source = self.gemini_api.generate_image(
            prompt=image_prompt,
            style=random.choice(["realistic", "artistic", "minimalist"])
        )

        caption = self._generate_image_caption(viral_keywords, index)

        keywords = user_prefs.get("preferred_keywords", []) + viral_keywords + ["AbimanyuAI"]
        keywords = list(dict.fromkeys(keywords))[:6]

        return GeneratedContent(
            content_type="image",
            caption=caption,
            description=f"AI-generated image about {viral_keywords[0] if viral_keywords else 'innovation'}",
            keywords=keywords,
            media_source=media_source,
            viral_score=idea.viral_score,
            trend_alignment=viral_keywords
        )

    def _generate_meme_text(self, viral_keywords: List[str], index: int) -> tuple:
        """Generate top and bottom text for memes"""
        meme_texts = [
            ("When you finally understand the trend", "But then it changes again"),
            ("My brain processing", f"{viral_keywords[0] if viral_keywords else 'new information'}"),
            ("What I think vs Reality", "When trying new technology"),
            ("The moment you realize", f"{viral_keywords[0] if viral_keywords else 'innovation'} is amazing")
        ]

        return meme_texts[index % len(meme_texts)]

    def _generate_image_prompt(self, viral_keywords: List[str], user_prefs: Dict, index: int) -> str:
        """Generate image prompt for REAL Gemini AI"""
        main_topic = viral_keywords[0] if viral_keywords else "technology innovation"
        user_style = user_prefs.get("visual_affinities", ["modern"])[0]

        prompts = [
            f"Create a stunning {user_style} visual representation of {main_topic} and its impact on society. Show advanced technology, digital transformation, and innovation in a professional social media style.",
            f"Generate an engaging {user_style} image about breakthroughs in {main_topic}. Include futuristic elements, data visualization, and cutting-edge technology concepts.",
            f"Design a {user_style} social media optimized image showcasing {main_topic} innovations. Feature modern design, compelling visuals, and brand-friendly content."
        ]

        return prompts[index % len(prompts)]

    def _generate_image_caption(self, viral_keywords: List[str], index: int) -> str:
        """Generate caption for AI-generated images"""
        main_topic = viral_keywords[0] if viral_keywords else "Technology"

        captions = [
            f"🚀 The Future of {main_topic} is Here! AI-generated visual showcasing groundbreaking innovations. by Abimanyu-AI Hackathon",
            f"💡 {main_topic} Revolution Unveiled! Stunning AI-created image of next-generation technology. by Abimanyu-AI Hackathon",
            f"🎯 Breaking Boundaries in {main_topic}! AI-powered visualization of cutting-edge advancements. by Abimanyu-AI Hackathon"
        ]

        return captions[index % len(captions)]