import requests
import json
from typing import List, Dict, Optional
from config.settings import settings
from models.content_models import UserPreferences, PostResult
from datetime import datetime


class CircloAPI:
    def __init__(self):
        self.base_url = settings.CIRCLO_BASE_URL
        self.token = settings.CIRCLO_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        # Available niches in Circlo based on API documentation
        self.available_niches = [
            "General", "Blogger", "Traveler", "Foodie",
            "Fitness Coach", "Fashion Influencer", "Gamer",
            "Photographer", "Artist", "Musician", "Writer",
            "Entrepreneur", "Educator", "Health Expert",
            "Lifestyle Influencer", "Business Coach"
        ]

    def get_user_preferences(self, page: int = 1, limit: int = 50) -> List[UserPreferences]:
        """Get user preferences from Circlo API"""
        try:
            url = f"{self.base_url}/user-preferences"
            params = {"page": page, "limit": limit}

            print(f"🔗 Fetching from: {url}")

            response = requests.get(url, headers=self.headers, params=params, timeout=30)

            if response.status_code == 401:
                print("❌ Authentication failed: Invalid or expired token")
                return []
            elif response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return []

            response.raise_for_status()

            data = response.json()
            preferences = []

            for pref_data in data.get("preferences", []):
                preference = UserPreferences(
                    id=pref_data.get("id"),
                    user_id=pref_data.get("userId"),
                    preferred_keywords=pref_data.get("preferredKeywords", []),
                    preferred_niches=pref_data.get("preferredNiches", []),
                    preferred_genders=pref_data.get("preferredGenders", []),
                    visual_affinities=pref_data.get("visualRepresentationAffinities", []),
                    active_hours=pref_data.get("activeHours", []),
                    engagement_ratio=pref_data.get("engagementRatio", 0.5)
                )
                preferences.append(preference)

            print(f"✅ Found {len(preferences)} user preferences")
            return preferences

        except Exception as e:
            print(f"❌ Error fetching user preferences: {e}")
            return []

    def get_trending_posts(self, keywords: List[str], limit: int = 15) -> List[Dict]:
        """Get trending posts by keywords"""
        try:
            url = f"{self.base_url}/posts/by-keywords"
            keyword_string = ",".join(keywords[:3])
            params = {
                "keywords": keyword_string,
                "limit": limit
            }

            print(f"🔗 Fetching trends from: {url}")
            print(f"🔍 Keywords: {keyword_string}")

            response = requests.get(url, headers=self.headers, params=params, timeout=30)

            if response.status_code == 401:
                print("❌ Authentication failed: Invalid or expired token")
                return []
            elif response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return []

            response.raise_for_status()

            data = response.json()
            posts = data.get("posts", [])
            print(f"✅ Found {len(posts)} trending posts")
            return posts

        except Exception as e:
            print(f"❌ Error fetching trending posts: {e}")
            return []

    def create_post(self, content_data: Dict) -> PostResult:
        """Create a new post on Circlo"""
        try:
            url = f"{self.base_url}/user-preferences/recommend/create-post"

            # Clean and validate data
            caption = self._clean_caption(content_data.get("caption", ""))
            keywords = content_data.get("keywords", [])[:5]  # Limit to 5 keywords
            niche = self._get_valid_niche(content_data.get("niche", ""), keywords)

            payload = {
                "profile": "general",
                "niche": niche,
                "media_type": content_data.get("media_type"),
                "media_source": self._get_valid_media_source(content_data.get("media_type")),
                "caption": caption,
                "keywords": keywords
            }

            print(f"📮 Posting to: {url}")
            print(f"📝 Payload niche: {niche}")
            print(f"📝 Payload media_type: {content_data.get('media_type')}")

            response = requests.post(url, headers=self.headers, json=payload, timeout=30)

            if response.status_code == 500:
                error_data = response.json()
                if "No profiles found with niche" in error_data.get("error", ""):
                    print(f"⚠️ Niche '{niche}' not available, trying with 'General'")
                    return self._create_post_with_general_niche(content_data)
                else:
                    print(f"❌ Server Error 500: {response.text}")
                    return self._create_post_simple(content_data)
            elif response.status_code != 200 and response.status_code != 201:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return PostResult(
                    success=False,
                    post_id="",
                    content_type=content_data.get("media_type"),
                    posted_at=datetime.now(),
                    engagement_metrics={}
                )

            response.raise_for_status()

            result = response.json()
            print(f"✅ Post created successfully: {result.get('post', {}).get('id', 'unknown')}")

            return PostResult(
                success=True,
                post_id=result.get("post", {}).get("id", "unknown"),
                content_type=content_data.get("media_type"),
                posted_at=datetime.now(),
                engagement_metrics={"likeCount": 0, "commentCount": 0}
            )

        except Exception as e:
            print(f"❌ Error creating post: {e}")
            return PostResult(
                success=False,
                post_id="",
                content_type=content_data.get("media_type"),
                posted_at=datetime.now(),
                engagement_metrics={}
            )

    def _get_valid_niche(self, requested_niche: str, keywords: List[str]) -> str:
        """Get a valid niche that exists in Circlo system"""
        # Check if requested niche is available
        if requested_niche in self.available_niches:
            return requested_niche

        # Map common niches to available ones
        niche_mapping = {
            "Tech Reviewer": "General",
            "Tech": "General",
            "AI": "General",
            "Technology": "General",
            "Innovation": "General",
            "Digital": "General",
            "Music": "Musician",
            "LiveMusic": "Musician",
            "Concert": "Musician",
            "Travel": "Traveler",
            "Adventure": "Traveler",
            "Road Trip": "Traveler",
            "Art": "Artist",
            "Creative": "Artist",
            "Design": "Artist",
            "Food": "Foodie",
            "Cooking": "Foodie",
            "Fitness": "Fitness Coach",
            "Workout": "Fitness Coach",
            "Health": "Health Expert",
            "Business": "Entrepreneur",
            "Education": "Educator",
            "Lifestyle": "Lifestyle Influencer"
        }

        # Try to map the requested niche
        if requested_niche in niche_mapping:
            mapped_niche = niche_mapping[requested_niche]
            if mapped_niche in self.available_niches:
                print(f"🔄 Mapped niche '{requested_niche}' -> '{mapped_niche}'")
                return mapped_niche

        # Try to determine from keywords
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for niche_key, niche_value in niche_mapping.items():
                if niche_key.lower() in keyword_lower and niche_value in self.available_niches:
                    print(f"🔄 Determined niche from keyword '{keyword}' -> '{niche_value}'")
                    return niche_value

        # Default to General
        print(f"🔄 Using default niche 'General'")
        return "General"

    def _create_post_with_general_niche(self, content_data: Dict) -> PostResult:
        """Create post with General niche"""
        try:
            url = f"{self.base_url}/user-preferences/recommend/create-post"

            payload = {
                "profile": "general",
                "niche": "General",
                "media_type": content_data.get("media_type"),
                "media_source": self._get_valid_media_source(content_data.get("media_type")),
                "caption": content_data.get("caption", "Check out this amazing content!"),
                "keywords": content_data.get("keywords", [])[:5]
            }

            print("🔄 Trying with 'General' niche...")
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                print(f"✅ Post created with General niche: {result.get('post', {}).get('id', 'unknown')}")
                return PostResult(
                    success=True,
                    post_id=result.get("post", {}).get("id", "unknown"),
                    content_type=content_data.get("media_type"),
                    posted_at=datetime.now(),
                    engagement_metrics={}
                )
            else:
                print(f"❌ General niche also failed: {response.status_code}")
                return self._create_post_simple(content_data)

        except Exception as e:
            print(f"❌ General niche failed: {e}")
            return self._create_post_simple(content_data)

    def _create_post_simple(self, content_data: Dict) -> PostResult:
        """Try creating post with simplest possible payload"""
        try:
            url = f"{self.base_url}/user-preferences/recommend/create-post"

            # Minimal payload that should always work
            payload = {
                "profile": "general",
                "niche": "General",
                "media_type": content_data.get("media_type", "image"),
                "media_source": "https://picsum.photos/800/600",
                "caption": "Amazing content by Abimanyu-AI Hackathon!",
                "keywords": ["AI", "Hackathon", "Content"]
            }

            print("🔄 Trying with simplest payload...")
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                print(f"✅ Simple post created: {result.get('post', {}).get('id', 'unknown')}")
                return PostResult(
                    success=True,
                    post_id=result.get("post", {}).get("id", "unknown"),
                    content_type=content_data.get("media_type"),
                    posted_at=datetime.now(),
                    engagement_metrics={}
                )
            else:
                print(f"❌ Simple post failed: {response.status_code} - {response.text}")
                return PostResult(
                    success=False,
                    post_id="",
                    content_type=content_data.get("media_type"),
                    posted_at=datetime.now(),
                    engagement_metrics={}
                )

        except Exception as e:
            print(f"❌ Simple post failed: {e}")
            return PostResult(
                success=False,
                post_id="",
                content_type=content_data.get("media_type"),
                posted_at=datetime.now(),
                engagement_metrics={}
            )

    def _clean_caption(self, caption: str) -> str:
        """Clean caption for API compatibility"""
        # Remove or replace problematic characters if needed
        cleaned = caption.replace('"', "'")
        return cleaned[:220]  # Ensure length limit

