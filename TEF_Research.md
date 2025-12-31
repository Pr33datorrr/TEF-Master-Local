# **Master Data Package: TEF Master Local App**

Version: 1.0 (Consolidated)  
Target: Coding Agent / Developer  
Context: This document contains the verified data structures, syllabus logic, and resource URLs needed to populate the app.py and database of the TEF Master Local LMS.

## **1\. The Ultimate Resource Library (JSON Database)**

Instruction for Agent: Use this JSON object to populate the resources table in SQLite or the main dataframe in Streamlit.  
Source: Merged from verified URLs (Doc 1\) and Categories (Doc 2).  
\[  
  {  
    "id": "res\_001",  
    "category": "Official & Simulation",  
    "name": "Le français des affaires \- Samples",  
    "url": "\[https://www.lefrancaisdesaffaires.fr/en/candidate/test-evaluation-francais/tef-canada/preparation/\](https://www.lefrancaisdesaffaires.fr/en/candidate/test-evaluation-francais/tef-canada/preparation/)",  
    "description": "Official CCI Paris sample papers for Reading, Listening, and Writing. The gold standard for exam format."  
  },  
  {  
    "id": "res\_002",  
    "category": "Official & Simulation",  
    "name": "TV5Monde TEF Simulator",  
    "url": "\[https://apprendre.tv5monde.com/fr/tcf\](https://apprendre.tv5monde.com/fr/tcf)",  
    "description": "Real-condition 90-minute exam simulator. Best for testing endurance."  
  },  
  {  
    "id": "res\_003",  
    "category": "Official & Simulation",  
    "name": "French Test Simulator",  
    "url": "\[https://frenchtestsimulator.com/\](https://frenchtestsimulator.com/)",  
    "description": "Realistic online interface that mimics the official e-TEF software."  
  },  
  {  
    "id": "res\_004",  
    "category": "Listening (Compréhension Orale)",  
    "name": "RFI Savoirs \- Journal en français facile",  
    "url": "\[https://savoirs.rfi.fr/fr/apprendre-enseigner/langue-francaise/journal-en-francais-facile\](https://savoirs.rfi.fr/fr/apprendre-enseigner/langue-francaise/journal-en-francais-facile)",  
    "description": "Daily 10-minute news with transcripts. Essential for Section C & D listening."  
  },  
  {  
    "id": "res\_005",  
    "category": "Listening (Compréhension Orale)",  
    "name": "InnerFrench Podcast",  
    "url": "\[https://innerfrench.com/podcast/\](https://innerfrench.com/podcast/)",  
    "description": "Intermediate listening (B1-B2) focusing on culture and society. Clear audio."  
  },  
  {  
    "id": "res\_006",  
    "category": "Grammar & Structure",  
    "name": "Lawless French",  
    "url": "\[https://www.lawlessfrench.com/grammar/lessons-by-level/\](https://www.lawlessfrench.com/grammar/lessons-by-level/)",  
    "description": "The primary grammar reference. CEFR-categorized lessons (A1-C1)."  
  },  
  {  
    "id": "res\_007",  
    "category": "Reading & Vocab",  
    "name": "Le Monde",  
    "url": "\[https://www.lemonde.fr\](https://www.lemonde.fr)",  
    "description": "High-level authentic news for Section D reading practice."  
  },  
  {  
    "id": "res\_008",  
    "category": "Reading & Vocab",  
    "name": "FrenchLearner Vocabulary Lists",  
    "url": "\[https://www.frenchlearner.com/vocabulary/environment/\](https://www.frenchlearner.com/vocabulary/environment/)",  
    "description": "Thematic vocabulary lists (Environment, Health) crucial for Section B writing."  
  }  
\]

## **2\. The Dynamic Study Roadmap (12-Week Syllabus)**

**Instruction for Agent:** This python dictionary maps the weekly progression. It uses a "Task-Based" approach (teaching grammar *for* specific exam tasks).

study\_roadmap \= {  
    "Month 1": {  
        "Focus": "The Narrative Arc (Past Tenses & Fait Divers)",  
        "Weeks": {  
            1: {  
                "Title": "Foundations of the Past",  
                "Grammar": \["Passé Composé (Avoir vs Être)", "Regular/Irregular Participles"\],  
                "Theme": "Daily Routine & Accidents",  
                "TEF\_Task": "Section A: Intro to Fait Divers",  
                "Resource\_ID": "res\_006"  \# Link to Lawless French  
            },  
            2: {  
                "Title": "Setting the Scene",  
                "Grammar": \["L'Imparfait (Description)", "PC vs Imparfait (Interruption Rule)"\],  
                "Theme": "Weather & Emotions",  
                "TEF\_Task": "Section A: Writing the 'Chapeau' (Intro)",  
                "Resource\_ID": "res\_006"  
            },  
            3: {  
                "Title": "Complex Narration",  
                "Grammar": \["Passive Voice (La Voix Passive)", "Time Markers (Hier, La veille)"\],  
                "Theme": "Crime & Justice",  
                "TEF\_Task": "Section A: Full Narration",  
                "Resource\_ID": "res\_004"  \# RFI for listening to news reports  
            },  
            4: {  
                "Title": "Synthesis & Speed",  
                "Grammar": \["Plus-que-parfait (Past Perfect)", "Adverb Placement"\],  
                "Theme": "Emergency Services",  
                "TEF\_Task": "Section A: Timed Mock Test (10 mins)",  
                "Resource\_ID": "res\_001"  \# Official Samples  
            }  
        }  
    },  
    "Month 2": {  
        "Focus": "The Argumentative Arc (Opinion & Formal Letter)",  
        "Weeks": {  
            5: {  
                "Title": "Structuring Opinion",  
                "Grammar": \["Present Indicative (Review)", "Logical Connectors (Toutefois, Par contre)"\],  
                "Theme": "Work & Employment (Télétravail)",  
                "TEF\_Task": "Section B: Formal Letter Structure",  
                "Resource\_ID": "res\_001"  
            },  
            6: {  
                "Title": "The Art of Convincing",  
                "Grammar": \["Subjunctive Present (Necessity/Emotion)", "Il faut que..."\],  
                "Theme": "Education & Technology",  
                "TEF\_Task": "Section B: Expressing Necessity",  
                "Resource\_ID": "res\_006"  
            },  
            7: {  
                "Title": "Hypothetical Scenarios",  
                "Grammar": \["Conditional Present (Politeness)", "Si Clauses (Hypothesis)"\],  
                "Theme": "Travel & Tourism",  
                "TEF\_Task": "Section B: Making Suggestions",  
                "Resource\_ID": "res\_006"  
            },  
            8: {  
                "Title": "Advanced Argumentation",  
                "Grammar": \["Relative Pronouns (Qui, Que, Dont)", "Mise en relief (C'est...qui)"\],  
                "Theme": "Society & Culture",  
                "TEF\_Task": "Section B: Timed Mock Test (200 words)",  
                "Resource\_ID": "res\_007"  \# Le Monde for opinion pieces  
            }  
        }  
    },  
    "Month 3": {  
        "Focus": "Mastery & Endurance (B2/C1 Polish)",  
        "Weeks": {  
            9: {  
                "Title": "Listening Intensity",  
                "Grammar": \["Futur Antérieur", "Gérondif (Simultaneous action)"\],  
                "Theme": "Health & Science",  
                "TEF\_Task": "Listening Sections C & D (Long audio)",  
                "Resource\_ID": "res\_004"  
            },  
            10: {  
                "Title": "Precision Grammar",  
                "Grammar": \["Object Pronouns (COD/COI/Y/En)", "Prepositions"\],  
                "Theme": "Environment & Ecology",  
                "TEF\_Task": "Lexique et Structure Drills",  
                "Resource\_ID": "res\_006"  
            },  
            11: {  
                "Title": "Speaking Fluency",  
                "Grammar": \["Discourse Markers (Oral connectors)", "Question Inversion"\],  
                "Theme": "Abstract Topics (Happiness, Success)",  
                "TEF\_Task": "Expression Orale (Section A & B)",  
                "Resource\_ID": "res\_001"  
            },  
            12: {  
                "Title": "The Final Countdown",  
                "Grammar": \["Review of Weak Points", "False Friends"\],  
                "Theme": "Review Top 10 Themes",  
                "TEF\_Task": "Full Mock Exam (All Sections)",  
                "Resource\_ID": "res\_002"  \# TV5 Simulator  
            }  
        }  
    }  
}

## **3\. The Writing Clinic Prompts (Metadata-Rich)**

**Instruction for Agent:** Use this list for the "Random Prompt" generator. The metadata field should be used to provide hints to the user or context to the AI Grader.

writing\_prompts \= \[  
    \# \--- SECTION A: FAIT DIVERS (Narrative) \---  
    {  
        "id": "A\_01",  
        "type": "Section A",  
        "topic": "The Hero Dog",  
        "prompt": "Un chien réveille sa famille et les sauve d'un incendie. Racontez.",  
        "word\_count": 80,  
        "metadata": {  
            "tense\_focus": \["Passé Composé", "Imparfait"\],  
            "key\_vocab": \["aboyer", "fumée", "pompiers", "sauver"\]  
        }  
    },  
    {  
        "id": "A\_02",  
        "type": "Section A",  
        "topic": "The Lottery Surprise",  
        "prompt": "Un homme jette son ticket de loto par erreur et le retrouve le lendemain. Racontez la suite.",  
        "word\_count": 80,  
        "metadata": {  
            "tense\_focus": \["Plus-que-parfait", "Passé Composé"\],  
            "key\_vocab": \["ticket", "poubelle", "chance", "millionnaire"\]  
        }  
    },  
    {  
        "id": "A\_03",  
        "type": "Section A",  
        "topic": "The Good Samaritan",  
        "prompt": "Une vieille dame perd son sac et un jeune homme le lui rapporte intact. Racontez l'histoire.",  
        "word\_count": 80,  
        "metadata": {  
            "tense\_focus": \["Passé Composé", "Imparfait"\],  
            "key\_vocab": \["perdre", "rapporter", "honnêteté", "remercier"\]  
        }  
    },  
      
    \# \--- SECTION B: ARGUMENTATION (Formal Letter) \---  
    {  
        "id": "B\_01",  
        "type": "Section B",  
        "topic": "Free Museums",  
        "prompt": "Vous avez lu que tous les musées devraient être gratuits. Écrivez au journal pour donner votre opinion.",  
        "word\_count": 200,  
        "metadata": {  
            "structure": "Formal Letter",  
            "grammar\_focus": \["Subjunctive", "Connectors"\],  
            "key\_arguments": \["Culture for all", "Economic cost", "Education"\]  
        }  
    },  
    {  
        "id": "B\_02",  
        "type": "Section B",  
        "topic": "Smartphones in Schools",  
        "prompt": "Un article propose d'interdire les portables au lycée. Vous réagissez.",  
        "word\_count": 200,  
        "metadata": {  
            "structure": "Formal Letter",  
            "grammar\_focus": \["Conditional (Suggestion)", "Subjunctive"\],  
            "key\_arguments": \["Concentration", "Cyberbullying", "Pedagogical tool"\]  
        }  
    },  
    {  
        "id": "B\_03",  
        "type": "Section B",  
        "topic": "Work from Home",  
        "prompt": "Votre entreprise veut rendre le télétravail obligatoire. Vous écrivez au DRH pour exprimer votre désaccord.",  
        "word\_count": 200,  
        "metadata": {  
            "structure": "Formal Letter",  
            "grammar\_focus": \["Polite refusal", "Logical connectors"\],  
            "key\_arguments": \["Social isolation", "Team spirit", "Work-life balance"\]  
        }  
    }  
\]  
