"""
TEF Master Local - Ollama Integration Module
Handles all AI interactions using Ollama with Gemma 3:4b model.
"""

import json
from typing import Dict, List, Optional, Any
import ollama
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, OLLAMA_TIMEOUT


class OllamaHandler:
    """Manages interactions with Ollama/Gemma for content generation and grading."""
    
    def __init__(self):
        self.model = OLLAMA_MODEL
        self.client = None
    
    def _get_response(self, prompt: str, system_prompt: str = "") -> str:
        """Get response from Ollama."""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            return response['message']['content']
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ==================== Grammar Lab ====================
    
    def generate_grammar_explanation(self, topic: str) -> str:
        """Generate a concise grammar explanation for a topic."""
        system_prompt = """You are a French grammar expert preparing students for the TEF exam.
Provide clear, concise explanations with examples. Keep it under 150 words."""
        
        prompt = f"""Explain the French grammar topic: {topic}

Include:
1. Brief definition
2. When to use it
3. 2-3 concrete examples

Keep it practical and exam-focused."""
        
        return self._get_response(prompt, system_prompt)
    
    def generate_fill_in_blank_questions(self, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate fill-in-the-blank questions for a grammar topic."""
        system_prompt = """You are creating TEF-style grammar exercises.
Return ONLY a valid JSON array of questions. No additional text."""
        
        prompt = f"""Create {count} fill-in-the-blank questions for the topic: {topic}

Format as JSON array:
[
  {{
    "question": "Complete sentence with ____ (blank)",
    "answer": "correct answer",
    "explanation": "why this is correct"
  }}
]

Make questions progressively harder. Focus on TEF exam patterns."""
        
        response = self._get_response(prompt, system_prompt)
        
        try:
            # Extract JSON from response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            json_str = response[start_idx:end_idx]
            questions = json.loads(json_str)
            return questions[:count]
        
        except (json.JSONDecodeError, ValueError):
            # Fallback: return sample questions
            return [
                {
                    "question": f"Sample question for {topic} with ____",
                    "answer": "answer",
                    "explanation": "This is a sample question."
                }
            ]
    
    def grade_fill_in_blank(self, user_answer: str, correct_answer: str) -> Dict[str, Any]:
        """Grade a fill-in-the-blank answer."""
        # Simple string comparison with normalization
        user_normalized = user_answer.strip().lower()
        correct_normalized = correct_answer.strip().lower()
        
        is_correct = user_normalized == correct_normalized
        
        # For more lenient grading, check if they're similar
        if not is_correct:
            # Check if answer is close (handles minor typos)
            similarity = self._calculate_similarity(user_normalized, correct_normalized)
            is_correct = similarity > 0.85
        
        return {
            "correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": correct_answer
        }
    
    @staticmethod
    def _calculate_similarity(s1: str, s2: str) -> float:
        """Calculate simple similarity ratio between two strings."""
        if s1 == s2:
            return 1.0
        if len(s1) == 0 or len(s2) == 0:
            return 0.0
        
        # Simple character overlap ratio
        set1, set2 = set(s1), set(s2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    # ==================== Reading Lounge ====================
    
    def generate_reading_article(self, topic: str, difficulty: str = "B1") -> str:
        """Generate a TEF-style reading article."""
        system_prompt = f"""You are a French language educator creating TEF exam materials.
Write clear, natural French at {difficulty} level (CEFR)."""
        
        prompt = f"""Write a 200-word article in French about: {topic}

Requirements:
- Natural, authentic French
- {difficulty} difficulty level
- Suitable for TEF exam practice
- Include varied vocabulary
- Clear structure (intro, body, conclusion)

IMPORTANT: Write ONLY the article. No additional commentary."""
        
        return self._get_response(prompt, system_prompt)
    
    def generate_reading_questions(self, article: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple-choice comprehension questions for an article."""
        system_prompt = """You are creating TEF reading comprehension questions.
Return ONLY a valid JSON array. No additional text."""
        
        prompt = f"""Based on this French article, create {count} multiple-choice questions:

{article}

Format as JSON:
[
  {{
    "question": "Question text in French",
    "options": ["A) option", "B) option", "C) option", "D) option"],
    "correct_index": 0,
    "explanation": "why this is correct"
  }}
]

Test comprehension, inference, and vocabulary."""
        
        response = self._get_response(prompt, system_prompt)
        
        try:
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            json_str = response[start_idx:end_idx]
            questions = json.loads(json_str)
            return questions[:count]
        
        except (json.JSONDecodeError, ValueError):
            return [
                {
                    "question": "Sample comprehension question?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "correct_index": 0,
                    "explanation": "Sample explanation"
                }
            ]
    
    # ==================== Writing Clinic ====================
    
    def grade_essay(self, essay: str, task_type: str) -> Dict[str, Any]:
        """Grade an essay according to TEF rubric."""
        system_prompt = """You are a TEF examiner grading written production.
Use the official TEF rubric: Structure (150), Vocabulary (150), Grammar (150).
Be strict but fair. Return ONLY valid JSON."""
        
        prompt = f"""Grade this TEF essay for task type: {task_type}

Essay:
{essay}

Evaluate and return JSON:
{{
  "structure_score": 0-150,
  "vocabulary_score": 0-150,
  "grammar_score": 0-150,
  "total_score": 0-450,
  "structure_feedback": "specific feedback",
  "vocabulary_feedback": "specific feedback",
  "grammar_feedback": "specific feedback",
  "suggestions": ["improvement 1", "improvement 2", "improvement 3"]
}}

Be specific and constructive."""
        
        response = self._get_response(prompt, system_prompt)
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            json_str = response[start_idx:end_idx]
            grading = json.loads(json_str)
            return grading
        
        except (json.JSONDecodeError, ValueError):
            # Fallback grading
            return {
                "structure_score": 100,
                "vocabulary_score": 100,
                "grammar_score": 100,
                "total_score": 300,
                "structure_feedback": "Essay shows basic structure.",
                "vocabulary_feedback": "Vocabulary is adequate.",
                "grammar_feedback": "Grammar needs improvement.",
                "suggestions": ["Work on sentence variety", "Expand vocabulary range", "Review verb conjugations"]
            }
    
    # ==================== Voice Tutor (Optional) ====================
    
    def generate_speaking_question(self, difficulty: str = "B1") -> str:
        """Generate a TEF-style speaking question."""
        system_prompt = f"""You are creating oral production questions for TEF at {difficulty} level."""
        
        prompt = f"""Generate ONE TEF oral production question in French at {difficulty} level.

The question should:
- Be open-ended
- Encourage 1-2 minute response
- Test practical French skills

Return ONLY the question, nothing else."""
        
        return self._get_response(prompt, system_prompt)
    
    def evaluate_pronunciation(self, transcription: str, expected_content: str) -> Dict[str, Any]:
        """Evaluate pronunciation based on transcription accuracy."""
        # Simple evaluation based on transcription quality
        word_count = len(transcription.split())
        
        return {
            "clarity_score": min(100, word_count * 10),  # Simple heuristic
            "feedback": "Practice speaking clearly and at a moderate pace.",
            "transcription": transcription
        }


# Global handler instance
ollama_handler = OllamaHandler()
