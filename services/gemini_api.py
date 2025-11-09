import requests
import json
from typing import Dict, List
from config.settings import settings


class GeminiAPI:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = settings.GEMINI_BASE_URL

    def generate_content(self, prompt: str, context: Dict = None) -> str:
        """Generate content using Gemini AI"""
        try:
            url = f"{self.base_url}?key={self.api_key}"

            full_prompt = self._build_prompt(prompt, context)

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            return "Content generation failed."

    def _build_prompt(self, prompt: str, context: Dict) -> str:
        """Build enhanced prompt with context"""
        if not context:
            return prompt

        context_str = json.dumps(context, indent=2)
        return f"Context: {context_str}\n\nTask: {prompt}"

    def generate_viral_caption(self, trend_data: Dict, content_idea: Dict) -> Dict:
        """Generate viral caption and description for content"""
        prompt = f"""
        You are a viral content creator. Create engaging social media content.

        TREND ANALYSIS: {json.dumps(trend_data, indent=2)}
        CONTENT IDEA: {json.dumps(content_idea, indent=2)}

        Generate:
        1. A compelling caption (max 220 characters)
        2. Detailed visual description for AI generation
        3. 5 relevant hashtags

        Format your response as:
        CAPTION: [your caption]
        DESCRIPTION: [visual description] 
        HASHTAGS: [hashtag1, hashtag2, hashtag3, hashtag4, hashtag5]
        """

        response = self.generate_content(prompt)
        return self._parse_content_response(response)

    def generate_video_script(self, trend_data: Dict, content_idea: Dict) -> Dict:
        """Generate viral video script"""
        prompt = f"""
        You are a viral video scriptwriter. Create engaging video content.

        TREND DATA: {json.dumps(trend_data, indent=2)}
        VIDEO IDEA: {json.dumps(content_idea, indent=2)}

        Generate:
        1. Engaging video script (45-60 seconds)
        2. Scene descriptions
        3. Viral hook in first 3 seconds
        4. Call-to-action

        Format:
        SCRIPT: [full script]
        HOOK: [opening hook]
        SCENES: [scene descriptions]
        CTA: [call to action]
        """

        response = self.generate_content(prompt)
        return self._parse_video_response(response)

    def _parse_content_response(self, response: str) -> Dict:
        """Parse Gemini response for content generation"""
        try:
            lines = response.split('\n')
            result = {"caption": "", "description": "", "hashtags": []}

            current_section = ""
            for line in lines:
                line = line.strip()
                if line.startswith("CAPTION:"):
                    current_section = "caption"
                    result["caption"] = line.replace("CAPTION:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    current_section = "description"
                    result["description"] = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("HASHTAGS:"):
                    current_section = "hashtags"
                    hashtags_str = line.replace("HASHTAGS:", "").strip()
                    result["hashtags"] = [tag.strip() for tag in hashtags_str.split(',')]
                elif current_section and line:
                    result[current_section] += " " + line

            return result

        except Exception as e:
            print(f"Error parsing content response: {e}")
            return {
                "caption": "Check out this amazing content!",
                "description": "Engaging social media content",
                "hashtags": ["viral", "trending", "content"]
            }

    def _parse_video_response(self, response: str) -> Dict:
        """Parse Gemini response for video script"""
        try:
            lines = response.split('\n')
            result = {"script": "", "hook": "", "scenes": "", "cta": ""}

            current_section = ""
            for line in lines:
                line = line.strip()
                if line.startswith("SCRIPT:"):
                    current_section = "script"
                    result["script"] = line.replace("SCRIPT:", "").strip()
                elif line.startswith("HOOK:"):
                    current_section = "hook"
                    result["hook"] = line.replace("HOOK:", "").strip()
                elif line.startswith("SCENES:"):
                    current_section = "scenes"
                    result["scenes"] = line.replace("SCENES:", "").strip()
                elif line.startswith("CTA:"):
                    current_section = "cta"
                    result["cta"] = line.replace("CTA:", "").strip()
                elif current_section and line:
                    result[current_section] += " " + line

            return result

        except Exception as e:
            print(f"Error parsing video response: {e}")
            return {
                "script": "Engaging video content about current trends.",
                "hook": "You won't believe this!",
                "scenes": "Various engaging scenes",
                "cta": "Follow for more content!"
            }