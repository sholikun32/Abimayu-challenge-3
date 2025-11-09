from typing import List, Dict
from models.content_models import ContentIdea, TrendAnalysis, UserPreferences


class MediaDirector:
    def __init__(self):
        self.content_mix = {
            "viral": 40,
            "educational": 30,
            "entertaining": 20,
            "promotional": 10
        }

    def plan_content_strategy(self,
                              user_prefs: UserPreferences,
                              trend_analysis: TrendAnalysis) -> Dict:
        """Plan content strategy based on trends and user preferences"""
        print("🎬 Planning content strategy...")

        content_ideas = self._generate_content_ideas(user_prefs, trend_analysis)
        prioritized_content = self._prioritize_content(content_ideas, trend_analysis)

        # Determine niche from user preferences
        niche = "General"
        if user_prefs.preferred_niches:
            niche = user_prefs.preferred_niches[0]

        return {
            "content_strategy": {
                "target_keywords": user_prefs.preferred_keywords + trend_analysis.viral_keywords,
                "niche": niche,
                "content_mix": self.content_mix,
                "recommended_formats": [trend_analysis.best_content_type, "video", "image"]
            },
            "content_ideas": content_ideas,
            "prioritized_content": prioritized_content
        }

    def _generate_content_ideas(self,
                                user_prefs: UserPreferences,
                                trend_analysis: TrendAnalysis) -> List[ContentIdea]:
        """Generate content ideas based on trends and user preferences"""
        ideas = []

        viral_keywords = trend_analysis.viral_keywords
        user_keywords = user_prefs.preferred_keywords

        # Combine and get unique keywords
        all_keywords = list(dict.fromkeys(viral_keywords + user_keywords))

        # Ensure we have keywords
        if not all_keywords:
            all_keywords = ["Music", "Travel", "Tech"]

        # Idea 1: Based on top viral keyword
        ideas.append(ContentIdea(
            content_type=trend_analysis.best_content_type,
            theme=user_prefs.visual_affinities[0] if user_prefs.visual_affinities else "modern",
            description=f"Engaging content about {all_keywords[0]}",
            style="trending",
            priority="high",
            viral_score=85
        ))

        # Idea 2: Based on user preference
        if len(all_keywords) > 1:
            ideas.append(ContentIdea(
                content_type="image",
                theme="educational",
                description=f"Informative content about {all_keywords[1]}",
                style="informative",
                priority="medium",
                viral_score=75
            ))

        # Idea 3: Mixed content
        if len(all_keywords) > 2:
            ideas.append(ContentIdea(
                content_type="video" if trend_analysis.best_content_type == "image" else "image",
                theme="entertaining",
                description=f"Entertaining content combining {all_keywords[2]} and trends",
                style="engaging",
                priority="medium",
                viral_score=80
            ))

        return ideas

    def _prioritize_content(self,
                            content_ideas: List[ContentIdea],
                            trend_analysis: TrendAnalysis) -> List[ContentIdea]:
        """Prioritize content based on viral potential"""
        priority_order = {"high": 3, "medium": 2, "low": 1}

        prioritized = sorted(
            content_ideas,
            key=lambda x: (
                    priority_order.get(x.priority, 1) * 10 +
                    x.viral_score +
                    (10 if x.content_type == trend_analysis.best_content_type else 0)
            ),
            reverse=True
        )

        return prioritized[:3]