"""
Test script to check available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Checking available Gemini models...\n")

try:
    models = genai.list_models()
    
    print("✅ Available models that support generateContent:\n")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"   • {model.name}")
            print(f"     Display name: {model.display_name}")
            print(f"     Description: {model.description[:100]}...")
            print()
    
    print("\n💡 Recommendation: Use one of the models listed above")
    print("   Most common: 'models/gemini-1.5-flash' or 'models/gemini-1.5-pro'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📝 Note: Make sure your API key is valid")
