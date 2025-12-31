"""
TEF Master Local - Configuration Module
Centralized configuration for app settings, Ollama integration, and feature flags.
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "tef_master.db"

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_TIMEOUT = 120  # seconds

# Feature Flags
ENABLE_VOICE_TUTOR = False  # Set to True to enable Voice Tutor features

# App Settings
APP_TITLE = "TEF Master Local"
APP_ICON = "📚"
DEFAULT_PORT = 8501
SERVER_ADDRESS = "0.0.0.0"  # For mobile network access

# Gamification Settings
XP_PER_GRAMMAR_QUESTION = 10
XP_PER_READING_QUESTION = 15
XP_PER_WRITING_SUBMISSION = 50
XP_PER_VOICE_PRACTICE = 20

# Week unlock requirements
QUESTIONS_TO_UNLOCK_WEEK = 20  # Complete 20 questions to unlock next week

# Mobile breakpoints (for CSS)
MOBILE_MAX_WIDTH = "768px"

# Theme colors
PRIMARY_COLOR = "#4A90E2"
SUCCESS_COLOR = "#27AE60"
WARNING_COLOR = "#F39C12"
DANGER_COLOR = "#E74C3C"

# TEF Score ranges
TEF_SCORE_MAX = 450
TEF_WRITING_STRUCTURE_MAX = 150
TEF_WRITING_VOCABULARY_MAX = 150
TEF_WRITING_GRAMMAR_MAX = 150

# Resource categories (extensible)
RESOURCE_CATEGORIES = [
    "Grammar",
    "Reading",
    "Listening",
    "Writing",
    "Practice Tests",
    "Cultural Content",
    "Vocabulary",
    "Pronunciation"
]

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
