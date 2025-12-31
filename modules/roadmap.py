"""
TEF Master Local - Study Roadmap Module
Dynamic week-by-week curriculum with Grammar Lab and Reading Lounge.
"""

import streamlit as st
from database import db
from ollama_handler import ollama_handler
from data.syllabus import TEF_SYLLABUS, get_week_data, get_all_levels
from components.progress_bar import (
    display_week_card, display_progress_bar, show_loading_spinner
)
from config import XP_PER_GRAMMAR_QUESTION, XP_PER_READING_QUESTION


def render_roadmap():
    """Main roadmap interface."""
    st.header("📚 Your Study Roadmap")
    
    # CHECK IF MODULE IS SELECTED FIRST
    if "current_module" in st.session_state and "current_week" in st.session_state:
        week_data = get_week_data(st.session_state.current_week)
        
        if week_data is None:
            st.error(f"Week {st.session_state.current_week} data not found!")
            if st.button("← Back to Roadmap"):
                del st.session_state.current_module
                del st.session_state.current_week
                st.rerun()
            return
        
        # Render the selected module
        if st.session_state.current_module == "grammar":
            render_grammar_lab(week_data)
        elif st.session_state.current_module == "reading":
            render_reading_lounge(week_data)
        elif st.session_state.current_module == "writing":
            # Writing content
            st.markdown("---")
            st.subheader(f"✍️ Writing Practice - Week {st.session_state.current_week}")
            
            st.info("💡 **Tip:** For full writing practice with AI grading, use the '✍️ Writing Clinic' tab at the top!")
            
            # Show week's writing task
            writing_task = week_data.get("writing_task", "Practice writing on the topics covered this week.")
            st.markdown("**This week's focus:**")
            st.markdown(f"- {writing_task}")
            
            st.markdown("**Quick practice ideas:**")
            topics = week_data.get("grammar_topics", [])
            for i, topic in enumerate(topics[:3], 1):
                st.markdown(f"{i}. Write 3-4 sentences using: **{topic}**")
            
            # Back button
            st.markdown("---")
            if st.button("← Back to Roadmap", use_container_width=True):
                del st.session_state.current_module
                del st.session_state.current_week
                st.rerun()
        
        # STOP HERE - don't show weeks when module is active
        return
    
    # Only show weeks if NO module is selected
    # Display progress overview
    total_xp = db.get_total_xp()
    display_progress_bar(
        len([w for w in TEF_SYLLABUS if db.is_week_unlocked(w["week"])]),
        len(TEF_SYLLABUS),
        "Weeks Unlocked"
    )
    
    # Level filter
    st.subheader("Filter by Level")
    selected_level = st.selectbox(
        "Choose CEFR Level",
        ["All"] + get_all_levels(),
        key="level_filter"
    )
    
    # Display weeks
    st.markdown("---")
    
    for week in TEF_SYLLABUS:
        if selected_level != "All" and week["level"] != selected_level:
            continue
        
        week_num = week["week"]
        is_locked = not db.is_week_unlocked(week_num)
        
        # Display week card with buttons inside
        status_emoji = "🔒" if is_locked else "📖"
        expander_label = f"{status_emoji} Week {week_num}: {week['title']} ({week['level']}) - +{week['xp_value']} XP"
        
        with st.expander(expander_label, expanded=(not is_locked)):
            if is_locked:
                st.warning("🔒 Complete previous weeks to unlock this content")
            else:
                # Show week details
                st.markdown(f"**Level:** {week['level']} | **XP:** +{week['xp_value']}")
                
                # Action buttons RIGHT HERE inside expander
                st.markdown("**Choose an activity:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📖 Grammar Lab", key=f"grammar_{week_num}", use_container_width=True):
                        st.session_state.current_module = "grammar"
                        st.session_state.current_week = week_num
                        st.rerun()
                
                with col2:
                    if st.button("📰 Reading", key=f"reading_{week_num}", use_container_width=True):
                        st.session_state.current_module = "reading"
                        st.session_state.current_week = week_num
                        st.rerun()
                
                with col3:
                    if st.button("✍️ Writing", key=f"writing_{week_num}", use_container_width=True):
                        st.session_state.current_module = "writing"
                        st.session_state.current_week = week_num
                        st.rerun()


def render_grammar_lab(week_data: dict):
    """Grammar Lab: Explanation + Fill-in-the-blank questions."""
    st.subheader(f"📖 Grammar Lab - Week {week_data['week']}")
    st.markdown(f"**Topic:** {week_data['title']}")
    
    if st.button("← Back to Roadmap"):
        del st.session_state.current_module
        del st.session_state.current_week
        st.rerun()
    
    st.markdown("---")
    
    # Topic selection
    topics = week_data["grammar_topics"]
    selected_topic = st.selectbox("Select Grammar Topic", topics, key="grammar_topic")
    
    if st.button("🎯 Generate Lesson", key="gen_grammar"):
        with show_loading_spinner("Generating grammar explanation..."):
            explanation = ollama_handler.generate_grammar_explanation(selected_topic)
            st.session_state.grammar_explanation = explanation
        
        with show_loading_spinner("Creating practice questions..."):
            questions = ollama_handler.generate_fill_in_blank_questions(selected_topic, count=5)
            st.session_state.grammar_questions = questions
            st.session_state.grammar_answers = {}
            st.session_state.grammar_results = {}
            # Create unique session key for this exercise set
            st.session_state.grammar_session_key = f"grammar_{week_data['week']}_{selected_topic}_{hash(str(questions))}"
    
    # Display explanation
    if "grammar_explanation" in st.session_state:
        with st.expander("📚 Topic Explanation", expanded=True):
            st.markdown(st.session_state.grammar_explanation)
    
    # Display questions
    if "grammar_questions" in st.session_state:
        st.subheader("🎯 Practice Exercises")
        
        questions = st.session_state.grammar_questions
        
        for idx, q in enumerate(questions):
            st.markdown(f"**Question {idx + 1}:** {q['question']}")
            
            # Answer input
            answer_key = f"answer_{idx}"
            user_answer = st.text_input(
                "Your answer:",
                key=f"input_{answer_key}",
                disabled=answer_key in st.session_state.grammar_results
            )
            
            col1, col2 = st.columns([1, 3])
            
            # Check button - use database to track completion
            with col1:
                already_answered = answer_key in st.session_state.grammar_results
                
                if not already_answered and user_answer.strip():
                    if st.button("✅ Check Answer", key=f"check_{idx}", use_container_width=True):
                        result = ollama_handler.grade_fill_in_blank(
                            user_answer, q["answer"]
                        )
                        st.session_state.grammar_results[answer_key] = result
                        
                        # Award XP only if this specific question hasn't been completed before
                        if result["correct"]:
                            # Create unique ID for this question: week + topic + question content hash
                            question_id = f"grammar_w{week_data['week']}_{selected_topic}_q{idx}_{hash(q['question'])}"
                            
                            # Check database if already completed
                            if not db.is_question_completed(question_id):
                                db.add_xp(XP_PER_GRAMMAR_QUESTION, f"Grammar: {selected_topic} Q{idx+1}")
                                db.mark_question_completed(question_id, week_data['week'], "grammar")
                        
                        st.rerun()
                elif already_answered:
                    st.caption("Answered ✓")
            
            # Show result
            if answer_key in st.session_state.grammar_results:
                result = st.session_state.grammar_results[answer_key]
                if result["correct"]:
                    st.success(f"✅ Correct! +{XP_PER_GRAMMAR_QUESTION} XP")
                else:
                    st.error(f"❌ Incorrect. Correct answer: **{q['answer']}**")
                    st.info(f"💡 {q['explanation']}")
            
            st.markdown("---")
        
        # Check completion
        if len(st.session_state.grammar_results) == len(questions):
            correct_count = sum(1 for r in st.session_state.grammar_results.values() if r["correct"])
            st.success(f"🎉 Exercise Complete! Score: {correct_count}/{len(questions)}")
            
            # Save progress
            score = int((correct_count / len(questions)) * 100)
            db.save_progress(week_data["week"], "grammar", True, score)
            
            if st.button("🔄 Try Another Topic"):
                for key in ["grammar_explanation", "grammar_questions", "grammar_answers", "grammar_results"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()


def render_reading_lounge(week_data: dict):
    """Reading Lounge: AI-generated article + comprehension questions."""
    st.subheader(f"📰 Reading Lounge - Week {week_data['week']}")
    st.markdown(f"**Level:** {week_data['level']}")
    
    if st.button("← Back to Roadmap"):
        del st.session_state.current_module
        del st.session_state.current_week
        st.rerun()
    
    st.markdown("---")
    
    # Topic selection
    topics = week_data["reading_topics"]
    selected_topic = st.selectbox("Select Reading Topic", topics, key="reading_topic")
    
    if st.button("📰 Generate Article", key="gen_article"):
        with show_loading_spinner("Generating authentic French article..."):
            article = ollama_handler.generate_reading_article(
                selected_topic, 
                difficulty=week_data["level"]
            )
            st.session_state.reading_article = article
        
        with show_loading_spinner("Creating comprehension questions..."):
            questions = ollama_handler.generate_reading_questions(article, count=5)
            st.session_state.reading_questions = questions
            st.session_state.reading_results = {}
    
    # Display article
    if "reading_article" in st.session_state:
        with st.expander("📄 Article", expanded=True):
            st.markdown(st.session_state.reading_article)
    
    # Display questions
    if "reading_questions" in st.session_state:
        st.subheader("❓ Comprehension Questions")
        
        questions = st.session_state.reading_questions
        
        for idx, q in enumerate(questions):
            st.markdown(f"**Question {idx + 1}:** {q['question']}")
            
            answer_key = f"reading_answer_{idx}"
            
            # Radio buttons for MCQ
            selected_option = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"radio_{answer_key}",
                disabled=answer_key in st.session_state.reading_results
            )
            
            if st.button("Check Answer", key=f"check_reading_{idx}",
                        disabled=answer_key in st.session_state.reading_results):
                selected_index = q["options"].index(selected_option)
                is_correct = selected_index == q["correct_index"]
                
                st.session_state.reading_results[answer_key] = {
                    "correct": is_correct,
                    "selected": selected_index,
                    "correct_index": q["correct_index"]
                }
                
                # Award XP if correct
                if is_correct:
                    db.add_xp(XP_PER_READING_QUESTION, f"Reading: {selected_topic}")
                
                st.rerun()
            
            # Show result
            if answer_key in st.session_state.reading_results:
                result = st.session_state.reading_results[answer_key]
                if result["correct"]:
                    st.success(f"✅ Correct! +{XP_PER_READING_QUESTION} XP")
                else:
                    st.error(f"❌ Incorrect. Correct answer: **{q['options'][q['correct_index']]}**")
                    st.info(f"💡 {q['explanation']}")
            
            st.markdown("---")
        
        # Check completion
        if len(st.session_state.reading_results) == len(questions):
            correct_count = sum(1 for r in st.session_state.reading_results.values() if r["correct"])
            st.success(f"🎉 Reading Complete! Score: {correct_count}/{len(questions)}")
            
            # Save progress
            score = int((correct_count / len(questions)) * 100)
            db.save_progress(week_data["week"], "reading", True, score)
            
            if st.button("🔄 Try Another Article"):
                for key in ["reading_article", "reading_questions", "reading_results"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
