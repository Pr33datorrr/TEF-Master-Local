"""
TEF Master Local - Enhanced Writing Clinic Module
AI-powered essay grading with TEF rubric feedback + Research-based prompts.
"""

import streamlit as st
from database import db
from ai_handler import ai_handler
from components.progress_bar import show_loading_spinner
from config import XP_PER_WRITING_SUBMISSION, TEF_SCORE_MAX
from data.writing_prompts import get_all_prompts, get_prompts_by_type, get_random_prompt


def render_writing_clinic():
    """Main Writing Clinic interface."""
    st.header("✍️ TEF Writing Clinic")
    st.markdown("Get your essays graded by AI using the **official TEF rubric** with real TEF prompts!")
    
    # Prompt selection mode
    st.subheader("1️⃣ Select Your Practice Mode")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Random Section A (Fait Divers - 80 words)", use_container_width=True):
            prompt = get_random_prompt("Section A")
            st.session_state.selected_prompt = prompt
            st.session_state.clear_essay = True
    
    with col2:
        if st.button("🎲 Random Section B (Letter - 200 words)", use_container_width=True):
            prompt = get_random_prompt("Section B")
            st.session_state.selected_prompt = prompt
            st.session_state.clear_essay = True
    
    # Manual selection
    all_prompts = get_all_prompts()
    prompt_titles = [f"{p['id']}: {p['topic']}" for p in all_prompts]
    selected_title = st.selectbox(
        "Or choose a specific prompt:",
        ["Select manually..."] + prompt_titles,
        key="manual_prompt"
    )
    
    if selected_title != "Select manually...":
        prompt_id = selected_title.split(":")[0]
        prompt = next((p for p in all_prompts if p["id"] == prompt_id), None)
        if prompt:
            st.session_state.selected_prompt = prompt
    
    # Display selected prompt
    if "selected_prompt" in st.session_state:
        prompt = st.session_state.selected_prompt
        
        with st.expander("📋 Your Writing Task", expanded=True):
            st.markdown(f"**Type:** {prompt['type']}")
            st.markdown(f"**Topic:** {prompt['topic']}")
            st.markdown(f"**Target:** {prompt['word_count']} words")
            st.markdown("---")
            st.markdown(f"### 📝 Prompt")
            st.info(prompt['prompt'])
            
            # Show metadata hints
            metadata = prompt.get('metadata', {})
            if metadata:
                st.markdown("### 💡 Hints")
                
                col1, col2 = st.columns(2)
                with col1:
                    if 'tense_focus' in metadata:
                        st.markdown("**Grammar Focus:**")
                        for tense in metadata['tense_focus']:
                            st.markdown(f"- {tense}")
                    if 'grammar_focus' in metadata:
                        st.markdown("**Grammar Focus:**")
                        for item in metadata['grammar_focus']:
                            st.markdown(f"- {item}")
                
                with col2:
                    if 'key_vocab' in metadata:
                        st.markdown("**Key Vocabulary:**")
                        st.markdown(", ".join(metadata['key_vocab']))
                    if 'key_arguments' in metadata:
                        st.markdown("**Possible Arguments:**")
                        for arg in metadata['key_arguments']:
                            st.markdown(f"- {arg}")
                
                if 'structure_hints' in metadata:
                    st.markdown("**Structure Tips:**")
                    st.markdown(metadata['structure_hints'])
        
        # Essay input
        st.subheader("2️⃣ Write Your Essay")
        
        # Clear essay if new prompt selected
        if st.session_state.get('clear_essay', False):
            if 'essay_input' in st.session_state:
                del st.session_state['essay_input']
            st.session_state.clear_essay = False
        
        essay = st.text_area(
            "Type your essay in French:",
            height=300,
            key="essay_input",
            placeholder="Écrivez votre texte ici..."
        )
        
        # Word count
        word_count = len(essay.split()) if essay else 0
        target = prompt['word_count']
        word_diff = word_count - target
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.caption(f"Word count: {word_count} / {target} ({word_diff:+d})")
        with col2:
            if abs(word_diff) <= 20:
                st.success("✅ Good length!")
            elif word_diff > 20:
                st.warning("⚠️ Too long")
            else:
                st.info("ℹ️ Add more words")
        
        # Grade button
        col1, col2 = st.columns([1, 3])
        with col1:
            grade_button = st.button("🎯 Grade My Essay", disabled=word_count < 20)
        
        if grade_button:
            with show_loading_spinner("Analyzing your essay according to TEF rubric..."):
                grading = ai_handler.grade_essay(essay, prompt['type'])
                st.session_state.writing_grading = grading
                
                # Award XP
                db.add_xp(XP_PER_WRITING_SUBMISSION, f"Writing: {prompt['topic']}")
                
                # Save progress
                db.save_progress(0, "writing", True, grading["total_score"])
        
        # Display grading results
        if "writing_grading" in st.session_state:
            st.markdown("---")
            st.subheader("📊 Your TEF Score")
            
            grading = st.session_state.writing_grading
            
            # Overall score
            total_score = grading["total_score"]
            percentage = (total_score / TEF_SCORE_MAX) * 100
            
            st.metric(
                "Total Score",
                f"{total_score}/{TEF_SCORE_MAX}",
                delta=f"{percentage:.1f}%"
            )
            
            # Detailed scores
            st.markdown("### 📈 Score Breakdown")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Structure", f"{grading['structure_score']}/150")
                with st.expander("Structure Feedback"):
                    st.markdown(grading["structure_feedback"])
            
            with col2:
                st.metric("Vocabulary", f"{grading['vocabulary_score']}/150")
                with st.expander("Vocabulary Feedback"):
                    st.markdown(grading["vocabulary_feedback"])
            
            with col3:
                st.metric("Grammar", f"{grading['grammar_score']}/150")
                with st.expander("Grammar Feedback"):
                    st.markdown(grading["grammar_feedback"])
            
            # Suggestions
            st.markdown("### 💡 Improvement Suggestions")
            for i, suggestion in enumerate(grading.get("suggestions", []), 1):
                st.markdown(f"{i}. {suggestion}")
            
            st.success(f"🎉 Essay graded! +{XP_PER_WRITING_SUBMISSION} XP earned")
            
            # Reset button
            if st.button("📝 Try Another Prompt"):
                del st.session_state.writing_grading
                del st.session_state.selected_prompt
                if 'essay_input' in st.session_state:
                    del st.session_state.essay_input
                st.rerun()
    else:
        st.info("👆 Click a button above to get started with a writing prompt!")
