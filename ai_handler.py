"""
TEF Master Cloud - Hybrid AI Integration Module
Handles AI interactions with fallback logic (Local -> Cloud) and Internet Search.
"""

import json
import os
import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from google import genai
import ollama
from ddgs import DDGS
from config import GEMINI_CONFIG, OLLAMA_CONFIG, AI_PROVIDER, SEARCH_ENABLED

class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system_prompt: str = "") -> str:
        pass

class OllamaProvider(AIProvider):
    """Local AI Provider using Ollama."""
    
    def __init__(self):
        self._name = f"Local ({OLLAMA_CONFIG['model']})"
        self.client = ollama.Client(host=OLLAMA_CONFIG['base_url'])
        self.model = OLLAMA_CONFIG['model']
        self._available = False
        self._check_availability()
    
    def _check_availability(self):
        try:
            # Quick list call to check connection
            self.client.list()
            self._available = True
        except:
            self._available = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_available(self) -> bool:
        # Re-check on demand if previously unavailable (in case user started it)
        if not self._available:
            self._check_availability()
        return self._available

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(model=self.model, messages=messages)
        return response['message']['content']

    def generate_json(self, prompt: str, system_prompt: str = "") -> str:
        # Helper to gently coerce JSON if model doesn't support 'format="json"' strictly
        # But Gemma 3 usually does.
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt + "\n\nCRITICAL: RESPONSE MUST BE VALID MINIFIED JSON. NO MARKDOWN."})
        
        # Note: 'format="json"' is supported in newer Ollama versions
        try:
             response = self.client.chat(model=self.model, messages=messages, format="json", options={"temperature": 0.2})
             return response['message']['content']
        except:
             # Fallback without format="json" if model/version issues
             response = self.client.chat(model=self.model, messages=messages)
             return response['message']['content']


class GeminiProvider(AIProvider):
    """Cloud AI Provider using new Google GenAI SDK (v1.0+)."""
    
    def __init__(self):
        self._name = f"Cloud ({GEMINI_CONFIG['model']})"
        self.model_name = GEMINI_CONFIG['model']
        self._available = False
        self._setup_api()
    
    def _setup_api(self):
        self.api_key = None
        # Priority: 1. Streamlit Secrets, 2. Environment Variable
        if "GEMINI_API_KEY" in st.secrets:
            self.api_key = st.secrets["GEMINI_API_KEY"]
        elif GEMINI_CONFIG['api_key_env_var'] in os.environ:
            self.api_key = os.environ[GEMINI_CONFIG['api_key_env_var']]
            
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self._available = True
            except:
                self._available = False
        else:
            self._available = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_available(self) -> bool:
        return self._available

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        if not self._available: raise Exception("Gemini API not configured")
        
        config = {'temperature': 0.7}
        final_prompt = prompt
        
        # Gemma models (via Google API) do not support 'system_instruction' param
        # We must merge it into the user prompt.
        is_gemma = "gemma" in self.model_name.lower()
        
        if system_prompt:
             if is_gemma:
                 # Check if the user specifically requested structured formatting for the model
                 # otherwise just clear separation
                 final_prompt = f"{system_prompt}\n\n{prompt}"
             else:
                 config['system_instruction'] = system_prompt

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt,
            config=config
        )
        return response.text

    def generate_json(self, prompt: str, system_prompt: str = "") -> str:
        if not self._available: raise Exception("Gemini API not configured")
        
        config = {'temperature': 0.7}
        final_prompt = prompt
        is_gemma = "gemma" in self.model_name.lower()

        if not is_gemma:
            # Only Gemini models support native JSON mode via API param
            config['response_mime_type'] = 'application/json'

        if system_prompt:
            if is_gemma:
                final_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                config['system_instruction'] = system_prompt

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt,
            config=config
        )
        return response.text


class HybridHandler:
    """Manages AI interactions with fallback logic and Internet Search."""
    
    def __init__(self):
        self.ollama = OllamaProvider()
        self.gemini = GeminiProvider()
        self.search = DDGS() if SEARCH_ENABLED else None
        
    def _get_active_provider(self) -> AIProvider:
        """Determines best available provider based on config."""
        
        # 1. Force Local
        if AI_PROVIDER == "LOCAL":
            if self.ollama.is_available: return self.ollama
            raise Exception("Ollama is not running but AI_PROVIDER is set to LOCAL.")

        # 2. Force Cloud
        if AI_PROVIDER == "CLOUD":
            if self.gemini.is_available: return self.gemini
            raise Exception("Gemini API key missing but AI_PROVIDER is set to CLOUD.")

        # 3. AUTO (Default)
        if self.ollama.is_available:
            return self.ollama
        elif self.gemini.is_available:
            return self.gemini
        else:
            return None

    def get_status(self) -> str:
        provider = self._get_active_provider()
        if provider:
            return f"🟢 Connected: {provider.name}"
        return "🔴 No AI Connected (Start Ollama or set API Key)"

    def fetch_content(self, query: str, max_results: int = 3) -> str:
        """Search the internet for context."""
        if not SEARCH_ENABLED or not self.search:
            return ""
        
        try:
            results = self.search.text(query, max_results=max_results)
            context = ""
            for r in results:
                context += f"- Title: {r['title']}\n  URL: {r['href']}\n  Summary: {r['body']}\n\n"
            return context
        except Exception as e:
            return f"Error fetching content: {str(e)}"

    def _get_response_hybrid(self, prompt: str, system_prompt: str = "", json_mode: bool = False, use_search: bool = False) -> str:
        """Central generation logic with fallback and optional search."""
        
        # 1. Determine priority order
        providers = []
        
        # Check active preference
        if AI_PROVIDER == "LOCAL":
            providers.append(self.ollama)
        elif AI_PROVIDER == "CLOUD":
            providers.append(self.gemini)
        else: # AUTO
            # Priority: Local -> Cloud
            # We add BOTH if auto, regardless of current availability, to allow failover
            # But we prioritize Ollama if it LOOKS available
            if self.ollama.is_available:
                providers.append(self.ollama)
                providers.append(self.gemini)
            else:
                providers.append(self.gemini)
                # Optionally add Ollama as backup-backup? No, if it's dead it's dead.

        if not providers:
            # Fallback if nothing configured
            providers = [self.gemini]

        # Enhance prompt with search if requested
        final_prompt = prompt
        if use_search and SEARCH_ENABLED and self.search:
            try:
                # Heuristic: Extract search query from prompt or just use prompt
                context = self.fetch_content(prompt[:100]) # simple heuristic
                if context:
                    final_prompt = f"Context from Internet:\n{context}\n\nUser Question:\n{prompt}"
            except:
                pass # Search failure shouldn't block AI

        # 2. Try providers in order
        last_error = None
        
        for provider in providers:
            try:
                # Skip if we know it's unavailable (unless it's the only one)
                if not provider.is_available and len(providers) > 1:
                    continue
                    
                if json_mode:
                    result = provider.generate_json(final_prompt, system_prompt)
                    # CRITICAL: Validate JSON immediately. 
                    # If Local AI returns garbage, we MUST fail here to trigger failover to Cloud.
                    try:
                        cleaned = result.replace('```json', '').replace('```', '').strip()
                        # specific fix for common issues
                        if not cleaned: raise ValueError("Empty response")
                        json.loads(cleaned)
                        # passed validation, use original result (or cleaned?) 
                        # Return cleaned to save next step overhead
                        result = cleaned 
                    except Exception as json_err:
                        raise ValueError(f"Provider returned invalid JSON: {str(json_err)}")
                else:
                    result = provider.generate_text(final_prompt, system_prompt)
                    
                # If we got here, success!
                return result
                
            except Exception as e:
                last_error = e
                # Failover to next provider
                continue

        # If all failed
        return f"Error: All AI providers failed. Last error: {str(last_error)}"

    # ==================== Public Methods ====================

    def generate_grammar_explanation(self, topic: str) -> str:
        prompt = f"""Explain the French grammar topic: {topic}
        Include:
        1. Brief definition
        2. When to use it
        3. 2-3 concrete examples
        Keep it practical and exam-focused."""
        
        # Enhanced System Prompt to be aware of provider capabilities if needed
        system = "You are a French grammar expert preparing students for the TEF exam."
        
        return self._get_response_hybrid(prompt, system, use_search=True) # Search can help with obscure topics

    def generate_fill_in_blank_questions(self, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        system = "You are creating TEF-style grammar exercises. Return ONLY a valid JSON array."
        prompt = f"""Create {count} fill-in-the-blank questions for: {topic}.
        Format as JSON array: [{{"question": "...", "answer": "...", "explanation": "..."}}]"""
        
        response = self._get_response_hybrid(prompt, system, json_mode=True)
        try:
            cleaned = response.replace('```json', '').replace('```', '')
            return json.loads(cleaned)[:count]
        except:
            return []

    def grade_fill_in_blank(self, user_answer: str, correct_answer: str) -> Dict[str, Any]:
        # Simple local logic first
        u, c = user_answer.strip().lower(), correct_answer.strip().lower()
        if u == c: return {"correct": True, "user_answer": user_answer, "correct_answer": correct_answer}
        
        # Fuzzy match logic (could use Levenshtein here to save AI calls, but keeping it simple)
        # Using a simple set similarity for now to avoid dependency import issues if not present
        # In a robust app, use `thefuzz` or similar.
        metric = self._calculate_similarity(u, c)
        return {"correct": metric > 0.85, "user_answer": user_answer, "correct_answer": correct_answer}

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        if s1 == s2: return 1.0
        if not s1 or not s2: return 0.0
        set1, set2 = set(s1), set(s2)
        return len(set1 & set2) / len(set1 | set2)

    def generate_reading_article(self, topic: str, difficulty: str = "B1") -> str:
        system = f"Write clear, natural French at {difficulty} level."
        prompt = f"Write a 200-word article in French about: {topic}."
        # Use search to get real facts about the topic!
        return self._get_response_hybrid(prompt, system, use_search=True)

    def generate_reading_questions(self, article: str, count: int = 5) -> List[Dict[str, Any]]:
        system = "Return ONLY a valid JSON array."
        prompt = f"""Create {count} MCQ questions based on: \n{article}\n
        Format: [{{"question": "...", "options": ["A)..."], "correct_index": 0, "explanation": "..."}}]"""
        
        response = self._get_response_hybrid(prompt, system, json_mode=True)
        try:
            cleaned = response.replace('```json', '').replace('```', '')
            return json.loads(cleaned)[:count]
        except:
            return []

    def grade_essay(self, essay: str, task_type: str) -> Dict[str, Any]:
        system = "You are a TEF examiner. Return ONLY JSON."
        prompt = f"Grade this essay for '{task_type}'. Return JSON with structure_score, vocabulary_score, grammar_score, total_score, feedbacks, suggestions."
        
        response = self._get_response_hybrid(prompt, system, json_mode=True)
        try:
            cleaned = response.replace('```json', '').replace('```', '')
            return json.loads(cleaned)
        except:
            return {"total_score": 0, "structure_score":0, "vocabulary_score":0, "grammar_score":0, "structure_feedback": "Error", "suggestions": ["AI Error"]}

    def generate_speaking_question(self, difficulty: str = "B1") -> str:
        return self._get_response_hybrid(f"Generate one TEF speaking question (Level {difficulty}). Return ONLY text.", "")

    def evaluate_pronunciation(self, transcription: str, original_text: str) -> Dict[str, Any]:
        # Placeholder for pronunciation feedback
        return {"feedback": "Good effort! (Detailed phonetic analysis requires Audio analysis updates)"}
    
    # NEW: Generic Tutor Function
    def ask_tutor(self, query: str) -> str:
        """General purpose tutor function with search access."""
        system = "You are a helpful TEF tutor. Use the provided context to answer accurately."
        return self._get_response_hybrid(query, system, use_search=True)


# Global instance
ai_handler = HybridHandler()
