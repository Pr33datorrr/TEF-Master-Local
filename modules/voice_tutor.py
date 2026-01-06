"""
TEF Master Local - Voice Tutor Module (Optional)
Speaking practice with STT and TTS.
"""

import streamlit as st
from config import ENABLE_VOICE_TUTOR

# Only import if feature is enabled
if ENABLE_VOICE_TUTOR:
    try:
        import whisper
        from gtts import gTTS
        import tempfile
        import os
        from ai_handler import ai_handler
        from database import db
        from config import XP_PER_VOICE_PRACTICE
        DEPENDENCIES_AVAILABLE = True
    except ImportError:
        DEPENDENCIES_AVAILABLE = False
else:
    DEPENDENCIES_AVAILABLE = False


def render_voice_tutor():
    """Main Voice Tutor interface."""
    
    if not ENABLE_VOICE_TUTOR:
        st.header("🎙️ Voice Tutor (Beta)")
        st.warning("""
        **Voice Tutor is currently disabled.**
        
        To enable this feature:
        1. Install dependencies: `pip install openai-whisper gtts`
        2. Install ffmpeg from https://ffmpeg.org
        3. Set `ENABLE_VOICE_TUTOR = True` in `config.py`
        """)
        return
    
    if not DEPENDENCIES_AVAILABLE:
        st.error("""
        **Missing dependencies!**
        
        Please install:
        - `pip install openai-whisper gtts`
        - ffmpeg from https://ffmpeg.org
        """)
        return
    
    st.header("🎙️ Voice Tutor - Speaking Practice")
    st.markdown("Practice your oral French with AI feedback!")
    
    # Mode selection
    st.subheader("Quick Fire Mode")
    st.markdown("AI asks a question → You respond → Get pronunciation feedback")
    
    # Difficulty selection
    difficulty = st.select_slider(
        "Select difficulty",
        options=["A1", "A2", "B1", "B2"],
        value="B1"
    )
    
    if st.button("🎲 Generate Question"):
        with st.spinner("Generating speaking question..."):
            question = ai_handler.generate_speaking_question(difficulty)
            st.session_state.voice_question = question
            
            # Generate TTS
            tts = gTTS(text=question, lang='fr')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                st.session_state.voice_audio_path = fp.name
    
    # Display question
    if "voice_question" in st.session_state:
        st.markdown("### 🗣️ Your Question:")
        st.info(st.session_state.voice_question)
        
        # Play audio
        if "voice_audio_path" in st.session_state:
            with open(st.session_state.voice_audio_path, 'rb') as audio_file:
                st.audio(audio_file.read(), format='audio/mp3')
        
        # Recording
        st.markdown("### 🎤 Your Response")
        st.markdown("*Note: Browser-based audio recording coming soon. For now, use an external recorder.*")
        
        uploaded_audio = st.file_uploader(
            "Upload your recorded response (MP3/WAV)",
            type=['mp3', 'wav', 'm4a'],
            key="audio_upload"
        )
        
        if uploaded_audio and st.button("📊 Evaluate My Pronunciation"):
            with st.spinner("Transcribing your response..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    fp.write(uploaded_audio.read())
                    temp_path = fp.name
                
                try:
                    # Load Whisper model
                    model = whisper.load_model("base")
                    result = model.transcribe(temp_path, language='fr')
                    transcription = result["text"]
                    
                    # Evaluate
                    evaluation = ai_handler.evaluate_pronunciation(
                        transcription,
                        st.session_state.voice_question
                    )
                    
                    st.success("✅ Transcription Complete!")
                    st.markdown(f"**You said:** {transcription}")
                    st.markdown(f"**Feedback:** {evaluation['feedback']}")
                    
                    # Award XP
                    db.add_xp(XP_PER_VOICE_PRACTICE, "Voice Practice")
                    st.success(f"+{XP_PER_VOICE_PRACTICE} XP earned!")
                    
                finally:
                    # Clean up
                    os.unlink(temp_path)
        
        if st.button("🔄 New Question"):
            for key in ["voice_question", "voice_audio_path"]:
                if key in st.session_state:
                    # Clean up audio file
                    if key == "voice_audio_path":
                        try:
                            os.unlink(st.session_state[key])
                        except:
                            pass
                    del st.session_state[key]
            st.rerun()
