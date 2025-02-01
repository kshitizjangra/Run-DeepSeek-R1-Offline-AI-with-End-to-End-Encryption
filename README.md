# DeepSeek R1 - AI Companion

## Overview
DeepSeek R1 is an AI-powered coding assistant built with Streamlit. It provides an interactive chat interface to help developers with coding queries, debugging, and AI-generated solutions using locally hosted models. 

This application is designed for privacy, ensuring that all data and interactions remain entirely local, with encrypted chat history for additional security.

---

## Features
✅ Secure AI Chat with Encrypted Chat History  
✅ Locally Hosted AI Model (No External Data Transfer)  
✅ Customizable Chat Bubble Colors  
✅ AI Model Selection (DeepSeek R1, Mistral, Llama, etc.)  
✅ Smooth UI with Dynamic Elements  
✅ Downloadable Chat History  
✅ Option to Clear Chat History Instantly  

---

## Installation
### Step 1: Install Required Dependencies
Before running the application, make sure you have all necessary dependencies installed. You can install them using the following command:
```bash
pip install -r prerequisites.txt
```

### Step 2: Install and Set Up Ollama
1. **Download Ollama**: Install the Ollama app for your OS (Windows, Mac, or Linux) from [ollama.com](https://ollama.com).
2. **Download AI Models**: You can download and use any model of your choice. To download a model, use the command:
   ```bash
   ollama run "model_name"
   ```
   The first-time setup may take a few minutes.
3. **Check Installed Models**: Run the command:
   ```bash
   ollama list
   ```
   This will display all downloaded models.
4. **Delete a Model (If Needed)**: To remove a model, use:
   ```bash
   ollama delete "model_name"
   ```

---

## Running the Application
After installing dependencies and setting up Ollama, run the application using:
```bash
streamlit run app.py
```

This will launch the AI chat assistant in your browser.

---

## File Structure
```
├── app.py               # Main application script
├── chat_history.json    # Encrypted chat history (auto-generated)
├── encryption_key.key   # Encryption key file (auto-generated)
├── prerequisites.txt    # Required dependencies
└── README.md            # Documentation
```

---

## Configuration & Customization
### AI Model Selection
You can choose different AI models from the sidebar, such as:
- `deepseek-r1:1.5b`
- `deepseek-r1:7b`
- `mistral-7b`
- `llama3.3`

You are not limited to these models; you can download and use any model supported by Ollama.

### Custom Chat Bubble Colors
You can personalize the chat appearance by selecting custom colors for the user and AI message bubbles from the sidebar.

### Clearing and Downloading Chat History
- **Clear Chat**: Click the "Clear Chat" button in the sidebar to reset the conversation.
- **Download Chat Log**: Save your chat as a text file by clicking "Download Chat Log."

---

## Security & Privacy
🔒 **Local Execution**: No internet connection is needed; all data remains on your device.  
🔒 **Encrypted Chat History**: Messages are stored in `chat_history.json` using AES encryption via `cryptography`.  
🔒 **No External API Calls**: The AI model runs entirely on your local machine.

---

## Prerequisites
The `prerequisites.txt` file includes:
```txt
# For Web Framework
streamlit

# For Chat Encryption
cryptography

# For LLM & AI Model Handling
langchain_ollama
langchain_core

# Utility Libraries
watchdog  # Auto-reload for live changes (only if needed)
pygments  # Syntax highlighting (optional)
```

---

## Contributing
This project is open-source! Feel free to contribute by submitting issues or pull requests.

---

## License
This project is released under an open-source license. Feel free to use and modify it as needed!

---

## Support
If you encounter any issues, please open an issue on the GitHub repository or reach out to the community.

Happy coding! 🚀
