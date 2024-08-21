from dotenv import load_dotenv
import google.generativeai as genai
import os
import streamlit as st

load_dotenv()

# Custom CSS styles
st.markdown("""
    <style>
        /* Set background color */
        body {
            background-color: #f0f2f6;
        }
        /* Set title style */
        .stMarkdown h1 {
            color: #3d5a80;
            font-family: 'Arial', sans-serif;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Style the input box */
        .stTextInput input {
            border-radius: 10px;
            border: 2px solid #3d5a80;
            padding: 10px;
            width: 100%;
        }
        /* Style the buttons */
        .stButton button {
            background-color: #3d5a80;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #98c1d9;
        }
        /* Chat message styles */
        .chat-user {
            color: #293241;
            font-weight: bold;
        }
        .chat-message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
            background-color: #e0fbfc;
            font-family: 'Verdana', sans-serif;
            font-size: 1em;
        }
        .chat-bot {
            color: #ee6c4d;
            font-weight: bold;
        }
        .chat-response {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f0f2f6;
            font-family: 'Verdana', sans-serif;
            font-size: 1em;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Viswanath's CHATBOT🤖")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")
id = 0

# Initialize messages and id
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "id" not in st.session_state:
    st.session_state["id"] = 1  # Start the ID at 1 for user and bot interactions

# Chat model
chat = model.start_chat(history=[])

# Function to show the history
def show_history():
    st.write("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        if msg["user"] == "You":
            st.write(f"<div class='chat-user'>You:</div><div class='chat-message'>{msg['message']}</div>", unsafe_allow_html=True)
        else:
            st.write(f"<div class='chat-bot'>Bot:</div><div class='chat-response'>{msg['message']}</div>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)

def main():
    st.write("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Always display the initial assistant message
    st.write("<div class='chat-bot'>Bot:</div><div class='chat-response'>Hello Viswanath👋, How can I assist you today?</div>", unsafe_allow_html=True)

    user_message = st.text_input("Enter your message:")
    if st.button("Send ➤"):
        id = st.session_state["id"] + 1
        st.session_state["id"] += 1

        # Storing message from the user
        st.session_state["messages"].append(
            {"id": id, "user": "You", "message": user_message}
        )
        response = chat.send_message(user_message)

        # Storing reply from the bot
        st.session_state["messages"].append(
            {"id": id + 1, "user": "Bot", "message": response.text}
        )
        st.write(f"<div class='chat-bot'>Bot:</div><div class='chat-response'>{response.text}</div>", unsafe_allow_html=True)
    
    if st.button("History⏳"):
        show_history()
    st.write("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
