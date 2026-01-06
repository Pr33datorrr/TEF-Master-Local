"""
TEF Master Cloud - Configuration Module
Centralized configuration for app settings, Hybrid AI integration (Local/Cloud), and feature flags.
"""

import os
from pathlib import Path
import streamlit as st

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# ==================== AI Configuration ====================

# AI Provider Options: "AUTO", "LOCAL", "CLOUD"
# AUTO: Tries Local first, falls back to Cloud
# LOCAL: Forces Local (Ollama)
# CLOUD: Forces Cloud (Gemini)
AI_PROVIDER = "AUTO"

# Internet Search
SEARCH_ENABLED = True

# 1. Local Configuration (Ollama)
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "gemma3:4b",   # User confirmed local model
    "timeout": 120
}

# 2. Cloud Configuration (Gemini)
GEMINI_CONFIG = {
    # Using 'gemini-2.0-flash-exp' as primary for speed/performance 
    # but kept 'gemini-1.5-flash' variable invalid if needed.
    # User also mentioned 'gemma-3-12b-it' might be available via API.
    "model": "gemma-3-27b-it", 
    "api_key_env_var": "GEMINI_API_KEY"
}


# ==================== Feature Flags ====================
ENABLE_VOICE_TUTOR = False  # Set to True to enable Voice Tutor features

# ==================== App Settings ====================
APP_TITLE = "TEF Master Cloud"
APP_ICON = "🇫🇷"

# Gamification Settings
XP_PER_GRAMMAR_QUESTION = 10
XP_PER_READING_QUESTION = 15
XP_PER_WRITING_SUBMISSION = 50
XP_PER_VOICE_PRACTICE = 20
XP_PER_SEARCH_QUERY = 5     # New XP for learning via search

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
