# test_api.py
import os
from dotenv import load_dotenv
from openai import OpenAI

print("--- Starting API Key Test ---")

# 1. Load the .env file
print("Loading .env file...")
load_dotenv()

# 2. Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n🔴 FAILURE: OPENAI_API_KEY not found.")
    print("   Please check your .env file. It should contain: OPENAI_API_KEY='sk-...'")
    exit()

print("   API Key found. Initializing OpenAI client...")

try:
    # 3. Try to use the key to make a simple API call
    client = OpenAI(api_key=api_key)
    
    print("   Sending a test request to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'hello'."}]
    )
    
    # 4. If we get here, it worked!
    print("\n✅ SUCCESS! Your OpenAI API key is working correctly.")
    print(f"   Response from OpenAI: {response.choices[0].message.content}")

except Exception as e:
    # 5. If it fails, print the exact error from OpenAI.
    print("\n🔴 FAILURE: The API key is invalid or has a billing issue.")
    print("--- OpenAI Error Details ---")
    print(e)
    print("----------------------------")