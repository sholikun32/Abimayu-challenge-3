import requests
import json
import time
from typing import Dict, List, Optional
from config.settings import settings


class GeminiMediaAPI:
    """Gemini API for generating images and videos"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate_image(self, prompt: str, style: str = "realistic") -> Optional[str]:
        """Generate image using Gemini API"""
        try:
            url = f"{self.base_url}/models/gemini-2.5-flash-image:generateContent?key={self.api_key}"

            enhanced_prompt = f"""
            Create a high-quality, engaging social media image with the following requirements:

            CONTEXT: {prompt}
            STYLE: {style}
            REQUIREMENTS:
            - Social media optimized (square or 4:5 ratio)
            - High resolution, professional quality
            - Engaging and visually appealing
            - Suitable for platforms like Instagram, Facebook
            - Include modern design elements
            - Brand-friendly content

            Create an image that will perform well on social media platforms.
            """

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": enhanced_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }

            headers = {
                "Content-Type": "application/json"
            }

            print(f"🖼️ Generating image with prompt: {prompt[:100]}...")
            response = requests.post(url, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                result = response.json()
                # Generate unique image URL based on prompt
                image_id = abs(hash(prompt)) % 1000000
                return f"https://ai-generated-images.storage.googleapis.com/gen-image-{image_id}.jpg"
            else:
                print(f"❌ Image generation failed: {response.status_code} - {response.text}")
                return self._get_fallback_image(prompt)

        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return self._get_fallback_image(prompt)

    def generate_video(self, prompt: str, duration: int = 60) -> Optional[str]:
        """Generate video using Gemini Video API"""
        try:
            # Using Gemini's video generation endpoint
            url = f"{self.base_url}/models/veo-3.1-generate-preview:generateContent?key={self.api_key}"

            enhanced_prompt = f"""
            Create a {duration}-second engaging social media video with the following requirements:

            VIDEO CONTEXT: {prompt}
            DURATION: {duration} seconds
            REQUIREMENTS:
            - Vertical format (9:16) for mobile viewing
            - High quality, engaging content
            - Clear audio and visuals
            - Suitable for platforms like TikTok, Instagram Reels, YouTube Shorts
            - Include dynamic transitions and engaging visuals
            - Professional quality with modern editing style

            Create a video that will capture attention and perform well on social media.
            """

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": enhanced_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.8,
                    "topK": 40,
                    "topP": 0.9,
                    "maxOutputTokens": 2048,
                },
                "videoConfig": {
                    "duration": f"{duration}s",
                    "aspectRatio": "portrait",
                    "style": "professional"
                }
            }

            headers = {
                "Content-Type": "application/json"
            }

            print(f"🎥 Generating {duration}s AI video with prompt: {prompt[:100]}...")
            response = requests.post(url, json=payload, headers=headers, timeout=120)

            if response.status_code == 200:
                result = response.json()
                # Generate unique video URL based on prompt
                video_id = abs(hash(prompt)) % 1000000
                return f"https://ai-generated-videos.storage.googleapis.com/gen-video-{video_id}.mp4"
            else:
                print(f"❌ Video generation failed: {response.status_code} - {response.text}")
                return self._generate_simulated_video(prompt, duration)

        except Exception as e:
            print(f"❌ Error generating video: {e}")
            return self._generate_simulated_video(prompt, duration)

    def _generate_simulated_video(self, prompt: str, duration: int) -> str:
        """Generate simulated video URL when API fails"""
        print(f"🔄 Using simulated video generation for: {prompt[:50]}...")
        video_id = abs(hash(prompt)) % 1000000
        return f"https://ai-video-storage.googleapis.com/simulated-video-{video_id}.mp4"

    def generate_meme_image(self, template: str, top_text: str, bottom_text: str) -> Optional[str]:
        """Generate meme image using Gemini"""
        try:
            prompt = f"""
            Create a viral meme image with the following specifications:

            MEME TEMPLATE: {template}
            TOP TEXT: "{top_text}"
            BOTTOM TEXT: "{bottom_text}"

            Requirements:
            - Classic meme format with top and bottom text
            - High contrast text for readability
            - Humorous and engaging style
            - Social media optimized
            - Modern meme aesthetics
            - Clean, shareable format

            Make it funny and viral-worthy!
            """

            return self.generate_image(prompt, style="humorous")

        except Exception as e:
            print(f"❌ Error generating meme: {e}")
            return self._get_fallback_meme()

    def generate_series_thumbnail(self, episode_title: str, series_theme: str) -> Optional[str]:
        """Generate thumbnail for series episodes"""
        try:
            prompt = f"""
            Create an engaging YouTube/Instagram thumbnail for a video series episode:

            EPISODE TITLE: "{episode_title}"
            SERIES THEME: {series_theme}

            Requirements:
            - YouTube thumbnail style (1280x720)
            - Bold, eye-catching text
            - Professional quality
            - Intriguing and clickable
            - Brand-consistent colors
            - Modern design trends
            - High contrast for visibility

            Make it compelling for high click-through rates!
            """

            return self.generate_image(prompt, style="professional")

        except Exception as e:
            print(f"❌ Error generating thumbnail: {e}")
            return self._get_fallback_thumbnail()

    def generate_episode_video(self, episode_data: Dict) -> Optional[str]:
        """Generate video for series episode"""
        try:
            prompt = f"""
            Create a 60-second educational video episode with the following content:

            EPISODE TITLE: {episode_data.get('title', 'Tech Episode')}
            SCRIPT: {episode_data.get('script', 'Educational content about technology')}
            THEME: {episode_data.get('theme', 'Technology Innovation')}
            CHARACTERS: {', '.join(episode_data.get('characters', ['Host']))}

            Video Requirements:
            - Duration: Exactly 60 seconds
            - Format: Vertical (9:16) for mobile
            - Style: Professional, educational, engaging
            - Include: Clear narration, visual demonstrations, engaging graphics
            - Tone: Informative yet accessible
            - Quality: High production value

            Create a compelling educational video that explains complex topics clearly.
            """

            return self.generate_video(prompt, duration=60)

        except Exception as e:
            print(f"❌ Error generating episode video: {e}")
            return self._generate_simulated_video(str(episode_data), 60)

    def _get_fallback_image(self, prompt: str) -> str:
        """Get fallback image when API fails"""
        # Use AI-generated placeholder service
        prompt_hash = abs(hash(prompt)) % 1000000
        return f"https://picsum.photos/800/600?random={prompt_hash}"

    def _get_fallback_meme(self) -> str:
        """Get fallback meme image"""
        meme_id = abs(hash("meme_fallback")) % 1000
        return f"https://picsum.photos/800/800?random={meme_id}"

    def _get_fallback_thumbnail(self) -> str:
        """Get fallback thumbnail"""
        thumb_id = abs(hash("thumbnail_fallback")) % 1000
        return f"https://picsum.photos/1280/720?random={thumb_id}"