# Google-ADK-Experiment
Repository for learning and experimenting with Google's Agent Development Kit (ADK).

This project demonstrates a sophisticated AI agent built using the Google Agent Development Kit (ADK). This agent acts as an orchestrator, capable of handling diverse user requests by delegating tasks to specialized sub-agents and interacting with external tools. It's designed for modularity and extensibility, showcasing how to build complex conversational flows.

### ✨ Features

* Orchestrated Agent Team: A TeamOrchestrator agent (the root_agent) intelligently routes user queries to the appropriate sub-agent or handles them directly.
* Weather Information: Retrieves current weather conditions for any specified city using the WeatherAPI.com external tool.
* Dynamic Greetings: Utilizes a dedicated greeting_agent to provide friendly and customizable hellos.
* Polite Farewells: Employs a farewell_agent to gracefully end conversations.
* Modular Design: Agents and tools are organized within a Python package, promoting clean code and reusability.
* Gemini 1.5 Flash Powered: Leverages Google's powerful gemini-1.5-flash large language model for natural language understanding and generation.

### 🚀 Getting Started
Follow these steps to set up and run the agent team on your local machine.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUsername/Google-ADK-Experiment.git
   cd Google-ADK-Experiment
   ```
2. **Set up Virtual Environment:**
   
   It's highly recommended to use a virtual environment to manage project dependencies.
   ```bash
   python -m venv venv
   ```
   Then activate the virtual environment-

   On Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   On Mac:
   ```bash
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API Keys:**

   This project requires API keys for both Google Gemini models and WeatherAPI.com.

   1. **Create a .env file: In the multi tool agent of your project directory (Google-ADK-Experiment/multi_tool_agent), create a file named .env.**
   2. **Add your API keys to .env:**
      ```bash
      GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
      WEATHERAPI_API_KEY="YOUR_WEATHERAPI_API_KEY_HERE"
      ```
      * Google Gemini API Key: Obtain your key from Google AI Studio.
      * WeatherAPI.com API Key: Register and get your free API key from WeatherAPI.com.
   
