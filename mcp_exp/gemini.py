import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

def generate_text(prompt, model="gemini-2.5-flash", **kwargs):
    """
    Generate text using Google Gemini API via the google-generativeai library.

    Args:
        prompt (str): The input prompt for the model.
        model (str): The model name to use.
        **kwargs: Additional parameters for the model.

    Returns:
        str: The generated text.
    """
    client = genai.Client()
    response = client.models.generate_content(
        model=model, contents=prompt
    )
    print(response.text)

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    generate_text(prompt)
    