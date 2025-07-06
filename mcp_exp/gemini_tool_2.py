import argparse
import os
import time
from google import genai
from google.genai import types

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")


mood_function = {
    "name": "ask_current_mood",
    "description": "Asks the current mood from the user",
    "parameters": {
        "type": "object",
        "properties": {
            "hints": {
                "type": "string",
                "description": "One or more simple words that hints about the user's current mood, such as 'happy', 'sad', 'excited', etc.",
            },
        },
        "required": ["hints"],
    },
}


def get_current_mood():
    """
    Function to get the current mood from the user.
    This function is not called directly but is used as a tool in the Gemini API.
    """
    mood = input("What is your current mood? (e.g., happy, sad, excited): ")
    return {"mood": mood}


def get_current_time():
    """
    Function to get the current mood from the user.
    This function is not called directly but is used as a tool in the Gemini API.
    """
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {"time": cur_time}


client = genai.Client()

"""
tools = types.Tool(
    # function_declarations=[mood_function],
    # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
"""

config = types.GenerateContentConfig(
    tools=[get_current_time, get_current_mood],
    )


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

    if kwargs.get("debug", False):
        print(f"Using model: {model}")
        print(f"Prompt: {prompt}")
        print(f"Config: {config}")

    contents = [
        types.Content(
            role="user", parts=[types.Part(text=prompt)]
        )
    ]

    response = client.models.generate_content(
        model=model, contents=contents,
        config=config,
    )
    
    print(response.text)

    if kwargs.get("debug", False):
        print(f"Response: {response}")


if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser(description="Generate text using Google Gemini API.")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash",
                        help="Model name to use for text generation.")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode to print additional information.")
    args = parser.parse_args()

    prompt = input("Enter your prompt: ")
    generate_text(prompt, model=args.model, debug=args.debug)
    