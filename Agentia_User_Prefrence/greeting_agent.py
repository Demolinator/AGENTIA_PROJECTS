import os
import re
import requests
import random
import psycopg2
from psycopg2.extras import DictCursor
from langgraph.graph import StateGraph
from langgraph.constants import START, END
from typing import TypedDict
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# PostgreSQL Initialization
def initialize_database():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        cursor_factory=DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            location TEXT,
            conversation_history TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Ensure the database and table are initialized
initialize_database()

# Function to query Gemini LLM
def query_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        if hasattr(response, "candidates") and len(response.candidates) > 0:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "I'm sorry, I couldn't generate a response at this time."
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return "An error occurred while processing your request."

# Function to get the user's location
def get_user_location() -> str:
    try:
        # Replace 'YOUR_IPINFO_API_KEY' with your actual ipinfo.io API key
        response = requests.get("https://ipinfo.io", timeout=5)
        data = response.json()
        return data.get("city", "Unknown Location")
    except Exception as e:
        print(f"Debug: Error getting location - {e}")
        return "Unknown Location"

# Function to get the weather for a given location
def get_coordinates(location: str) -> dict:
    try:
        # Simplified to use only the city name
        url = f"https://nominatim.openstreetmap.org/search?city={location}&format=json"
        headers = {"User-Agent": "YourAppName/1.0 (contact@example.com)"}  # Replace with your contact info
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = float(data[0]["lat"])
                longitude = float(data[0]["lon"])
                print(f"Debug: Found coordinates - Latitude: {latitude}, Longitude: {longitude}")
                return {"latitude": latitude, "longitude": longitude}
            else:
                print(f"Debug: No coordinates found for {location}")
                return {}
        else:
            print(f"Debug: Geocoding API returned status code {response.status_code}")
            return {}
    except Exception as e:
        print(f"Debug: Error fetching coordinates - {e}")
        return {}

WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear skies",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorms",
    96: "Thunderstorms with slight hail",
    99: "Thunderstorms with heavy hail"
}


def get_weather_for_today(location: str) -> str:
    try:
        coordinates = get_coordinates(location)
        if not coordinates:
            return f"Sorry, weather information is not available for {location}."

        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            current_weather = data.get("current_weather", {})
            temperature = current_weather.get("temperature")
            weather_code = current_weather.get("weathercode", -1)

            description = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Unknown weather condition")

            if temperature is not None:
                return f"The weather in {location} is {description} with a temperature of {temperature}°C."
            else:
                return f"Weather details are incomplete for {location}. Please try again later."
        else:
            return f"Could not fetch weather details for {location}."
    except Exception as e:
        return "Could not fetch weather details at the moment. Please try again later."


# Define the state schema
class State(TypedDict):
    message: str
    greeting_response: str
    weather_response: str
    joke_response: str
    final_response: str

# Greeting Agent Node with Gemini
def greeting_agent_function(state: State) -> State:
    message = state.get("message", "").strip()
    prompt = f"The user said: '{message}'. Generate a friendly greeting response."
    gemini_response = query_gemini(prompt)

    if gemini_response:
        state["greeting_response"] = gemini_response
    else:
        greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Hey! Need any help?"
        ]
        state["greeting_response"] = random.choice(greetings)

    return state

# Weather Agent Node
def weather_agent_function(state: State) -> State:
    message = state.get("message", "").strip().lower()
    if "weather" in message or "temperature" in message or "forecast" in message:
        location = get_user_location()
        fallback_weather_response = get_weather_for_today(location)

        prompt = (
            f"The user asked about the weather in {location}. The current weather is: {fallback_weather_response}.\n"
            f"Generate a friendly and concise response incorporating this information."
        )

        gemini_response = query_gemini(prompt)

        # Use Gemini response or fallback data
        state["weather_response"] = (
            gemini_response if gemini_response else fallback_weather_response
        )
    else:
        state["weather_response"] = "I can provide weather information if you ask specifically."
    return state

# Joke Agent Node with Gemini
def joke_agent_function(state: State) -> State:
    joke_keywords = ["joke", "funny", "laugh"]
    message = state.get("message", "").strip().lower()

    if any(keyword in message for keyword in joke_keywords):
        fallback_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!"
        ]
        fallback_joke = random.choice(fallback_jokes)

        prompt = "The user asked for a joke. Provide a lighthearted and funny joke."
        gemini_response = query_gemini(prompt)

        state["joke_response"] = gemini_response if gemini_response else fallback_joke
    else:
        state["joke_response"] = "I can tell jokes if you ask for one!"

    return state

# Persistent User Preference Agent
# Persistent User Preference Agent
class UserPreferenceAgent:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            database=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            cursor_factory=DictCursor
        )
        self.cursor = self.conn.cursor()

    def signup(self, user_id: str, name: str, password: str) -> str:
        try:
            self.cursor.execute(
                "INSERT INTO user_preferences (user_id, name, password, conversation_history) VALUES (%s, %s, %s, %s)",
                (user_id, name, password, "")
            )
            self.conn.commit()
            return f"Signup successful! Welcome, {name.capitalize()}."
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return "This user already exists. Please log in."

    def login(self, user_id: str, password: str) -> str:
        self.cursor.execute(
            "SELECT name, password FROM user_preferences WHERE user_id = %s", (user_id,)
        )
        result = self.cursor.fetchone()
        if not result:
            return "User not found. Please sign up first."
        name, stored_password = result
        if stored_password == password:
            return f"Login successful! Welcome back, {name.capitalize()}."
        return "Incorrect password. Please try again."

    def get_user_name(self, user_id: str) -> str:
        self.cursor.execute(
            "SELECT name FROM user_preferences WHERE user_id = %s", (user_id,)
        )
        result = self.cursor.fetchone()
        return result["name"] if result else None

    def update_conversation_history(self, user_id: str, message: str, response: str) -> None:
        if user_id:
            self.cursor.execute(
                "SELECT conversation_history FROM user_preferences WHERE user_id = %s", (user_id,)
            )
            result = self.cursor.fetchone()
            if result:
                updated_history = (result[0] or "") + f"User: {message}\nBot: {response}\n"
                self.cursor.execute(
                    "UPDATE user_preferences SET conversation_history = %s WHERE user_id = %s",
                    (updated_history, user_id)
                )
                self.conn.commit()

    def get_conversation_history(self, user_id: str) -> str:
        self.cursor.execute(
            "SELECT conversation_history FROM user_preferences WHERE user_id = %s", (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else "No history available."

    def close(self):
        self.cursor.close()
        self.conn.close()

# Instantiate UserPreferenceAgent
user_pref_agent = UserPreferenceAgent()

# Update the Front-End Orchestration Function
# Store a global session for simplicity
# Global session management
SESSION_USER_ID = None

SESSION_USER_ID = None


def front_end_agent_function(state: State) -> State:
    global SESSION_USER_ID
    message = state["message"].strip().lower()

    # Handle signup
    if "my name is" in message:
        name = message.split("my name is")[-1].strip()
        user_id = str(hash(name.lower()))
        SESSION_USER_ID = user_id
        response = user_pref_agent.signup(user_id, name, "default_password")
        if "successful" in response.lower():
            state["final_response"] = response
            user_pref_agent.update_conversation_history(user_id, message, response)
        return state

    # Handle login
    if "log me in" in message:
        if SESSION_USER_ID:
            user_name = user_pref_agent.get_user_name(SESSION_USER_ID)
            if user_name:
                response = f"Hi {user_name.capitalize()}! You're now logged in."
            else:
                response = "I couldn't find your account. Please sign up first."
        else:
            response = "You need to provide your name to log in. Try: 'My name is [Your Name]'."
        state["final_response"] = response
        if SESSION_USER_ID:
            user_pref_agent.update_conversation_history(SESSION_USER_ID, message, response)
        return state

    # Handle "What is my name?"
    if "what is my name" in message:
        if SESSION_USER_ID:
            user_name = user_pref_agent.get_user_name(SESSION_USER_ID)
            response = f"Your name is {user_name.capitalize()}." if user_name else "I don't have your name stored. Please sign up first."
        else:
            response = "You are not logged in. Please sign up or log in first."
        state["final_response"] = response
        if SESSION_USER_ID:
            user_pref_agent.update_conversation_history(SESSION_USER_ID, message, response)
        return state

    # Handle conversation history retrieval
    if "show my history" in message:
        if SESSION_USER_ID:
            response = user_pref_agent.get_conversation_history(SESSION_USER_ID)
        else:
            response = "No session found. Please log in first."
        state["final_response"] = response
        return state

    # Default: Let Gemini handle irrelevant queries
    gemini_response = query_gemini(
        f"The user said: '{state['message']}'. Generate a helpful and polite response."
    )
    response = gemini_response or "Sorry, I didn't understand that. Try logging in, signing up, or asking for help."
    state["final_response"] = response
    if SESSION_USER_ID:
        user_pref_agent.update_conversation_history(SESSION_USER_ID, message, response)
    return state


# Create StateGraph with the defined state schema
greeting_graph = StateGraph(state_schema=State)

# Add nodes
greeting_graph.add_node("GreetingAgent", greeting_agent_function)
greeting_graph.add_node("WeatherAgent", weather_agent_function)
greeting_graph.add_node("JokeAgent", joke_agent_function)
greeting_graph.add_node("FrontEndAgent", front_end_agent_function)

# Define the workflow
greeting_graph.add_edge(START, "GreetingAgent")  # Process greeting first
greeting_graph.add_edge("GreetingAgent", "JokeAgent")  # Route to JokeAgent
greeting_graph.add_edge("JokeAgent", "WeatherAgent")  # Route to WeatherAgent
greeting_graph.add_edge("WeatherAgent", "FrontEndAgent")  # Pass weather to front-end
greeting_graph.add_edge("FrontEndAgent", END)  # End workflow at front-end

# Compile the graph
compiled_graph = greeting_graph.compile()

# Function to run the graph
def run_greeting_agent(input_message: str) -> str:
    # Prepare initial state
    initial_state = {
        "message": input_message,
        "greeting_response": "",
        "weather_response": "",
        "joke_response": "",
        "final_response": ""
    }
    result = compiled_graph.invoke(initial_state)
    return result["final_response"]

# Test the agents
if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' or 'quit' to end the conversation.")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = run_greeting_agent(user_message)
        print(f"Chatbot: {response}")

