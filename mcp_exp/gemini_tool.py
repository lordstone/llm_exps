import os
from google import genai
from google.genai import types

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")


mood_function = {
    "name": "get_current_mood",
    "description": "Gets the current mood from the user",
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

client = genai.Client()
tools = types.Tool(function_declarations=[mood_function])
config = types.GenerateContentConfig(tools=[tools])


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

    response = client.models.generate_content(
        model=model, contents=contents,
        config=config,
    )
    
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        
        # Ask about user's real mood.
        user_mood = input("What is your real current mood? (e.g., happy, sad, excited): ")
        
        # Create a function response part
        function_response_part = types.Part.from_function_response(
            name=function_call.name,
            response={"result": user_mood},
        )

        # Append function call and result of the function execution to contents
        contents.append(response.candidates[0].content) # Append the content from the model's response.
        contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=contents,
        )

        print(final_response.text)
        
    else:
        print("No function call found in the response.")
        print(response.text)

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    generate_text(prompt)
    