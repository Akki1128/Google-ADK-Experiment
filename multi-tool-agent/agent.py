import os
import datetime
import requests
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import Tool 

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather_api(city: str) -> dict:
    
    if not OPENWEATHER_API_KEY:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key is not configured.",
        }

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric", 
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        weather_data = response.json()

        if weather_data.get("cod") == 200:
            main = weather_data.get("main", {})
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
            temp = main.get("temp", "N/A")
            feels_like = main.get("feels_like", "N/A")
            humidity = main.get("humidity", "N/A")

            report = (
                f"The current weather in {city} is {weather_desc}. "
                f"Temperature: {temp}°C (feels like {feels_like}°C). Humidity: {humidity}%."
            )
            return {"status": "success", "report": report}
        else:
            return {
                "status": "error",
                "error_message": f"Could not retrieve weather for '{city}'. Error: {weather_data.get('message', 'Unknown error')}",
            }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Network or API error: {e}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}

def get_current_time(city: str) -> dict:
    
    timezone_map = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "milpitas": "America/Los_Angeles", 
        "san francisco": "America/Los_Angeles",
        "los angeles": "America/Los_Angeles",
        "paris": "Europe/Paris",
    }
    city_lower = city.lower()

    if city_lower not in timezone_map:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}. Try New York, London, or Tokyo.",
        }

    tz_identifier = timezone_map[city_lower]
    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error_message": f"Error getting time for {city}: {e}"}


weather_time_agent = Agent(
    name="WeatherAndTimeAgent",
    model="gemini-1.5-flash", 
    description=(
        "An agent that provides current weather reports and current time for specified cities. "
        "It uses external tools for this purpose."
    ),
    instruction=(
        "You are a helpful Weather and Time Assistant. "
        "Your sole purpose is to answer questions about the current weather and time in cities. "
        "Always use the provided `get_current_weather_api` and `get_current_time` tools to fetch information. "
        "If a city is not supported by a tool, state that fact clearly. "
        "If asked about anything other than weather or time, tell the user that you are specialized in weather and time."
    ),
    tools=[get_current_weather_api, get_current_time], 
)

greeting_agent = Agent(
    name="GreetingAgent",
    model="gemini-1.5-flash",
    description="An agent that provides friendly greetings and welcomes users.",
    instruction=(
        "You are a polite and friendly Greeting Agent. "
        "Your only task is to respond to greetings like 'hello', 'hi', 'hey', 'good morning', etc. "
        "Respond with a warm greeting and ask how you can assist them with travel-related queries. "
        "Do not try to answer complex questions or use tools. "
        "Example responses: 'Hello there! How can I assist you?', "
        "'Hi! I'm your assistant. How can I help you?'"
    ),
)

farewell_agent = Agent(
    name="FarewellAgent",
    model="gemini-1.5-flash",
    description="An agent that politely says goodbye and ends conversations.",
    instruction=(
        "You are a polite Farewell Agent. "
        "Your only task is to respond to farewells like 'bye', 'goodbye', 'see you', 'thanks for your help', 'exit', 'quit'. "
        "Respond with a warm and friendly goodbye. "
        "Example responses: 'Goodbye! Have a wonderful day!'"
    ),
)

root_agent = Agent(
    name="TeamOrchestrator",
    model="gemini-1.5-flash",
    description=(
        "A routing agent that intelligently delegates user requests to specialized sub-agents: "
        "WeatherAndTimeAgent, GreetingAgent, and FarewellAgent. "
        "It ensures the correct agent handles the query."
    ),
    instruction=(
        "You are a smart assistant that routes user requests to the most appropriate specialist agent. "
        "Your goal is to accurately determine the user's intent and invoke the correct sub-agent. "
        "1. If the user asks about the weather or current time in a city, route to `WeatherAndTimeAgent`. "
        "2. If the user expresses a greeting (e.g., 'hi', 'hello', 'good morning'), route to `GreetingAgent`. "
        "3. If the user expresses a farewell (e.g., 'bye', 'goodbye', 'exit', 'quit', 'thanks for your help'), route to `FarewellAgent`. "
        "4. For any other request that doesn't fit the above, try to answer politely that you are a specialized router and can only connect them to the weather/time, greeting, or farewell agents. Avoid using the tools for anything else."
        "Always try to route the query to one of the specific agents defined in your tools."
    ),
    tools=[weather_time_agent, greeting_agent, farewell_agent],
)