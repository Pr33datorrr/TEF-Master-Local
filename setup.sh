#!/bin/bash
echo "==================================================================="
echo "TEF Master Local - Environment Setup (WSL/Linux)"
echo "Optimized for NVIDIA RTX 4060 (CUDA Support)"
echo "==================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Create virtual environment (recommended)
read -p "Create a virtual environment? (recommended) [y/n]: " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment activated!"
    echo ""
fi

echo "[Step 1/5] Installing PyTorch with CUDA support..."
echo "This may take several minutes..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if [ $? -ne 0 ]; then
    echo "WARNING: PyTorch installation failed. Continuing anyway..."
fi
echo ""

echo "[Step 2/5] Installing core dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi
echo ""

echo "[Step 3/5] Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "ERROR: Ollama is not installed!"
    echo "Install Ollama on WSL:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    echo "After installation, run this script again."
    exit 1
else
    echo "Ollama detected: $(ollama --version)"
fi
echo ""

echo "[Step 4/5] Pulling Gemma 3:4b model from Ollama..."
echo "This will download approximately 2-3 GB. Please be patient..."

# Check if ollama is running, start if needed
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama server in background..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

ollama pull gemma3:4b
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to pull Gemma model"
    echo "Please check your internet connection and try again"
    exit 1
fi
echo "Model downloaded successfully!"
echo ""

echo "[Step 5/5] Optional: Voice Tutor Setup"
echo ""
read -p "Do you want to install Voice Tutor dependencies? (y/n): " install_voice
if [[ $install_voice == "y" || $install_voice == "Y" ]]; then
    echo "Installing Whisper and gTTS..."
    pip install openai-whisper gtts
    
    echo ""
    echo "NOTE: Voice Tutor requires ffmpeg"
    echo "Install with: sudo apt install ffmpeg"
    echo ""
    
    echo "To enable Voice Tutor, set ENABLE_VOICE_TUTOR=True in config.py"
    echo ""
fi

echo ""
echo "==================================================================="
echo "Setup Complete!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Run: ./launch.sh (or 'streamlit run app.py')"
echo "3. Access from:"
echo "   - Desktop: http://localhost:8501"
echo "   - Mobile: http://YOUR_IP:8501"
echo ""
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "NOTE: Remember to activate venv in future sessions:"
    echo "      source venv/bin/activate"
    echo ""
fi
echo "For Voice Tutor: Install ffmpeg and set ENABLE_VOICE_TUTOR=True"
echo ""
