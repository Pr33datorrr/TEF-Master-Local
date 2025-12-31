"""
TEF Master Local - Database Module
SQLite database operations for progress tracking, XP, streaks, and favorites.
"""

import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from config import DB_PATH


class Database:
    """Handles all database operations for TEF Master Local."""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a database connection."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with required tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Progress tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                week_number INTEGER NOT NULL,
                module_type TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                score INTEGER,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # XP history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS xp_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                xp_gained INTEGER NOT NULL,
                activity TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Streaks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_activity_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Favorites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                resource_id TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Completed questions tracker (to prevent duplicate XP)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completed_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                question_id TEXT NOT NULL UNIQUE,
                week_number INTEGER,
                module_type TEXT,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Create default user if not exists
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (1, 'default')")
        cursor.execute("INSERT OR IGNORE INTO streaks (user_id, current_streak, best_streak) VALUES (1, 0, 0)")
        
        conn.commit()
        conn.close()
    
    # ==================== Progress Tracking ====================
    
    def save_progress(self, week_number: int, module_type: str, completed: bool = True, 
                     score: Optional[int] = None, user_id: int = 1):
        """Save or update progress for a specific module."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO progress (user_id, week_number, module_type, completed, score, completed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, week_number, module_type, completed, score, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_week_progress(self, week_number: int, user_id: int = 1) -> Dict[str, Any]:
        """Get progress for a specific week."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT module_type, completed, score
            FROM progress
            WHERE user_id = ? AND week_number = ?
        """, (user_id, week_number))
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            'grammar': any(r[0] == 'grammar' and r[1] for r in results),
            'reading': any(r[0] == 'reading' and r[1] for r in results),
            'writing': any(r[0] == 'writing' and r[1] for r in results),
            'total_completed': sum(1 for r in results if r[1])
        }
    
    def is_week_unlocked(self, week_number: int, user_id: int = 1) -> bool:
        """Check if a week is unlocked based on previous week completion."""
        # First 3 weeks are always unlocked for new users
        if week_number <= 3:
            return True
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if user has completed at least one module for each previous week
        # More flexible unlock: just need SOME activity in previous weeks
        cursor.execute("""
            SELECT COUNT(DISTINCT week_number) 
            FROM progress 
            WHERE user_id = ? AND week_number < ? AND completed = 1
        """, (user_id, week_number))
        
        weeks_with_progress = cursor.fetchone()[0]
        conn.close()
        
        # Unlock if user has completed at least 1 module per previous week
        # Example: Week 5 requires progress in at least 2 previous weeks (50% of 4)
        required_weeks = max(1, (week_number - 3) // 2)  # More lenient
        return weeks_with_progress >= required_weeks
    
    # ==================== XP Management ====================
    
    def add_xp(self, xp_amount: int, activity: str, user_id: int = 1):
        """Add XP for an activity."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO xp_history (user_id, xp_gained, activity)
            VALUES (?, ?, ?)
        """, (user_id, xp_amount, activity))
        
        conn.commit()
        conn.close()
        
        # Update streak
        self.update_streak(user_id)
    
    def get_total_xp(self, user_id: int = 1) -> int:
        """Get total XP for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(xp_gained), 0)
            FROM xp_history
            WHERE user_id = ?
        """, (user_id,))
        
        total_xp = cursor.fetchone()[0]
        conn.close()
        
        return total_xp
    
    def get_daily_xp(self, user_id: int = 1) -> int:
        """Get XP earned today."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = date.today()
        cursor.execute("""
            SELECT COALESCE(SUM(xp_gained), 0)
            FROM xp_history
            WHERE user_id = ? AND DATE(earned_at) = ?
        """, (user_id, today))
        
        daily_xp = cursor.fetchone()[0]
        conn.close()
        
        return daily_xp
    
    # ==================== Streak Management ====================
    
    def update_streak(self, user_id: int = 1):
        """Update streak based on activity."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current streak info
        cursor.execute("""
            SELECT current_streak, best_streak, last_activity_date
            FROM streaks
            WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        if not result:
            return
        
        current_streak, best_streak, last_date = result
        today = date.today()
        
        # Convert last_date string to date object
        if last_date:
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
            days_diff = (today - last_date).days
        else:
            days_diff = 0
        
        # Update streak logic
        if days_diff == 0:
            # Same day, no change
            pass
        elif days_diff == 1:
            # Consecutive day
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            # Streak broken
            current_streak = 1
        
        cursor.execute("""
            UPDATE streaks
            SET current_streak = ?, best_streak = ?, last_activity_date = ?
            WHERE user_id = ?
        """, (current_streak, best_streak, today, user_id))
        
        conn.commit()
        conn.close()
    
    def get_streak(self, user_id: int = 1) -> Dict[str, int]:
        """Get current and best streak."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT current_streak, best_streak
            FROM streaks
            WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'current': result[0], 'best': result[1]}
        return {'current': 0, 'best': 0}
    
    # ==================== Favorites ====================
    
    def add_favorite(self, resource_id: str, user_id: int = 1):
        """Add a resource to favorites."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO favorites (user_id, resource_id)
            VALUES (?, ?)
        """, (user_id, resource_id))
        
        conn.commit()
        conn.close()
    
    def remove_favorite(self, resource_id: str, user_id: int = 1):
        """Remove a resource from favorites."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM favorites
            WHERE user_id = ? AND resource_id = ?
        """, (user_id, resource_id))
        
        conn.commit()
        conn.close()
    
    def get_favorites(self, user_id: int = 1) -> List[str]:
        """Get all favorite resource IDs."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT resource_id
            FROM favorites
            WHERE user_id = ?
        """, (user_id,))
        
        favorites = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return favorites
    
    def is_favorite(self, resource_id: str, user_id: int = 1) -> bool:
        """Check if a resource is favorited."""
        return resource_id in self.get_favorites(user_id)
    
    # ==================== Question Tracking (Prevent Duplicate XP) ====================
    
    def is_question_completed(self, question_id: str, user_id: int = 1) -> bool:
        """Check if a question has been completed before."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM completed_questions
            WHERE user_id = ? AND question_id = ?
        """, (user_id, question_id))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def mark_question_completed(self, question_id: str, week_number: int, 
                               module_type: str, user_id: int = 1):
        """Mark a question as completed."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO completed_questions 
            (user_id, question_id, week_number, module_type)
            VALUES (?, ?, ?, ?)
        """, (user_id, question_id, week_number, module_type))
        
        conn.commit()
        conn.close()


# Global database instance
db = Database()
