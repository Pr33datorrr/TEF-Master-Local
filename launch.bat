@echo off
echo ===================================================================
echo Starting TEF Master Local
echo ===================================================================
echo.
echo 📚 Launching on http://localhost:8501
echo 📱 Mobile access: http://YOUR_LOCAL_IP:8501
echo.
echo To find your local IP:
echo - Windows: Run 'ipconfig' and look for IPv4 Address
echo - The app will be accessible from any device on your network
echo.
echo Press Ctrl+C to stop the server
echo ===================================================================
echo.

streamlit run app.py --server.address=0.0.0.0 --server.port=8501
