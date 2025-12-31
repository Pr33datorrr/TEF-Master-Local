"""
TEF Master Local - Enhanced Resource Library
Integrated with official TEF resources from research document.
EASILY EXTENSIBLE: Add new resources by appending to RESOURCES list.
"""

# Each resource has: id, category, title, url, description
# To add new resources, simply append to this list

RESOURCES = [
    # ==================== Official & Simulation ====================
    {
        "id": "res_001",
        "category": "Official & Simulation",
        "title": "Le français des affaires - Official Samples",
        "url": "https://www.lefrancaisdesaffaires.fr/en/candidate/test-evaluation-francais/tef-canada/preparation/",
        "description": "Official CCI Paris sample papers for Reading, Listening, and Writing. The gold standard for exam format."
    },
    {
        "id": "res_002",
        "category": "Official & Simulation",
        "title": "TV5Monde TEF Simulator",
        "url": "https://apprendre.tv5monde.com/fr/tcf",
        "description": "Real-condition 90-minute exam simulator. Best for testing endurance."
    },
    {
        "id": "res_003",
        "category": "Official & Simulation",
        "title": "French Test Simulator",
        "url": "https://frenchtestsimulator.com/",
        "description": "Realistic online interface that mimics the official e-TEF software."
    },
    
    # ==================== Listening ====================
    {
        "id": "res_004",
        "category": "Listening",
        "title": "RFI Savoirs - Journal en français facile",
        "url": "https://savoirs.rfi.fr/fr/apprendre-enseigner/langue-francaise/journal-en-francais-facile",
        "description": "Daily 10-minute news with transcripts. Essential for Section C & D listening."
    },
    {
        "id": "res_005",
        "category": "Listening",
        "title": "InnerFrench Podcast",
        "url": "https://innerfrench.com/podcast/",
        "description": "Intermediate listening (B1-B2) focusing on culture and society. Clear audio."
    },
    {
        "id": "list_003",
        "category": "Listening",
        "title": "France Info - Direct Radio",
        "url": "https://www.francetvinfo.fr/en-direct/radio.html",
        "description": "Live French radio - authentic listening practice."
    },
    {
        "id": "list_002",
        "category": "Listening",
        "title": "Podcast Français Facile",
        "url": "https://www.podcastfrancaisfacile.com/",
        "description": "Graded listening materials with transcripts from A1 to B2."
    },
    
    # ==================== Grammar & Structure ====================
    {
        "id": "res_006",
        "category": "Grammar",
        "title": "Lawless French - Grammar by Level",
        "url": "https://www.lawlessfrench.com/grammar/lessons-by-level/",
        "description": "The primary grammar reference. CEFR-categorized lessons (A1-C1)."
    },
    {
        "id": "gram_002",
        "category": "Grammar",
        "title": "Le Point du FLE - Grammaire",
        "url": "https://www.lepointdufle.net/p/grammaire.htm",
        "description": "Extensive grammar resource directory with explanations and exercises."
    },
    {
        "id": "gram_003",
        "category": "Grammar",
        "title": "Français Facile - Grammaire",
        "url": "https://www.francaisfacile.com/index.php",
        "description": "Thousands of free grammar exercises with instant feedback."
    },
    
    # ==================== Reading & Vocabulary ====================
    {
        "id": "res_007",
        "category": "Reading",
        "title": "Le Monde",
        "url": "https://www.lemonde.fr",
        "description": "High-level authentic news for Section D reading practice."
    },
    {
        "id": "res_008",
        "category": "Vocabulary",
        "title": "FrenchLearner Vocabulary Lists",
        "url": "https://www.frenchlearner.com/vocabulary/environment/",
        "description": "Thematic vocabulary lists (Environment, Health) crucial for Section B writing."
    },
    {
        "id": "read_002",
        "category": "Reading",
        "title": "1jour1actu",
        "url": "https://www.1jour1actu.com/",
        "description": "News for young readers - accessible French at A2-B1 level."
    },
    {
        "id": "read_003",
        "category": "Reading",
        "title": "Le Monde - Faits Divers",
        "url": "https://www.lemonde.fr/police-justice/",
        "description": "Real 'faits divers' articles - essential for TEF writing practice."
    },
    {
        "id": "vocab_002",
        "category": "Vocabulary",
        "title": "WordReference French Dictionary",
        "url": "https://www.wordreference.com/fr/",
        "description": "Best online French-English dictionary with examples and forums."
    },
    {
        "id": "vocab_003",
        "category": "Vocabulary",
        "title": "Larousse Dictionary",
        "url": "https://www.larousse.fr/dictionnaires/francais",
        "description": "Authoritative French monolingual dictionary."
    },
    {
        "id": "vocab_001",
        "category": "Vocabulary",
        "title": "Quizlet - TEF Vocabulary Sets",
        "url": "https://quizlet.com/subject/tef-canada/",
        "description": "User-created TEF vocabulary flashcard sets."
    },
    
    # ==================== Writing ====================
    {
        "id": "writ_001",
        "category": "Writing",
        "title": "PrepMyFuture - TEF Writing Tips",
        "url": "https://prepmyfuture.com/tef-canada-writing-tips/",
        "description": "Free TEF writing strategies and task examples."
    },
    {
        "id": "writ_002",
        "category": "Writing",
        "title": "BonPatron - Grammar Checker",
        "url": "https://bonpatron.com/",
        "description": "Free online grammar and spelling checker for French writing."
    },
    {
        "id": "writ_003",
        "category": "Writing",
        "title": "Lingolia - French Writing Exercises",
        "url": "https://francais.lingolia.com/en/writing",
        "description": "Guided writing exercises and composition practice."
    },
    
    # ==================== Practice Tests ====================
    {
        "id": "test_001",
        "category": "Practice Tests",
        "title": "PrepMyFuture - Free TEF Practice",
        "url": "https://prepmyfuture.com/free-tef-canada-practice-tests/",
        "description": "Free TEF practice tests and sample questions."
    },
    {
        "id": "test_002",
        "category": "Practice Tests",
        "title": "RFI Savoirs - Test de niveau",
        "url": "https://savoirs.rfi.fr/fr/testez-votre-niveau-de-francais",
        "description": "Free level assessment test to track your progress."
    },
    
    # ==================== Cultural Content ====================
    {
        "id": "cult_001",
        "category": "Cultural Content",
        "title": "Arte (Français)",
        "url": "https://www.arte.tv/fr/",
        "description": "French-German cultural TV channel with documentaries and films."
    },
    {
        "id": "cult_002",
        "category": "Cultural Content",
        "title": "France 24 - L'info en continu",
        "url": "https://www.france24.com/fr/",
        "description": "24/7 French news channel with videos and articles."
    },
    {
        "id": "cult_003",
        "category": "Cultural Content",
        "title": "Karambolage - Arte",
        "url": "https://www.arte.tv/fr/videos/RC-014034/karambolage/",
        "description": "Fun short videos comparing French and German cultures."
    },
    {
        "id": "yt_001",
        "category": "Cultural Content",
        "title": "YouTube - Easy French",
        "url": "https://www.youtube.com/@EasyFrench",
        "description": "Street interviews in French with subtitles (great for listening)."
    },
    
    # ==================== Pronunciation ====================
    {
        "id": "pron_001",
        "category": "Pronunciation",
        "title": "Forvo - French Pronunciation",
        "url": "https://forvo.com/languages/fr/",
        "description": "Native speaker pronunciations for any French word."
    },
    {
        "id": "pron_002",
        "category": "Pronunciation",
        "title": "YouTube - Français avec Pierre",
        "url": "https://www.youtube.com/@francaisavecpierre",
        "description": "Excellent pronunciation and speaking tutorials."
    },
    {
        "id": "yt_002",
        "category": "Pronunciation",
        "title": "YouTube - Français Authentique",
        "url": "https://www.youtube.com/@francaisauthentique",
        "description": "Natural French learning through authentic content."
    }
]


def get_all_resources():
    """Get all resources."""
    return RESOURCES


def get_resources_by_category(category: str):
    """Get resources filtered by category."""
    return [r for r in RESOURCES if r["category"] == category]


def search_resources(query: str):
    """Search resources by title or description."""
    query_lower = query.lower()
    return [
        r for r in RESOURCES 
        if query_lower in r["title"].lower() or query_lower in r["description"].lower()
    ]


def get_resource_by_id(resource_id: str):
    """Get a specific resource by ID."""
    for resource in RESOURCES:
        if resource["id"] == resource_id:
            return resource
    return None


def get_all_categories():
    """Get all unique categories."""
    return sorted(list(set(r["category"] for r in RESOURCES)))


# ==================== EXTENSIBILITY GUIDE ====================
"""
TO ADD NEW RESOURCES:

1. Add a new dictionary to the RESOURCES list above with this format:
   {
       "id": "category_xxx",  # Unique ID (use category prefix + number)
       "category": "Category Name",  # Must match existing or create new category
       "title": "Resource Title",
       "url": "https://example.com",
       "description": "Brief description of the resource"
   }

2. Example of adding a new grammar resource:
   {
       "id": "gram_004",
       "category": "Grammar",
       "title": "New Grammar Site",
       "url": "https://newsite.com",
       "description": "Great explanations for advanced learners."
   }

3. To add a new category, just use a new category name in any resource.
   The system automatically detects all categories.

4. Save this file - changes appear immediately in the app!
"""
