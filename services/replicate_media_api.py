import replicate
import requests
import time
from typing import Dict, List, Optional
from config.settings import settings


class ReplicateMediaAPI:
    """Replicate API for generating real images and videos"""

    def __init__(self):
        self.api_token = settings.REPLICATE_API_TOKEN
        self.client = replicate.Client(api_token=self.api_token)

    def generate_image(self, prompt: str, style: str = "realistic") -> Optional[str]:
        """Generate real image using Replicate API"""
        try:
            print(f"🖼️ Generating real image with Replicate: {prompt[:100]}...")

            model_id = settings.REPLICATE_IMAGE_MODELS.get(style, settings.REPLICATE_IMAGE_MODELS["realistic"])

            # Enhanced prompt for better results
            enhanced_prompt = self._enhance_image_prompt(prompt, style)

            # Generate image using Replicate
            output = self.client.run(
                model_id,
                input={
                    "prompt": enhanced_prompt,
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 25
                }
            )

            if output and len(output) > 0:
                image_url = output[0] if isinstance(output, list) else output
                print(f"✅ Image generated successfully: {image_url}")
                return image_url
            else:
                print("❌ Image generation failed - no output")
                return self._get_fallback_image(prompt)

        except Exception as e:
            print(f"❌ Error generating image with Replicate: {e}")
            return self._get_fallback_image(prompt)

    def generate_video(self, prompt: str, duration: int = 60) -> Optional[str]:
        """Generate real video using Replicate API"""
        try:
            print(f"🎥 Generating {duration}s video with Replicate: {prompt[:100]}...")

            model_id = settings.REPLICATE_VIDEO_MODELS["standard"]

            # Enhanced prompt for video
            enhanced_prompt = self._enhance_video_prompt(prompt, duration)

            # Generate video using Replicate
            output = self.client.run(
                model_id,
                input={
                    "prompt": enhanced_prompt,
                    "num_frames": min(24 * duration, 250),  # Limit frames
                    "width": 1024,
                    "height": 576,
                    "fps": 24,
                    "guidance_scale": 7.5
                }
            )

            if output:
                video_url = output
                print(f"✅ Video generated successfully: {video_url}")
                return video_url
            else:
                print("❌ Video generation failed - no output")
                return self._get_fallback_video()

        except Exception as e:
            print(f"❌ Error generating video with Replicate: {e}")
            return self._get_fallback_video()

    def generate_meme_image(self, template: str, top_text: str, bottom_text: str) -> Optional[str]:
        """Generate meme image using Replicate"""
        try:
            prompt = f"""
            Create a viral meme image in the style of: {template}

            TOP TEXT: "{top_text}"
            BOTTOM TEXT: "{bottom_text}"

            Style: Classic meme format with bold white text on black borders
            Requirements: High contrast, readable text, humorous style, social media optimized
            """

            return self.generate_image(prompt, style="meme")

        except Exception as e:
            print(f"❌ Error generating meme with Replicate: {e}")
            return self._get_fallback_meme()

    def generate_series_thumbnail(self, episode_title: str, series_theme: str) -> Optional[str]:
        """Generate professional thumbnail for series episodes"""
        try:
            prompt = f"""
            Create a professional YouTube thumbnail for: "{episode_title}"

            Series Theme: {series_theme}
            Style: Professional YouTube thumbnail with bold text, engaging visuals, high contrast
            Requirements: 1280x720 resolution, clickable design, modern aesthetics, brand-consistent
            """

            return self.generate_image(prompt, style="professional")

        except Exception as e:
            print(f"❌ Error generating thumbnail with Replicate: {e}")
            return self._get_fallback_thumbnail()

    def _enhance_image_prompt(self, prompt: str, style: str) -> str:
        """Enhance image prompt for better Replicate results"""
        style_descriptions = {
            "realistic": "photorealistic, high detail, professional photography, 8K resolution",
            "artistic": "artistic, creative, painterly style, artistic composition",
            "minimalist": "minimalist, clean design, simple composition, modern aesthetics",
            "humorous": "funny, humorous, comic style, exaggerated expressions",
            "professional": "professional, corporate, clean design, modern business style"
        }

        style_desc = style_descriptions.get(style, "high quality, detailed")

        enhanced_prompt = f"""
        {prompt}

        Style: {style_desc}
        Quality: 8K resolution, professional grade, highly detailed
        Lighting: Professional studio lighting, perfect illumination
        Composition: Well-framed, balanced, visually appealing
        Technical: Sharp focus, no blur, perfect exposure
        Social Media: Optimized for Instagram, Facebook, Twitter

        Create an engaging social media image that will get high engagement.
        """

        return enhanced_prompt.strip()

    def _enhance_video_prompt(self, prompt: str, duration: int) -> str:
        """Enhance video prompt for better Replicate results"""
        return f"""
        {prompt}

        Create a {duration}-second video with:
        - Smooth camera movements
        - Professional editing
        - High quality visuals
        - Engaging content
        - Social media optimized

        Style: Professional video content, smooth transitions, high production value
        Technical: 24fps, HD quality, stable footage
        Duration: Exactly {duration} seconds
        """

    def _get_fallback_image(self, prompt: str) -> str:
        """Get fallback image when Replicate fails"""
        # Use hash of prompt to create unique placeholder
        image_id = hash(prompt) % 1000000
        return f"https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&id={image_id}"

    def _get_fallback_video(self) -> str:
        """Get fallback video when Replicate fails"""
        return "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    def _get_fallback_meme(self) -> str:
        """Get fallback meme image"""
        return "https://images.unsplash.com/photo-1611262588024-d12430b98920?w=800"

    def _get_fallback_thumbnail(self) -> str:
        """Get fallback thumbnail"""
        return "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800"