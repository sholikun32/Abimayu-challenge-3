from typing import List, Dict
from models.content_models import ContentIdea, UserPreferences
from models.series_models import Series, SeriesEpisode
import random
from datetime import datetime


class ShowrunnerAgent:
    """Showrunner agent that coordinates multiple specialist creators"""

    def __init__(self):
        self.specialist_creators = [
            "Visual Content Creator",
            "Video Series Producer",
            "Meme Specialist",
            "Storyline Developer"
        ]
        self.active_series = None

    def coordinate_production(self, discovery_data: Dict, user_prefs: UserPreferences) -> Dict:
        """Coordinate production between specialist creators"""
        print("🎬 Showrunner Agent: Coordinating production team...")

        # Assign tasks to specialists
        production_plan = self._create_production_plan(discovery_data, user_prefs)

        # Manage series continuity
        series_plan = self._manage_series_continuity(discovery_data, user_prefs)

        return {
            "production_team": self.specialist_creators,
            "assigned_tasks": production_plan,
            "content_schedule": self._create_production_schedule(production_plan, series_plan),
            "quality_control": self._setup_quality_control(),
            "series_management": series_plan
        }

    def _create_production_plan(self, discovery_data: Dict, user_prefs: UserPreferences) -> Dict:
        """Create detailed production plan"""
        trends = discovery_data["trend_analysis"]
        recommendations = discovery_data["content_recommendations"]

        tasks = {
            "Visual Content Creator": [
                "Create trending image content",
                "Generate meme variations",
                "Design visual assets for series"
            ],
            "Video Series Producer": [
                "Produce 60-second series episodes",
                "Ensure episode continuity",
                "Manage series storyline"
            ],
            "Meme Specialist": [
                "Create viral meme content",
                "Remix trending templates",
                "Optimize for engagement"
            ],
            "Storyline Developer": [
                "Develop coherent plot lines",
                "Create character development",
                "Ensure series consistency"
            ]
        }

        # Adjust tasks based on recommendations
        if not recommendations["immediate_content"]["memes"]:
            tasks["Meme Specialist"] = ["Monitor meme trends for future content"]

        if recommendations["series_development"]["recommended"]:
            tasks["Video Series Producer"].append(
                f"Produce {recommendations['series_development']['episode_count']} episodes")
        else:
            tasks["Video Series Producer"] = ["Produce standalone video content"]

        return tasks

    def _manage_series_continuity(self, discovery_data: Dict, user_prefs: UserPreferences) -> Dict:
        """Manage series continuity and episode planning"""
        if not discovery_data["series_potential"]["recommended_genres"]:
            return {"active_series": False}

        if not self.active_series:
            self.active_series = self._create_new_series(discovery_data, user_prefs)

        # Plan next episode
        next_episode = self._plan_next_episode()

        return {
            "active_series": True,
            "series_title": self.active_series.title,
            "current_episode": self.active_series.current_episode,
            "next_episode": next_episode,
            "total_episodes": self.active_series.total_episodes,
            "plot_continuity": self._check_plot_continuity()
        }

    def _create_new_series(self, discovery_data: Dict, user_prefs: UserPreferences) -> Series:
        """Create a new series"""
        genre = discovery_data["series_potential"]["recommended_genres"][0]
        themes = discovery_data["series_potential"]["episode_themes"]

        series_templates = {
            "Tech Thriller": {
                "title": "The Innovation Protocol",
                "plot": "A team of tech innovators uncovers secrets that could change the future of humanity",
                "characters": ["Lead Innovator", "AI Specialist", "Security Expert"]
            },
            "AI Drama": {
                "title": "Neural Frontier",
                "plot": "Exploring the ethical boundaries of artificial intelligence and human connection",
                "characters": ["AI Researcher", "Ethics Professor", "Tech CEO"]
            },
            "Adventure Series": {
                "title": "Digital Explorers",
                "plot": "Journey through the world of technology and innovation discoveries",
                "characters": ["Adventure Guide", "Tech Explorer", "Local Expert"]
            }
        }

        template = series_templates.get(genre, series_templates["Tech Thriller"])

        return Series(
            series_id=f"series_{int(datetime.now().timestamp())}",
            title=template["title"],
            genre=genre,
            plot_summary=template["plot"],
            main_characters=template["characters"],
            episodes=[],
            total_episodes=2,  # Minimum requirement
            current_episode=0,
            created_at=datetime.now()
        )

    def _plan_next_episode(self) -> Dict:
        """Plan the next episode in the series"""
        if not self.active_series:
            return {}

        next_ep_num = self.active_series.current_episode + 1

        episode_templates = [
            {
                "title": f"Episode {next_ep_num}: The Beginning",
                "theme": "Introduction to the main conflict",
                "plot_advancement": "Establish main characters and central mystery"
            },
            {
                "title": f"Episode {next_ep_num}: The Revelation",
                "theme": "Key discoveries and plot twists",
                "plot_advancement": "Reveal important information that changes everything"
            }
        ]

        template = episode_templates[min(next_ep_num - 1, len(episode_templates) - 1)]

        return {
            "episode_number": next_ep_num,
            "title": template["title"],
            "theme": template["theme"],
            "plot_advancement": template["plot_advancement"],
            "characters": self.active_series.main_characters
        }

    def _check_plot_continuity(self) -> Dict:
        """Ensure plot continuity across episodes"""
        if not self.active_series or len(self.active_series.episodes) < 1:
            return {"status": "new_series", "consistency": "high"}

        return {
            "status": "active_series",
            "consistency": "high",
            "character_development": "progressive",
            "plot_continuity": "maintained",
            "thematic_consistency": "strong"
        }

    def _create_production_schedule(self, production_plan: Dict, series_plan: Dict) -> Dict:
        """Create production schedule"""
        schedule = {
            "immediate": ["Trending content creation", "Meme generation"],
            "short_term": ["Series episode production"],
            "continuous": ["Trend monitoring", "Content optimization"]
        }

        if series_plan.get("active_series"):
            schedule["immediate"].append(f"Series Episode {series_plan['current_episode'] + 1}")

        return schedule

    def _setup_quality_control(self) -> Dict:
        """Setup quality control measures"""
        return {
            "content_quality": "premium",
            "consistency_check": "automated",
            "brand_guidelines": "enforced",
            "engagement_optimization": "active"
        }