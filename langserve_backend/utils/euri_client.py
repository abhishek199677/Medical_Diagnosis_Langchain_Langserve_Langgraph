import requests
from dotenv import load_dotenv
import os


load_dotenv()

BASE_URL = "https://api.openai.com/v1"
           

def openai_chat_completion(messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
    
    # Get API key from environment variables
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        return "Error: OPENAI_API_KEY not found in .env file"
    
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as e:
        return f"HTTP error: {e} | Response content: {response.text}"
    except ValueError:
        return f"Invalid JSON in response: {response.text}"

    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]
    else:
        return f"Unexpected API response format: {data}"
