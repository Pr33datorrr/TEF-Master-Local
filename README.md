# 🇫🇷 TEF Master Cloud

![TEF Master Cloud Banner](assets/hero_banner.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tef-master.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**TEF Master Cloud** is an AI-powered study companion designed to help you achieve **CLB 7+** in the *Test d'Évaluation de Français* (TEF) Canada exam.

It features a unique **Hybrid AI Architecture** that runs for free on your laptop (Local AI) and seamlessy switches to the Cloud for mobile access.

## ✨ Key Features

### 🧠 Hybrid AI Core
*   **Local Power**: Runs on `Gemma 3 (27b)` locally via Ollama for zero-latency, private, and free tutoring.
*   **Cloud Freedom**: Automatically switches to `Google Gemini (Flash)` when deployed or on mobile.
*   **Internet Powered**: The AI Tutor can search the web to answer questions about current events, culture, or specific grammar rules.

### 📚 Interactive Modules
*   **Grammar Lab**: AI generates infinite practice exercises tailored to your weak points.
*   **Writing Clinic**: Submit essays and get instant feedback scored against official TEF rubrics.
*   **AI Tutor**: A chat interface that acts as your personal French research assistant.
*   **Listening & Reading**: Structured lessons to improve comprehension.

### 📱 Mobile Ready
Fully responsive design optimized for study on the go.

## 📸 Screenshots

### AI Tutor in Action
![AI Tutor Interface](assets/ai_tutor_demo.png)

## 🚀 Getting Started

### Cloud Access
Simply visit: **[https://tef-master.streamlit.app](https://tef-master.streamlit.app)**

### Local Installation
1.  **Clone the repo**:
    ```bash
    git clone https://github.com/Pr33datorrr/TEF-Master-Local.git
    cd TEF-Master-Local
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run with Streamlit**:
    ```bash
    streamlit run app.py
    ```

## 🛠️ Configuration
*   **Gemini API**: Set `GEMINI_API_KEY` in `.streamlit/secrets.toml`.
*   **Ollama**: Install [Ollama](https://ollama.com) and pull `gemma3`.

---
*Built with ❤️ using Streamlit, Google Gemini, and Python.*
