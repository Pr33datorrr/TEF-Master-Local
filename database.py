"""
TEF Master Cloud - Database Module
Firestore database operations for progress tracking, XP, streaks, and favorites.
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import google.auth

# Only initialize app once
if not firebase_admin._apps:
    try:
        # 1. Try Streamlit Secrets (for Cloud Deployment)
        if "firebase" in st.secrets:
            # Create a dict from secrets that looks like service account JSON
            cred = credentials.Certificate(dict(st.secrets["firebase"]))
            firebase_admin.initialize_app(cred)
        
        # 2. Try Google Application Default Credentials (for Local Dev with gcloud)
        else:
            # This requires 'gcloud auth application-default login' to have been run locally
            # or running in a GCP environment
            cred, project_id = google.auth.default()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
            })
            
    except Exception as e:
        print(f"Warning: Firebase Auth failed. Some features may not work. Error: {e}")
        # Fallback for when we might be rebuilding during build process without secrets
        pass

def get_db():
    """Get Firestore client."""
    try:
        return firestore.client()
    except Exception:
        return None

class Database:
    """Handles all database operations using Firestore."""
    
    def __init__(self):
        self.db = get_db()
        # Fixed user ID for single-user mode (can be expanded later)
        self.user_id = "default_user_v1"
    
    def _get_user_ref(self):
        if not self.db: return None
        return self.db.collection('users').document(self.user_id)
        
    def init_database(self):
        """
        Initialize database. 
        In Firestore, explicit table creation is not needed.
        But we ensure the user document exists.
        """
        if not self.db: return

        user_ref = self._get_user_ref()
        doc = user_ref.get()
        if not doc.exists:
            user_ref.set({
                'username': 'default',
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            # Init streak
            self.db.collection('streaks').document(self.user_id).set({
                'current_streak': 0,
                'best_streak': 0,
                'last_activity_date': None
            })

    # ==================== Progress Tracking ====================
    
    def save_progress(self, week_number: int, module_type: str, completed: bool = True, 
                     score: Optional[int] = None, user_id: str = None):
        """Save or update progress."""
        if not self.db: return
        uid = user_id or self.user_id
        
        # We store progress as individual documents in a subcollection or root collection
        # Let's use a subcollection 'progress' under the user
        
        progress_data = {
            'week_number': week_number,
            'module_type': module_type,
            'completed': completed,
            'score': score,
            'completed_at': firestore.SERVER_TIMESTAMP
        }
        
        # Use a composite ID to easily update/overwrite specific module progress
        doc_id = f"week_{week_number}_{module_type}"
        
        self.db.collection('users').document(uid).collection('progress').document(doc_id).set(
            progress_data
        )
    
    def get_week_progress(self, week_number: int, user_id: str = None) -> Dict[str, Any]:
        """Get progress for a specific week."""
        if not self.db: return {'grammar': False, 'reading': False, 'writing': False, 'total_completed': 0}
        uid = user_id or self.user_id
        
        docs = self.db.collection('users').document(uid).collection('progress')\
            .where('week_number', '==', week_number).stream()
            
        results = [doc.to_dict() for doc in docs]
        
        return {
            'grammar': any(r.get('module_type') == 'grammar' and r.get('completed') for r in results),
            'reading': any(r.get('module_type') == 'reading' and r.get('completed') for r in results),
            'writing': any(r.get('module_type') == 'writing' and r.get('completed') for r in results),
            'total_completed': sum(1 for r in results if r.get('completed'))
        }
    
    def is_week_unlocked(self, week_number: int, user_id: str = None) -> bool:
        """Check if a week is unlocked."""
        if week_number <= 3:
            return True
        
        if not self.db: return False
        uid = user_id or self.user_id
        
        # Count weeks with at least one completed module
        # Firestore counting can be expensive, but acceptable for this scale
        
        # Get all progress items for previous weeks
        # Note: In a large app, we would cache this "unlocked_level" on the user doc
        docs = self.db.collection('users').document(uid).collection('progress')\
            .where('week_number', '<', week_number)\
            .where('completed', '==', True)\
            .stream()
            
        unique_weeks = set()
        for doc in docs:
            unique_weeks.add(doc.to_dict().get('week_number'))
            
        weeks_with_progress = len(unique_weeks)
        required_weeks = max(1, (week_number - 3) // 2)
        
        return weeks_with_progress >= required_weeks
    
    # ==================== XP Management ====================
    
    def add_xp(self, xp_amount: int, activity: str, user_id: str = None):
        """Add XP."""
        if not self.db: return
        uid = user_id or self.user_id
        
        self.db.collection('users').document(uid).collection('xp_history').add({
            'xp_gained': xp_amount,
            'activity': activity,
            'earned_at': firestore.SERVER_TIMESTAMP
        })
        
        self.update_streak(uid)
    
    def get_total_xp(self, user_id: str = None) -> int:
        """Get total XP."""
        if not self.db: return 0
        uid = user_id or self.user_id
        
        # Ideally, use an aggregation query or maintain a counter
        # For now, simple client-side sum (watch read costs if history grows huge)
        # Optimization: We should probably store a running total in user doc
        
        docs = self.db.collection('users').document(uid).collection('xp_history').stream()
        return sum(doc.to_dict().get('xp_gained', 0) for doc in docs)
    
    def get_daily_xp(self, user_id: str = None) -> int:
        """Get XP earned today."""
        if not self.db: return 0
        uid = user_id or self.user_id
        
        today_start = datetime.combine(date.today(), datetime.min.time())
        
        docs = self.db.collection('users').document(uid).collection('xp_history')\
            .where('earned_at', '>=', today_start).stream()
            
        return sum(doc.to_dict().get('xp_gained', 0) for doc in docs)
    
    # ==================== Streak Management ====================
    
    def update_streak(self, user_id: str = None):
        """Update streak."""
        if not self.db: return
        uid = user_id or self.user_id
        
        streak_ref = self.db.collection('streaks').document(uid)
        doc = streak_ref.get()
        
        if not doc.exists:
            self.init_database()
            doc = streak_ref.get()
            
        data = doc.to_dict()
        current_streak = data.get('current_streak', 0)
        best_streak = data.get('best_streak', 0)
        last_date_str = data.get('last_activity_date') # Stored as string YYYY-MM-DD usually for simple compare
        
        today_str = date.today().isoformat()
        
        if last_date_str == today_str:
            return # Already active today
            
        if last_date_str:
            last_date = date.fromisoformat(last_date_str)
            days_diff = (date.today() - last_date).days
            
            if days_diff == 1:
                current_streak += 1
            elif days_diff > 1:
                current_streak = 1
        else:
            current_streak = 1
            
        best_streak = max(best_streak, current_streak)
        
        streak_ref.update({
            'current_streak': current_streak,
            'best_streak': best_streak,
            'last_activity_date': today_str
        })
    
    def get_streak(self, user_id: str = None) -> Dict[str, int]:
        """Get streak info."""
        if not self.db: return {'current': 0, 'best': 0}
        uid = user_id or self.user_id
        
        doc = self.db.collection('streaks').document(uid).get()
        if doc.exists:
            data = doc.to_dict()
            return {'current': data.get('current_streak', 0), 'best': data.get('best_streak', 0)}
        return {'current': 0, 'best': 0}

    # ==================== Favorites ====================
    
    def add_favorite(self, resource_id: str, user_id: str = None):
        """Add favorite."""
        if not self.db: return
        uid = user_id or self.user_id
        
        self.db.collection('users').document(uid).collection('favorites').document(resource_id).set({
            'resource_id': resource_id,
            'added_at': firestore.SERVER_TIMESTAMP
        })
    
    def remove_favorite(self, resource_id: str, user_id: str = None):
        """Remove favorite."""
        if not self.db: return
        uid = user_id or self.user_id
        
        self.db.collection('users').document(uid).collection('favorites').document(resource_id).delete()
    
    def get_favorites(self, user_id: str = None) -> List[str]:
        """Get favorites."""
        if not self.db: return []
        uid = user_id or self.user_id
        
        docs = self.db.collection('users').document(uid).collection('favorites').stream()
        return [doc.id for doc in docs]
    
    def is_favorite(self, resource_id: str, user_id: str = None) -> bool:
        return resource_id in self.get_favorites(user_id)

    # ==================== Question Tracking ====================

    def is_question_completed(self, question_id: str, user_id: str = None) -> bool:
        if not self.db: return False
        uid = user_id or self.user_id
        
        # Use a deterministic ID for the doc to quick check existence
        doc_id = f"{uid}_{question_id}"
        doc = self.db.collection('completed_questions').document(doc_id).get()
        return doc.exists
        
    def mark_question_completed(self, question_id: str, week_number: int, 
                               module_type: str, user_id: str = None):
        if not self.db: return
        uid = user_id or self.user_id
        
        doc_id = f"{uid}_{question_id}"
        self.db.collection('completed_questions').document(doc_id).set({
            'user_id': uid,
            'question_id': question_id,
            'week_number': week_number,
            'module_type': module_type,
            'completed_at': firestore.SERVER_TIMESTAMP
        })

# Global database instance
db = Database()
