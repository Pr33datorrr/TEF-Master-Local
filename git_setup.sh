#!/bin/bash
# Git setup script for TEF Master Local

cd /home/iyash/TEF

echo "Setting up Git repository..."

# Configure Git
git config --global user.name "TEF Developer"
git config --global user.email "tef@example.com"

# Add everything and create initial commit
git add -A
git commit -m "feat: Initial TEF Master Local - Complete LMS Application

Features:
- 30-week TEF curriculum (A1-B2) with XP gamification
- Grammar Lab with AI-generated fill-in-blank exercises
- Reading Lounge with AI articles and comprehension tests
- Writing Clinic with TEF rubric grading (450-point scale)
- Resource Library with 40+ official TEF resources
- Progress tracking database with streak system
- Question completion tracking to prevent duplicate XP
- Mobile-optimized Streamlit UI
- WSL/Linux setup and launch scripts
- Integration with Ollama (Gemma 3:4b) for AI features

Tech Stack: Python, Streamlit, SQLite, Ollama, CUDA optimization"

echo ""
echo "✅ Git repository set up successfully!"
echo ""
echo "Commit history:"
git log --oneline
echo ""
echo "Now create a GitHub repository and run:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/TEF-Master-Local.git"
echo "  git branch -M main"
echo "  git push -u origin main"
