import json

# Load knowledge base from JSON file
with open("knowledge_base/maize_diseases.json", "r") as f:
    knowledge_base = json.load(f)

def get_disease_info(disease_name):
    
    # Load disease database
    with open("knowledge_base/maize_diseases.json", "r") as f:
        diseases = json.load(f)
        print("disease", diseases)

    for disease in diseases:
        print(disease_name.lower())
        print(disease.get("name", "").lower())
        if isinstance(disease, dict) and disease.get("name", "").lower() in disease_name.lower():
            print("new")
            return {  # Always return a dictionary
                "name": disease["name"],
                "symptoms": disease["symptoms"],
                "treatment": disease["treatment"],
                "cause": disease['cause'],
                "prevention": disease['prevention'],
                "about": disease['about']
            }
        
    from router.chatbot import get_memory
    
    last_disease = get_memory("last_disease")
    print("last_disease", last_disease)
    for disease in diseases:
        if isinstance(disease, dict) and last_disease.lower() in disease.get("name", "").lower():
            print("hello")
            return {  # Always return a dictionary
                "name": disease["name"],
                "symptoms": disease["symptoms"],
                "treatment": disease["treatment"],
                "cause": disease['cause'],
                "prevention": disease['prevention'],
                "about": disease['about']
            }

    return None