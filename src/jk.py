import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found. Check your .env file.")
else:
    print(f"✅ Key found: {api_key[:5]}... Attempting to list models...\n")
    genai.configure(api_key=api_key)
    
    try:
        found_any = False
        for m in genai.list_models():
            # Only show models that can generate content (chat models)
            if 'generateContent' in m.supported_generation_methods:
                print(f"AVAILABLE MODEL: {m.name}")
                found_any = True
        
        if not found_any:
            print("⚠️ No chat models found. Your API Key might be restricted or invalid.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")