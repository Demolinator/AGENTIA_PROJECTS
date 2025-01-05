from langgraph.graph import StateGraph
from langgraph.constants import START, END
from typing import TypedDict
import re

# Define the state schema
class State(TypedDict):
    message: str
    greeting_response: str
    final_response: str


# Greeting Agent Node
def greeting_agent_function(state: State) -> State:
    # Expanded list of greetings
    greetings = [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "how are you", "greetings", "salutations", "what's up", "howdy"
    ]
    message = state.get("message", "").strip().lower()

    # Create a regex pattern to match any greeting, case-insensitive
    greeting_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, greetings)) + r')\b', re.IGNORECASE)

    # Search for the pattern in the message
    if greeting_pattern.search(message):
        state["greeting_response"] = "Hello! How can I assist you today?"
    else:
        state["greeting_response"] = "I only handle greetings right now."
    return state


# Front-End Orchestration Node
def front_end_agent_function(state: State) -> State:
    greeting_response = state.get("greeting_response")
    if greeting_response:
        state["final_response"] = greeting_response
    else:
        state["final_response"] = "I can only handle greetings for now!"
    return state

# Create StateGraph with the defined state schema
greeting_graph = StateGraph(state_schema=State)

# Add nodes
greeting_graph.add_node("GreetingAgent", greeting_agent_function)
greeting_graph.add_node("FrontEndAgent", front_end_agent_function)

# Define the workflow
greeting_graph.add_edge(START, "FrontEndAgent")  # Set entry point
greeting_graph.add_edge("FrontEndAgent", "GreetingAgent")
greeting_graph.add_edge("GreetingAgent", END)  # Set end point

# Compile the graph
compiled_graph = greeting_graph.compile()

# Function to run the graph
def run_greeting_agent(input_message: str) -> str:
    result = compiled_graph.invoke(
        {"message": input_message}
    )
    return result["final_response"]

# Test the agents
if __name__ == "__main__":
    user_message = input("Enter your message: ")
    response = run_greeting_agent(user_message)
    print(response)
