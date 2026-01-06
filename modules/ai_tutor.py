"""
TEF Master Cloud - AI Tutor Module
Interactive Chat interface with Internet Search capabilities.
"""

import streamlit as st
from ai_handler import ai_handler
from config import XP_PER_SEARCH_QUERY
from database import db

def render_ai_tutor():
    """Main AI Tutor interface."""
    st.header("🤖 AI Tutor & Research Assistant")
    st.markdown("Ask anything! The AI can search the web for real-time info.")
    
    # Initialize chat history
    if "tutor_messages" not in st.session_state:
        st.session_state.tutor_messages = []
        # Add welcome message
        st.session_state.tutor_messages.append({
            "role": "assistant",
            "content": "Bonjour! I am your AI Tutor. I can help you with grammar, find French news, or explain cultural topics. What do you want to learn today?"
        })

    # Display chat messages
    for msg in st.session_state.tutor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about French grammar, news, or culture..."):
        # Add user message
        st.session_state.tutor_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking (and searching if needed)..."):
                response = ai_handler.ask_tutor(prompt)
                st.markdown(response)
                
                # Add assistant message
                st.session_state.tutor_messages.append({"role": "assistant", "content": response})
                
                # Award XP (once per query)
                # Simple check to avoid spamming XP: just add it. Gamification is for fun.
                db.add_xp(XP_PER_SEARCH_QUERY, "AI Tutor Query")
