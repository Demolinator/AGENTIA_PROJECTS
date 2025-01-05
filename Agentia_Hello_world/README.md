# **Agentia Hello World: Greeting Agent Project**

Welcome to the **Agentia Hello World** project! This repository demonstrates a simple yet powerful multi-agent conversation system, focusing on natural language interactions. The project features a **Front-End Orchestration Agent** and a **Greeting Agent**, designed to showcase how agents communicate and collaborate seamlessly.

---

## **Project Overview**

This project is a foundational step into the world of multi-agent systems, where different agents work together to handle user queries. It follows best practices for modularity, reusability, and clarity, making it easy to understand and expand upon.

### **What This Project Does**
- **Front-End Orchestration Agent**:  
  Acts as the user-facing layer. It receives user messages, decides how to handle them, and consolidates responses.
  
- **Greeting Agent**:  
  A specialized agent that handles simple greetings (like "Hello," "How are you?") and responds accordingly.

This project is built using the **LangGraph** library, which simplifies multi-agent workflows with a graph-based approach.

---

## **Features**

### **Natural Language Processing**
- Detects greetings like "hello," "hi," "good morning," and more.
- Responds with friendly messages such as:  
  *"Hello! How can I assist you today?"*
- Provides default responses for unsupported queries:  
  *"I only handle greetings right now."*

### **Modular Design**
- Agents are modular and reusable for other projects.
- Clear separation between the **Front-End Orchestration Agent** and **Greeting Agent**.

### **Debugging and Logging**
- Debug logs trace the flow of user messages and agent responses.

---

## **How It Works**

### **User Interaction**
1. The user enters a message (e.g., `"hello"`) via the command line.

### **Message Routing**
2. The **Front-End Orchestration Agent** routes the message to the **Greeting Agent** if it detects a greeting.

### **Response Generation**
3. The **Greeting Agent** processes the message, identifies if it’s a greeting, and generates an appropriate response.

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
pip install langgraph
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

Enter your message: how are you
Hello! How can I assist you today?

Enter your message: tell me a joke
I only handle greetings right now.
```

## **Project Structure**
```plaintext
.
├── greeting_agent.py        # Main script for the project
├── README.md                # Project documentation
└── requirements.txt         # Dependencies for the project
```

## **Key Components**

### **Front-End Orchestration Agent**
- Manages user interaction and message routing.
- Consolidates responses from specialized agents.

### **Greeting Agent**
- Handles simple greetings and generates friendly responses.
- Provides default responses for non-greeting messages.

### **LangGraph**
- A graph-based library that simplifies multi-agent workflows.

---

## **Testing and Validation**

### **Manual Testing**
- Run the script, input messages, and verify the responses.

### **Debug Logs**
- Debugging logs are included to trace the flow of messages between agents.
