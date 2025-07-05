import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

def query_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
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
    # Extract and print the generated text from the response
    try:
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                text = parts[0].get("text", "")
                print(text)
            else:
                print("No parts found in the response.")
        else:
            print("No candidates found in the response.")
    except Exception as e:
        print(f"Error extracting response: {e}")