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
    greetings = [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "how are you", "greetings", "salutations", "what's up", "howdy"
    ]
    message = state.get("message", "").strip().lower()

    print(f"Debug: Received message = '{message}'")

    greeting_pattern = re.compile(r'(?:' + '|'.join(map(re.escape, greetings)) + r')', re.IGNORECASE)

    if greeting_pattern.search(message):
        print("Debug: Greeting detected!")
        state["greeting_response"] = "Hello! How can I assist you today?"
    else:
        print("Debug: No greeting detected.")
        state["greeting_response"] = "I only handle greetings right now."
    return state

# Front-End Orchestration Node
def front_end_agent_function(state: State) -> State:
    print(f"Debug: Received state in FrontEndAgent = {state}")

    # Ensure greeting_response is updated before final_response
    if "greeting_response" in state and state["greeting_response"]:
        state["final_response"] = state["greeting_response"]
        print("Debug: Final response updated with greeting_response!")
    else:
        state["final_response"] = "I can only handle greetings for now!"
        print("Debug: Final response set to default message.")
    return state

# Create StateGraph with the defined state schema
greeting_graph = StateGraph(state_schema=State)

# Add nodes
greeting_graph.add_node("GreetingAgent", greeting_agent_function)
greeting_graph.add_node("FrontEndAgent", front_end_agent_function)

# Define the workflow
greeting_graph.add_edge(START, "GreetingAgent")  # Process greeting first
greeting_graph.add_edge("GreetingAgent", "FrontEndAgent")  # Pass greeting to front-end
greeting_graph.add_edge("FrontEndAgent", END)  # End workflow at front-end

# Compile the graph
compiled_graph = greeting_graph.compile()

# Function to run the graph
def run_greeting_agent(input_message: str) -> str:
    # Prepare initial state
    initial_state = {"message": input_message, "greeting_response": "", "final_response": ""}
    result = compiled_graph.invoke(initial_state)
    return result["final_response"]

# Test the agents
if __name__ == "__main__":
    user_message = input("Enter your message: ")
    response = run_greeting_agent(user_message)
    print(response)
