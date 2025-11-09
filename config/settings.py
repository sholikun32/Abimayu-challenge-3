import os
from datetime import timedelta


class Settings:
    # API Keys
    CIRCLO_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwZmRjNjkxLTIzMDAtNDM4Mi04ODI4LWE1NzI0YjQ5OTNiYiIsImVtYWlsIjoiZGV2QHNlbnRpLmdsb2JhbCIsImlzX2d1ZXN0IjpmYWxzZSwiaWF0IjoxNzYyNTcyMDYzLCJleHAiOjQ5MTgzMzIwNjN9.deShmmIRMKrRS1avZtNwY0u01_QwEcdBeDd_DJ2Qfxw"

    # Gemini API - For image and video generation
    GEMINI_API_KEY = "AIzaSyCf7UaqKDceSF8gXMfXQaONZXCPDDYRHnk"

    # API Endpoints
    CIRCLO_BASE_URL = "https://api.getcirclo.com/api"
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    # Available Niches in Circlo - CORRECTED based on API errors
    AVAILABLE_NICHES = [
        "General", "Blogger", "Traveler", "Foodie",
        "Fitness Coach", "Fashion Influencer", "Gamer",
        "Photographer", "Artist", "Musician", "Writer",
        "Entrepreneur", "Educator", "Health Expert",
        "Lifestyle Influencer", "Business Coach"
    ]

    # Content Settings
    CONTENT_TYPES = ["image", "video"]
    MAX_KEYWORDS = 6
    SCHEDULE_INTERVAL = timedelta(minutes=5)

    # Agent Settings
    TREND_ANALYSIS_LIMIT = 20
    CONTENT_QUEUE_SIZE = 3

    # Media Generation Settings
    IMAGE_STYLES = ["realistic", "artistic", "minimalist", "humorous", "professional"]
    VIDEO_DURATIONS = [30, 60, 90]  # seconds


settings = Settings()