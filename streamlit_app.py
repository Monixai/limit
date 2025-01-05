import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["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"])
assistant_id = st.secrets["asst_3wno6BHmoVQ8Sgo5I4hkKLvG"]

# Page config
st.set_page_config(
    page_title="Sakura AI Assistant",
    page_icon="🌸",
    layout="wide"
)

# Custom CSS with cyberpunk theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --main-cyan: #00ffff;
        --main-purple: #9933ff;
        --main-black: #0a0a0a;
        --main-gray: #1f1f1f;
    }
    
    /* Overall page styling */
    .stApp {
        background-color: var(--main-black);
        color: white;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(45deg, var(--main-purple), var(--main-cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: var(--main-gray);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--main-cyan);
    }
    
    /* Message styling */
    .user-message {
        background-color: rgba(0, 255, 255, 0.1);
        border-left: 3px solid var(--main-cyan);
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    .assistant-message {
        background-color: rgba(153, 51, 255, 0.1);
        border-right: 3px solid var(--main-purple);
        padding: 10px;
        margin: 10px 0;
        border-radius: 10px 0 0 10px;
    }
    
    /* Input styling */
    .stTextInput input {
        background-color: var(--main-gray) !important;
        color: white !important;
        border: 1px solid var(--main-cyan) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus {
        box-shadow: 0 0 10px var(--main-cyan) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, var(--main-purple), var(--main-cyan)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        background: var(--main-black);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--main-purple), var(--main-cyan));
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# App header
st.markdown('<h1 class="main-header">Sakura AI Assistant</h1>', unsafe_allow_html=True)

# Chat interface
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        message_class = "user-message" if message["role"] == "user" else "assistant-message"
        st.markdown(f'<div class="{message_class}">{message["content"]}</div>', 
                   unsafe_allow_html=True)

# Input area
input_container = st.container()
with input_container:
    if prompt := st.text_input("Message Sakura...", key="user_input"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Send to assistant
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create run
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        # Show typing indicator
        with st.spinner("Sakura is typing..."):
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )

            # Get response
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            
            assistant_message = messages.data[0].content[0].text.value
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Rerun to update chat
        st.rerun()
