"""
TEF Master Local - Progress Display Components
Reusable UI components for progress visualization.
"""

import streamlit as st


def display_progress_bar(current_value: int, max_value: int, label: str = "Progress"):
    """Display a progress bar with percentage."""
    percentage = (current_value / max_value * 100) if max_value > 0 else 0
    st.progress(min(current_value / max_value, 1.0) if max_value > 0 else 0)
    st.caption(f"{label}: {current_value}/{max_value} ({percentage:.1f}%)")


def display_xp_card(total_xp: int, daily_xp: int):
    """Display XP in a card format."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total XP", f"{total_xp:,}", delta=None)
    with col2:
        st.metric("Today's XP", f"+{daily_xp}", delta=daily_xp if daily_xp > 0 else None)


def display_streak(current_streak: int, best_streak: int):
    """Display streak information with fire emoji."""
    if current_streak > 0:
        st.markdown(f"### 🔥 {current_streak} day streak!")
    else:
        st.markdown("### 💤 No active streak")
    
    st.caption(f"Best streak: {best_streak} days")


def display_level_badge(level: str):
    """Display CEFR level badge."""
    colors = {
        "A1": "#3498db",  # Blue
        "A2": "#2ecc71",  # Green
        "B1": "#f39c12",  # Orange
        "B2": "#e74c3c",  # Red
    }
    
    color = colors.get(level, "#95a5a6")
    st.markdown(
        f'<span style="background-color:{color}; color:white; padding:5px 15px; '
        f'border-radius:20px; font-weight:bold;">{level}</span>',
        unsafe_allow_html=True
    )


def display_week_card(week_data: dict, is_locked: bool = False, is_current: bool = False):
    """Display a week card in the roadmap using native Streamlit components."""
    week_num = week_data["week"]
    title = week_data["title"]
    level = week_data["level"]
    xp_value = week_data["xp_value"]
    
    # Use expander for better mobile UX
    status_emoji = "🔒" if is_locked else "✅" if is_current else "📖"
    expander_label = f"{status_emoji} Week {week_num}: {title} ({level}) - +{xp_value} XP"
    
    # IMPORTANT: Expand unlocked weeks by default
    with st.expander(expander_label, expanded=(not is_locked)):
        if is_locked:
            st.warning("🔒 Complete previous weeks to unlock this content")
        else:
            # Show week details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Level:** {level}")
                st.markdown(f"**XP Reward:** +{xp_value}")
            with col2:
                topics = week_data.get("grammar_topics", [])
                if topics:
                    st.markdown("**Topics:**")
                    for topic in topics[:2]:  # Show first 2
                        st.markdown(f"• {topic}")
            
            # Return True to indicate should show buttons
            return True
    
    return False




def show_loading_spinner(message: str = "Generating innovative exercises..."):
    """Display a loading spinner for AI operations."""
    return st.spinner(message)
