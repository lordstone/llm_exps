import os
from google import genai
from google.genai import types

from utils import print_thoughts

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")


def generate_text(model="gemini-2.5-flash", **kwargs):
    """
    Generate text using Google Gemini API via the google-generativeai library.

    Args:
        model (str): The model name to use.
        **kwargs: Additional parameters for the model.

    Returns:
        str: The generated text.
    """
    client = genai.Client()
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True
            ),
        )
    )

    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        if user_input.strip() == "debug":
            for message in chat.get_history():
                print(f'role - {message.role}',end=": ")
                print(message.parts[0].text)
            continue

        response = chat.send_message(user_input)
        print_thoughts(response)
        print(f"Response: {response.text}")


if __name__ == "__main__":
    generate_text()
