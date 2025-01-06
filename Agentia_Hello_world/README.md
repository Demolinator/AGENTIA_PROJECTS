# **Agentia Hello World: Greeting Agent Project**

Welcome to the **Agentia Hello World** project! This repository demonstrates a simple yet powerful multi-agent conversation system, focusing on natural language interactions. The project features a **Front-End Orchestration Agent**, a **Greeting Agent**, a **Weather Agent**, and a newly added **Joke Agent**, designed to showcase how agents communicate and collaborate seamlessly.

---

## **Project Overview**

This project is a foundational step into the world of multi-agent systems, where different agents work together to handle user queries. It follows best practices for modularity, reusability, and clarity, making it easy to understand and expand upon.

### **What This Project Does**
- **Front-End Orchestration Agent**:  
  Acts as the user-facing layer. It receives user messages, decides how to handle them, and consolidates responses.
  
- **Greeting Agent**:  
  A specialized agent that handles simple greetings (like "Hello," "How are you?") and responds accordingly.
  
- **Weather Agent**:  
  An agent that fetches real-time weather information based on the user's location and responds with the current temperature and weather condition.

- **Joke Agent**:  
  A newly added agent that generates humorous responses and tells jokes based on user queries.

This project is built using the **LangGraph** library, which simplifies multi-agent workflows with a graph-based approach.

---

## **Features**

### **Natural Language Processing**
- Detects greetings like "hello," "hi," "good morning," and more.
- Responds with friendly messages such as:  
  *"Hello! How can I assist you today?"*
- Provides real-time weather updates like:  
  *"The weather in Karachi is clear skies with a temperature of 30°C."*
- Tells jokes such as:  
  *"Why don't scientists trust atoms? Because they make up everything!"*
- Handles multi-step queries by consolidating responses from multiple agents.

### **Modular Design**
- Agents are modular and reusable for other projects.
- Clear separation between the **Front-End Orchestration Agent**, **Greeting Agent**, **Weather Agent**, and **Joke Agent**.

### **Advanced Orchestration**
- Supports multi-intent queries such as:  
  *"Tell me a joke and the weather."*

### **Debugging and Logging**
- Debug logs trace the flow of user messages and agent responses.

---

## **How It Works**

### **User Interaction**
1. The user enters a message (e.g., `"hello"` or `"tell me the weather"`) via the command line.

### **Message Routing**
2. The **Front-End Orchestration Agent** routes the message to the appropriate agent:
   - **Greeting Agent** for greetings.
   - **Weather Agent** for weather-related queries.
   - **Joke Agent** for humor-related queries.

### **Response Generation**
3. The respective agent processes the message and generates an appropriate response:
   - The **Greeting Agent** responds to greetings.
   - The **Weather Agent** fetches real-time weather data based on the user's location.
   - The **Joke Agent** tells a joke or responds humorously.

### **Final Reply**
4. The response is returned to the user via the **Front-End Orchestration Agent**.

---

## **Getting Started**

### **Prerequisites**
Ensure you have the following installed:
- **Python 3.8 or higher**
- **`langgraph` library**

Install the dependencies using `pip`:

```bash
pip install langgraph requests
```

## **Clone the Repository**

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/agentia-hello-world.git
cd agentia-hello-world
```

## **Usage**

Run the script and start interacting:

```bash
python greeting_agent.py
```

## **Example Interaction**

```bash
Enter your message: hello
Hello! How can I assist you today?

Enter your message: can you tell me the weather
The weather in Karachi is clear skies with a temperature of 30°C.

Enter your message: tell me a joke
Why don't scientists trust atoms? Because they make up everything!

Enter your message: tell me a joke and the weather
Why don't scientists trust atoms? Because they make up everything! The weather in Karachi is clear skies with a temperature of 30°C.
```

---

## **Project Structure**

```plaintext
.
├── greeting_agent.py        # Main script for the project
├── README.md                # Project documentation
└── requirements.txt         # Dependencies for the project
```

---

## **Key Components**

### **Front-End Orchestration Agent**
- Manages user interaction and message routing.
- Consolidates responses from specialized agents.
- Supports context-aware interactions and multi-intent queries.

### **Greeting Agent**
- Handles simple greetings and generates friendly responses.
- Provides default responses for non-greeting messages.

### **Weather Agent**
- Fetches real-time weather information based on the user's location.
- Provides weather updates like temperature and weather condition.
- Uses geocoding to retrieve location coordinates dynamically.

### **Joke Agent**
- Generates humorous responses based on user input.
- Can combine jokes with other queries (e.g., weather jokes).

### **LangGraph**
- A graph-based library that simplifies multi-agent workflows.

---

## **Testing and Validation**

### **Manual Testing**
- Run the script, input messages, and verify the responses.

### **Debug Logs**
- Debugging logs are included to trace the flow of messages between agents.
