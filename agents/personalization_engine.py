from typing import List, Dict, Optional
from models.content_models import UserPreferences
from services.circlo_api import CircloAPI
import random


class PersonalizationEngine:
    """Agentic system that generates personalized content based on real user preferences"""

    def __init__(self):
        self.circlo_api = CircloAPI()
        self.content_strategies = {
            "Tech Reviewer": self._tech_reviewer_strategy,
            "Musician": self._musician_strategy,
            "Traveler": self._traveler_strategy,
            "Artist": self._artist_strategy,
            "Foodie": self._foodie_strategy,
            "Fitness Coach": self._fitness_coach_strategy,
            "General": self._general_strategy
        }

    def analyze_user_profile(self, user_preferences: UserPreferences) -> Dict:
        """Analyze user preferences to create personalized content strategy"""
        print("🎯 Personalization Engine: Analyzing user profile...")

        primary_niche = self._determine_primary_niche(user_preferences)
        content_preferences = self._analyze_content_preferences(user_preferences)
        engagement_patterns = self._analyze_engagement_patterns(user_preferences)

        return {
            "user_id": user_preferences.user_id,
            "primary_niche": primary_niche,
            "content_preferences": content_preferences,
            "engagement_patterns": engagement_patterns,
            "personalized_strategy": self._create_personalized_strategy(primary_niche, user_preferences),
            "content_recommendations": self._generate_content_recommendations(user_preferences)
        }

    def generate_personalized_content_ideas(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Generate personalized content ideas based on user profile and trends"""
        print("💡 Generating personalized content ideas...")

        primary_niche = user_profile["primary_niche"]
        strategy_function = self.content_strategies.get(primary_niche, self._general_strategy)

        content_ideas = strategy_function(user_profile, trend_data)

        # Add personalization score to each idea
        for idea in content_ideas:
            idea["personalization_score"] = self._calculate_personalization_score(idea, user_profile)

        return sorted(content_ideas, key=lambda x: x["personalization_score"], reverse=True)[:5]

    def _determine_primary_niche(self, user_preferences: UserPreferences) -> str:
        """Determine user's primary niche based on preferences"""
        if user_preferences.preferred_niches:
            return user_preferences.preferred_niches[0]

        # Fallback: determine from keywords
        keywords = [kw.lower() for kw in user_preferences.preferred_keywords]

        niche_keywords = {
            "Tech Reviewer": ["tech", "ai", "digital", "innovation", "software", "hardware"],
            "Musician": ["music", "concert", "band", "song", "livemusic", "audio"],
            "Traveler": ["travel", "trip", "adventure", "journey", "explore", "destination"],
            "Artist": ["art", "creative", "design", "painting", "drawing", "visual"],
            "Foodie": ["food", "restaurant", "cooking", "recipe", "culinary", "dish"],
            "Fitness Coach": ["fitness", "workout", "health", "exercise", "gym", "training"]
        }

        best_niche = "General"
        max_matches = 0

        for niche, niche_keys in niche_keywords.items():
            matches = sum(1 for key in niche_keys if any(key in kw for kw in keywords))
            if matches > max_matches:
                max_matches = matches
                best_niche = niche

        return best_niche

    def _analyze_content_preferences(self, user_preferences: UserPreferences) -> Dict:
        """Analyze user's content preferences"""
        keywords = user_preferences.preferred_keywords
        visual_affinities = user_preferences.visual_affinities

        return {
            "preferred_topics": keywords[:10],
            "visual_style": visual_affinities[0] if visual_affinities else "modern",
            "content_types": self._infer_content_types(keywords),
            "engagement_level": "high" if user_preferences.engagement_ratio > 0.7 else "medium",
            "active_times": user_preferences.active_hours
        }

    def _analyze_engagement_patterns(self, user_preferences: UserPreferences) -> Dict:
        """Analyze user engagement patterns"""
        engagement_ratio = user_preferences.engagement_ratio

        engagement_level = "high" if engagement_ratio > 0.7 else "medium" if engagement_ratio > 0.4 else "low"
        interaction_likelihood = "high" if engagement_ratio > 0.6 else "medium" if engagement_ratio > 0.3 else "low"

        return {
            "engagement_score": engagement_ratio,
            "engagement_level": engagement_level,  # FIXED: Add this key
            "content_frequency": self._recommend_content_frequency(engagement_ratio),
            "optimal_timing": user_preferences.active_hours[:2] if user_preferences.active_hours else ["12:00 UTC",
                                                                                                       "18:00 UTC"],
            "interaction_likelihood": interaction_likelihood
        }

    def _create_personalized_strategy(self, niche: str, user_preferences: UserPreferences) -> Dict:
        """Create personalized content strategy"""
        strategies = {
            "Tech Reviewer": {
                "focus": "Technology innovations and reviews",
                "content_mix": {"educational": 40, "reviews": 30, "news": 20, "tutorials": 10},
                "tone": "Professional yet accessible",
                "visual_style": "Modern, clean, tech-focused"
            },
            "Musician": {
                "focus": "Music performances and industry insights",
                "content_mix": {"performances": 40, "behind_scenes": 25, "tutorials": 20, "reviews": 15},
                "tone": "Creative and engaging",
                "visual_style": "Dynamic, emotional, performance-oriented"
            },
            "Traveler": {
                "focus": "Adventure and destination experiences",
                "content_mix": {"destinations": 35, "adventures": 30, "tips": 20, "culture": 15},
                "tone": "Inspirational and informative",
                "visual_style": "Vibrant, scenic, immersive"
            },
            "Artist": {
                "focus": "Creative process and artistic expression",
                "content_mix": {"creations": 45, "process": 25, "inspiration": 20, "tutorials": 10},
                "tone": "Expressive and thoughtful",
                "visual_style": "Aesthetic, detailed, creative"
            },
            "Foodie": {
                "focus": "Culinary experiences and food exploration",
                "content_mix": {"recipes": 35, "reviews": 30, "techniques": 20, "culture": 15},
                "tone": "Appetizing and informative",
                "visual_style": "Vibrant, appetizing, detailed"
            },
            "Fitness Coach": {
                "focus": "Health, fitness and wellness",
                "content_mix": {"workouts": 40, "nutrition": 25, "motivation": 20, "reviews": 15},
                "tone": "Energetic and motivational",
                "visual_style": "Dynamic, clean, inspiring"
            }
        }

        return strategies.get(niche, {
            "focus": "General interest topics",
            "content_mix": {"educational": 35, "entertaining": 30, "inspirational": 20, "news": 15},
            "tone": "Friendly and engaging",
            "visual_style": "Modern and clean"
        })

    def _generate_content_recommendations(self, user_preferences: UserPreferences) -> List[Dict]:
        """Generate personalized content recommendations"""
        keywords = user_preferences.preferred_keywords

        recommendations = []
        for keyword in keywords[:5]:
            recommendations.append({
                "topic": keyword,
                "content_types": self._suggest_content_types(keyword),
                "angle": self._suggest_content_angle(keyword),
                "target_audience": "existing_followers"
            })

        return recommendations

    def _tech_reviewer_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Tech Reviewer niche"""
        viral_keywords = trend_data.get("viral_keywords", [])
        user_keywords = user_profile["content_preferences"]["preferred_topics"]

        ideas = []

        # Tech review ideas
        ideas.append({
            "type": "video",
            "title": f"Review: {viral_keywords[0] if viral_keywords else 'Latest Tech'} Innovation",
            "description": f"In-depth review of {viral_keywords[0] if viral_keywords else 'new technology'} and its practical applications",
            "keywords": user_keywords[:3] + viral_keywords[:2],
            "personalization_factors": ["user_interest", "trend_alignment"]
        })

        # Tutorial ideas
        ideas.append({
            "type": "image",
            "title": f"How to Master {user_keywords[0] if user_keywords else 'Technology'}",
            "description": f"Step-by-step guide to understanding {user_keywords[0] if user_keywords else 'tech topic'}",
            "keywords": user_keywords[:2] + ["tutorial", "guide"],
            "personalization_factors": ["user_expertise", "educational_value"]
        })

        # News ideas
        ideas.append({
            "type": "video",
            "title": f"Breaking: {viral_keywords[1] if len(viral_keywords) > 1 else 'Tech'} Update",
            "description": f"Latest news and updates about {viral_keywords[1] if len(viral_keywords) > 1 else 'technology trends'}",
            "keywords": user_keywords[:2] + viral_keywords[:2] + ["news"],
            "personalization_factors": ["timeliness", "trend_relevance"]
        })

        return ideas

    def _musician_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Musician niche"""
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        viral_keywords = trend_data.get("viral_keywords", [])

        ideas = []

        ideas.append({
            "type": "video",
            "title": f"Live {user_keywords[0] if user_keywords else 'Music'} Performance",
            "description": "Raw and authentic musical performance showcasing talent and emotion",
            "keywords": user_keywords[:3] + ["live", "performance", "music"] + viral_keywords[:2],
            "personalization_factors": ["user_talent", "emotional_connection"]
        })

        ideas.append({
            "type": "image",
            "title": "Behind the Music Creation",
            "description": "Glimpse into the creative process and inspiration behind the music",
            "keywords": user_keywords[:2] + ["creative", "process", "inspiration"],
            "personalization_factors": ["authenticity", "creative_expression"]
        })

        ideas.append({
            "type": "video",
            "title": f"{viral_keywords[0] if viral_keywords else 'Trending'} Music Session",
            "description": "Music performance incorporating current trends and viral elements",
            "keywords": user_keywords[:2] + viral_keywords[:2] + ["session", "trending"],
            "personalization_factors": ["trend_alignment", "virality_potential"]
        })

        return ideas

    def _traveler_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Traveler niche"""
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        viral_keywords = trend_data.get("viral_keywords", [])

        ideas = []

        ideas.append({
            "type": "image",
            "title": f"{user_keywords[0] if user_keywords else 'Amazing'} Destination Discovery",
            "description": "Stunning visual journey through amazing travel destinations and experiences",
            "keywords": user_keywords[:3] + ["travel", "adventure", "discovery"] + viral_keywords[:2],
            "personalization_factors": ["wanderlust", "visual_appeal"]
        })

        ideas.append({
            "type": "video",
            "title": f"{viral_keywords[0] if viral_keywords else 'Essential'} Travel Tips & Secrets",
            "description": "Expert travel advice and hidden gems for adventurous souls",
            "keywords": user_keywords[:2] + ["tips", "advice", "adventure"] + viral_keywords[:2],
            "personalization_factors": ["practical_value", "expert_insights"]
        })

        return ideas

    def _artist_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Artist niche"""
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        viral_keywords = trend_data.get("viral_keywords", [])

        ideas = []

        ideas.append({
            "type": "image",
            "title": f"{user_keywords[0] if user_keywords else 'Creative'} Process Revealed",
            "description": "Step-by-step look at artistic creation from concept to completion",
            "keywords": user_keywords[:3] + ["art", "creative", "process"] + viral_keywords[:2],
            "personalization_factors": ["creative_expression", "educational_value"]
        })

        ideas.append({
            "type": "video",
            "title": f"Art in Motion: {viral_keywords[0] if viral_keywords else 'Creative'} Journey",
            "description": "Time-lapse and process video showing artistic techniques and styles",
            "keywords": user_keywords[:2] + ["timelapse", "technique", "artistic"] + viral_keywords[:2],
            "personalization_factors": ["visual_storytelling", "skill_demonstration"]
        })

        return ideas

    def _foodie_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Foodie niche"""
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        viral_keywords = trend_data.get("viral_keywords", [])

        ideas = []

        ideas.append({
            "type": "image",
            "title": f"{user_keywords[0] if user_keywords else 'Delicious'} Culinary Creations",
            "description": "Beautifully presented food and culinary experiences",
            "keywords": user_keywords[:3] + ["food", "culinary", "recipe"] + viral_keywords[:2],
            "personalization_factors": ["visual_appeal", "sensory_experience"]
        })

        ideas.append({
            "type": "video",
            "title": f"{viral_keywords[0] if viral_keywords else 'Cooking'} Masterclass",
            "description": "Step-by-step cooking tutorial and culinary techniques",
            "keywords": user_keywords[:2] + ["cooking", "tutorial", "masterclass"] + viral_keywords[:2],
            "personalization_factors": ["educational", "skill_development"]
        })

        return ideas

    def _fitness_coach_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Content strategy for Fitness Coach niche"""
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        viral_keywords = trend_data.get("viral_keywords", [])

        ideas = []

        ideas.append({
            "type": "video",
            "title": f"{user_keywords[0] if user_keywords else 'Effective'} Workout Session",
            "description": "Effective fitness routines and exercise demonstrations",
            "keywords": user_keywords[:3] + ["fitness", "workout", "health"] + viral_keywords[:2],
            "personalization_factors": ["practical_value", "motivational"]
        })

        ideas.append({
            "type": "image",
            "title": f"{viral_keywords[0] if viral_keywords else 'Fitness'} Progress & Results",
            "description": "Inspirational fitness journey and transformation results",
            "keywords": user_keywords[:2] + ["progress", "results", "transformation"] + viral_keywords[:2],
            "personalization_factors": ["inspirational", "results_driven"]
        })

        return ideas

    def _general_strategy(self, user_profile: Dict, trend_data: Dict) -> List[Dict]:
        """Default content strategy"""
        viral_keywords = trend_data.get("viral_keywords", [])
        user_keywords = user_profile["content_preferences"]["preferred_topics"]

        ideas = []

        ideas.append({
            "type": "image",
            "title": f"Exploring {user_keywords[0] if user_keywords else 'Interesting Topics'}",
            "description": f"Engaging content about {user_keywords[0] if user_keywords else 'current interests'}",
            "keywords": user_keywords[:2] + viral_keywords[:2],
            "personalization_factors": ["user_interest", "trend_alignment"]
        })

        ideas.append({
            "type": "video",
            "title": f"{viral_keywords[0] if viral_keywords else 'Trending'} Insights & Updates",
            "description": f"Latest updates and insights about {viral_keywords[0] if viral_keywords else 'current trends'}",
            "keywords": user_keywords[:2] + viral_keywords[:2] + ["insights", "updates"],
            "personalization_factors": ["timeliness", "information_value"]
        })

        return ideas

    def _infer_content_types(self, keywords: List[str]) -> List[str]:
        """Infer preferred content types from keywords"""
        content_types = []

        video_indicators = ["tutorial", "review", "performance", "demonstration", "guide", "session", "class"]
        image_indicators = ["visual", "art", "design", "photo", "meme", "creation", "progress"]

        for keyword in keywords:
            keyword_lower = keyword.lower()
            if any(indicator in keyword_lower for indicator in video_indicators):
                content_types.append("video")
            elif any(indicator in keyword_lower for indicator in image_indicators):
                content_types.append("image")

        return list(set(content_types)) if content_types else ["image", "video"]

    def _recommend_content_frequency(self, engagement_ratio: float) -> str:
        """Recommend content frequency based on engagement"""
        if engagement_ratio > 0.8:
            return "daily"
        elif engagement_ratio > 0.6:
            return "every_other_day"
        else:
            return "weekly"

    def _suggest_content_types(self, keyword: str) -> List[str]:
        """Suggest content types for a specific keyword"""
        keyword_lower = keyword.lower()

        if any(topic in keyword_lower for topic in ["music", "performance", "tutorial", "workout", "cooking"]):
            return ["video", "image"]
        elif any(topic in keyword_lower for topic in ["art", "design", "photo", "food", "progress"]):
            return ["image", "video"]
        else:
            return ["image", "video"]

    def _suggest_content_angle(self, keyword: str) -> str:
        """Suggest content angle for a keyword"""
        angles = [
            "Educational perspective",
            "Behind the scenes look",
            "Expert insights",
            "Beginner-friendly guide",
            "Advanced techniques",
            "Inspirational story",
            "Step-by-step process",
            "Results and outcomes"
        ]
        return random.choice(angles)

    def _calculate_personalization_score(self, content_idea: Dict, user_profile: Dict) -> int:
        """Calculate how well content idea matches user profile"""
        score = 50  # Base score

        # Add points for keyword alignment
        user_keywords = user_profile["content_preferences"]["preferred_topics"]
        content_keywords = content_idea.get("keywords", [])

        keyword_matches = sum(1 for kw in content_keywords if kw in user_keywords)
        score += keyword_matches * 10

        # Add points for niche alignment
        if user_profile["primary_niche"] != "General":
            score += 20

        # Add points for engagement factors
        engagement_factors = content_idea.get("personalization_factors", [])
        score += len(engagement_factors) * 5

        return min(100, score)