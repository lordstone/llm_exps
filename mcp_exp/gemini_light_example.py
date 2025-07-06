from google import genai
from google.genai import types

# Actual function implementations
def power_disco_ball_impl(power: bool) -> dict:
    """Powers the spinning disco ball.

    Args:
        power: Whether to turn the disco ball on or off.

    Returns:
        A status dictionary indicating the current state.
    """
    return {"status": f"Disco ball powered {'on' if power else 'off'}"}

def start_music_impl(energetic: bool, loud: bool) -> dict:
    """Play some music matching the specified parameters.

    Args:
        energetic: Whether the music is energetic or not.
        loud: Whether the music is loud or not.

    Returns:
        A dictionary containing the music settings.
    """
    music_type = "energetic" if energetic else "chill"
    volume = "loud" if loud else "quiet"
    return {"music_type": music_type, "volume": volume}

def dim_lights_impl(brightness: float) -> dict:
    """Dim the lights.

    Args:
        brightness: The brightness of the lights, 0.0 is off, 1.0 is full.

    Returns:
        A dictionary containing the new brightness setting.
    """
    return {"brightness": brightness}


def mood_impl() -> dict:
    """Set the mood for the party based on user time.

    Returns:
        A dictionary containing the new mood setting.
    """
    cur_time = genai.Client().get_current_time()
    if cur_time.hour < 12:
        mood = "inspired"
    elif cur_time.hour < 18:
        mood = "excited"
    else:
        mood = "relaxed"
    return {"mood": mood}

# Configure the client
client = genai.Client()
config = types.GenerateContentConfig(
    tools=[power_disco_ball_impl, start_music_impl, dim_lights_impl, mood_impl]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Let's throw a party. How is the everything now?",
    config=config,
)

print("\nExample 2: Automatic function calling")
print(response.text)
# I've turned on the disco ball, started playing loud and energetic music, and dimmed the lights to 50% brightness. Let's get this party started!
