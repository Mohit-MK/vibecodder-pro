from google import genai
import os

# 1. SETUP: Put your API key inside the quotes
API_KEY = "AIzaSyAhL-qmPb8qX-rU4bHCEWoqs5liOWFIZoQ"
client = genai.Client(api_key=API_KEY)

def start_vibe():
    print("\n--- 🪐 CHROMEOS VIBE PLATFORM ---")
    
    # 2. Get your idea
    vibe = input("What do you want to build? (e.g. 'A simple calculator')\n> ")
    print("✨ AI is thinking...")

    # 3. Request the code from Gemini 3
    # We use 'gemini-3-flash-preview' for the best 2026 performance
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=f"Write a complete, working Python script for: {vibe}. Output ONLY raw code. No talk, no markdown."
    )
    
    # 4. Clean the code (removing any triple backticks)
    raw_code = response.text.replace("```python", "").replace("```", "").strip()
    
    # 5. Save it to a file
    with open("app.py", "w") as f:
        f.write(raw_code)
    
    print("✅ Done! Saved to 'app.py'.")

    # 6. Ask to run it
    confirm = input("Run it now? (y/n): ")
    if confirm.lower() == 'y':
        print("\n--- RUNNING YOUR APP ---")
        # On ChromeOS, always use python3
        os.system("python3 app.py")

if __name__ == "__main__":
    start_vibe()