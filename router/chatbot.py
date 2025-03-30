import json
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from utils.intent_classifier import classify_intent
from utils.knowledge_retriever import get_disease_info

router = APIRouter()
templates = Jinja2Templates(directory="templates")

MEMORY_FILE = "memory.json"

# Ensure the JSON memory file exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)


# Function to load memory.json
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"chat_history": [], "last_disease": ""}  # Default structure

# Function to save memory.json
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def set_memory(key, value):
    memory = load_memory()
    memory[key] = value  # Update the existing key only
    save_memory(memory)

def get_memory(key):
    memory = load_memory()
    return memory.get(key, None)  # Retrieve value for the key


@router.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    
    user_input = data.get("message")

    if not user_input:
        raise HTTPException(status_code=400, detail="Invalid input: 'message' is required.")

    # Classify user intent
    intent = classify_intent(user_input)
    print("Intent:", intent)

    if intent in ["disease_info"]:

        # Extract disease info
        disease_info = get_disease_info(user_input)
        print("disease_info", disease_info)
        if disease_info:
            # Store last mentioned disease
            set_memory("last_disease", disease_info.get("name"))
            response = disease_info["symptoms"]
        else:
            response = "I'm sorry, I couldn't find information on that disease."

    elif intent == "general_info":
        response = "Maize requires warm temperatures, good soil, and proper irrigation."
    
    elif intent == "greeting":
        response = "Hello! How I can help you?"
    

    elif intent in ["cure", "treatment"]:
        disease_info = get_disease_info(user_input)
        # print("disease_info",disease_info )

        if disease_info:
            set_memory("last_disease", disease_info.get("name"))  # Retrieve treatment info
            response = disease_info['treatment']
        else:
            response = "Please mention the disease name for treatment details."
        
    elif intent == "cause":
        disease_info = get_disease_info(user_input)
        # print("disease_info",disease_info )
        
        if disease_info:
            set_memory("last_disease", disease_info.get("name"))  # Retrieve treatment info
            response = disease_info['cause']
        else:
            response = "Please mention the disease name for treatment details."

    elif intent == "prevention":
        disease_info = get_disease_info(user_input)
        # print("disease_info",disease_info )
        
        if disease_info:
            set_memory("last_disease", disease_info.get("name"))  # Retrieve treatment info
            response = disease_info['prevention']
        else:
            response = "Please mention the disease name for treatment details."

    elif intent == "about":
        disease_info = get_disease_info(user_input)
        # print("disease_info",disease_info )
        
        if disease_info:
            set_memory("last_disease", disease_info.get("name"))  # Retrieve treatment info
            response = disease_info['about']
        else:
            response = "Please mention the disease name for treatment details."

    else:
        response = "I'm sorry, I didn't understand that. Please ask about maize diseases or treatments."

    return JSONResponse({"response": response})


@router.post("/save_chat")
async def save_chat(request: Request):
    """Saves user message and bot response with timestamp in chat_history."""
    try:
        # Parse incoming JSON request body
        data = await request.json()
        user_message = data.get("user_message")
        bot_response = data.get("bot_response")

        if not user_message or not bot_response:
            raise HTTPException(status_code=400, detail="Both user_message and bot_response are required.")

        # Load existing memory
        memory = load_memory()

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append new chat message with timestamp
        memory.setdefault("chat_history", []).append({
            "timestamp": timestamp,
            "user": user_message,
            "bot": bot_response
        })

        # Save updated memory
        save_memory(memory)

        return JSONResponse(content={"message": "Chat saved successfully.", "timestamp": timestamp})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving chat: {str(e)}")

@router.post("/clear_chat")
async def clear_chat_memory():
    """Clears chat history and resets last_disease in memory.json."""
    try:
        # Load existing memory
        memory = load_memory()
        
        # Reset last_disease and optionally clear chat logs
        memory["last_disease"] = ''  # Reset stored disease

        # Save updated memory
        save_memory(memory)
        
        return JSONResponse(content={"message": "Chat history and last disease reset successfully."})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))