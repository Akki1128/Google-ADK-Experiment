import os
import requests
from typing import Optional
from google.genai import types 
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
#from google.adk.models.lite_llm import LiteLlm 
from google.adk.sessions import InMemorySessionService

load_dotenv()
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

def get_current_weather_api(city: str) -> dict:
    if not WEATHERAPI_API_KEY:
        return {
            "status": "error",
            "error_message": "WeatherAPI.com API key is not configured.",
        }

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHERAPI_API_KEY, 
        "q": city,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        weather_data = response.json()

        current_data = weather_data.get("current", {})
        location_data = weather_data.get("location", {})

        if response.status_code == 200: 
            temp_c = current_data.get("temp_c", "N/A")
            feels_like_c = current_data.get("feelslike_c", "N/A")
            humidity = current_data.get("humidity", "N/A")
            weather_condition = current_data.get("condition", {}).get("text", "N/A")
            city_name = location_data.get("name", city) 

            report = (
                f"The current weather in {city_name} is {weather_condition}. "
                f"Temperature: {temp_c}°C (feels like {feels_like_c}°C). Humidity: {humidity}%."
            )
            return {"status": "success", "report": report}
        else:
            error_message = weather_data.get("error", {}).get("message", "Unknown error")
            return {
                "status": "error",
                "error_message": f"Could not retrieve weather for '{city}'. Error: {error_message}",
            }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Network or API error: {e}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}


def say_hello(name: Optional[str] = None) -> str: 
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello there!" 
    return greeting

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."

print("Greeting and Farewell tools defined.")


# --- Greeting Agent ---
greeting_agent = None
try:
    greeting_agent = Agent(
        model = "gemini-1.5-flash",
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
    print(f"Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")
except Exception as e:
    print(f"Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}")

# --- Farewell Agent ---
farewell_agent = None
try:
    farewell_agent = Agent(
        model = "gemini-1.5-flash",
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                    "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
        tools=[say_goodbye],
    )
    print(f"Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
except Exception as e:
    print(f"Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")
    
    
root_agent = Agent(
    name="TeamOrchestrator", 
    model="gemini-1.5-flash",
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                "You have specialized sub-agents: "
                "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                "If it's a weather request, handle it yourself using 'get_weather'. "
                "For anything else, respond appropriately or state you cannot handle it.",
    tools=[get_current_weather_api], 
    sub_agents=[greeting_agent, farewell_agent]
)
