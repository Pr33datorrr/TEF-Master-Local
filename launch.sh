#!/bin/bash
echo "==================================================================="
echo "TEF Master Local - Network Configuration Helper"
echo "==================================================================="
echo ""

# Get Windows host IP (for mobile access)
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')

echo "📱 Mobile Access Setup:"
echo "-------------------------------------------------------------------"
echo "Your Windows IP: $WINDOWS_IP"
echo ""
echo "On your mobile device, open:"
echo "  http://$WINDOWS_IP:8501"
echo ""
echo "If connection fails, run these commands in Windows PowerShell (as Admin):"
echo "  netsh advfirewall firewall add rule name=\"Streamlit\" dir=in action=allow protocol=TCP localport=8501"
echo "-------------------------------------------------------------------"
echo ""

# Start the app
echo "Starting TEF Master Local..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

streamlit run app.py --server.address=0.0.0.0 --server.port=8501
