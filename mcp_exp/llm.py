import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

def query_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    result = query_gemini(prompt)
    print(result)