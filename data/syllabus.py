"""
TEF Master Local - Syllabus Data
Week-by-week curriculum structure for TEF preparation (A1 to B2).
Easily extensible - add new weeks as needed.
"""

# TEF Syllabus organized by CEFR levels and weeks
# Each week contains: level, grammar topics, vocabulary themes, and XP value

TEF_SYLLABUS = [
    # ==================== A1 Level (Weeks 1-8) ====================
    {
        "week": 1,
        "level": "A1",
        "title": "Introduction & Greetings",
        "grammar_topics": ["Present tense - être", "Present tense - avoir", "Subject pronouns"],
        "vocabulary_themes": ["Greetings", "Introductions", "Numbers 1-20"],
        "reading_topics": ["Simple dialogues", "Basic personal information"],
        "writing_tasks": ["Introduce yourself", "Write a simple greeting card"],
        "xp_value": 100
    },
    {
        "week": 2,
        "level": "A1",
        "title": "Daily Routines",
        "grammar_topics": ["Regular -ER verbs", "Negation (ne...pas)", "Question formation"],
        "vocabulary_themes": ["Daily activities", "Time expressions", "Family members"],
        "reading_topics": ["Daily schedules", "Family descriptions"],
        "writing_tasks": ["Describe your day", "Write about your family"],
        "xp_value": 100
    },
    {
        "week": 3,
        "level": "A1",
        "title": "Food & Shopping",
        "grammar_topics": ["Articles (le, la, les)", "Partitive articles", "Quantities"],
        "vocabulary_themes": ["Food items", "Shopping vocabulary", "Restaurants"],
        "reading_topics": ["Menus", "Shopping lists", "Recipes"],
        "writing_tasks": ["Write a shopping list", "Order in a restaurant"],
        "xp_value": 100
    },
    {
        "week": 4,
        "level": "A1",
        "title": "Places & Directions",
        "grammar_topics": ["Prepositions of place", "Aller (to go)", "Imperative mood"],
        "vocabulary_themes": ["City locations", "Directions", "Transportation"],
        "reading_topics": ["Maps", "Direction instructions"],
        "writing_tasks": ["Give directions", "Describe your neighborhood"],
        "xp_value": 100
    },
    {
        "week": 5,
        "level": "A1",
        "title": "Hobbies & Leisure",
        "grammar_topics": ["Faire expressions", "Irregular verbs", "Adjective agreement"],
        "vocabulary_themes": ["Hobbies", "Sports", "Free time activities"],
        "reading_topics": ["Activity descriptions", "Sports articles"],
        "writing_tasks": ["Describe your hobbies", "Invitation to an activity"],
        "xp_value": 100
    },
    {
        "week": 6,
        "level": "A1",
        "title": "Weather & Seasons",
        "grammar_topics": ["Impersonal expressions", "Faire + weather", "Future proche"],
        "vocabulary_themes": ["Weather", "Seasons", "Clothing"],
        "reading_topics": ["Weather forecasts", "Seasonal activities"],
        "writing_tasks": ["Describe today's weather", "Write about your favorite season"],
        "xp_value": 100
    },
    {
        "week": 7,
        "level": "A1",
        "title": "Health & Body",
        "grammar_topics": ["Reflexive verbs", "Avoir mal à", "Modal verbs (pouvoir, vouloir)"],
        "vocabulary_themes": ["Body parts", "Health", "Doctor visits"],
        "reading_topics": ["Health advice", "Doctor dialogues"],
        "writing_tasks": ["Describe an illness", "Make a doctor appointment"],
        "xp_value": 100
    },
    {
        "week": 8,
        "level": "A1",
        "title": "A1 Review & Assessment",
        "grammar_topics": ["All A1 grammar review"],
        "vocabulary_themes": ["All A1 vocabulary review"],
        "reading_topics": ["Mixed A1 texts"],
        "writing_tasks": ["Comprehensive A1 writing task"],
        "xp_value": 150
    },
    
    # ==================== A2 Level (Weeks 9-16) ====================
    {
        "week": 9,
        "level": "A2",
        "title": "Past Events - Passé Composé",
        "grammar_topics": ["Passé composé with avoir", "Passé composé with être", "Past participles"],
        "vocabulary_themes": ["Past time expressions", "Life events", "Vacations"],
        "reading_topics": ["Personal narratives", "Travel stories"],
        "writing_tasks": ["Recount a vacation", "Describe a past event"],
        "xp_value": 120
    },
    {
        "week": 10,
        "level": "A2",
        "title": "Making Comparisons",
        "grammar_topics": ["Comparative adjectives", "Superlative", "Comparative adverbs"],
        "vocabulary_themes": ["Describing people", "Products", "Cities"],
        "reading_topics": ["Product comparisons", "City descriptions"],
        "writing_tasks": ["Compare two cities", "Product review"],
        "xp_value": 120
    },
    {
        "week": 11,
        "level": "A2",
        "title": "Future Plans",
        "grammar_topics": ["Simple future", "Future proche vs future simple", "Time expressions"],
        "vocabulary_themes": ["Goals", "Projects", "Career"],
        "reading_topics": ["Future predictions", "Career plans"],
        "writing_tasks": ["Describe your future plans", "5-year goals"],
        "xp_value": 120
    },
    {
        "week": 12,
        "level": "A2",
        "title": "Describing the Past - Imparfait",
        "grammar_topics": ["Imparfait formation", "Imparfait vs passé composé", "Habitual actions"],
        "vocabulary_themes": ["Childhood", "Habits", "Memories"],
        "reading_topics": ["Childhood stories", "Historical descriptions"],
        "writing_tasks": ["Describe your childhood", "A memorable experience"],
        "xp_value": 120
    },
    {
        "week": 13,
        "level": "A2",
        "title": "Expressing Opinions",
        "grammar_topics": ["Opinion verbs", "Subjunctive introduction", "Conjunctions"],
        "vocabulary_themes": ["Opinions", "Preferences", "Debates"],
        "reading_topics": ["Opinion articles", "Reviews"],
        "writing_tasks": ["Write a review", "Express your opinion on a topic"],
        "xp_value": 120
    },
    {
        "week": 14,
        "level": "A2",
        "title": "Hypothetical Situations",
        "grammar_topics": ["Conditional present", "Si clauses (basic)", "Polite requests"],
        "vocabulary_themes": ["Wishes", "Dreams", "Advice"],
        "reading_topics": ["Advice columns", "Dream scenarios"],
        "writing_tasks": ["Give advice", "Describe your dream life"],
        "xp_value": 120
    },
    {
        "week": 15,
        "level": "A2",
        "title": "Pronouns & Object Complements",
        "grammar_topics": ["Direct object pronouns", "Indirect object pronouns", "Y and EN"],
        "vocabulary_themes": ["Replacing nouns", "Communication", "Relationships"],
        "reading_topics": ["Dialogues with pronouns", "Letters"],
        "writing_tasks": ["Write a letter using pronouns", "Respond to messages"],
        "xp_value": 120
    },
    {
        "week": 16,
        "level": "A2",
        "title": "A2 Review & Assessment",
        "grammar_topics": ["All A2 grammar review"],
        "vocabulary_themes": ["All A2 vocabulary review"],
        "reading_topics": ["Mixed A2 texts"],
        "writing_tasks": ["Comprehensive A2 writing task"],
        "xp_value": 150
    },
    
    # ==================== B1 Level (Weeks 17-24) ====================
    {
        "week": 17,
        "level": "B1",
        "title": "Complex Past Narratives",
        "grammar_topics": ["Plus-que-parfait", "Past narrative sequencing", "Reported speech (past)"],
        "vocabulary_themes": ["Storytelling", "News events", "Biographies"],
        "reading_topics": ["News articles", "Biographies"],
        "writing_tasks": ["Write a news article (fait divers)", "Tell a complex story"],
        "xp_value": 140
    },
    {
        "week": 18,
        "level": "B1",
        "title": "Subjunctive Mood - Emotions",
        "grammar_topics": ["Subjunctive with emotions", "Subjunctive with doubt", "Expressions requiring subjunctive"],
        "vocabulary_themes": ["Emotions", "Uncertainty", "Wishes"],
        "reading_topics": ["Emotional texts", "Opinion pieces"],
        "writing_tasks": ["Express emotions and wishes", "Argumentative paragraph"],
        "xp_value": 140
    },
    {
        "week": 19,
        "level": "B1",
        "title": "Cause, Consequence, Purpose",
        "grammar_topics": ["Causal conjunctions", "Consequence markers", "Purpose clauses"],
        "vocabulary_themes": ["Reasoning", "Arguments", "Explanations"],
        "reading_topics": ["Explanatory texts", "Argumentative essays"],
        "writing_tasks": ["Explain causes and effects", "Argumentative essay"],
        "xp_value": 140
    },
    {
        "week": 20,
        "level": "B1",
        "title": "Passive Voice & Impersonal Constructions",
        "grammar_topics": ["Passive voice", "On construction", "Reflexive passive"],
        "vocabulary_themes": ["Formal writing", "Processes", "Instructions"],
        "reading_topics": ["Formal texts", "Instructions"],
        "writing_tasks": ["Formal letter", "Process description"],
        "xp_value": 140
    },
    {
        "week": 21,
        "level": "B1",
        "title": "Relative Pronouns & Complex Sentences",
        "grammar_topics": ["Qui, que, dont, où", "Complex relative clauses", "Sentence subordination"],
        "vocabulary_themes": ["Descriptions", "Definitions", "Specifications"],
        "reading_topics": ["Descriptive texts", "Definitions"],
        "writing_tasks": ["Write detailed descriptions", "Define concepts"],
        "xp_value": 140
    },
    {
        "week": 22,
        "level": "B1",
        "title": "Agreement & Participles",
        "grammar_topics": ["Past participle agreement", "Present participle", "Gerund"],
        "vocabulary_themes": ["Accuracy", "Details", "Formal writing"],
        "reading_topics": ["Formal documents", "Literature excerpts"],
        "writing_tasks": ["Formal composition", "Detailed account"],
        "xp_value": 140
    },
    {
        "week": 23,
        "level": "B1",
        "title": "Argumentation & Debate",
        "grammar_topics": ["Argumentative connectors", "Concession", "Opposition"],
        "vocabulary_themes": ["Debate vocabulary", "Arguments", "Counter-arguments"],
        "reading_topics": ["Opinion articles", "Debates"],
        "writing_tasks": ["Letter of argument", "Debate position paper"],
        "xp_value": 140
    },
    {
        "week": 24,
        "level": "B1",
        "title": "B1 Review & Assessment",
        "grammar_topics": ["All B1 grammar review"],
        "vocabulary_themes": ["All B1 vocabulary review"],
        "reading_topics": ["Mixed B1 texts"],
        "writing_tasks": ["Comprehensive B1 writing task"],
        "xp_value": 200
    },
    
    # ==================== B2 Level (Weeks 25-30) ====================
    {
        "week": 25,
        "level": "B2",
        "title": "Advanced Subjunctive",
        "grammar_topics": ["Subjunctive in relative clauses", "Subjunctive after superlatives", "Past subjunctive"],
        "vocabulary_themes": ["Nuanced opinions", "Complex emotions", "Abstract concepts"],
        "reading_topics": ["Literary texts", "Complex opinion pieces"],
        "writing_tasks": ["Nuanced argumentation", "Complex analysis"],
        "xp_value": 160
    },
    {
        "week": 26,
        "level": "B2",
        "title": "Conditional & Hypothetical (Advanced)",
        "grammar_topics": ["Conditional past", "Advanced si clauses", "Mixed conditionals"],
        "vocabulary_themes": ["Regrets", "Hypothetical scenarios", "Advice giving"],
        "reading_topics": ["Philosophical texts", "Analysis"],
        "writing_tasks": ["Reflect on hypothetical situations", "Analyze scenarios"],
        "xp_value": 160
    },
    {
        "week": 27,
        "level": "B2",
        "title": "Discourse Markers & Cohesion",
        "grammar_topics": ["Advanced connectors", "Discourse organization", "Text cohesion"],
        "vocabulary_themes": ["Formal discourse", "Academic writing", "Professional communication"],
        "reading_topics": ["Academic articles", "Professional texts"],
        "writing_tasks": ["Academic essay", "Professional report"],
        "xp_value": 160
    },
    {
        "week": 28,
        "level": "B2",
        "title": "Stylistic Variations",
        "grammar_topics": ["Literary tenses", "Style register", "Narrative techniques"],
        "vocabulary_themes": ["Stylistic choices", "Register", "Tone"],
        "reading_topics": ["Literary excerpts", "Varied styles"],
        "writing_tasks": ["Creative writing with style variation", "Formal letter with literary touch"],
        "xp_value": 160
    },
    {
        "week": 29,
        "level": "B2",
        "title": "TEF Exam Strategies",
        "grammar_topics": ["All grammar review", "Common pitfalls", "Exam techniques"],
        "vocabulary_themes": ["TEF-specific vocabulary", "Exam terminology"],
        "reading_topics": ["Real TEF practice texts"],
        "writing_tasks": ["Timed TEF writing tasks", "All task types"],
        "xp_value": 160
    },
    {
        "week": 30,
        "level": "B2",
        "title": "Final Review & Mock Exam",
        "grammar_topics": ["Comprehensive grammar review (A1-B2)"],
        "vocabulary_themes": ["Comprehensive vocabulary review"],
        "reading_topics": ["Full-length mock reading comprehension"],
        "writing_tasks": ["Full TEF mock exam writing section"],
        "xp_value": 200
    }
]


def get_week_data(week_number: int):
    """Get data for a specific week."""
    for week in TEF_SYLLABUS:
        if week["week"] == week_number:
            return week
    return None


def get_weeks_by_level(level: str):
    """Get all weeks for a specific CEFR level."""
    return [week for week in TEF_SYLLABUS if week["level"] == level]


def get_total_weeks():
    """Get total number of weeks in curriculum."""
    return len(TEF_SYLLABUS)


def get_all_levels():
    """Get all unique levels in curriculum."""
    return sorted(list(set(week["level"] for week in TEF_SYLLABUS)))
