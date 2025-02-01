import streamlit as st
import datetime
import json
import time
import random
import os
from cryptography.fernet import Fernet

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"
ENCRYPTION_KEY_FILE = "encryption_key.key"

# Generate Encryption Key (Only Once)
def generate_key():
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)

# Load Encryption Key
def load_key():
    return open(ENCRYPTION_KEY_FILE, "rb").read()

# Ensure Key Exists
if not os.path.exists(ENCRYPTION_KEY_FILE):
    generate_key()
encryption_key = load_key()
cipher = Fernet(encryption_key)

# Encrypt Message
def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

# Decrypt Message
def decrypt_message(encrypted_message):
    return cipher.decrypt(encrypted_message.encode()).decode()

# Welcome messages for AI
WELCOME_MESSAGES = [
    "Hello, I'm DeepSeek. How can I assist you with coding today??",
    "Ready to code and debug together?? Let's get started..",
    "Questions?? I'm here to help you."
]

# Load & Save Chat History with Encryption
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as file:
            encrypted_history = json.load(file)
            return [
                {
                    "role": msg["role"],
                    "content": decrypt_message(msg["content"]),
                    "timestamp": msg["timestamp"]
                }
                for msg in encrypted_history
            ]
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # No welcome message here; it’s handled in session_state initialization

def save_chat_history(history):
    encrypted_history = [
        {
            "role": msg["role"],
            "content": encrypt_message(msg["content"]),
            "timestamp": msg["timestamp"]
        }
        for msg in history
    ]
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(encrypted_history, file)

# Load chat history
if "message_log" not in st.session_state:
    st.session_state.message_log = load_chat_history()
    # Add welcome message only if history is empty
    if not st.session_state.message_log:
        st.session_state.message_log.append({
            "role": "ai",
            "content": random.choice(WELCOME_MESSAGES),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })

if "bubble_color_user" not in st.session_state:
    st.session_state.bubble_color_user = "#1E90FF"

if "bubble_color_ai" not in st.session_state:
    st.session_state.bubble_color_ai = "#282C34"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "deepseek-r1:1.5b"

st.markdown(f"""
    <style>
        .main {{
            background-color: rgba(0, 0, 0, 0.7); 
            border-radius: 12px;
            padding: 16px;
        }}
        .sidebar .sidebar-content {{ background-color: #161B22 !important; }}
        .chat-container {{ display: flex; flex-direction: column; }}
        .chat-avatar {{
            width: 30px; 
            height: 30px; 
            margin-right: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 16px;
            font-weight: bold;
            color: white;
        }}
        .message {{
            display: flex; 
            align-items: center; 
            margin-bottom: 15px;
            border-radius: 10px;
            padding: 10px;
        }}
        .user-message {{
            background-color: {st.session_state.bubble_color_user};
            color: white;
            align-self: flex-end;
            justify-content: flex-end;
            border-top-right-radius: 0px;
        }}
        .ai-message {{
            background-color: {st.session_state.bubble_color_ai};
            color: white;
            align-self: flex-start;
            justify-content: flex-start;
            border-top-left-radius: 0px;
        }}
        .timestamp {{ font-size: 0.8em; color: #bbbbbb; margin-top: 5px; }}
        .user-avatar {{ background-color: #1E90FF; }}
        .ai-avatar {{ background-color: #282C34; }}
    </style>
""", unsafe_allow_html=True)

# Smooth Fade-in Header
st.markdown("<h1 style='text-align: center;'>DeepSeek R1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>AI Companion</h3>", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("Select AI Model")
    model_options = ["deepseek-r1:1.5b", "deepseek-r1:7b", "mistral-7b", "llama3.3"]
    st.session_state.selected_model = st.selectbox("Choose the model you want to use", model_options, index=model_options.index(st.session_state.selected_model))

    # Chat Bubble Colors
    st.subheader("Customize Chat Bubble Colors")
    user_color = st.color_picker("User Bubble Color", st.session_state.bubble_color_user)
    ai_color = st.color_picker("AI Bubble Color", st.session_state.bubble_color_ai)
    
    if st.button("Apply Colors"):
        st.session_state.bubble_color_user = user_color
        st.session_state.bubble_color_ai = ai_color
        st.rerun()
    
    st.divider()
    
    # Clear Chat Button
    if st.button("Clear Chat"):
        st.session_state.message_log = [{"role": "ai", "content": random.choice(WELCOME_MESSAGES), "timestamp": datetime.datetime.now().strftime("%H:%M:%S")}] 
        save_chat_history(st.session_state.message_log)
        st.rerun()
    
    # Download Chat Button
    if st.button("Download Chat Log"):
        conversation_text = "\n".join([f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['content']}" for msg in st.session_state.message_log])
        st.download_button("Download Chat Log", conversation_text, file_name="chat_log.txt")

# Initialize AI Model
llm_engine = ChatOllama(model=st.session_state.selected_model, base_url="http://localhost:11434", temperature=0.3)

# System Prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solutions with strategic print statements for debugging. Always respond in English."
)

# Display Chat Messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        bubble_class = "user-message" if message["role"] == "user" else "ai-message"
        avatar_class = "user-avatar" if message["role"] == "user" else "ai-avatar"
        avatar_text = "Me" if message["role"] == "user" else "AI"
        st.markdown(f"""
            <div class="message {bubble_class}">
                <div class="chat-avatar {avatar_class}">{avatar_text}</div>
                <div>
                    <p>{message["content"]}</p>
                    <p class="timestamp">{message.get("timestamp", "")}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Chat Input & Processing
user_query = st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    try:
        response = processing_pipeline.invoke({})
    except Exception as e:
        response = f"Oops! Something went wrong: {str(e)}"
    return response

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Add User Message
    st.session_state.message_log.append({"role": "user", "content": user_query, "timestamp": current_time})

    # Show Progress Bar during AI Response Generation
    progress_bar = st.progress(0)
    for percent in range(0, 101, 10):  # Incremental loading bar
        time.sleep(0.1)  # Simulates processing delay
        progress_bar.progress(percent)
    progress_bar.empty()  # Remove the progress bar when done

    # Generate AI Response
    prompt_chain = build_prompt_chain()
    ai_response = generate_ai_response(prompt_chain)

    # Add AI Response
    st.session_state.message_log.append({"role": "ai", "content": ai_response, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})

    # Save History & Rerun
    save_chat_history(st.session_state.message_log)
    st.rerun()
