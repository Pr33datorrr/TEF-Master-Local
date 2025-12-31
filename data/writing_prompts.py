"""
TEF Master Local - Enhanced Writing Prompts
Metadata-rich prompts from TEF research for realistic practice.
"""

# Writing prompts with detailed metadata for both user hints and AI grading

WRITING_PROMPTS = [
    # ==================== SECTION A: FAIT DIVERS (Narrative) ====================
    {
        "id": "A_01",
        "type": "Section A - Fait Divers",
        "topic": "The Hero Dog",
        "prompt": "Un chien réveille sa famille et les sauve d'un incendie. Racontez.",
        "word_count": 80,
        "metadata": {
            "tense_focus": ["Passé Composé", "Imparfait"],
            "key_vocab": ["aboyer", "fumée", "pompiers", "sauver"],
            "structure_hints": "1) Set the scene (Imparfait), 2) Describe the action (Passé Composé), 3) Conclude with the outcome"
        }
    },
    {
        "id": "A_02",
        "type": "Section A - Fait Divers",
        "topic": "The Lottery Surprise",
        "prompt": "Un homme jette son ticket de loto par erreur et le retrouve le lendemain. Racontez la suite.",
        "word_count": 80,
        "metadata": {
            "tense_focus": ["Plus-que-parfait", "Passé Composé"],
            "key_vocab": ["ticket", "poubelle", "chance", "millionnaire"],
            "structure_hints": "Use Plus-que-parfait to show what had happened before finding the ticket"
        }
    },
    {
        "id": "A_03",
        "type": "Section A - Fait Divers",
        "topic": "The Good Samaritan",
        "prompt": "Une vieille dame perd son sac et un jeune homme le lui rapporte intact. Racontez l'histoire.",
        "word_count": 80,
        "metadata": {
            "tense_focus": ["Passé Composé", "Imparfait"],
            "key_vocab": ["perdre", "rapporter", "honnêteté", "remercier"],
            "structure_hints": "Focus on the sequence of events and the emotional impact"
        }
    },
      
    # ==================== SECTION B: ARGUMENTATION (Formal Letter) ====================
    {
        "id": "B_01",
        "type": "Section B - Formal Letter",
        "topic": "Free Museums",
        "prompt": "Vous avez lu que tous les musées devraient être gratuits. Écrivez au journal pour donner votre opinion.",
        "word_count": 200,
        "metadata": {
            "structure": "Formal Letter",
            "grammar_focus": ["Subjunctive", "Connectors"],
            "key_arguments": ["Culture for all", "Economic cost", "Education"],
            "structure_hints": "1) Opening formula, 2) State position, 3) 2-3 arguments with connectors, 4) Conclusion, 5) Closing formula"
        }
    },
    {
        "id": "B_02",
        "type": "Section B - Formal Letter",
        "topic": "Smartphones in Schools",
        "prompt": "Un article propose d'interdire les portables au lycée. Vous réagissez.",
        "word_count": 200,
        "metadata": {
            "structure": "Formal Letter",
            "grammar_focus": ["Conditional (Suggestion)", "Subjunctive"],
            "key_arguments": ["Concentration", "Cyberbullying", "Pedagogical tool"],
            "structure_hints": "Use 'Il serait préférable que...', 'Bien que...', etc."
        }
    },
    {
        "id": "B_03",
        "type": "Section B - Formal Letter",
        "topic": "Work from Home",
        "prompt": "Votre entreprise veut rendre le télétravail obligatoire. Vous écrivez au DRH pour exprimer votre désaccord.",
        "word_count": 200,
        "metadata": {
            "structure": "Formal Letter",
            "grammar_focus": ["Polite refusal", "Logical connectors"],
            "key_arguments": ["Social isolation", "Team spirit", "Work-life balance"],
            "structure_hints": "Use polite conditional: 'Je souhaiterais...', 'Il me semble que...'"
        }
    },
    
    # Add original prompts from writing_clinic.py
    {
        "id": "A_04",
        "type": "Section A - Fait Divers",
        "topic": "Traffic Accident",
        "prompt": "Un accident de voiture s'est produit à un carrefour très fréquenté. Décrivez les faits.",
        "word_count": 80,
        "metadata": {
            "tense_focus": ["Passé Composé", "Imparfait"],
            "key_vocab": ["carrefour", "percuter", "blessé", "urgences"],
            "structure_hints": "Who, what, when, where - classic news style"
        }
    },
    {
        "id": "B_04",
        "type": "Section B - Complaint Letter",
        "topic": "Defective Product",
        "prompt": "Vous avez acheté un produit défectueux. Écrivez à l'entreprise pour vous plaindre et demander une solution.",
        "word_count": 200,
        "metadata": {
            "structure": "Formal Letter",
            "grammar_focus": ["Conditional (polite request)", "Past tenses"],
            "key_arguments": ["Description of problem", "Impact", "Expected resolution"],
            "structure_hints": "Formal opening, state facts, express disappointment politely, request action"
        }
    },
    {
        "id": "B_05",
        "type": "Section B - Invitation Response",
        "topic": "Wedding Invitation",
        "prompt": "Un ami vous invite à son mariage, mais vous ne pouvez pas y assister. Écrivez pour expliquer pourquoi et vous excuser.",
        "word_count": 80,
        "metadata": {
            "structure": "Informal Letter/Email",
            "grammar_focus": ["Future proche", "Conditional"],
            "key_arguments": ["Apology", "Reason", "Good wishes"],
            "structure_hints": "Warm opening, sincere apology, brief explanation, congratulations"
        }
    }
]


def get_all_prompts():
    """Get all writing prompts."""
    return WRITING_PROMPTS


def get_prompts_by_type(prompt_type: str):
    """Get prompts by type (Section A or Section B)."""
    return [p for p in WRITING_PROMPTS if prompt_type in p["type"]]


def get_random_prompt(prompt_type=None):
    """Get a random prompt, optionally filtered by type."""
    import random
    if prompt_type:
        prompts = get_prompts_by_type(prompt_type)
    else:
        prompts = WRITING_PROMPTS
    return random.choice(prompts) if prompts else None


def get_prompt_by_id(prompt_id: str):
    """Get a specific prompt by ID."""
    for prompt in WRITING_PROMPTS:
        if prompt["id"] == prompt_id:
            return prompt
    return None
