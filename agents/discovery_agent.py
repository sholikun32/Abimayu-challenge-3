from typing import List, Dict
from models.content_models import TrendAnalysis, UserPreferences
from services.circlo_api import CircloAPI
import random


class DiscoveryAgent:
    """Enhanced discovery agent that finds and reacts to online trends"""

    def __init__(self):
        self.circlo_api = CircloAPI()
        self.trend_categories = {
            "viral_memes": ["meme", "funny", "viral", "trending"],
            "tech_innovation": ["tech", "ai", "innovation", "future"],
            "entertainment": ["music", "movie", "series", "entertainment"],
            "lifestyle": ["travel", "food", "fitness", "lifestyle"]
        }

    def discover_trends(self, user_preferences: UserPreferences) -> Dict:
        """Discover comprehensive trends including memes and series potential"""
        print("🔍 Discovery Agent: Analyzing online trends...")

        # Get trending posts
        keywords = user_preferences.preferred_keywords or ["tech", "innovation", "AI"]
        trending_posts = self.circlo_api.get_trending_posts(keywords)

        # Analyze multiple aspects
        trend_analysis = self._analyze_comprehensive_trends(trending_posts)
        meme_potential = self._analyze_meme_potential(trending_posts)
        series_potential = self._analyze_series_potential(user_preferences, trend_analysis)

        return {
            "trend_analysis": trend_analysis,
            "meme_potential": meme_potential,
            "series_potential": series_potential,
            "content_recommendations": self._generate_recommendations(trend_analysis, meme_potential, series_potential)
        }

    def _analyze_comprehensive_trends(self, posts: List[Dict]) -> TrendAnalysis:
        """Analyze trends with enhanced metrics"""
        keyword_analysis = {}
        engagement_patterns = {}
        content_types = {}
        meme_keywords = []

        for post in posts:
            # Keyword analysis
            for keyword in post.get("keywords", []):
                keyword_analysis[keyword] = keyword_analysis.get(keyword, 0) + 1
                # Identify meme potential
                if any(meme_word in keyword.lower() for meme_word in self.trend_categories["viral_memes"]):
                    meme_keywords.append(keyword)

            # Engagement analysis
            engagement = post.get("likeCount", 0) + post.get("commentCount", 0)
            post_type = post.get("postType", "unknown")
            engagement_patterns[post_type] = engagement_patterns.get(post_type, 0) + engagement
            content_types[post_type] = content_types.get(post_type, 0) + 1

        # Get viral keywords
        viral_keywords = sorted(keyword_analysis.items(), key=lambda x: x[1], reverse=True)[:5]
        viral_keywords = [kw[0] for kw in viral_keywords]

        # Determine best content type
        best_content_type = max(engagement_patterns.items(), key=lambda x: x[1], default=("image", 0))[0]

        return TrendAnalysis(
            viral_keywords=viral_keywords,
            engagement_patterns=engagement_patterns,
            best_content_type=best_content_type,
            total_posts_analyzed=len(posts),
            viral_score=min(100, len(posts) * 2 + len(viral_keywords) * 10),
            meme_keywords=list(set(meme_keywords))[:3]
        )

    def _analyze_meme_potential(self, posts: List[Dict]) -> Dict:
        """Analyze potential for meme creation"""
        meme_engagement = 0
        meme_count = 0

        for post in posts:
            caption = post.get("caption", "").lower()
            keywords = [kw.lower() for kw in post.get("keywords", [])]

            # Check for meme characteristics
            if any(meme_indicator in caption for meme_indicator in ["meme", "funny", "lol", "😂", "🤣"]):
                meme_count += 1
                meme_engagement += post.get("likeCount", 0) + post.get("commentCount", 0)

        meme_potential_score = min(100, (meme_count * 20) + (meme_engagement // 10))

        return {
            "meme_potential_score": meme_potential_score,
            "meme_templates_suggested": self._suggest_meme_templates(posts),
            "virality_confidence": "high" if meme_potential_score > 70 else "medium" if meme_potential_score > 40 else "low"
        }

    def _analyze_series_potential(self, user_preferences: UserPreferences, trend_analysis: TrendAnalysis) -> Dict:
        """Analyze potential for series creation based on trends"""
        preferred_genres = self._map_keywords_to_genres(
            user_preferences.preferred_keywords + trend_analysis.viral_keywords)

        return {
            "recommended_genres": preferred_genres[:2],
            "episode_themes": self._generate_episode_themes(trend_analysis.viral_keywords),
            "series_potential_score": min(100, len(trend_analysis.viral_keywords) * 15),
            "character_concepts": self._generate_character_concepts(user_preferences, trend_analysis)
        }

    def _suggest_meme_templates(self, posts: List[Dict]) -> List[str]:
        """Suggest meme templates based on trending content"""
        templates = [
            "Reaction Meme", "Comparison Meme", "Trending Audio Meme",
            "Context Meme", "Challenge Meme", "Remix Meme"
        ]
        return random.sample(templates, min(3, len(templates)))

    def _map_keywords_to_genres(self, keywords: List[str]) -> List[str]:
        """Map keywords to potential series genres"""
        genre_map = {
            "tech": "Tech Thriller", "ai": "AI Drama", "future": "Sci-Fi",
            "music": "Music Documentary", "travel": "Adventure Series",
            "art": "Creative Journey", "innovation": "Innovation Showcase"
        }

        genres = []
        for keyword in keywords:
            key_lower = keyword.lower()
            for genre_key, genre_name in genre_map.items():
                if genre_key in key_lower and genre_name not in genres:
                    genres.append(genre_name)

        return genres if genres else ["Tech Documentary", "Innovation Series"]

    def _generate_episode_themes(self, viral_keywords: List[str]) -> List[str]:
        """Generate episode themes based on viral topics"""
        themes = []
        for keyword in viral_keywords[:3]:
            themes.append(f"The Future of {keyword}")
            themes.append(f"{keyword} Revolution")
            themes.append(f"Behind the {keyword}")
        return themes

    def _generate_character_concepts(self, user_preferences: UserPreferences, trend_analysis: TrendAnalysis) -> List[
        str]:
        """Generate character concepts for series"""
        concepts = [
            "Tech Innovator exploring new frontiers",
            "AI Researcher solving complex problems",
            "Digital Artist creating futuristic visions",
            "Adventure Seeker discovering innovations"
        ]
        return concepts[:2]

    def _generate_recommendations(self, trend_analysis: TrendAnalysis, meme_potential: Dict,
                                  series_potential: Dict) -> Dict:
        """Generate content recommendations"""
        return {
            "immediate_content": {
                "memes": meme_potential["meme_potential_score"] > 50,
                "trending_posts": True,
                "educational_content": True
            },
            "series_development": {
                "recommended": series_potential["series_potential_score"] > 60,
                "genre": series_potential["recommended_genres"][0] if series_potential[
                    "recommended_genres"] else "Tech Documentary",
                "episode_count": 2
            },
            "content_schedule": {
                "frequency": "continuous",
                "next_series_episode": "immediate" if series_potential["series_potential_score"] > 60 else "next_cycle"
            }
        }