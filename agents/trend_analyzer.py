from typing import List, Dict
from models.content_models import TrendAnalysis, UserPreferences
from services.circlo_api import CircloAPI


class TrendAnalyzer:
    def __init__(self):
        self.circlo_api = CircloAPI()

    def analyze_trends(self, user_preferences: UserPreferences) -> TrendAnalysis:
        """Analyze current trends and viral content"""
        print("🔍 Analyzing current trends...")

        # Get trending posts based on user preferences
        keywords = user_preferences.preferred_keywords or ["tech", "innovation", "AI", "digital", "future"]
        trending_posts = self.circlo_api.get_trending_posts(keywords)

        # Analyze trends
        trend_data = self._analyze_trend_data(trending_posts)

        return TrendAnalysis(
            viral_keywords=trend_data["viral_keywords"],
            engagement_patterns=trend_data["engagement_patterns"],
            best_content_type=trend_data["best_content_type"],
            total_posts_analyzed=len(trending_posts),
            viral_score=trend_data["viral_score"]
        )

    def _analyze_trend_data(self, posts: List[Dict]) -> Dict:
        """Analyze trend data from posts"""
        keyword_analysis = {}
        engagement_patterns = {"image": 50, "video": 40}
        content_types = {"image": 1, "video": 1}

        # If we have real posts, analyze them
        if posts:
            print(f"   📊 Analyzing {len(posts)} real posts from Circlo...")
            for post in posts:
                # Analyze keywords from real posts
                for keyword in post.get("keywords", []):
                    keyword_analysis[keyword] = keyword_analysis.get(keyword, 0) + 1

                # Analyze engagement from real posts
                engagement = post.get("likeCount", 0) + post.get("commentCount", 0)
                post_type = post.get("postType", "unknown")
                engagement_patterns[post_type] = engagement_patterns.get(post_type, 0) + engagement
                content_types[post_type] = content_types.get(post_type, 0) + 1

            # Get viral keywords from real data
            viral_keywords = sorted(
                keyword_analysis.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            viral_keywords = [kw[0] for kw in viral_keywords]

            # Determine best content type from real data
            best_content_type = max(
                engagement_patterns.items(),
                key=lambda x: x[1],
                default=("image", 0)
            )[0]

            viral_score = min(100, len(posts) * 2 + len(viral_keywords) * 10)

        else:
            # Use default trends if no posts
            print("   🧪 Using default trends (no posts found)")
            viral_keywords = ["AI", "technology", "innovation", "digital", "future"]
            best_content_type = "image"
            viral_score = 60

        print(f"   🔥 Viral keywords: {', '.join(viral_keywords[:3])}")
        print(f"   🎯 Best content type: {best_content_type}")

        return {
            "viral_keywords": viral_keywords,
            "engagement_patterns": engagement_patterns,
            "best_content_type": best_content_type,
            "viral_score": viral_score
        }