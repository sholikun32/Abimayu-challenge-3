from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class UserPreferences:
    id: str
    user_id: str
    preferred_keywords: List[str]
    preferred_niches: List[str]
    preferred_genders: List[str]
    visual_affinities: List[str]
    active_hours: List[str]
    engagement_ratio: float

@dataclass
class TrendAnalysis:
    viral_keywords: List[str]
    engagement_patterns: Dict[str, int]
    best_content_type: str
    total_posts_analyzed: int
    viral_score: int
    meme_keywords: List[str] = None

    def __post_init__(self):
        if self.meme_keywords is None:
            self.meme_keywords = []

@dataclass
class ContentIdea:
    content_type: str
    theme: str
    description: str
    style: str
    duration: Optional[str] = None
    priority: str = "medium"
    viral_score: int = 0

@dataclass
class GeneratedContent:
    content_type: str
    caption: str
    description: str
    keywords: List[str]
    media_source: str
    viral_score: int
    trend_alignment: List[str]
    episode_data: Optional[Dict] = None

    def __post_init__(self):
        if self.episode_data is None:
            self.episode_data = {}

@dataclass
class PostResult:
    success: bool
    post_id: str
    content_type: str
    posted_at: datetime
    engagement_metrics: Dict