@echo off
echo ===================================================================
echo TEF Master Local - Environment Setup
echo Optimized for NVIDIA RTX 4060 (CUDA Support)
echo ===================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo [Step 1/5] Installing PyTorch with CUDA support...
echo This may take several minutes...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if errorlevel 1 (
    echo WARNING: PyTorch installation failed. Continuing anyway...
)
echo.

echo [Step 2/5] Installing core dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)
echo.

echo [Step 3/5] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Ollama is not installed!
    echo Please install Ollama from: https://ollama.ai
    echo After installation, run this script again.
    pause
    exit /b 1
) else (
    echo Ollama detected successfully!
)
echo.

echo [Step 4/5] Pulling Gemma 3:4b model from Ollama...
echo This will download approximately 2-3 GB. Please be patient...
ollama pull gemma3:4b
if errorlevel 1 (
    echo ERROR: Failed to pull Gemma model
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo Model downloaded successfully!
echo.

echo [Step 5/5] Optional: Voice Tutor Setup
echo.
set /p INSTALL_VOICE="Do you want to install Voice Tutor dependencies? (y/n): "
if /i "%INSTALL_VOICE%"=="y" (
    echo Installing Whisper and gTTS...
    pip install openai-whisper gtts
    
    echo.
    echo NOTE: Voice Tutor requires ffmpeg
    echo Download from: https://ffmpeg.org/download.html
    echo After installing ffmpeg, add it to your system PATH
    echo.
    
    echo To enable Voice Tutor, set ENABLE_VOICE_TUTOR=True in config.py
    echo.
)

echo.
echo ===================================================================
echo Setup Complete! 
echo ===================================================================
echo.
echo Next steps:
echo 1. Ensure Ollama is running (it should start automatically)
echo 2. Run: launch.bat (or 'streamlit run app.py')
echo 3. Access from mobile: http://YOUR_IP:8501
echo.
echo For Voice Tutor: Install ffmpeg and set ENABLE_VOICE_TUTOR=True
echo.
pause
