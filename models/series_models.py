from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class SeriesEpisode:
    episode_number: int
    title: str
    script: str
    scenes: List[Dict]
    duration: str
    characters: List[str]
    plot_advancement: str
    media_source: str
    keywords: List[str]
    posted: bool = False

@dataclass
class Series:
    series_id: str
    title: str
    genre: str
    plot_summary: str
    main_characters: List[str]
    episodes: List[SeriesEpisode]
    total_episodes: int
    current_episode: int
    created_at: datetime