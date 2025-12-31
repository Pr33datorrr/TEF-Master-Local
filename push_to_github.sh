#!/bin/bash
# Quick Git setup and push to GitHub
# Run this from WSL terminal: bash push_to_github.sh

echo "🚀 Setting up Git and pushing to GitHub..."
echo ""

# Initialize git
git init
echo "✅ Git initialized"

# Configure git (if not already configured globally)
git config user.name "Pr33datorrr" 2>/dev/null || git config --global user.name "Pr33datorrr"
git config user.email "dev@tef.local" 2>/dev/null || git config --global user.email "dev@tef.local"
echo "✅ Git configured"

# Add all files
git add -A
echo "✅ Files staged"

# Create initial commit
git commit -m "feat: TEF Master Local - Complete LMS Application

Full-featured locally hosted LMS for TEF exam preparation with:
- 30-week curriculum (A1-B2) with XP gamification
- AI-powered Grammar Lab, Reading Lounge, Writing Clinic
- 40+ official TEF resources
- Progress tracking with duplicate XP prevention
- Mobile-optimized UI
- Ollama integration (Gemma 3:4b)"

echo "✅ Initial commit created"

# Add GitHub remote
git remote add origin https://github.com/Pr33datorrr/TEF-Master-Local.git
echo "✅ Remote added"

# Rename branch to main
git branch -M main
echo "✅ Branch renamed to main"

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ DONE! Your code is now on GitHub:"
echo "   https://github.com/Pr33datorrr/TEF-Master-Local"
