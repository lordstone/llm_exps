import argparse
import os
import time
from google import genai
from google.genai import types

from utils import print_thoughts

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")


current_mood_function = {
    "name": "get_current_mood",
    "description": "Asks the current mood from the user",
    "parameters": {
        "type": "object",
        "properties": {
            "mood": {
                "type": "string",
                "description": "The user's current mood, such as 'happy', 'sad', 'excited', etc.",
            },
        },
        "required": ["mood"],
    }
}

current_time_function = {
    "name": "get_current_time",
    "description": "Get current time from the client",
    "parameters": {
        "type": "object",
        "properties": {
        },
        "required": [],
    }
}

weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}


def get_current_mood() -> dict:
    """Gets the current mood from the user.

    Returns:
        A dictionary containing the user's mood.
    """
    mood = input("What is your current mood? (e.g., happy, sad, excited): ")
    return {"mood": mood}


def get_current_time() -> str:
    """Gets the current time from the client.

    Returns:
        A dict containing a "time" value with Time and date in the format "YYYY-MM-DD HH:MM:SS".
    """
    return {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}


client = genai.Client()


tools = types.Tool(
     function_declarations=[current_mood_function, current_time_function, weather_function],
    # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)


"""config = types.GenerateContentConfig(
    tools=[get_current_time, get_current_mood],
    )
    """



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

    contents = [
        types.Content(
            role="user", parts=[types.Part(text=prompt)]
        )
    ]

    configs = types.GenerateContentConfig(
        # tools=[tools]
    )

    if kwargs.get("thinking", False):
        print("Using thinking for the model.")
        configs.thinking_config=types.ThinkingConfig(
                include_thoughts=True
            )
        # Turn off thinking:
        # thinking_config=types.ThinkingConfig(thinking_budget=0)
        # Turn on dynamic thinking:
        # thinking_config=types.ThinkingConfig(thinking_budget=-1)
        
    if kwargs.get("tools", False):
        # configs.tools = [get_current_time, get_current_mood]
        print("Using tools for the model.")
        configs.tools = [tools]

    if kwargs.get("debug", False):
        print(f"Using model: {model}")
        print(f"Prompt: {prompt}")
        print(f"Config: {configs}")

    response = client.models.generate_content(
        model=model, contents=prompt,
        config=configs
    )
    
    # print(response.text)

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")

        # Call the function and get the result
        if function_call.name == "get_current_mood":
            result = get_current_mood()
        elif function_call.name == "get_current_time":
            result = get_current_time()
        elif function_call.name == "get_current_temperature":
            result = input(f"Enter current temperature for the location: {function_call.args}")
        else:
            raise ValueError(f"Unknown function call: {function_call.name}")

        # Create a function response part
        function_response_part = types.Part.from_function_response(
            name=function_call.name,
            response={"result": result},
        )

        # Append function call and result of the function execution to contents
        contents.append(response.candidates[0].content)
        contents.append(types.Content(role="user", parts=[function_response_part]))

        final_response = client.models.generate_content(
            model=model,
            config=configs,
            contents=contents,
        )

        if kwargs.get("thinking", False):
            print_thoughts(final_response)

        print(final_response.text)
    else:
        print("No function call found in the response.")
        
        if kwargs.get("thinking", False):
            print_thoughts(response)

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
    parser.add_argument("--thinking", action="store_true",
                        help="Enable thinking mode for the model.")
    parser.add_argument("--tools", action="store_true",
                        help="Enable tools for the model.")
    args = parser.parse_args()

    prompt = input("Enter your prompt: ")
    generate_text(prompt, model=args.model, debug=args.debug, tools=args.tools, thinking=args.thinking)
    