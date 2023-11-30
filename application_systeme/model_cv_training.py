# Définir les règles de correspondance pour les compétences
import nlp as nlp
from spacy.matcher import Matcher

competence_patterns = [
    [
    {"LOWER": {"IN": ["python", "java", "c++", "javascript", "html", "css", "sql","github", "symfony", "c","php","django","asp.net core 6","c#",".net","angular"]}},
    {"LOWER": "machine", "OP": "?"},
    {"LOWER": "learning", "OP": "?"},
    {"LOWER": "deep", "OP": "?"},
    {"LOWER": {"IN": ["data", "big", "business"]}, "OP": "?"},
    {"LOWER": {"IN": ["engineer", "developer", "scientist", "analyst"]}, "OP": "?"},
    ]
]

certification_patterns = [
    [
    {"LOWER": {"IN": ["pcap", "oca", "aws", "rhce", "rhca", "pcep", "oracle","pspm", "scrum","mta"]}},
    {"LOWER": "machine", "OP": "?"},
    {"LOWER": "learning", "OP": "?"},
    {"LOWER": "deep", "OP": "?"},
    {"LOWER": {"IN": ["data", "big", "business"]}, "OP": "?"},
    {"LOWER": {"IN": ["engineer", "developer", "scientist", "analyst"]}, "OP": "?"},
    ]
]

formation_patterns = [
    [
    {"LEMMA": {"IN": ["étude", "école", "master", "licence", "diplôme", "formation", "ingénieur"]}},
    {"LOWER": {"IN": ["en", "de", "à"]}, "OP": "?"},
    {"IS_TITLE": True, "OP": "?"},

    {"IS_DIGIT": True, "OP": "?"},
    ]
]

experience_patterns = [
    [
    {"LEMMA": {"IN": ["travailler", "emploi", "expérience", "stage", "stage", "snim", "societe", "tek-up",""]}},
    {"LOWER": {"IN": ["en", "à"]}, "OP": "?"},
    {"IS_TITLE": True, "OP": "?"},
    {"LOWER": "chez", "OP": "?"},
    {"IS_TITLE": True, "OP": "?"},
    ]
]
langages_patterns = [
    [
    {"LOWER": {"IN": ["anglais","français"]}},

]
    ]


# Définir les règles de correspondance pour les formations


# Définir les règles de correspondance pour l'expérience professionnelle


# Identifier les entités nommées pertinentes en utilisant les règles de correspondance







