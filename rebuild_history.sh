#!/bin/bash
# Rebuild Git history with logical commits
# This will reset and create separate commits for each major feature

echo "🔄 Rebuilding Git history with feature commits..."
echo ""

# Reset to start fresh (keeping files)
git reset --soft HEAD~1
git reset

echo "Creating logical commit history..."
echo ""

# Commit 1: Project foundation
git add .gitignore README.md requirements.txt
git commit -m "feat: Initial project setup

- Add .gitignore for Python, SQLite, and temporary files
- Add comprehensive README with installation and usage guide
- Add requirements.txt with Streamlit and Ollama dependencies"

# Commit 2: Core infrastructure
git add config.py database.py ollama_handler.py
git commit -m "feat: Add core infrastructure

- config.py: Centralized configuration for Ollama, XP values, and feature flags
- database.py: SQLite handler with progress, XP, streaks, and favorites tracking
- ollama_handler.py: AI integration for content generation and grading"

# Commit 3: Data structures
git add data/__init__.py data/syllabus.py
git commit -m "feat: Add 30-week TEF curriculum data

- 30 weeks of structured content from A1 to B2
- Grammar topics, reading themes, writing tasks per week
- XP rewards and level progression system"

# Commit 4: Resources
git add data/resources.py data/writing_prompts.py
git commit -m "feat: Add official TEF resources and writing prompts

- 40+ curated free TEF resources (Lawless French, TV5Monde, RFI)
- Metadata-rich writing prompts for Section A (Fait Divers) and B (Letters)
- Grammar focus, key vocabulary, and structure hints"

# Commit 5: UI Components
git add components/__init__.py components/progress_bar.py
git commit -m "feat: Add reusable UI components

- Progress bars for week completion tracking
- XP cards and streak displays
- Mobile-optimized week card component with expanders"

# Commit 6: Study Roadmap module
git add modules/__init__.py modules/roadmap.py
git commit -m "feat: Add Study Roadmap with Grammar Lab and Reading Lounge

- Interactive 30-week curriculum display
- Grammar Lab: AI-generated explanations and fill-in-blank exercises
- Reading Lounge: AI-generated articles with comprehension questions
- Module selection and navigation system"

# Commit 7: Writing Clinic
git add modules/writing_clinic.py
git commit -m "feat: Add Writing Clinic with AI grading

- Real TEF Section A/B prompts with metadata
- AI grading using official TEF rubric (450-point scale)
- Structure, Vocabulary, and Grammar feedback
- Random prompt generator for practice"

# Commit 8: Resource Library and Voice Tutor
git add modules/resources.py modules/voice_tutor.py
git commit -m "feat: Add Resource Library and optional Voice Tutor

- Resource Library: Search, category filtering, and favorites system
- Voice Tutor: Whisper STT and gTTS for pronunciation practice
- Extensibility guide for adding custom resources"

# Commit 9: Main application
git add app.py
git commit -m "feat: Add main Streamlit application

- Horizontal navigation with streamlit-option-menu
- Mobile-optimized CSS for responsive design
- Sidebar with progress tracking (XP, streaks, level)
- Integration of all feature modules"

# Commit 10: Setup scripts
git add setup.sh launch.sh setup_env.bat launch.bat
git commit -m "feat: Add setup and launch scripts

- setup.sh: WSL/Linux environment setup with PyTorch CUDA and Ollama
- launch.sh: App launcher with Windows IP detection for mobile access
- Windows batch file equivalents for Windows users"

# Commit 11: Bug fixes and improvements
git add -A
git commit -m "fix: Week unlock logic and UI interactivity

- First 3 weeks now unlocked by default for new users
- Progressive unlock based on completing modules
- Buttons moved inside expanders for better click handling
- Removed loading popup for cleaner UX" --allow-empty

# Commit 12: Duplicate XP prevention
git add database.py modules/roadmap.py
git commit -m "fix: Prevent duplicate XP awards

- Add completed_questions table to track answered questions
- Questions identified by unique hash of week + topic + content
- Database persistence prevents XP duplication across refreshes
- Single-click button reliability improvements" --allow-empty

echo ""
echo "✅ Git history rebuilt with 12 logical commits!"
echo ""
echo "Commit history:"
git log --oneline --decorate
echo ""
echo "To update GitHub (force push):"
echo "  git push -f origin main"
echo ""
echo "⚠️  Note: This will rewrite GitHub history. Only do this if you're the only contributor."
