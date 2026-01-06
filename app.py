"""
TEF Master Cloud - Main Application
A comprehensive Learning Management System for TEF exam preparation.
Powered by Google Gemini and Firebase.
"""

import streamlit as st
import warnings
import logging

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
# Specific suppression for the httplib2 noise if possible, usually Deprecation covers it

# Configure logging to reduce noise
logging.getLogger("googleapiclient").setLevel(logging.ERROR)
logging.getLogger("httplib2").setLevel(logging.ERROR)

from streamlit_option_menu import option_menu

# Import modules
from database import db
from config import (
    APP_TITLE, APP_ICON, 
    ENABLE_VOICE_TUTOR, GEMINI_CONFIG
)
from components.progress_bar import (
    display_xp_card, display_streak, display_progress_bar
)
from modules.roadmap import render_roadmap
from modules.writing_clinic import render_writing_clinic
from modules.resources import render_resources
from modules.voice_tutor import render_voice_tutor
from modules.ai_tutor import render_ai_tutor


# ==================== Page Configuration ====================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== Custom CSS for Mobile Optimization ====================
st.markdown("""
<style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.5rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.3rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
    }
    
    /* Improved button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Card-like containers */
    .stContainer {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background-color: #4A90E2;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==================== Initialize Session State ====================
def init_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = "roadmap"


# ==================== Sidebar ====================
def render_sidebar():
    """Render sidebar with user stats and navigation."""
    with st.sidebar:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.markdown("*Your AI-Powered TEF Companion*")
        st.markdown("---")
        
        # User Progress Section
        st.subheader("📊 Your Progress")
        
        # XP Display
        total_xp = db.get_total_xp()
        daily_xp = db.get_daily_xp()
        display_xp_card(total_xp, daily_xp)
        
        st.markdown("---")
        
        # Streak Display
        streak_data = db.get_streak()
        display_streak(streak_data["current"], streak_data["best"])
        
        st.markdown("---")
        
        # Overall Progress
        st.subheader("🎯 Overall Mastery")
        from data.syllabus import get_total_weeks
        total_weeks = get_total_weeks()
        unlocked_weeks = sum(1 for i in range(1, total_weeks + 1) if db.is_week_unlocked(i))
        display_progress_bar(unlocked_weeks, total_weeks, "Weeks Completed")
        
        st.markdown("---")
        
        # Quick Links
        st.subheader("🔗 Quick Links")
        st.markdown("- [Official TEF Website](https://www.lefrancaisdesaffaires.fr/tests-diplomes/test-evaluation-francais-tef/)")
        st.markdown("- [CEFR Levels Explained](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions)")
        
        st.markdown("---")
        
        # AI Status
        from ai_handler import ai_handler
        status = ai_handler.get_status()
        st.caption(status)
        if "Local" in status:
             st.caption("⚡ Running locally on GPU")
        elif "Cloud" in status:
             st.caption(f"☁️ Running on Gemini Cloud ({GEMINI_CONFIG['model']})")


# ==================== Main Navigation ====================
def main():
    """Main application logic."""
    init_session_state()
    render_sidebar()
    
    # Main navigation menu
    menu_options = ["📚 Study Roadmap", "🤖 AI Tutor", "✍️ Writing Clinic", "📖 Resources"]
    menu_icons = ["book", "robot", "pencil", "folder"]
    
    if ENABLE_VOICE_TUTOR:
        menu_options.append("🎙️ Voice Tutor")
        menu_icons.append("mic")
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#4A90E2", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#4A90E2"},
        }
    )
    
    # Render selected page
    st.markdown("---")
    
    if selected == "📚 Study Roadmap":
        render_roadmap()

    elif selected == "🤖 AI Tutor":
        render_ai_tutor()
    
    elif selected == "✍️ Writing Clinic":
        render_writing_clinic()
    
    elif selected == "📖 Resources":
        render_resources()
    
    elif selected == "🎙️ Voice Tutor" and ENABLE_VOICE_TUTOR:
        render_voice_tutor()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 12px;'>
            <p>TEF Master Cloud | Built with Streamlit & Gemini | 
            <a href='https://github.com' target='_blank'>GitHub</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================== Entry Point ====================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"""
        **An error occurred:** {str(e)}
        
        **Troubleshooting:**
        - Check your internet connection
        - Verify API keys are configured in secrets.toml
        - Ensure Firebase credentials are valid
        
        **Need help?** Check the README or restart the application.
        """)
        st.exception(e)
