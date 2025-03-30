import spacy

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

# Define keyword-based intent categories
INTENT_KEYWORDS = {
    "disease_info": ["symptoms", "identify", "recognize", "disease", "infection", "affects"],
    "treatment": ["treatment", "cure", "remedy", "control", "management", "prevention"],
    "cause": ["cause", "reason", "origin", "why", "how it starts", "pathogen", "fungus", "bacteria", "virus"],
    "prevention": ["prevent", "avoid", "stop", "reduce risk", "protection", "crop rotation", "resistant variety", "field sanitation"],
    "general_info": ["maize farming", "grow maize", "cultivation", "climate", "conditions"],
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "how are you", "greetings"],
    "about": ["about", "explain", "describe", "details", "information", "what is", "tell me about", "help"]
}

def classify_intent(user_input: str) -> str:
    """
    Classifies user queries into predefined intent categories.
    """
    doc = nlp(user_input.lower())

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(token.text in keywords for token in doc):
            print("intent", intent)
            return intent
    
    return "unknown"  # Default intent if no match is found
