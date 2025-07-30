# Import necessary libraries
import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
# Set the overall page configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# --- Sidebar for Information ---
st.sidebar.title("About")
st.sidebar.info(
    "This is an interactive chatbot powered by Google's Gemini 1.5 Flash model and built with Streamlit."
)

# --- Background Setter Function ---
# This function sets the background color of the app
def set_background(color):
    # Create CSS to set the background color
    css = f'''
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {color};
    }}
    </style>
    '''
    # Apply the CSS to the app
    st.markdown(css, unsafe_allow_html=True)

# Call the function to set the background with a hardcoded color
set_background("#f0f2f6")

# --- Gemini API Configuration ---
# Configure the Gemini API with the secret key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Helper Function for Gemini ---
# This function communicates with the Gemini API
def get_gemini_response(prompt, chat_history):
    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Format the chat history for the API
    history = [
        {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
        for msg in chat_history
    ]
    # Start a chat session with the model
    chat = model.start_chat(history=history)
    # Send the user's prompt and get the response
    response = chat.send_message(prompt)
    return response.text

# --- Streamlit App ---
# Display the main title using markdown for custom styling
st.markdown('<h1 style="text-align: center; color: #1E90FF;">Interactive Gemini Chatbot</h1>', unsafe_allow_html=True)

# Define paths for local avatar images (ensure you have an 'assets' folder with these images)
user_avatar = "assets/user.png"
ai_avatar = "assets/ai.png"

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages from the chat history
for message in st.session_state.messages:
    avatar = user_avatar if message["role"] == "user" else ai_avatar
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Get user input from the chat input box
if prompt := st.chat_input("What would you like to know?"):
    # Add user's message to the history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user's message in the chat
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    # Show a spinner while waiting for the model's response
    with st.spinner("Thinking..."):
        # Get the response from the Gemini model
        response = get_gemini_response(prompt, st.session_state.messages)
        
    # Display the assistant's response in the chat
    with st.chat_message("assistant", avatar=ai_avatar):
        st.markdown(response)
    # Add the assistant's response to the history
    st.session_state.messages.append({"role": "assistant", "content": response})